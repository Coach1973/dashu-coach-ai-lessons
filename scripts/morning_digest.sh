#!/bin/bash
# morning_digest.sh
# 用途：每天早上 06:00 跑，掃前 12 小時（昨晚 18:00 到今早 06:00）的 git commits
#      過濾掉純 auto-backup 雜訊，把「值得教練知道的工作」摘要成 5-10 行
#      沒事（純備份）就安靜輸出空字串，cron 不會發通知
# 建立：2026-06-05（教練睡 10 小時沒看到報告，要求補上「凌晨自動摘要」機制）
# 下次升級時如需改語法，只動這支腳本，不動 cron

set -e

cd /Users/bymyway/.openclaw/workspace

# === 取時間範圍（macOS 用 -v，Linux 用 -d）===
TS=$(date '+%Y-%m-%d %H:%M')
if date -v-12H '+%Y-%m-%d %H:%M' >/dev/null 2>&1; then
    SINCE=$(date -v-12H '+%Y-%m-%d %H:%M')
else
    SINCE=$(date -d '12 hours ago' '+%Y-%m-%d %H:%M')
fi

# === 抓前 12 小時的所有 commit（不含 merge）===
COMMITS=$(git log --since="$SINCE" --no-merges --pretty=format:"%h|%s|%an" 2>/dev/null)
TOTAL=$(echo "$COMMITS" | grep -c "|" 2>/dev/null || echo 0)
TOTAL=${TOTAL:-0}

if [ "$TOTAL" = "0" ]; then
    # 沒任何 commit，安靜
    exit 0
fi

# === 分類：過濾純備份 ===
# 自動備份類型：auto-backup、[auto] 對話記錄、auto: 接力棒/蒸餾/狀態 等系統自動運作
BACKUP_COUNT=$(echo "$COMMITS" | grep -cE "auto-backup|\[auto\]|auto:" || true)
BACKUP_COUNT=${BACKUP_COUNT:-0}
NOTABLE=$(echo "$COMMITS" | grep -vE "auto-backup|\[auto\]|auto:" | head -8)
NOTABLE_COUNT=$(echo "$NOTABLE" | grep -c "|" 2>/dev/null || echo 0)
NOTABLE_COUNT=${NOTABLE_COUNT:-0}

if [ "$NOTABLE_COUNT" = "0" ]; then
    # 全部都是 auto-backup，安靜
    exit 0
fi

# === 產出摘要 ===
cat <<EOF
☀️ 早安，教練。$TS 起床摘要

過去 12 小時（$SINCE 起）共 $TOTAL 個 commit
其中 $BACKUP_COUNT 個是純自動備份（略過）
$NOTABLE_COUNT 個值得您看一下：

EOF

echo "$NOTABLE" | while IFS='|' read -r hash msg author; do
    [ -z "$hash" ] && continue
    echo "• \`$hash\` $msg"
done

cat <<EOF

💡 看完整 log：\`cd ~/.openclaw/workspace && git log --since="$SINCE"\`
EOF
