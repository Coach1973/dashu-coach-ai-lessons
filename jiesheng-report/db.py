import os
import sqlite3
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), "jiesheng_report.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

WORKSHOPS = ["台南", "台北"]
PAID_METHODS = ["ATM", "PAYUNi", "其他"]
REFERRERS = ["曜董", "大樹", "佩君", "Lavi"]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_conn()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    existing_cols = {row["name"] for row in conn.execute("PRAGMA table_info(registrants)")}
    if "referrer" not in existing_cols:
        conn.execute("ALTER TABLE registrants ADD COLUMN referrer TEXT")
    if "submitter" not in existing_cols:
        conn.execute("ALTER TABLE registrants ADD COLUMN submitter TEXT")
    conn.commit()
    conn.close()


def list_registrants(conn: sqlite3.Connection, workshop: str):
    return conn.execute(
        "SELECT * FROM registrants WHERE workshop = ? ORDER BY register_date DESC, created_at DESC",
        (workshop,),
    ).fetchall()


def get_stats(conn: sqlite3.Connection) -> dict:
    """回傳三場各自的 {total, paid, unpaid}"""
    stats = {}
    for w in WORKSHOPS:
        row = conn.execute(
            "SELECT COUNT(*) AS total, SUM(paid) AS paid FROM registrants WHERE workshop = ?",
            (w,),
        ).fetchone()
        total = row["total"] or 0
        paid = row["paid"] or 0
        stats[w] = {"total": total, "paid": paid, "unpaid": total - paid}
    return stats


def add_registrant(conn: sqlite3.Connection, workshop: str, name: str, phone: str,
                    register_date: str, note: str, referrer: str = None,
                    paid: bool = False, paid_method: str = None, amount=None,
                    submitter: str = None) -> int:
    paid_date = date.today().isoformat() if paid else None
    cur = conn.execute(
        """INSERT INTO registrants
           (workshop, name, phone, register_date, note, referrer,
            paid, paid_method, paid_date, amount, submitter)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (workshop, name, phone or None, register_date, note or None, referrer or None,
         1 if paid else 0, paid_method if paid else None, paid_date, amount, submitter or None),
    )
    conn.commit()
    return cur.lastrowid


def update_registrant(conn: sqlite3.Connection, reg_id: int, name: str, phone: str,
                       register_date: str, note: str, paid_method: str, amount,
                       referrer: str = None, submitter: str = None) -> None:
    conn.execute(
        """UPDATE registrants SET name = ?, phone = ?, register_date = ?, note = ?,
           paid_method = ?, amount = ?, referrer = ?, submitter = ?,
           updated_at = datetime('now', 'localtime')
           WHERE id = ?""",
        (name, phone or None, register_date, note or None, paid_method or None, amount,
         referrer or None, submitter or None, reg_id),
    )
    conn.commit()


def set_paid(conn: sqlite3.Connection, reg_id: int, paid: bool, paid_method: str, amount) -> None:
    paid_date = "date('now', 'localtime')" if paid else "NULL"
    conn.execute(
        f"""UPDATE registrants SET paid = ?, paid_method = ?, amount = ?,
            paid_date = {paid_date}, updated_at = datetime('now', 'localtime')
            WHERE id = ?""",
        (1 if paid else 0, paid_method if paid else None, amount, reg_id),
    )
    conn.commit()


def delete_registrant(conn: sqlite3.Connection, reg_id: int) -> None:
    conn.execute("DELETE FROM registrants WHERE id = ?", (reg_id,))
    conn.commit()


def get_registrant(conn: sqlite3.Connection, reg_id: int):
    return conn.execute("SELECT * FROM registrants WHERE id = ?", (reg_id,)).fetchone()
