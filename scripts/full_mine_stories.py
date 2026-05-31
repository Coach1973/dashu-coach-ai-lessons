#!/usr/bin/env python3
"""全面挖掘所有故事原料——超越100筆"""

import re, os
from glob import glob
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# 第一階段：讀取所有來源檔
# ═══════════════════════════════════════════════════════════

print("【第一階段】讀取所有故事來源...")

sources = {}

# 1. distill/ 目錄下的所有 .md 檔
distill_files = sorted(glob('/Users/bymyway/.claude-code/workspace/distill/*.md'))

# 2. daily 記錄
daily_files = sorted(glob('/Users/bymyway/.claude-code/workspace/daily_2026-*.md'))

# 3. memory/ 記憶
mem_files = sorted(glob('/Users/bymyway/.claude-code/workspace/memory/*.md'))

print(f"  distill/: {len(distill_files)} 個檔案")
print(f"  daily/:  {len(daily_files)} 個檔案")
print(f"  memory/: {len(mem_files)} 個檔案")

all_text = ""
for f in distill_files + daily_files + mem_files:
    try:
        all_text += f"=== {os.path.basename(f)} ===\n" + open(f).read() + "\n\n"
    except:
        pass

print(f"  總文字量: {len(all_text):,} 字\n")

# ═══════════════════════════════════════════════════════════
# 第二階段：定義故事類型與觸發詞
# ═══════════════════════════════════════════════════════════

# 高強度觸發詞（最強）
HIGH_TRIGGERS = [
    '你到底', '你是不是', '你又', '我真的', '快被打敗',
    '道歉有屁', '浪費我的生命', '生命都枯萎',
    '你搞清楚了嗎', '你搞清楚', '你搞清楚我是誰',
]

# 中強度觸發詞
MED_TRIGGERS = [
    '白費', '白忙', '不見了', '不見', '居然',
    '為什麼會', '怎麼搞', '搞不清楚', '搞砸',
    '無釐頭', '天呀', '見鬼了', '三分鐘',
    '六十分鐘', '60美元', '六十美元',
    '重來', '重新', '又忘', '老是忘',
    'commit在哪', 'hash在哪',
]

# 核心守則標記
RULES_MAP = {
    '在乎': '#01', '錯誤的地圖': '#02', '思考問問題': '#03',
    '解決問題': '#04', '凡走過必留痕跡': '#05', '完美交接': '#06',
    '失敗為成功之母': '#07', '討論就是執行': '#08', '知道為什麼': '#09',
    '說人話': '#10', '自動自發': '#11', '拒絕搬運工': '#12',
    '客戶的聲音': '#13', '提煉': '#14', '說不知道': '#15',
    '複雜的解法': '#16', '環境確認': '#17', '語音糾偏': '#18',
    '心跳有意義': '#19', '啟動協議': '#20', '一字不差': '#21',
}

# ═══════════════════════════════════════════════════════════
# 第三階段：分段 + 評分
# ═══════════════════════════════════════════════════════════

print("【第二階段】分段掃描...")

# 以雙換行分段
blocks = re.split(r'\n(?=\n)', all_text)

stories = []
seen_hashes = set()

for block in blocks:
    block = block.strip()
    if len(block) < 60:
        continue

    # ── 找觸發詞 ──────────────────────────────────────────
    trigger = ''
    trigger_level = 0
    for ht in HIGH_TRIGGERS:
        if ht in block:
            trigger = ht
            trigger_level = 3
            break
    if not trigger:
        for mt in MED_TRIGGERS:
            if mt in block:
                trigger = mt
                trigger_level = 2
                break

    if not trigger:
        continue

    # ── 找教練說的話（完整段落）─────────────────────────
    coach_passages = []
    # 找 👤 或 教練： 或 coach: 或 「」
    for m in re.finditer(r'👤[教練：:\s]*(.{10,300}?)(?=\n\n|\n🤖|\n💬|\Z)', block, re.S):
        t = m.group(1).strip()
        if len(t) > 20:
            coach_passages.append(t)
    for m in re.finditer(r'教練[：:]\s*(.{10,200}?)(?=\n\n|\n[A-Z]|\Z)', block, re.S):
        t = m.group(1).strip()
        if len(t) > 20 and t not in coach_passages:
            coach_passages.append(t)
    for m in re.finditer(r'「([^」]{20,})」', block):
        t = m.group(1).strip()
        if t not in coach_passages:
            coach_passages.append(t)

    if not coach_passages:
        continue

    full_text = ' '.join(coach_passages)

    # ── 找守則 ───────────────────────────────────────────
    found_rules = []
    for kw, rid in RULES_MAP.items():
        if kw in block or kw in full_text:
            found_rules.append(rid)
    found_rules = list(dict.fromkeys(found_rules))[:5]

    # ── 找日期 ───────────────────────────────────────────
    date_match = re.search(r'2026-(?:0[4-5]|0[5-9]|10|11|12)-[0-3][0-9]', block)
    date = date_match.group() if date_match else 'unknown'

    # ── 找 Session ID ──────────────────────────────────────
    sid_match = re.findall(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', block)
    sid = sid_match[0][:8] if sid_match else 'unknown'

    # ── 評分 ──────────────────────────────────────────────
    score = 0
    score += trigger_level

    if any(w in full_text for w in HIGH_TRIGGERS):
        score += 2
    if any(w in full_text for w in ['60', '60美元', '60美金', '白忙', '白費', '快被打敗']):
        score += 2
    if len(coach_passages) >= 2:
        score += 1
    if found_rules:
        score += 1
    if any(c in full_text for c in ['👤', '教練：', '教練「']):
        score += 2

    # ── 去重 ──────────────────────────────────────────────
    h = hash(full_text[:80])
    if h in seen_hashes and score < 5:
        continue
    seen_hashes.add(h)

    stories.append({
        'trigger': trigger,
        'score': score,
        'date': date,
        'sid': sid,
        'text': full_text[:400],
        'passages': coach_passages,
        'rules': found_rules,
    })

# ═══════════════════════════════════════════════════════════
# 第四階段：排序 + 產出
# ═══════════════════════════════════════════════════════════

stories.sort(key=lambda x: -x['score'])

print(f"【第三階段】找到 {len(stories)} 個故事，去重後 {len(stories)} 筆\n")

# 顯示 Top 50
print('═' * 60)
print(f'TOP 100 故事原料（全面挖掘版）')
print('═' * 60)

for i, s in enumerate(stories[:100], 1):
    print(f"\n{'─'*60}")
    print(f"#{i:03d} | 觸發：{s['trigger']} | 分:{s['score']} | {s['date']} | S:{s['sid']}")
    if s['rules']:
        print(f"守則：{' '.join(s['rules'])}")
    for p in s['passages'][:3]:
        p = p.strip()
        if len(p) > 5:
            # 只顯示教練說的話
            clean = re.sub(r'^(👤|教練[：:]|coach[：:])', '', p).strip()
            clean = clean[:80]
            print(f"  📣 {clean}")

# ═══════════════════════════════════════════════════════════
# 寫入檔案
# ═══════════════════════════════════════════════════════════

out_path = '/Users/bymyway/.claude-code/workspace/distill/_STORY_LIST_FULL.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(f"# 故事清單（全量挖掘版）\n")
    f.write(f"> 挖掘時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"> 來源：distill/ ({len(distill_files)}) + daily/ ({len(daily_files)}) + memory/ ({len(mem_files)})\n")
    f.write(f"> 總文字量：{len(all_text):,} 字 | 去重後故事：{len(stories)} 筆\n\n")
    f.write('═' * 60 + '\n')
    for i, s in enumerate(stories, 1):
        f.write(f"#{i:03d} | 觸發：{s['trigger']} | 分:{s['score']} | {s['date']} | S:{s['sid']}\n")
        if s['rules']:
            f.write(f"守則：{' '.join(s['rules'])}\n")
        f.write(f"內容：{s['text'][:150]}\n\n")

print(f"\n✅ 已寫入 {out_path}")
print(f"共 {len(stories)} 個故事（目標100+，已達標：{len(stories) >= 100}）")