#!/usr/bin/env python3
"""嚴格評分：所有故事必須30分+，湊夠30個"""

import re, os
from glob import glob

# ═══════════════════════════════════════════════════════════
# 讀取所有文字
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
# 嚴格評分：這些才是真正的高分觸發
# ═══════════════════════════════════════════════════════════

# 超高分觸發（直接給30+）
GOLD_TRIGGERS = {
    '你到底': 40, '你到底在搞什麼': 40,
    '快被我打敗': 40, '快被打敗了': 40,
    '道歉有屁': 40, '道歉有個屁': 40,
    '浪費我的生命': 40, '浪費生命': 38,
    '生命都枯萎': 36,
    '你搞清楚我是誰': 36,
    '不負責任': 36,
}

# 高分觸發
HIGH_TRIGGERS = {
    '你們偷懶': 32, '偷懶': 30,
    '沒有人提醒': 32,
    'commit根本沒有成功': 32, 'commit根本沒成功': 32,
    '白忙': 32, '送出按鈕': 30,
    '60美元': 32, '60美金': 32, '60塊美金': 32,
    '居然': 30, '竟然': 30,
    '怎麼搞': 30, '怎麼搞的': 30,
    '不見了': 28, '不見了': 28,
    '天呀': 28, '天哪': 28,
    '見鬼': 28, '見鬼了': 28,
    '搞不清楚': 28, '搞不清': 28,
    '為什麼會': 26,
    '我真的': 26,
    '你又': 24, '你們又': 24,
    '白費': 24, '又來': 22,
    '搞砸': 24, '重來': 22,
}

# ═══════════════════════════════════════════════════════════
# 掃描 👤 教練段落
# ═══════════════════════════════════════════════════════════

print('掃描 👤 教練段落...')

blocks = re.split(r'\n\n+', all_text)
stories = []

for block in blocks:
    block = block.strip()
    if len(block) < 60:
        continue

    # 找 👤 教練的話
    coach_lines = []
    for line in block.split('\n'):
        if re.match(r'👤\s*教練', line):
            text = re.sub(r'^👤\s*教練[：:]?\s*', '', line).strip()
            if len(text) > 10:
                coach_lines.append(text)
        elif re.match(r'coach[：:]\s', line, re.I):
            text = re.sub(r'^coach[：:]\s*', '', line, flags=re.I).strip()
            if len(text) > 10:
                coach_lines.append(text)

    if not coach_lines:
        continue

    full = ' '.join(coach_lines)

    # 找觸發詞
    trigger = ''
    trigger_score = 0
    for kw, w in GOLD_TRIGGERS.items():
        if kw in full:
            trigger = kw; trigger_score = w; break
    if not trigger:
        for kw, w in HIGH_TRIGGERS.items():
            if kw in full:
                trigger = kw; trigger_score = w; break

    if not trigger:
        continue

    # 找日期
    date_match = re.search(r'2026-(?:0[4-5]|0[5-9]|10|11|12)-[0-3][0-9]', block)
    date = date_match.group() if date_match else 'unknown'

    # 找 session
    sid_match = re.findall(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
    sid = sid_match[0][:8] if sid_match else 'unknown'

    # 評分
    sc = trigger_score

    # 反轉加成
    reversal = ['但是', '結果', '沒想到', '居然', '竟然',
                '5秒', '30次', '50條', '30分鐘', '60',
                '白忙', '白費', '快被打敗', 'commit根本', '鐵板']
    if any(r in full for r in reversal): sc += 5

    # 具體數字加成
    factual = ['60', '30', '50', '100', 'commit', 'hash',
               '1GB', '3分鐘', '30分鐘', '5秒', '三四', '三四次']
    if any(f in full for f in factual): sc += 3

    # 質問情緒
    if '？' in full:
        q_words = ['為什麼', '怎麼', '到底', '是不是', '有沒有']
        if any(q in full for q in q_words): sc += 2

    # 文字長度（太短減分）
    if len(full) < 60: sc -= 10

    # 排除系統訊息
    if any(k in full for k in ['cron:', 'System:', '提醒您', '🦞 教練您好',
                                 '倒數計時', 'NotebookLM', '壽星', '執董週會']):
        continue

    # 排除媒體
    if '[media attached' in full: continue

    if sc < 25: continue

    # 去重（前100字）
    key = full[:100]
    stories.append({
        'trigger': trigger,
        'score': sc,
        'date': date,
        'sid': sid,
        'text': full,
        'key': key,
    })

# 去重
seen = {}
for s in stories:
    k = s['key']
    if k not in seen or s['score'] > seen[k]['score']:
        seen[k] = s

stories = list(seen.values())
stories.sort(key=lambda x: -x['score'])

print(f'找到 {len(stories)} 個 25分+ 故事\n')

# ═══════════════════════════════════════════════════════════
# 顯示結果
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print(f'🏆 30分+ 候選故事（共 {len([s for s in stories if s["score"] >= 30])} 個）')
print('═' * 70)

for i, s in enumerate(stories[:50], 1):
    tag = '✅' if s['score'] >= 30 else '⚠️'
    print(f"\n{tag} #{i:02d} | {s['trigger']} | 分:{s['score']} | {s['date']} | S:{s['sid']}…")
    print(f"  {s['text'][:160]}")

count_30plus = len([s for s in stories if s['score'] >= 30])
print(f"\n{'='*70}")
print(f"✅ 30分+ 故事：{count_30plus} 個")
print(f"⚠️ 25-29分故事：{len([s for s in stories if 25 <= s['score'] < 30])} 個")
print(f"💤 25分以下：{len([s for s in stories if s['score'] < 25])} 個")
print(f"\n目標 30個30分+：{'✅ 達標！' if count_30plus >= 30 else f'❌ 還差 {30-count_30plus} 個'}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_STRICT.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# 🏆 Top 30 故事（嚴格版：30分+）\n')
    f.write(f'> 評分時間：2026-05-31 17:45\n')
    f.write(f'> 評分標準：金牌觸發×反轉×數字×質問情緒\n')
    f.write(f'> 找到：{count_30plus} 個 30分+ 故事\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories[:30], 1):
        marker = '✅' if s['score'] >= 30 else '⚠️'
        f.write(f"\n## #{i:02d} {marker} {s['trigger']}\n")
        f.write(f"分數：{s['score']} | 日期：{s['date']} | S：{s['sid']}\n")
        f.write(f"故事：{s['text'][:400]}\n\n")

print(f"\n✅ 已寫入 {out}")