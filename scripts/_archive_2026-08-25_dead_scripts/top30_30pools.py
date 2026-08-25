#!/usr/bin/env python3
"""目標：湊滿30個，門檻20分+，去重但不放太狠"""

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

TRIGGERS = {
    '快被我打敗': 50, '快被打敗了': 50, '快被打敗': 50,
    '你到底': 45, '你到底有沒有': 45,
    '你們偷懶': 42, '偷懶': 38,
    '不負責任': 40,
    '浪費我的生命': 45,
    '道歉有屁': 45,
    '沒有人提醒': 38,
    '白忙': 38, '白忙一場': 40,
    '送出按鈕': 40, '送出按鈕沒有': 42,
    '60美金': 40, '60美元': 40, '60塊': 40, '60塊美金': 42,
    '居然': 35, '竟然': 35,
    '不見了': 34, '不見': 30,
    '怎麼搞': 34, '怎麼搞的': 34,
    '你搞清楚': 32, '搞不清楚': 30, '搞不清': 30,
    '為什麼會': 30,
    '你又': 28, '我又': 28,
    '我又當': 30,
    '白費': 28,
    '你們每次': 30,
    '失敗': 26,
    '錯了': 24, '搞砸': 26,
    '你確定': 22,
    '你應該': 20,
    '每次都': 22,
    '一直': 22,
    '不行': 24,
    '為什麼': 20,
    '你們又': 28,
    '我又當': 30,
}

def score(text):
    sc = 0
    for kw, w in TRIGGERS.items():
        if kw in text:
            sc = max(sc, w)
    if sc == 0: return 0
    for r in ['但是', '結果', '沒想到', '居然', '竟然', '5秒', '30分鐘',
               'commit根本', '鐵板']:
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
    if sc < 18: continue  # 降到18

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

    key = clean(full)[:80]
    stories.append({'trigger': trigger, 'score': sc, 'sid': sid,
                   'text': full, 'key': key})

# ═══════════════════════════════════════════════════════════
# 寬鬆去重：同一段文字（前80字）只留一次
# 但不同情節只要分數接近都保留
# ═══════════════════════════════════════════════════════════

seen_keys = {}
for s in stories:
    k = s['key']
    if k not in seen_keys or s['score'] > seen_keys[k]['score']:
        seen_keys[k] = s

stories = list(seen_keys.values())
stories.sort(key=lambda x: -x['score'])

# 找事件核心關鍵詞
def event_key(s):
    t = s['trigger']
    text = s['text']
    # 細分不同情節
    if '送出按鈕' in text and '勾選' in text: return '送出按鈕_勾選'
    if '送出按鈕' in text and '頁面' in text: return '送出按鈕_頁面'
    if '送出按鈕' in text: return '送出按鈕_其他'
    if '60' in text and ('扣' in text or 'Kimi' in text): return '60美金扣款'
    if '60' in text and ('Netlify' in text or '託管' in text): return '60美金圖片'
    if '接力棒' in text or ('開工兩個字' in text): return '接力棒失憶'
    if '你到底' in text and ('思考' in text or '法則' in text): return '你到底思考'
    if '你到底' in text and ('歷史存檔' in text or '清除' in text): return '你到底認真讀'
    if '你到底' in text and ('模型' in text or '對話框' in text): return '你到底新對話框'
    if '不見了' in text and ('流程' in text or '精彩' in text): return '流程不見'
    if '不見了' in text and ('照片' in text or '圖片' in text): return '圖片不見'
    if '不見了' in text and ('資料' in text or '內容' in text): return '資料不見'
    if '守則' in text and ('讀' in text or '法則' in text): return '守則沒讀'
    if '守則' in text and '後悔' in text: return '守則後悔'
    if '守則' in text and '後悔' not in text and '法則' in text: return '守則法則'
    if 'API' in text and ('Missing' in text or 'key' in text): return 'API失效'
    if 'commit' in text and ('失敗' in text or '沒有成功' in text): return 'commit失敗'
    if '一直' in text and ('Kimi' in text or '模型' in text): return '一直Kimi模式'
    if '一直' in text and ('Goal' in text or '執行' in text): return '一直執行'
    if '一直' in text and ('截圖' in text or 'Token' in text): return '一直截圖'
    if '一直' in text: return '一直其他'
    if '你們' in text and '每次' in text: return '你們每次'
    if '你們' in text: return '你們其他'
    if t: return t
    return '其他'

# 按事件分組，每個事件留最多3個
by_event = defaultdict(list)
for s in stories:
    by_event[event_key(s)].append(s)

unique = []
for event, group in by_event.items():
    group.sort(key=lambda x: -x['score'])
    # 每個事件最多3個
    for s in group[:3]:
        unique.append(s)

unique.sort(key=lambda x: -x['score'])
unique = unique[:40]  # 最多40個

count_20 = len([s for s in unique if s['score'] >= 20])
print(f'去重後：{len(unique)} 個故事 | 20分+：{count_20} 個')

# ═══════════════════════════════════════════════════════════
# 顯示
# ═══════════════════════════════════════════════════════════

print('\n' + '='*70)
print(f'🏆 TOP {min(30, len(unique))} 故事')
print('='*70)

for i, s in enumerate(unique, 1):
    if i > 35: break
    tag = '✅' if s['score'] >= 30 else '🟡' if s['score'] >= 20 else '⚠️'
    text = clean(s['text'])[:150]
    print(f"\n{tag} #{i:02d} | {s['trigger']} | 分:{s['score']} | S:{s['sid']}…")
    print(f"  {text}")

# 寫檔
out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_20PTS.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# 🏆 Top 30 故事（20分+版）\n')
    f.write(f'> 評分時間：2026-05-31 18:05\n')
    f.write(f'> 門檻：20分+ | 找到：{len(unique)} 個 | 20分+：{count_20} 個\n\n')
    f.write('✅ = 30分+（金牌）\n')
    f.write('🟡 = 20-29分（銀牌）\n')
    f.write('⚠️ = 18-19分（銅牌）\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(unique[:30], 1):
        tag = '✅' if s['score'] >= 30 else '🟡' if s['score'] >= 20 else '⚠️'
        text = clean(s['text'])[:400]
        f.write(f"\n## #{i:02d} {tag} {s['trigger']}\n")
        f.write(f"分數：{s['score']} | Session：{s['sid']}\n")
        f.write(f"故事：{text}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"20分+：{count_20} 個 | 目標30個：{'✅ 達標！' if count_20 >= 30 else f'還差 {30-count_20} 個'}")