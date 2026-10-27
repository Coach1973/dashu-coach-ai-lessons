# -*- coding: utf-8 -*-
"""作品頁／策展頁「留資料」後台（教練 2026-10-27 要求「寫好的資料在哪裡、給我網址」）

背景：/api/works/contact 與 /api/rongtree/hold 都把留言寫進 works_contact_leads，
但全專案只有 INSERT、沒有任何一處 SELECT 或後台頁 —— 教練在網站上完全看不到自己收的資料。
本模組補上那一頁。存取方式沿用既有慣例：短網址本身就是通行證（不需帳密），
簽章用 app.secret_key（EVENT_SECRET_KEY），無簽章一律 404。
"""
import hashlib
import hmac
import html

import db

E = html.escape

BASE_CSS = """
:root{--ink:#0e1712;--ink-2:#14211a;--paper:#f2ead8;--paper-2:#e8dcc3;--line:#cdbd9c;--on-ink:#efe6d2;--mute:#a7b2a3;
--on-paper:#1d2a22;--on-paper-mute:#5b6656;--amber:#d9a441;--amber-hi:#f0c46a;--amber-deep:#9a6a1c}
*{box-sizing:border-box}body{margin:0;font:400 17px/1.8 "Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;letter-spacing:.02em}
h1,h2,h3{font-family:"Noto Serif TC","Songti TC",serif;margin:0}
.wrap{max-width:1080px;margin:0 auto;padding:32px 16px 64px}
.back{margin:0 0 18px}.back a{color:var(--amber-deep);text-decoration:none;font-weight:700}
table{width:100%;border-collapse:collapse;margin-top:20px;font-size:15px}
td,th{text-align:left;padding:10px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--on-paper-mute);font-weight:700;white-space:nowrap}
.name{font-weight:700}.muted{color:var(--on-paper-mute);font-size:13px}
.msg{white-space:pre-wrap;word-break:break-word}
.site a{color:var(--amber-deep)}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0 0}
.bar a{font-size:14px;padding:4px 12px;border:1px solid var(--line);border-radius:999px;text-decoration:none;color:var(--on-paper-mute)}
.bar a.on{background:var(--amber);border-color:var(--amber);color:var(--ink);font-weight:700}
.count{color:var(--on-paper-mute);font-size:14px}
@media print{.back,.bar{display:none}}
"""


# ---------- 簽章 ----------
def _sig(secret: str, msg: str) -> str:
    return hmac.new(secret.encode(), msg.encode(), hashlib.sha256).hexdigest()[:24]


def list_sig(secret):
    return _sig(secret, "works-leads")


def list_code(secret):
    """後台短網址用的短碼（12 碼），跟長簽章同源。"""
    return list_sig(secret)[:12]


def list_url(secret):
    """後台短網址（教練：後台網址一律短址）；長連結 /leads?k=… 也有效。"""
    return f"https://event.bymyway.com/leads/a/{list_code(secret)}"


# ---------- 資料 ----------
def all_leads(site=None, limit=500):
    conn = db.get_conn()
    try:
        if site:
            return conn.execute(
                "SELECT id, site, site_title, name, phone, item, email, message, ip, created_at "
                "FROM works_contact_leads WHERE site=? ORDER BY id DESC LIMIT ?",
                (site, limit)).fetchall()
        return conn.execute(
            "SELECT id, site, site_title, name, phone, item, email, message, ip, created_at "
            "FROM works_contact_leads ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    finally:
        conn.close()


def site_counts():
    conn = db.get_conn()
    try:
        rows = conn.execute(
            "SELECT site, site_title, COUNT(*) AS n FROM works_contact_leads GROUP BY site, site_title"
        ).fetchall()
        return [(r["site"], r["site_title"], r["n"]) for r in rows]
    finally:
        conn.close()


# ---------- 頁面 ----------
def render_list(secret, site=None):
    rows = all_leads(site=site)
    counts = site_counts()
    total = sum(n for _, _, n in counts)

    tabs = ["<div class='bar'><a class='on' href='/leads/a/%s'>全部（%d 筆）</a>" % (list_code(secret), total)]
    for s, title, n in counts:
        cur = " class='on'" if s == site else ""
        tabs.append("<a%s href='/leads/a/%s?site=%s'>%s（%d）</a>"
                    % (cur, list_code(secret), html.escape(s, quote=True), E(title or s), n))
    tabs.append("</div>")

    body = ""
    for r in rows:
        contact = E(r["phone"] or "")
        if r["email"]:
            contact += ("<br>" if contact else "") + E(r["email"])
        body += (
            "<tr>"
            f"<td class='muted'>{E(r['created_at'] or '')}</td>"
            f"<td class='name'>{E(r['name'] or '')}</td>"
            f"<td>{contact}</td>"
            f"<td>{E(r['item'] or '')}</td>"
            f"<td class='site'>{E(r['site_title'] or r['site'] or '')}</td>"
            f"<td class='msg'>{E(r['message'] or '')}</td>"
            "</tr>"
        )
    if not body:
        body = "<tr><td colspan='6' class='muted'>還沒有任何留資料。</td></tr>"

    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>留資料後台</title><style>{BASE_CSS}
body{{background:var(--paper);color:var(--on-paper)}}</style></head><body><div class="wrap">
<p class="back"><a href="/">← 回 event.bymyway.com</a></p>
<h1>留資料後台</h1>
<p class="sub muted">策展頁／作品頁的「留資料」表單收到的內容都存這裡（跟 Telegram 通知同一份資料）。<br>
電話、Email 屬個人資料，這頁有簽章保護、也加了 noindex，請勿轉貼網址。</p>
{''.join(tabs)}
<table><thead><tr><th>時間</th><th>姓名</th><th>聯絡方式</th><th>想了解</th><th>來源頁</th><th>留言</th></tr></thead>
<tbody>{body}</tbody></table>
<p class="count">共 {total} 筆（本頁顯示最近 {len(rows)} 筆）</p>
</div></body></html>"""
