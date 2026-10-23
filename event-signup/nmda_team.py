"""中華新媒體影音發展協會（NMDA）：理監事團隊頁（2026-10-23 教練交辦）

照 tut_team.py（南應大理監事/顧問團隊）同一套機制複製，只換資料、文字與色系，南應大那套不動：
  名單先放「空座位」，本人（或教練的建置模式）點進去補照片、職稱、簡介 → 立刻上架。
公開頁是 NMDA 網站自己的靜態頁 github_repos/nmda/team.html，載入時讀 /api/nmda/team/board（資料只有一份，在資料庫）。

網址：
  /api/nmda/team/board           公開頁讀的資料（CORS *、no-store；?build=簽章碼 多給每人編輯網址）
  /nmda/team/join                我要建立檔案（名單上有名字的先點名字）
  /nmda/team/claim/<id>   POST   認領空座位 → 轉到自己的修改頁
  /nmda/team/edit/<token>        本人專屬修改連結（含刪除）
  /nmda/team/photo/<檔名>         照片
  /nmda/team/a/<code>            管理後台（簽章短址）：隱藏／刪除／新增空座位
  /nmda/b/<code>                 教練的建置模式短網址 → /curated/nmda/team.html?build=<code>
色系：NMDA 官網的紅黑米色（#b3221d / #171714 / #f3efe6）。
"""
import hashlib
import hmac
import html
import os
import re
import secrets
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

import db

UPLOAD_DIR = Path(__file__).resolve().parent / "nmda_team_uploads"
MAX_UPLOAD = 12_000_000
MAX_EDGE = 900
PHOTO_RE = re.compile(r"^[0-9a-f]{16}\.jpg$")
SITE = "https://event.bymyway.com"
PAGE_URL = f"{SITE}/curated/nmda/team.html"
TITLE = "中華新媒體影音發展協會"
ROLE_ORDER = ["理事長", "副理事長", "常務理事", "理事", "常務監事", "監事召集人", "監事", "創會長", "秘書長", "總幹事", "執行長", "顧問"]
LINKS = [("link_web", "網站"), ("link_fb", "Facebook"), ("link_ig", "Instagram"), ("link_line", "LINE")]
FIELDS = ["role", "name", "company_title", "bio"] + [k for k, _ in LINKS]
LIMITS = {"role": 20, "name": 30, "company_title": 60, "bio": 800,
          "link_web": 300, "link_fb": 300, "link_ig": 300, "link_line": 300}

# 教練 2026-10-23 先放的兩個名字，其餘名單之後由教練貼、或本人自己建立。職稱、簡介、照片都先空著，不替本人編。
BOARD_SEATS = ["陳佩君", "吳大樹"]

E = html.escape


# ---------- 資料 ----------
def _conn():
    conn = db.get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS nmda_team_members ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT NOT NULL DEFAULT '',"
        " name TEXT NOT NULL, company_title TEXT NOT NULL DEFAULT '',"
        " bio TEXT NOT NULL DEFAULT '', photo_file TEXT, link_web TEXT NOT NULL DEFAULT '',"
        " link_fb TEXT NOT NULL DEFAULT '', link_ig TEXT NOT NULL DEFAULT '', link_line TEXT NOT NULL DEFAULT '',"
        " edit_token TEXT NOT NULL UNIQUE, filled INTEGER NOT NULL DEFAULT 1, hidden INTEGER NOT NULL DEFAULT 0,"
        " sort INTEGER NOT NULL DEFAULT 999, ip TEXT,"
        " created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        " updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))"
    )
    return conn


def seed_seats():
    """第一次用到時放好空座位；表裡已經有任何資料就不再動（不會重複、不會蓋掉本人填的）。"""
    conn = _conn()
    if not conn.execute("SELECT 1 FROM nmda_team_members LIMIT 1").fetchone():
        for i, name in enumerate(BOARD_SEATS):
            conn.execute("INSERT INTO nmda_team_members (name, edit_token, filled, sort) VALUES (?, ?, 0, ?)",
                         (name, secrets.token_urlsafe(16), i))
        conn.commit()
    conn.close()


def _rank(r):
    role = r["role"] or ""
    idx = next((i for i, k in enumerate(ROLE_ORDER) if k in role), len(ROLE_ORDER))
    return (idx, r["sort"], r["id"])


def list_members(include_hidden=False):
    seed_seats()
    conn = _conn()
    rows = conn.execute("SELECT * FROM nmda_team_members" + ("" if include_hidden else " WHERE hidden=0")).fetchall()
    conn.close()
    return sorted(rows, key=_rank)


def board_public(build=""):
    """公開頁用的資料。一般訪客只有公開欄位（不含修改連結、IP）；build＝教練的建置模式簽章短碼，對了才多給每人的編輯網址。"""
    out = []
    for r in list_members():
        item = {"id": r["id"], "filled": bool(r["filled"]), "name": r["name"], "role": r["role"],
                "title": r["company_title"], "bio": r["bio"],
                "photo": f"{SITE}/nmda/team/photo/{r['photo_file']}" if r["photo_file"] else "",
                "links": [{"label": lab, "url": r[k]} for k, lab in LINKS if r[k]]}
        if build:
            item["edit"] = f"{SITE}/nmda/team/edit/{r['edit_token']}?build={build}"
        out.append(item)
    return out


def get_by_token(token):
    if not token or len(token) > 64:
        return None
    conn = _conn()
    r = conn.execute("SELECT * FROM nmda_team_members WHERE edit_token=?", (token,)).fetchone()
    conn.close()
    return r


def get_by_id(mid):
    conn = _conn()
    r = conn.execute("SELECT * FROM nmda_team_members WHERE id=?", (mid,)).fetchone()
    conn.close()
    return r


def open_seats():
    return [r for r in list_members() if not r["filled"]]


def _norm_link(key, v):
    v = v.strip()
    if not v:
        return ""
    if key == "link_line" and not re.match(r"^https?://", v, re.I):
        return "https://line.me/ti/p/~" + re.sub(r"[^\w.@-]", "", v.lstrip("@"))
    if not re.match(r"^https?://", v, re.I):
        v = "https://" + v
    return v if re.match(r"^https?://[^\s<>\"']+$", v) else ""


def clean_form(form, need_photo, partial=False):
    """回傳 (資料 dict, 錯誤訊息)。partial＝教練的建置模式，只要有姓名就收，其他之後補。"""
    d = {}
    for k in FIELDS:
        v = (form.get(k) or "").strip()
        v = v[:LIMITS.get(k, 20)] if k == "bio" else re.sub(r"\s+", " ", v)[:LIMITS.get(k, 20)]
        d[k] = _norm_link(k, v) if k.startswith("link_") else v
    if partial:
        return d, ("" if d["name"] else "請填寫「姓名」")
    for k, label in (("name", "姓名"), ("company_title", "公司／職稱"), ("bio", "個人簡介")):
        if not d[k]:
            return d, f"請填寫「{label}」"
    if need_photo:
        return d, "請上傳一張照片"
    return d, ""


def save_photo(file_storage):
    """驗證是真的圖片、轉正、縮圖存 jpg；回傳檔名，失敗回 None。"""
    return _save_image_bytes(file_storage.read(MAX_UPLOAD + 1))


def _save_image_bytes(data):
    if not data or len(data) > MAX_UPLOAD:
        return None
    try:
        img = Image.open(BytesIO(data))
        img.load()
    except (UnidentifiedImageError, OSError):
        return None
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    img.thumbnail((MAX_EDGE, MAX_EDGE))
    UPLOAD_DIR.mkdir(exist_ok=True)
    name = f"{os.urandom(8).hex()}.jpg"
    img.save(UPLOAD_DIR / name, "JPEG", quality=85)
    return name


def insert(d, photo_file, ip):
    token = secrets.token_urlsafe(16)
    conn = _conn()
    conn.execute(
        f"INSERT INTO nmda_team_members ({', '.join(FIELDS)}, photo_file, edit_token, filled, ip)"
        f" VALUES ({', '.join('?' * len(FIELDS))}, ?, ?, 1, ?)",
        [d[k] for k in FIELDS] + [photo_file, token, ip])
    conn.commit()
    conn.close()
    return token


def update(mid, d, photo_file):
    conn = _conn()
    sets = ", ".join(f"{k}=?" for k in FIELDS)
    conn.execute(f"UPDATE nmda_team_members SET {sets}, photo_file=COALESCE(?, photo_file), filled=1,"
                 " updated_at=datetime('now','localtime') WHERE id=?", [d[k] for k in FIELDS] + [photo_file, mid])
    conn.commit()
    conn.close()


def delete(mid):
    r = get_by_id(mid)
    conn = _conn()
    conn.execute("DELETE FROM nmda_team_members WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    if r and r["photo_file"] and PHOTO_RE.match(r["photo_file"]):
        (UPLOAD_DIR / r["photo_file"]).unlink(missing_ok=True)


def set_hidden(mid, hidden):
    conn = _conn()
    conn.execute("UPDATE nmda_team_members SET hidden=? WHERE id=?", (1 if hidden else 0, mid))
    conn.commit()
    conn.close()


def add_seat(role, name, title):
    conn = _conn()
    conn.execute("INSERT INTO nmda_team_members (role, name, company_title, edit_token, filled) VALUES (?,?,?,?,0)",
                 (role[:20], name[:30], title[:60], secrets.token_urlsafe(16)))
    conn.commit()
    conn.close()


# ---------- 簽章 ----------
def admin_code(secret):
    return hmac.new(secret.encode(), b"nmda-team-admin", hashlib.sha256).hexdigest()[:12]


def admin_url(secret):
    return f"{SITE}/nmda/team/a/{admin_code(secret)}"


def build_url(secret):
    return f"{SITE}/nmda/b/{admin_code(secret)}"


# ---------- 頁面（報名／修改／後台；公開名單頁是 nmda 網站自己的 team.html） ----------
CSS = """
:root{--bg:#f3efe6;--paper:#faf7f0;--ink:#171714;--muted:#6d6a62;--line:#cec7b9;--red:#b3221d;--dark:#171714;--ok:#2f6b34}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 20px/1.75 "Noto Sans TC",sans-serif}
a{color:var(--red)}h1,h2,h3{font-family:"Noto Serif TC",serif;line-height:1.3;margin:0}
.wrap{max-width:820px;margin:0 auto;padding:0 16px}
.top{background:var(--dark);color:#fff}.top .wrap{display:flex;gap:18px;align-items:center;min-height:56px;flex-wrap:wrap;max-width:1080px}
.top a{color:#ddd;text-decoration:none}.top b{font-family:"Noto Serif TC",serif;margin-right:auto;color:#fff}
.kicker{letter-spacing:.14em;color:var(--red);font-weight:600;margin:0 0 6px}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 28px;border:1px solid var(--red);background:var(--red);
color:#fff;font:600 20px/1 "Noto Sans TC",sans-serif;text-decoration:none;cursor:pointer}
.btn.ghost{background:none;color:var(--red)}.btn.danger{background:none;border-color:#a33a3a;color:#a33a3a;min-height:44px}
.paper{background:var(--paper);border:1px solid var(--line);padding:clamp(20px,4vw,36px);margin:28px 0 56px}
.field{display:flex;flex-direction:column;margin-bottom:18px}label{font-weight:600;margin-bottom:6px}
.req{color:var(--red)}.opt{color:var(--muted);font-weight:400;margin-left:6px}
input[type=text],input[type=url],textarea{font:inherit;color:var(--ink);border:1.5px solid var(--line);padding:10px 14px;min-height:50px;width:100%;background:#fff;border-radius:0}
textarea{min-height:150px;resize:vertical}input:focus,textarea:focus{outline:none;border-color:var(--red)}
.hint{color:var(--muted);margin-top:4px}.two{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}
.err{background:#fbeded;color:#a33a3a;padding:12px 16px;margin-bottom:18px}.ok{background:#eef6ee;color:var(--ok);padding:12px 16px;margin-bottom:18px}
.claim{background:var(--paper);border:1px solid var(--line);padding:18px 20px;margin:24px 0}.claim p{margin:0 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips form{margin:0}
.chips button{font:inherit;min-height:44px;padding:0 18px;border:1px solid var(--red);background:#fff;color:var(--ink);cursor:pointer}
.cur{display:flex;gap:12px;align-items:center;margin-bottom:8px}.cur img,.cur .ph{width:64px;height:64px;border-radius:50%;object-fit:cover}
.ph{display:flex;align-items:center;justify-content:center;background:#eadfd0;color:var(--red);font:700 28px/1 "Noto Serif TC",serif}
.copy{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 20px}.copy input{flex:1;min-width:220px;font:inherit;border:1.5px solid var(--line);padding:10px 12px}
table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:10px 6px;border-bottom:1px solid var(--line);vertical-align:top}
td form{display:inline}td button{font:inherit;padding:4px 10px;border:1px solid var(--line);background:#fff;cursor:pointer}
footer{background:var(--dark);color:#bbb;padding:28px 0}footer a{color:#fff}
@media(max-width:640px){.two{grid-template-columns:1fr}}
"""


def _page(title, body, robots=True):
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{'' if robots else '<meta name="robots" content="noindex,nofollow">'}
<title>{E(title)}</title><meta name="theme-color" content="#171714">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600&family=Noto+Serif+TC:wght@500;700;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="top"><div class="wrap"><b>{TITLE}</b><a href="/curated/nmda/team.html">理監事團隊</a><a href="/curated/nmda/">協會首頁</a></div></div>
{body}
<footer><div class="wrap">{TITLE}｜資料由本人自行填寫與維護｜<a href="/curated/nmda/team.html">看理監事團隊</a></div></footer>
</body></html>"""


def _photo(r):
    if r["photo_file"]:
        return f'<img src="/nmda/team/photo/{E(r["photo_file"])}" alt="{E(r["name"])}">'
    return f'<span class="ph" aria-hidden="true">{E((r["name"] or "?")[:1])}</span>'


def _form_html(action, d, error, existing=None, seats=(), build=""):
    d = d or {}
    rq = "" if build else "required"   # 建置模式：職稱、簡介、照片都不必填
    v = lambda k: E(d.get(k, "") or "")  # noqa: E731
    photo_req = not (existing and existing["photo_file"]) and not build
    cur = (f'<div class="cur">{_photo(existing)}<span class="hint">目前的照片；不換就不用再上傳</span></div>'
           if existing and existing["photo_file"] else "")
    claim = ""
    if seats:
        part = "".join(f'<form method="post" action="/nmda/team/claim/{s["id"]}"><button>{E(s["name"])}</button></form>' for s in seats)
        claim = (f'<div class="claim"><p><b>名單上已經有您的名字？</b>直接點您的名字，補上照片與簡介即可，不用重新填。</p>'
                 f'<div class="chips">{part}</div></div>')
    links = "".join(
        f'<div class="field"><label for="{k}">{lab}<span class="opt">選填</span></label>'
        f'<input type="text" id="{k}" name="{k}" value="{v(k)}" placeholder="{"LINE ID 或加好友網址" if k == "link_line" else "https://"}"></div>'
        for k, lab in LINKS)
    return f"""{claim}<form class="paper" method="post" action="{action}" enctype="multipart/form-data">
{f'<p class="err" role="alert">{E(error)}</p>' if error else ''}
<div class="two">
<div class="field"><label for="name">姓名<span class="req"> *</span></label><input type="text" id="name" name="name" value="{v('name')}" required maxlength="30" autocomplete="name"></div>
<div class="field"><label for="role">協會職務<span class="opt">選填</span></label><input type="text" id="role" name="role" value="{v('role')}" maxlength="20" placeholder="例：理事長、常務理事、監事"></div>
</div>
<div class="field"><label for="company_title">公司／職稱<span class="req"> *</span></label><input type="text" id="company_title" name="company_title" value="{v('company_title')}" {rq} maxlength="60" placeholder="例：大樹教育 創辦人"></div>
<div class="field"><label for="bio">個人簡介<span class="req"> *</span></label><textarea id="bio" name="bio" {rq} maxlength="800" placeholder="您的專長、經歷，以及能為協會會員提供的資源（800 字內）">{v('bio')}</textarea></div>
<div class="field"><label for="photo">個人照片{'<span class="req"> *</span>' if photo_req else '<span class="opt">選填</span>'}</label>{cur}
<input type="file" id="photo" name="photo" accept="image/*" {"required" if photo_req else ""}><p class="hint">清楚的半身照最好，手機照片直接傳即可</p></div>
<div class="two">{links}</div>
<input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<button class="btn" type="submit">{'儲存修改' if existing else '送出並上架'}</button>
</form>"""


def render_join(d=None, error=""):
    body = f"""<div class="wrap" style="padding-top:36px">
<p class="kicker">我要建立檔案</p><h1>建立您的理監事檔案</h1>
<p style="color:var(--muted)">送出後立刻出現在「理監事團隊」頁面，並給您一條專屬修改連結，之後隨時可以自己修改。</p>
{_form_html("/nmda/team/join", d, error, seats=open_seats())}</div>"""
    return _page("我要建立檔案｜" + TITLE, body, robots=False)


def render_edit(r, d=None, error="", saved=False, first=False, build=""):
    d = d or dict(r)
    url = f"{SITE}/nmda/team/edit/{r['edit_token']}"
    back = f"/curated/nmda/team.html" + (f"?build={E(build)}" if build else "")
    bnote = ('<p class="ok" role="status">🛠 建置模式：照片、職稱、簡介可以只補其中一項，按「儲存修改」就更新。</p>' if build else "")
    note = ""
    if first:
        note = ('<p class="ok" role="status"><b>已上架！</b>這是您的專屬修改連結，請存起來（加入書籤或傳給自己 LINE），之後修改資料都用它：</p>'
                f'<div class="copy"><input id="me" value="{E(url)}" readonly><button class="btn" type="button" '
                f'onclick="navigator.clipboard.writeText(document.getElementById(\'me\').value).then(()=>this.textContent=\'已複製\')">複製連結</button>'
                f'<a class="btn ghost" href="{back}">看我的檔案</a></div>')
    elif saved:
        note = f'<p class="ok" role="status">已儲存，頁面已更新。<a href="{back}">回理監事團隊頁看看</a></p>'
    elif not r["filled"]:
        note = '<p class="ok" role="status">您的名字已經在名單上了，補上照片與簡介，按「儲存修改」就會上架。</p>'
    body = f"""<div class="wrap" style="padding-top:36px">
<p class="kicker">專屬修改頁</p><h1>{E(r['name'])} 的檔案</h1>
{bnote}{note}
{_form_html(f"/nmda/team/edit/{r['edit_token']}" + (f"?build={E(build)}" if build else ""), d, error, existing=r, build=build)}
<form method="post" action="/nmda/team/edit/{r['edit_token']}/delete" onsubmit="return confirm('確定要刪除您的檔案嗎？刪除後就不會出現在理監事團隊頁。')" style="margin:-32px 0 56px">
<button class="btn danger">刪除我的檔案</button></form></div>"""
    return _page("修改我的檔案｜" + TITLE, body, robots=False)


def render_admin(secret, msg=""):
    code = admin_code(secret)
    rows = list_members(include_hidden=True)
    tr = "".join(
        f"<tr><td>{E(r['role'])}</td><td><b>{E(r['name'])}</b><br>{E(r['company_title'])}</td>"
        f"<td>{'✅ 已上架' if r['filled'] else '🪑 空座位'}{'<br>🙈 已隱藏' if r['hidden'] else ''}</td>"
        f"<td><a href='/nmda/team/edit/{E(r['edit_token'])}' target='_blank' rel='noopener'>修改</a> "
        f"<button type='button' data-url='{SITE}/nmda/team/edit/{E(r['edit_token'])}' onclick='copyLink(this)'>複製專屬連結</button> "
        f"<form method='post' action='/nmda/team/a/{code}/hide/{r['id']}'><input type='hidden' name='hidden' value='{0 if r['hidden'] else 1}'>"
        f"<button>{'恢復顯示' if r['hidden'] else '隱藏'}</button></form> "
        f"<form method='post' action='/nmda/team/a/{code}/delete/{r['id']}' onsubmit=\"return confirm('確定刪除？')\"><button>刪除</button></form></td></tr>"
        for r in rows)
    body = f"""<div class="wrap" style="padding-top:32px;padding-bottom:56px;max-width:1000px">
<h1>理監事團隊・管理後台</h1>
<p style="color:var(--muted)">「修改」可直接幫本人改資料；「隱藏」先不公開、資料保留；有人亂填可以刪除。<a href="/curated/nmda/team.html" target="_blank">看公開頁</a></p>
{f'<p class="ok">{E(msg)}</p>' if msg else ''}
<p class="hint">「複製專屬連結」＝傳給本人讓他自己補資料或修改的連結（不用登入）；這個後台網址只有你知道，不要傳給別人。</p>
<table><thead><tr><th>職務</th><th>姓名／公司</th><th>狀態</th><th></th></tr></thead><tbody>{tr}</tbody></table>
<form class="paper" method="post" action="/nmda/team/a/{code}/seat"><h2 style="font-size:24px;margin-bottom:12px">新增空座位</h2>
<p class="hint" style="margin-top:0">理監事名單確定後，可先把名字放上去，本人點自己的名字補資料。</p>
<div class="two"><div class="field"><label for="s_name">姓名</label><input type="text" id="s_name" name="name" required maxlength="30"></div>
<div class="field"><label for="s_role">職務</label><input type="text" id="s_role" name="role" maxlength="20" placeholder="例：常務理事"></div></div>
<div class="field"><label for="s_title">公司／職稱</label><input type="text" id="s_title" name="company_title" maxlength="60"></div>
<button class="btn">新增座位</button></form></div>
<script>
function copyLink(btn) {{
  var url = btn.getAttribute('data-url');
  var done = function () {{ var t = btn.textContent; btn.textContent = '已複製！'; setTimeout(function () {{ btn.textContent = t; }}, 1800); }};
  if (navigator.clipboard) {{ navigator.clipboard.writeText(url).then(done, function () {{ prompt('請複製這條連結：', url); }}); }}
  else {{ prompt('請複製這條連結：', url); }}
}}
</script>"""
    return _page("管理後台｜" + TITLE, body, robots=False)
