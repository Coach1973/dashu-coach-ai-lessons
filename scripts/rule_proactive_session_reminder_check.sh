#!/bin/bash
# ⚠️ 【功能已合併，本檔不再單獨註冊】2026-08-25 賈維斯體檢標註
# 這支的邏輯已於 2026-08-12 併入 scripts/stop_rules_master.py（12 支 Stop hook 合成單一總管，
# 避免每支各自重讀同一份 transcript，實測 14MB 檔 1.111 秒 → 0.066 秒）。
# 所以它「沒註冊進 settings.json」是正確狀態，不是漏裝。
# 原本的「# Hook：Stop」宣告改成下面這行，避免 audit_claude_hooks_registered.sh 每次都誤報。
# 已合併：Stop（實際執行者為 stop_rules_master.py）
# 用途：session_length_hook.sh（UserPromptSubmit）每過門檻就把「本場已約N輪」
#       塞進AI自己看得到的系統提醒，但那只是「餵給AI看」，不保證AI會主動
#       講給教練聽。這支 hook 補上那一段——檢查AI這輪的回覆有沒有真的把
#       提醒轉成講給教練聽的話，沒有就提醒自己補講。
# 起因（2026-07-02 教練親口）：記憶檔 feedback_proactive_session_reminder.md
#       早在2026-05-20就寫「視窗長度由我主動管，不等教練追問」，
#       session_length_hook.sh也確實每次都注入提醒，但軍師這場對話（75輪）
#       仍然是教練自己開口問「需要總結上傳嗎」才處理——機制存在但沒兌現，
#       跟案例37同一種病：SOP/機制存在≠真的被執行。
# 對齊守則#11（自動自發要體現在每次的主動關懷）。
set -uo pipefail

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
[[ -z "$SESSION_ID" || -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

THRESHOLD=20
BAND=10

# 跟 session_length_hook.sh 用同一套算法數輪數，保持一致
# 2026-08-12 體檢第2項：輪數與最終回覆都改讀 lib/stop_ctx.sh 共用快取
# （原本這支自己解析整份 jsonl 兩次：一次算輪數、一次抓最後回覆）
CTX=$(bash /Users/bymyway/.openclaw/workspace/scripts/lib/stop_ctx.sh "$TRANSCRIPT_PATH" "$SESSION_ID" 2>/dev/null) || exit 0
TURNS=$(printf '%s' "$CTX" | /usr/bin/jq -r '.user_turns // 0' 2>/dev/null)

[[ -z "$TURNS" || "$TURNS" -lt "$THRESHOLD" ]] && exit 0

CUR_BAND=$(( (TURNS / BAND) * BAND ))

MENTIONED_MARKER="/tmp/session_proactive_mentioned_${SESSION_ID}"
LAST_MENTIONED=0
[[ -f "$MENTIONED_MARKER" ]] && LAST_MENTIONED=$(cat "$MENTIONED_MARKER" 2>/dev/null || echo 0)

# 這個輪數帶已經主動提過了，不用再提醒
[[ "$CUR_BAND" -le "$LAST_MENTIONED" ]] && exit 0

LAST_TEXT=$(printf '%s' "$CTX" | /usr/bin/jq -r '.last_assistant_text // ""' 2>/dev/null)

# 檢查AI這輪的回覆有沒有主動提到「開新視窗/總結上傳」相關字眼
if printf '%s' "$LAST_TEXT" | grep -qE '開新視窗|開新的對話|新對話框|總結.{0,4}上傳|換新視窗|/clear'; then
  echo "$CUR_BAND" > "$MENTIONED_MARKER"
  exit 0
fi

{
  printf '\n🌱 守則#11 主動關懷偵測（系統 grep，Warn 級提醒）\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
  printf '本場已約 %s 輪，session_length_hook 已經提醒過，但這輪回覆\n' "$TURNS"
  printf '沒有主動跟教練提「建議開新視窗/總結上傳」——這是靠教練自己問才處理的。\n\n'
  printf '2026-07-02 教練親口：這條記憶檔 feedback_proactive_session_reminder.md\n'
  printf '早在2026-05-20就寫「視窗長度由我主動管，不等教練追問」，機制存在但沒兌現。\n\n'
  printf '✅ 下一輪回覆時，主動加一句提醒（不用等教練問）。\n'
  printf '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n'
} >&2

exit 0
