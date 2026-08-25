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
    conn.commit()
    conn.close()


def already_processed(conn: sqlite3.Connection, image_filename: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM cards WHERE image_filename = ?", (image_filename,)
    ).fetchone()
    return row is not None


def insert_card_pending(conn: sqlite3.Connection, image_filename: str) -> int:
    """上傳當下先佔位存檔名，欄位皆空、狀態pending，實際辨識交給背景worker慢慢處理"""
    cur = conn.execute(
        "INSERT INTO cards (image_filename, status) VALUES (?, 'pending')", (image_filename,)
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
            """SELECT cm.*, c.name AS card_name, c.company AS card_company, c.mobile AS card_mobile
               FROM chain_members cm
               LEFT JOIN cards c ON c.id = cm.card_id
               WHERE cm.chain_id = ? ORDER BY cm.id""",
            (chain["id"],),
        ).fetchall()
        result.append({"chain": chain, "members": members})
    return result


def card_already_in_chain(conn: sqlite3.Connection, chain_id: int, card_id: int) -> bool:
    row = conn.execute(
        "SELECT 1 FROM chain_members WHERE chain_id = ? AND card_id = ?", (chain_id, card_id)
    ).fetchone()
    return row is not None


# ---------- 團隊成員與跟進紀錄 ----------

def get_team_member(conn: sqlite3.Connection, username: str):
    return conn.execute(
        "SELECT * FROM team_members WHERE username = ?", (username,)
    ).fetchone()


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
