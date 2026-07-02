#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
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
TURNS=$(python3 -c "
import json
n=0
try:
    with open('$TRANSCRIPT_PATH') as f:
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

MENTIONED_MARKER="/tmp/session_proactive_mentioned_${SESSION_ID}"
LAST_MENTIONED=0
[[ -f "$MENTIONED_MARKER" ]] && LAST_MENTIONED=$(cat "$MENTIONED_MARKER" 2>/dev/null || echo 0)

# 這個輪數帶已經主動提過了，不用再提醒
[[ "$CUR_BAND" -le "$LAST_MENTIONED" ]] && exit 0

LAST_TEXT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json
path = sys.argv[1]
try:
    with open(path) as f:
        lines = [l for l in f if l.strip()]
except Exception:
    sys.exit(0)
for line in reversed(lines):
    try:
        evt = json.loads(line)
        if evt.get('type') == 'assistant':
            contents = evt.get('message', {}).get('content', [])
            texts = [c.get('text', '') for c in contents if c.get('type') == 'text']
            print('\n'.join(texts))
            break
    except Exception:
        continue
PYEOF
)

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
