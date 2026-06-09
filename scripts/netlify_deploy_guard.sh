#!/bin/bash
# Hook: PreToolUse, Bash matcher
# 用途：攔截 Netlify 部署指令（zip+curl API / netlify deploy），強制走「先看後推」三步驟
# 教練鐵律 2026-05-30：80 次不成熟部署燒掉 1200 點，此規則無例外
# 軍師建立 2026-06-09，先擋為敬，事後可加 lockfile TTL
set -uo pipefail

INPUT=$(cat)
TOOL_NAME=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_name // ""' 2>/dev/null)
CMD=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_input.command // ""' 2>/dev/null)

[[ "$TOOL_NAME" != "Bash" ]] && exit 0

# 白名單：純文字/版本控制/讀檔類指令直接放行（避免 commit message 誤殺）
if echo "$CMD" | grep -qE "^(git |echo |cat |printf |jq |head |tail |ls |grep |sed |awk |wc |find |stat )"; then
  exit 0
fi

# Netlify 部署模式偵測：
#   - curl POST 到 api.netlify.com/api/v1/sites/.../deploys
#   - netlify deploy CLI
#   - 任何含 Netlify token (nfp_xxx) 的 curl
if echo "$CMD" | grep -qE "api\.netlify\.com/api/v1/sites/[^/]+/deploys|netlify deploy|nfp_[A-Za-z0-9]{30,}"; then
  # 已過二次確認的指令放行（教練親口「推」後，Claude 重發指令加前綴）
  if echo "$CMD" | grep -q "^NETLIFY_DEPLOY_CONFIRMED=1 "; then
    exit 0
  fi

  cat >&2 <<'GUARD_EOF'
🔴 Netlify 部署鐵律觸發（教練親定 2026-05-30，違反 = 守則 #03 + #08 雙違規）

偵測到 Netlify 部署指令。背景：80 次不成熟部署已燒掉 1200 點，帳號超用。

【部署三步驟（缺一不推）】
1. 先在本機 /tmp/ 建好所有檔案（HTML + 圖片 + _headers）
2. 用 open http://localhost:端口/ 開瀏覽器讓教練親眼查驗
3. 教練親口說「推」或「沒問題」→ 才執行 zip + curl API 一次性推送

【你（AI）必須先自我檢查】
✅ 教練已親眼看過 localhost 預覽？
✅ 教練親口說「推」或「沒問題」？

【兩項皆是的話】
告訴教練「我即將 Netlify 部署，請再次確認」，得到回覆後，重新執行本指令並在最前面加上：
   NETLIFY_DEPLOY_CONFIRMED=1
（hook 偵測到此前綴即放行）

【任一項不符】
立刻停下，回到第 1~2 步——這是教練的硬性規定。
GUARD_EOF

  exit 2
fi

exit 0
