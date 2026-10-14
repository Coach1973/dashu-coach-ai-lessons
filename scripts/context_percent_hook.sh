#!/bin/bash
# Hook：UserPromptSubmit
# 用途：對話容量（context window）用量跨過 30%、35%、40%、50% 時，各提醒教練一次。
# 起因（2026-10-14 23:53 台灣時間，教練）：桌面版畫面上看不到 context 了，
#       「我一般都是 30% 出頭就開始會開新的對話框了」→ 請 AI 在 30/35/40/50% 各提醒一次。
# 原理（事件觸發，不輪詢）：教練每說一句話才算一次——從對話檔（~/.claude/projects/.../{session_id}.jsonl）
#       取最後一則 AI 回覆的用量：input + cache_creation + cache_read ＝ 目前對話容量。
#       2026-10-14 實測對照桌面版 get_usage：兩邊相符（26.8% vs 26%）。
# 視窗大小：預設 100 萬 token（教練用 1M 版本）；可用環境變數 CONTEXT_WINDOW 覆寫。
# 防洗版：同一場只在「第一次跨過」某條線時提醒；一次跳過好幾條只提醒最高那條。
set -uo pipefail

LEVELS="30 35 40 50"
WINDOW="${CONTEXT_WINDOW:-1000000}"
PROJECT_DIR="${CONTEXT_PROJECT_DIR:-$HOME/.claude/projects/-Users-bymyway--openclaw}"
MARKER_DIR="${CONTEXT_MARKER_DIR:-/tmp}"

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
[[ -z "$SESSION_ID" ]] && exit 0
JSONL="${PROJECT_DIR}/${SESSION_ID}.jsonl"
[[ -f "$JSONL" ]] || exit 0

TOTAL=$(python3 - "$JSONL" <<'PY' 2>/dev/null
import json, sys
tot = 0
for line in open(sys.argv[1], errors="ignore"):
    try:
        o = json.loads(line)
    except Exception:
        continue
    if o.get("type") != "assistant":
        continue
    m = o.get("message") or {}
    u = m.get("usage")
    if not u or m.get("model") == "<synthetic>":
        continue
    tot = (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)
print(tot)
PY
)
[[ -z "$TOTAL" || "$TOTAL" -le 0 ]] && exit 0

PCT=$(( TOTAL * 100 / WINDOW ))
MARKER="${MARKER_DIR}/context_remind_${SESSION_ID}"
LAST=0
[[ -f "$MARKER" ]] && LAST=$(cat "$MARKER" 2>/dev/null || echo 0)

HIT=0
for L in $LEVELS; do
  if [[ "$PCT" -ge "$L" && "$L" -gt "$LAST" ]]; then HIT=$L; fi
done
[[ "$HIT" -eq 0 ]] && exit 0
echo "$HIT" > "$MARKER"

WAN=$(( TOTAL / 10000 ))
echo "🧠 對話容量提醒（系統自動，教練 2026-10-14 要求）：本場對話已用約 ${PCT}%（約 ${WAN} 萬 token，視窗 $(( WINDOW / 10000 )) 萬），剛跨過 ${HIT}% 這條線。"
echo "👉 請在這一則回覆的「最前面」用一句白話告訴教練：目前用了約 ${PCT}%。"
if [[ "$HIT" -ge 50 ]]; then
  echo "   已過一半，建議這一段做完就說「總結」，我會更新接力棒並上傳，您再開新對話框。"
elif [[ "$HIT" -ge 40 ]]; then
  echo "   容量越來越滿，建議找個段落收尾，說「總結」後開新對話框。"
else
  echo "   教練習慣在 30% 出頭開新對話框；告一段落時說「總結」，我會更新接力棒並上傳，您就可以開新的。任務沒做完不必急著換。"
fi
exit 0
