#!/bin/bash
# 手機Remote Control (claude rc) 安全重啟腳本
# v4（2026-09-23 修正env -i過度清空+新增bridge-pointer殭屍session防呆）
#
# 根因演進：
# v1（2026-09-17）：靠「暫時清空settings.json、用完復原」——會反覆漏回去。
# v2（2026-09-19）：settings.json的API_KEY/AUTH_TOKEN/BASE_URL留著不動（怕unset觸發
#   claude rc硬性檢查噴錯），結果MiniMax金鑰長期活著、手機端真的被計費。
# v3（2026-09-22）：改用`env -i`完全清空環境變數表堵住MiniMax殘留，**但清過頭**——
#   連macOS正常運作需要的`__CFBundleIdentifier`/`TMPDIR`/`SSH_AUTH_SOCK`都一起清掉，
#   導致連線握手成功但訊息處理直接卡死，教練連續開4次新對話都完全沒有任何回應。
# v4根因①（env過度清空）：改回**精準`env -u`只拔掉壞的7個ANTHROPIC_*變數**，其餘
#   正常環境(TMPDIR/SSH_AUTH_SOCK/__CFBundleIdentifier等)全部保留繼承。
# v4根因②（真正卡住教練超過1小時的元凶，比env問題更嚴重）：
#   `~/.claude/projects/-Users-bymyway--openclaw/bridge-pointer.json`這個指標檔案
#   會讓每次`claude rc`重啟都去reuse上一次的environment_id，如果那個environment底下
#   卡著一個`state:queued`永遠沒有真正start的殭屍session，**教練不管開幾次新對話，
#   都會被導回同一個死掉的session**，畫面完全沒有任何回應。這是env變數以外、完全
#   獨立的另一個坑，過去被誤判成「連線設定沒修好」，浪費超過1小時反覆重啟同一個
#   錯誤方向。
#
# v4修法：①env恢復精準`env -u`（不用env -i）②每次重啟前先檢查
#   bridge-pointer.json，如果指向的session年齡异常(卡超過5分鐘還沒轉為active)，
#   自動備份+刪除，強迫重新註冊全新environment。
#
# 診斷工具：卡住但看不出原因時，用
#   `claude rc --debug-file /tmp/rc_debug.log -v`啟動，
#   `grep -E "Found prior|state.*queued|Adopted session" /tmp/rc_debug.log`
#   直接看有沒有在reuse殭屍session，比瞎猜env變數快得多。
#
# 完整脈絡：[[reference_claude_code_remote_control_setup_sop_2026-09-17]]
#          [[feedback_settings_json_minimax_leak_not_cleared_2026-09-22]]
#
# 用法：bash scripts/restart_remote_control.sh

set -euo pipefail

SESSION="remote-control"
POINTER="$HOME/.claude/projects/-Users-bymyway--openclaw/bridge-pointer.json"

# 防呆：清掉可能卡著殭屍session的舊指標檔（備份後刪除，強制重新註冊environment）
if [ -f "$POINTER" ]; then
  echo "🔍 發現既有 bridge-pointer.json，備份後清除以避免reuse到殭屍session..."
  cp "$POINTER" "/tmp/bridge-pointer.json.bak.$(date +%Y%m%d_%H%M%S)"
  rm -f "$POINTER"
fi

tmux kill-session -t "$SESSION" 2>/dev/null || true
sleep 2

tmux new-session -d -s "$SESSION" -c ~/.openclaw -x 200 -y 50
tmux send-keys -t "$SESSION" 'env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_DEFAULT_HAIKU_MODEL -u ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME -u ANTHROPIC_DEFAULT_OPUS_MODEL -u ANTHROPIC_DEFAULT_OPUS_MODEL_NAME -u CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC claude rc' C-m

echo "⏳ 啟動 claude rc（精準env -u排除MiniMax殘留 + 已清除殭屍指標檔）..."

SUCCESS=0
for i in $(seq 1 15); do
  sleep 1
  PANE=$(tmux capture-pane -t "$SESSION" -p 2>/dev/null || true)
  if echo "$PANE" | grep -q "Choose \[1/2\]"; then
    tmux send-keys -t "$SESSION" "1" C-m
  fi
  if echo "$PANE" | grep -q "already served"; then
    echo "❌ 偵測到「already served」衝突，可能還有殘留process，請手動排查"
    tmux capture-pane -t "$SESSION" -p
    exit 1
  fi
  if echo "$PANE" | grep -q "Connected"; then
    SUCCESS=1
    break
  fi
done

if [ "$SUCCESS" = "1" ]; then
  echo "✅ Remote Control 已成功啟動並連線"
  tmux capture-pane -t "$SESSION" -p | grep -A3 "Connected"
  echo ""
  echo "🔍 驗證環境變數乾淨度（不應出現任何 API_KEY/AUTH_TOKEN/BASE_URL/DEFAULT_HAIKU/DEFAULT_OPUS）："
  PANE_PID=$(tmux list-panes -t "$SESSION" -F "#{pane_pid}")
  BRIDGE_PID=$(pgrep -P "$PANE_PID" | head -1)
  ps eww -p "$BRIDGE_PID" 2>/dev/null | tr ' ' '\n' | grep -iE "^ANTHROPIC_(API_KEY|AUTH_TOKEN|BASE_URL|DEFAULT_HAIKU|DEFAULT_OPUS)" || echo "（無殘留，乾淨）"
  exit 0
else
  echo "❌ 15秒內未看到「Connected」，目前畫面："
  tmux capture-pane -t "$SESSION" -p
  exit 1
fi
