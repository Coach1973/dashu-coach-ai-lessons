#!/usr/bin/env python3
"""嚴格評分：從448個故事中找Top 30（修復版：只留真正教練情緒故事）"""

import re

data = open('/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_FINAL.md').read()

# ═══════════════════════════════════════════════════════════
# 評分權重
# ═══════════════════════════════════════════════════════════

TRIGGER_WEIGHT = {
    '你到底': 12, '你是不是': 8, '快被打敗': 12,
    '道歉有屁': 12, '道歉有個屁': 12, '浪費我的生命': 12,
    '生命都枯萎': 10, '你搞清楚': 6, '不見了': 6,
    '搞不清楚': 5, '為什麼會': 5, '怎麼搞': 6,
    '無釐頭': 6, '天呀': 4, '見鬼': 4,
    '白費': 4, '白忙': 4, '居然': 4,
    '重來': 3, '重新': 3, '又忘': 4,
    '老是忘': 5, 'commit': 3, 'hash': 3,
}

# 要排除的系統訊息模式
SYSTEM_EXCLUDE = [
    'cron:', 'System:', 'Exec completed', '提醒您',
    '倒數計時', 'NotebookLM', '壽星',
    '每.*小時', '每30分鐘', '每15分鐘', '可能在偷懶',
    '請記得繳納', '執董週會', '小人提',
    r'\[media attached', '頂級特助分工群',
    'EchoTokens', 'SYNTROL', 'Netlify 每個月',
    '小籠蝦', 'c工作', 'c工作的',
]

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
        trigger = m.group(2).strip()
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

        # 跳過：無觸發詞、系統訊息、太短
        if not trigger:
            i = j; continue
        if any(re.search(p, text) for p in SYSTEM_EXCLUDE):
            i = j; continue
        if len(text) < 30:
            i = j; continue
        # 跳過：全是引號包圍的普通對話（沒有情緒）
        if trigger not in str(TRIGGER_WEIGHT.keys()):
            i = j; continue

        stories.append({
            'num': num,
            'trigger': trigger,
            'base': base_score,
            'text': text,
        })
        i = j
    else:
        i += 1

print(f'過濾後有效故事：{len(stories)} 個\n')

# ═══════════════════════════════════════════════════════════
# 評分函數
# ═══════════════════════════════════════════════════════════

def score_story(s):
    trigger = s['trigger']
    text = s['text']
    s_score = 0

    # 1. 觸發詞強度（最重要）
    for kw, w in TRIGGER_WEIGHT.items():
        if kw in trigger:
            s_score += w
            break
    if s_score == 0:
        s_score += 2  # 默認

    # 2. 基分
    s_score += s['base']

    # 3. 有無峰迴路轉（反轉）
    reversal_words = ['但是', '結果', '沒想到', '出乎意料',
                      '誰知', '居然', '竟然', '竟然',
                      '他居然', '我居然', '5秒', '30次', '50條']
    if any(rw in text for rw in reversal_words):
        s_score += 4

    # 4. 有無具體數字/事實
    factual_words = ['60', '60美元', '60美金', '30次', '50條',
                     '100', 'commit', 'hash', 'Netlify',
                     '1GB', '三分鐘', '30分鐘', '5秒']
    if any(f in text for f in factual_words):
        s_score += 3

    # 5. 文字長度
    if len(text) > 150:
        s_score += 2
    elif len(text) < 50:
        s_score -= 2

    # 6. 有問號（質問情緒）
    if '？' in text or '?' in text:
        s_score += 2

    return s_score

# ═══════════════════════════════════════════════════════════
# 評分 + 排序
# ═══════════════════════════════════════════════════════════

for s in stories:
    s['final_score'] = score_story(s)

stories.sort(key=lambda x: -x['final_score'])

# ═══════════════════════════════════════════════════════════
# 產出 Top 30（顯示前40個供挑選）
# ═══════════════════════════════════════════════════════════

print('═' * 70)
print('🏆 TOP 40 故事候選（評分出爐，供教練挑選 Top 30）')
print('═' * 70)

for i, s in enumerate(stories[:40], 1):
    text = s['text'][:150]
    # 判斷強度
    marker = '🔴' if s['final_score'] >= 10 else '🟡' if s['final_score'] >= 6 else '  '
    print(f"\n{marker} #{i:02d} | 觸發：{s['trigger']} | 分:{s['final_score']}")
    print(f"  故事：{text}")

# ═══════════════════════════════════════════════════════════
# 寫入 Top 30 檔案
# ═══════════════════════════════════════════════════════════

out = '/Users/bymyway/.claude-code/workspace/distill/_TOP30_FROM_448.md'
with open(out, 'w', encoding='utf-8') as f:
    f.write('# Top 30 故事（從448個故事中評分出爐）\n')
    f.write('> 評分時間：2026-05-31 17:32\n')
    f.write('> 評分標準：觸發詞強度×反轉×具體數字×質問情緒\n')
    f.write(f'> 有效故事池：{len(stories)} 個 | 候選前40：已產出\n\n')
    f.write('🔴 = 最高強度（10分+）\n')
    f.write('🟡 = 中等強度（6-9分）\n\n')
    f.write('═' * 70 + '\n')
    for i, s in enumerate(stories[:30], 1):
        marker = '🔴' if s['final_score'] >= 10 else '🟡'
        f.write(f"\n## #{i:02d} {marker} {s['trigger']}\n")
        f.write(f"評分：{s['final_score']}（基分{s['base']} + 綜合）\n")
        f.write(f"故事：{s['text'][:300]}\n\n")

print(f"\n✅ 已寫入 {out}")
print(f"\n共 {len(stories)} 個有效故事")
print(f"Top 30 分數門檻：{stories[29]['final_score']} 分以上")