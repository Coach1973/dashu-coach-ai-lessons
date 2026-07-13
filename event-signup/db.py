import os
import re
import sqlite3

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
    conn.commit()
    conn.close()


def get_current_event(conn: sqlite3.Connection):
    return conn.execute("SELECT * FROM events WHERE is_current = 1 LIMIT 1").fetchone()


def set_current_event(conn: sqlite3.Connection, slug: str) -> bool:
    """把固定QR立牌(/checkin)導向的活動切換成slug這場。回傳False表示找不到這個活動。"""
    row = conn.execute("SELECT id FROM events WHERE slug = ?", (slug,)).fetchone()
    if not row:
        return False
    conn.execute("UPDATE events SET is_current = 0")
    conn.execute("UPDATE events SET is_current = 1 WHERE id = ?", (row["id"],))
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


def upsert_signup(conn: sqlite3.Connection, event_id: int, name: str, phone: str, company_title: str) -> str:
    """回傳 'new'（首次報名）或 'repeat'（這場已報過）"""
    row = conn.execute("SELECT id FROM attendees WHERE phone = ?", (phone,)).fetchone()
    if row:
        attendee_id = row["id"]
        conn.execute(
            """UPDATE attendees SET name = ?, company_title = COALESCE(NULLIF(?, ''), company_title),
               updated_at = datetime('now', 'localtime') WHERE id = ?""",
            (name, company_title, attendee_id),
        )
    else:
        cur = conn.execute(
            "INSERT INTO attendees (name, phone, company_title) VALUES (?, ?, ?)",
            (name, phone, company_title or None),
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
