"""通用抽取器抽不出來、但頁面確實有公益足跡的頁面：各自的讀取規則（2026-10-25，8ccafe 的足跡在 JS 陣列裡）。
回傳格式同 fp_generic.extract_generic；sync_peers.run 先看這裡有沒有該 slug 的規則。"""
import json, os, re, html
from PIL import Image
from fp_generic import BASE, _name_role


def _save_photo(slug, src_path):
    im = Image.open(src_path).convert('RGB')
    if im.width > 720:
        im = im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS)
    out = f"{os.environ.get('SC_BASE') or BASE + '/social-club'}/assets/people/{slug}.jpg"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, 'JPEG', quality=82, optimize=True)
    return f'assets/people/{slug}.jpg', [im.width, im.height, os.path.getsize(out)]


def ccafe8():
    """8ccafe：足跡在 `const CHARITY = [...]`（icon/kind/title/text/src），主圖用雙協會捐贈儀式合影 p060。"""
    t = open(f'{BASE}/8ccafe/index.html', encoding='utf-8').read()
    arr = json.loads(re.search(r'const CHARITY = (\[.*?\]);\n', t, re.S).group(1))
    items = []
    for c in arr:
        s = c['src'][0] if c['src'] else ['', '']
        items.append(dict(yr=c['kind'], title=c['title'], desc=c['text'], src='出處：' + s[0], href=s[1] or None))
    photo = _save_photo('8ccafe', f'{BASE}/8ccafe/photos/web/p060.jpg')
    name, role = _name_role('8ccafe')
    return dict(slug='8ccafe', name=name, role=role, illustration=False, url='https://event.bymyway.com/curated/8ccafe/',
                anchor='#charity', lede='協會、待用咖啡、免費講座、長者關懷與捐贈──每一項都附出處。',
                stats=[], items=items, photo=list(photo), photo_alt='雙協會捐贈儀式合影（2026）', caption='雙協會捐贈儀式合影（2026）')


MANUAL = {'8ccafe': ccafe8}

# 通用抽取後要修的欄位（頁面把「狀態」放在說明位置、或圖是 AI 示意圖）
FIX = {
    'meihua': dict(illustration=True, items=[
        dict(yr='持續 7 年以上', title='救國團人際關係班', desc='長期參與，與學員一起學習待人處事。', src='出處：BNI 會員資料表（2026.01）', href=None),
        dict(yr='現任', title='台南市婦女聯會 委員', desc='參與地方婦女事務。', src='出處：BNI 會員資料表（2026.01）', href=None),
        dict(yr='2026', title='合作金庫退休員工聯誼會 會長', desc='為退休同仁服務。', src='出處：BNI 會員資料表（2026.01）', href=None),
    ]),
}
