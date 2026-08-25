#!/usr/bin/env python3
"""嚴格去重：找30個真正不同的故事，分數全部30+"""

import re, os
from glob import glob

# ═══════════════════════════════════════════════════════════
# 讀取
# ═══════════════════════════════════════════════════════════

sources = [
    *sorted(glob('/Users/bymyway/.claude-code/workspace/distill/*.md')),
    *sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md')),
    *sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md')),
]
all_text = '\n\n'.join(open(f).read() for f in sources if os.path.exists(f))
print(f'文字量：{len(all_text):,} 字\n')

# ═══════════════════════════════════════════════════════════
# 評分（嚴格）
# ═══════════════════════════════════════════════════════════

TRIGGERS = {
    '快被打敗了': 45, '快被打敗': 45,
    '你到底': 40, '你到底有沒有': 40,
    '你們偷懶': 40, '偷懶': 35,
    '不負責任': 38,
    '浪費我的生命': 40,
    '道歉有屁': 40,
    '沒有人提醒': 35,
    '白忙': 35, '白忙一場': 38,
    '送出按鈕': 38, '送出按鈕沒有': 40,
    '60美金': 38, '60美元': 38, '60塊': 38,
    '居然': 32, '竟然': 32,
    '不見了': 32, '不見': 30, '不見了': 30,
    '怎麼搞': 32, '怎麼搞的': 32,
    '你搞清楚': 30,
    '搞不清楚': 30,
    '為什麼會': 28,
    '你又': 26, '我又': 26,
    '我又當': 28,
    '白費': 28,
    '你們每次': 28,
    '失敗': 26,
    '錯了': 24,
}

def score(text):
    sc = 0
    for kw, w in TRIGGERS.items():
        if kw in text:
            sc = max(sc, w)
    if sc == 0: return 0

    # 反轉
    for r in ['但是', '結果', '沒想到', '居然', '竟然', '5秒', '30分鐘',
               'commit根本', '鐵板', '我又', '我又說']:
        if r in text: sc += 5; break

    # 數字
    for f in ['60', '30', '50', '100', '三四', '1GB', '5秒']:
        if f in text: sc += 3; break

    # 問號情緒
    if '？' in text or '?' in text: sc += 2

    # 長度
    if len(text) < 50: sc -= 10
    elif len(text) > 200: sc += 2

    return sc

# ═══════════════════════════════════════════════════════════
# 嚴格去重：同一 session 只留一個最高分
# ═══════════════════════════════════════════════════════════

def extract_key(text):
    """用觸發詞+第一個完整句的核心內容當key"""
    text = re.sub(r'^\d+\s+', '', text)
    text = re.sub(r'\[media attached.*?\]', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'data:image.*?base64,', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(r'### .*', '', text)
    return text[:80].strip()

# ═══════════════════════════════════════════════════════════
# 掃描段落
# ═══════════════════════════════════════════════════════════

stories = []
blocks = re.split(r'\n\n+', all_text)

for block in blocks:
    block = block.strip()
    if len(block) < 80:
        continue

    # 找教練段落
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

    if not coach_parts:
        continue

    full = ' '.join(coach_parts)

    # 評分
    sc = score(full)
    if sc < 30:
        continue

    # 排除
    if any(k in full for k in ['cron:', 'System:', '提醒您', '🦞 教練您好',
                                 '倒數計時', 'NotebookLM', '壽星', '執董週會',
                                 r'\[media attached', 'Exec completed',
                                 'FB.*壽星', '每四小時', 'GitHub Actions',
                                 'data:image', 'base64,']):
        continue

    # 找session
    sids = re.findall(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
    sid = sids[0][:8] if sids else 'unknown'

    # 觸發詞
    trigger = ''
    for kw in TRIGGERS:
        if kw in full:
            trigger = kw; break

    # 嚴格去重：用觸發詞+關鍵情節
    key = trigger + extract_key(full)

    stories.append({
        'trigger': trigger,
        'score': sc,
        'sid': sid,
        'text': full,
        'key': key,
    })

# ═══════════════════════════════════════════════════════════
# 嚴格去重邏輯：
# 1. 同一觸發詞只留最高分
# 2. 同類情節（送出按鈕/60美金/接力棒）只留一個
# ═══════════════════════════════════════════════════════════

# 按觸發詞分組
from collections import defaultdict
by_trigger = defaultdict(list)
for s in stories:
    by_trigger[s['trigger']].append(s)

# 每個觸發詞只留最佳
unique = []
seen_plots = set()
for trigger, group in by_trigger.items():
    best = max(group, key=lambda x: x['score'])
    # 特殊：同類情節再做一次去重
    plot = trigger
    if '送出按鈕' in best['text'] or '白忙' in best['text']: plot = '送出按鈕'
    elif '60' in best['text'] and ('扣' in best['text'] or '美金' in best['text']): plot = '60美金'
    elif '新視窗' in best['text'] or '接力棒' in best['text']: plot = '接力棒失憶'
    elif 'commit' in best['text'] and '失敗' in best['text']: plot = 'commit失敗'
    elif '不見' in best['text'] and '流程' in best['text']: plot = '流程不見'
    elif '你到底' in best['text'] and '思考' in best['text']: plot = '你到底思考'
    elif '你到底' in best['text'] and '認真' in best['text']: plot = '你到底認真'
    elif '守則' in best['text'] and ('讀' in best['text'] or '法則' in best['text']): plot = '守則沒讀'

    if plot not in seen_plots:
        seen_plots.add(plot)
        unique.append(best)
    else:
        # 如果情節重複，保留分數更高的
        for existing in unique:
            if existing['key'][:40] == best['key'][:40] and best['score'] > existing['score']:
                unique.remove(existing)
                seen_plots.add(plot + '_alt')
                unique.append(best)
                break

unique.sort(key=lambda x: -x['score'])

print(f'嚴格去重後：{len(unique)} 個故事\n')
count_30 = len([s for s in unique if s['score'] >= 30])
print(f'30分+：{count_30} 個')

# ═══════════════════════════════════════════════════════════
# 顯示 Top 40
# ═══════════════════════════════════════════════════════════

print('\n' + '='*70)
print(f'🏆 TOP 40 真正獨立故事（30分+）')
print('='*70)

for i, s in enumerate(unique[:40], 1):
    tag = '✅' if s['score'] >= 30 else '⚠️'
    text = s['text'][:160]
    # 清理行號
    text = re.sub(r'^\d+\s+', '', text)
    text = re.sub(r'\d+\s+(「)', r'\1', text)
    print(f"\n{tag} #{i:02d} | {s['trigger']} | 分:{s['score']} | S:{s['sid']}…")
    print(f"  {text}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_STRICT_FINAL.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# 🏆 Top 30 故事（嚴格版·全部30分+）\n')
    f.write(f'> 評分時間：2026-05-31 17:55\n')
    f.write(f'> 嚴格去重：同一觸發詞→1個，同類情節→1個\n')
    f.write(f'> 找到：{len(unique)} 個獨立故事 | 30分+：{count_30} 個\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(unique[:30], 1):
        tag = '✅' if s['score'] >= 30 else '⚠️'
        text = s['text'][:400]
        text = re.sub(r'^\d+\s+', '', text)
        text = re.sub(r'\d+\s+(「)', r'\1', text)
        f.write(f"\n## #{i:02d} {tag} {s['trigger']}\n")
        f.write(f"分數：{s['score']} | Session：{s['sid']}\n")
        f.write(f"故事：{text}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"30分+：{count_30} 個 | 還差：{max(0, 30-count_30)} 個")