#!/usr/bin/env python3
"""終極挖掘：從每日蒸餾檔中找教練原話故事原料"""

import re, os
from glob import glob
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# 收集所有蒸餾來源的教練原話
# ═══════════════════════════════════════════════════════════

DISTILL_FILES = [
    '/Users/bymyway/.claude-code/workspace/distill/terminal_2026-05-30_complete.md',  # 88 sessions!
    '/Users/bymyway/.claude-code/workspace/distill/terminal_2026-05-28.md',
    '/Users/bymyway/.claude-code/workspace/distill/terminal_2026-05-31.md',
    '/Users/bymyway/.claude-code/workspace/distill/超大檔蒸餾_終端機A_0525.md',
    '/Users/bymyway/.claude-code/workspace/distill/CloudCode桌面版對話精華_教練原聲.md',
    '/Users/bymyway/.claude-code/workspace/distill/top20_valuable_sessions.md',
    '/Users/bymyway/.claude-code/workspace/distill/terminalB_top50.md',
    '/Users/bymyway/.claude-code/workspace/distill/守則經典場景_21條全集.md',
]

# 讀所有 daily files
DAILY_FILES = sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md'))
MEM_FILES    = sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md'))

all_text = ''
for f in DISTILL_FILES + DAILY_FILES + MEM_FILES:
    if os.path.exists(f):
        all_text += open(f).read() + '\n\n'

print(f'總文字量：{len(all_text):,} 字')

# ═══════════════════════════════════════════════════════════
# 找所有 👤 教練說的話段落
# ═══════════════════════════════════════════════════════════

# 觸發詞定義
HIGH = [
    '你到底', '你是不是', '你又', '我真的', '快被打敗',
    '道歉有屁', '道歉有個屁', '浪費我的生命', '生命都枯萎',
    '你搞清楚了嗎', '你搞清楚', '你搞清楚我是誰',
    '為什麼要問', '為什麼要分三次',
]
MED = [
    '白費', '白忙', '不見了', '不見', '居然',
    '為什麼會', '怎麼搞', '搞不清楚', '搞砸',
    '無釐頭', '天呀', '見鬼了',
    '60美金', '60美元', '六十美元',
    '重新', '又忘', '老是忘',
    'commit在哪', 'hash在哪',
    '沒有人提醒', '沒有回應',
]

# ═══════════════════════════════════════════════════════════
# 找 👤 教練段落
# ═══════════════════════════════════════════════════════════

# 把所有 👤 教練：... 的段落抽出來
passages = []
current = None
buffer = []

for line in all_text.split('\n'):
    m = re.match(r'👤\s*教練[：:]?\s*(.*)', line)
    if m:
        if buffer and current:
            current['lines'].extend(buffer)
        text = m.group(1).strip()
        if text:
            current = {
                'text': text,
                'lines': [text],
                'session': 'unknown',
                'date': 'unknown',
            }
            buffer = []
        else:
            buffer = []
            if current:
                buffer = []
    elif current:
        buffer.append(line)
        # 遇到 🤖 或空行 = 段落結束
        if line.startswith('🤖') or (line.strip() == '' and len(buffer) > 3):
            current['lines'] = [l for l in current['lines'] if l.strip()]
            full = ' '.join(current['lines'])
            if len(full) > 15:
                current['full'] = full
                passages.append(current)
            current = None
            buffer = []

# ═══════════════════════════════════════════════════════════
# 評分
# ═══════════════════════════════════════════════════════════

def score(p):
    text = p.get('full', p.get('text', ''))
    s = 0
    for ht in HIGH:
        if ht in text:
            s += 5
            break
    if not s:
        for mt in MED:
            if mt in text:
                s += 3
                break
    # 有具體數字/事實
    if re.search(r'[0-9]+[天次分鐘]', text): s += 1
    # 有問句情緒
    if re.search(r'[？?！!]', text): s += 1
    # 長度適中
    if 30 < len(text) < 300: s += 1
    return s

for p in passages:
    p['score'] = score(p)

passages.sort(key=lambda x: -x['score'])

# 去重（相同觸發詞 + 前50字相似）
seen = set()
unique = []
for p in passages:
    key = p.get('full', p.get('text', ''))[:60]
    # 找觸發詞
    trigger = ''
    for ht in HIGH:
        if ht in key:
            trigger = ht; break
    if not trigger:
        for mt in MED:
            if mt in key:
                trigger = mt; break
    h = hash(trigger + key)
    if h not in seen:
        seen.add(h)
        unique.append(p)

print(f'找到 {len(passages)} 個教練段落 → 去重後 {len(unique)} 個獨立故事\n')

# ═══════════════════════════════════════════════════════════
# 產出 TOP 120
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print(f'TOP 120 故事原料（終極挖掘版）')
print('═' * 70)

for i, p in enumerate(unique[:120], 1):
    text = p.get('full', p.get('text', ''))
    # 清理行號殘留
    text = re.sub(r'^\d+\s+', '', text)
    text = re.sub(r'\s*\d+\s+(「)', r' \1', text)
    print(f"\n#{i:03d} | 分:{p['score']} | S:{p['session']}…")
    # 找出觸發詞
    trigger = ''
    for ht in HIGH:
        if ht in text: trigger = ht; break
    if not trigger:
        for mt in MED:
            if mt in text: trigger = mt; break
    if trigger:
        print(f"  🔥 觸發：{trigger}")
    print(f"  📣 {text[:120]}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_ULTIMATE.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write(f"# 故事清單（終極挖掘版）\n")
    f.write(f"> 挖掘時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"> 來源：蒸餾檔({len(DISTILL_FILES)}) + 每日({len(DAILY_FILES)}) + 記憶({len(MEM_FILES)})\n")
    f.write(f"> 總文字量：{len(all_text):,} 字\n")
    f.write(f"> 找到：{len(passages)} 個教練段落 → 去重後：{len(unique)} 個獨立故事\n\n")
    f.write('═' * 70 + '\n')
    for i, p in enumerate(unique, 1):
        text = p.get('full', p.get('text', ''))
        text = re.sub(r'^\d+\s+', '', text)
        trigger = ''
        for ht in HIGH:
            if ht in text: trigger = ht; break
        if not trigger:
            for mt in MED:
                if mt in text: trigger = mt; break
        f.write(f"#{i:03d} | 觸發：{trigger} | 分:{p['score']}\n")
        f.write(f"內容：{text[:200]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"目標100+：{'✅ 達標 ' + str(len(unique)) + ' 筆' if len(unique) >= 100 else '❌ 還差 ' + str(100 - len(unique)) + ' 筆'}")