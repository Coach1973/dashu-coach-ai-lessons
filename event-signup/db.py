import os
import re
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "event.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_conn()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    existing_cols = {row["name"] for row in conn.execute("PRAGMA table_info(attendees)")}
    if "line_user_id" not in existing_cols:
        conn.execute("ALTER TABLE attendees ADD COLUMN line_user_id TEXT")
    event_cols = {row["name"] for row in conn.execute("PRAGMA table_info(events)")}
    if "is_current" not in event_cols:
        conn.execute("ALTER TABLE events ADD COLUMN is_current INTEGER NOT NULL DEFAULT 0")
    todo_cols = {row["name"] for row in conn.execute("PRAGMA table_info(todos)")}
    if "reminder_cron_id" not in todo_cols:
        conn.execute("ALTER TABLE todos ADD COLUMN reminder_cron_id TEXT")
    conn.commit()
    conn.close()


def get_routing_mode(conn: sqlite3.Connection) -> str:
    """回傳 'auto' 或 'manual'。預設 auto（沒設定過就是自動）。"""
    row = conn.execute("SELECT value FROM app_settings WHERE key = 'routing_mode'").fetchone()
    return row["value"] if row else "auto"


def set_routing_mode(conn: sqlite3.Connection, mode: str) -> None:
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES ('routing_mode', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (mode,),
    )
    conn.commit()


def get_current_event(conn: sqlite3.Connection):
    """/checkin 實際導去哪一場，依 routing_mode 決定：
    auto   → 自動抓「日期最接近、還沒過期」的那場；同一天有多場時，用 start_time 挑目前時間點該去的那場
             （已開始的場次裡選最晚開始的那個；若都還沒開始，選當天最早那場）；
             全部過期則退回最近一場已過期的活動。
    manual → 照後台手動指定的 is_current 那筆（跟原本行為一樣）。"""
    if get_routing_mode(conn) == "manual":
        return conn.execute("SELECT * FROM events WHERE is_current = 1 LIMIT 1").fetchone()

    target_date_row = conn.execute(
        "SELECT event_date FROM events WHERE event_date >= date('now', 'localtime') "
        "ORDER BY event_date ASC LIMIT 1"
    ).fetchone()
    if target_date_row:
        same_day = conn.execute(
            "SELECT * FROM events WHERE event_date = ? ORDER BY start_time ASC",
            (target_date_row["event_date"],),
        ).fetchall()
        if len(same_day) <= 1:
            return same_day[0] if same_day else None
        now_hm = datetime.now().strftime("%H:%M")
        started = [e for e in same_day if e["start_time"] and e["start_time"] <= now_hm]
        return started[-1] if started else same_day[0]

    return conn.execute(
        "SELECT * FROM events WHERE event_date < date('now', 'localtime') "
        "ORDER BY event_date DESC LIMIT 1"
    ).fetchone()


def get_slides_mode(conn: sqlite3.Connection) -> str:
    row = conn.execute("SELECT value FROM app_settings WHERE key = 'slides_mode'").fetchone()
    return row["value"] if row else "auto"


def set_slides_mode(conn: sqlite3.Connection, mode: str) -> None:
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES ('slides_mode', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (mode,),
    )
    conn.commit()


def get_manual_slide_file(conn: sqlite3.Connection) -> str | None:
    row = conn.execute("SELECT value FROM app_settings WHERE key = 'slides_manual_file'").fetchone()
    return row["value"] if row else None


def set_manual_slide_file(conn: sqlite3.Connection, filename: str) -> None:
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES ('slides_manual_file', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (filename,),
    )
    conn.commit()


def set_current_event(conn: sqlite3.Connection, slug: str) -> bool:
    """手動把固定QR立牌(/checkin)導向的活動切換成slug這場，並切成manual模式
    （手動選一次之後就不會被自動切換蓋掉，除非之後又按「恢復自動切換」）。
    回傳False表示找不到這個活動。"""
    row = conn.execute("SELECT id FROM events WHERE slug = ?", (slug,)).fetchone()
    if not row:
        return False
    conn.execute("UPDATE events SET is_current = 0")
    conn.execute("UPDATE events SET is_current = 1 WHERE id = ?", (row["id"],))
    set_routing_mode(conn, "manual")
    conn.commit()
    return True


def match_line_identity(conn: sqlite3.Connection, name: str, line_user_id: str) -> bool:
    """來賓在LINE傳「我是OOO，剛報名了XXX」時呼叫。用姓名比對最近一筆未綁定的報名記錄。
    回傳 True 表示比對成功並已存入 line_user_id。"""
    row = conn.execute(
        """SELECT id FROM attendees WHERE name = ? AND line_user_id IS NULL
           ORDER BY updated_at DESC LIMIT 1""",
        (name,),
    ).fetchone()
    if not row:
        return False
    conn.execute(
        "UPDATE attendees SET line_user_id = ?, updated_at = datetime('now', 'localtime') WHERE id = ?",
        (line_user_id, row["id"]),
    )
    conn.commit()
    return True


def normalize_phone(raw: str) -> str:
    """手機號只留數字：0912-345 678 → 0912345678；+886912345678 → 0912345678"""
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("886"):
        digits = "0" + digits[3:]
    return digits


def get_event(conn: sqlite3.Connection, slug: str):
    return conn.execute("SELECT * FROM events WHERE slug = ?", (slug,)).fetchone()


def get_wheel_roster(conn: sqlite3.Connection, event_id: int):
    """轉盤名單：這場已簽到、且還沒中獎過的人（依簽到時間排序）。"""
    return conn.execute(
        """SELECT a.id, a.name FROM attendees a
           JOIN signups s ON s.attendee_id = a.id
           WHERE s.event_id = ?
             AND a.id NOT IN (SELECT attendee_id FROM wheel_winners WHERE event_id = ?)
           ORDER BY s.created_at""",
        (event_id, event_id),
    ).fetchall()


def get_wheel_winners(conn: sqlite3.Connection, event_id: int):
    return conn.execute(
        """SELECT w.id, a.name, w.prize, w.created_at FROM wheel_winners w
           JOIN attendees a ON a.id = w.attendee_id
           WHERE w.event_id = ? ORDER BY w.created_at""",
        (event_id,),
    ).fetchall()


def add_wheel_winner(conn: sqlite3.Connection, event_id: int, attendee_id: int, prize: str) -> bool:
    """回傳False表示這個人在這場已經中過獎了（不重複記錄）。"""
    dup = conn.execute(
        "SELECT 1 FROM wheel_winners WHERE event_id = ? AND attendee_id = ?",
        (event_id, attendee_id),
    ).fetchone()
    if dup:
        return False
    conn.execute(
        "INSERT INTO wheel_winners (event_id, attendee_id, prize) VALUES (?, ?, ?)",
        (event_id, attendee_id, prize or None),
    )
    conn.commit()
    return True


def clear_wheel_winners(conn: sqlite3.Connection, event_id: int) -> None:
    """清空中獎名單，同時把獎品庫存全部復原(重置=這場重新抽，庫存也該回到滿的)。"""
    conn.execute("DELETE FROM wheel_winners WHERE event_id = ?", (event_id,))
    conn.execute(
        "UPDATE wheel_prizes SET remaining_qty = total_qty WHERE event_id = ?",
        (event_id,),
    )
    conn.commit()


def get_wheel_prizes(conn: sqlite3.Connection, event_id: int):
    """回傳這場活動的獎品清單，依sort_order排序。"""
    return conn.execute(
        "SELECT * FROM wheel_prizes WHERE event_id = ? ORDER BY sort_order, id",
        (event_id,),
    ).fetchall()


def set_wheel_prizes(conn: sqlite3.Connection, event_id: int, prizes: list[tuple[str, int]]) -> None:
    """整批設定這場活動的獎品清單(先清空舊的再寫入新的)。prizes是[(name, qty), ...]。"""
    conn.execute("DELETE FROM wheel_prizes WHERE event_id = ?", (event_id,))
    for i, (name, qty) in enumerate(prizes):
        conn.execute(
            "INSERT INTO wheel_prizes (event_id, name, total_qty, remaining_qty, sort_order) VALUES (?, ?, ?, ?, ?)",
            (event_id, name, qty, qty, i),
        )
    conn.commit()


def decrement_wheel_prize(conn: sqlite3.Connection, prize_id: int) -> str | None:
    """扣一個庫存，回傳獎品名稱；庫存已經是0時回傳None（不能再扣）。"""
    row = conn.execute("SELECT name, remaining_qty FROM wheel_prizes WHERE id = ?", (prize_id,)).fetchone()
    if not row or row["remaining_qty"] <= 0:
        return None
    conn.execute("UPDATE wheel_prizes SET remaining_qty = remaining_qty - 1 WHERE id = ?", (prize_id,))
    conn.commit()
    return row["name"]


def upsert_signup(conn: sqlite3.Connection, event_id: int, name: str, phone: str, company_title: str, email: str = "") -> str:
    """回傳 'new'（首次報名）或 'repeat'（這場已報過）"""
    row = conn.execute("SELECT id FROM attendees WHERE phone = ?", (phone,)).fetchone()
    if row:
        attendee_id = row["id"]
        conn.execute(
            """UPDATE attendees SET name = ?, company_title = COALESCE(NULLIF(?, ''), company_title),
               email = COALESCE(NULLIF(?, ''), email),
               updated_at = datetime('now', 'localtime') WHERE id = ?""",
            (name, company_title, email, attendee_id),
        )
    else:
        cur = conn.execute(
            "INSERT INTO attendees (name, phone, company_title, email) VALUES (?, ?, ?, ?)",
            (name, phone, company_title or None, email or None),
        )
        attendee_id = cur.lastrowid

    dup = conn.execute(
        "SELECT 1 FROM signups WHERE attendee_id = ? AND event_id = ?",
        (attendee_id, event_id),
    ).fetchone()
    if not dup:
        conn.execute(
            "INSERT INTO signups (attendee_id, event_id) VALUES (?, ?)",
            (attendee_id, event_id),
        )
    conn.commit()
    return "repeat" if dup else "new"


# ---- 大樹小講場次管理（2026-08-23 教練交辦：場次改資料庫當唯一真相源，後台自己管） ----

def list_site_sessions(conn: sqlite3.Connection, site: str = "bigtree"):
    """後台列表用：該站台全部場次，未來的排前面、過去的排後面（各自依日期排序）。"""
    return conn.execute(
        """SELECT e.*, COUNT(s.id) AS signup_count,
                  CASE WHEN e.event_date < date('now','localtime') THEN 1 ELSE 0 END AS is_past
           FROM events e LEFT JOIN signups s ON s.event_id = e.id
           WHERE e.site = ?
           GROUP BY e.id
           ORDER BY is_past, e.event_date, COALESCE(e.start_time,'')""",
        (site,),
    ).fetchall()


def get_session(conn: sqlite3.Connection, event_id: int):
    return conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()


def save_session(conn: sqlite3.Connection, data: dict, event_id: int | None = None) -> tuple[bool, str]:
    """新增或更新一場活動。回傳 (成功與否, 訊息)。"""
    required = ("slug", "name", "event_date")
    for key in required:
        if not (data.get(key) or "").strip():
            return False, "網址短名、主題、日期都要填。"

    fields = ("slug", "name", "event_date", "start_time", "slot_key",
              "location", "venue", "address", "transport", "status", "site",
              "show_live_count")
    vals = {k: (data.get(k) or "").strip() or None for k in fields}
    vals["site"] = vals["site"] or "bigtree"
    vals["status"] = vals["status"] or "active"
    # checkbox 欄位：勾了才會出現在 form data 裡（值是 "on"），沒勾則完全不會送出這個 key
    vals["show_live_count"] = 1 if data.get("show_live_count") else 0

    clash = conn.execute(
        "SELECT id FROM events WHERE slug = ? AND id IS NOT ?", (vals["slug"], event_id)
    ).fetchone()
    if clash:
        return False, f"網址短名「{vals['slug']}」已經被其他場次用了，請換一個。"

    if event_id:
        conn.execute(
            f"UPDATE events SET {', '.join(f'{k}=?' for k in fields)} WHERE id = ?",
            (*vals.values(), event_id),
        )
        msg = "已更新這場活動。"
    else:
        conn.execute(
            f"INSERT INTO events ({', '.join(fields)}) VALUES ({', '.join('?' * len(fields))})",
            tuple(vals.values()),
        )
        msg = "已新增一場活動。"
    conn.commit()
    return True, msg


def set_session_status(conn: sqlite3.Connection, event_id: int, status: str) -> None:
    if status not in ("active", "cancelled", "draft"):
        return
    conn.execute("UPDATE events SET status = ? WHERE id = ?", (status, event_id))
    conn.commit()


def delete_session(conn: sqlite3.Connection, event_id: int) -> tuple[bool, str]:
    """刪除場次。已經有人報名的不給刪（避免報名紀錄變成孤兒），改建議設為已取消。"""
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM signups WHERE event_id = ?", (event_id,)
    ).fetchone()
    if row["c"]:
        return False, f"這場已經有 {row['c']} 筆報名紀錄，不能直接刪除。請改用「設為已取消」，紀錄才不會不見。"
    conn.execute("DELETE FROM wheel_prizes WHERE event_id = ?", (event_id,))
    conn.execute("DELETE FROM wheel_winners WHERE event_id = ?", (event_id,))
    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    return True, "已刪除這場活動。"
