#!/bin/bash
# Hook：PreToolUse（matcher: Bash）
# 用途：攔截「open -a Google Chrome / start chrome」開啟本機 127.0.0.1/localhost:<port>
#       的指令，若埠號落在瀏覽器內建 ERR_UNSAFE_PORT 黑名單，直接擋下並提醒改用
#       別的埠或對外網址——不要等跳出來教練看到「無法連上這個網站」才發現。
# 起因（2026-07-28 教練親口）：event-signup用5060埠，教練連127.0.0.1:5060出現
#       ERR_UNSAFE_PORT，一開始誤判成網路問題。教練要求「寫進SOP，不要每次都要
#       我提醒『記得跳HTML』然後結果是無法顯示網頁」。
# 設計原則：只攔本機127.0.0.1/localhost開頭的網址（對外網址走443/80不受此限制，
#       不需要檢查）。黑名單只列常見/曾踩雷過的埠號，不追求列全瀏覽器原始碼裡的完整清單。
set -uo pipefail

INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_input.command // ""' 2>/dev/null)

# 白名單：純文字/版本控制/讀檔類指令直接放行——避免commit message、echo說明文字
# 剛好同時含有「open -a Google Chrome」跟「127.0.0.1:port」兩段文字被誤判成真的執行
# （2026-07-28實測：commit訊息描述這支hook自己時真的誤觸發過，仿照netlify_deploy_guard.sh設計）
echo "$CMD" | grep -qE "^\s*(git |echo |printf |cat |jq )" && exit 0

# 只攔「真的執行」的 open -a Google Chrome / start chrome 指令——要求該片段前面
# 是指令起始位置或 &&/;/| 等指令分隔符，不能是任意文字中間，且後面要真的接網址參數
echo "$CMD" | grep -qE '(^|&&|;|\|)\s*(open\s+-a\s+"?Google Chrome"?|start\s+chrome)\s+"?(https?://|file://)' || exit 0
echo "$CMD" | grep -qE '(127\.0\.0\.1|localhost):[0-9]+' || exit 0

PORT=$(echo "$CMD" | grep -oE '(127\.0\.0\.1|localhost):[0-9]+' | head -1 | grep -oE '[0-9]+$')
[[ -z "$PORT" ]] && exit 0

# 瀏覽器(Chrome/Firefox等)內建ERR_UNSAFE_PORT黑名單，這裡只列常見/已知會撞到的
UNSAFE_PORTS=" 1 7 9 11 13 15 17 19 20 21 22 23 25 37 42 43 53 69 77 79 87 95 101 102 103 104 109 110 111 113 115 117 119 123 135 139 143 179 389 427 465 512 513 514 515 526 530 531 532 540 548 554 556 563 587 601 636 989 990 993 995 1719 1720 1723 2049 3659 4045 5060 5061 6000 6566 6665 6666 6667 6668 6669 6697 10080 "

if [[ "$UNSAFE_PORTS" == *" $PORT "* ]]; then
  cat >&2 <<GUARD_EOF

🔴🔒 瀏覽器不安全埠攔截（2026-07-28 教練親定，避免ERR_UNSAFE_PORT重演）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
偵測到要用瀏覽器開啟本機埠 ${PORT}——這個埠在Chrome/Firefox內建安全黑名單裡，
瀏覽器會直接拒絕連線並顯示「ERR_UNSAFE_PORT / 無法連上這個網站」，
跟服務本身是否正常運作無關，就算curl測試200也一樣打不開。

✅ 改用以下其中一種方式，不要直接開這個埠：
  1. 如果這個服務已經有對外網址（Cloudflare Tunnel/Netlify等，走443），優先用那個網址
  2. 如果是本機臨時測試伺服器（python3 -m http.server這類），換一個安全埠再開
     （例如 8000/8080/8901 這類常見開發埠都安全）
  3. 如果是既有服務（像event-signup用5060）改埠風險較高（牽動已印QR碼/systemd設定），
     不要當場改埠，改用它的對外網址驗證，或用Flask test_client產生靜態快照給教練看

參考記憶：reference_browser_unsafe_port_5060
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GUARD_EOF
  exit 2
fi

exit 0
