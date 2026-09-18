#!/bin/bash
# 手機Remote Control (claude rc) 安全重啟腳本
# 根因（2026-09-19查明）：~/.claude/settings.json 的全域 env 區塊（MiniMax路由設定：
# ANTHROPIC_API_KEY/BASE_URL/AUTH_TOKEN/MODEL/CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC）
# 會被 claude CLI 無條件套用到每一個 claude 呼叫（包含 claude rc），
# 不受呼叫端 `env -u` 或 `--setting-sources` 影響（該flag在目前CLI版本已失效，"Unknown argument"）。
# claude rc 啟動當下需要真正的 api.anthropic.com + 未停用的 feature-flag 評估，
# 兩者都會被上述全域設定擋下。
#
# 解法：啟動當下暫時移開 settings.json（不影響其他已在跑的claude session，
# 因為env是process啟動時讀取一次，不是持續輪詢檔案），host process成功啟動、
# 讀完自己需要的env之後，process記憶體裡已經有了，跟檔案是否存在無關，
# 立即把settings.json還原，全程檔案「消失」的時間窗口不到10秒。
#
# 用法：bash scripts/restart_remote_control.sh

set -euo pipefail

SETTINGS="/Users/bymyway/.claude/settings.json"
BACKUP="/tmp/settings_rc_restart_backup_$(date +%s).json"
SESSION="remote-control"

if [ ! -f "$SETTINGS" ]; then
  echo "❌ 異常：$SETTINGS 不存在，可能上次還原失敗，請人工檢查 /tmp/settings_*.json 備份"
  exit 1
fi

cp "$SETTINGS" "$BACKUP"
echo "✅ 已備份 settings.json → $BACKUP"

restore_settings() {
  if [ -f "${SETTINGS}.tmp_restart" ]; then
    mv "${SETTINGS}.tmp_restart" "$SETTINGS"
    echo "✅ settings.json 已還原"
  fi
}
trap restore_settings EXIT

tmux kill-session -t "$SESSION" 2>/dev/null || true

mv "$SETTINGS" "${SETTINGS}.tmp_restart"
echo "⏳ settings.json 暫時移開，啟動 claude rc..."

tmux new-session -d -s "$SESSION" -x 200 -y 50
tmux send-keys -t "$SESSION" "unset ANTHROPIC_API_KEY ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_MODEL ANTHROPIC_DEFAULT_HAIKU_MODEL ANTHROPIC_DEFAULT_OPUS_MODEL ANTHROPIC_DEFAULT_SONNET_MODEL CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC; claude rc" C-m

# 等待啟動，最多10秒，看到「Connected」就算成功
SUCCESS=0
for i in $(seq 1 10); do
  sleep 1
  if tmux capture-pane -t "$SESSION" -p 2>/dev/null | grep -q "Connected"; then
    SUCCESS=1
    break
  fi
done

# trap 會自動還原settings.json

if [ "$SUCCESS" = "1" ]; then
  echo "✅ Remote Control 已成功啟動並連線"
  tmux capture-pane -t "$SESSION" -p | grep -A3 "Connected"
  exit 0
else
  echo "❌ 10秒內未看到「Connected」，目前畫面："
  tmux capture-pane -t "$SESSION" -p
  exit 1
fi
