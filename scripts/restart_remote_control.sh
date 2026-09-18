#!/bin/bash
# 手機Remote Control (claude rc) 安全重啟腳本
# v2（2026-09-19 簡化版，取代舊版「搬移settings.json」做法）
#
# 舊版根因（2026-09-19 00:xx查明）：真正擋住 claude rc 啟動的只有
# CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1（會阻擋 Remote Control 必須的
# feature-flag評估），這個key原本同時存在於 ~/.zshrc 的 export 跟
# ~/.claude/settings.json 的全域 env 區塊，且 settings.json 的版本會被 claude CLI
# 無條件套用、不受呼叫端 `env -u` 影響，導致舊版只能靠「暫時搬移整份settings.json」硬解。
#
# v2改動（2026-09-19 05:xx）：已把 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC 從
# settings.json 的 env 區塊永久移除（不再需要整份搬移還原這麼粗暴的做法），
# 現在只要在啟動 claude rc 的那個shell裡 unset 掉 .zshrc 匯出的同名shell變數即可。
#
# ⚠️反直覺的坑（反覆實測4次同一結論，2026-09-19）：**絕對不要主動
# unset ANTHROPIC_BASE_URL / ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN**——
# 明確unset這三個反而會觸發 claude rc 自己的硬性檢查噴錯
# 「ANTHROPIC_BASE_URL is set and does not point at api.anthropic.com」，
# 即使unset後的值理當是空的。只unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC
# 這一個變數才會成功連線，其餘三個變數留給settings.json自然套用（不會造成問題，
# 見下方nettop驗證）。
#
# 🔍 順便實測澄清（nettop+lsof驗證，2026-09-19）：這台Mac的Claude Code CLI在有效
# Claude Pro OAuth登入狀態下，ANTHROPIC_BASE_URL/API_KEY/AUTH_TOKEN實際上不影響
# 真正連線目的地（推測是MiniMax金鑰格式sk-cp-0_開頭不被CLI辨識為合法Anthropic key，
# 自動fallback回原生OAuth）——用ps aux揪出的既有RC session(PID 4439)全程只連到
# 160.79.104.10（真Anthropic），從沒連過MiniMax真實IP(175.99.116.25，TLS憑證
# www.minimax.io)。
#
# ANTHROPIC_MODEL / ANTHROPIC_DEFAULT_SONNET_MODEL 明確帶入 claude-sonnet-5[1m]，
# 讓手機這條連線拿到1M context（已用 --print 直接測試過，真Anthropic backend
# 認得這個model id，回應 CTX=1000000）。
#
# 用法：bash scripts/restart_remote_control.sh

set -euo pipefail

SESSION="remote-control"

tmux kill-session -t "$SESSION" 2>/dev/null || true

tmux new-session -d -s "$SESSION" -x 200 -y 50
tmux send-keys -t "$SESSION" 'unset CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC; export ANTHROPIC_MODEL="claude-sonnet-5[1m]" ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-5[1m]"; claude rc' C-m

echo "⏳ 啟動 claude rc..."

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
  exit 0
else
  echo "❌ 15秒內未看到「Connected」，目前畫面："
  tmux capture-pane -t "$SESSION" -p
  exit 1
fi
