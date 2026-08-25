#!/usr/bin/env python3
"""深度挖掘：找比現有Top30更強的故事，替換弱的故事"""

import re, os
from glob import glob
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# 讀取所有蒸餾檔（找最強教練故事）
# ═══════════════════════════════════════════════════════════

distill_files = sorted(glob('/Users/bymyway/.claude-code/workspace/distill/*.md'))
daily_files   = sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md'))
mem_files     = sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md'))

all_text = ''
for f in distill_files + daily_files + mem_files:
    if os.path.exists(f):
        all_text += open(f).read() + '\n\n'

print(f'總文字量：{len(all_text):,} 字\n')

# ═══════════════════════════════════════════════════════════
# 超強觸發詞（這些分數要給最高）
# ═══════════════════════════════════════════════════════════

SUPER_TRIGGERS = [
    '你到底', '你到底在搞什麼',
    '快被打敗', '快被我打敗',
    '道歉有屁', '道歉有個屁',
    '浪費我的生命', '浪費生命',
    '生命都枯萎',
    '你搞清楚我是誰',
    '不見了', '不見',
    '搞不清楚', '搞不清',
    '為什麼會',
    '怎麼搞',
    '你們偷懶',
    '沒有人提醒',
    'commit根本沒有成功',
    '不負責任',
    '60美金', '60美元', '60塊',
    '白忙', '白費',
    '居然', '竟然',
    '無釐頭',
]

STRONG_TRIGGERS = [
    '你們每次', '你又', '我真的',
    '天呀', '見鬼', '搞砸',
    '重來', '又忘', '老是忘',
    '又來', '又出事',
    '老是', '一直',
]

# ═══════════════════════════════════════════════════════════
# 找 👤 教練段落（提取完整對話）
# ═══════════════════════════════════════════════════════════

print('掃描 👤 教練段落...')

# 找所有 👤 或 coach: 或 教練： 的段落
# 以連續空行分段
blocks = re.split(r'\n\n+', all_text)

stories = []
for block in blocks:
    block = block.strip()
    if len(block) < 80:
        continue

    # 找 👤 教練的話
    coach_lines = []
    for line in block.split('\n'):
        if re.match(r'👤\s*教練', line):
            # 去掉 👤 教練： 前綴
            text = re.sub(r'^👤\s*教練[：:]?\s*', '', line)
            text = text.strip()
            if len(text) > 10:
                coach_lines.append(text)
        elif re.match(r'coach[：:]\s', line, re.I):
            text = re.sub(r'^coach[：:]\s*', '', line, flags=re.I)
            text = text.strip()
            if len(text) > 10:
                coach_lines.append(text)

    if not coach_lines:
        continue

    full = ' '.join(coach_lines)

    # 找觸發詞
    trigger = ''
    level = 0
    for st in SUPER_TRIGGERS:
        if st in full:
            trigger = st
            level = 2
            break
    if level == 0:
        for st in STRONG_TRIGGERS:
            if st in full:
                trigger = st
                level = 1
                break

    # 找日期
    date_match = re.search(r'2026-(?:0[4-5]|0[5-9]|10|11|12)-[0-3][0-9]', block)
    date = date_match.group() if date_match else 'unknown'

    # 找 session
    sid_match = re.findall(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
    sid = sid_match[0][:8] if sid_match else 'unknown'

    # 評分
    sc = 0
    if level == 2: sc += 20  # 超強觸發
    elif level == 1: sc += 8  # 強觸發

    # 反轉/具體事實
    reversal = ['但是', '結果', '沒想到', '居然', '竟然',
                '5秒', '30次', '50條', '30分鐘', '60',
                '白忙', '白費', '快被打敗']
    if any(r in full for r in reversal): sc += 8

    # 具體數字
    factual = ['60', '30', '50', '100', 'commit', 'hash',
               '1GB', '3分鐘', '30分鐘', '5秒']
    if any(f in full for f in factual): sc += 5

    # 質問情緒
    if '？' in full or '?' in full: sc += 3
    if any(q in full for q in ['為什麼', '怎麼', '到底', '是不是', '有沒有']): sc += 3

    # 文字長度
    if len(full) > 200: sc += 3
    elif len(full) < 40: sc -= 5

    # 排除系統訊息
    if any(k in full for k in ['cron:', 'System:', '提醒您', '🦞 教練您好',
                                 '倒數計時', 'NotebookLM', '壽星', '執董週會']):
        continue

    # 排除媒體附件
    if '[media attached' in full: continue

    # 排除常見普通對話
    if sc < 5: continue

    # 去重（同觸發詞+同內容前60字）
    key = trigger + full[:80]
    stories.append({
        'trigger': trigger,
        'score': sc,
        'date': date,
        'sid': sid,
        'text': full,
        'key': key,
    })

# ═══════════════════════════════════════════════════════════
# 去重
# ═══════════════════════════════════════════════════════════

seen = {}
for s in stories:
    k = s['key']
    if k not in seen or s['score'] > seen[k]['score']:
        seen[k] = s

stories = list(seen.values())
stories.sort(key=lambda x: -x['score'])

print(f'找到 {len(stories)} 個有效故事\n')

# ═══════════════════════════════════════════════════════════
# 顯示 Top 50 候選
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print('🏆 TOP 50 候選（深度挖掘）')
print('═' * 70)

for i, s in enumerate(stories[:50], 1):
    text = s['text'][:160]
    marker = '🔴' if s['score'] >= 20 else '🟡' if s['score'] >= 10 else '  '
    print(f"\n{marker} #{i:02d} | {s['trigger']} | 分:{s['score']} | {s['date']} | S:{s['sid']}…")
    print(f"  故事：{text}")

# ═══════════════════════════════════════════════════════════
# 寫入完整 Top 50 檔案
# ═══════════════════════════════════════════════════════════

out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_DEEP.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# Top 30 故事（深度挖掘版）\n')
    f.write(f'> 挖掘時間：{datetime.now().strftime("%Y-%m-%d %H:%M")}\n')
    f.write(f'> 來源：蒸餾檔 + 每日記錄 + 記憶檔\n')
    f.write(f'> 評分：超強觸發×反轉×具體數字×質問情緒\n')
    f.write(f'> 找到：{len(stories)} 個有效故事\n\n')
    f.write('🔴 = 20分+（最高強度）\n')
    f.write('🟡 = 10-19分（強）\n')
    f.write('  = 5-9分（中等）\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories, 1):
        marker = '🔴' if s['score'] >= 20 else '🟡' if s['score'] >= 10 else ''
        f.write(f"\n## #{i:02d} {marker} {s['trigger']}\n")
        f.write(f"分數：{s['score']} | 日期：{s['date']} | S：{s['sid']}\n")
        f.write(f"故事：{s['text'][:400]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"Top 50 分數區間：{stories[0]['score']} ~ {stories[49]['score']}")
print(f"故事池：{len(stories)} 個")