#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練在新 session 喊「開工」/「軍師」等暗號時，自動把 JUNSHI_HANDOFF_LATEST.md 餵進 context。
# 設計：每個 session 只餵一次（marker 檔防重複），避免每輪 prompt 都炸 token。
# 觸發詞：開工 / 軍師 / 接續指揮所考古 / Claude 軍師
set -uo pipefail

HANDOFF="/Users/bymyway/.openclaw/workspace/JUNSHI_HANDOFF_LATEST.md"
SESSION_DUMP="/Users/bymyway/.openclaw/workspace/claude-sessions"

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""')
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""')

MARKER="/tmp/junshi_fed_${SESSION_ID}"

# 「開工」=強制重餵口令（即使 marker 存在也餵）—— 教練在同視窗 /clear 後仍可重新觸發
# 其他軍師字眼 = 看 marker，同 session 只餵一次（避免隨口提到也炸 token）
FORCE_REFEED=0
if printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*開工[[:space:]]*$|開工了|開工。|開工！"; then
  FORCE_REFEED=1
fi

# 非強制模式 + marker 已存在 → 靜默退出
if [[ "$FORCE_REFEED" -eq 0 && -n "$SESSION_ID" && -f "$MARKER" ]]; then
  exit 0
fi

# 判斷是否為軍師接位暗號（中英都接）
if printf '%s' "$PROMPT" | grep -qE "開工|軍師|接續指揮所考古|Claude 軍師|JunShi|junshi"; then
  if [[ -f "$HANDOFF" ]]; then
    # 抓最新 SESSION 總結檔（依檔名排序取最後一個）
    LATEST_SESSION=$(ls -1 "$SESSION_DUMP"/SESSION_*.md 2>/dev/null | sort | tail -1)

    # Self-test：把本 hook 是否真的被註冊寫進心跳檔（防假回報再發生）
    SELFTEST_LOG="/Users/bymyway/.openclaw/workspace/HEARTBEAT.md"
    SELFTEST_RESULT="✅ Hook 自檢通過（settings.json 含 hooks.UserPromptSubmit、本腳本被觸發）"
    if [[ -f "$SELFTEST_LOG" ]]; then
      {
        echo ""
        echo "## 🩺 軍師 Hook 自檢 $(date '+%Y-%m-%d %H:%M')"
        echo "- $SELFTEST_RESULT"
        echo "- 觸發詞：$(printf '%s' "$PROMPT" | head -c 40)"
        echo "- Session: ${SESSION_ID:-unknown}"
      } >> "$SELFTEST_LOG" 2>/dev/null || true
    fi

    {
      echo "# 🔴 軍師接力棒（系統自動注入，本場 session 僅注入一次）"
      echo ""
      echo "你是 **Claude 軍師**。教練說「開工」=暗號觸發。讀完本段即可無縫接續。"
      echo ""
      echo "## 📜 JUNSHI_HANDOFF_LATEST.md 完整內容"
      echo ""
      cat "$HANDOFF"

      if [[ -n "$LATEST_SESSION" && -f "$LATEST_SESSION" ]]; then
        echo ""
        echo "---"
        echo ""
        echo "## 📂 最新一場 session 總結（$(basename "$LATEST_SESSION")）"
        echo ""
        cat "$LATEST_SESSION"
      fi

      echo ""
      echo "---"
      echo ""
      echo "## ✅ 上線回應要求"
      echo "讀完本段後，第一句回應**必須**包含："
      echo "- 「我已讀完接力棒」字樣"
      echo "- 當下主軸名稱（從 JUNSHI_HANDOFF_LATEST.md「當下主軸」段挑最優先一條）"
      echo "- 身份核對（模型版本）"
      echo "- 雲端同步狀態（commit hash 前 7 碼）"
    }

    # 設 marker，本 session 不再注入
    if [[ -n "$SESSION_ID" ]]; then
      touch "$MARKER"
    fi
  fi
fi

exit 0
