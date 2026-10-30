"""中華新媒體影音發展協會（NMDA）：會員資料頁（2026-10-30 教練交辦）

協會會員自己建立檔案（姓名、公司／職稱、簡介、照片、連結），送出立刻上架到 NMDA 網站的「會員資料」頁。
架構照 nmda_team.py（理監事團隊）複製：資料只有一份在資料庫，公開頁是 NMDA 網站自己的靜態頁 github_repos/nmda/members.html，載入時讀 API。
連結欄位照 AI 百人導師（mentor100）的樣式，再加 LinkedIn 領英，共 10 種。

網址：
  /api/nmda/members/board        公開頁讀的資料（CORS *、no-store）
  /nmda/members/join             我要建立檔案
  /nmda/members/edit/<token>     本人專屬修改連結（含刪除）
  /nmda/members/photo/<檔名>      照片
  /nmda/members/a/<code>         管理後台（簽章短址）：修改／隱藏／刪除
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
from nmda_team import CSS

UPLOAD_DIR = Path(__file__).resolve().parent / "nmda_members_uploads"
MAX_UPLOAD = 12_000_000
MAX_EDGE = 900
PHOTO_RE = re.compile(r"^[0-9a-f]{16}\.jpg$")
SITE = "https://event.bymyway.com"
PAGE_URL = f"{SITE}/curated/nmda/members.html"
TITLE = "中華新媒體影音發展協會"

# (欄位, 表單標題, 公開頁按鈕文字, 範例網址)；順序與文字照 mentor100 的 link_defs，另加 LinkedIn 領英
LINKS = [
    ("link_web", "官網", "官網", "https://..."),
    ("link_fb", "Facebook 粉絲專頁", "Facebook", "https://facebook.com/..."),
    ("link_ig", "Instagram", "Instagram", "https://instagram.com/..."),
    ("link_threads", "Threads", "Threads", "https://threads.net/..."),
    ("link_youtube", "YouTube", "YouTube", "https://youtube.com/..."),
    ("link_linkedin", "LinkedIn 領英", "LinkedIn", "https://linkedin.com/in/..."),
    ("link_podcast", "Podcast", "Podcast", "https://..."),
    ("link_blog", "部落格文章", "部落格", "https://..."),
    ("link_gjw", "乾淨世界 GJW", "GJW", "https://www.ganjing.world/..."),
    ("link_line", "LINE", "LINE", "LINE ID 或加好友網址"),
]
LINK_KEYS = [k for k, _, _, _ in LINKS]
FIELDS = ["name", "company_title", "bio"] + LINK_KEYS
LIMITS = {"name": 30, "company_title": 60, "bio": 800, **{k: 300 for k in LINK_KEYS}}

E = html.escape


# ---------- 資料 ----------
def _conn():
    conn = db.get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS nmda_members ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,"
        " company_title TEXT NOT NULL DEFAULT '', bio TEXT NOT NULL DEFAULT '', photo_file TEXT,"
        + "".join(f" {k} TEXT NOT NULL DEFAULT ''," for k in LINK_KEYS) +
        " edit_token TEXT NOT NULL UNIQUE, hidden INTEGER NOT NULL DEFAULT 0, ip TEXT,"
        " created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        " updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))"
    )
    return conn


def list_members(include_hidden=False):
    """新建立的排最前面。"""
    conn = _conn()
    rows = conn.execute("SELECT * FROM nmda_members" + ("" if include_hidden else " WHERE hidden=0") + " ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def board_public():
    """公開頁用的資料：只有公開欄位，不含修改連結、IP。"""
    return [{"id": r["id"], "name": r["name"], "title": r["company_title"], "bio": r["bio"],
             "photo": f"{SITE}/nmda/members/photo/{r['photo_file']}" if r["photo_file"] else "",
             "links": [{"label": lab, "url": r[k]} for k, _, lab, _ in LINKS if r[k]]}
            for r in list_members()]


def get_by_token(token):
    if not token or len(token) > 64:
        return None
    conn = _conn()
    r = conn.execute("SELECT * FROM nmda_members WHERE edit_token=?", (token,)).fetchone()
    conn.close()
    return r


def get_by_id(mid):
    conn = _conn()
    r = conn.execute("SELECT * FROM nmda_members WHERE id=?", (mid,)).fetchone()
    conn.close()
    return r


def _norm_link(key, v):
    v = v.strip()
    if not v:
        return ""
    if key == "link_line" and not re.match(r"^https?://", v, re.I):
        return "https://line.me/ti/p/~" + re.sub(r"[^\w.@-]", "", v.lstrip("@"))
    if not re.match(r"^https?://", v, re.I):
        v = "https://" + v
    return v if re.match(r"^https?://[^\s<>\"']+$", v) else ""


def clean_form(form, need_photo):
    """回傳 (資料 dict, 錯誤訊息)。"""
    d = {}
    for k in FIELDS:
        v = (form.get(k) or "").strip()
        v = v[:LIMITS[k]] if k == "bio" else re.sub(r"\s+", " ", v)[:LIMITS[k]]
        d[k] = _norm_link(k, v) if k.startswith("link_") else v
    for k, label in (("name", "姓名"), ("company_title", "公司／職稱"), ("bio", "個人簡介")):
        if not d[k]:
            return d, f"請填寫「{label}」"
    if need_photo:
        return d, "請上傳一張照片"
    return d, ""


def save_photo(file_storage):
    """驗證是真的圖片、轉正、縮圖存 jpg；回傳檔名，失敗回 None。"""
    data = file_storage.read(MAX_UPLOAD + 1)
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
        f"INSERT INTO nmda_members ({', '.join(FIELDS)}, photo_file, edit_token, ip)"
        f" VALUES ({', '.join('?' * len(FIELDS))}, ?, ?, ?)",
        [d[k] for k in FIELDS] + [photo_file, token, ip])
    conn.commit()
    conn.close()
    return token


def update(mid, d, photo_file):
    conn = _conn()
    sets = ", ".join(f"{k}=?" for k in FIELDS)
    conn.execute(f"UPDATE nmda_members SET {sets}, photo_file=COALESCE(?, photo_file),"
                 " updated_at=datetime('now','localtime') WHERE id=?", [d[k] for k in FIELDS] + [photo_file, mid])
    conn.commit()
    conn.close()


def delete(mid):
    r = get_by_id(mid)
    conn = _conn()
    conn.execute("DELETE FROM nmda_members WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    if r and r["photo_file"] and PHOTO_RE.match(r["photo_file"]):
        (UPLOAD_DIR / r["photo_file"]).unlink(missing_ok=True)


def set_hidden(mid, hidden):
    conn = _conn()
    conn.execute("UPDATE nmda_members SET hidden=? WHERE id=?", (1 if hidden else 0, mid))
    conn.commit()
    conn.close()


# ---------- 簽章 ----------
def admin_code(secret):
    return hmac.new(secret.encode(), b"nmda-members-admin", hashlib.sha256).hexdigest()[:12]


def admin_url(secret):
    return f"{SITE}/nmda/members/a/{admin_code(secret)}"


# ---------- 頁面（建立／修改／後台；公開名單頁是 nmda 網站自己的 members.html） ----------
def _page(title, body):
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{E(title)}</title><meta name="theme-color" content="#171714">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;600&family=Noto+Serif+TC:wght@500;700;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="top"><div class="wrap"><b>{TITLE}</b><a href="/curated/nmda/members.html">會員資料</a><a href="/curated/nmda/">協會首頁</a></div></div>
{body}
<footer><div class="wrap">{TITLE}｜資料由本人自行填寫與維護｜<a href="/curated/nmda/members.html">看會員資料</a></div></footer>
</body></html>"""


def _photo(r):
    if r["photo_file"]:
        return f'<img src="/nmda/members/photo/{E(r["photo_file"])}" alt="{E(r["name"])}">'
    return f'<span class="ph" aria-hidden="true">{E((r["name"] or "?")[:1])}</span>'


def _form_html(action, d, error, existing=None):
    d = d or {}
    v = lambda k: E(d.get(k, "") or "")  # noqa: E731
    photo_req = not (existing and existing["photo_file"])
    cur = (f'<div class="cur">{_photo(existing)}<span class="hint">目前的照片；不換就不用再上傳</span></div>'
           if existing and existing["photo_file"] else "")
    links = "".join(
        f'<div class="field"><label for="{k}">{E(title)}<span class="opt">選填</span></label>'
        f'<input type="text" id="{k}" name="{k}" value="{v(k)}" placeholder="{E(ph)}"></div>'
        for k, title, _, ph in LINKS)
    return f"""<form class="paper" method="post" action="{action}" enctype="multipart/form-data">
{f'<p class="err" role="alert">{E(error)}</p>' if error else ''}
<div class="field"><label for="name">姓名<span class="req"> *</span></label><input type="text" id="name" name="name" value="{v('name')}" required maxlength="30" autocomplete="name"></div>
<div class="field"><label for="company_title">公司／職稱<span class="req"> *</span></label><input type="text" id="company_title" name="company_title" value="{v('company_title')}" required maxlength="60" placeholder="例：大樹教育 創辦人"></div>
<div class="field"><label for="bio">個人簡介<span class="req"> *</span></label><textarea id="bio" name="bio" required maxlength="800" placeholder="您的專長、經歷，以及能為協會會員提供的資源（800 字內）">{v('bio')}</textarea></div>
<div class="field"><label for="photo">個人照片{'<span class="req"> *</span>' if photo_req else '<span class="opt">選填</span>'}</label>{cur}
<input type="file" id="photo" name="photo" accept="image/*" {"required" if photo_req else ""}><p class="hint">清楚的半身照最好，手機照片直接傳即可</p></div>
<p class="hint" style="margin:8px 0 14px"><b>連結</b>（都選填，有哪個填哪個，會在您的卡片上顯示成按鈕）</p>
<div class="two">{links}</div>
<input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<button class="btn" type="submit">{'儲存修改' if existing else '送出並上架'}</button>
</form>"""


def render_join(d=None, error=""):
    body = f"""<div class="wrap" style="padding-top:36px">
<p class="kicker">我要建立檔案</p><h1>建立您的會員檔案</h1>
<p style="color:var(--muted)">送出後立刻出現在「會員資料」頁面，並給您一條專屬修改連結，之後隨時可以自己修改。</p>
{_form_html("/nmda/members/join", d, error)}</div>"""
    return _page("我要建立檔案｜" + TITLE, body)


def render_edit(r, d=None, error="", saved=False, first=False):
    d = d or dict(r)
    url = f"{SITE}/nmda/members/edit/{r['edit_token']}"
    note = ""
    if first:
        note = ('<p class="ok" role="status"><b>已上架！</b>這是您的專屬修改連結，請存起來（加入書籤或傳給自己 LINE），之後修改資料都用它：</p>'
                f'<div class="copy"><input id="me" value="{E(url)}" readonly><button class="btn" type="button" '
                f'onclick="navigator.clipboard.writeText(document.getElementById(\'me\').value).then(()=>this.textContent=\'已複製\')">複製連結</button>'
                f'<a class="btn ghost" href="/curated/nmda/members.html">看我的檔案</a></div>')
    elif saved:
        note = '<p class="ok" role="status">已儲存，頁面已更新。<a href="/curated/nmda/members.html">回會員資料頁看看</a></p>'
    body = f"""<div class="wrap" style="padding-top:36px">
<p class="kicker">專屬修改頁</p><h1>{E(r['name'])} 的檔案</h1>
{note}
{_form_html(f"/nmda/members/edit/{r['edit_token']}", d, error, existing=r)}
<form method="post" action="/nmda/members/edit/{r['edit_token']}/delete" onsubmit="return confirm('確定要刪除您的檔案嗎？刪除後就不會出現在會員資料頁。')" style="margin:-32px 0 56px">
<button class="btn danger">刪除我的檔案</button></form></div>"""
    return _page("修改我的檔案｜" + TITLE, body)


def render_admin(secret, msg=""):
    code = admin_code(secret)
    rows = list_members(include_hidden=True)
    tr = "".join(
        f"<tr><td><b>{E(r['name'])}</b><br>{E(r['company_title'])}</td>"
        f"<td>{'🙈 已隱藏' if r['hidden'] else '✅ 已上架'}<br><span class='hint'>{E(r['created_at'])}</span></td>"
        f"<td><a href='/nmda/members/edit/{E(r['edit_token'])}' target='_blank' rel='noopener'>修改</a> "
        f"<button type='button' data-url='{SITE}/nmda/members/edit/{E(r['edit_token'])}' onclick='copyLink(this)'>複製專屬連結</button> "
        f"<form method='post' action='/nmda/members/a/{code}/hide/{r['id']}'><input type='hidden' name='hidden' value='{0 if r['hidden'] else 1}'>"
        f"<button>{'恢復顯示' if r['hidden'] else '隱藏'}</button></form> "
        f"<form method='post' action='/nmda/members/a/{code}/delete/{r['id']}' onsubmit=\"return confirm('確定刪除？')\"><button>刪除</button></form></td></tr>"
        for r in rows)
    body = f"""<div class="wrap" style="padding-top:32px;padding-bottom:56px;max-width:1000px">
<h1>會員資料・管理後台</h1>
<p style="color:var(--muted)">「修改」可直接幫會員改資料；「隱藏」先不公開、資料保留；有人亂填可以刪除。<a href="/curated/nmda/members.html" target="_blank">看公開頁</a></p>
{f'<p class="ok">{E(msg)}</p>' if msg else ''}
<p class="hint">「複製專屬連結」＝傳給本人讓他自己修改的連結（不用登入）；這個後台網址只有你知道，不要傳給別人。</p>
<table><thead><tr><th>姓名／公司</th><th>狀態</th><th></th></tr></thead><tbody>{tr or '<tr><td colspan="3">還沒有人建立檔案</td></tr>'}</tbody></table></div>
<script>
function copyLink(btn) {{
  var url = btn.getAttribute('data-url');
  var done = function () {{ var t = btn.textContent; btn.textContent = '已複製！'; setTimeout(function () {{ btn.textContent = t; }}, 1800); }};
  if (navigator.clipboard) {{ navigator.clipboard.writeText(url).then(done, function () {{ prompt('請複製這條連結：', url); }}); }}
  else {{ prompt('請複製這條連結：', url); }}
}}
</script>"""
    return _page("管理後台｜" + TITLE, body)
