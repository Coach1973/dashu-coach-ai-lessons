"""把 fp_data.json 產生成「首批足跡夥伴」區塊，並（可重複執行地）放進 social-club/index.html。"""
import json, os, re, html
from PIL import Image

BASE = os.environ.get('SC_BASE') or os.path.expanduser('~/github_repos/social-club')
data = {d['slug']: d for d in json.load(open('fp_data.json', encoding='utf-8'))}
esc = lambda s: html.escape(s or '', quote=True)

ORDER = ['andy-chen', 'ruifeng', 'lidie', 'patrick-chu', 'angel-sister', 'social-good']  # 教練給的順序；吳錦昌＝順發示範單位，放最後
CAPTION = {
    'social-good': '蔦松藝術高中舞蹈科演出《舞扇清賢》（廖素貞／大紀元 2020）',
    'andy-chen': '讀著孩子們寄來的感謝信',
    'ruifeng': '短宣隊員與泰北長輩相擁',
    'lidie': '台新「您的一票 決定愛的力量」',
    'patrick-chu': '朱元中於行政院 PDIS 簡報全人樂活公益新創計畫',
    'angel-sister': '在高醫癌症兒童病房當志工，分享耶穌的愛（攝影／基督教今日報 林子騫）',
}
ILLUSTRATION = {'andy-chen'}  # 原頁標示「示意插畫」的圖，這裡一樣要標
BTN_TEXT = {'social-good': '看發起人完整足跡'}

def card(d):
    slug = d['slug']
    path, meta = d['photo']
    w, h = Image.open(f'{BASE}/{path}').size
    stats = ''.join(f'<div><b>{esc(n)}</b><span>{esc(l)}</span></div>' for n, l in d['stats'])
    items = []
    for it in d['items']:
        src = esc(it['src'])
        if it['href']:
            # 出處文字整段當連結（與原頁一致）
            src = f'<a href="{esc(it["href"])}" target="_blank" rel="noopener">{src}</a>'
        items.append(f'<li><span class="yr">{esc(it["yr"])}</span><div><h4>{esc(it["title"])}</h4>' + (f'<p>{esc(it["desc"])}</p>' if it['desc'] else '') + (f'<span class="src">{src}</span>' if it['src'] else '') + '</div></li>')
    tag = '<span class="pe-tag">示意插畫</span>' if slug in ILLUSTRATION else ''
    btn = BTN_TEXT.get(slug, '看完整專屬頁')
    return f'''<article class="pe" id="pe-{slug}">
  <figure class="pe-photo"><img src="{path}" alt="{esc(d['photo_alt'])}" width="{w}" height="{h}" loading="lazy">{tag}<figcaption>{esc(CAPTION[slug])}</figcaption></figure>
  <div class="pe-body">
    <p class="pe-role">{esc(d['role'])}</p>
    <h3>{esc(d['name'])}</h3>
    <p class="pe-lede">{esc(d['lede'])}</p>
    <div class="pe-stats">{stats}</div>
    <div class="pe-actions"><a class="btn btn-blue" href="{esc(d['url'] + d['anchor'])}" target="_blank" rel="noopener">{btn} <span class="arrow" aria-hidden="true">→</span></a></div>
  </div>
  <details class="pe-tl"><summary>展開足跡時間軸（{len(d['items'])} 則）</summary><ol>{''.join(items)}</ol></details>
</article>'''

roster = ''.join(f'<li><a href="#pe-{s}">{esc(data[s]["name"])}</a></li>' for s in ORDER)
roster += '<li class="sun"><a href="#sunfar">吳錦昌董事長・順發示範單位</a></li>'
SECTION = f'''<!-- PEERS-START（2026-10-16 教練交辦：首批足跡夥伴；內容由各人專屬頁面的「公益足跡」逐字擷取） -->
<section class="peers" id="peers" aria-labelledby="pe-title">
  <div class="wrap">
    <div class="pe-head">
      <div class="eyebrow">首批足跡夥伴・已有 7 位</div>
      <h2 id="pe-title">好事，已經有人在做了。</h2>
      <p class="lead">不用等到一百位。順發之外，已有 6 位的公益足跡整理成專屬網頁，每一則足跡都附出處。以下是他們頁面裡的「公益足跡」，原文擷取；想看完整故事，點「看完整專屬頁」。</p>
    </div>
    <ul class="pe-roster" aria-label="首批足跡夥伴名單">{roster}</ul>
    <div class="pe-list">
{chr(10).join(card(data[s]) for s in ORDER)}
    </div>
    <p class="pe-note">足跡內容與照片擷取自各人專屬頁面，出處標示於每則足跡；照片版權屬原拍攝與發布單位。標示「待本人確認」的項目，尚待本人確認。</p>
  </div>
</section>
<!-- PEERS-END -->
'''

CSS = '''/* PEERS-CSS-START：首批足跡夥伴（字一律 ≥20px） */
.peers{background:#fff;padding:140px 0}
.peers h2{font-size:clamp(34px,4.4vw,56px);line-height:1.25;margin:18px 0 26px}
.pe-head{max-width:46em}
.pe-roster{list-style:none;margin:40px 0 56px;padding:0;display:flex;flex-wrap:wrap;gap:12px}
.pe-roster a{display:inline-flex;align-items:center;min-height:52px;padding:10px 22px;border:2px solid var(--line);border-radius:999px;background:var(--mist);color:var(--ink);font:700 20px/1.3 var(--sans);text-decoration:none}
.pe-roster a:hover,.pe-roster a:focus-visible{border-color:var(--blue);background:var(--sky)}
.pe-roster .sun a{background:var(--sun);border-color:var(--sun)}
.pe-list{display:grid;gap:40px}
.pe{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;box-shadow:0 12px 40px -24px rgba(10,31,61,.35);scroll-margin-top:96px}
.pe-photo{margin:0;position:relative;background:var(--sky);display:flex;flex-direction:column}
.pe-photo img{width:100%;flex:1;min-height:260px;object-fit:cover;display:block}
.pe-photo figcaption{padding:14px 20px;font:500 20px/1.5 var(--sans);color:var(--ink-soft);background:var(--mist)}
.pe-tag{position:absolute;top:14px;left:14px;background:rgba(10,31,61,.82);color:#fff;font:700 20px/1 var(--sans);padding:8px 14px;border-radius:999px}
.pe-body{padding:40px 44px 36px;min-width:0}
.pe-role{margin:0;font:700 20px/1.5 var(--sans);color:var(--blue);letter-spacing:.06em}
.pe h3{font-size:clamp(30px,3vw,38px);line-height:1.3;margin:6px 0 14px}
.pe-lede{font:400 21px/1.85 var(--sans);color:var(--ink-soft);margin:0 0 26px}
.pe-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid var(--line)}
.pe-stats div{padding:18px 18px 18px 0;border-bottom:1px solid var(--line)}
.pe-stats div:nth-child(odd){padding-right:24px}
.pe-stats b{display:block;font:800 34px/1.2 var(--serif);color:var(--blue-deep)}
.pe-stats span{display:block;font:400 20px/1.55 var(--sans);color:var(--ink-soft);margin-top:4px}
.pe-actions{display:flex;flex-wrap:wrap;gap:14px;margin-top:28px}
.pe-actions .btn{padding:16px 26px;min-height:56px}
.btn-blue{background:var(--blue);color:#fff}
.btn-blue:hover,.btn-blue:focus-visible{background:var(--blue-deep)}
.pe-tl{grid-column:1/-1;border-top:1px solid var(--line);background:var(--mist)}
.pe-tl>summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:22px 44px;min-height:64px;font:700 20px/1.4 var(--sans);color:var(--ink)}
.pe-tl>summary::-webkit-details-marker{display:none}
.pe-tl>summary::after{content:"＋";font-size:28px;color:var(--blue)}
.pe-tl[open]>summary::after{content:"－"}
.pe-tl ol{list-style:none;margin:0;padding:6px 44px 36px}
.pe-tl li{display:grid;grid-template-columns:9.5em minmax(0,1fr);gap:8px 24px;padding:20px 0;border-top:1px solid var(--line)}
.pe-tl .yr{font:800 20px/1.5 var(--sans);color:var(--blue)}
.pe-tl h4{font:700 22px/1.5 var(--serif);margin:0 0 6px;color:var(--ink)}
.pe-tl p{font:400 20px/1.75 var(--sans);color:var(--ink-soft);margin:0}
.pe-tl .src{display:block;margin-top:8px;font:500 20px/1.6 var(--sans);color:var(--ink-soft)}
.pe-tl .src a{color:var(--blue)}
.pe-note{margin:44px 0 0;font:400 20px/1.8 var(--sans);color:var(--ink-soft)}
@media (max-width:1000px){.pe{grid-template-columns:1fr}.pe-photo img{min-height:0;aspect-ratio:16/10}.pe-body{padding:32px 26px 28px}.pe-tl>summary{padding:20px 26px}.pe-tl ol{padding:6px 26px 30px}}
@media (max-width:700px){.peers{padding:100px 0}.pe-stats{grid-template-columns:1fr}.pe-stats div,.pe-stats div:nth-child(odd){padding-right:0}.pe-tl li{grid-template-columns:1fr;gap:4px}}
/* PEERS-CSS-END */
'''

NAV_ITEM = '<li class="opt"><a href="#peers">足跡夥伴</a></li>\n        '

p = f'{BASE}/index.html'
t = open(p, encoding='utf-8').read()
# 先移除舊的（可重複執行）
t = re.sub(r'<!-- PEERS-START.*?<!-- PEERS-END -->\n', '', t, flags=re.S)
t = re.sub(r'/\* PEERS-CSS-START.*?/\* PEERS-CSS-END \*/\n', '', t, flags=re.S)
t = t.replace(NAV_ITEM, '')
# 放進去
i = t.index('</style>')
t = t[:i] + CSS + t[i:]
m = re.search(r'<section class="media"', t)
# 如果媒體牆前面有 HTML 註解，放在註解前面
cm = re.search(r'<!--[^>]*-->\s*$', t[:m.start()])
at = cm.start() if cm else m.start()
t = t[:at] + SECTION + t[at:]
nav_anchor = '<li class="opt"><a href="#sunfar">順發示範</a></li>\n        '
assert nav_anchor in t
t = t.replace(nav_anchor, nav_anchor + NAV_ITEM)
# 導覽列多一項「足跡夥伴」後，1181～1234px 寬最右邊按鈕會被擠出畫面 → 漢堡選單門檻從 1180 提高到 1260（CSS 與 nav-burger 兩處要一起改）
t = t.replace('@media (max-width:1180px){.nav ul li.opt{display:none}}', '@media (max-width:1260px){.nav ul li.opt{display:none}}')
t = t.replace('data-bp="1180"', 'data-bp="1260"')
assert '@media (max-width:1260px){.nav ul li.opt{display:none}}' in t and 'data-bp="1260"' in t
open(p, 'w', encoding='utf-8').write(t)
print('ok', len(t))
