#!/bin/bash
# 手機Remote Control (claude rc) 安全重啟腳本
# v3（2026-09-22 永久拔除MiniMax版，取代v2的unset做法）
#
# 根因演進：
# v1（2026-09-17）：靠「暫時清空settings.json、用完復原」——會反覆漏回去。
# v2（2026-09-19）：改用shell層`unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`+
#   export ANTHROPIC_MODEL，settings.json的API_KEY/AUTH_TOKEN/BASE_URL留著不動
#   （怕unset觸發claude rc硬性檢查噴錯）。
# v3根因（2026-09-22教練用雙帳單交叉比對抓到）：v2讓settings.json的MiniMax金鑰/
#   BASE_URL/DEFAULT_HAIKU_MODEL/DEFAULT_OPUS_MODEL長期活著，手機端某些對話串
#   （非這支腳本啟動的主線，是手機app自己spawn的子session）拿這組殘留憑證真的打
#   MiniMax、真的被計費。更關鍵的坑：**已經在跑的shell（包括這個Claude Code session
#   自己的Bash工具shell）啟動當下就注入好舊的ANTHROPIC_*環境變數，事後改settings.json
#   不會讓這些已存在的shell/process重新讀取**——用這種shell開新tmux session，子行程
#   還是會繼承到舊值，跟settings.json當下內容無關。
#
# v3修法：①`~/.claude/settings.json`永久移除ANTHROPIC_API_KEY/AUTH_TOKEN/BASE_URL/
#   DEFAULT_HAIKU_MODEL/DEFAULT_OPUS_MODEL（不再「用完復原」，因為終端機/桌面版本來
#   就用claude-sonnet-5原生model走OAuth，從未依賴這幾個fallback變數，拔掉無影響）
#   ②啟動claude rc改用`env -i`完全清空環境變數表（不繼承任何父shell的舊值），只留
#   HOME/USER/PATH/TERM/SHELL+明確帶入的ANTHROPIC_MODEL/DEFAULT_SONNET_MODEL，
#   物理上讓這個process樹裡不存在任何MiniMax金鑰/URL可用。
#
# 完整脈絡：[[reference_claude_code_remote_control_setup_sop_2026-09-17]]
#          [[feedback_settings_json_minimax_leak_not_cleared_2026-09-22]]
#
# 用法：bash scripts/restart_remote_control.sh

set -euo pipefail

SESSION="remote-control"

tmux kill-session -t "$SESSION" 2>/dev/null || true

tmux new-session -d -s "$SESSION" -c ~/.openclaw -x 200 -y 50
tmux send-keys -t "$SESSION" 'env -i HOME="$HOME" USER="$USER" PATH="$PATH" TERM="$TERM" SHELL="$SHELL" ANTHROPIC_MODEL="claude-sonnet-5[1m]" ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-5[1m]" claude rc' C-m

echo "⏳ 啟動 claude rc（env -i 乾淨環境，物理排除MiniMax殘留憑證）..."

# 有些情況會先跳「spawn mode」選單（same-dir/worktree），偵測到就直接選預設值[1]
SUCCESS=0
for i in $(seq 1 15); do
  sleep 1
  PANE=$(tmux capture-pane -t "$SESSION" -p 2>/dev/null || true)
  if echo "$PANE" | grep -q "Choose \[1/2\]"; then
    tmux send-keys -t "$SESSION" "1" C-m
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
  CHILD=$(pgrep -P "$PANE_PID" | head -1)
  ps eww -p "$CHILD" 2>/dev/null | tr ' ' '\n' | grep -iE "ANTHROPIC" || echo "（無殘留，乾淨）"
  exit 0
else
  echo "❌ 15秒內未看到「Connected」，目前畫面："
  tmux capture-pane -t "$SESSION" -p
  exit 1
fi
