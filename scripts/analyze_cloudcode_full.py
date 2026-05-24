#!/usr/bin/env python3
"""
Cloud Code Desktop 全量蒸餾：教練核心需求 + 溝通風格 + 失敗模式
對全部 28 個 session 完整掃描
"""
import json, os, sys
from datetime import datetime
from collections import Counter, defaultdict

BASE = os.path.expanduser('~/Library/Application Support/Claude/local-agent-mode-sessions/')

sessions = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f == 'audit.jsonl':
            sp = os.path.join(root, f)
            sessions.append((sp, os.path.getmtime(sp)))
sessions.sort(key=lambda x: x[1], reverse=True)

# ── 第一階段：全部掃描 ──────────────────────────────────────
print("Phase 1: 全量掃描中...")

coach_all = defaultdict(list)  # date -> [msg,...]
turns_per_session = []

for sp, mtime in sessions:
    dt = datetime.fromtimestamp(mtime)
    date = dt.strftime('%Y-%m-%d')
    try:
        with open(sp) as fh:
            lines = fh.readlines()
        turns = 0
        for line in lines:
            if not line.strip(): continue
            try:
                e = json.loads(line)
                t = e.get('type', '')
                if t == 'user':
                    content = e.get('message', {}).get('content', '')
                    if isinstance(content, list):
                        texts = [c.get('text', '') for c in content if c.get('type') == 'text']
                        content = ' '.join(texts)
                    content = (content or '').strip()
                    if content and not content.startswith('<local-command>') and not content.startswith('</') and len(content) >= 6:
                        # 過濾系統訊息
                        skip = False
                        for kw in ['This session is being continued', 'Summary:', 'Primary Request', 'Key Technical', 'Files and Code']:
                            if content.startswith(kw): skip = True; break
                        if not skip:
                            coach_all[date].append(content[:400])
                    turns += 1
                elif t == 'assistant':
                    turns += 1
            except:
                pass
        if turns > 0:
            turns_per_session.append({'date': date, 'time': dt.strftime('%H:%M'), 'turns': turns, 'msgs': len(coach_all[date])})
    except:
        pass

total_msgs = sum(len(v) for v in coach_all.values())
print(f"掃描完成：{len(sessions)} 個 session，{total_msgs} 則教練訊息，覆蓋 {min(coach_all.keys())} ~ {max(coach_all.keys())}")

# ── 第二階段：行為分類（全部 session）──────────────────────
print("\nPhase 2: 行為分類中...")

categories = {
    'direct_cmd': [],     # 幫我...
    'step_directive': [], # 先...再...
    'correction': [],     # 不是.../不要...
    'verification': [],   # 確認/檢查/看一下
    'question': [],       # 提問
    'feedback': [],       # 反饋（謝謝/很棒/不錯）
    'context_switch': [],  # 換話題
    'fb_ops': [],         # FB 操作相關
    'file_ops': [],       # 檔案操作相關
    'frustration': [],    # 不耐煩/挫折
}

for date, msgs in coach_all.items():
    for msg in msgs:
        l = msg.lower()
        if any(k in l for k in ['不是這樣', '不要', '錯了', '重新', '修正', '重做', '你搞錯了', '你要確認']):
            categories['correction'].append(msg)
        elif any(k in l for k in ['幫我', '你去', '執行', '做一下', '幫大樹']):
            categories['direct_cmd'].append(msg)
        elif any(k in l for k in ['先', '再', '然後', '第一步', '第二步', '接著']):
            categories['step_directive'].append(msg)
        elif any(k in l for k in ['確認', '檢查', '看一下', '幫我看', '我看看', '目前']):
            categories['verification'].append(msg)
        elif '?' in msg or '？' in msg:
            categories['question'].append(msg)
        elif any(k in l for k in ['謝謝', '很棒', '不錯', '厲害', '很好', '正確']):
            categories['feedback'].append(msg)
        elif any(k in l for k in ['facebook', 'fb', 'messenger', '壽星', '生日', '發送訊息', '私訊']):
            categories['fb_ops'].append(msg)
        elif any(k in l for k in ['檔案', '資料夾', '刪除', '移動', '整理', '下載', '上傳']):
            categories['file_ops'].append(msg)
        elif any(k in l for k in ['算了', '算了', '不做了', '不用了', '放棄', '算了']):
            categories['frustration'].append(msg)
        else:
            categories['context_switch'].append(msg)

print("\n=== 全部 session 行為分類統計 ===")
for cat, items in sorted(categories.items(), key=lambda x: -len(x[1])):
    print(f"\n[{cat}] {len(items)}則")
    for item in items[:4]:
        print(f"  → {item[:90]}")

# ── 第三階段：核心需求提煉 ────────────────────────────────
print("\n\n=== 教練核心需求提煉 ===")

# 把所有訊息合併統計關鍵詞
all_msgs_flat = []
for msgs in coach_all.values():
    all_msgs_flat.extend(msgs)

print(f"\n總教練訊息：{len(all_msgs_flat)}則")
print(f"涵蓋 {len(coach_all)} 個工作日")

# 主題分類
themes = {
    'FB 操作': 0,
    '檔案整理': 0,
    '生日祝福': 0,
    '安裝設定': 0,
    'API/技術問題': 0,
    '工作流程自動化': 0,
    '記憶/交接問題': 0,
    '溝通/人機介面': 0,
    '時間/成本': 0,
    '其他': 0,
}

theme_signatures = {
    'FB 操作': ['fb', 'facebook', 'messenger', '貼文', '壽星', '生日', '私訊', '粉絲團', 'line'],
    '檔案整理': ['檔案', '資料夾', '整理', '刪除', '命名', '歸類', '分類', '下載'],
    '生日祝福': ['生日祝福', '壽星', '祝福語', '已傳送', '發送訊息'],
    '安裝設定': ['安裝', '設定', '設定', '設定', '下載', '更新', '版本'],
    'API/技術問題': ['api', 'error', 'token', '額度', '403', 'connect', '爬蟲', '抓取'],
    '工作流程自動化': ['自動化', '定時', '排程', 'cron', '每天', '每小時', '自動化'],
    '記憶/交接問題': ['記得', '忘記', '遺忘', '重開機', '沒了', '消失', '又忘了', '又忘記'],
    '溝通/人機介面': ['你叫什麼', '你是誰', '你怎麼', '為什麼', '語音', '打字', '截圖'],
    '時間/成本': ['token', '花費', '成本', '多少', '費用', '消耗'],
}

for msg in all_msgs_flat:
    l = msg.lower()
    matched = False
    for theme, sigs in theme_signatures.items():
        if theme == '其他': continue
        if any(sig in l for sig in sigs):
            themes[theme] += 1
            matched = True
            break
    if not matched:
        themes['其他'] += 1

print("\n教練需求頻率排行榜：")
for theme, count in sorted(themes.items(), key=lambda x: -x[1]):
    bar = '█' * (count // 5) + '─' * (20 - count // 5)
    print(f"  {theme:15} {count:4}則  {bar}")

# ── 第四階段：失敗模式摘錄 ────────────────────────────────
print("\n\n=== 失敗模式——教練受挫的瞬間 ===")
frustration_msgs = []
for msgs in coach_all.values():
    for msg in msgs:
        l = msg.lower()
        if any(k in l for k in [
            '又忘了', '你又', '怎麼又', '每次都', '為什麼又', '不是', '你搞錯',
            '重新', '重做', '沒做', '怎麼沒有', '消失了', '又沒了', '記得這個問題',
            '解決不了', '無效', '失敗', '不行', '卡住', '壞了', '沒反應'
        ]):
            frustration_msgs.append(msg[:200])

print(f"\n找到 {len(frustration_msgs)} 則帶挫敗感的教練訊息")
for i, msg in enumerate(frustration_msgs[:20], 1):
    print(f"\n  {i}. {msg}")

# ── 第五階段：高價值語錄摘錄 ─────────────────────────────
print("\n\n=== 教練金句——值得銘記的話 ===")
golden = []
for msgs in coach_all.values():
    for msg in msgs:
        l = msg.lower()
        # 教練的原則性陳述
        if any(k in l for k in [
            '我要強調', '記住', '你一定要', '這是我的原則', '請注意',
            '我要提醒', '重要的是', '記得一件事', '你應該要知道',
            '我最在乎', '這個很重要', '核心是', '底線是', '鐵律'
        ]):
            golden.append(msg[:250])

print(f"\n找到 {len(golden)} 則原則性陳述")
for i, msg in enumerate(golden[:15], 1):
    print(f"\n  {i}. {msg}")

# ── 第六階段：每日工作負擔 ───────────────────────────────
print("\n\n=== 每日工作負擔（教練訊息數）===")
for date in sorted(coach_all.keys(), reverse=True):
    count = len(coach_all[date])
    bar = '█' * count
    print(f"  {date}  {count:4}則  {bar}")

PYEOF