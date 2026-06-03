#!/bin/bash
# Hook：UserPromptSubmit
# 用途：教練說「這個犯過了」時，自動搜尋 Top30_Index.md 對應案例，注入完整 NEC。
#       讓 Top30 試金石對照「不靠模型記得、靠系統強制」。
# 設計：偵測「又犯」「之前犯過」「說過很多次」等關鍵字
#       → 立即去 Top30_Index.md 找對應案例
#       → 注入「#X 案例 + NEC 檢查清單」
#       不命中則靜默退出（避免雜訊）
# 軍師建立 2026-06-04
set -uo pipefail

INPUT=$(cat)
Prompt=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

# 沒有 prompt 就靜默退出
[[ -z "$Prompt" ]] && exit 0

# === Top30 Index 路徑 ===
TOP30_INDEX="$HOME/.claude-code/workspace/Top30_Index.md"

# 找不到檔案就靜默退出
[[ -f "$TOP30_INDEX" ]] || exit 0

# === 觸發詞偵測 ===
TRIGGERED=0

if printf '%s' "$Prompt" | grep -qE "這個犯過|你又犯|又犯了|之前犯過|之前說過|說過很多次|我講過|講過了|提醒過|你又忘|你又問|你又.*犯"; then
  TRIGGERED=1
fi

# 沒有觸發就靜默
[[ $TRIGGERED -eq 0 ]] && exit 0

# === 關鍵字搜尋：根據 prompt 找對應的 Top30 案例 ===
find_matching_case() {
  local input="$1"

  # 模型切換
  if printf '%s' "$input" | grep -qE "模型.*切換|claude-code.json|kimi|\$60"; then
    awk '/^### #1 模型切換失效/,/^### #2 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 路徑搞混
  if printf '%s' "$input" | grep -qE "路徑|agents.*workspace|kong|peipei|身份維修"; then
    awk '/^### #2 三機身份維修/,/^### #3 /' "$TOP30_INDEX" | head -25
    return
  fi

  # distill 腳本
  if printf '%s' "$input" | grep -qE "distill|cron.*腳本|蒸餾.*腳本|腳本不存在"; then
    awk '/^### #3 Distill 腳本/,/^### #4 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 一字不差 / 守則
  if printf '%s' "$input" | grep -qE "守則|一字不差|原文|捏造"; then
    awk '/^### #4 「一字不差」/,/^### #5 /' "$TOP30_INDEX" | head -25
    return
  fi

  # BOOTSTRAP
  if printf '%s' "$input" | grep -qE "BOOTSTRAP|初始化|探索模式|SOUL.md"; then
    awk '/^### #5 BOOTSTRAP/,/^### #6 /' "$TOP30_INDEX" | head -25
    return
  fi

  # Hook
  if printf '%s' "$input" | grep -qE "hook|settings.json.*hook|假完成"; then
    awk '/^### #6 Hook 安裝/,/^### #7 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 接力棒
  if printf '%s' "$input" | grep -qE "接力棒|HANDOFF|新視窗|失憶"; then
    awk '/^### #7 新視窗失憶/,/^### #8 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 30分鐘回報
  if printf '%s' "$input" | grep -qE "30分鐘|回報|報告|HEARTBEAT_OK"; then
    awk '/^### #8 30分鐘回報/,/^### #9 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 身份
  if printf '%s' "$input" | grep -qE "身份|你是誰|幾號機|軍師|小龍蝦"; then
    awk '/^### #9 身份搞混/,/^### #10 /' "$TOP30_INDEX" | head -25
    return
  fi

  # gateway
  if printf '%s' "$input" | grep -qE "gateway|重啟|沒效|改完"; then
    awk '/^### #10 Session 在修改/,/^### #11 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 該問的不問
  if printf '%s' "$input" | grep -qE "幫我|要怎麼做|做嗎|你覺得呢"; then
    awk '/^### #11 該問的不問/,/^### #12 /' "$TOP30_INDEX" | head -25
    return
  fi

  # 預設：列出 Top 5 供教練確認
  awk '/^### #[1-5] / {p=1} p {print} /^### #6 / {p=0; exit}' "$TOP30_INDEX"
}

# === 嘗試根據 prompt 找對應案例 ===
MATCHED_CASE=$(find_matching_case "$Prompt")

# === 輸出 ===
if [[ -n "$MATCHED_CASE" ]]; then
  echo "🏆 Top30 試金石提醒（自動偵測教練說『犯過了』）"
  echo ""
  echo "🎯 偵測到教練說「這個犯過了」→ 系統自動從 Top30_Index.md 找對應案例："
  echo ""
  printf '%s\n' "$MATCHED_CASE"
  echo ""
  echo "💡 完整 30 個案例見：~/.claude-code/workspace/Top30_Index.md"
  echo "📂 詳細版本見：~/.claude-code/workspace/試金石/試金石_*.md"
  echo ""
  echo "（引用前先查 Top30_Index.md 確認一字不差。發現新案例，立即寫入並 commit。）"
fi

exit 0
