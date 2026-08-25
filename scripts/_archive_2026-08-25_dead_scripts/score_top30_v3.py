#!/usr/bin/env python3
"""從448個故事中直接評分，取Top 30"""

import re

data = open('/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_FINAL.md').read()

# ═══════════════════════════════════════════════════════════
# 評分權重
# ═══════════════════════════════════════════════════════════

TRIGGER_WEIGHT = {
    '你到底': 15, '你是不是': 10, '快被打敗': 15,
    '道歉有屁': 15, '浪費我的生命': 15, '生命都枯萎': 12,
    '你搞清楚': 8, '不見了': 8, '搞不清楚': 7,
    '為什麼會': 7, '怎麼搞': 8, '無釐頭': 8,
    '天呀': 6, '見鬼': 6, '白費': 6, '白忙': 6,
    '居然': 6, '重來': 4, '重新': 3,
}

# ═══════════════════════════════════════════════════════════
# 解析故事（直接讀所有故事，不管有沒有觸發詞）
# ═══════════════════════════════════════════════════════════

stories = []
lines = data.split('\n')

i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'#(\d+)\s*⭐?\s*🔶?\s*\|\s*觸發：\s*\|\s*分:(\d+)', line)
    if m:
        num = m.group(1)
        base_score = int(m.group(2))
        # 讀內容
        content_lines = []
        j = i + 1
        while j < len(lines) and lines[j]:
            if re.match(r'^#\d', lines[j]):
                break
            content_lines.append(lines[j])
            j += 1
        text = '\n'.join(content_lines)
        text = re.sub(r'^故事：', '', text).strip()
        text = re.sub(r'^\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'^\d+\s+', '', text)
        text = re.sub(r'\s*\d+\s+(「)', r' \1', text)

        # 跳過系統訊息
        system_kw = ['cron:', 'System:', 'Exec completed', '提醒您', '倒數計時',
                      'NotebookLM', '壽星', '執董週會', '小人提',
                      r'\[media attached', '頂級特助分工群',
                      'EchoTokens', 'SYNTROL', 'Netlify 每個月',
                      '小籠蝦', 'c工作', 'c工作的',
                      '可能', '每四小時', '每30分鐘', '每15分鐘',
                      '繳納', '年會', '教練您好', '🦞']
        if any(k in text for k in system_kw):
            i = j; continue
        if len(text) < 20:
            i = j; continue

        stories.append({
            'num': num,
            'base': base_score,
            'text': text,
            'trigger': '',
        })
        i = j
    else:
        i += 1

# 同時解析有觸發詞的（⭐那批）
i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'#(\d+)\s*⭐?\s*🔶?\s*\|\s*觸發：(.+?)\s*\|\s*分:(\d+)', line)
    if m:
        num = m.group(1)
        trigger = m.group(2).strip()
        base_score = int(m.group(3))
        if trigger and trigger not in ['', ' ']:
            content_lines = []
            j = i + 1
            while j < len(lines) and lines[j]:
                if re.match(r'^#\d', lines[j]):
                    break
                content_lines.append(lines[j])
                j += 1
            text = '\n'.join(content_lines)
            text = re.sub(r'^故事：', '', text).strip()
            text = re.sub(r'^\*\*(.+?)\*\*', r'\1', text)
            text = re.sub(r'^\d+\s+', '', text)
            text = re.sub(r'\s*\d+\s+(「)', r' \1', text)

            if len(text) >= 20:
                stories.append({
                    'num': num,
                    'trigger': trigger,
                    'base': base_score,
                    'text': text,
                })
            i = j
        else:
            i += 1
    else:
        i += 1

print(f'有效故事：{len(stories)} 個\n')

# ═══════════════════════════════════════════════════════════
# 評分
# ═══════════════════════════════════════════════════════════

def score_story(s):
    text = s['text']
    trigger = s['trigger']
    sc = 0

    # 1. 觸發詞
    for kw, w in TRIGGER_WEIGHT.items():
        if kw in (trigger or ''):
            sc += w; break
    if sc == 0 and trigger:
        sc += 3  # 有觸發詞但不在名單
    if not trigger:
        # 掃文字本身找情緒詞
        for kw, w in TRIGGER_WEIGHT.items():
            if kw in text:
                sc += w // 2  # 強度減半
                break

    # 2. 基分
    sc += s['base']

    # 3. 反轉
    reversal = ['但是', '結果', '沒想到', '出乎意料',
                '誰知', '居然', '竟然', '他居然',
                '5秒', '30次', '50條', '30分鐘', '5分鐘',
                '白忙', '白費', '快被打敗']
    if any(rw in text for rw in reversal):
        sc += 5

    # 4. 具體數字/事實
    factual = ['60', '60美元', '60美金', '60塊', '30次', '50條',
               '100', 'commit', 'hash', 'Netlify',
               '1GB', '3分鐘', '30分鐘', '5秒']
    if any(f in text for f in factual):
        sc += 3

    # 5. 質問情緒（問號+情緒詞）
    q_words = ['為什麼', '怎麼', '到底', '是不是', '有沒有']
    if '？' in text or '?' in text:
        sc += 2
        if any(qw in text for qw in q_words):
            sc += 3

    # 6. 文字長度（太短不夠豐富）
    if len(text) < 40:
        sc -= 3
    elif len(text) > 150:
        sc += 2

    return sc

# ═══════════════════════════════════════════════════════════
# 去重（同內容取最高分）
# ═══════════════════════════════════════════════════════════

for s in stories:
    s['final_score'] = score_story(s)

# 按內容前60字去重
seen = {}
for s in stories:
    key = s['text'][:60]
    if key not in seen or s['final_score'] > seen[key]['final_score']:
        seen[key] = s

stories = list(seen.values())
stories.sort(key=lambda x: -x['final_score'])

print(f'去重後：{len(stories)} 個\n')

# ═══════════════════════════════════════════════════════════
# 產出 Top 30
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print('🏆 TOP 30 故事（三層判定法）')
print('═' * 70)

for i, s in enumerate(stories[:30], 1):
    text = s['text'][:180]
    t = s['trigger']
    marker = '🔴' if s['final_score'] >= 12 else '🟡' if s['final_score'] >= 7 else '  '
    print(f"\n{marker} #{i:02d} | 觸發：{t or '（情緒關鍵詞）'} | 分:{s['final_score']}")
    print(f"  故事：{text}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_FROM_448.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# Top 30 故事（從448個故事中評分出爐）\n')
    f.write('> 評分時間：2026-05-31 17:35\n')
    f.write('> 評分標準：觸發詞強度×反轉×具體數字×質問情緒\n')
    f.write(f'> 去重後故事池：{len(stories)} 個\n\n')
    f.write('🔴 = 最高強度（12分+）\n')
    f.write('🟡 = 中等強度（7-11分）\n')
    f.write('  = 普通（<7分）\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories[:30], 1):
        t = s['trigger']
        marker = '🔴' if s['final_score'] >= 12 else '🟡' if s['final_score'] >= 7 else ''
        f.write(f"\n## #{i:02d} {marker} {t or '（情緒關鍵詞）'}\n")
        f.write(f"評分：{s['final_score']}（基分{s['base']} + 綜合）\n")
        f.write(f"故事：{s['text'][:300]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"Top 30 分數區間：{stories[0]['final_score']} ~ {stories[29]['final_score']}")
print(f"故事池：{len(stories)} 個")