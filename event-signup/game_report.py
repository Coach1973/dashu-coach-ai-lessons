"""互動教材的「學習報告」（2026-10-25 教練交辦：BNI 來賓接待工作坊 bni-gusest，跟孫林博士共同創作）

策展中心的互動遊戲頁本身是靜態 HTML，玩家的輸入原本只存在自己的瀏覽器。這支讓它「最後產生一份報告」：
  遊戲頁把作答整理成一般格式（標題＋各區段的「題目：答案」＋分數＋回饋）POST 上來 → 存資料庫 →
  回傳一個專屬報告網址（可分享、可列印成 PDF），並通知「活動報名即時通知」群。
格式不綁特定遊戲，之後別的互動教材照同一格式送就能用（site＝策展網址代號）。

網址：
  POST /api/game/report            遊戲頁送報告（同網域，不開 CORS）；名字開頭「【測試】」不發通知
  /game-report/<token>             個人報告頁（noindex，拿到網址的人才看得到）
  /gr/<code>                       講師後台短網址（同 /game-report/a/<code>，?site= 可篩選某個遊戲）
"""
import hashlib
import hmac
import html
import json
import secrets

import db

SITE = "https://event.bymyway.com"
E = html.escape
LIMIT_TEXT = 1200      # 每一題答案最多字數
LIMIT_ITEMS = 60       # 一份報告最多幾題
LIMIT_SECTIONS = 16
TEST_PREFIX = "【測試】"


def _conn():
    conn = db.get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS game_reports ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT, site TEXT NOT NULL, site_title TEXT NOT NULL DEFAULT '',"
        " token TEXT NOT NULL UNIQUE, name TEXT NOT NULL, chapter TEXT NOT NULL DEFAULT '',"
        " data TEXT NOT NULL, ip TEXT,"
        " created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))")
    return conn


def _s(v, n):
    return " ".join(str(v or "").split())[:n] if n <= 40 else str(v or "").strip()[:n]


def clean(payload):
    """只留看得懂的欄位、截斷長度；姓名必填。回傳 (資料, 錯誤訊息)。"""
    name, chapter = _s(payload.get("name"), 30), _s(payload.get("chapter"), 30)
    if not name:
        return None, "請先填寫姓名，報告才知道是誰的"
    sections, count = [], 0
    for sec in (payload.get("sections") or [])[:LIMIT_SECTIONS]:
        if not isinstance(sec, dict):
            continue
        items = []
        for it in (sec.get("items") or []):
            if count >= LIMIT_ITEMS or not isinstance(it, dict):
                break
            items.append({"label": _s(it.get("label"), 200), "value": _s(it.get("value"), LIMIT_TEXT)})
            count += 1
        sections.append({"title": _s(sec.get("title"), 40), "items": items})
    scores = []
    for sc in (payload.get("scores") or [])[:8]:
        try:
            got, total = int(sc.get("got", 0)), int(sc.get("total", 0))
        except (TypeError, ValueError, AttributeError):
            continue
        if 0 < total <= 100 and 0 <= got <= total:
            scores.append({"label": _s(sc.get("label"), 20), "got": got, "total": total})
    feedback = [_s(x, 300) for x in (payload.get("feedback") or [])[:8] if str(x or "").strip()]
    return {"name": name, "chapter": chapter, "game": _s(payload.get("game"), 60), "sections": sections,
            "scores": scores, "feedback": feedback, "takeaway": _s(payload.get("takeaway"), 120)}, ""


def save(site, site_title, d, ip):
    token = secrets.token_urlsafe(12)
    conn = _conn()
    conn.execute("INSERT INTO game_reports (site, site_title, token, name, chapter, data, ip) VALUES (?,?,?,?,?,?,?)",
                 (site, site_title, token, d["name"], d["chapter"], json.dumps(d, ensure_ascii=False), ip))
    conn.commit()
    conn.close()
    return token


def get(token):
    conn = _conn()
    r = conn.execute("SELECT * FROM game_reports WHERE token=?", (token,)).fetchone()
    conn.close()
    return r


def delete(token):
    conn = _conn()
    conn.execute("DELETE FROM game_reports WHERE token=?", (token,))
    conn.commit()
    conn.close()


def list_reports(site=""):
    conn = _conn()
    q, a = "SELECT * FROM game_reports", ()
    if site:
        q, a = q + " WHERE site=?", (site,)
    rows = conn.execute(q + " ORDER BY id DESC LIMIT 500", a).fetchall()
    conn.close()
    return rows


def report_url(token):
    return f"{SITE}/game-report/{token}"


def admin_code(secret):
    return hmac.new(secret.encode(), b"game-report-admin", hashlib.sha256).hexdigest()[:12]


def admin_url(secret, site=""):
    """講師後台短網址（教練 10/10：後台一律短網址）；/game-report/a/<碼>?site= 長網址照樣有效。"""
    return f"{SITE}/gr/{admin_code(secret)}"


def summary_line(d):
    return "　".join(f"{s['label']} {s['got']}/{s['total']}" for s in d["scores"])


# ---------- 頁面（配色沿用 bni-gusest 互動教材：米白紙、深墨、BNI 紅） ----------
CSS = """
:root{--paper:#f5efe4;--card:#fbf8f2;--ink:#1d1a16;--ink-2:#4a443b;--ink-3:#7a7266;--line:#d9cfbd;--red:#b5122b;--red-wash:#f4dcd9;--ok:#2f6b4f;--ok-wash:#dcebe2}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 20px/1.8 "Noto Sans TC","PingFang TC",sans-serif}
h1,h2,h3{font-family:"Noto Serif TC","Songti TC",serif;line-height:1.3;margin:0}
a{color:var(--red)}.wrap{max-width:860px;margin:0 auto;padding:0 16px}
.top{background:var(--ink);color:#fff}.top .wrap{display:flex;gap:16px;align-items:center;min-height:60px;flex-wrap:wrap}
.top b{font-family:"Noto Serif TC",serif;margin-right:auto}.top a{color:#eee}
.head{padding:44px 0 8px}.kicker{color:var(--red);font-weight:700;letter-spacing:.12em;margin:0 0 8px}
.head h1{font-size:clamp(34px,6vw,52px)}.who{margin:14px 0 0;color:var(--ink-2)}
.scores{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:28px 0}
.sc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}
.sc .n{font:900 44px/1.1 "Noto Serif TC",serif;color:var(--red)}.sc .n small{font-size:24px;color:var(--ink-3)}
.sc .l{color:var(--ink-2)}
.fb{background:var(--ok-wash);border-left:6px solid var(--ok);border-radius:10px;padding:18px 22px;margin:0 0 28px}
.fb h2{font-size:26px;margin-bottom:8px}.fb ul{margin:0;padding-left:1.2em}
.sec{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:clamp(18px,4vw,32px);margin:0 0 22px;break-inside:avoid}
.sec h2{font-size:28px;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid var(--red-wash)}
.it{margin:0 0 16px}.it:last-child{margin:0}.it .q{font-weight:700;color:var(--ink-2)}
.it .a{white-space:pre-wrap;margin:4px 0 0}.it .a.empty{color:var(--ink-3)}
.take{background:var(--ink);color:#fff;border-radius:14px;padding:28px 30px;margin:0 0 28px}
.take h2{font-size:28px}.take p{margin:6px 0 0;color:#ddd}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 44px}
.btn{display:inline-flex;align-items:center;min-height:52px;padding:0 26px;border-radius:999px;border:1.5px solid var(--red);background:var(--red);color:#fff;font:700 20px/1 "Noto Sans TC",sans-serif;text-decoration:none;cursor:pointer}
.btn.ghost{background:none;color:var(--red)}
table{width:100%;border-collapse:collapse;background:var(--card)}td,th{text-align:left;padding:12px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl{overflow-x:auto;margin:20px 0 48px}
footer{color:var(--ink-3);padding:24px 0 40px;border-top:1px solid var(--line)}
@media print{.top,.btns,footer{display:none}body{background:#fff;font-size:16px}.sec,.sc{border-color:#bbb}.take{background:#fff;color:#000;border:2px solid #000}.take p{color:#000}}
"""


def _page(title, body):
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{E(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Noto+Serif+TC:wght@700;900&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{body}</body></html>"""


def render_report(r):
    d = json.loads(r["data"])
    game = d.get("game") or r["site_title"] or "互動教材"
    back = f"/curated/{E(r['site'])}/"
    who = E(d["name"]) + (f"｜{E(d['chapter'])}" if d.get("chapter") else "")
    scores = "".join(f'<div class="sc"><div class="n">{s["got"]}<small> / {s["total"]}</small></div><div class="l">{E(s["label"])}</div></div>'
                     for s in d["scores"])
    fb = ("<div class=\"fb\"><h2>給你的回饋</h2><ul>" + "".join(f"<li>{E(x)}</li>" for x in d["feedback"]) + "</ul></div>") if d["feedback"] else ""
    secs = ""
    for sec in d["sections"]:
        if not sec["items"]:
            continue
        items = "".join(f'<div class="it"><div class="q">{E(i["label"])}</div>'
                        f'<p class="a{"" if i["value"] else " empty"}">{E(i["value"]) if i["value"] else "（沒有填寫）"}</p></div>'
                        for i in sec["items"])
        secs += f'<section class="sec"><h2>{E(sec["title"])}</h2>{items}</section>'
    take = f'<div class="take"><h2>{E(d["takeaway"])}</h2><p>帶著這份報告，下一次接待就用得上。</p></div>' if d.get("takeaway") else ""
    body = f"""<div class="top"><div class="wrap"><b>{E(game)}</b><a href="{back}">回到互動教材</a></div></div>
<main class="wrap"><div class="head"><p class="kicker">學習報告</p><h1>{who}</h1>
<p class="who">完成時間：{E(r['created_at'][:16])}</p></div>
{f'<div class="scores">{scores}</div>' if scores else ''}{fb}{secs}{take}
<div class="btns"><button class="btn" onclick="window.print()">列印／存成 PDF</button>
<button class="btn ghost" id="cp">複製這份報告的網址</button><a class="btn ghost" href="{back}">回到互動教材</a></div></main>
<footer><div class="wrap">{E(game)}｜這份報告只有拿到網址的人看得到</div></footer>
<script>document.getElementById('cp').onclick=function(){{var u=location.href.split('#')[0];
(navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){{this.textContent='已複製網址 ✓'}}.bind(this),function(){{prompt('請複製這個網址',u)}})}}</script>"""
    return _page(f"{d['name']} 的學習報告｜{game}", body)


def render_admin(rows, site=""):
    trs = ""
    for r in rows:
        d = json.loads(r["data"])
        trs += (f"<tr><td>{E(r['created_at'][:16])}</td><td>{E(r['name'])}</td><td>{E(r['chapter'])}</td>"
                f"<td>{E(r['site_title'] or r['site'])}</td><td>{E(summary_line(d))}</td>"
                f"<td><a href=\"/game-report/{E(r['token'])}\" target=\"_blank\">看報告</a></td></tr>")
    body = f"""<div class="top"><div class="wrap"><b>互動教材・學習報告後台</b></div></div>
<main class="wrap"><div class="head"><p class="kicker">講師用</p><h1>共 {len(rows)} 份報告</h1>
<p class="who">{'篩選：' + E(site) if site else '全部互動教材'}</p></div>
<div class="tbl"><table><tr><th>時間</th><th>姓名</th><th>分會</th><th>教材</th><th>成績</th><th></th></tr>{trs or '<tr><td colspan="6">還沒有人送出報告</td></tr>'}</table></div></main>"""
    return _page("學習報告後台", body)
