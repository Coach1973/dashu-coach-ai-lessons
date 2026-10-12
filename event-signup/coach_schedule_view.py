"""教練行程頁（2026-10-12）：只有拿到網址（含一段隨機代碼）的人看得到。

資料來源＝workspace/knowledges/教練行程總表.json（scripts/coach_schedule.py 維護），每次開頁即時讀，行程一改頁面就跟著變。
對外只顯示「哪些時段已有安排／可約的晚上時段」，不顯示行程內容與地點（隱私）。
代碼放在 workspace/state/coach_schedule_token.txt；要換網址就改這個檔（舊網址立即失效）。
"""
import datetime as dt
import fcntl
import hmac
import json
import os
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


def token_ok(token: str) -> bool:
    try:
        real = TOKEN_FILE.read_text().strip()
    except OSError:
        return False
    return bool(real) and hmac.compare_digest(real, token or "")


def _hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def _fmt(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def _busy(d, data):
    iso = d.isoformat()
    out = []
    for e in data.get("events", []):
        if e["date"] <= iso <= e.get("end_date", e["date"]):
            out.append((0, 1440, e) if e.get("allday") else (_hm(e["start"]), _hm(e["end"]), e))
    for r in data.get("recurring", []):
        if d.weekday() != r["weekday"]:
            continue
        if r.get("since") and iso < r["since"]:
            continue
        if r.get("until") and iso > r["until"]:
            continue
        if iso in r.get("skip", []):
            continue
        out.append((_hm(r["start"]), _hm(r["end"]), r))
    return sorted(out, key=lambda x: x[0])


def _free(busy, ws, we):
    cur, slots = ws, []
    for s, e, _ in busy:
        if e <= cur or s >= we:
            continue
        if s - cur >= 60:
            slots.append((cur, min(s, we)))
        cur = max(cur, e)
    if we - cur >= 60:
        slots.append((cur, we))
    return slots


def _starts(slots):
    """每個可約區間，每小時一個起點，一場 1 小時"""
    out = []
    for a, b in slots:
        t = a
        while t + 60 <= b:
            out.append(t)
            t += 60
    return out


def book(date_s, start_s, name, contact, topic):
    """預約一個 1 小時時段：寫成「待確認」的訪談行程（先占位，教練確認或取消）。
    回傳 (ok, 訊息或事件)。伺服器端重新檢查，不信任網頁送來的時段。"""
    name, contact, topic = (name or "").strip()[:40], (contact or "").strip()[:80], (topic or "").strip()[:200]
    if not name or not contact:
        return False, "請填寫姓名與聯絡方式"
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
        win = data.get("interview_window", {"start": "19:00", "end": "22:00"})
        busy = _busy(d, data)
        if st not in _starts(_free(busy, _hm(win["start"]), _hm(win["end"]))):
            return False, "這個時段剛剛被預約走了，請選別的時間"
        ev = {"id": uuid.uuid4().hex[:8], "date": d.isoformat(), "start": _fmt(st), "end": _fmt(st + 60),
              "title": f"訪談預約（待確認）：{name}", "source": "預約頁", "kind": "interview", "tentative": True,
              "note": f"聯絡：{contact}" + (f"｜主題：{topic}" if topic else "")}
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


def render(token: str = "") -> str:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    win = data.get("interview_window", {"start": "19:00", "end": "22:00"})
    ws, we = _hm(win["start"]), _hm(win["end"])
    today = dt.datetime.now(TZ).date()
    rows = []
    for i in range(DAYS):
        d = today + dt.timedelta(days=i)
        busy = _busy(d, data)
        btns = ""
        label = f"{d.month}/{d.day}（{WEEK[d.weekday()]}）"
        if any((s, e) == (0, 1440) for s, e, _ in busy):
            status = '<span class="no">整天不方便</span>'
            free = ""
            cls = "off"
        else:
            slots = _free(busy, ws, we)
            tentative = any(ev.get("tentative") for _, _, ev in busy)
            if slots:
                btns = "".join(
                    f'<button type="button" class="slot" data-d="{d.isoformat()}" data-t="{_fmt(t)}" '
                    f'data-l="{escape(label)} {_fmt(t)}–{_fmt(t + 60)}">{_fmt(t)}</button>'
                    for t in _starts(slots)
                )
                free = "__BTNS__"
                status = '<span class="ok">晚上可約</span>'
                cls = "on"
            else:
                free, status, cls = "", '<span class="no">晚上已滿</span>', "off"
            if tentative and slots:
                status += ' <span class="tn">部分待確認</span>'
        busy_txt = "、".join(
            ("整天" if (s, e) == (0, 1440) else f"{_fmt(s)}–{_fmt(e)}") for s, e, _ in busy
        ) or "—"
        rows.append(
            f'<tr class="{cls}"><td class="d">{escape(label)}</td><td>{status}</td>'
            f'<td class="f">{(btns if free == "__BTNS__" else "—")}</td><td class="b">{escape(busy_txt)}</td></tr>'
        )
    updated = escape(str(data.get("updated_at", "")))
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>大樹教練｜可約時間</title>
<style>
:root{{--bg:#faf8f4;--fg:#222;--mut:#777;--card:#fff;--line:#e6e1d8;--ok:#1a7f4b;--no:#b3261e;--tn:#9a6b00}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141414;--fg:#eee;--mut:#999;--card:#1e1e1e;--line:#333;--ok:#5fd08f;--no:#ff8a80;--tn:#ffcc66}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,"PingFang TC","Noto Sans TC",sans-serif}}
main{{max-width:760px;margin:0 auto;padding:24px 16px 48px}}
h1{{font-size:1.4rem;margin:0 0 4px}}p.s{{color:var(--mut);margin:0 0 18px;font-size:.92rem}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:.8rem;color:var(--mut);font-weight:600}}tr:last-child td{{border-bottom:0}}
td.d{{white-space:nowrap;font-weight:600}}td.b{{color:var(--mut);font-size:.88rem}}
.ok{{color:var(--ok);font-weight:600}}.no{{color:var(--no)}}.tn{{color:var(--tn);font-size:.8rem}}
tr.off td.d{{color:var(--mut)}}
@media (max-width:560px){{th:nth-child(4),td.b{{display:none}}}}
.n{{color:var(--mut);font-size:.85rem;margin-top:14px}}
.slot{{font:inherit;padding:6px 12px;margin:2px 6px 2px 0;border:1px solid var(--ok);color:var(--ok);background:transparent;border-radius:999px;cursor:pointer}}
.slot:hover,.slot.sel{{background:var(--ok);color:var(--bg)}}
#f{{display:none;margin-top:16px;padding:16px;background:var(--card);border:1px solid var(--line);border-radius:12px}}
#f h2{{font-size:1.05rem;margin:0 0 10px}}#f label{{display:block;font-size:.88rem;color:var(--mut);margin-top:10px}}
#f input,#f textarea{{width:100%;font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg)}}
#f button.go{{margin-top:14px;width:100%;font:inherit;font-weight:600;padding:12px;border:0;border-radius:10px;background:var(--ok);color:var(--bg);cursor:pointer}}
#msg{{margin-top:10px}}.hp{{position:absolute;left:-9999px}}
</style></head><body><main>
<h1>大樹教練｜訪談可約時間</h1>
<p class="s">未來 {DAYS} 天。訪談預設在晚上 {escape(win['start'])}–{escape(win['end'])}，一場約 1 小時。</p>
<div class="box"><table>
<tr><th>日期</th><th>狀態</th><th>點選時間預約</th><th>已有安排</th></tr>
{''.join(rows)}
</table></div>
<form id="f" autocomplete="off">
<h2>預約：<span id="pick"></span></h2>
<label>您的姓名<input name="name" required maxlength="40"></label>
<label>聯絡方式（電話、LINE 或 Email）<input name="contact" required maxlength="80"></label>
<label>訪談主題（選填）<textarea name="topic" rows="2" maxlength="200"></textarea></label>
<input class="hp" name="website" tabindex="-1" aria-hidden="true">
<button class="go" type="submit">送出預約</button><div id="msg"></div>
</form>
<p class="n">點上面的時間按鈕即可預約，送出後教練會收到通知；教練確認後才算排定，我們會再與您聯繫。本頁隨教練行程即時更新（行程更新：{updated}）。</p>
</main>
<script>
var cur=null,f=document.getElementById('f'),msg=document.getElementById('msg');
document.querySelectorAll('.slot').forEach(function(b){{b.onclick=function(){{
 document.querySelectorAll('.slot.sel').forEach(function(x){{x.classList.remove('sel')}});
 b.classList.add('sel');cur={{d:b.dataset.d,t:b.dataset.t}};
 document.getElementById('pick').textContent=b.dataset.l;f.style.display='block';msg.textContent='';
 f.scrollIntoView({{behavior:'smooth',block:'center'}});}}}});
f.onsubmit=function(e){{e.preventDefault();if(!cur)return;
 var fd=new FormData(f),btn=f.querySelector('.go');btn.disabled=true;msg.textContent='送出中…';
 fetch('/schedule/{token}/book',{{method:'POST',headers:{{'Content-Type':'application/json'}},
  body:JSON.stringify({{date:cur.d,start:cur.t,name:fd.get('name'),contact:fd.get('contact'),topic:fd.get('topic'),website:fd.get('website')}})}})
 .then(function(r){{return r.json()}}).then(function(j){{
  if(j.ok){{f.innerHTML='<h2>✅ 已收到預約</h2><p>'+j.label+'<br>教練確認後會與您聯繫，謝謝！</p>'}}
  else{{msg.textContent=j.error||'送出失敗，請稍後再試';btn.disabled=false}}}})
 .catch(function(){{msg.textContent='網路異常，請稍後再試';btn.disabled=false}})}};
</script></body></html>"""
