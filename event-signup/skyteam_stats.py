"""顧問師天團（/curated/skyteam/）的人氣排序＋到訪次數，機制比照 mentor100（AI 百人導師）。

- 到訪次數：每次載入頁面記一筆（含重複造訪），只算 TRACKING_START 之後的
- 點擊次數：每次點某位顧問師（頭像牆、名錄卡片）記一筆，前面固定區依點擊次數由高到低排
"""
import re
import time

import db

TRACKING_START = "2026-10-25 00:00:00"  # 教練 2026-10-25 指定的起算點
_BOT_RE = re.compile(r"bot|spider|crawl|preview|facebookexternalhit|line-poker|slurp|curl|python", re.I)
_HITS: dict = {}  # ip -> [時間戳]，防灌爆：每個IP每小時最多 120 筆


def _conn():
    conn = db.get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS skyteam_visits ("
                 " id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT NOT NULL,"
                 " visited_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))")
    conn.execute("CREATE TABLE IF NOT EXISTS skyteam_clicks ("
                 " id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,"
                 " clicked_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))")
    return conn


def is_bot(user_agent: str) -> bool:
    return bool(_BOT_RE.search(user_agent or ""))


def allowed(ip: str) -> bool:
    now = time.time()
    hits = [t for t in _HITS.get(ip, []) if now - t < 3600]
    if len(hits) >= 120:
        _HITS[ip] = hits
        return False
    _HITS[ip] = hits + [now]
    return True


def stats() -> dict:
    conn = _conn()
    try:
        views = conn.execute("SELECT COUNT(*) FROM skyteam_visits WHERE visited_at >= ?",
                             (TRACKING_START,)).fetchone()[0]
        rows = conn.execute("SELECT name, COUNT(*) FROM skyteam_clicks WHERE clicked_at >= ? GROUP BY name",
                            (TRACKING_START,)).fetchall()
        return {"views": views, "clicks": {r[0]: r[1] for r in rows}}
    finally:
        conn.close()


def log_visit(ip: str) -> None:
    conn = _conn()
    try:
        conn.execute("INSERT INTO skyteam_visits (ip) VALUES (?)", (ip,))
        conn.commit()
    finally:
        conn.close()


def log_click(name: str) -> bool:
    name = (name or "").strip()
    if not name or len(name) > 40:
        return False
    conn = _conn()
    try:
        conn.execute("INSERT INTO skyteam_clicks (name) VALUES (?)", (name,))
        conn.commit()
        return True
    finally:
        conn.close()
