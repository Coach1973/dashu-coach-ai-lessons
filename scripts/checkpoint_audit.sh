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
    # 2026-08-25 賈維斯體檢：原本只寫 log 沒人看，等於這道防線從來沒真的示警過。
    # 門檻刻意設高（超過 3 小時沒存雲端才講），正常每小時自動 commit 的情況完全不會觸發，
    # 避免變成教練罵過的「不影響工作卻一直吵」的假警報。
    if [ "$AGE_MINUTES" -gt 180 ]; then
        /Users/bymyway/.openclaw/workspace/scripts/notify_coach.sh "⚠️ 有資料超過 3 小時沒備份到雲端

目前有 $UNCOMMITTED 個檔案還沒存上雲端，
上一次成功備份是 $((AGE_MINUTES / 60)) 小時前。

正常情況每小時會自動備份一次，超過 3 小時代表自動備份可能卡住了。
跟軍師說一聲，我來查。" 21600 checkpoint_stale
    fi
else
    echo "[$(date '+%H:%M')] ✅ 無未 commit 檔案" >> /tmp/checkpoint_audit.log
fi

echo "✅ checkpoint_audit 完成：$UNCOMMITTED 未commit，$AGE_MINUTES 分鐘前"
