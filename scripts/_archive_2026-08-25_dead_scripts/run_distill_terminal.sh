#!/bin/bash
# run_distill_terminal.sh — 終端機對話全自動蒸餾 wrapper
# 流程：提取教練原話 → LLM 蒸餾 → git commit push
# cron 每 2 小時跑一次
# 軍師建立 2026-05-30
set -uo pipefail

WORKSPACE="/Users/bymyway/.openclaw/workspace"
LOG="/tmp/distill_terminal.log"

echo "[$(date '+%Y-%m-%d %H:%M')] === 開始終端機蒸餾 ===" >> "$LOG"

# 第一步：提取教練原話到 pending_distill/
/usr/bin/python3 "$WORKSPACE/scripts/extract_terminal_sessions.py" >> "$LOG" 2>&1

# 第二步：LLM 蒸餾
/usr/bin/python3 "$WORKSPACE/scripts/distill_terminal_llm.py" >> "$LOG" 2>&1

# 第三步：git commit push（只在有變動時）
cd "$WORKSPACE"
git add distill/terminal_*.md terminal-notes/distilled/ terminal-notes/.distill_llm_state.json terminal-notes/.extract_state.json 2>/dev/null

if git diff --cached --quiet 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M')] 無新蒸餾內容，跳過 commit" >> "$LOG"
else
    git commit -m "auto: 終端機對話蒸餾 $(date '+%H:%M')" >> "$LOG" 2>&1
    git push origin main >> "$LOG" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M')] ✅ 蒸餾 commit + push 完成" >> "$LOG"
fi
