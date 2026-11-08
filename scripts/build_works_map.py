#!/usr/bin/env python3
"""產生「大樹作品分類表」單頁網頁。
用法：python3 build_works_map.py <輸出資料夾>     （寫出 index.html）
資料：works_map_classify.load()（all-works/data.json ＋ 人才軍火庫名單）"""
import html, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import works_map_classify as wc

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
items, generated = wc.load()
E = html.escape


def kind(u):
    if "event.bymyway.com" in u: return "作品庫"
    if "github.io" in u: return "GitHub 網頁"
    return "GitHub 倉庫"


nav, secs = [], []
for key, num, title, desc in wc.CATS:
    g = sorted([x for x in items if x["cat"] == key], key=lambda x: x["updated"], reverse=True)
    nav.append(f'<a href="#c-{key}" data-k="{key}"><b>{num}</b> {E(title)} <i>{len(g)}</i></a>')
    cards = []
    for x in g:
        tags = "".join(f'<em class="t">{E(t)}</em>' for t in x["tags"])
        cards.append(
            f'<a class="card" href="{E(x["url"])}" target="_blank" rel="noopener" data-s="{E((x["name"] + " " + x["id"]).lower())}">'
            f'<span class="n">{E(x["name"])}</span>'
            f'<span class="m"><code>{E(x["id"])}</code> · {kind(x["url"])} · {E(x["updated"])}</span>{tags}</a>')
    secs.append(f'<section id="c-{key}" data-k="{key}"><h2><span class="no">{num}</span>{E(title)}'
                f'<small>{len(g)} 個</small></h2><p class="d">{E(desc)}</p><div class="grid">{"".join(cards)}</div></section>')

page = f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>大樹作品分類表</title>
<style>
:root{{--bg:#F5F1E8;--ink:#1F2A24;--mut:#5A6359;--card:#fff;--line:#DDD5C3;--g:#2F5D46;--gold:#B98B2E}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:150px}}
body{{margin:0;background:var(--bg);color:var(--ink);font:20px/1.7 "Noto Sans TC","PingFang TC",system-ui,sans-serif}}
header{{position:sticky;top:0;z-index:10;background:#1F3A2D;color:#F7F1DF;padding:12px 16px;box-shadow:0 2px 10px rgba(0,0,0,.25)}}
.hin{{max-width:1100px;margin:auto}}
h1{{margin:0;font:900 28px/1.3 "Noto Serif TC",serif}}
h1 small{{font:400 20px/1.4 sans-serif;color:#CFE0D4;margin-left:10px}}
#q{{width:100%;margin-top:8px;font:20px sans-serif;padding:10px 16px;border-radius:12px;border:0}}
nav{{display:flex;gap:8px;overflow-x:auto;padding:8px 0 2px;-webkit-overflow-scrolling:touch}}
nav a{{flex:none;color:#F7F1DF;text-decoration:none;border:1px solid #567A67;border-radius:999px;padding:4px 14px;white-space:nowrap}}
nav a b{{color:#E8C673}}nav a i{{font-style:normal;color:#E8C673;margin-left:4px}}
main{{max-width:1100px;margin:auto;padding:24px 16px 60px}}
.lead{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px 20px;margin-bottom:28px}}
.lead p{{margin:4px 0}}
section{{margin:36px 0}}
h2{{font:900 30px/1.3 "Noto Serif TC",serif;margin:0;color:var(--g);display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}}
h2 .no{{background:var(--gold);color:#fff;border-radius:10px;padding:0 12px;font:900 24px/1.5 sans-serif}}
h2 small{{font:400 20px sans-serif;color:var(--mut)}}
.d{{margin:4px 0 14px;color:var(--mut)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}
.card{{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;color:inherit;text-decoration:none}}
.card:hover{{border-color:var(--g);box-shadow:0 6px 18px -8px rgba(47,93,70,.5)}}
.card .n{{display:block;font-weight:700;line-height:1.45;overflow-wrap:anywhere}}
.card .m{{display:block;color:var(--mut);font-size:20px;overflow-wrap:anywhere}}
.card code{{font:20px ui-monospace,monospace}}
.t{{display:inline-block;font-style:normal;margin:4px 6px 0 0;padding:0 10px;border-radius:999px;background:#FBEFD0;color:#7A5A12;border:1px solid #E4CF94}}
.hide{{display:none!important}}
footer{{max-width:1100px;margin:0 auto;padding:0 16px 40px;color:var(--mut)}}
footer a{{color:var(--g);margin-right:14px}}
</style></head><body>
<header><div class="hin"><h1>大樹作品分類表<small>共 {len(items)} 個</small></h1>
<input id="q" type="search" placeholder="搜尋名字、網址代號（例：佩佩、tea、peipei）" aria-label="搜尋">
<nav>{"".join(nav)}</nav></div></header>
<main>
<div class="lead"><p>每個作品只放在一個分類，點卡片就開啟網頁。黃色小標籤＝<b>只在 GitHub</b>（還沒放進作品庫）、<b>已下架</b>、<b>私有</b>。</p>
<p>資料更新時間：{E(generated)}（來源：完整作品一覽）。</p></div>
{"".join(secs)}
</main>
<footer><p>本網頁由 <a href="https://www.tava-ai.com/" target="_blank" rel="noopener">TAVA AI</a> 製作</p>
<p>友善連結：<a href="https://event.bymyway.com/curated/rongtree/" target="_blank" rel="noopener">榮樹下</a>
<a href="https://event.bymyway.com/curated/skyteam/" target="_blank" rel="noopener">顧問師天團・人才軍火庫</a></p></footer>
<script>
(function(){{
 var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('.card')),secs=[].slice.call(document.querySelectorAll('section'));
 q.addEventListener('input',function(){{
  var v=q.value.trim().toLowerCase();
  cards.forEach(function(c){{c.classList.toggle('hide',v&&c.dataset.s.indexOf(v)<0)}});
  secs.forEach(function(s){{var n=s.querySelectorAll('.card:not(.hide)').length;s.classList.toggle('hide',!n);s.querySelector('small').textContent=n+' 個'}});
 }});
}})();
</script></body></html>"""
(out / "index.html").write_text(page, encoding="utf-8")
print("ok", len(items), "items ->", out / "index.html")
