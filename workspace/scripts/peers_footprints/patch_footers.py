import os, re, sys
BASE = os.path.expanduser('~/github_repos'); OUT = os.path.abspath('pv1')
R = 'https://event.bymyway.com/curated'
def a(href, text): return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'
VOL = a(f'{R}/rongtree/volunteer.html', '招募志工團隊')
SG = a(f'{R}/social-good/', '真公益')
SC = a(f'{R}/social-club/', '真公益・企業家俱樂部')
ROONG = a(f'{R}/rongtree/', '榮樹下')
EXTRA_INLINE = '　' + VOL + '　' + SG + '　' + SC   # 與 social-good 頁尾同樣的全形空格分隔
res = {}
for slug in ['ruifeng', 'lidie', 'angel-sister', 'andy-chen', 'patrick-chu']:
    t = open(f'{BASE}/{slug}/index.html', encoding='utf-8', newline='').read()
    if '招募志工團隊' in t[t.rfind('<footer'):]:
        res[slug] = 'already'; continue
    if slug == 'patrick-chu':
        old = f'<p>{a(R + "/rongtree/", "友善連結 榮樹下")}</p>'
        assert t.count(old) == 1, (slug, t.count(old))
        new = old + '\n  ' + f'<p>{a(R + "/rongtree/volunteer.html", "友善連結 招募志工團隊")}</p>' + '\n  ' + f'<p>{a(R + "/social-good/", "友善連結 真公益")}</p>' + '\n  ' + f'<p>{a(R + "/social-club/", "友善連結 真公益・企業家俱樂部")}</p>'
    else:
        f0 = t.rfind('<footer')
        i = t.find(ROONG, f0)
        assert i != -1 and t.count(ROONG, f0) == 1, (slug, 'anchor')
        old = ROONG; new = ROONG + EXTRA_INLINE
        # 只替換頁尾裡那一個
        t = t[:i] + new + t[i + len(old):]
        d = f'{OUT}/{slug}'; os.makedirs(d, exist_ok=True)
        open(f'{d}/index.html', 'w', encoding='utf-8', newline='').write(t)
        res[slug] = f'+{len(new)-len(old)} bytes'; continue
    t = t.replace(old, new, 1)
    d = f'{OUT}/{slug}'; os.makedirs(d, exist_ok=True)
    open(f'{d}/index.html', 'w', encoding='utf-8', newline='').write(t)
    res[slug] = f'+{len(new)-len(old)} bytes'
print(res)
