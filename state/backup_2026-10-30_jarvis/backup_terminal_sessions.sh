#!/bin/bash
# backup_terminal_sessions.sh — 每 15 分鐘執行
# 用途：把終端機（Claude Code）的對話檔自動備份進工作區，確保上雲、永不只躺本機。
#       解決「教練忘記說『總結上傳』就沒人接」的安全網缺口。
# 原理：複製近 24h 有更新的 .jsonl 到 terminal-notes/raw_sessions/，交給 cron commit+push。
# 注意：這是「原始對話保全」，不是「蒸餾總結」。蒸餾仍需教練說「總結上傳」或另跑 LLM。
# 軍師建立 2026-05-28
set -uo pipefail

SRC="/Users/bymyway/.claude/projects/-Users-bymyway--openclaw"
DST="/Users/bymyway/.openclaw/workspace/terminal-notes/raw_sessions"

mkdir -p "$DST"

# 只備份近 24 小時有更新的對話檔（活躍 session），避免每次掃全部
COUNT=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  cp "$f" "$DST/" 2>/dev/null && COUNT=$((COUNT+1))
done < <(find "$SRC" -maxdepth 1 -name '*.jsonl' -mtime -1 2>/dev/null)

echo "[$(date '+%Y-%m-%d %H:%M')] 備份 $COUNT 個活躍對話檔到 raw_sessions/"
