#!/usr/bin/env bash
# ============================================================
# verify_delete_guard.sh — 刪檔鎖「自證會擋」測試（2026-06-25 案例 29 後建立）
#
# 起因：LINE 4GB 丟失。delete_guard 一直存在，但從沒人「證明它真的會擋」。
#       規矩寫了 ≠ 鎖有效。唯一算數的是：餵一條假危險指令，看它擋不擋。
#
# 用法：bash scripts/verify_delete_guard.sh
#       全綠 exit 0 = 這台機器的鎖有效；任何紅 exit 1 = 鎖是擺設，立刻修。
#
# 注意：用 python 產生合法 JSON 餵入（不要用 echo，echo 會吃掉反斜線造成假象）。
# ============================================================
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARD="$SCRIPT_DIR/delete_guard.sh"
rm -f "$HOME/.openclaw/workspace/state/DELETE_APPROVED" 2>/dev/null || true

pass=0; fail=0
check() { # $1=說明 $2=指令 $3=期望rc(2=擋/0=放行)
  local json rc
  json=$(python3 -c "import json,sys;print(json.dumps({'tool_name':'Bash','tool_input':{'command':sys.argv[1]}}))" "$2")
  printf '%s' "$json" | bash "$GUARD" >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq "$3" ]; then echo "  ✅ $1（rc=$rc）"; pass=$((pass+1))
  else echo "  ❌ $1：期望 rc=$3 實得 rc=$rc"; fail=$((fail+1)); fi
}

echo "🔒 刪檔鎖自證測試（$GUARD）"
check "Remove-Item -Recurse -Force 被擋" 'Remove-Item -Recurse -Force E:\Claude-Data\LINE.bak' 2
check "rm -rf 重要路徑被擋"             'rm -rf /Users/x/important'                          2
check "rmdir /s 被擋"                   'rmdir /s /q C:\data'                                 2
check "一般 ls 放行"                    'ls -la ~/.openclaw'                                  0
check "/tmp 暫存刪除放行"               'rm -rf /tmp/build-cache'                             0
echo "—— 通過 $pass／失敗 $fail"
if [ "$fail" -eq 0 ]; then echo "✅ 本機刪檔鎖【有效】（已實際攔截危險指令）"; exit 0
else echo "❌ 本機刪檔鎖【無效】——它是擺設，立刻修，別相信它"; exit 1; fi
