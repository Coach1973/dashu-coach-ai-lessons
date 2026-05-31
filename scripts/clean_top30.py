#!/usr/bin/env python3
"""產出乾淨 Top 30（去重+清理系統訊息）"""

import re

data = open('/Users/bymyway/.claude-code/workspace/distill/_TOP30_DEEP.md').read()

# ═══════════════════════════════════════════════════════════
# 解析故事
# ═══════════════════════════════════════════════════════════

stories = []
lines = data.split('\n')

i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'## #(\d+)\s+(.+?)\s*$', line)
    if m:
        num = int(m.group(1))
        marker_part = m.group(2).strip()
        # 找分數行
        score = 0
        j = i + 1
        content = []
        next_num = None
        while j < len(lines):
            nl = lines[j]
            nm = re.match(r'## #(\d+)', nl)
            if nm:
                next_num = int(nm.group(1))
                break
            if nl.startswith('分數：'):
                sm = re.search(r'分數：(\d+)', nl)
                if sm: score = int(sm.group(1))
            elif nl.startswith('故事：'):
                content.append(nl.replace('故事：', '').strip())
            j += 1
        text = '\n'.join(content).strip()

        # 跳過系統訊息和媒體
        if any(k in text for k in ['Exec completed', 'System (untrusted)',
                                     '\[media attached', 'Telegram:', 'LINE:',
                                     'cron:', '提醒您', '🦞 教練您好']):
            i = next_num or (i+1); continue
        if not text or len(text) < 30:
            i = next_num or (i+1); continue

        # 觸發詞
        trigger = re.search(r'🔴\s*(.+?)$|🟡\s*(.+?)$', marker_part)
        t = (trigger.group(1) or trigger.group(2) if trigger else '').strip()

        stories.append({
            'num': num,
            'trigger': t,
            'score': score,
            'text': text,
        })
        i = next_num or (i+1)
    else:
        i += 1

# 去重（按內容前80字）
seen = {}
for s in stories:
    k = s['text'][:80]
    if k not in seen or s['score'] > seen[k]['score']:
        seen[k] = s

stories = list(seen.values())
stories.sort(key=lambda x: -x['score'])

print(f'去重後：{len(stories)} 個故事\n')

# ═══════════════════════════════════════════════════════════
# 產出 Top 30
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print('🏆 TOP 30 故事（乾淨版）')
print('═' * 70)

for i, s in enumerate(stories[:30], 1):
    t = s['trigger'] or '（情緒關鍵詞）'
    marker = '🔴' if s['score'] >= 20 else '🟡' if s['score'] >= 10 else '  '
    print(f"\n{marker} #{i:02d} | {t} | 分:{s['score']}")
    print(f"  {s['text'][:180]}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_FINAL.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# 🏆 Top 30 故事（最終版）\n')
    f.write('> 評分時間：2026-05-31 17:40\n')
    f.write('> 來源：深度挖掘156個→去重→Top30\n')
    f.write('> 評分：觸發詞強度×反轉×具體數字×質問情緒\n\n')
    f.write('🔴 = 20分+（最高強度）\n')
    f.write('🟡 = 10-19分（強）\n')
    f.write('  = 5-9分（中等）\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories[:30], 1):
        t = s['trigger'] or '（情緒關鍵詞）'
        marker = '🔴' if s['score'] >= 20 else '🟡' if s['score'] >= 10 else ''
        f.write(f"\n## #{i:02d} {marker} {t}\n")
        f.write(f"分數：{s['score']}\n")
        f.write(f"故事：{s['text'][:400]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"Top 30 分數區間：{stories[0]['score']} ~ {stories[29]['score']}")