#!/usr/bin/env python3
"""深度挖掘每日記錄中的教練故事原料"""

import re, os
from glob import glob
from datetime import datetime

# 讀取所有每日記錄
daily_files = sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md'))
memory_files = sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md'))

all_text = ''
for f in daily_files + memory_files:
    try:
        all_text += open(f).read() + '\n\n'
    except:
        pass

print(f'掃描 {len(daily_files)} 個每日 + {len(memory_files)} 個記憶檔')
print(f'總文字量: {len(all_text):,} 字')

# ── 觸發詞正則 ─────────────────────────────────────────────────
TRIGGER_PATTERNS = [
    (r'「(.+?)」', '引號'),
    (r'『(.+?)』', '雙引號'),
]

HIGH_TRIGGERS = ['你到底', '你是不是', '我真的', '白費', '白忙', '不見了', '居然', '為什麼會',
                 '怎麼搞', '搞不清楚', '搞清楚', '無釐頭', '快被打敗', '道歉有屁',
                 '浪費我的', '三分鐘', '六十分鐘', '六十美元']

# ── 找出所有教練說話段落（找 👤 或 coach: 或 教練： 或 「） ──
# 先找教練情緒段
passages = []
# 以 👤 或 教練： 或 coach: 開頭的段落
speaker_patterns = [
    r'👤?\s*教練[：:]\s*["「]?(.+?)(?=\n\n|\n👤|\n🤖|\n[A-Z]|\Z)',
    r'(coach|Coach|COACH)[：:]\s*(.+?)(?=\n\n|\n[A-Z]|\Z)',
]

# 掃描整個文本，以空行分段
blocks = re.split(r'\n(?=\n)', all_text)

for block in blocks:
    block = block.strip()
    if len(block) < 30:
        continue

    # 找教練說的話
    coach_texts = []
    for m in re.finditer(r'👤\s*教練[：:]?\s*(.+?)(?=\n\n|\n🤖|\n💬|\Z)', block, re.S):
        coach_texts.append(m.group(1).strip())
    for m in re.finditer(r'教練[：:]\s*(.+?)(?=\n\n|\n[A-Z]|\Z)', block, re.S):
        t = m.group(1).strip()
        if len(t) > 10 and '教練' not in t[:10]:
            coach_texts.append(t)

    if not coach_texts:
        continue

    combined = ' '.join(coach_texts)

    # 找情緒觸發詞
    trigger = ''
    for ht in HIGH_TRIGGERS:
        if ht in combined:
            trigger = ht
            break

    # 評分
    score = 0
    if trigger: score += 3
    if any(w in combined for w in ['你到底', '你是不是', '我真的', '快被打敗', '道歉有屁']): score += 2
    if any(w in combined for w in ['白費', '白忙', '不見了', '居然', '浪費']): score += 1
    if len(combined) > 100: score += 1
    if re.search(r'[0-9]+[分小時次]', combined): score += 1

    if score >= 1 and trigger:
        # 找日期
        date_match = re.search(r'2026-[0-9]+-[0-9]+', block)
        date = date_match.group() if date_match else 'unknown'

        # 找 session id
        sid_match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
        sid = sid_match.group(1)[:8] if sid_match else 'unknown'

        # 找守則標記
        rules = re.findall(r'守則[：:]?\s*#?([0-9]+)', combined)
        rules += re.findall(r'#([0-9]+)', combined)
        rules = list(dict.fromkeys(rules))[:5]

        passages.append({
            'trigger': trigger,
            'score': score,
            'date': date,
            'sid': sid,
            'text': combined[:300],
            'rules': rules,
        })

# 去重（相似的段落合起來）
seen = set()
unique = []
for p in passages:
    key = p['trigger'] + p['text'][:50]
    if key not in seen:
        seen.add(key)
        unique.append(p)

unique.sort(key=lambda x: -x['score'])

print(f'找到 {len(unique)} 個獨立故事原料（去重後）\n')

# 輸出
print('=' * 60)
print('TOP 100 故事原料（深度挖掘版）')
print('=' * 60)

for i, p in enumerate(unique[:100], 1):
    print(f"\n{'─'*60}")
    print(f"#{i:03d} | 觸發：{p['trigger']} | 分:{p['score']} | 日期:{p['date']} | S:{p['sid']}…")
    print(f"守則：#{' #'.join(p['rules']) if p['rules'] else '?'}")
    # 只顯示教練說的話（去掉AI回應）
    lines = p['text'].split('\n')
    coach_lines = [l for l in lines if any(c in l for c in ['👤', '教練', 'Coach', '"', '「', '『'])]
    for cl in coach_lines[:4]:
        cl = cl.strip()
        if len(cl) > 5:
            print(f"  📣 {cl[:80]}")

# 寫檔
output_path = '/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_DEEP.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"# 故事清單（深度挖掘版）\n")
    f.write(f"> 挖掘時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"> 來源：每日記錄 + 記憶檔（共 {len(daily_files)} 個每日 + {len(memory_files)} 個記憶檔）\n")
    f.write(f"> 原始段落：{len(passages)} → 去重後：{len(unique)}\n\n")
    f.write('=' * 60 + '\n')
    for i, p in enumerate(unique, 1):
        f.write(f"#{i:03d} | 觸發：{p['trigger']} | 分:{p['score']} | {p['date']} | S:{p['sid']}\n")
        f.write(f"守則：#{' #'.join(p['rules']) if p['rules'] else '?'}\n")
        f.write(f"內容：{p['text'][:120]}\n\n")

print(f"\n✅ 已寫入 {output_path}")
print(f"共 {len(unique)} 個故事原料")