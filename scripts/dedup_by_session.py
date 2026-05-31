#!/usr/bin/env python3
"""從全量挖掘清單，去重到100+個獨立Session故事"""

import re

data = open('/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_FULL.md').read()

# 解析每個故事
entries = []
current = {}
for line in data.split('\n'):
    m = re.match(r'#(\d+)\s*\|\s*觸發：(.+?)\s*\|\s*分:(\d+)\s*\|\s*(.+?)\s*\|\s*S:(.+)', line)
    if m:
        if current:
            entries.append(current)
        current = {
            'num': m.group(1),
            'trigger': m.group(2),
            'score': int(m.group(3)),
            'date': m.group(4),
            'sid': m.group(5).strip(),
        }
    elif current:
        if line.startswith('守則：'):
            current['rules'] = line.replace('守則：', '').strip()
        elif line.startswith('內容：'):
            current['text'] = line.replace('內容：', '').strip()
if current:
    entries.append(current)

print(f'解析 {len(entries)} 個故事片段')

# 按 Session ID 分組，每組只留最高分
from collections import defaultdict
by_sid = defaultdict(list)
for e in entries:
    by_sid[e.get('sid', 'unknown')].append(e)

print(f'Session 數量: {len(by_sid)}')

# 評分函數
def score_entry(e):
    s = e.get('score', 0)
    t = e.get('trigger', '')
    if any(w in t for w in ['你到底', '你是不是', '我真的', '快被打敗', '道歉有屁']): s += 3
    elif any(w in t for w in ['白費', '白忙', '不見', '居然', '搞砸']): s += 2
    return s

# 每組取最佳
unique = []
seen_texts = set()
for sid, group in by_sid.items():
    best = max(group, key=score_entry)
    text = best.get('text', '')[:60]
    if text not in seen_texts:
        seen_texts.add(text)
        unique.append(best)

unique.sort(key=lambda x: -score_entry(x))

print(f'去重後獨立故事: {len(unique)} 筆\n')

# 顯示前 120
print('═' * 70)
print(f'TOP 120 獨立故事（按Session去重）')
print('═' * 70)

for i, e in enumerate(unique[:120], 1):
    print(f"\n#{i:03d} | 觸發：{e['trigger']} | 分:{e.get('score',0)} | {e.get('date','?')} | S:{e.get('sid','?')}…")
    if e.get('rules'):
        print(f"  守則：{e['rules']}")
    text = e.get('text', '')
    # 清理行號
    text = re.sub(r'^\d+\s+', '', text)
    text = re.sub(r'\d+\s+(「)', r'\1', text)
    print(f"  → {text[:100]}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_120.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write(f"# 獨立故事清單（按Session去重）\n")
    f.write(f"> 挖掘時間：2026-05-31 17:20\n")
    f.write(f"> 獨立Session數：{len(by_sid)} | 去重後故事：{len(unique)} 筆\n\n")
    f.write('═' * 70 + '\n')
    for i, e in enumerate(unique, 1):
        f.write(f"#{i:03d} | 觸發：{e['trigger']} | 分:{e.get('score',0)} | {e.get('date','?')} | S:{e.get('sid','?')}\n")
        if e.get('rules'):
            f.write(f"守則：{e['rules']}\n")
        text = e.get('text', '')
        text = re.sub(r'^\d+\s+', '', text)
        f.write(f"內容：{text[:150]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"目標100+：{'✅ 達標 ' + str(len(unique)) + ' 筆' if len(unique) >= 100 else '❌ 還差 ' + str(100 - len(unique)) + ' 筆'}")