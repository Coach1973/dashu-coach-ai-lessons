"""榮樹下來賓進度表（2026-10-29 教練：不要另開 Google 試算表，直接在 SOP 網頁上勾選，存進資料庫）

一列＝行程總表裡的一場榮樹下訪談。自動帶出的欄位（不用勾）：來賓、邀請人、訪談時間、代預約、來賓卡；
團隊手動勾選的欄位存在 rongtree_tracker 表（以行程的 id 對應），大家看到的是同一份。
網址：/api/rongtree/tracker/<團隊代碼>（GET 讀、POST 改一格；代碼同來賓卡後台 /rongtree/a/<代碼>）
"""
import datetime as dt
import json

import rongtree_guest as rg

TZ = dt.timezone(dt.timedelta(hours=8))
PAST_DAYS, AHEAD_DAYS = 120, 60   # 進度表涵蓋：過去 120 天（追 Podcast、短影音）到未來 60 天

# 手動欄位：True＝勾選框；清單＝下拉選項（第一個空字串＝還沒填）
FIELDS = {
    "group": True,                          # 進預約群
    "warm": ["", "會前會 ✅", "直接上"],     # 暖身
    "done": True,                           # 已訪談
    "biggroup": ["", "願意 → 已入大群", "不方便"],
    "podcast": True,                        # Podcast 已上架
    "shorts": ["", "暫存待剪", "已發布"],     # 短影音
}


def _conn():
    conn = rg.db.get_conn()
    conn.execute("CREATE TABLE IF NOT EXISTS rongtree_tracker ("
                 " event_id TEXT PRIMARY KEY, data TEXT NOT NULL DEFAULT '{}',"
                 " updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))")
    return conn


def _interviews():
    """行程總表裡過去 120 天到未來 60 天的榮樹下訪談（同一場的 Google 日曆副本只留總表那筆，跟節目網站同一套）。"""
    try:
        data = json.loads(rg.SCHEDULE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []
    now = dt.datetime.now(TZ)
    out = []
    for e in data.get("events", []):
        t = e.get("title", "")
        if e.get("allday") or not e.get("id") or not (e.get("booking_type") == "榮樹下訪談" or t.startswith("榮樹下訪談") or t.startswith("訪談預約（待確認）")):
            continue
        try:
            start = dt.datetime.fromisoformat(f"{e['date']}T{e['start']}:00+08:00")
        except (KeyError, ValueError):
            continue
        if now - dt.timedelta(days=PAST_DAYS) <= start <= now + dt.timedelta(days=AHEAD_DAYS):
            out.append(e)
    mine = {(e["date"], e["start"]) for e in out if e.get("source") != "Google日曆"}
    out = [e for e in out if e.get("source") != "Google日曆" or (e["date"], e["start"]) not in mine]
    return sorted(out, key=lambda e: (e["date"], e["start"]))


def rows():
    conn = _conn()
    saved = {r["event_id"]: json.loads(r["data"]) for r in conn.execute("SELECT event_id, data FROM rongtree_tracker")}
    forms = conn.execute("SELECT token, data FROM rongtree_guest_forms WHERE deleted_at IS NULL").fetchall() \
        if conn.execute("SELECT 1 FROM sqlite_master WHERE name='rongtree_guest_forms'").fetchone() else []
    conn.close()
    now = dt.datetime.now(TZ)
    out = []
    for e in _interviews():
        tok = e.get("form_token")
        mine = [json.loads(f["data"]).get("name", "") for f in forms if tok and rg._slot_has(f["token"], tok)]
        guest = "、".join(n for n in mine if n) or e.get("guest") or ""
        if not guest and not e.get("booked_by"):
            continue  # 跟節目網站同一條（教練 2026-10-22）：沒人預約、連來賓是誰都不知道的，不列
        start = dt.datetime.fromisoformat(f"{e['date']}T{e['start']}:00+08:00")
        out.append({"id": e["id"], "date": e["date"], "start": e["start"], "end": e.get("end", ""),
                    "past": start < now,
                    "guest": guest,
                    "inviter": e.get("booked_by", ""),
                    "booked": "待確認" if e.get("tentative") else "✅",
                    "cards": len(mine),
                    "form": f"/rongtree/guest/{tok}" if tok else "",
                    **{k: saved.get(e["id"], {}).get(k, False if v is True else "") for k, v in FIELDS.items()}})
    return out


def set_field(event_id, field, value):
    """改一格。回傳 (ok, 錯誤訊息)。只收進度表上看得到的那幾場、只收白名單欄位與選項。"""
    if field not in FIELDS:
        return False, "沒有這個欄位"
    spec = FIELDS[field]
    if spec is True:
        if not isinstance(value, bool):
            return False, "勾選欄只能是勾或不勾"
    elif value not in spec:
        return False, "選項不正確"
    if event_id not in {e["id"] for e in _interviews()}:
        return False, "找不到這場訪談"
    conn = _conn()
    r = conn.execute("SELECT data FROM rongtree_tracker WHERE event_id=?", (event_id,)).fetchone()
    d = json.loads(r["data"]) if r else {}
    d[field] = value
    conn.execute("INSERT INTO rongtree_tracker (event_id, data) VALUES (?, ?) "
                 "ON CONFLICT(event_id) DO UPDATE SET data=excluded.data, updated_at=datetime('now','localtime')",
                 (event_id, json.dumps(d, ensure_ascii=False)))
    conn.commit()
    conn.close()
    return True, None
