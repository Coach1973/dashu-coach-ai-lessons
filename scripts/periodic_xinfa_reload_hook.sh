#!/bin/bash
# Hook：UserPromptSubmit
# 用途：長對話每 N 輪，把「特助21守則」完整原文重新塞回 context 一次。
#
# 起因（2026-08-08 教練親問）：
#   「如果不能讀守則，那我花費心思寫出來的守則意義是什麼？」
#   CLAUDE.md 裡的守則全文只在 session 開始那一刻載入一次，隨對話變長，
#   系統可能把最早的 context 壓縮/摘要掉（本場已到20輪，session_length_hook.sh
#   只提醒「該開新視窗」，完全沒有把守則文字補回來）——這是「守則有沒有真的
#   還在我眼前」這件事，第一次有辦法用可驗證的方式補強，而不是空談「我會記得」。
#
# 原理：跟 session_length_hook.sh 用同一套輪數計算＋10輪一個band的節流設計，
#       每個新band第一次觸發時，直接把 特助心法.md 21條守則完整原文（含教練
#       親筆詮釋）貼回 context，不是連結、不是摘要，是原文。
#
# 軍師建立 2026-08-08（教練當場質問後動手，非承諾）
set -uo pipefail

THRESHOLD=20
BAND=10
PROJECT_DIR="/Users/bymyway/.claude/projects/-Users-bymyway--openclaw"
XINFA="$HOME/.openclaw/workspace/特助心法.md"

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
[[ -z "$SESSION_ID" ]] && exit 0
[[ -f "$XINFA" ]] || exit 0

# 2026-10-17：優先用 hook 輸入的 transcript_path——「開工」開在 worktree，對話記錄不在 PROJECT_DIR，
# 寫死路徑時找不到檔就靜靜退出，開工對話從沒重貼過守則（守則納入賈維斯_研究與方案_2026-10-17.md 原因5）
JSONL=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
[[ -f "$JSONL" ]] || JSONL="${PROJECT_DIR}/${SESSION_ID}.jsonl"
[[ -f "$JSONL" ]] || exit 0

TURNS=$(python3 -c "
import json
n=0
try:
    with open('$JSONL') as f:
        for line in f:
            try: o=json.loads(line)
            except: continue
            if o.get('type')=='user':
                c=(o.get('message') or {}).get('content')
                if isinstance(c,str) and c.strip():
                    n+=1
                elif isinstance(c,list):
                    has_text=any(isinstance(b,dict) and b.get('type')=='text' for b in c)
                    has_tr=any(isinstance(b,dict) and b.get('type')=='tool_result' for b in c)
                    if has_text and not has_tr:
                        n+=1
except: pass
print(n)
" 2>/dev/null)

[[ -z "$TURNS" || "$TURNS" -lt "$THRESHOLD" ]] && exit 0

CUR_BAND=$(( (TURNS / BAND) * BAND ))

MARKER="/tmp/xinfa_reload_band_${SESSION_ID}"
LAST_BAND=0
[[ -f "$MARKER" ]] && LAST_BAND=$(cat "$MARKER" 2>/dev/null || echo 0)

[[ "$CUR_BAND" -le "$LAST_BAND" ]] && exit 0

echo "$CUR_BAND" > "$MARKER"

printf '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '📜 守則全文重新載入（系統自動，第 %s 輪節點，非教練主動要求）\n' "$CUR_BAND"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
printf '對話已超過 %s 輪，session一開始載入的CLAUDE.md守則文字可能已被系統壓縮/摘要。\n' "$CUR_BAND"
printf '以下是特助21守則完整原文，重新確保仍在context裡，接下來的回應要對照這份原文，不憑印象。\n\n'

sed -n '54,165p' "$XINFA"

printf '\n（來源：%s，第%s輪自動重載）\n' "$XINFA" "$CUR_BAND"
printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'

exit 0
