"""教練行程頁（2026-10-12）：只有拿到網址（含一段隨機代碼）的人看得到。

資料來源＝workspace/knowledges/教練行程總表.json（scripts/coach_schedule.py 維護），每次開頁即時讀，行程一改頁面就跟著變。
每個時段顯示行程名稱（教練 2026-10-13：行程本來就公開，只要一個頁面，不分教練版、訪客版），不顯示地點與備註。
預約不填姓名電話（教練 2026-10-13：會約的只有兩個人）：點空檔→選類型。選「榮樹下訪談」＝邱裕榮；
「咖啡會議／電話回訪／入會訪談」＝陳佩君老師（BNI）。其他行程類型（諮詢會議、分享會、線上學習、戰報…）不開放預約。
代碼放在 workspace/state/coach_schedule_token.txt；要換網址就改這個檔（舊網址立即失效）。
"""
import datetime as dt
import fcntl
import hmac
import json
import os
import secrets
import tempfile
import uuid
from html import escape
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DATA = WS / "knowledges" / "教練行程總表.json"
TOKEN_FILE = WS / "state" / "coach_schedule_token.txt"
WEEK = "一二三四五六日"
TZ = dt.timezone(dt.timedelta(hours=8))
DAYS = 28
SESSION = 60  # 一場 1 小時
BUFFER = 30   # 兩場訪談之間的緩衝（教練 2026-10-19：要喝水、上廁所、跟下一位來賓打招呼暖場，不能 8 點結束 8 點又開下一場）
CANCELLABLE = ("預約頁", "巴哈", "coach", "教練")  # 跟 coach_schedule.py 的同名常數一致：只有總表自己的行程可取消


def token_ok(token: str) -> bool:
    try:
        real = TOKEN_FILE.read_text().strip()
    except OSError:
        return False
    return bool(real) and hmac.compare_digest(real, token or "")


# 預約頁可選的類型 → 誰會約（教練 2026-10-13 指定，只開放這四種）
BOOKING_TYPES = {
    "榮樹下訪談": "邱裕榮",
    "咖啡會議": "陳佩君老師",
    "電話回訪": "陳佩君老師",
    "入會訪談": "陳佩君老師",
}


def _show_title(ev):
    """預約頁進來的預約只顯示類型（舊資料沒有類型＝榮樹下訪談），不秀預約者姓名；還沒確認的後面會加「（待確認）」"""
    if ev.get("guest"):
        return f"榮樹下訪談：{ev['guest']}" + (f"（{ev['guest_field']}）" if ev.get("guest_field") else "")
    if ev.get("source") == "預約頁":
        return ev.get("booking_type") or "榮樹下訪談"
    return ev.get("title", "")


def _hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def _fmt(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def _busy(d, data):
    iso = d.isoformat()
    out = []
    for e in data.get("events", []):
        if e.get("covered_by_google"):  # 2026-10-13：同一件 Google 日曆已有，不重複列（同 coach_schedule.blocks_on）
            continue
        if e["date"] <= iso <= e.get("end_date", e["date"]):
            out.append((0, 1440, e) if e.get("allday") else (_hm(e["start"]), _hm(e["end"]), _yield_if_online(e, d)))
    for r in data.get("recurring", []):
        if d.weekday() != r["weekday"]:
            continue
        if r.get("since") and iso < r["since"]:
            continue
        if r.get("until") and iso > r["until"]:
            continue
        if iso in r.get("skip", []) or iso in r.get("gskip", []):
            continue
        out.append((_hm(r["start"]), _hm(r["end"]), _yield_if_online(r, d)))
    return sorted(out, key=lambda x: x[0])


def _yield_if_online(item, d):
    """2026-10-15 教練：週四的線上聚會／線上學習保留，但訪談優先，預約頁不擋。
    Google 同步會整批重建一次性行程，所以用名稱判斷，不靠資料旗標。"""
    if d.weekday() == 3 and str(item.get("title", "")).startswith("線上"):
        return {**item, "yield": True}
    return item


def _is_interview(ev):
    """訪談類行程（預約頁預約、總表訪談、標題有「訪談」）：前後各留 BUFFER 分鐘緩衝；一般會議（BNI 例會、團隊會議…）不加。
    每週固定行程（有 weekday）一律不算：週四那列「休息（訪談間隔）」本身就是緩衝，標題雖有「訪談」不能再加一圈。"""
    if "weekday" in ev:
        return False
    return ev.get("kind") == "interview" or bool(ev.get("guest")) or "訪談" in str(ev.get("title", ""))


def _free(busy, ws, we):
    cur, slots = ws, []
    for s, e, x in busy:
        if x.get("yield"):  # 2026-10-15 教練：線上聚會／學習保留，但訪談優先，不擋預約
            continue
        if _is_interview(x):  # 2026-10-19 教練：已有訪談的前後各留半小時，不能一場接一場
            s, e = s - BUFFER, e + BUFFER
        if e <= cur or s >= we:
            continue
        if s - cur >= 60:
            slots.append((cur, min(s, we)))
        cur = max(cur, e)
    if we - cur >= 60:
        slots.append((cur, we))
    return slots


def _starts(slots):
    """每個可約區間：一場 1 小時＋場間緩衝 30 分，所以每 90 分鐘一個起點（19:00、20:30、22:00…）"""
    out = []
    for a, b in slots:
        t = a
        while t + SESSION <= b:
            out.append(t)
            t += SESSION + BUFFER
    return out


def _win_start(data, d=None):
    """白天可約窗口的起點。2026-10-23 教練：週六 9:30 起（總表 interview_window_start_by_weekday，鍵＝星期幾、0＝週一），
    其他天照 interview_window。跟 scripts/coach_schedule.py 的 win_start 同一套。"""
    start = data.get("interview_window", {"start": "10:00"})["start"]
    if d is not None:
        start = data.get("interview_window_start_by_weekday", {}).get(str(d.weekday()), start)
    return _hm(start)


def _day_slots(busy, data, d=None):
    """(白天起點, 晚上起點)。render 與 book 共用同一套算法，畫面看到的時段＝伺服器認得的時段。
    白天最後一場要在晚上開始前留出緩衝（19:00 晚上開始 → 白天最晚 18:30 結束）。"""
    eve = data.get("evening_window", {"start": "19:00", "end": "22:00"})
    ws, es, ee = _win_start(data, d), _hm(eve["start"]), _hm(eve["end"])
    return _starts(_free(busy, ws, es - BUFFER)), _starts(_free(busy, es, ee))


def _day_windows(busy, data, d=None):
    """(白天空檔, 晚上空檔)：整段可約區間，例如晚上 [(19:00, 23:00)]。
    2026-10-22 教練：不再切成固定的整點格子，來賓自己挑區間內任何一個小時（例如 19:30–20:30）；
    已有訪談的前後各留 30 分鐘，已經算在 _free 裡。"""
    eve = data.get("evening_window", {"start": "19:00", "end": "22:00"})
    ws, es, ee = _win_start(data, d), _hm(eve["start"]), _hm(eve["end"])
    return _free(busy, ws, es - BUFFER), _free(busy, es, ee)


def _fits(st, windows):
    """這一個小時（st 起算 60 分鐘）是否完整落在某段空檔裡"""
    return any(a <= st and st + SESSION <= b for a, b in windows)


STEP = 30  # 預約頁下拉選單的開始時間間隔（19:00、19:30、20:00…）


def _refresh_google():
    """打開預約頁、預約的當下才去看 Google 日曆（一分鐘內看過就不再看）；讀不到就用現有資料。"""
    import subprocess
    try:
        subprocess.run(["/usr/bin/python3", "-I", str(WS / "scripts" / "coach_schedule.py"), "ensure-fresh"],
                       capture_output=True, text=True, timeout=25)
    except Exception:  # noqa: BLE001
        pass


def book(date_s, start_s, booking_type, who=None, note=None, guest=None):
    """預約一個 1 小時時段：寫成「待確認」的行程（先占位，教練確認或取消）。
    who／note：榮樹下網頁「我要預約」（官網預約）用——預約人不是預設的那位，單位與聯絡方式只放 note（私人，不公開）。
    guest：預約人姓名（2026-10-30 教練：前置作業要看得到是誰預約，不再只寫「待確認」）。
    回傳 (ok, 訊息或事件)。伺服器端重新檢查，不信任網頁送來的時段與類型。"""
    _refresh_google()
    booking_type = (booking_type or "").strip()
    if booking_type not in BOOKING_TYPES:
        return False, "請選擇預約類型"
    who = who or BOOKING_TYPES[booking_type]
    try:
        d = dt.date.fromisoformat(date_s)
        st = _hm(start_s)
    except (ValueError, AttributeError):
        return False, "日期或時間格式不正確"
    today = dt.datetime.now(TZ).date()
    if not (today <= d < today + dt.timedelta(days=DAYS)):
        return False, "這個日期不在可預約範圍"
    lockf = open(str(DATA) + ".lock", "w")
    fcntl.flock(lockf, fcntl.LOCK_EX)
    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
        busy = _busy(d, data)
        if st % 5 or not _fits(st, sum(_day_windows(busy, data, d), [])):
            return False, "這個時段剛剛被預約走了，或離前後訪談不到 30 分鐘，請選別的時間"
        ev = {"id": uuid.uuid4().hex[:8], "date": d.isoformat(), "start": _fmt(st), "end": _fmt(st + 60),
              "title": f"{booking_type}（待確認）", "source": "預約頁", "kind": "interview", "tentative": True,
              "booking_type": booking_type, "booked_by": who, "note": note or f"預約人：{who}（預約頁點選）"}
        if guest:
            ev["guest"] = guest[:40]
            ev["guest_by"] = who
        if booking_type == "榮樹下訪談":   # 2026-10-29：來賓資料表網址在預約當下就配好（格式同 coach_schedule.guest_form_url），不用等 5 分鐘的補配
            ev["form_token"] = secrets.token_urlsafe(9)
        data["events"].append(ev)
        data["updated_at"] = dt.datetime.now(TZ).strftime("%Y-%m-%d %H:%M")
        fd, tmp = tempfile.mkstemp(dir=str(DATA.parent), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, DATA)
        return True, ev
    finally:
        fcntl.flock(lockf, fcntl.LOCK_UN)
        lockf.close()


def cancel(item_id, date_s):
    """預約頁的取消鈕。實際取消交給 coach_schedule.py cancel（同一套：刪行程、清提醒、刪 Google 那筆）。回傳 (ok, 訊息)"""
    import subprocess
    if not item_id or len(item_id) > 64:
        return False, "找不到這筆行程"
    r = subprocess.run(["/usr/bin/python3", "-I", str(WS / "scripts" / "coach_schedule.py"), "cancel", "--id", item_id, "--date", date_s or ""],
                       capture_output=True, text=True, timeout=120)
    out = (r.stdout or "").strip().splitlines()
    if r.returncode != 0:
        return False, (out[-1] if out else "取消失敗")
    return True, out[-1].replace("✅ 已取消：", "") if out else ""


def render(token: str = "") -> str:
    """2026-10-13 教練：重新設計得好看一點；點空檔直接出四個類型按鈕，不填姓名電話。"""
    _refresh_google()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    eve = data.get("evening_window", {"start": "19:00", "end": "22:00"})
    today = dt.datetime.now(TZ).date()
    cards, n_open = [], 0

    def slot_btns(d, windows, cls):
        """一段空檔一顆按鈕（例：19:00–23:00 有空檔），點下去再選要哪一個小時"""
        lab = f"{d.month}/{d.day}（{WEEK[d.weekday()]}）"
        return "".join(
            f'<button type="button" class="slot {cls}" data-d="{d.isoformat()}" data-a="{a}" data-b="{b}" '
            f'data-l="{escape(lab)}">{_fmt(a)}–{_fmt(b)}<small>有空檔</small></button>'
            for a, b in windows
        )

    week_of = None
    now_chip = '<span class="chip now">今天</span>'
    for i in range(DAYS):
        d = today + dt.timedelta(days=i)
        monday = d - dt.timedelta(days=d.weekday())
        if monday != week_of:
            week_of = monday
            sunday = monday + dt.timedelta(days=6)
            name = "本週" if i == 0 or monday <= today else ("下週" if monday - today <= dt.timedelta(days=7) else "")
            cards.append(f'<h2 class="wk"><span>{name}</span>{monday.month}/{monday.day} – {sunday.month}/{sunday.day}</h2>')
        busy = _busy(d, data)
        allday = any((s_, e_) == (0, 1440) for s_, e_, _ in busy)
        day_starts, eve_starts = ([], []) if allday else _day_windows(busy, data, d)
        n_open += bool(eve_starts)
        if eve_starts:
            chip = '<span class="chip ok">晚上可約</span>'
        elif day_starts:
            chip = '<span class="chip dt">白天可約</span>'
        else:
            chip = '<span class="chip full">已排滿</span>'
        def cancel_btn(ev, d=d):
            if ev.get("source") not in CANCELLABLE and "weekday" not in ev:
                return ""
            lab = f"{d.month}/{d.day}（{WEEK[d.weekday()]}）{_show_title(ev)}"
            return (f'<button type="button" class="cx" data-id="{escape(ev["id"])}" data-d="{d.isoformat()}" '
                    f'data-l="{escape(lab)}{"（每週固定，只取消這一次）" if "weekday" in ev else ""}">取消</button>')

        busy_html = "".join(
            f'<li class="{"tn" if ev.get("tentative") else ""}"><time>{"整天" if (s_, e_) == (0, 1440) else f"{_fmt(s_)}–{_fmt(e_)}"}</time>'
            f'<span>{escape(_show_title(ev))}{"<em>待確認</em>" if ev.get("tentative") else ""}</span>{cancel_btn(ev)}</li>'
            for s_, e_, ev in busy
        )
        slots = slot_btns(d, eve_starts, "eve") + slot_btns(d, day_starts, "dayt")
        state = "open" if eve_starts else ("dayonly" if day_starts else "full")
        cards.append(
            f'<article class="day {state}{" today" if i == 0 else ""}">'
            f'<div class="date"><b>{d.day}</b><span>週{WEEK[d.weekday()]}</span></div>'
            f'<div class="body"><div class="top">{chip}{now_chip if i == 0 else ""}</div>'
            f'{f"<div class=slots>{slots}</div>" if slots else ""}'
            f'{f"<details><summary>已有安排 {len(busy)} 項</summary><ul class=busy>{busy_html}</ul></details>" if busy else ""}'
            f'</div></article>'
        )
    updated = escape(str(data.get("updated_at", "")))
    types_html = "".join(
        f'<button type="button" class="type{" main" if t == "榮樹下訪談" else ""}" data-type="{escape(t)}">'
        f'<b>{escape(t)}</b><small>{escape(sub)}</small></button>'
        for t, sub in (("榮樹下訪談", "Podcast 錄音 ‧ 邱裕榮"), ("咖啡會議", "BNI ‧ 陳佩君老師"),
                       ("電話回訪", "BNI ‧ 陳佩君老師"), ("入會訪談", "BNI ‧ 陳佩君老師"))
    )
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>大樹教練｜可約時間</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6f1e7;--paper:#fffdf8;--ink:#2b2418;--mut:#7d7262;--line:#e7dccb;--green:#2f6b4f;--green-soft:#e3efe7;
--amber:#b9822f;--amber-soft:#f6ead3;--red:#a8432f;--shadow:0 1px 2px rgba(60,40,10,.06),0 6px 20px rgba(60,40,10,.06)}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16130f;--paper:#201b15;--ink:#f1e9dc;--mut:#a89c8a;--line:#3a3127;
--green:#7cc49d;--green-soft:#1f3329;--amber:#e0b06a;--amber-soft:#3a2d18;--red:#ec8b77;--shadow:none}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,"PingFang TC","Noto Sans TC",sans-serif;-webkit-font-smoothing:antialiased}}
main{{max-width:720px;margin:0 auto;padding:36px 16px 72px}}
header .eyebrow{{font-size:.78rem;letter-spacing:.24em;color:var(--amber);font-weight:700;margin:0 0 6px}}
h1{{font:900 clamp(1.7rem,6vw,2.3rem)/1.25 "Noto Serif TC",serif;margin:0 0 10px}}
.lede{{color:var(--mut);margin:0 0 18px}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 14px;font-size:.85rem;color:var(--mut);margin-bottom:12px}}
.legend i{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:0}}
.toggle{{font:inherit;font-size:.9rem;padding:8px 14px;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;cursor:pointer}}
.toggle[aria-pressed=true]{{border-color:var(--amber);color:var(--amber)}}
h2.wk{{font-weight:700;font-size:.85rem;line-height:1;color:var(--mut);letter-spacing:.06em;margin:30px 0 10px;display:flex;gap:10px;align-items:center}}
h2.wk span:not(:empty){{color:var(--ink);font-weight:800}}
h2.wk::after{{content:"";flex:1;height:1px;background:var(--line)}}
.day{{display:flex;gap:16px;background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin:0 0 10px;box-shadow:var(--shadow)}}
.day.full{{background:transparent;box-shadow:none;opacity:.72}}
.day.today{{border-color:var(--amber)}}
.date{{flex:none;width:58px;text-align:center;padding-top:2px}}
.date b{{display:block;font:900 1.9rem/1 "Noto Serif TC",serif}}
.date span{{display:block;font-size:.72rem;color:var(--mut);margin-top:6px;white-space:nowrap}}
.body{{flex:1;min-width:0}}
.top{{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}}
.chip{{display:inline-block;line-height:1.5;font-size:.74rem;font-weight:700;padding:3px 9px;border-radius:999px;letter-spacing:.04em}}
.chip.ok{{background:var(--green-soft);color:var(--green)}}.chip.dt{{background:var(--amber-soft);color:var(--amber)}}
.chip.full{{background:transparent;color:var(--mut);border:1px solid var(--line)}}.chip.now{{background:var(--ink);color:var(--paper)}}
.slots{{display:flex;flex-wrap:wrap;gap:8px}}
.slot{{font-family:inherit;font-weight:700;font-size:.98rem;line-height:1;font-variant-numeric:tabular-nums;padding:11px 16px;min-width:76px;border-radius:12px;border:1.5px solid var(--green);
background:var(--paper);color:var(--green);cursor:pointer;transition:transform .12s,background .12s}}
.slot:hover{{background:var(--green-soft)}}.slot:active{{transform:scale(.96)}}
.slot small{{display:block;font-size:.72rem;font-weight:600;margin-top:4px;opacity:.85}}
.pickt{{display:flex;flex-direction:column;gap:6px;font-size:.88rem;color:var(--mut);margin:10px 0 6px}}
.pickt select{{font:inherit;font-size:1.15rem;font-weight:700;padding:10px 12px;border-radius:12px;border:1.5px solid var(--green);background:var(--bg);color:var(--ink)}}
.slot.dayt{{display:none;border-color:var(--amber);color:var(--amber)}}.slot.dayt:hover{{background:var(--amber-soft)}}
body.showday .slot.dayt{{display:inline-block}}
.day.dayonly .slots{{display:none}}body.showday .day.dayonly .slots{{display:flex}}
details{{margin-top:10px;font-size:.88rem}}summary{{cursor:pointer;color:var(--mut);list-style:none}}
summary::-webkit-details-marker{{display:none}}summary::before{{content:"＋ "}}details[open] summary::before{{content:"－ "}}
.day.full details summary{{color:var(--ink)}}
.busy{{list-style:none;margin:8px 0 0;padding:0}}
.busy li{{display:flex;gap:12px;padding:6px 0;border-top:1px dashed var(--line)}}
.busy time{{flex:none;width:96px;color:var(--mut);font-variant-numeric:tabular-nums}}
.busy li span{{flex:1;min-width:0}}
.cx{{flex:none;font:inherit;font-size:.78rem;padding:3px 10px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--red);cursor:pointer}}
.cx:hover{{border-color:var(--red)}}.cx:disabled{{opacity:.5;cursor:wait}}
.busy em{{font-style:normal;font-size:.75rem;color:var(--amber);margin-left:6px}}
.foot{{color:var(--mut);font-size:.82rem;margin-top:28px;text-align:center}}
dialog{{border:0;border-radius:20px;padding:0;width:min(440px,calc(100% - 32px));background:var(--paper);color:var(--ink);box-shadow:0 20px 60px rgba(0,0,0,.25)}}
dialog::backdrop{{background:rgba(30,20,10,.45);backdrop-filter:blur(2px)}}
.sheet{{padding:22px 20px 20px}}
.sheet .when{{font-size:.8rem;letter-spacing:.18em;color:var(--amber);font-weight:700;margin:0}}
.sheet h3{{font:900 1.5rem/1.3 "Noto Serif TC",serif;margin:4px 0 4px}}
.sheet p.hint{{color:var(--mut);font-size:.88rem;margin:0 0 16px}}
.types{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.type{{font:inherit;text-align:left;padding:14px;border-radius:14px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer;transition:border-color .12s,transform .12s}}
.type:hover{{border-color:var(--green)}}.type:active{{transform:scale(.97)}}
.type b{{display:block;font-size:1.05rem}}.type small{{display:block;color:var(--mut);font-size:.78rem;margin-top:3px}}
.type.main{{grid-column:1/-1;background:var(--green);border-color:var(--green);color:#fff}}
.type.main small{{color:rgba(255,255,255,.82)}}.type.main:hover{{filter:brightness(1.08)}}
.type:disabled{{opacity:.5;cursor:wait}}
.close{{margin-top:14px;width:100%;font:inherit;padding:10px;border:0;background:transparent;color:var(--mut);cursor:pointer}}
.done{{text-align:center;padding:8px 0 4px}}.done .ic{{font-size:2.4rem}}
#err{{color:var(--red);font-size:.88rem;min-height:1.2em;margin:10px 0 0}}
@media (max-width:420px){{.day{{gap:12px;padding:12px}}.date{{width:46px}}.date b{{font-size:1.6rem}}.slot{{min-width:68px;padding:10px 12px}}}}
</style></head><body><main>
<header>
<p class="eyebrow">大樹教練 ‧ 可約時間</p>
<h1>挑一段空檔，<br>選您要的那一個小時。</h1>
<p class="lede">未來 {DAYS} 天，晚上 {escape(eve['start'])}–{escape(eve['end'])} 優先。綠色是整段有空的時間，點下去選想要的一個小時（例如 19:30–20:30），再選類型就送出；前後訪談會自動留 30 分鐘緩衝，教練確認後就排定。</p>
<div class="legend"><span><i style="background:var(--green)"></i>晚上可約（{n_open} 天）</span><span><i style="background:var(--amber)"></i>白天時段</span><span><i style="background:var(--line)"></i>已排滿</span></div>
<button type="button" class="toggle" id="dt" aria-pressed="false">也看白天時段</button>
</header>
{''.join(cards)}
<p class="foot">本頁隨教練行程即時更新 ‧ 行程更新：{updated}</p>
</main>
<dialog id="dlg" aria-labelledby="pick"><div class="sheet" id="sheet">
<p class="when">預約時段</p><h3 id="pick"></h3>
<label class="pickt">要哪一個小時<select id="st"></select></label>
<p class="hint">選好時間，再選一個類型，按下就送出。</p>
<div class="types">{types_html}</div><p id="err" role="alert"></p>
<button type="button" class="close" id="x">取消</button></div></dialog>
<script>
var cur=null,dlg=document.getElementById('dlg'),sheet=document.getElementById('sheet'),orig=sheet.innerHTML,dt=document.getElementById('dt');
dt.onclick=function(){{var on=document.body.classList.toggle('showday');dt.setAttribute('aria-pressed',on);dt.textContent=on?'只看晚上':'也看白天時段';}};
function bind(){{
 document.getElementById('x').onclick=function(){{dlg.close()}};
 sheet.querySelectorAll('.type').forEach(function(b){{b.onclick=function(){{book(b.dataset.type)}}}});
}}
function hm(m){{return ('0'+Math.floor(m/60)).slice(-2)+':'+('0'+m%60).slice(-2)}}
document.querySelectorAll('.slot').forEach(function(b){{b.onclick=function(){{
 var a=+b.dataset.a,z=+b.dataset.b,ts=[];for(var t=a;t+60<=z;t+={STEP})ts.push(t);if(ts[ts.length-1]!==z-60)ts.push(z-60);
 cur={{d:b.dataset.d,l:b.dataset.l}};sheet.innerHTML=orig;bind();
 document.getElementById('pick').textContent=b.dataset.l+' '+hm(a)+'–'+hm(z)+' 有空檔';
 document.getElementById('st').innerHTML=ts.map(function(t){{return '<option value="'+hm(t)+'">'+hm(t)+'–'+hm(t+60)+'</option>'}}).join('');
 if(dlg.showModal)dlg.showModal();else dlg.setAttribute('open','');}}}});
document.querySelectorAll('.cx').forEach(function(b){{b.onclick=function(){{
 if(!confirm('確定要取消這筆行程嗎？\\n\\n'+b.dataset.l+'\\n\\n取消後教練 Google 日曆裡我們寫過的那一筆也會一起刪掉。'))return;
 b.disabled=true;b.textContent='取消中…';
 fetch('/schedule/{token}/cancel',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{id:b.dataset.id,date:b.dataset.d}})}})
 .then(function(r){{return r.json()}}).then(function(j){{if(j.ok)location.reload();else{{alert(j.error||'取消失敗，請稍後再試');b.disabled=false;b.textContent='取消'}}}})
 .catch(function(){{alert('網路異常，請稍後再試');b.disabled=false;b.textContent='取消'}});}}}});
dlg.addEventListener('click',function(e){{if(e.target===dlg)dlg.close()}});
dlg.addEventListener('close',function(){{if(sheet.dataset.ok)location.reload()}});
function book(type){{
 var err=document.getElementById('err'),st=document.getElementById('st').value;cur.t=st;
 var m=+st.slice(0,2)*60+ +st.slice(3);cur.l=cur.l.split(' ')[0]+' '+st+'–'+hm(m+60);
 sheet.querySelectorAll('.type').forEach(function(x){{x.disabled=true}});err.textContent='送出中…';
 fetch('/schedule/{token}/book',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{date:cur.d,start:st,type:type}})}})
 .then(function(r){{return r.json()}}).then(function(j){{
  if(j.ok){{sheet.dataset.ok='1';sheet.innerHTML='<div class="done"><div class="ic">✅</div><p class="when">已送出</p><h3></h3><p class="hint"></p></div><button type="button" class="close" id="x">完成</button>';
   sheet.querySelector('h3').textContent=type;sheet.querySelector('.hint').textContent=cur.l+'　等教練確認後就排定。';
   document.getElementById('x').onclick=function(){{dlg.close()}};}}
  else{{err.textContent=j.error||'送出失敗，請稍後再試';sheet.querySelectorAll('.type').forEach(function(x){{x.disabled=false}})}}}})
 .catch(function(){{err.textContent='網路異常，請稍後再試';sheet.querySelectorAll('.type').forEach(function(x){{x.disabled=false}})}});
}}
</script></body></html>"""
