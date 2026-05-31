#!/usr/bin/env python3
"""湊滿30個：門檻降到20分+，嚴格去重"""

import re, os
from glob import glob
from collections import defaultdict

sources = [
    *sorted(glob('/Users/bymyway/.claude-code/workspace/distill/*.md')),
    *sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md')),
    *sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md')),
]
all_text = '\n\n'.join(open(f).read() for f in sources if os.path.exists(f))
print(f'文字量：{len(all_text):,} 字\n')

# ═══════════════════════════════════════════════════════════
# 評分
# ═══════════════════════════════════════════════════════════

TRIGGERS = {
    '快被我打敗': 50, '快被打敗了': 50, '快被打敗': 50,
    '你到底': 45, '你到底有沒有': 45,
    '你們偷懶': 42, '偷懶': 38,
    '不負責任': 40,
    '浪費我的生命': 45,
    '道歉有屁': 45, '道歉有個屁': 45,
    '沒有人提醒': 38,
    '白忙': 38, '白忙一場': 40,
    '送出按鈕': 40, '送出按鈕沒有': 42,
    '60美金': 40, '60美元': 40, '60塊': 40, '60塊美金': 42,
    '居然': 35, '竟然': 35,
    '不見了': 34, '不見': 30, '不見了': 34,
    '怎麼搞': 34, '怎麼搞的': 34,
    '你搞清楚': 32, '搞不清楚': 30, '搞不清': 30,
    '為什麼會': 30,
    '為什麼會這樣': 35,
    '你又': 28, '我又': 28,
    '我又當': 30, '我又當': 30,
    '白費': 28,
    '你們每次': 30,
    '失敗': 26,
    '錯了': 24, '搞砸': 26,
    '你確定': 22,
    '你應該': 20,
    '每次都': 22,
    '一直': 22,
    '你們每次': 28,
    '不行': 24,
}

def score(text):
    sc = 0
    for kw, w in TRIGGERS.items():
        if kw in text:
            sc = max(sc, w)
    if sc == 0: return 0

    for r in ['但是', '結果', '沒想到', '居然', '竟然', '5秒', '30分鐘',
               'commit根本', '鐵板', '我又', '我又說']:
        if r in text: sc += 5; break

    for f in ['60', '30', '50', '100', '三四', '1GB', '5秒', '1.2B']:
        if f in text: sc += 3; break

    if '？' in text or '?' in text: sc += 2
    if len(text) < 50: sc -= 10
    elif len(text) > 200: sc += 2

    return sc

def clean(text):
    text = re.sub(r'^\d+\s+', '', text)
    text = re.sub(r'\d+\s+(「)', r'\1', text)
    text = re.sub(r'\[media attached.*?\]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'data:image.*?base64,', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(r'### .*', '', text)
    text = re.sub(r'\|.*?\|', '', text)
    text = re.sub(r'\*+', '', text)
    return text.strip()

# ═══════════════════════════════════════════════════════════
# 掃描
# ═══════════════════════════════════════════════════════════

stories = []
blocks = re.split(r'\n\n+', all_text)

for block in blocks:
    block = block.strip()
    if len(block) < 80: continue

    coach_parts = []
    for line in block.split('\n'):
        m = re.match(r'👤\s*教練[：:]?\s*(.+)', line)
        if m: coach_parts.append(m.group(1).strip())
        m = re.match(r'教練[：:]\s*(.{15,})', line)
        if m and '教練' not in m.group(1)[:15]: coach_parts.append(m.group(1).strip())
        m = re.match(r'coach[：:]\s*(.{15,})', line, re.I)
        if m: coach_parts.append(m.group(1).strip())
        m = re.match(r'大樹教練[：:]\s*(.{15,})', line)
        if m: coach_parts.append(m.group(1).strip())

    if not coach_parts: continue
    full = ' '.join(coach_parts)
    sc = score(full)
    if sc < 20: continue

    if any(k in full for k in ['cron:', 'System:', '提醒您', '🦞 教練您好',
                               '倒數計時', 'NotebookLM', '壽星', '執董週會',
                               r'\[media attached', 'Exec completed',
                               'FB.*壽星', '每四小時', 'GitHub Actions',
                               'data:image', 'base64,']): continue

    sids = re.findall(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
    sid = sids[0][:8] if sids else 'unknown'

    trigger = ''
    for kw in TRIGGERS:
        if kw in full:
            trigger = kw; break

    key = trigger + clean(full)[:60]

    stories.append({'trigger': trigger, 'score': sc, 'sid': sid,
                   'text': full, 'key': key})

# ═══════════════════════════════════════════════════════════
# 去重（情節分組）
# ═══════════════════════════════════════════════════════════

# 按情節分組
PLOT_TRIGGERS = [
    ('送出按鈕', ['送出按鈕', '白忙', '白忙一場', '白費']),
    ('60美金扣款', ['60美金', '60美元', '60塊', '60塊美金', '扣了']),
    ('接力棒失憶', ['偷懶', '新視窗', '接力棒', '開工兩個字']),
    ('你到底思考', ['你到底', '有沒有在思考', '有沒有認真', '法則']),
    ('守則沒讀', ['法則', '守則', '讀完', '規則']),
    ('commit失敗', ['commit', 'commit根本', 'hash']),
    ('流程不見', ['不見了', '不見', '流程', '精彩']),
    ('Missing API', ['Missing API', 'API key', 'auth']),
    ('搞不清楚', ['搞不清楚', '搞不清', '不知道']),
    ('你又當', ['我又', '我又當', '你又']),
]

def get_plot(s):
    t = s['trigger']
    text = s['text']
    for plot_name, keywords in PLOT_TRIGGERS:
        for kw in keywords:
            if kw in text:
                return plot_name
    return t or '其他'

by_plot = defaultdict(list)
for s in stories:
    plot = get_plot(s)
    by_plot[plot].append(s)

# 每個情節只留最高分
unique = []
seen_plots = set()
for plot, group in by_plot.items():
    best = max(group, key=lambda x: x['score'])
    if plot not in seen_plots:
        seen_plots.add(plot)
        unique.append(best)
    else:
        # 如果情節相同但分更高，替換
        for i, existing in enumerate(unique):
            if get_plot(existing) == plot and best['score'] > existing['score']:
                unique[i] = best
                break

# 排序
unique.sort(key=lambda x: -x['score'])

print(f'情節去重後：{len(unique)} 個故事')
count_20 = len([s for s in unique if s['score'] >= 20])
print(f'20分+：{count_20} 個\n')

# ═══════════════════════════════════════════════════════════
# 如果湊不滿30個，放寬到情節內再多留幾個
# ═══════════════════════════════════════════════════════════

if len(unique) < 30:
    print(f'湊不滿30個，放寬標準...')
    # 每個情節多留2個
    for plot, group in by_plot.items():
        group.sort(key=lambda x: -x['score'])
        for i, s in enumerate(group[:3]):
            key = get_plot(s) + clean(s['text'])[:30]
            if all(clean(e['text'])[:30] != clean(s['text'])[:30] for e in unique):
                unique.append(s)
                if len(unique) >= 40: break
        if len(unique) >= 40: break

    unique.sort(key=lambda x: -x['score'])
    unique = unique[:40]
    print(f'放寬後：{len(unique)} 個故事')

count_20 = len([s for s in unique if s['score'] >= 20])
print(f'\n最終：{len(unique)} 個故事 | 20分+：{count_20} 個')

# ═══════════════════════════════════════════════════════════
# 顯示
# ═══════════════════════════════════════════════════════════

print('\n' + '='*70)
print(f'🏆 TOP {len(unique)} 故事（20分+）')
print('='*70)

for i, s in enumerate(unique, 1):
    tag = '✅' if s['score'] >= 30 else '🟡' if s['score'] >= 20 else '⚠️'
    text = clean(s['text'])[:150]
    print(f"\n{tag} #{i:02d} | {s['trigger']} | 分:{s['score']} | S:{s['sid']}…")
    print(f"  {text}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_20PTS.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# 🏆 Top 30 故事（20分+版）\n')
    f.write(f'> 評分時間：2026-05-31 18:00\n')
    f.write(f'> 門檻：20分+ | 找到：{len(unique)} 個 | 20分+：{count_20} 個\n\n')
    f.write('✅ = 30分+（金牌）\n')
    f.write('🟡 = 20-29分（銀牌）\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(unique[:30], 1):
        tag = '✅' if s['score'] >= 30 else '🟡' if s['score'] >= 20 else '⚠️'
        text = clean(s['text'])[:400]
        f.write(f"\n## #{i:02d} {tag} {s['trigger']}\n")
        f.write(f"分數：{s['score']} | Session：{s['sid']}\n")
        f.write(f"故事：{text}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"20分+：{count_20} 個 | 目標湊30個：{'✅ 達標！' if count_20 >= 30 else f'還差 {30-count_20} 個'}")