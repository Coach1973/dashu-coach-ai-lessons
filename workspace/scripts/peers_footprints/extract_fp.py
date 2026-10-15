"""從各人頁面的「公益足跡」區塊逐字抽出文字與主圖（不重打字，避免抄錯）。"""
import re, os, io, json, base64, html
from html.parser import HTMLParser
from PIL import Image

BASE = os.path.expanduser('~/github_repos')
VOID = {'img', 'br', 'hr', 'input', 'meta', 'link', 'source', 'wbr'}


class N:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []
        self.text = None

    def cls(self):
        return set((self.attrs.get('class') or '').split())

    def walk(self):
        for k in self.kids:
            if isinstance(k, N):
                yield k
                yield from k.walk()


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = N('root', {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = N(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.kids.append(N(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.kids.append(data)


def parse(fragment):
    p = P()
    p.feed(fragment)
    return p.root


def txt(n):
    out = []

    def rec(x):
        if isinstance(x, str):
            out.append(x)
        elif x.tag in ('script', 'style', 'svg'):
            return
        elif x.tag == 'br':
            out.append(' ')
        else:
            for k in x.kids:
                rec(k)
    rec(n)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


def find(n, tag=None, c=None):
    for x in n.walk():
        if (tag is None or x.tag == tag) and (c is None or c in x.cls()):
            yield x


def first(n, tag=None, c=None):
    return next(find(n, tag, c), None)


def section_html(page, start_pat):
    t = open(f'{BASE}/{page}/index.html', encoding='utf-8').read()
    b = t[t.find('<body'):]
    m = re.search(start_pat, b)
    e = b.find('</section>', m.start())
    return b[m.start():e + len('</section>')]


ALTS = {}


def save_photo(img, slug):
    ALTS[slug] = img.attrs.get('alt', '')
    src = img.attrs.get('src', '')
    m = re.match(r'data:image/[a-z+]+;base64,(.*)', src, re.S)
    if not m:
        return None, src
    im = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
    w = 720
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    d = f'{BASE}/social-club/assets/people'
    os.makedirs(d, exist_ok=True)
    path = f'{d}/{slug}.jpg'
    im.save(path, 'JPEG', quality=82, optimize=True)
    return f'assets/people/{slug}.jpg', (im.width, im.height, os.path.getsize(path))


def src_of(n):
    """出處：回傳 (文字, 連結或 None)"""
    if n is None:
        return ('', None)
    a = n if n.tag == 'a' else first(n, 'a')
    return (txt(n), a.attrs.get('href') if a else None)


PEOPLE = []


def person(slug, page, name, role, start, anchor, **kw):
    PEOPLE.append(dict(slug=slug, page=page, name=name, role=role, start=start, anchor=anchor, **kw))


def run(save=True):
    out = []
    for p in PEOPLE:
        sec = parse(section_html(p['page'], p['start']))
        d = dict(slug=p['slug'], name=p['name'], role=p['role'], url=f"https://event.bymyway.com/curated/{p['page']}/", anchor=p['anchor'])
        d.update(p['fn'](sec, p['slug'], save))
        d['photo_alt'] = ALTS.get(p['slug'], '')
        out.append(d)
    return out


# ---------- 各頁面的抽取規則 ----------
def f_ruifeng(sec, slug, save):
    r = {}
    r['lede'] = txt(first(sec, 'p', 'lede'))
    r['stats'] = [(txt(first(x, 'b')), txt(first(x, 'span'))) for x in find(first(sec, None, 'ch-nums'), 'div', 'num')]
    r['items'] = []
    for a in find(sec, 'article', 'fp'):
        fpb = first(a, 'div', 'fpb')
        ps = [k for k in fpb.kids if isinstance(k, N) and k.tag == 'p']
        s_t, s_h = src_of(first(fpb, 'a', 'src'))
        r['items'].append(dict(yr=txt(first(fpb, 'p', 'fpy')), title=txt(first(fpb, 'h3')), desc=txt(ps[-1]), src=s_t, href=s_h))
    r['photo'] = save_photo(first(first(sec, 'figure', 'ch-photo'), 'img'), slug) if save else None
    return r


def f_lidie(sec, slug, save):
    r = {}
    intro = first(sec, 'div', 'gy-intro')
    r['lede'] = txt([k for k in first(intro, 'div').kids if isinstance(k, N) and k.tag == 'p'][0])
    r['stats'] = [(txt(first(x, 'b')), txt(first(x, 'span'))) for x in first(sec, 'div', 'gnums').kids if isinstance(x, N) and x.tag == 'div']
    r['items'] = []
    for a in find(sec, 'article', 'fp'):
        ft = first(a, 'div', 'ft')
        s_t, s_h = src_of(first(ft, 'a'))
        ps = [k for k in ft.kids if isinstance(k, N) and k.tag == 'p']
        r['items'].append(dict(yr=txt(first(ft, 'span', 'y')), title=txt(first(ft, 'h4')), desc=txt(ps[0]) if ps else '', src=s_t, href=s_h))
    r['photo'] = save_photo(first(first(sec, 'div', 'gy-ph'), 'img'), slug) if save else None
    return r


def f_patrick(sec, slug, save):
    r = {}
    r['lede'] = ''
    for p_ in find(sec, 'p'):
        if txt(p_).startswith('他沒有把公益當成'):
            r['lede'] = txt(p_)
            break
    r['stats'] = []
    for x in find(sec, 'div', 'gs'):
        b = txt(first(x, 'b'))
        r['stats'].append((b, txt(first(x, 'span')) + (('（' + txt(first(x, 'small')) + '）') if first(x, 'small') else '')))
    r['items'] = []
    for li in find(sec, 'li', 'fp-step'):
        r['items'].append(dict(yr=txt(first(li, 'p', 'fp-yr')), title=txt(first(li, 'h3')), desc=txt(first(li, 'p', 'fp-txt')), src=txt(first(li, 'p', 'fp-src')), href=None))
    r['photo'] = save_photo(first(sec, 'img'), slug) if save else None
    return r


def f_angel(sec, slug, save):
    r = {}
    cover = first(sec, 'div', 'fp-cover')
    r['lede'] = txt([k for k in find(cover, 'p') if not k.cls()][0])
    r['stats'] = []
    for x in first(sec, 'div', 'fp-stats').kids:
        if isinstance(x, N) and x.tag == 'div':
            r['stats'].append((txt(first(x, 'b')), txt(first(x, 'span')) + '（' + txt(first(x, 'i')) + '）'))
    r['items'] = []
    for it in find(sec, 'div', 'tl-item'):
        card = first(it, None, 'tl-card') or it
        ps = [k for k in find(card, 'p') if not k.cls()]
        s_t, s_h = src_of(first(card, None, 'src'))
        s_t = re.sub(r'^示意插畫', '', s_t)
        r['items'].append(dict(yr=txt(first(card, 'time')), title=txt(first(card, 'h4')), desc=txt(ps[0]) if ps else '', src=s_t, href=s_h))
    r['photo'] = save_photo(first(first(cover, 'figure'), 'img'), slug) if save else None
    return r


def f_andy(sec, slug, save):
    r = {}
    intro = first(sec, 'div', 'give-intro')
    r['lede'] = txt([k for k in find(first(intro, 'div'), 'p') if not k.cls()][0])
    r['stats'] = [(txt(first(x, 'b')), txt(first(x, 'span'))) for x in first(sec, 'div', 'gnums').kids if isinstance(x, N) and x.tag == 'div']
    r['items'] = []
    for li in find(sec, 'li', 'fpi'):
        d = first(li, 'div')
        ps = [k for k in d.kids if isinstance(k, N) and k.tag == 'p' and not k.cls()]
        s_t, s_h = src_of(first(d, 'p', 'src'))
        r['items'].append(dict(yr=txt(first(d, 'p', 'yr')), title=txt(first(d, 'h4')), desc=txt(ps[0]) if ps else '', src=s_t, href=s_h))
    r['photo'] = save_photo(first(first(intro, 'figure'), 'img'), slug) if save else None
    return r


def f_coach(sec, slug, save):
    r = {}
    founder = parse(section_html('social-good', r'<section class="bio" id="founder"'))
    case = parse(section_html('social-good', r'<section class="case"'))
    r['lede'] = txt(first(founder, 'p', 'lead'))
    r['stats'] = [('21 場', '2019 蔦松公益巡講，歷時約 3 個月'), ('130 餘萬', '扣除場地費後全數捐給蔦松藝術高中'), ('NT$300', '每人酌收，交通、路費、住宿發起人自理'), ('第 16 場', '桃園企業主聽完當場加碼捐 100 萬')]
    r['items'] = []
    for it in find(sec, 'li', 'tl-item'):
        s_t, s_h = src_of(first(it, 'span', 'src'))
        r['items'].append(dict(yr=txt(first(it, 'div', 'tl-year')), title=txt(first(it, 'h4')), desc=txt(find(first(it, 'div', 'tl-text'), 'p').__next__()), src=s_t, href=s_h))
    img = first(case, 'img')
    r['photo'] = save_photo(img, slug) if (save and img is not None) else None
    return r


person('ruifeng', 'ruifeng', '何瑞峰牧師', '華岡福音隊・泰緬邊境同行', r'<section class="charity"', '#charity', fn=f_ruifeng)
person('lidie', 'lidie', '張麗蝶董事長', 'T1科技 ‧ 元照科技照明', r'<section class="sec cream" id="giving"', '#giving', fn=f_lidie)
person('patrick-chu', 'patrick-chu', '朱元中顧問', '天下顧問・B 型企業', r'<section class="good"', '#good', fn=f_patrick)
person('angel-sister', 'angel-sister', '陳淑玲天使姐姐', 'CBMC 高雄一分會會長・職場宣教者', r'<section id="footprint"', '#footprint', fn=f_angel)
person('andy-chen', 'andy-chen', '陳顯立執行長', '好廣告數據創辦人・《信任效應》作者', r'<section class="sec give"', '#give', fn=f_andy)
person('social-good', 'social-good', '大樹教練・吳大樹', '真公益發起人', r'<section class="tlsec"', '#founder', fn=f_coach)

if __name__ == '__main__':
    data = run(save=False)
    for d in data:
        print('=====', d['name'], 'stats', len(d.get('stats', [])), 'items', len(d['items']))
        print('  lede:', d.get('lede', '')[:60])
        print('  stats:', d.get('stats'))
        for it in d['items'][:2] + d['items'][-1:]:
            print('  -', it['yr'], '|', it['title'], '|', it['desc'][:40], '|', it['src'][:30], it['href'])
