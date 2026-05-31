#!/usr/bin/env python3
"""嚴格評分：從448個故事中找Top 30"""

import re

data = open('/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_FINAL.md').read()

# ═══════════════════════════════════════════════════════════
# 評分權重
# ═══════════════════════════════════════════════════════════

TRIGGER_WEIGHT = {
    '你到底': 10, '你是不是': 8, '快被打敗': 10,
    '道歉有屁': 10, '浪費我的生命': 10, '生命都枯萎': 8,
    '你搞清楚': 6, '不見了': 5, '搞不清楚': 4,
    '為什麼會': 4, '怎麼搞': 4, '無釐頭': 5,
    '天呀': 3, '見鬼': 3, '白費': 3, '白忙': 3,
    '居然': 3, '重來': 2, '重新': 2,
}

# 守則 DNA（觸及最高指導原則）
RULES_DNA = {
    '#01': '在乎', '#02': '地圖', '#03': '思考',
    '#04': '解決問題', '#05': '痕跡', '#06': '交接',
    '#07': '失敗', '#08': '執行', '#09': '判斷力',
    '#10': '說人話', '#11': '自動自發', '#12': '拒絕搬運工',
    '#13': '客戶聲音', '#14': '提煉', '#15': '誠實',
    '#16': '複雜', '#17': '環境', '#18': '語音糾偏',
    '#19': '心跳', '#20': '啟動', '#21': '一字不差',
}

# 反轉關鍵字
REVERSAL = ['但是', '結果', '沒想到', '出乎意料', '反轉',
            '沒想到', '誰知', '居然', '竟然', '竟然']

# 具體數字/事實
FACTUAL = ['60', '60美元', '60美金', '30次', '50條', '100',
           '一分鐘', '三分鐘', '30分鐘', '60分鐘',
           'commit', 'hash', 'Netlify', 'JSONL']

# ═══════════════════════════════════════════════════════════
# 解析故事
# ═══════════════════════════════════════════════════════════

stories = []
lines = data.split('\n')

i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'#(\d+)\s*⭐?\s*🔶?\s*\|\s*觸發：(.+?)\s*\|\s*分:(\d+)', line)
    if m:
        num = m.group(1)
        trigger = m.group(2)
        base_score = int(m.group(3))
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

        stories.append({
            'num': num,
            'trigger': trigger,
            'base': base_score,
            'text': text,
        })
        i = j
    else:
        i += 1

print(f'解析 {len(stories)} 個故事\n')

# ═══════════════════════════════════════════════════════════
# 評分函數
# ═══════════════════════════════════════════════════════════

def score_story(s):
    trigger = s['trigger']
    text = s['text']
    s_score = s['base']

    # 1. 觸發詞強度（最重要）
    for kw, w in TRIGGER_WEIGHT.items():
        if kw in trigger:
            s_score += w
            break

    # 2. 有無守則 DNA
    for rid, name in RULES_DNA.items():
        if rid in text or name in text:
            s_score += 3
            break

    # 3. 有無峰迴路轉（反轉）
    if any(rw in text for rw in REVERSAL):
        s_score += 3

    # 4. 有無具體數字/事實
    if any(f in text for f in FACTUAL):
        s_score += 2

    # 5. 三幕劇潛力：有教練情緒 + 有AI行為
    if any(w in text for w in ['你到底', '為什麼', '我說', '教練']):
        s_score += 1
    if 'AI' in text or '小龍蝦' in text or '🤖' in text:
        s_score += 1

    # 6. 文字長度（太短不夠豐富）
    if len(text) < 40:
        s_score -= 3
    elif len(text) > 150:
        s_score += 2

    return s_score

# ═══════════════════════════════════════════════════════════
# 評分 + 排序
# ═══════════════════════════════════════════════════════════

for s in stories:
    s['final_score'] = score_story(s)

stories.sort(key=lambda x: -x['final_score'])

# ═══════════════════════════════════════════════════════════
# 產出 Top 30
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print('🏆 TOP 30 故事（三層判定法評分）')
print('═' * 70)

for i, s in enumerate(stories[:30], 1):
    text = s['text'][:200]
    print(f"\n{'─'*60}")
    print(f"#{i:02d} | ⭐ 觸發：{s['trigger']} | 基分:{s['base']} | 終分:{s['final_score']}")
    print(f"故事：{text}")

# ═══════════════════════════════════════════════════════════
# 寫入 Top 30 檔案
# ═══════════════════════════════════════════════════════════

out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_ALL_448.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# Top 30 故事清單（從448個故事中評分出爐）\n')
    f.write('> 評分時間：2026-05-31 17:30\n')
    f.write('> 評分標準：三層判定法（觸發詞×守則DNA×反轉×具體事實）\n')
    f.write('> 總故事池：448 個\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories[:30], 1):
        f.write(f"\n## #{i:02d} {s['trigger']}\n")
        f.write(f"評分：基分{s['base']} + 終分{s['final_score']}\n")
        f.write(f"故事：{s['text'][:300]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"\n🏆 Top 30 分數區間：{stories[0]['final_score']} ~ {stories[29]['final_score']}")
print(f"📊 全部故事分數區間：{stories[0]['final_score']} ~ {stories[-1]['final_score']}")