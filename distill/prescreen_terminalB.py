#!/usr/bin/env python3
"""
預篩腳本：自動識別值得蒸餾的教練訊息
標準：6個值得收錄條件
"""
import json, os, re

SUM_FILE = os.path.expanduser('~/.openclaw/workspace/distill/terminalB_message_summary.md')
OUT_FILE = os.path.expanduser('~/.openclaw/workspace/distill/terminalB_candidates.md')

# 讀取所有訊息
with open(os.path.expanduser('~/.openclaw/workspace/distill/terminalB_all_messages.jsonl')) as f:
    all_msgs = [json.loads(l) for l in f if l.strip()]

print(f"總訊息：{len(all_msgs)}")

# 預篩關鍵字
SCREEN_PATTERNS = {
    # 1.新規則/守則/原則
    '新規則': [r'守則', r'原則', r'鐵律', r'規定', r'不准', r'不要', r'必須', r'絕對'],
    # 2.糾正AI
    '糾正': [r'不是', r'錯了', r'重新', r'再說一遍', r'搞清楚', r'你搞', r'重新來', r'失敗', r'不行', r'不對'],
    # 3.價值判斷
    '價值判斷': [r'值得', r'重要', r'優先', r'核心', r'關鍵', r'決策', r'方向', r'對的', r'錯的'],
    # 4.數字/事實
    '數字事實': [r'\d+', r'MB', r'GB', r'Token', r'token', r'分鐘', r'小時', r'天', r'次'],
    # 5.任務分配
    '分配分工': [r'你做', r'交給', r'負責', r'分工', r'指定', r'讓.*做'],
    # 6.教練口頭禪/情緒
    '情緒/口頭禪': [r'不對', r'再說', r'等等', r'停', r'慢著', r'等等', r'算了', r'好', r'好（', r'好的'],
    # 7.系統類
    '系統建置': [r'commit', r'push', r'script', r'腳本', r'自動化', r'流程'],
    # 8.教練說"記住"
    '記憶指令': [r'記住', r'記得', r'寫下', r'存'],
    # 9.教練說話很長（可能很重要）
    '長訊息': [],  # 會單獨處理
}

candidates = []
for m in all_msgs:
    content = m['content']
    reasons = []

    # 長訊息（>=500字）可能重要
    if len(content) >= 500:
        reasons.append('長訊息')

    # 關鍵字匹配
    for reason, patterns in SCREEN_PATTERNS.items():
        if reason == '長訊息':
            continue
        for pat in patterns:
            if re.search(pat, content):
                reasons.append(reason)
                break

    # 訊息中包含明確口語化表達（教練風格）
    if any(kw in content for kw in ['教練', '教練說', '教練：', '我告訴你', '你搞清楚']):
        if '新規則' not in reasons:
            reasons.append('教練風格')

    # 包含具體操作指示
    if any(kw in content for kw in ['做', '去做', '執行', '跑', '開', '關', '改']):
        if len(content) >= 200:
            reasons.append('具體操作')

    if reasons:
        candidates.append({
            **m,
            'reasons': list(set(reasons)),
            'reasons_str': ', '.join(set(reasons))
        })

print(f"初步候選：{len(candidates)} 則")
for r in sorted(set(m['reasons_str'] for m in candidates)):
    cnt = sum(1 for m in candidates if r in m['reasons_str'])
    print(f"  {r}: {cnt}")

# 寫入候選檔
with open(OUT_FILE, 'w') as f:
    f.write("# 終端機B候選場景（預篩後）\n\n")
    f.write(f"> 總訊息：{len(all_msgs)} | 候選：{len(candidates)}\n\n")
    f.write("---\n\n")
    for i, m in enumerate(candidates, 1):
        reasons = ', '.join(sorted(m['reasons']))
        f.write(f"## [{i:03d}] {m['file'][:12]} ({m['char_count']}字)\n")
        f.write(f"> 匹配：{reasons}\n\n")
        preview = m['content'][:400].replace('\n', ' ')
        f.write(f"{preview}...\n\n")

print(f"\n候選檔寫入：{OUT_FILE}")

# 寫JSON版本（供程式進一步處理）
cand_json = os.path.expanduser('~/.openclaw/workspace/distill/terminalB_candidates.jsonl')
with open(cand_json, 'w') as f:
    for m in candidates:
        f.write(json.dumps(m, ensure_ascii=False) + '\n')
print(f"JSON版：{cand_json}")
