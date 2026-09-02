import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "namecards.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    existing_cols = {row["name"] for row in conn.execute("PRAGMA table_info(cards)")}
    if "extra_images" not in existing_cols:
        conn.execute("ALTER TABLE cards ADD COLUMN extra_images TEXT")
    if "standard_category" not in existing_cols:
        conn.execute("ALTER TABLE cards ADD COLUMN standard_category TEXT")
    if "bni_status" not in existing_cols:
        conn.execute("ALTER TABLE cards ADD COLUMN bni_status TEXT DEFAULT 'unknown'")
    if "bni_note" not in existing_cols:
        conn.execute("ALTER TABLE cards ADD COLUMN bni_note TEXT")
    if "source_guest_id" not in existing_cols:
        conn.execute("ALTER TABLE cards ADD COLUMN source_guest_id INTEGER REFERENCES guests(id)")
    if "uploaded_by" not in existing_cols:
        conn.execute("ALTER TABLE cards ADD COLUMN uploaded_by TEXT")
    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_cards_source_guest_id "
        "ON cards(source_guest_id) WHERE source_guest_id IS NOT NULL"
    )
    existing_team_cols = {row["name"] for row in conn.execute("PRAGMA table_info(team_members)")}
    if "status" not in existing_team_cols:
        # 既有帳號(教練手動建立)一律視為approved，不受新審核流程影響
        conn.execute("ALTER TABLE team_members ADD COLUMN status TEXT DEFAULT 'approved'")
    if "applied_at" not in existing_team_cols:
        conn.execute("ALTER TABLE team_members ADD COLUMN applied_at TEXT")
    conn.commit()
    conn.close()


def already_processed(conn: sqlite3.Connection, image_filename: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM cards WHERE image_filename = ?", (image_filename,)
    ).fetchone()
    return row is not None


def insert_split_marker(conn: sqlite3.Connection, image_filename: str) -> int:
    """一張照片被偵測出含多張名片、已裁切成獨立圖片後，原始合照仍要留一筆佔位
    記錄(避免下次掃描重複偵測裁切)，但它不是真實名片，status='split'讓首頁
    搜尋結果排除顯示，不會誤導成「辨識失敗」。"""
    cur = conn.execute(
        "INSERT INTO cards (image_filename, status) VALUES (?, 'split')", (image_filename,)
    )
    conn.commit()
    return cur.lastrowid


def insert_card_pending(conn: sqlite3.Connection, image_filename: str, uploaded_by: str = None) -> int:
    """上傳當下先佔位存檔名，欄位皆空、狀態pending，實際辨識交給背景worker慢慢處理"""
    cur = conn.execute(
        "INSERT INTO cards (image_filename, status, uploaded_by) VALUES (?, 'pending', ?)",
        (image_filename, uploaded_by),
    )
    conn.commit()
    return cur.lastrowid


def list_pending_cards(conn: sqlite3.Connection, limit: int = 20):
    return conn.execute(
        "SELECT * FROM cards WHERE status = 'pending' ORDER BY id LIMIT ?", (limit,)
    ).fetchall()


def claim_for_processing(conn: sqlite3.Connection, card_id: int) -> bool:
    """搶下這筆pending記錄要開始處理，避免多個背景worker並行搶同一筆。回傳是否搶成功。"""
    cur = conn.execute(
        "UPDATE cards SET status = 'processing' WHERE id = ? AND status = 'pending'", (card_id,)
    )
    conn.commit()
    return cur.rowcount > 0


def update_card_after_extraction(conn: sqlite3.Connection, card_id: int, fields: dict) -> None:
    """背景worker辨識完成後，把pending/processing記錄補上實際內容"""
    if "_error" in fields:
        conn.execute(
            "UPDATE cards SET status = 'failed', raw_response = ? WHERE id = ?",
            (fields.get("_raw", ""), card_id),
        )
        conn.commit()
        return
    keywords = fields.get("keywords") or []
    conn.execute(
        """UPDATE cards SET name=?, title=?, company=?, mobile=?, landline=?, email=?,
           line_id=?, website=?, address=?, tagline=?, category=?, standard_category=?,
           keywords=?, confidence_notes=?, raw_response=?, status=? WHERE id=?""",
        (
            fields.get("name"), fields.get("title"), fields.get("company"),
            fields.get("mobile"), fields.get("landline"), fields.get("email"),
            fields.get("line_id"), fields.get("website"), fields.get("address"),
            fields.get("tagline"), fields.get("category"), fields.get("standard_category"),
            json.dumps(keywords, ensure_ascii=False), fields.get("confidence_notes"),
            json.dumps(fields, ensure_ascii=False),
            "needs_review" if fields.get("confidence_notes") else "ok",
            card_id,
        ),
    )
    conn.commit()


def delete_card(conn: sqlite3.Connection, card_id: int) -> None:
    """刪除名片，連同關聯的產業鏈角色/跟進紀錄一併清掉，不留孤兒資料"""
    follow_up = conn.execute("SELECT id FROM follow_ups WHERE card_id = ?", (card_id,)).fetchone()
    if follow_up:
        conn.execute("DELETE FROM follow_up_logs WHERE follow_up_id = ?", (follow_up["id"],))
        conn.execute("DELETE FROM follow_ups WHERE id = ?", (follow_up["id"],))
    conn.execute("DELETE FROM chain_members WHERE card_id = ?", (card_id,))
    conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()


def update_card_manual(conn: sqlite3.Connection, card_id: int, fields: dict) -> None:
    """團隊成員手動編輯修正AI辨識錯誤的欄位"""
    keywords = fields.get("keywords")
    conn.execute(
        """UPDATE cards SET name=?, title=?, company=?, mobile=?, landline=?, email=?,
           line_id=?, website=?, address=?, tagline=?, category=?, standard_category=?,
           keywords=?, status=? WHERE id=?""",
        (
            fields.get("name"), fields.get("title"), fields.get("company"),
            fields.get("mobile"), fields.get("landline"), fields.get("email"),
            fields.get("line_id"), fields.get("website"), fields.get("address"),
            fields.get("tagline"), fields.get("category"), fields.get("standard_category"),
            json.dumps(keywords, ensure_ascii=False) if keywords is not None else None,
            "ok",
            card_id,
        ),
    )
    conn.commit()


def insert_card(conn: sqlite3.Connection, image_filename: str, fields: dict) -> int:
    if "_error" in fields:
        cur = conn.execute(
            "INSERT INTO cards (image_filename, status, raw_response) VALUES (?, 'failed', ?)",
            (image_filename, fields.get("_raw", "")),
        )
        conn.commit()
        return cur.lastrowid

    keywords = fields.get("keywords") or []
    cur = conn.execute(
        """INSERT INTO cards
           (image_filename, name, title, company, mobile, landline, email,
            line_id, website, address, tagline, category, standard_category, keywords,
            confidence_notes, raw_response, status)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            image_filename,
            fields.get("name"),
            fields.get("title"),
            fields.get("company"),
            fields.get("mobile"),
            fields.get("landline"),
            fields.get("email"),
            fields.get("line_id"),
            fields.get("website"),
            fields.get("address"),
            fields.get("tagline"),
            fields.get("category"),
            fields.get("standard_category"),
            json.dumps(keywords, ensure_ascii=False),
            fields.get("confidence_notes"),
            json.dumps(fields, ensure_ascii=False),
            "needs_review" if fields.get("confidence_notes") else "ok",
        ),
    )
    conn.commit()
    return cur.lastrowid


# ---------- 產業鏈 ----------

def create_chain(conn: sqlite3.Connection, name: str, core_theme: str = "") -> int:
    cur = conn.execute(
        "INSERT INTO industry_chains (name, core_theme) VALUES (?, ?)", (name, core_theme)
    )
    conn.commit()
    return cur.lastrowid


def find_chain_by_name(conn: sqlite3.Connection, name: str):
    return conn.execute(
        "SELECT * FROM industry_chains WHERE name = ?", (name,)
    ).fetchone()


def add_chain_member(
    conn: sqlite3.Connection, chain_id: int, card_id: int | None, role_name: str,
    is_gap: bool = False, match_reason: str = "",
) -> int:
    cur = conn.execute(
        """INSERT INTO chain_members (chain_id, card_id, role_name, is_gap, match_reason)
           VALUES (?, ?, ?, ?, ?)""",
        (chain_id, card_id, role_name, 1 if is_gap else 0, match_reason),
    )
    conn.commit()
    return cur.lastrowid


def list_chains_with_members(conn: sqlite3.Connection):
    """回傳每條產業鏈+其所有角色位置(含已補位名片基本資料/待補位缺口)"""
    chains = conn.execute("SELECT * FROM industry_chains ORDER BY id").fetchall()
    result = []
    for chain in chains:
        members = conn.execute(
            """SELECT cm.id, cm.chain_id, cm.card_id, cm.role_name, cm.is_gap, cm.match_reason,
                      c.name AS card_name, c.company AS card_company, c.mobile AS card_mobile,
                      c.bni_status AS card_bni_status, c.bni_note AS card_bni_note
               FROM chain_members cm
               LEFT JOIN cards c ON c.id = cm.card_id
               WHERE cm.chain_id = ? ORDER BY cm.id""",
            (chain["id"],),
        ).fetchall()
        result.append({"chain": chain, "members": members})
    return result


def update_card_bni_status(conn: sqlite3.Connection, card_id: int, bni_status: str, bni_note: str = "") -> None:
    """標記這張名片(已經有真實聯絡資料的人)的BNI會員狀態：unknown(未確認)/
    bni_member(已是BNI會員)/not_bni(確定非BNI會員，真正的招募目標)。
    只套用在已上傳的真實名片上，不套用在AI建議的抽象待招募角色(教練親定：
    沒有聯絡方式的缺口，標示會員與否沒有實際用途)。"""
    conn.execute(
        "UPDATE cards SET bni_status = ?, bni_note = ? WHERE id = ?",
        (bni_status, bni_note or None, card_id),
    )
    conn.commit()


def card_already_in_chain(conn: sqlite3.Connection, chain_id: int, card_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM chain_members WHERE chain_id = ? AND card_id = ?", (chain_id, card_id)
    ).fetchone()
    return row is not None


# ---------- 團隊成員與跟進紀錄 ----------

DEFAULT_APPLICANT_PASSWORD = "88888"  # 教練拍板：自助申請帳號統一預設密碼


def get_team_member(conn: sqlite3.Connection, username: str):
    return conn.execute(
        "SELECT * FROM team_members WHERE username = ?", (username,)
    ).fetchone()


def apply_team_member(conn: sqlite3.Connection, mobile: str, display_name: str) -> str:
    """自助申請帳號(姓名+行動電話)，密碼統一預設88888，狀態待審核。
    回傳 'created'(新申請) / 'reapplied'(原本rejected重新申請) / 'exists'(已是pending或approved)。"""
    from werkzeug.security import generate_password_hash

    existing = get_team_member(conn, mobile)
    if existing is None:
        conn.execute(
            """INSERT INTO team_members (username, password_hash, display_name, status, applied_at)
               VALUES (?, ?, ?, 'pending', datetime('now'))""",
            (mobile, generate_password_hash(DEFAULT_APPLICANT_PASSWORD), display_name),
        )
        conn.commit()
        return "created"
    if existing["status"] == "rejected":
        conn.execute(
            """UPDATE team_members SET status = 'pending', display_name = ?,
               applied_at = datetime('now') WHERE username = ?""",
            (display_name, mobile),
        )
        conn.commit()
        return "reapplied"
    return "exists"


def list_team_members_by_status(conn: sqlite3.Connection, status: str):
    return conn.execute(
        "SELECT * FROM team_members WHERE status = ? ORDER BY applied_at DESC", (status,)
    ).fetchall()


def set_team_member_status(conn: sqlite3.Connection, member_id: int, status: str) -> None:
    conn.execute("UPDATE team_members SET status = ? WHERE id = ?", (status, member_id))
    conn.commit()


def get_or_create_follow_up(conn: sqlite3.Connection, card_id: int):
    row = conn.execute("SELECT * FROM follow_ups WHERE card_id = ?", (card_id,)).fetchone()
    if row:
        return row
    conn.execute(
        "INSERT INTO follow_ups (card_id, stage) VALUES (?, '待邀約')", (card_id,)
    )
    conn.commit()
    return conn.execute("SELECT * FROM follow_ups WHERE card_id = ?", (card_id,)).fetchone()


def update_follow_up_stage(conn: sqlite3.Connection, card_id: int, stage: str, assigned_to: str = "") -> None:
    conn.execute(
        """UPDATE follow_ups SET stage = ?, assigned_to = ?, updated_at = datetime('now', 'localtime')
           WHERE card_id = ?""",
        (stage, assigned_to, card_id),
    )
    conn.commit()


def add_follow_up_log(conn: sqlite3.Connection, follow_up_id: int, channel: str, content: str, logged_by: str) -> None:
    conn.execute(
        """INSERT INTO follow_up_logs (follow_up_id, channel, content, logged_by)
           VALUES (?, ?, ?, ?)""",
        (follow_up_id, channel, content, logged_by),
    )
    conn.commit()


def list_follow_up_logs(conn: sqlite3.Connection, follow_up_id: int):
    return conn.execute(
        "SELECT * FROM follow_up_logs WHERE follow_up_id = ? ORDER BY contacted_at DESC",
        (follow_up_id,),
    ).fetchall()
