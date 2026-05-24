#!/bin/bash
# checkpoint_audit.sh — 每 15 分鐘檢查 workspace 是否有未 commit 的檔案
# 觸發：系統 crontab（每 15 分鐘）
# 用途：確保 15 分鐘內一定有人 commit，防止「說了沒做」
# 設計：軍師，2026-05-24

WS="/Users/bymyway/.openclaw/workspace"
cd "$WS" || exit 1

UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
LAST_COMMIT_TIME=$(git log -1 --format='%at' 2>/dev/null || echo 0)
NOW=$(date +%s)
AGE_MINUTES=$(( (NOW - LAST_COMMIT_TIME) / 60 ))

if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "[$(date '+%H:%M')] ⚠️ 未 commit：$UNCOMMITTED 個檔案，上次 commit 是 $AGE_MINUTES 分鐘前" >> /tmp/checkpoint_audit.log
else
    echo "[$(date '+%H:%M')] ✅ 無未 commit 檔案" >> /tmp/checkpoint_audit.log
fi

echo "✅ checkpoint_audit 完成：$UNCOMMITTED 未commit，$AGE_MINUTES 分鐘前"
