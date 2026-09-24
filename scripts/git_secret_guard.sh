#!/bin/bash
# git_secret_guard.sh — 提交前自動攔截金鑰，裝成兩個 repo 的 pre-commit hook
#
# 建立原因（2026-08-25 賈維斯體檢，當場踩到）：
#   軍師在納管檔案時「有做金鑰掃描」，掃出 2 個，但因為掃描跟 commit 寫在同一串指令裡，
#   掃描結果只是印出來、沒有阻斷，token 照樣被 commit + push 出去。
#   教訓：檢查如果不能擋，就只是「提醒自己記得看」，等同沒有防呆。
#   （對應教練鐵律：防呆必須是機關，不能是 opt-in 的規矩）
#
# 行為：發現疑似金鑰 → 直接擋下 commit（exit 1），並指出檔案與行號。
#      真的需要放行時：git commit --no-verify

set -uo pipefail

PATTERNS='([0-9]{9,10}:AA[A-Za-z0-9_-]{30,}|sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|nfp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|ghp_[A-Za-z0-9]{30,}|AIza[A-Za-z0-9_-]{30,})'

# 只檢查這次要提交的內容，不掃整個 repo
FILES=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$FILES" ] && exit 0

HITS=""
while IFS= read -r f; do
    [ -f "$f" ] || continue
    # openclaw.json 是既有設計（私有 repo 內備份設定含 token），不在本檢查範圍
    case "$f" in
        openclaw.json|*/openclaw.json|*.bak*|*credentials*) continue ;;
        # 對話逐字備份：內容是教練與 AI 講過的話，不可控（提到什麼就記什麼），
        # 且由每 15 分鐘的自動備份 cron 提交——擋住它會讓整個備份系統卡死，
        # 那比「私有 repo 裡有一組歷史 token」嚴重得多。
        # 治本方式是不讓 token 出現在對話裡（＝腳本不要硬編碼），已於同日全數改掉。
        terminal-notes/*|*/terminal-notes/*|*.jsonl) continue ;;
    esac
    m=$(git show ":$f" 2>/dev/null | grep -nEo "$PATTERNS" | head -3)
    if [ -n "$m" ]; then
        HITS="${HITS}\n  🔴 $f"
        while IFS= read -r line; do
            # 只顯示前 12 碼，不把完整金鑰印在終端機上
            HITS="${HITS}\n       第 $(echo "$line" | cut -d: -f1) 行：$(echo "$line" | cut -d: -f2- | cut -c1-12)…（已截斷）"
        done <<< "$m"
    fi
done <<< "$FILES"

if [ -n "$HITS" ]; then
    echo ""
    echo "🚫 提交被擋下：偵測到疑似金鑰／Token"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "$HITS"
    echo ""
    echo "📜 執行細則 N8 記憶鐵律：寫進版控前先過敏感資料檢查，"
    echo "   命中就先遮蔽或抽到權限受限的獨立檔案，不能靠「反正之後會發現」。"
    echo ""
    echo "✅ 正確做法："
    echo "   1. 把金鑰改成從設定檔讀取（參考 scripts/notify_coach.sh 的寫法）"
    echo "   2. 或抽到 credentials/ 底下（該目錄已在 .gitignore）"
    echo "   3. 確定是誤判才用：git commit --no-verify"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi

exit 0
