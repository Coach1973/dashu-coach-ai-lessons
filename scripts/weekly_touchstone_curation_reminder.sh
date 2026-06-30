#!/bin/bash
# 每週日晚上 21:00 提醒：top10_dynamic.md 是否需要策展更新
# 機制：對比「特助場景庫_自動增量.md」近 7 天新增的場景 vs top10_dynamic.md 已有條目
# 軍師方案（守則 #16 簡單為正解）— 教練 2026-06-30 18:53 拍板：軍師決策不請示
set -uo pipefail

WS="/Users/bymyway/.openclaw/workspace"
HEARTBEAT="$WS/HEARTBEAT.md"
TOP10="$WS/distill/top10_dynamic.md"
SCENE="$WS/distill/特助場景庫_自動增量.md"
LOG="/tmp/touchstone_curation_reminder.log"

ts="$(date '+%Y-%m-%d %H:%M')"

# 近 7 天有沒有新場景候選
RECENT_SCENES=0
if [[ -f "$SCENE" ]]; then
    RECENT_SCENES=$(awk '/^## 案例 \[AUTO-/' "$SCENE" 2>/dev/null | tail -50 | wc -l | tr -d ' ')
fi

# top10_dynamic.md 上次更新距今
TOP10_AGE_DAYS=99
if [[ -f "$TOP10" ]]; then
    TOP10_MTIME=$(stat -f %m "$TOP10")
    NOW=$(date +%s)
    TOP10_AGE_DAYS=$(( (NOW - TOP10_MTIME) / 86400 ))
fi

# 條件：距上次策展 > 7 天 + 有新場景候選 → 寫提醒
if (( TOP10_AGE_DAYS > 7 )) && (( RECENT_SCENES > 0 )); then
    REMINDER="
## 🪨 試金石策展提醒 ${ts}
- top10_dynamic.md 已 ${TOP10_AGE_DAYS} 天未更新
- 候選池：特助場景庫_自動增量.md 累積 ${RECENT_SCENES} 個自動場景
- 動作：教練動嘴「策展試金石」→ 軍師讀候選池挑出值得收錄的，升級成 top10_dynamic.md 條目"
    if ! grep -q "試金石策展提醒 $(date '+%Y-%m-%d')" "$HEARTBEAT" 2>/dev/null; then
        echo "$REMINDER" >> "$HEARTBEAT"
        echo "[${ts}] 寫入策展提醒（age=${TOP10_AGE_DAYS}d, scenes=${RECENT_SCENES}）" >> "$LOG"
    fi
else
    echo "[${ts}] no reminder（age=${TOP10_AGE_DAYS}d, scenes=${RECENT_SCENES}）" >> "$LOG"
fi

exit 0
