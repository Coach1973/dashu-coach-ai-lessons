#!/usr/bin/env python3
"""足跡夥伴自動同步（2026-10-25，教練：有公益足跡的網頁一律進真公益「足跡夥伴」，要自動化，事件觸發）。

用法：
  sync_peers.py <slug> [<slug>...]   新上架／更新的頁面：有公益足跡（≥3 則）就加進 fp_data.json 並重新產生區塊、推上線
  sync_peers.py --scan               掃全部策展頁，補上還沒進名單的（上架程式在批次處理完呼叫它）
環境變數 SC_BASE：改指定要寫的 social-club 副本（預覽用）；預設是正式倉庫並 commit＋push。
輸出最後一行 JSON：{"added":[...],"manual":[{"slug":..,"reason":..}],"pushed":true/false}
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DB_PATH = os.path.join(HERE, 'fp_data.json')
GH = os.path.expanduser('~/github_repos')
SC_LIVE = f'{GH}/social-club'
REG = os.path.expanduser('~/.openclaw/workspace/event-signup/curated_sites_registry.json')

# 教練 2026-10-16 給的前 6 位：頁面結構各不相同，用手寫抽取規則（extract_fp.py）；新加的人走通用抽取器
ORIGINAL_META = {
    'andy-chen': dict(caption='讀著孩子們寄來的感謝信', illustration=True),
    'ruifeng': dict(caption='短宣隊員與泰北長輩相擁'),
    'lidie': dict(caption='台新「您的一票 決定愛的力量」'),
    'patrick-chu': dict(caption='朱元中於行政院 PDIS 簡報全人樂活公益新創計畫'),
    'angel-sister': dict(caption='在高醫癌症兒童病房當志工，分享耶穌的愛（攝影／基督教今日報 林子騫）'),
    'social-good': dict(caption='蔦松藝術高中舞蹈科演出《舞扇清賢》（廖素貞／大紀元 2020）', btn='看發起人完整足跡'),
}
ORIGINAL_ORDER = ['andy-chen', 'ruifeng', 'lidie', 'patrick-chu', 'angel-sister', 'social-good']


# 不是個人頁、或已另外處理的：大樹教練＝social-good 那張卡；111-wei 是競選頁（「競選足跡」不是公益足跡）
EXCLUDE = {'social-club', 'social-good', 'skyteam', 'rongtree', 'coachwu', '111-wei', 'runforfuture', 'bigtree-2'}


# 頁面標題抓出來的名字／頭銜有些不適合直接當卡片標題，這裡逐位修正（新增的人預設用頁面標題，不對再加一行）
OVERRIDE = {
    'drsoonlin': dict(name='孫林博士 Dr. Soonlin', role='教學進化學院創辦人'),
    'kunting': dict(name='鄒昆廷老師', role='企業 AI 導入顧問・易經決策'),
    'zhou-ruiqi': dict(role='永樂市場資深布商・布思綠創辦人'),
    'lovingfamily': dict(name='李忠儒（戀家大叔）'),
    'charles-lin': dict(name='林家旭博士'),
}


def load_db():
    if os.path.exists(DB_PATH):
        return json.load(open(DB_PATH, encoding='utf-8'))
    import extract_fp
    rows = {d['slug']: d for d in extract_fp.run(save=True)}
    db = []
    for s in ORIGINAL_ORDER:
        d = rows[s]
        d['photo'] = [d['photo'][0], list(d['photo'][1])]
        d.update(ORIGINAL_META[s])
        db.append(d)
    save_db(db)
    return db


def save_db(db):
    json.dump(db, open(DB_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def upload_order():
    try:
        reg = json.load(open(REG, encoding='utf-8'))
        items = reg if isinstance(reg, list) else list(reg.values())[0]
        return [s['slug'] for s in sorted((x for x in items if isinstance(x, dict)), key=lambda x: x.get('uploaded_at', ''))]
    except Exception:
        return []


def run(slugs):
    import fp_generic
    db = load_db()
    have = {d['slug'] for d in db}
    added, manual = [], []
    for s in slugs:
        if s in have or s in EXCLUDE:
            continue
        if not os.path.exists(f'{GH}/{s}/index.html'):
            continue
        try:
            d = fp_generic.extract_generic(s, save=True)
        except Exception as e:  # noqa: BLE001
            manual.append(dict(slug=s, reason=f'抽取出錯 {e!r}'[:80]))
            continue
        if d is None:
            # 有公益足跡標題卻抽不出來才算「需人工」；整頁根本沒有公益足跡就安靜略過
            if fp_generic.LAST_REASON and fp_generic.LAST_REASON != '沒有公益足跡區塊':
                manual.append(dict(slug=s, reason=fp_generic.LAST_REASON))
            continue
        d.update(OVERRIDE.get(s, {}))
        db.append(d)
        added.append(s)
    if added:
        save_db(db)
    return db, added, manual


def render():
    r = subprocess.run([sys.executable, os.path.join(HERE, 'render_fp.py')], cwd=HERE, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()[-300:]


def publish(msg):
    if os.environ.get('SC_BASE'):
        return False
    st = subprocess.run(['git', '-C', SC_LIVE, 'status', '--short'], capture_output=True, text=True).stdout.strip()
    if not st:
        return False
    subprocess.run(['git', '-C', SC_LIVE, 'add', '-A', 'index.html', 'assets/people'], check=True)
    subprocess.run(['git', '-C', SC_LIVE, 'commit', '-q', '-m', msg + '\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>'], check=True)
    subprocess.run(['git', '-C', SC_LIVE, 'push', '-q', 'origin', 'main'], check=True)
    return True


def main():
    args = sys.argv[1:]
    names = [a for a in args if not a.startswith('--')]
    slugs = names or upload_order()
    db, added, manual = run(slugs)
    ok, out = (True, '')
    pushed = False
    if added or '--force' in args:
        ok, out = render()
        if ok:
            pushed = publish(f'[Mac] 足跡夥伴自動同步：新增 {len(added)} 位（{"、".join(added)}）')
    print(json.dumps(dict(added=added, manual=manual, render_ok=ok, pushed=pushed, total=len(db)), ensure_ascii=False))


if __name__ == '__main__':
    main()
