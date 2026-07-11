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
    conn.commit()
    conn.close()


def already_processed(conn: sqlite3.Connection, image_filename: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM cards WHERE image_filename = ?", (image_filename,)
    ).fetchone()
    return row is not None


def insert_card(conn: sqlite3.Connection, image_filename: str, fields: dict) -> None:
    if "_error" in fields:
        conn.execute(
            "INSERT INTO cards (image_filename, status, raw_response) VALUES (?, 'failed', ?)",
            (image_filename, fields.get("_raw", "")),
        )
        conn.commit()
        return

    keywords = fields.get("keywords") or []
    conn.execute(
        """INSERT INTO cards
           (image_filename, name, title, company, mobile, landline, email,
            line_id, website, address, tagline, category, keywords,
            confidence_notes, raw_response, status)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
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
            json.dumps(keywords, ensure_ascii=False),
            fields.get("confidence_notes"),
            json.dumps(fields, ensure_ascii=False),
            "needs_review" if fields.get("confidence_notes") else "ok",
        ),
    )
    conn.commit()
