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
    conn.commit()
    conn.close()


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
