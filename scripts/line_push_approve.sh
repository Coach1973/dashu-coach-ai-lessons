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
