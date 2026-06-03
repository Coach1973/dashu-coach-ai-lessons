#!/bin/bash
# 終端機對話全自動蒸餾 wrapper
# 1. extract：JSONL → pending_distill/*.txt
# 2. distill：呼叫 LLM 蒸餾 → distill/terminal_YYYY-MM-DD.md
# 3. commit + push
# 軍師建立 2026-06-03

cd /Users/bymyway/.openclaw/workspace || exit 1

echo "===== [run_terminal_distill] $(date +'%Y-%m-%d %H:%M:%S') ====="

# Step 1: extract（無需 LLM）
/opt/homebrew/bin/python3 scripts/extract_terminal_sessions.py >> /tmp/terminal_distill.log 2>&1

# Step 2: distill（呼叫 MiniMax）
/opt/homebrew/bin/python3 scripts/distill_terminal_llm.py >> /tmp/terminal_distill.log 2>&1

# Step 3: commit + push 今日蒸餾產出（如果有變更）
TODAY=$(date +%Y-%m-%d)
TARGET="distill/terminal_${TODAY}.md"

if [ -f "$TARGET" ]; then
    if git diff --quiet "$TARGET" 2>/dev/null && ! git ls-files --error-unmatch "$TARGET" >/dev/null 2>&1; then
        git add "$TARGET"
    elif ! git diff --quiet "$TARGET" 2>/dev/null; then
        git add "$TARGET"
    fi
    if ! git diff --staged --quiet 2>/dev/null; then
        git commit -m "auto: 終端機對話蒸餾 ${TODAY}" >> /tmp/terminal_distill.log 2>&1
        git push origin main >> /tmp/terminal_distill.log 2>&1
        echo "[完成] commit + push ${TARGET}" >> /tmp/terminal_distill.log
    fi
fi
