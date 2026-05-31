#!/usr/bin/env python3
"""過濾系統訊息，只留教練真正的對話故事"""

import re

# 讀取終極挖掘檔
data = open('/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_ULTIMATE.md').read()

# ═══════════════════════════════════════════════════════════
# 系統訊息關鍵字（要排除）
# ═══════════════════════════════════════════════════════════

SYSTEM_PATTERNS = [
    r'^\[cron:', r'^\[System', r'^System:', r'^Exec completed',
    r'提醒您.*信用卡', r'提醒您.*報名', r'^🦞.*關懷時間',
    r'每.*分鐘.*提醒', r'每.*小時.*提醒', r'^哈囉.*教練.*🎓',
    r'請記得繳納', r'倒數計時', r'NotebookLM.*搬家',
    r'FB.*壽星', r'早安教練.*🦞', r'晚安教練',
    r'每四小時.*主動', r'每30分鐘.*任務', r'^✅ 執行完畢',
    r'^⚠️.*可能在偷懶', r'^早安教練.*🌅',
    r'目標心跳驅動', r'小人提.*補助', r'執董週會',
]

def is_system(text):
    for p in SYSTEM_PATTERNS:
        if re.search(p, text):
            return True
    return False

# ═══════════════════════════════════════════════════════════
# 解析故事
# ═══════════════════════════════════════════════════════════

stories = []
lines = data.split('\n')

i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'#(\d+)\s+\|\s*觸發：(.+?)\s*\|\s*分:(\d+)', line)
    if m:
        num = m.group(1)
        trigger = m.group(2)
        score = int(m.group(3))
        # 讀內容行
        content_lines = []
        j = i + 1
        while j < len(lines) and lines[j]:
            if re.match(r'^#\d', lines[j]):
                break
            content_lines.append(lines[j])
            j += 1
        full = '\n'.join(content_lines).strip()
        # 去掉「內容：」前綴
        full = re.sub(r'^內容：', '', full)
        # 清理行號殘留
        full = re.sub(r'^\d+\s+', '', full)
        full = re.sub(r'\s*\d+\s+(「)', r' \1', full)

        # 過濾系統訊息
        if not is_system(full) and len(full) > 20:
            stories.append({
                'num': num,
                'trigger': trigger,
                'score': score,
                'text': full,
            })
        i = j
    else:
        i += 1

print(f'過濾後真實教練故事：{len(stories)} 個')

# ═══════════════════════════════════════════════════════════
# 按情緒強度分級
# ═══════════════════════════════════════════════════════════

HIGH = ['你到底', '你是不是', '我真的', '快被打敗', '道歉有屁', '浪費我的生命',
        '你搞清楚', '不見了', '搞不清楚', '為什麼會', '怎麼搞', '無釐頭', '天呀', '見鬼']

def tier(s):
    t = s['trigger']
    for h in HIGH:
        if h in t:
            return 0  # 最強
    return 1  # 普通

stories.sort(key=lambda x: (tier(x), -x['score']))

# ═══════════════════════════════════════════════════════════
# 產出乾淨清單（至少100個高品質故事）
# ═══════════════════════════════════════════════════════════

print(f'最終清單：{len(stories)} 個故事\n')

# 寫入 distill/_STORY_LIST_FINAL.md
out_path = '/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_FINAL.md'

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(f"# 故事清單（最終版）\n")
    f.write(f"> 挖掘時間：2026-05-31 17:25\n")
    f.write(f"> 總故事數：{len(stories)} 個（已過濾系統訊息）\n")
    f.write(f"> 評分：觸發詞強度 + 情緒分數\n")
    f.write(f"> 等級：⭐ = 最高強度 🔶 = 中等強度\n\n")

    f.write('═' * 70 + '\n')
    f.write('【⭐ 最高強度故事】（教練情緒反應最強）\n')
    f.write('═' * 70 + '\n')

    tier_count = 0
    for i, s in enumerate(stories, 1):
        if tier(s) == 0:
            tier_count += 1
            marker = '⭐'
            f.write(f"\n{'─'*60}\n")
            f.write(f"#{i:03d}{marker} | 觸發：{s['trigger']} | 分:{s['score']}\n")
            f.write(f"故事：{s['text'][:300]}\n")

    f.write('\n' + '═' * 70 + '\n')
    f.write('【🔶 中等強度故事】（仍有價值但情緒強度中等）\n')
    f.write('═' * 70 + '\n')

    for i, s in enumerate(stories, 1):
        if tier(s) == 1:
            f.write(f"\n#{i:03d}🔶 | 觸發：{s['trigger']} | 分:{s['score']}\n")
            f.write(f"故事：{s['text'][:200]}\n")

print(f"✅ 已寫入 {out_path}")
print(f"⭐ 最高強度：{tier_count} 個")
print(f"🔶 中等強度：{len(stories) - tier_count} 個")
print(f"合計：{len(stories)} 個故事")

# 同時產出簡短清單供教練快速瀏覽
short = '/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_TOP100.md'
with open(short, 'w', encoding='utf-8') as f:
    f.write(f"# Top 100 故事精選清單\n")
    f.write(f"> 篩選時間：2026-05-31 17:25\n")
    f.write(f"> 從 {len(stories)} 個故事中精選前 100 個\n\n")
    f.write('─' * 70 + '\n')
    for i, s in enumerate(stories[:100], 1):
        marker = '⭐' if tier(s) == 0 else ''
        f.write(f"#{i:03d}{marker} {s['trigger']} | {s['text'][:80]}…\n")

print(f"✅ 精簡版已寫入 {short}")