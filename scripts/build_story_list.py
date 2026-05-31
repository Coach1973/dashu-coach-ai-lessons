#!/usr/bin/env python3
"""從接力棒提取所有原料，去重，產出 Top 30 故事清單"""

import re

raw = open('/Users/bymyway/.claude-code/workspace/JUNSHI_HANDOFF_LATEST.md').read()

# 提取 | C-XX | #NNN | title | ✅ | trigger | 這類行
lines = [l for l in raw.split('\n') if re.match(r'\| C-\d+ \|', l)]
print(f'共 {len(lines)} 個原料行')

# 解析每行：| C-01 | #107 | 誰允許它切回去的？ | ✅ | 切回去 |
stories = []
for line in lines:
    parts = [p.strip() for p in line.split('|')]
    # parts: ['', 'C-01', '#107', '誰允許...', '✅', '切回去', '']
    cid = parts[1]
    mat_raw = parts[2]
    title = parts[3]
    trigger = parts[5]  # ✅ 在 parts[4]，真正的 trigger 在 parts[5]

    # 提取 session ID
    sid_match = re.search(r'\(([a-f0-9-]+)\)', mat_raw)
    sid = sid_match.group(1) if sid_match else 'unknown'

    stories.append({'cid': cid, 'sid': sid, 'title': title, 'trigger': trigger})

print(f'觸發詞樣本: {[s["trigger"] for s in stories[:5]]}')

# 評分函數
def score(s):
    t = s['trigger']
    score_map = {
        '你到底': 3, '你到底在搞什麼': 3, '你是不是': 3, '你又不是': 3,
        '白費': 2, '不見了': 2, '偷懶': 2, '白忙': 2,
        '搞不清楚': 2, '搞清楚': 2, '居然': 2,
        '重新做': 1, '為什麼會': 1, '還記得': 1, '怎麼搞': 1,
    }
    base = score_map.get(t, 1)
    title = s['title']
    if 'commit' in title.lower(): base += 1
    if '居然' in title: base += 1
    if '白忙' in title or '白費' in title: base += 1
    return base

# 按 session 分組，每組只留最高分
from collections import defaultdict
by_sid = defaultdict(list)
for s in stories:
    by_sid[s['sid']].append(s)

unique = []
for sid, group in by_sid.items():
    best = max(group, key=score)
    best['score'] = score(best)
    unique.append(best)

# 排序
unique.sort(key=lambda x: -x['score'])

print(f'去重後 {len(unique)} 個獨立 session')
print()
print('## Top 25 故事清單（去重版）\n')
for i, s in enumerate(unique[:25], 1):
    print(f"{i:02d}. 【{s['cid']}】{s['title']}")
    print(f"    Session: {s['sid']} | 觸發詞: {s['trigger']} | 分數: {s['score']}")
    print()