"""「零基礎學 AI，讓你被看見」現場互動頁（大樹教練 × 中華新媒體影音發展協會）的資料後端（2026-10-31）

頁面 github_repos/ai-impact（https://event.bymyway.com/curated/ai-impact/）原本 API_BASE=null，
每個人的票、提問、回饋只存在自己手機的瀏覽器，講師的螢幕完全看不到。
這支接上頁面內建的「連線模式」：同網域 /api/nmda-ai，頁面每 4 秒讀一次 /state。

端點（跟頁面內註解一致）：
  GET  /api/nmda-ai/state?event=…            全部目前資料
  POST /api/nmda-ai/polls/<poll>/vote        {option, delta:1|-1}
  POST /api/nmda-ai/options                  {key, label, poll}
  POST /api/nmda-ai/questions                {id, topic, body, name}
  POST /api/nmda-ai/questions/<id>/vote      {delta}
  POST /api/nmda-ai/echoes                   {id, body}
  POST /api/nmda-ai/skills                   {id, name, kind, use, how, by}
  POST /api/nmda-ai/skills/<id>/like         {delta}
  POST /api/nmda-ai/words                    {w}
  POST /api/nmda-ai/reset?key=…              清空（開場前彩排後用，key 是後台簽章）
資料另存 nmda_ai.db（不碰 event.db）。每個 IP 每分鐘最多 60 次寫入，欄位長度都有上限。
"""
import hashlib
import hmac
import json
import os
import re
import sqlite3
import threading
import time
from pathlib import Path

from flask import Blueprint, jsonify, request

bp = Blueprint("nmda_ai", __name__, url_prefix="/api/nmda-ai")

# 11/01：資料庫放在 workspace 外面。放在 workspace 內且沒進 git 時，每次收工自動備份（git stash -u）會把它收走、
# 程式在空檔期建一個空新檔，原資料就放不回來（統計全清空、介面 500）。
DB_PATH = Path(os.environ.get("NMDA_AI_DB", Path.home() / ".openclaw" / "data" / "nmda_ai.db"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
SEED_PATH = Path(__file__).resolve().parent / "nmda_ai_seed_skills.json"
_LOCK = threading.Lock()
_HITS: dict = {}
ID_RE = re.compile(r"^[A-Za-z0-9_\-]{1,40}$")
KINDS = {"AI 指令", "工具／網站", "工作流程", "其他"}


_SCHEMA = """
        CREATE TABLE IF NOT EXISTS polls (poll TEXT, opt TEXT, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY (poll, opt));
        CREATE TABLE IF NOT EXISTS options (key TEXT PRIMARY KEY, label TEXT, poll TEXT);
        CREATE TABLE IF NOT EXISTS questions (id TEXT PRIMARY KEY, topic TEXT, body TEXT, name TEXT,
            votes INTEGER NOT NULL DEFAULT 0, answered INTEGER NOT NULL DEFAULT 0, ts INTEGER);
        CREATE TABLE IF NOT EXISTS echoes (id TEXT PRIMARY KEY, body TEXT, ts INTEGER);
        CREATE TABLE IF NOT EXISTS skills (id TEXT PRIMARY KEY, name TEXT, kind TEXT, use TEXT, how TEXT,
            by TEXT, likes INTEGER NOT NULL DEFAULT 0, ts INTEGER);
        CREATE TABLE IF NOT EXISTS words (w TEXT PRIMARY KEY, n INTEGER NOT NULL DEFAULT 0);
        """


def _conn():
    c = sqlite3.connect(DB_PATH, timeout=10)
    try:
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.executescript(_SCHEMA)  # 檔案被換成空檔時自動補表，不再 500
    except Exception:
        c.close()  # 設定失敗也要關，否則每次失敗漏一條連線（10/31 開檔數爆掉的原因）
        raise
    return c


def init_db():
    with _LOCK:
        c = _conn()
        c.executescript(_SCHEMA)
        if not c.execute("SELECT 1 FROM skills LIMIT 1").fetchone() and SEED_PATH.exists():
            now = int(time.time() * 1000)
            for i, s in enumerate(json.loads(SEED_PATH.read_text(encoding="utf-8"))):
                c.execute("INSERT OR IGNORE INTO skills VALUES (?,?,?,?,?,?,?,?)",
                          (s["id"], s["name"], s["kind"], s["use"], s["how"], s.get("by", ""), 0, now - (i + 1) * 3600_000))
        c.commit()
        c.close()


def _s(v, n):
    return str(v or "").strip()[:n]


def _delta(data):
    return 1 if data.get("delta", 1) >= 0 else -1


def _limited():
    ip = request.headers.get("CF-Connecting-IP") or request.remote_addr or "?"
    now = time.time()
    hits = [t for t in _HITS.get(ip, []) if now - t < 60]
    hits.append(now)
    _HITS[ip] = hits
    return len(hits) > 600  # 11/01 教練：同 IP 重複也照算；現場同一個 WiFi 70 人各勾 8 個不能被擋，這只防惡意洪水


@bp.before_request
def _guard():
    if request.method == "POST" and _limited():
        return jsonify(error="too many"), 429


@bp.after_request
def _headers(resp):
    resp.headers["Cache-Control"] = "no-store"
    return resp


@bp.get("/state")
def state():
    c = _conn()
    try:
        return _state_json(c)
    finally:
        c.close()


def _state_json(c):
    polls: dict = {}
    for r in c.execute("SELECT poll, opt, n FROM polls WHERE n > 0"):
        polls.setdefault(r["poll"], {})[r["opt"]] = r["n"]
    out = {
        "polls": polls,
        "options": [dict(r) for r in c.execute("SELECT key, label, poll FROM options")],
        "questions": [{**dict(r), "answered": bool(r["answered"])} for r in c.execute("SELECT * FROM questions ORDER BY ts")],
        "echoes": [dict(r) for r in c.execute("SELECT id, body, ts FROM echoes ORDER BY ts")],
        "skills": [dict(r) for r in c.execute("SELECT * FROM skills ORDER BY ts")],
        "words": [dict(r) for r in c.execute("SELECT w, n FROM words ORDER BY n DESC LIMIT 80")],
    }
    return jsonify(out)


def _write(sql, params):
    with _LOCK:
        c = _conn()
        try:
            c.execute(sql, params)
            c.commit()
        finally:
            c.close()


@bp.post("/polls/<poll>/vote")
def poll_vote(poll):
    d = request.get_json(silent=True) or {}
    opt = _s(d.get("option"), 60)
    if not ID_RE.match(poll) or not opt:
        return jsonify(error="bad"), 400
    _write("INSERT INTO polls (poll, opt, n) VALUES (?,?,MAX(0,?)) "
           "ON CONFLICT(poll, opt) DO UPDATE SET n = MAX(0, n + ?)", (poll, opt, _delta(d), _delta(d)))
    return jsonify(ok=True)


@bp.post("/options")
def add_option():
    d = request.get_json(silent=True) or {}
    key, label = _s(d.get("key"), 60), _s(d.get("label"), 60)
    if not key or not label:
        return jsonify(error="bad"), 400
    _write("INSERT OR IGNORE INTO options VALUES (?,?,?)", (key, label, _s(d.get("poll"), 20) or "ability"))
    return jsonify(ok=True)


@bp.post("/questions")
def add_question():
    d = request.get_json(silent=True) or {}
    qid, body = _s(d.get("id"), 40), _s(d.get("body"), 500)
    if not ID_RE.match(qid) or not body:
        return jsonify(error="bad"), 400
    _write("INSERT OR IGNORE INTO questions (id, topic, body, name, votes, answered, ts) VALUES (?,?,?,?,0,0,?)",
           (qid, _s(d.get("topic"), 40), body, _s(d.get("name"), 30), int(time.time() * 1000)))
    return jsonify(ok=True)


@bp.post("/questions/<qid>/vote")
def vote_question(qid):
    d = request.get_json(silent=True) or {}
    _write("UPDATE questions SET votes = MAX(0, votes + ?) WHERE id = ?", (_delta(d), qid))
    return jsonify(ok=True)


@bp.post("/echoes")
def add_echo():
    d = request.get_json(silent=True) or {}
    eid, body = _s(d.get("id"), 40), _s(d.get("body"), 300)
    if not ID_RE.match(eid) or not body:
        return jsonify(error="bad"), 400
    _write("INSERT OR IGNORE INTO echoes VALUES (?,?,?)", (eid, body, int(time.time() * 1000)))
    return jsonify(ok=True)


@bp.post("/skills")
def add_skill():
    d = request.get_json(silent=True) or {}
    sid, name, how = _s(d.get("id"), 40), _s(d.get("name"), 60), _s(d.get("how"), 1500)
    kind = d.get("kind") if d.get("kind") in KINDS else _s(d.get("kind"), 20)
    if not ID_RE.match(sid) or not name or not how:
        return jsonify(error="bad"), 400
    _write("INSERT OR IGNORE INTO skills VALUES (?,?,?,?,?,?,0,?)",
           (sid, name, kind, _s(d.get("use"), 200), how, _s(d.get("by"), 30), int(time.time() * 1000)))
    return jsonify(ok=True)


@bp.post("/skills/<sid>/like")
def like_skill(sid):
    d = request.get_json(silent=True) or {}
    _write("UPDATE skills SET likes = MAX(0, likes + ?) WHERE id = ?", (_delta(d), sid))
    return jsonify(ok=True)


@bp.post("/words")
def add_word():
    d = request.get_json(silent=True) or {}
    w = _s(d.get("w"), 20)
    if not w:
        return jsonify(error="bad"), 400
    _write("INSERT INTO words (w, n) VALUES (?,1) ON CONFLICT(w) DO UPDATE SET n = n + 1", (w,))
    return jsonify(ok=True)


def _reset_key():
    secret = os.environ.get("EVENT_SECRET_KEY", "") or "nmda-ai"
    return hmac.new(secret.encode(), b"nmda-ai-reset", hashlib.sha256).hexdigest()[:16]


@bp.post("/reset")
def reset():
    if not hmac.compare_digest(request.args.get("key", ""), _reset_key()):
        return jsonify(error="forbidden"), 403
    with _LOCK:
        c = _conn()
        try:
            for t in ("polls", "options", "questions", "echoes", "words"):
                c.execute(f"DELETE FROM {t}")
            c.execute("UPDATE skills SET likes = 0")
            c.execute("DELETE FROM skills WHERE id NOT LIKE 'seed%'")
            c.commit()
        finally:
            c.close()
    return jsonify(ok=True)


init_db()
