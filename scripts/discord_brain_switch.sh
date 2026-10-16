#!/bin/bash
# Discord 機器人「龍蝦特助」換腦（2026-10-17）
#   minimax：小龍蝦（OpenClaw，腦是 MiniMax-M3）——平常聊天用，省 Claude 用量（預設）
#   claude ：真的 Claude（Mac 上 tmux 視窗 discord-claude 常駐，用教練的 Pro 用量）
#   status ：看現在是哪一邊
# 用法：bash scripts/discord_brain_switch.sh minimax|claude|status
# 兩邊不能同時開（同一把金鑰會雙重回覆），所以一定先關一邊再開另一邊。
# 切換會重啟小龍蝦閘道，Telegram／LINE 會斷約 20 秒。
# 教練 10/17：「我只需要知道兩邊都通用，但我如果真的要聊天、要幹嘛，為了節省流量」→ 平常用 minimax。
set -u
MODE="${1:-status}"
OC() { openclaw "$@" 2>&1 | grep -v -E 'ExperimentalWarning|trace-warnings|Retrying'; }
start_claude() {
  tmux has-session -t discord-claude 2>/dev/null && return 0
  tmux new-session -d -s discord-claude -x 160 -y 50 -c "$HOME/claude-discord" \
    "env -i HOME=$HOME USER=$USER LOGNAME=$USER PATH=$PATH TERM=xterm-256color LANG=en_US.UTF-8 claude --channels plugin:discord@claude-plugins-official"
}
status() {
  echo "Claude 視窗（discord-claude）：$(tmux has-session -t discord-claude 2>/dev/null && echo 開著 || echo 沒開)"
  OC channels status --probe | grep -E '^- (Discord|Telegram|LINE)' | sed -E 's/, (token|mode|bot|groups|signing|transport|in:|intents).*//'
}
case "$MODE" in
  minimax)
    tmux kill-session -t discord-claude 2>/dev/null
    printf '{ channels: { discord: { enabled: true } } }\n' | OC config patch --stdin
    OC gateway restart | tail -1; sleep 25; status ;;
  claude)
    printf '{ channels: { discord: { enabled: false } } }\n' | OC config patch --stdin
    OC gateway restart | tail -1; sleep 20; start_claude; sleep 12; status ;;
  status) status ;;
  *) echo "用法：$0 minimax|claude|status"; exit 1 ;;
esac
