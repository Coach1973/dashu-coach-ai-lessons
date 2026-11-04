#!/bin/bash
# 驗收「網頁交付前自檢」分不分得出好壞（2026-11-04 雲端）：修前要抓到日出段、修後要 0 紅燈。
# 用法：bash cloud_tasks/2026-11-04_page_preflight/test_page_preflight.sh   （本機開 8791，不碰 8765 正式資料）
cd "$(dirname "$0")" || exit 2
PF=../../scripts/page_preflight.js
python3 -m http.server 8791 --bind 127.0.0.1 >/dev/null 2>&1 & SRV=$!
trap 'kill $SRV 2>/dev/null' EXIT
sleep 1
fail=0
out=$(node "$PF" http://127.0.0.1:8791/before_fix.html); code=$?
n=$(printf '%s\n' "$out" | grep -c '痊癒之後.*對比')
if [ "$code" = 1 ] && [ "$n" -ge 1 ]; then echo "✅ 修前：抓到日出段（$n 個寬度）"; else echo "❌ 修前：沒抓到日出段（結束碼 $code）"; fail=1; fi
out=$(node "$PF" http://127.0.0.1:8791/after_fix.html); code=$?
reds=$(printf '%s\n' "$out" | grep -o '[0-9]* 處看不清' | grep -o '^[0-9]*' | paste -sd+ - | bc 2>/dev/null); reds=${reds:-0}
if [ "$reds" -le 3 ] && ! printf '%s\n' "$out" | grep -q '痊癒之後.*對比'; then echo "✅ 修後：紅燈 $reds 處，日出段不在裡面"; else echo "❌ 修後：紅燈 $reds 處"; fail=1; fi
exit $fail
