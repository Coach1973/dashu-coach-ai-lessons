#!/bin/bash
# 截圖鎖永久測試套件（案例 F 教訓：每次修改 hook 必先跑測試，全過才能 commit）
# 用法：bash test_screenshot_lock.sh

S=/Users/bymyway/.openclaw/workspace/scripts/screenshot_lock.sh
TOKEN=~/.openclaw/workspace/state/SCREENSHOT_APPROVED
PASS=0; FAIL=0

check() {  # check <測試名> <期望代碼> <實際代碼>
  if [ "$2" = "$3" ]; then
    echo "✅ $1"; PASS=$((PASS+1))
  else
    echo "❌ $1（期望 $2，實際 $3）"; FAIL=$((FAIL+1))
  fi
}

# 備份現有通行證狀態，測完還原
HAD_TOKEN=0; [ -f "$TOKEN" ] && HAD_TOKEN=1 && mv "$TOKEN" "$TOKEN.bak"

# 1. 沒通行證 → 直接截圖工具要被擋（exit 2）
echo '{"tool_name":"mcp__computer-use__screenshot","tool_input":{}}' | bash $S >/dev/null 2>&1
check "1 沒通行證截圖→擋" 2 $?

# 2. 沒通行證 → zoom 也要被擋
echo '{"tool_name":"mcp__computer-use__zoom","tool_input":{"region":[0,0,100,100]}}' | bash $S >/dev/null 2>&1
check "2 沒通行證zoom→擋" 2 $?

# 3. Chrome computer 點擊（非截圖）→ 放行
echo '{"tool_name":"mcp__Claude_in_Chrome__computer","tool_input":{"action":"left_click","coordinate":[1,2],"tabId":1}}' | bash $S >/dev/null 2>&1
check "3 點滑鼠非截圖→放行" 0 $?

# 4. Chrome computer 截圖 → 擋
echo '{"tool_name":"mcp__Claude_in_Chrome__computer","tool_input":{"action":"screenshot","tabId":1}}' | bash $S >/dev/null 2>&1
check "4 Chrome截圖→擋" 2 $?

# 5. 批次裡偷夾截圖 → 擋
echo '{"tool_name":"mcp__computer-use__computer_batch","tool_input":{"actions":[{"action":"left_click","coordinate":[1,2]},{"action":"screenshot"}]}}' | bash $S >/dev/null 2>&1
check "5 批次夾帶截圖→擋" 2 $?

# 6. 批次全是普通動作 → 放行
echo '{"tool_name":"mcp__computer-use__computer_batch","tool_input":{"actions":[{"action":"left_click","coordinate":[1,2]},{"action":"type","text":"hi"}]}}' | bash $S >/dev/null 2>&1
check "6 批次無截圖→放行" 0 $?

# 7. browser_batch 夾截圖 → 擋
echo '{"tool_name":"mcp__Claude_in_Chrome__browser_batch","tool_input":{"actions":[{"name":"computer","input":{"action":"screenshot","tabId":1}}]}}' | bash $S >/dev/null 2>&1
check "7 瀏覽器批次夾截圖→擋" 2 $?

# 8. 有通行證（10分鐘內）→ 放行
mkdir -p "$(dirname "$TOKEN")" && touch "$TOKEN"
echo '{"tool_name":"mcp__computer-use__screenshot","tool_input":{}}' | bash $S >/dev/null 2>&1
check "8 有通行證截圖→放行" 0 $?
rm -f "$TOKEN"

# 9. 通行證過期（假裝 11 分鐘前發的）→ 擋
touch "$TOKEN" && touch -A -001100 "$TOKEN" 2>/dev/null || touch -d "11 minutes ago" "$TOKEN" 2>/dev/null
python3 -c "import os,time; p=os.path.expanduser('$TOKEN'); os.utime(p,(time.time()-660,time.time()-660))"
echo '{"tool_name":"mcp__computer-use__screenshot","tool_input":{}}' | bash $S >/dev/null 2>&1
check "9 通行證過期→擋且銷毀" 2 $?
[ ! -f "$TOKEN" ] && echo "✅ 9b 過期通行證已自動銷毀" && PASS=$((PASS+1)) || { echo "❌ 9b 過期通行證沒銷毀"; FAIL=$((FAIL+1)); }

# 10. 非截圖類普通工具（防誤殺）→ 放行
echo '{"tool_name":"mcp__Claude_Preview__preview_snapshot","tool_input":{}}' | bash $S >/dev/null 2>&1
check "10 其他工具不誤殺→放行" 0 $?

# 還原
[ $HAD_TOKEN = 1 ] && mv "$TOKEN.bak" "$TOKEN"

echo ""
echo "結果：$PASS 過 / $FAIL 失敗"
[ $FAIL = 0 ] && echo "🎉 全數通過" || exit 1
