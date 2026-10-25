#!/bin/bash
# Hook：UserPromptSubmit
# 用途：偵測對話長度，超過門檻自動提醒教練「準備開新視窗」。
#       教練長期靠人工判斷對話太長，此 hook 把判斷自動化。
# 原理：從 session_id 算出對話檔（~/.claude/projects/.../{session_id}.jsonl），
#       數 user 真實發言輪數，>= 門檻就注入提醒。
# 防洗版：marker 記錄上次提醒的「輪數帶」，每 +10 輪才提醒一次（20/30/40...）。
# 軍師建立 2026-05-28（教練親定門檻 20 輪）
set -uo pipefail

THRESHOLD=20            # 第一次提醒的輪數
BAND=10                 # 之後每多 N 輪再提醒一次
PROJECT_DIR="/Users/bymyway/.claude/projects/-Users-bymyway--openclaw"

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
[[ -z "$SESSION_ID" ]] && exit 0

JSONL="${PROJECT_DIR}/${SESSION_ID}.jsonl"
[[ -f "$JSONL" ]] || exit 0

# 數 user 真實發言（排除 tool_result / meta）
TURNS=$(python3 -c "
import json, sys
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

# 算目前所在的「輪數帶」（20→20, 30→30, 35→30）
CUR_BAND=$(( (TURNS / BAND) * BAND ))

MARKER="/tmp/session_len_band_${SESSION_ID}"
LAST_BAND=0
[[ -f "$MARKER" ]] && LAST_BAND=$(cat "$MARKER" 2>/dev/null || echo 0)

# 這個帶已經提醒過就不再提醒
[[ "$CUR_BAND" -le "$LAST_BAND" ]] && exit 0

echo "$CUR_BAND" > "$MARKER"

echo "🔔 對話長度提醒（系統自動）：本場已約 ${TURNS} 輪對話。"
echo "   建議告一段落時：說「總結並上傳」→ 我會蒸餾紀錄+commit，然後你可開新視窗（/clear）。"
echo "   ⚠️ 回覆時兩個數字一起講：「已 ${TURNS} 輪」＋「對話容量約 xx%」（用 get_usage 查 context.percentUsed，或看容量報告）。"
echo "      輪數只是參考，容量才決定要不要換；兩個都給教練，由教練自己評估（教練 10/25 19:55）。"
echo "   （提醒只是參考，任務沒做完不必急著換。）"

exit 0
