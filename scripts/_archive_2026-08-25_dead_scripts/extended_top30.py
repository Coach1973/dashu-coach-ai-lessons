#!/usr/bin/env python3
"""擴充挖掘：找更多30分+故事，目標湊滿30個"""

import re, os
from glob import glob

# ═══════════════════════════════════════════════════════════
# 讀取所有文字（擴大來源）
# ═══════════════════════════════════════════════════════════

sources = [
    *sorted(glob('/Users/bymyway/.claude-code/workspace/distill/*.md')),
    *sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md')),
    *sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md')),
    # 加入更多可能的來源
]

all_text = ''
for f in sources:
    if os.path.exists(f):
        all_text += open(f).read() + '\n\n'

print(f'掃描 {len(sources)} 個檔案，總文字量：{len(all_text):,} 字\n')

# ═══════════════════════════════════════════════════════════
# 擴充觸發詞表（覆蓋更多類型）
# ═══════════════════════════════════════════════════════════

# 金牌觸發（40分起）
GOLD = {
    '你到底': 40, '你到底在搞什麼': 40, '你到底有沒有': 40,
    '快被我打敗': 40, '快被打敗了': 40, '快被打敗': 40,
    '道歉有屁': 40, '道歉有個屁': 40,
    '浪費我的生命': 40,
    '生命都枯萎': 36,
    '你搞清楚我是誰': 36, '你搞清楚你是誰': 36,
    '不負責任': 36,
    '偷懶': 36, '你們偷懶': 40,
}

# 高分觸發（30分起）
HIGH = {
    '沒有人提醒': 35,
    'commit根本沒有成功': 35, 'commit根本沒成功': 35,
    '白忙': 34, '送出按鈕沒有': 34,
    '60美元': 34, '60美金': 34, '60塊美金': 34, '60塊': 34,
    '居然': 32, '竟然': 32,
    '怎麼搞': 32, '怎麼搞的': 32,
    '不見了': 30, '圖片都不見': 30, '照片不見': 30,
    '天呀': 30, '天哪': 30,
    '見鬼': 30, '見鬼了': 30, '見鬼了又': 30,
    '搞不清楚': 30, '搞不清': 30, '精神錯亂': 30,
    '你又': 28, '你們又': 28,
    '我又': 28, '我又當': 28,
    '白費': 28, '白忙一場': 28,
    '不行': 26, '不行了': 26,
    '為什麼會': 26,
    '我真的': 26, '我真的很': 26,
    '怎麼會': 26, '怎麼可能': 26,
    '搞砸': 26,
    '重來': 24,
    '又忘': 24, '老是忘': 24, '忘了': 22,
    '一直': 22, '怎麼又': 22,
}

# 擴充觸發（15-25分）
MED = {
    '不對': 20, '不對了': 22,
    '為什麼': 20,
    '難道': 22,
    '你確定': 20,
    '你應該': 18,
    '你不': 18,
    '你沒有': 18,
    '沒有人': 20,
    '每次都': 20,
    '我一直': 22,
    '你們每次': 24,
    '不行': 22,
    '失敗': 22,
    '錯了': 20,
    '不準': 20,
    '假的': 22,
}

# ═══════════════════════════════════════════════════════════
# 段落掃描（兩種模式）
# ═══════════════════════════════════════════════════════════

def get_trigger_score(text):
    """找最高分觸發詞"""
    max_sc = 0
    trigger = ''
    for kw, sc in {**GOLD, **HIGH, **MED}.items():
        if kw in text and sc > max_sc:
            max_sc = sc
            trigger = kw
    return trigger, max_sc

def score_passage(text, trigger, trigger_score):
    """給段落評分"""
    sc = trigger_score
    if sc == 0:
        return 0

    # 反轉加成
    reversal = ['但是', '結果', '沒想到', '居然', '竟然',
                '5秒', '30次', '50條', '30分鐘', '60',
                '白忙', '白費', '快被打敗', 'commit根本', '鐵板',
                '他又', '他又說', '我又', '我又說']
    for r in reversal:
        if r in text:
            sc += 4
            break

    # 具體數字加成
    factual = ['60', '30', '50', '100', 'commit', 'hash',
               '1GB', '3分鐘', '30分鐘', '5秒', '三四', '三四次',
               '200', '300', '500', '1.2B', '227']
    for f in factual:
        if f in text:
            sc += 3
            break

    # 質問情緒（問號+情緒）
    if '？' in text or '?' in text:
        sc += 2

    # 守則提及（暗示有原則層次）
    rules_kw = ['守則', '法則', '原則', '信念', '使命', '願景', '理念']
    for r in rules_kw:
        if r in text:
            sc += 2
            break

    # 文字長度（太短不夠豐富）
    if len(text) < 50:
        sc -= 8
    elif len(text) > 200:
        sc += 2

    return sc

# ═══════════════════════════════════════════════════════════
# 掃描策略一：以空行分段
# ═══════════════════════════════════════════════════════════

print('策略一：空行分段掃描...')
blocks = re.split(r'\n\n+', all_text)
stories = []

for block in blocks:
    block = block.strip()
    if len(block) < 80:
        continue

    # 找教練說的話
    coach_parts = []
    for line in block.split('\n'):
        # 👤 教練：
        m = re.match(r'👤\s*教練[：:]?\s*(.+)', line)
        if m:
            t = m.group(1).strip()
            if len(t) > 10:
                coach_parts.append(t)
        # 教練：
        m = re.match(r'教練[：:]\s*(.{10,})', line)
        if m:
            t = m.group(1).strip()
            if len(t) > 15 and '教練' not in t[:15]:
                coach_parts.append(t)
        # coach: 或 coach：
        m = re.match(r'coach[：:]\s*(.{10,})', line, re.I)
        if m:
            t = m.group(1).strip()
            if len(t) > 15:
                coach_parts.append(t)
        # 大樹教練：
        m = re.match(r'大樹教練[：:]\s*(.{10,})', line)
        if m:
            t = m.group(1).strip()
            if len(t) > 15:
                coach_parts.append(t)

    if not coach_parts:
        continue

    full = ' '.join(coach_parts)

    # 找觸發詞
    trigger, trigger_score = get_trigger_score(full)
    if trigger_score == 0:
        continue

    # 評分
    sc = score_passage(full, trigger, trigger_score)
    if sc < 25:
        continue

    # 排除
    if any(k in full for k in ['cron:', 'System:', '提醒您', '🦞 教練您好',
                                 '倒數計時', 'NotebookLM', '壽星', '執董週會',
                                 r'\[media attached', 'Exec completed',
                                 'FB.*壽星', '每四小時']):
        continue

    # 去重（前100字）
    key = full[:100]
    sid = ''
    date_match = re.search(r'2026-(?:0[4-5]|0[5-9]|10|11|12)-[0-3][0-9]', block)
    sid_match = re.findall(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
    date = date_match.group() if date_match else 'unknown'
    sid = sid_match[0][:8] if sid_match else 'unknown'

    stories.append({'trigger': trigger, 'score': sc, 'date': date, 'sid': sid,
                   'text': full, 'key': key})

print(f'策略一找到：{len(stories)} 個')

# ═══════════════════════════════════════════════════════════
# 策略二：單行掃描（找長段落的教練句子）
# ═══════════════════════════════════════════════════════════

print('策略二：單行關鍵句掃描...')

for line in all_text.split('\n'):
    line = line.strip()
    if len(line) < 30:
        continue

    # 只看有教練標記的
    if not re.search(r'👤|教練[：:]|coach[：:]|大樹教練', line):
        continue

    # 去掉標記
    clean = re.sub(r'^(👤|教練[：:]|coach[：:]|大樹教練[：:])\s*', '', line)
    clean = re.sub(r'^\*\*', '', clean)
    clean = clean.strip()
    if len(clean) < 20:
        continue

    trigger, trigger_score = get_trigger_score(clean)
    if trigger_score < 30:
        continue

    # 排除
    if any(k in clean for k in ['cron:', 'System:', '提醒您', '🦞 教練您好',
                                  '倒數計時', 'NotebookLM', '壽星',
                                  r'\[media attached', 'Exec completed']):
        continue

    sc = score_passage(clean, trigger, trigger_score)
    if sc < 25:
        continue

    key = clean[:100]
    # 如果已經存在且分數更高，跳過
    if key in [s['key'] for s in stories]:
        continue

    stories.append({'trigger': trigger, 'score': sc, 'date': 'unknown',
                   'sid': 'unknown', 'text': clean, 'key': key})

print(f'策略二完成，總故事：{len(stories)} 個')

# ═══════════════════════════════════════════════════════════
# 策略三：直接搜「」引號內的高分段落
# ═══════════════════════════════════════════════════════════

print('策略三：「」引號掃描...')
for m in re.finditer(r'[「"]([^」"]{30,300})[」"]', all_text):
    quote = m.group(1)
    if any(k in quote for k in ['cron:', 'System:', '提醒您', 'Exec completed',
                                  r'\[media attached', '🦞 小龍蝦', '🦞 軍師']):
        continue
    trigger, trigger_score = get_trigger_score(quote)
    if trigger_score < 30:
        continue
    sc = score_passage(quote, trigger, trigger_score)
    if sc < 25:
        continue
    key = quote[:100]
    if key in [s['key'] for s in stories]:
        continue
    stories.append({'trigger': trigger, 'score': sc, 'date': 'unknown',
                   'sid': 'unknown', 'text': quote, 'key': key})

print(f'策略三完成，總故事：{len(stories)} 個')

# ═══════════════════════════════════════════════════════════
# 去重+排序
# ═══════════════════════════════════════════════════════════

seen = {}
for s in stories:
    k = s['key']
    if k not in seen or s['score'] > seen[k]['score']:
        seen[k] = s

stories = list(seen.values())
stories.sort(key=lambda x: -x['score'])

print(f'\n去重後：{len(stories)} 個故事')
count_30 = len([s for s in stories if s['score'] >= 30])
print(f'30分+：{count_30} 個')

# ═══════════════════════════════════════════════════════════
# 顯示 Top 50
# ═══════════════════════════════════════════════════════════

print('\n' + '='*70)
print(f'🏆 TOP 50 候選（擴充挖掘）')
print(f'30分+：{count_30} 個 | 目標：湊滿 30 個')
print('='*70)

for i, s in enumerate(stories[:50], 1):
    tag = '✅' if s['score'] >= 30 else '⚠️'
    print(f"\n{tag} #{i:02d} | {s['trigger']} | 分:{s['score']} | {s['date']} | S:{s['sid']}…")
    print(f"  {s['text'][:160]}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_EXTENDED.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# 🏆 Top 30 故事（擴充挖掘版）\n')
    f.write(f'> 評分時間：2026-05-31 17:50\n')
    f.write(f'> 三策略：空行分段 + 單行掃描 + 引號挖掘\n')
    f.write(f'> 找到：{len(stories)} 個故事 | 30分+：{count_30} 個\n\n')
    f.write('✅ = 30分+（最高強度）\n')
    f.write('⚠️ = 25-29分（強）\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories[:30], 1):
        tag = '✅' if s['score'] >= 30 else '⚠️'
        f.write(f"\n## #{i:02d} {tag} {s['trigger']}\n")
        f.write(f"分數：{s['score']} | {s['date']} | S:{s['sid']}\n")
        f.write(f"故事：{s['text'][:400]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"30分+：{count_30} 個 | 還差：{max(0, 30-count_30)} 個")