"""榮樹下來賓資料表＋AI 來賓卡（2026-10-14 教練：工作量太多，來賓背景整理與訪綱交給 AI）

流程：裕榮在 LINE 群組登記訪談對象（coach_schedule.py set-guest）→ 那場訪談拿到一組 form_token，
群組回覆附上「來賓資料表」網址 → 裕榮轉給來賓填 → 送出後 AI（MiniMax）產出來賓卡 →
巴哈助理群組收到「來賓卡完成」＋簽章網址，教練開來看 3 分鐘即可。

網址：
  /rongtree/guest/<token>                 來賓填表（拿到網址的人才進得來，不用登入）
  /rongtree/guest/<token>/card?k=<簽章>   AI 來賓卡（給教練與主持人）
  /rongtree/cards?k=<簽章>                全部來賓卡列表（後台，已收進大樹作品集）
"""
import base64
import hashlib
import hmac
import html
import json
import re
import subprocess
import threading
import urllib.request
from pathlib import Path

import db

WS = Path.home() / ".openclaw" / "workspace"
SCHEDULE = WS / "knowledges" / "教練行程總表.json"
UPLOAD_DIR = Path(__file__).resolve().parent / "rongtree_uploads"
KEY_FILE = WS / "state" / "minimax_api_key"   # 不進 git（.gitignore）
MINIMAX_URL = "https://api.minimax.io/anthropic/v1/messages"
MAX_PHOTO = 1_600_000
TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{8,40}$")
NODE = "/Users/bymyway/.nvm/versions/node/v24.21.0/bin/node"
OPENCLAW = "/Users/bymyway/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw/openclaw.mjs"
BAHA_GROUP = "-5115910257"

# (欄位, 標題, 型態, 必填, 提示)
FIELDS = [
    ("name", "姓名", "text", True, ""),
    ("title", "公司／職稱", "text", True, "例：順發電腦 董事長"),
    ("contact", "聯絡電話或 Email", "text", True, "節目上架時通知您"),
    ("intro", "一段自我介紹", "area", True, "主持人開場會用，100～200 字即可"),
    ("turns", "人生中最重要的三個轉折", "area", True, "每行一個，例：38 歲離開金融業，轉做照明"),
    ("story", "您的公益故事", "area", True, "為什麼開始、做了哪些事、最難忘的一刻"),
    ("action", "希望透過節目推動的事", "area", False, "想邀請聽眾一起做什麼？例：報名 Run for Future、支持某個公益團體"),
    ("links", "可公開的網站或社群連結", "area", False, "每行一個"),
    ("avoid", "不希望在節目中談到的話題", "area", False, "我們會避開"),
    ("invite", "想推薦誰坐上「樹蔭席」", "area", False, "願意為公益出一份力的朋友，選填"),
]


# ---------- 簽章 ----------
def _sig(secret: str, msg: str) -> str:
    return hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()[:24]


def card_sig(secret, token):
    return _sig(secret, f"rongtree-card:{token}")


def list_sig(secret):
    return _sig(secret, "rongtree-cards")


def card_url(secret, token):
    return f"https://event.bymyway.com/rongtree/guest/{token}/card?k={card_sig(secret, token)}"


def list_code(secret):
    return list_sig(secret)[:12]


def list_url(secret):
    """後台短網址（教練：後台網址一律短址）；舊的 /rongtree/cards?k=… 長連結照樣有效。"""
    return f"https://event.bymyway.com/rongtree/a/{list_code(secret)}"


# ---------- 資料 ----------
def find_event(token: str):
    if not TOKEN_RE.match(token or ""):
        return None
    try:
        data = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    return next((e for e in data.get("events", []) if e.get("form_token") == token), None)


def _conn():
    conn = db.get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS rongtree_guest_forms ("
        " token TEXT PRIMARY KEY, event_id TEXT, date TEXT, start TEXT, guest TEXT,"
        " data TEXT NOT NULL, photo_file TEXT, card TEXT, card_status TEXT NOT NULL DEFAULT 'pending',"
        " ip TEXT, created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        " updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))"
    )
    if "public" not in [c[1] for c in conn.execute("PRAGMA table_info(rongtree_guest_forms)")]:
        # 2026-10-14 教練：交了資料的來賓公開列在榮樹下網頁；有人亂填可在來賓卡頁按「從公開名單隱藏」
        conn.execute("ALTER TABLE rongtree_guest_forms ADD COLUMN public INTEGER NOT NULL DEFAULT 1")
    return conn


def get_form(token):
    conn = _conn()
    r = conn.execute("SELECT * FROM rongtree_guest_forms WHERE token=?", (token,)).fetchone()
    conn.close()
    return r


def all_forms():
    conn = _conn()
    rows = conn.execute("SELECT token, date, start, guest, card_status, updated_at FROM rongtree_guest_forms "
                        "ORDER BY date DESC, start DESC").fetchall()
    conn.close()
    return rows


# ---------- 公開名單（榮樹下網頁「訪談嘉賓前置作業」區，2026-10-14 教練：誰交了資料公開一目了然）----------
# 只公開：姓名、公司職稱、照片、一句話介紹、訪談時間。聯絡方式、不談的話題、AI 提醒與訪綱只在簽章來賓卡裡。
SCRIPT = WS / "scripts" / "coach_schedule.py"
_forms_at = {"t": 0.0}


def _ensure_forms():
    """每 5 分鐘最多一次：叫 coach_schedule.py 幫接下來每場訪談配好資料表網址（行程表只由那支腳本寫）。"""
    import time
    if time.time() - _forms_at["t"] < 300:
        return
    _forms_at["t"] = time.time()
    try:
        subprocess.run(["/usr/bin/python3", "-I", str(SCRIPT), "ensure-forms"], capture_output=True, timeout=60)
    except Exception:  # noqa: BLE001
        pass


def _upcoming(days=60):
    import datetime as dt
    tz = dt.timezone(dt.timedelta(hours=8))
    now = dt.datetime.now(tz)
    try:
        data = json.loads(SCHEDULE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return []
    out = []
    for e in data.get("events", []):
        t = e.get("title", "")
        if e.get("allday") or not (e.get("booking_type") == "榮樹下訪談" or t.startswith("榮樹下訪談") or t.startswith("訪談預約（待確認）")):
            continue
        try:
            start = dt.datetime.fromisoformat(f"{e['date']}T{e['start']}:00+08:00")
        except (KeyError, ValueError):
            continue
        if now - dt.timedelta(hours=2) <= start <= now + dt.timedelta(days=days):
            out.append(e)
    return sorted(out, key=lambda e: (e["date"], e["start"]))


def one_liner(r):
    if r["card_status"] == "done" and r["card"]:
        m = re.search(r"##\s*一句話介紹\s*\n+\s*(?:[-*]\s*)?(.+)", r["card"])
        if m:
            return m.group(1).strip()[:90]
    d = json.loads(r["data"])
    return (d.get("intro") or "")[:60]


def public_prep():
    _ensure_forms()
    conn = _conn()
    rows = conn.execute("SELECT * FROM rongtree_guest_forms ORDER BY date DESC, start DESC").fetchall()
    conn.close()
    by_token = {r["token"]: r for r in rows}
    upcoming = []
    for e in _upcoming():
        tok = e.get("form_token")
        r = by_token.get(tok) if tok else None
        upcoming.append({"date": e["date"], "start": e["start"], "end": e.get("end", ""),
                         "tentative": bool(e.get("tentative")),
                         "guest": (json.loads(r["data"])["name"] if r and r["public"] else e.get("guest") or ""),
                         "form": f"/rongtree/guest/{tok}" if tok else "", "submitted": bool(r)})
    guests = []
    for r in rows:
        if not r["public"]:
            continue
        d = json.loads(r["data"])
        guests.append({"name": d.get("name", ""), "title": d.get("title", ""), "line": one_liner(r),
                       "date": r["date"], "start": r["start"],
                       "photo": f"/rongtree/face/{r['token']}.jpg" if r["photo_file"] else ""})
    return {"ok": True, "upcoming": upcoming, "guests": guests}


def set_public(token, public: bool):
    conn = _conn()
    conn.execute("UPDATE rongtree_guest_forms SET public=? WHERE token=?", (1 if public else 0, token))
    conn.commit()
    conn.close()


def save(token, ev, payload, ip):
    """回傳 (ok, 錯誤訊息, 是否第一次交回)。照片可不傳；重送時沒附照片就保留舊照片。"""
    clean = {}
    for key, label, kind, req, _ in FIELDS:
        v = (payload.get(key) or "").strip()
        v = v[:1500] if kind == "area" else re.sub(r"\s+", " ", v)[:80]
        if req and not v:
            return False, f"請填寫「{label}」", False
        clean[key] = v
    if len(re.sub(r"\D", "", clean["contact"])) < 8 and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", clean["contact"]):
        return False, "請填寫正確的電話或 Email", False
    photo_file = None
    photo = payload.get("photo") or ""
    if photo:
        m = re.match(r"^data:image/(jpeg|jpg|png|webp);base64,(.+)$", photo, re.S)
        if not m:
            return False, "照片格式不支援，請換一張 JPG 或 PNG", False
        raw = base64.b64decode(m.group(2), validate=False)
        if len(raw) > MAX_PHOTO or (raw[:3] != b"\xff\xd8\xff" and raw[:8] != b"\x89PNG\r\n\x1a\n" and raw[8:12] != b"WEBP"):
            return False, "照片太大或格式不支援，請換一張", False
        UPLOAD_DIR.mkdir(exist_ok=True)
        photo_file = f"{token}.jpg"
        (UPLOAD_DIR / photo_file).write_bytes(raw)
    conn = _conn()
    old = conn.execute("SELECT photo_file FROM rongtree_guest_forms WHERE token=?", (token,)).fetchone()
    photo_file = photo_file or (old["photo_file"] if old else None)
    conn.execute(
        "INSERT INTO rongtree_guest_forms (token, event_id, date, start, guest, data, photo_file, card_status, ip) "
        "VALUES (?,?,?,?,?,?,?, 'pending', ?) ON CONFLICT(token) DO UPDATE SET "
        "data=excluded.data, photo_file=excluded.photo_file, guest=excluded.guest, date=excluded.date, "
        "start=excluded.start, card_status='pending', ip=excluded.ip, updated_at=datetime('now','localtime')",
        (token, ev.get("id"), ev.get("date"), ev.get("start"), clean["name"],
         json.dumps(clean, ensure_ascii=False), photo_file, ip))
    conn.commit()
    conn.close()
    return True, "", old is None


# ---------- AI 來賓卡 ----------
PROMPT = """你是 Podcast《榮樹下》的節目企劃。節目由邱裕榮（開場、介紹來賓）與吳大樹（主訪）共同主持，
主軸是公益，第一階段任務是推動 2027 年 4 月 18 日第五屆 Run for Future 順發 × 港都公益路跑。
每集另有 3～5 位「樹蔭席」列席嘉賓：他們不評分，聽完向來賓提一個好問題，並承諾自己能出的一份公益資源。

請根據下面「來賓自己填的資料」，用台灣繁體中文寫一張來賓卡，給主持人訪談前 3 分鐘看完。
規則：
- 只能根據資料寫，不可編造任何經歷、數字、頭銜；資料沒有的寫「資料未提供」。
- 金句只能從來賓原文摘錄，不可改寫成新的話。
- 涉及健康、醫療、科技效果、公益成效的說法，在「提醒」裡註明要以「來賓個人經驗」呈現。
- 一集只聚焦一個核心故事。
- 不可推測來賓性別，一律用名字或「來賓」稱呼，不用「她／他／女／男」。
- 來賓列在「不希望在節目中談到的話題」的內容，所有問題（含樹蔭席問題）都不可碰觸。

請照這個格式輸出（Markdown，不要多加其他段落）：
## 一句話介紹
（裕榮開場用，60 字內）
## 背景重點
（3～5 點）
## 本集核心故事
（建議 1 個，並說明為什麼聽眾會有共鳴）
## 三個核心問題
（大樹主訪用，照訪談順序）
## 樹蔭席可以提的好問題
（3 個，例如「你是怎麼熬過最難的時期？」這類有深度的問題）
## 金句候選
## 與公益／Run for Future 的連結點
## 提醒
（不談的話題、需謹慎的說法、資料缺漏）

訪談時間：{when}
來賓資料：
{data}
"""


def _call_minimax(prompt: str) -> str:
    import sys
    sys.path.insert(0, str(WS / "scripts"))
    from minimax_batch_guard import guard_call   # 教練畫的 MiniMax 用量紅線：越線就拋例外不呼叫
    guard_call("rongtree_guest_card")
    key = KEY_FILE.read_text().strip()
    req = urllib.request.Request(MINIMAX_URL, data=json.dumps({
        "model": "MiniMax-M3", "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Content-Type": "application/json", "x-api-key": key, "anthropic-version": "2023-06-01"})
    with urllib.request.urlopen(req, timeout=240) as r:
        res = json.loads(r.read().decode())
    text = "\n".join(b.get("text", "") for b in res.get("content", []) if b.get("type") == "text").strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
    if not text:
        raise RuntimeError("AI 沒有回傳內容")
    return text


def build_card(token):
    """產生來賓卡並存回資料庫；回傳 (ok, 訊息)。"""
    r = get_form(token)
    if not r:
        return False, "找不到資料"
    d = json.loads(r["data"])
    labels = {k: lab for k, lab, *_ in FIELDS}
    data_txt = "\n".join(f"【{labels[k]}】{v}" for k, v in d.items() if v and k != "contact")
    when = f"{r['date']} {r['start']}"
    conn = _conn()
    try:
        card = _call_minimax(PROMPT.format(when=when, data=data_txt))
        conn.execute("UPDATE rongtree_guest_forms SET card=?, card_status='done' WHERE token=?", (card, token))
        ok, msg = True, ""
    except Exception as e:  # noqa: BLE001
        conn.execute("UPDATE rongtree_guest_forms SET card_status='failed' WHERE token=?", (token,))
        ok, msg = False, str(e)[:200]
    conn.commit()
    conn.close()
    return ok, msg


def send_baha(text: str) -> bool:
    try:
        r = subprocess.run([NODE, OPENCLAW, "message", "send", "--channel", "telegram", "--account", "bot_peipei",
                            "--target", BAHA_GROUP, "-m", text], capture_output=True, text=True, timeout=90)
        return r.returncode == 0
    except Exception:  # noqa: BLE001
        return False


def build_card_and_notify(token, secret, fallback_notify, first=True):
    """背景執行：做來賓卡 → 通知巴哈助理群組（送不出去退回活動報名群）。"""
    ok, err = build_card(token)
    r = get_form(token)
    who = r["guest"] if r else "來賓"
    when = f"{r['date']} {r['start']}" if r else ""
    head = f"🎙️ 榮樹下來賓{'交回' if first else '更新'}了資料：{who}（{when} 訪談）"
    body = (f"{head}\nAI 來賓卡已完成，訪談前花 3 分鐘看：\n{card_url(secret, token)}" if ok
            else f"{head}\n⚠️ AI 來賓卡這次沒做出來（{err}），資料已存好，打開下面網址可以按「重新產生」：\n{card_url(secret, token)}")
    if not send_baha(body):
        fallback_notify(body)


def start_card(token, secret, fallback_notify, first=True):
    threading.Thread(target=build_card_and_notify, args=(token, secret, fallback_notify, first), daemon=True).start()


# ---------- 頁面 ----------
E = html.escape
BASE_CSS = """
:root{--ink:#0e1712;--ink-2:#14211a;--paper:#f2ead8;--paper-2:#e8dcc3;--line:#cdbd9c;--on-ink:#efe6d2;--mute:#a7b2a3;
--on-paper:#1d2a22;--on-paper-mute:#5b6656;--amber:#d9a441;--amber-hi:#f0c46a;--amber-deep:#9a6a1c}
*{box-sizing:border-box}body{margin:0;font:400 18px/1.8 "Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;letter-spacing:.02em}
h1,h2,h3{font-family:"Noto Serif TC","Songti TC",serif;margin:0}
.wrap{max-width:760px;margin:0 auto;padding:32px 16px 64px}
"""


def render_form(token, ev, existing):
    d = json.loads(existing["data"]) if existing else {}
    if not d.get("name") and ev.get("guest"):
        d["name"] = ev["guest"]
    when = f"{ev.get('date', '')} {ev.get('start', '')}–{ev.get('end', '')}"
    rows = []
    for key, label, kind, req, ph in FIELDS:
        star = '<span class="req">*</span>' if req else '<span class="opt">選填</span>'
        val = E(d.get(key, ""))
        ctl = (f'<textarea id="{key}" name="{key}" placeholder="{E(ph)}" {"required" if req else ""}>{val}</textarea>'
               if kind == "area" else
               f'<input id="{key}" name="{key}" value="{val}" placeholder="{E(ph)}" {"required" if req else ""}>')
        rows.append(f'<div class="field"><label for="{key}">{E(label)} {star}</label>{ctl}</div>')
    photo_note = "已收到您的照片，若不換可以不用再傳。" if existing and existing["photo_file"] else "節目封面與宣傳會用到，建議清楚的半身照。"
    again = '<p class="again">您先前已填過，修改後再送出一次即可。</p>' if existing else ""
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>榮樹下來賓資料表</title>
<style>{BASE_CSS}
body{{background:var(--ink);color:var(--on-ink)}}
.eyebrow{{color:var(--amber);letter-spacing:.2em;font-weight:500}}
h1{{font-size:clamp(28px,6vw,40px);line-height:1.3;margin:8px 0 12px}}
.lead{{color:var(--mute)}}.when{{display:inline-block;margin:6px 0 20px;padding:6px 14px;border:1px solid var(--amber);border-radius:999px;color:var(--amber-hi)}}
form{{background:rgba(239,230,210,.04);border:1px solid rgba(239,230,210,.14);border-radius:10px;padding:clamp(18px,4vw,32px)}}
.field{{display:flex;flex-direction:column;margin-bottom:18px}}
label{{margin-bottom:6px;color:#d8d6c6}}.req{{color:var(--amber)}}.opt{{color:var(--mute);font-size:15px}}
input,textarea{{font:inherit;color:var(--on-ink);background:rgba(239,230,210,.05);border:1px solid rgba(239,230,210,.25);border-radius:6px;padding:10px 12px;min-height:48px;width:100%}}
textarea{{min-height:110px;resize:vertical}}input:focus,textarea:focus{{outline:none;border-color:var(--amber)}}
.photo small{{color:var(--mute)}}
button{{font:500 19px/1 inherit;min-height:56px;padding:0 32px;border:0;border-radius:999px;background:var(--amber);color:#1a1206;cursor:pointer}}
button:disabled{{opacity:.6}}.msg{{margin-top:14px;min-height:1em;color:#f0a58c}}.again{{color:var(--amber-hi)}}
.consent{{color:var(--mute);font-size:16px;margin:4px 0 16px}}.consent b{{color:var(--on-ink)}}
.done{{display:none;text-align:center;padding:40px 0}}.done h2{{font-size:30px;margin-bottom:12px}}
</style></head><body><div class="wrap">
<p class="eyebrow">榮樹下 Podcast</p>
<h1>謝謝您，願意坐到榕樹下。</h1>
<p class="lead">為了讓訪談聚焦在您最動人的故事，麻煩花 10 分鐘留下以下資料。主持人會在訪談前先讀過，現場就能直接聊到重點。</p>
<span class="when">訪談時間：{E(when)}</span>
{again}
<form id="f" novalidate>
{''.join(rows)}
<div class="field photo"><label for="photo">個人照片 <span class="opt">選填</span></label>
<input type="file" id="photo" accept="image/*"><small>{photo_note}</small></div>
<p class="consent">送出即同意在榮樹下網站公開您的<b>姓名、公司職稱、照片與一句話介紹</b>；聯絡方式與其他內容只給主持人看。</p>
<button type="submit">送出資料</button><p class="msg" id="msg" role="alert"></p>
</form>
<div class="done" id="done" role="status"><h2>已收到，謝謝您！</h2><p class="lead">主持人會在訪談前讀過您的資料。想修改，再打開這個網址重新送出即可。</p></div>
</div>
<script>
(()=>{{
const f=document.getElementById('f'),msg=document.getElementById('msg');
function shrink(file){{return new Promise((ok,no)=>{{const img=new Image();img.onload=()=>{{const s=Math.min(1,1400/Math.max(img.width,img.height));
const c=document.createElement('canvas');c.width=Math.round(img.width*s);c.height=Math.round(img.height*s);c.getContext('2d').drawImage(img,0,0,c.width,c.height);
ok(c.toDataURL('image/jpeg',.85));URL.revokeObjectURL(img.src)}};img.onerror=()=>no();img.src=URL.createObjectURL(file)}})}}
f.addEventListener('submit',async e=>{{
  e.preventDefault();msg.textContent='';
  const miss=[...f.querySelectorAll('[required]')].find(el=>!el.value.trim());
  if(miss){{msg.textContent='還有必填欄位沒填：'+miss.closest('.field').querySelector('label').firstChild.textContent.trim();miss.focus();return}}
  const body={{}};f.querySelectorAll('input[name],textarea[name]').forEach(el=>body[el.name]=el.value);
  const file=document.getElementById('photo').files[0];
  const btn=f.querySelector('button');btn.disabled=true;btn.textContent='送出中…';
  try{{
    if(file)body.photo=await shrink(file);
    const r=await fetch(location.pathname,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(body)}});
    const j=await r.json();
    if(j.ok){{f.style.display='none';document.getElementById('done').style.display='block';scrollTo(0,0)}}
    else msg.textContent=j.error||'送出沒有成功，請再試一次';
  }}catch(_){{msg.textContent='網路不穩，送出沒有成功，請再試一次'}}
  btn.disabled=false;btn.textContent='送出資料';
}});
}})();
</script></body></html>"""


def _md(text: str) -> str:
    """把 AI 回的簡單 Markdown（##、- 、1. 、**粗體**）轉成 HTML。"""
    out, lst = [], None
    for line in text.splitlines():
        s = line.strip()
        m_ul, m_ol = re.match(r"^[-*・]\s+(.*)", s), re.match(r"^\d+[.、)]\s*(.*)", s)
        tag = "ul" if m_ul else "ol" if m_ol else None
        if lst and tag != lst:
            out.append(f"</{lst}>")
            lst = None
        inline = lambda t: re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", E(t))
        if s.startswith("#"):
            out.append(f"<h2>{inline(s.lstrip('#').strip())}</h2>")
        elif tag:
            if not lst:
                out.append(f"<{tag}>")
                lst = tag
            out.append(f"<li>{inline((m_ul or m_ol).group(1))}</li>")
        elif s:
            out.append(f"<p>{inline(s)}</p>")
    if lst:
        out.append(f"</{lst}>")
    return "\n".join(out)


def render_card(token, r, secret):
    d = json.loads(r["data"])
    k = card_sig(secret, token)
    photo = (f'<img class="face" src="/rongtree/guest/{token}/photo.jpg?k={k}" alt="{E(d.get("name", ""))}">'
             if r["photo_file"] else "")
    if r["card_status"] == "done" and r["card"]:
        card_html = _md(r["card"])
    elif r["card_status"] == "pending":
        card_html = "<p class='wait'>AI 正在整理來賓卡，約 1～2 分鐘，請稍後重新整理。</p>"
    else:
        card_html = "<p class='wait'>AI 這次沒有做出來賓卡，請按下方「重新產生」。</p>"
    raw = "".join(f"<dt>{E(lab)}</dt><dd>{E(d.get(key, '')) or '—'}</dd>" for key, lab, *_ in FIELDS)
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>來賓卡：{E(d.get('name', ''))}</title>
<style>{BASE_CSS}
body{{background:var(--paper);color:var(--on-paper)}}
.top{{display:flex;gap:18px;align-items:center;border-bottom:2px solid var(--amber-deep);padding-bottom:18px;margin-bottom:8px}}
.face{{width:96px;height:96px;border-radius:50%;object-fit:cover;border:2px solid var(--amber-deep);flex:none}}
.eyebrow{{color:var(--amber-deep);letter-spacing:.2em}}h1{{font-size:30px;line-height:1.3}}.sub{{color:var(--on-paper-mute)}}
h2{{font-size:21px;margin:26px 0 8px;color:var(--amber-deep)}}ul,ol{{padding-left:1.4em;margin:0}}li{{margin:4px 0}}
.wait{{background:var(--paper-2);padding:16px;border-radius:8px}}
details{{margin-top:36px;border-top:1px dashed var(--line);padding-top:12px}}summary{{cursor:pointer;color:var(--amber-deep)}}
dt{{font-weight:700;margin-top:12px}}dd{{margin:2px 0 0;white-space:pre-wrap}}
.tools{{margin-top:28px;display:flex;gap:12px;flex-wrap:wrap}}
.tools button,.tools a{{font:inherit;padding:10px 20px;border-radius:999px;border:1px solid var(--amber-deep);background:none;color:var(--amber-deep);text-decoration:none;cursor:pointer}}
@media print{{.tools,details summary{{display:none}}details{{display:block}}}}
</style></head><body><div class="wrap">
<div class="top">{photo}<div><p class="eyebrow">榮樹下來賓卡</p><h1>{E(d.get('name', ''))}</h1>
<p class="sub">{E(d.get('title', ''))}｜訪談 {E(r['date'] or '')} {E(r['start'] or '')}｜{'榮樹下網頁公開中' if r['public'] else '已從公開名單隱藏'}</p></div></div>
{card_html}
<details><summary>來賓填寫的原始資料</summary><dl>{raw}</dl></details>
<div class="tools">
<form method="post" action="/rongtree/guest/{token}/card/regen?k={k}"><button>重新產生來賓卡</button></form>
<form method="post" action="/rongtree/guest/{token}/card/public?k={k}"><input type="hidden" name="public" value="{0 if r['public'] else 1}"><button>{'從公開名單隱藏' if r['public'] else '恢復公開'}</button></form>
<a href="/rongtree/guest/{token}" target="_blank" rel="noopener">來賓填表頁</a>
<button onclick="print()">列印</button></div>
<p class="sub" style="margin-top:24px;font-size:15px">AI 依來賓自填資料整理，訪談前請自行確認內容。最後更新：{E(r['updated_at'])}</p>
</div></body></html>"""


def render_list(secret):
    status_txt = {"done": "✅ 來賓卡完成", "pending": "⏳ 整理中", "failed": "⚠️ 需重新產生"}
    rows = "".join(
        f"<tr><td>{E(r['date'] or '')} {E(r['start'] or '')}</td><td>{E(r['guest'] or '')}</td>"
        f"<td>{status_txt.get(r['card_status'], r['card_status'])}</td>"
        f"<td><a href='/rongtree/guest/{r['token']}/card?k={card_sig(secret, r['token'])}'>打開</a></td></tr>"
        for r in all_forms()) or "<tr><td colspan='4'>還沒有來賓交回資料。裕榮在 LINE 群組登記訪談對象後，群組回覆會附上來賓資料表網址。</td></tr>"
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>榮樹下來賓卡</title><style>{BASE_CSS}
body{{background:var(--paper);color:var(--on-paper)}}h1{{font-size:30px;margin-bottom:6px}}.sub{{color:var(--on-paper-mute)}}
table{{width:100%;border-collapse:collapse;margin-top:20px}}td,th{{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
a{{color:var(--amber-deep)}}</style></head><body><div class="wrap">
<h1>榮樹下來賓卡</h1><p class="sub">來賓交回資料表後，AI 自動整理的來賓卡都在這裡。</p>
<table><thead><tr><th>訪談時間</th><th>來賓</th><th>狀態</th><th></th></tr></thead><tbody>{rows}</tbody></table>
</div></body></html>"""
