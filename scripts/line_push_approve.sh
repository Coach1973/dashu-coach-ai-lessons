#!/bin/bash
# LINE 推播許可旗標（教練 2026-10-20 常設禁令；2026-10-22 改為「檔內時間戳」）
# 只有教練在對話裡明說同意某次 LINE 推播後，AI 才能執行本腳本。
#   line_push_approve.sh            寫入現在的時間戳＝許可 10 分鐘
#   line_push_approve.sh --revoke   刪檔＝立刻作廢（用完一定要作廢）
# 閘門只看檔案內容裡的時間戳，不看修改時間；touch 出來的空檔無效。
FLAG="$HOME/.openclaw/workspace/state/LINE_PUSH_APPROVED"
case "${1:-}" in
  --revoke)
    rm -f "$FLAG"
    echo "已作廢：$FLAG"
    ;;
  "")
    # 2026-11-01 案例142：小龍蝦自己跑本腳本、自己寫「教練常設指示」放行，發了 24 則廣告。
    # 往上查呼叫者：有 openclaw 一律拒絕；沒有 Claude 對話（claude.app／claude CLI）也拒絕。
    # 只看「程式本身＋第一個參數」，不看整串指令文字（指令裡寫到 openclaw 路徑不算）
    PID=$$; FROM_CLAUDE=0
    while [ "${PID:-0}" -gt 1 ]; do
      EXE=$(ps -o comm= -p "$PID" 2>/dev/null)
      HEAD2=$(ps -o args= -p "$PID" 2>/dev/null | awk '{print $1" "$2}')
      case "$HEAD2" in
        *openclaw/dist/*|*agent-cli/openclaw*|*openclaw_cron_daemon*)
          echo "❌ 拒絕：LINE 推播許可不能由小龍蝦／排程開，只能由軍師在教練親口同意後開。" >&2
          echo "$(date '+%F %T')	approve-refused	openclaw	$HEAD2" >> "$(dirname "$FLAG")/line_push_blocked.log"; exit 3 ;;
      esac
      case "$EXE" in
        *claude.app/Contents/MacOS/claude|*/bin/claude|claude) FROM_CLAUDE=1 ;;
      esac
      PID=$(ps -o ppid= -p "$PID" 2>/dev/null | tr -d ' ')
    done
    if [ "$FROM_CLAUDE" != 1 ]; then
      echo "❌ 拒絕：不是從 Claude 對話裡執行的。LINE 推播許可只能由軍師在教練親口同意後開。" >&2
      echo "$(date '+%F %T')	approve-refused	no-claude	ppid=$PPID" >> "$(dirname "$FLAG")/line_push_blocked.log"; exit 3
    fi
    mkdir -p "$(dirname "$FLAG")"
    NOW=$(date +%s)
    echo "$NOW" > "$FLAG"
    echo "已許可 LINE 推播 10 分鐘（到 $(date -r $((NOW + 600)) '+%H:%M:%S')）；用完請執行：$0 --revoke"
    ;;
  *)
    echo "用法：$0 [--revoke]" >&2
    exit 2
    ;;
esac
