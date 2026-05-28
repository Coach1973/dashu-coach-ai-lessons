#!/bin/bash
# split_memory.sh — 今日記憶檔自動分割（活躍檔達門檻就滾動，永遠保持輕量）
# 觸發：Mac crontab 每 30 分鐘
# 設計：軍師 Opus 4.7，2026-05-28
# 起因：distill_incremental.js 只會在 80K「警告」、不會真的拆，沒人手動拆 → 自動化補洞。
#       對應使命「老闆動嘴，AI 自動執行」：教練不用再被問「要不要拆」。
#
# 為什麼只處理「今日檔」：只有今日檔在持續增長、被讀最多次。歷史檔已靜態，
#   把它「滾動」只是改名字＋加空殼，那一大坨內容還擠在一個檔，並沒有變輕——
#   所以對歷史檔做滾動沒意義。要保持輕量，只需在今日檔成長過頭時滾動。
#
# 滾動邏輯：今日檔超過門檻 → 整本內容搬到 _pN.md（保留全部），
#   再開一本乾淨的活躍檔（之後的對話寫進這本）。內容一字不刪。

set -u
WS="/Users/bymyway/.openclaw/workspace"
MEM_DIR="$WS/memory"
THRESHOLD_KB=150          # ← 門檻。教練要改成 200 就改這一個數字
LOG="$WS/split_memory.log"
TS=$(date '+%Y-%m-%d %H:%M:%S')

# 今日日期（台灣時間 UTC+8，與 distill_incremental.js 一致，避免凌晨差一天）
TODAY=$(TZ='Asia/Taipei' date '+%Y-%m-%d')
f="$MEM_DIR/$TODAY.md"

if [ ! -f "$f" ]; then
  echo "[$TS] 今日（$TODAY）無記憶檔，跳過" >> "$LOG"
  exit 0
fi

size_kb=$(( $(stat -f%z "$f") / 1024 ))
if [ "$size_kb" -le "$THRESHOLD_KB" ]; then
  echo "[$TS] $TODAY ${size_kb}KB 未達門檻 ${THRESHOLD_KB}KB，不分割" >> "$LOG"
  exit 0
fi

# === 滾動分割 ===
base="$TODAY"
n=1
while [ -e "$MEM_DIR/${base}_p${n}.md" ]; do n=$((n+1)); done
archive="$MEM_DIR/${base}_p${n}.md"

mv "$f" "$archive"
cat > "$f" <<EOF
# 記憶檔 ${base}（續・自動分割第 $((n+1)) 段）

> 本日較早內容已自動歸檔，依序見：${base}_p1.md 起算到 ${base}_p${n}.md
> 自動分割：${TS}（達 ${size_kb}KB，門檻 ${THRESHOLD_KB}KB）
> 內容一字未刪，只是分本，方便快速讀取、省 AI 讀取量。

EOF

echo "[$TS] 分割 $base：${size_kb}KB → 歸檔 ${base}_p${n}.md，新開活躍檔" >> "$LOG"

git -C "$WS" add "memory/${base}.md" "memory/${base}_p${n}.md" >> "$LOG" 2>&1
git -C "$WS" commit -m "auto: 今日記憶檔自動分割 ${base}（${size_kb}KB→_p${n}，內容全保留）" >> "$LOG" 2>&1
if git -C "$WS" push origin main >> "$LOG" 2>&1; then
  echo "[$TS] push 成功" >> "$LOG"
else
  echo "[$TS] push 失敗，留待下次（commit 已在本地）" >> "$LOG"
fi
