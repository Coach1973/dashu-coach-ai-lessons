"""通用「公益足跡」抽取器（2026-10-25，教練：有公益足跡的網頁一律進真公益的足跡夥伴區，要自動化）。

從 ~/github_repos/<slug>/index.html 找「公益，是有足跡的。」那個區塊（或 id=charity/good/giving/footprint），
逐字抽出：導言、數字、足跡時間軸（年份／標題／說明／出處）、主圖。足跡不到 MIN_ITEMS 則不收（量不夠）。
"""
import io, os, re, base64, html
from PIL import Image
from extract_fp import parse, find, first, txt, N, BASE

MIN_ITEMS = 3
LAST_REASON = ''
PAGE_TEXT = {}
HEAD = '公益，是有足跡的'
FALLBACK_IDS = ('charity', 'good', 'giving', 'footprint', 'give')
ITEM_CLS = {'fp', 'fpi', 'fp-step', 'tl-item'}
YR_CLS = {'yr', 'y', 'fpy', 'fp-yr', 'tl-year', 'year'}
SRC_CLS = {'src', 'fp-src'}
SKIP_P = {'unit', 'kicker', 'eyebrow', 'cap', 'src', 'yr', 'fpy', 'fp-yr', 'fp-src', 'n'}


def _balanced(b, start):
    """從 start 位置的開始標籤，找到配對的結束標籤，回傳整段。"""
    m = re.match(r'<([a-zA-Z0-9]+)', b[start:])
    tag = m.group(1)
    depth, pos = 0, start
    for mm in re.finditer(r'<(/?)%s\b[^>]*>' % tag, b[start:]):
        depth += -1 if mm.group(1) else 1
        if depth == 0:
            return b[start:start + mm.end()]
    return b[start:]


def _section_html(page):
    t = open(f'{BASE}/{page}/index.html', encoding='utf-8', errors='replace').read()
    PAGE_TEXT[page] = t
    b = t[t.find('<body'):]
    i = b.find(HEAD)
    start = None
    if i >= 0:
        s = b.rfind('<section', 0, i)
        start = s if s >= 0 else None
    if start is None:
        for sid in FALLBACK_IDS:
            m = re.search(r'<(section|div)[^>]*id="%s"' % sid, b)
            if m:
                start = m.start()
                break
    if start is None:
        return None
    return _balanced(b, start)


def _txt_no(n, skip_cls):
    out = []

    def rec(x):
        if isinstance(x, str):
            out.append(x)
        elif x.tag in ('script', 'style', 'svg') or (x.cls() & skip_cls):
            return
        elif x.tag == 'br':
            out.append(' ')
        else:
            for k in x.kids:
                rec(k)
    rec(n)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


def _anc(n):
    p = n.parent
    while p is not None:
        yield p
        p = p.parent


YEAR = re.compile(r'^\s*((19|20)\d{2}|長期|至今|持續|近年|每年|現在|目前|多年)')


def _year_node(n):
    for x in n.walk():
        if x.tag in ('b', 'strong') and '｜' in txt(x) and YEAR.match(txt(x).split('｜')[0]) and len(txt(x).split('｜')[0]) <= 14:
            return x
        if (x.cls() & YR_CLS) and 1 <= len(txt(x)) <= 24:
            return x
        s = txt(x)
        if x.tag in ('time', 'span', 'p', 'div', 'b', 'strong', 'i', 'small') and 2 <= len(s) <= 14 and YEAR.match(s):
            return x
    return None


def _title_node(n):
    for tg in ('h3', 'h4', 'h5', 'strong', 'b'):
        x = first(n, tg)
        if x is not None and txt(x) and (not YEAR.match(txt(x)) or '｜' in txt(x)):
            return x
    for x in n.walk():
        if any(c in ('t', 'ttl', 'title', 'tt', 'nm') or 'title' in c for c in x.cls()) and txt(x) and not YEAR.match(txt(x)):
            return x
    for x in n.walk():
        if x.tag in ('span', 'p') and not (x.cls() & YR_CLS) and 6 <= len(txt(x)) <= 90 and not YEAR.match(txt(x)):
            return x
    return None


def _items(sec):
    best, bn = [], 0
    for par in [sec] + list(sec.walk()):
        kids = [k for k in par.kids if isinstance(k, N)]
        groups = {}
        for k in kids:
            groups.setdefault((k.tag, (sorted(k.cls()) or [''])[0]), []).append(k)
        for g in groups.values():
            ok = [k for k in g if _title_node(k) is not None and _year_node(k) is not None]
            if len(ok) >= 3 and len(ok) >= 0.5 * len(g) and len(ok) > bn:
                best, bn = g, len(g)
    nodes = best
    out = []
    for n in nodes:
        title = _title_node(n)
        yrn = _year_node(n)
        if title is None:
            continue
        srcn = next((x for x in n.walk() if any('src' in c or 'source' in c for c in x.cls())), None)
        skip = {c for x in n.walk() for c in x.cls() if 'src' in c or 'source' in c}
        desc = ''
        for p in find(n, 'p'):
            s = _txt_no(p, skip)
            if s and p is not yrn and not YEAR.match(s) and p.parent is not None and not (p.cls() & SKIP_P):
                desc = s
                break
        if not desc:  # 沒有 <p>：取標題之外最長的一段文字
            cands = [_txt_no(x, skip) for x in n.walk() if x.tag in ('div', 'span') and x is not yrn and x is not srcn]
            cands = [c for c in cands if c and c != txt(title) and not YEAR.match(c) and txt(title) not in c[:len(txt(title)) + 1]]
            desc = max(cands, key=len) if cands else ''
        if srcn is not None:
            a = srcn if srcn.tag == 'a' else first(srcn, 'a')
            s_t = txt(srcn)
        else:
            al = list(find(n, 'a'))
            a = al[-1] if al else None
            s_t = txt(a) if a is not None else ''
        s_t = re.sub(r'^示意插畫', '', s_t).strip()
        yr_t, ti_t = (txt(yrn) if yrn is not None else ''), txt(title)
        if yrn is not None and yrn is title and '｜' in ti_t:
            yr_t, ti_t = ti_t.split('｜', 1)
            if not desc:  # 說明是 <b> 後面的零散文字
                desc = _txt_no(n, skip | set(c for c in title.cls())).replace(txt(title), '').strip()
        out.append(dict(yr=yr_t, title=ti_t, desc=desc, src=s_t,
                        href=(a.attrs.get('href') if a is not None else None)))
    return out, nodes


def _stats(sec, nodes):
    inside = {id(x) for it in nodes for x in [it] + list(it.walk())}
    for c in sec.walk():
        if c.tag != 'div' or id(c) in inside:
            continue
        kids = [k for k in c.kids if isinstance(k, N) and k.tag == 'div']
        good = [k for k in kids if first(k, 'b') is not None and first(k, 'span') is not None
                and first(k, 'img') is None and len(txt(first(k, 'b'))) <= 14]
        if len(good) >= 3 and len(good) == len(kids):
            return [(txt(first(k, 'b')), txt(first(k, 'span'))) for k in good]
    return []


def _lede(sec):
    h = next((x for x in sec.walk() if x.tag == 'h2' and HEAD in txt(x)), None)
    if h is not None and h.parent is not None:
        past = False
        for k in h.parent.kids:
            if k is h:
                past = True
                continue
            if past and isinstance(k, N) and k.tag == 'p' and not (k.cls() & SKIP_P) and len(txt(k)) > 15:
                return txt(k)
    for p in find(sec, 'p'):
        if not (p.cls() & SKIP_P) and len(txt(p)) > 30:
            return txt(p)
    return ''


def _photo(sec, slug, nodes, save=True):
    inside = {id(x) for it in nodes for x in [it] + list(it.walk())}
    for img in find(sec, 'img'):
        if id(img) in inside:
            continue
        src = img.attrs.get('src', '')
        if not src and img.attrs.get('data-k'):
            km = re.search(r'["\']?%s["\']?\s*:\s*["\'](data:image/[a-z+]+;base64,[^"\']+)' % re.escape(img.attrs['data-k']), PAGE_TEXT.get(slug, ''))
            src = km.group(1) if km else ''
        im = None
        try:
            m = re.match(r'data:image/[a-z+]+;base64,(.*)', src, re.S)
            if m:
                im = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGB')
            elif src and not src.startswith(('http', '//')):
                im = Image.open(os.path.join(BASE, slug, src.split('?')[0].lstrip('/'))).convert('RGB')
        except Exception:
            im = None
        if im is None or im.width < 120:
            continue
        if im.width > 720:
            im = im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS)
        path = f"{os.environ.get('SC_BASE') or BASE + '/social-club'}/assets/people/{slug}.jpg"
        size = 0
        if save:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            im.save(path, 'JPEG', quality=82, optimize=True)
            size = os.path.getsize(path)
        cap = ''
        for k in (img.parent.kids if img.parent is not None else []):
            if isinstance(k, N) and (k.tag == 'figcaption' or 'cap' in k.cls()):
                cap = txt(k)
                break
        return f'assets/people/{slug}.jpg', [im.width, im.height, size], img.attrs.get('alt', ''), cap
    return None


def _name_role(page):
    t = open(f'{BASE}/{page}/index.html', encoding='utf-8', errors='replace').read()
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    title = html.unescape(m.group(1)).strip() if m else page
    parts = [x.strip() for x in re.split(r'[｜|]', title) if x.strip()]
    name = re.sub(r'^Dr\.?\s*', '', parts[0]) if parts else page
    role = '・'.join(parts[1:3]) if len(parts) > 1 else ''
    return name, role


def extract_generic(slug, save=True):
    """回傳可寫進 fp_data.json 的 dict；沒有公益足跡、量不夠或抓不到主圖回 None。"""
    global LAST_REASON
    sh = _section_html(slug)
    if not sh:
        LAST_REASON = '沒有公益足跡區塊'
        return None
    sec = parse(sh)
    items, nodes = _items(sec)
    if len(items) < MIN_ITEMS:
        LAST_REASON = f'足跡只有 {len(items)} 則（不到 {MIN_ITEMS} 則）'
        return None
    ph = _photo(sec, slug, nodes, save)
    if ph is None:
        try:
            ph = _photo(parse(PAGE_TEXT[slug][PAGE_TEXT[slug].find('<body'):]), slug, [], save)
        except Exception:
            ph = None
    if ph is None:
        LAST_REASON = '區塊裡找不到可用的主圖'
        return None
    LAST_REASON = ''
    name, role = _name_role(slug)
    sid = re.search(r'<section[^>]*id="([^"]+)"', sh[:400])
    ill = (ph[3] or ph[2]).startswith('示意插畫') or ph[2].startswith('示意插畫')
    cap = re.sub(r'^示意插畫[\s：:｜-]*', '', ph[3] or ph[2])
    return dict(slug=slug, name=name, role=role, illustration=ill, url=f'https://event.bymyway.com/curated/{slug}/',
                anchor=('#' + sid.group(1)) if sid else '', lede=_lede(sec), stats=_stats(sec, nodes), items=items,
                photo=[ph[0], ph[1]], photo_alt=ph[2], caption=cap)
