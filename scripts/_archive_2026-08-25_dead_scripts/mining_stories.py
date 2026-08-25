#!/usr/bin/env python3
"""從原料堆挖故事，跑出100+筆故事清單"""

import re
from datetime import datetime

raw = open('/Users/bymyway/.claude-code/workspace/distill/_RAW_MATERIALS_FOR_JUNSHI.md').read()

# 以 "### 原料 #" 為界切成段落
segments = re.split(r'\n(?=### 原料 #)', raw)
segments = [s for s in segments if s.strip()]
print(f'共切成 {len(segments)} 個段落')

stories = []
for seg in segments:
    # 提取原料編號
    num_match = re.search(r'原料 #(\d+)', seg)
    cid = num_match.group(1) if num_match else '?'

    # Session ID
    sid_match = re.search(r'Session ID[：:]\s*`?([a-f0-9-]{36})`?', seg)
    sid = sid_match.group(1)[:8] if sid_match else 'unknown'

    # 觸發詞（第一個「情緒觸發詞」）
    trigger_match = re.search(r'情緒觸發詞[：:]\s*[「"\'(](.+?)[)」"\'\)]', seg)
    trigger = trigger_match.group(1) if trigger_match else ''

    # 教練引述（第一段 > 開頭）
    quotes = re.findall(r'>\s*["「]([^"」]{10,80})["」]', seg)
    coach_quotes = quotes[:3] if quotes else []

    # 原始段落（找 ``` 包起來的）
    code_blocks = re.findall(r'```[\s\S]*?```', seg)
    raw_text = ''
    for block in code_blocks:
        # 去掉 ``` 標記
        cleaned = re.sub(r'```\w*', '', block)
        raw_text += cleaned[:200] + '...'

    # 守則DNA（找 #數字）
    rules = re.findall(r'#(\d+)', seg)
    rules = list(dict.fromkeys(rules))[:5]  # 去重取前5個

    # 對話輪數
    coach_match = re.search(r'教練\s*(\d+)\s*輪', seg)
    ai_match = re.search(r'AI\s*(\d+)\s*輪', seg)
    coach_rounds = int(coach_match.group(1)) if coach_match else 0
    ai_rounds = int(ai_match.group(1)) if ai_match else 0

    stories.append({
        'cid': cid,
        'sid': sid,
        'trigger': trigger,
        'coach_quotes': coach_quotes,
        'raw_snippet': raw_text[:100],
        'rules': rules,
        'coach_rounds': coach_rounds,
        'ai_rounds': ai_rounds,
    })

print(f'解析出 {len(stories)} 個故事')
print()

# 評分
def score(s):
    t = s['trigger']
    base = 0
    if any(w in t for w in ['你到底', '你是不是', '你又', '我真的很']): base += 4
    elif any(w in t for w in ['居然', '白費', '不見了', '白忙', '搞砸']): base += 3
    elif any(w in t for w in ['搞不清楚', '搞清楚', '怎麼搞', '重新']): base += 2
    elif t: base += 1

    if s['coach_rounds'] >= 4: base += 2
    elif s['coach_rounds'] >= 2: base += 1

    if s['coach_quotes']: base += 1

    if len(s['raw_snippet']) > 50: base += 1

    return base

for s in stories:
    s['score'] = score(s)

stories.sort(key=lambda x: -x['score'])

print('=' * 60)
print(f'Top 50 故事清單（按評分排序）')
print('=' * 60)

for i, s in enumerate(stories[:50], 1):
    print(f"\n{'─'*50}")
    print(f"#{i:03d} 【#{s['cid']}】Session: {s['sid']}…")
    print(f"觸發詞：{s['trigger']}")
    print(f"分數：{s['score']} | 教練{s['coach_rounds']}輪+AI{s['ai_rounds']}輪")
    if s['coach_quotes']:
        print(f"教練金句：")
        for q in s['coach_quotes'][:2]:
            print(f"  → {q[:60]}")
    if s['rules']:
        print(f"守則DNA：#{' #'.join(s['rules'])}")
    print(f"原料：{s['raw_snippet'][:80]}")

# 寫入檔案
output = open('/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_100.md', 'w', encoding='utf-8')
output.write(f"# 故事清單（共 {len(stories)} 筆）\n")
output.write(f"> 挖掘時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
output.write(f"> 評分：觸發詞強度 × 教練輪數 × 有無引述\n\n")
output.write('─' * 60 + '\n')
for i, s in enumerate(stories, 1):
    output.write(f"#{i:03d} | #{s['cid']} | {s['sid']}… | {s['trigger']} | 分:{s['score']} | 守則:#{' #'.join(s['rules'])}\n")
    if s['coach_quotes']:
        for q in s['coach_quotes'][:2]:
            output.write(f"  → {q[:70]}\n")

output.close()
print(f"\n已寫入 distill/_STORY_LIST_100.md（共{len(stories)}筆）")