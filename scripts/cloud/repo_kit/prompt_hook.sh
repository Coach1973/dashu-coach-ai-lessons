#!/bin/bash
# 雲端對話每句話提醒（UserPromptSubmit）：台灣時間＋三件最重要的事。由 Mac 自動同步，請勿手改。
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0
TW=$(TZ='Asia/Taipei' date '+%Y-%m-%d %A %H:%M' 2>/dev/null)
echo "🕐 台灣時間 ${TW}（雲端主機是 UTC；對大樹教練一律講台灣時間，白話講「下午 2 點半」）"
echo "☁️ 大樹教練雲端規則提醒：①第一行亮燈（🔵Haiku／🟢Sonnet／🟣Opus；閒聊寫「🔵 閒聊」）②方向清楚就做完，不問「同不同意」；推不上 main 就推 claude/* 分支＋寫信 docs/to_junshi/，由 Mac 軍師驗證上線 ③交付前自己驗證，口頭完成不算。規則全文：.claude/coach-rules/RULES.md"
exit 0
