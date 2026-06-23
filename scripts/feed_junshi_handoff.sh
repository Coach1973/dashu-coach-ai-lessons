#!/bin/bash
# Hook：UserPromptSubmit（Mac 終端機版 v2 · 六步驟全注入）
# 用途：教練喊「開工」時，自動把六步驟內容（接力棒+HEARTBEAT+試金石+memory+knowledges）餵進 context。
# 設計：對應 Windows feed_junshi_handoff.ps1，雙邊邏輯對等。
#       v2 改動（2026-06-23 教練親口「對長期有好處的事不問直接做」）：
#       - 不只注入接力棒，連同 HEARTBEAT/試金石最新 3 案/memory 最新日/knowledges 近 7 天清單全部一次注入
#       - 每場 session 仍只注入一次（marker 防重）；「開工」整句強制重餵
#       - 先 git pull 拉雲端最新（跟 Windows v2 對齊），保證雙邊永遠看同一版
set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
HANDOFF="$WORKSPACE/JUNSHI_HANDOFF_LATEST.md"
SESSION_DUMP="$WORKSPACE/claude-sessions"
HEARTBEAT="$WORKSPACE/HEARTBEAT.md"
STONE="$WORKSPACE/試金石/試金石_案例庫.md"
MEMORY_DIR="$WORKSPACE/memory"
KNOWLEDGES_DIR="$WORKSPACE/knowledges"

INPUT=$(cat)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""')
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""')

MARKER="/tmp/junshi_fed_${SESSION_ID}"

# 「開工」整句 = 強制重餵口令（/clear 後仍可重觸發）
FORCE_REFEED=0
if printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*開工[[:space:]]*$|開工了|開工。|開工！|開工幹活"; then
  FORCE_REFEED=1
fi

# 非強制 + marker 已存在 → 靜默退出
if [[ "$FORCE_REFEED" -eq 0 && -n "$SESSION_ID" && -f "$MARKER" ]]; then
  exit 0
fi

# 觸發詞檢測：整句僅「開」「開工」「工作」「幹活」單一動詞 → 觸發；含「軍師」字眼也觸發
if ! printf '%s' "$PROMPT" | grep -qE "^[[:space:]]*(開|開工|工作|幹活|開始工作)[[:space:]。！!]*$|軍師|接續指揮所|JunShi|junshi"; then
  exit 0
fi

if [[ ! -f "$HANDOFF" ]]; then
  exit 0
fi

# ───────── 🌐 先 git pull 拉雲端最新（跟 Windows v2 對齊）─────────
PULL_STATUS="（本機非 git repo，略過 pull）"
if [[ -d "$WORKSPACE/.git" ]]; then
  cd "$WORKSPACE" || exit 0
  DIRTY=$(git status --porcelain 2>/dev/null)
  STASHED=0
  if [[ -n "$DIRTY" ]]; then
    if git stash push -u -m "auto-pull-stash-$(date +%Y%m%d%H%M%S)" --quiet 2>/dev/null; then
      STASHED=1
    fi
  fi
  if git pull --quiet --rebase 2>/dev/null; then
    HEAD_HASH=$(git rev-parse --short HEAD 2>/dev/null)
    PULL_STATUS="✅ 已拉雲端最新（HEAD: ${HEAD_HASH}）"
  else
    PULL_STATUS="⚠️ Pull 警告：本地有衝突或網路失敗（請手動處理）"
  fi
  if [[ "$STASHED" -eq 1 ]]; then
    git stash pop --quiet 2>/dev/null || true
  fi
fi

# 抓最新 SESSION 總結
LATEST_SESSION=$(ls -1 "$SESSION_DUMP"/SESSION_*.md 2>/dev/null | sort | tail -1)

# Self-test 寫入 HEARTBEAT（防假回報）
if [[ -f "$HEARTBEAT" ]]; then
  {
    echo ""
    echo "## 🩺 軍師 Hook 自檢 $(date '+%Y-%m-%d %H:%M')（Mac v2 六步驟注入）"
    echo "- ✅ Hook 觸發 + 六步驟內容注入完成"
    echo "- 觸發詞：$(printf '%s' "$PROMPT" | head -c 40)"
    echo "- 雲端狀態：${PULL_STATUS}"
    echo "- Session: ${SESSION_ID:-unknown}"
  } >> "$HEARTBEAT" 2>/dev/null || true
fi

# ───────── 注入內容開始 ─────────
{
  echo "# 🔴 軍師接力棒 v2（六步驟全注入，本場 session 僅一次）"
  echo ""
  echo "## 🌐 雲端同步狀態"
  echo ""
  echo "- ${PULL_STATUS}"
  echo "- workspace: \`${WORKSPACE}\`"
  echo ""
  echo "## 🪪 身份硬性告知"
  echo ""
  echo "- **平台**：Mac 終端機（CLI）/ 桌面版 GUI App"
  echo "- **工作目錄**：\`${WORKSPACE}\`（不是 \`~/.openclaw/\`——那只是 OpenClaw 系統運行根目錄）"
  echo "- **身份等級**：軍師（Opus）"
  echo "- **commit 前綴**：\`[Mac]\`（區分 Windows 軍師的 \`[Win]\`）"
  echo "- **稱呼教練**：**大樹教練**"
  echo ""
  echo "🔴 **絕對禁區**：cwd 雖然指向 \`~/.openclaw/\`，但**所有心法/接力棒/試金石/memory 都在 \`workspace/\` 子目錄**。動手前先 \`ls\` 驗證，不可憑 cwd 直覺拼路徑。"
  echo ""
  echo "---"
  echo ""
  echo "教練說「開工/開/工作/幹活」=暗號觸發。讀完本段即可無縫接續。"

  # ───────── 第 1 步：接力棒 ─────────
  echo ""
  echo "## 📜 第 1 步：接力棒（JUNSHI_HANDOFF_LATEST.md 全文）"
  echo ""
  cat "$HANDOFF"

  # ───────── 第 2 步：HEARTBEAT 熱上下文 ─────────
  if [[ -f "$HEARTBEAT" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 🩺 第 2 步：HEARTBEAT.md（最近 50 行熱上下文）"
    echo ""
    tail -50 "$HEARTBEAT"
  fi

  # ───────── 第 3 步：血淚試金石最新 3 案例 ─────────
  if [[ -f "$STONE" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 🔴 第 3 步：血淚試金石最新 3 案例（守則 #07 同處跌倒鐵律）"
    echo ""
    LAST_3_START=$(grep -nE "^## 案例" "$STONE" | tail -3 | head -1 | cut -d: -f1)
    if [[ -n "$LAST_3_START" ]]; then
      tail -n +"$LAST_3_START" "$STONE"
    else
      echo "（無法定位案例段落，請手動查閱 試金石/試金石_案例庫.md）"
    fi
  fi

  # ───────── 第 4 步：knowledges 最近 7 天新檔清單 ─────────
  if [[ -d "$KNOWLEDGES_DIR" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 📚 第 4 步：knowledges/ 最近 7 天新建/修改檔案清單"
    echo ""
    FOUND_KNOWLEDGES=0
    while IFS= read -r f; do
      if [[ -n "$f" ]]; then
        FIRST_LINE=$(head -1 "$f" 2>/dev/null | sed 's/^# //')
        echo "- \`$(basename "$f")\`：${FIRST_LINE}"
        FOUND_KNOWLEDGES=1
      fi
    done < <(find "$KNOWLEDGES_DIR" -maxdepth 1 -type f -name "*.md" -mtime -7 2>/dev/null | sort)
    if [[ "$FOUND_KNOWLEDGES" -eq 0 ]]; then
      echo "（過去 7 天無新檔）"
    fi
  fi

  # ───────── 第 5 步：memory 最新日 ─────────
  if [[ -d "$MEMORY_DIR" ]]; then
    LATEST_MEMORY=$(ls -1 "$MEMORY_DIR"/20[2-9][0-9]-[0-9][0-9]-[0-9][0-9].md 2>/dev/null | sort | tail -1)
    if [[ -n "$LATEST_MEMORY" && -f "$LATEST_MEMORY" ]]; then
      echo ""
      echo "---"
      echo ""
      echo "## 🧠 第 5 步：memory 最新日（$(basename "$LATEST_MEMORY")）"
      echo ""
      cat "$LATEST_MEMORY"
    fi
  fi

  # ───────── 最新一場 SESSION 總結（保留 v1 行為）─────────
  if [[ -n "$LATEST_SESSION" && -f "$LATEST_SESSION" ]]; then
    echo ""
    echo "---"
    echo ""
    echo "## 📂 最新一場 session 總結（$(basename "$LATEST_SESSION")）"
    echo ""
    cat "$LATEST_SESSION"
  fi

  # ───────── 第 6 步：上線回應要求 ─────────
  echo ""
  echo "---"
  echo ""
  echo "## ✅ 第 6 步：上線回應要求"
  echo "讀完本段後，第一句回應**必須**包含："
  echo "- 「我已讀完接力棒」字樣"
  echo "- 當下主軸名稱（從 JUNSHI_HANDOFF_LATEST.md「本棒主軸」段挑最優先一條）"
  echo "- 身份核對（模型版本 + 平台：Mac 終端機/桌面版）"
  echo "- 雲端同步狀態（${PULL_STATUS}）"
  echo "- 詢問教練「今天從哪件事開始？」"
}

# 設 marker，本 session 不再注入
if [[ -n "$SESSION_ID" ]]; then
  touch "$MARKER"
fi

exit 0
