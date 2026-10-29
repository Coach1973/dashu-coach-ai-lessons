#!/bin/bash
# Hook：UserPromptSubmit（2026-10-30 教練拍板：逐字存檔改事件觸發，教練說話當下就存）
# 背景跑 recall.py --harvest-now：等 20 秒讓這句寫進對話檔、收進逐字保險箱、15 分鐘內沒收到就推播。
# 一律放行：不讀輸入、不輸出、馬上結束，壞了也不會擋住教練說話（10/16 擋 3.5 小時的教訓）。
cat >/dev/null
f=/Users/bymyway/.openclaw/workspace/scripts/recall.py
[ -f "$f" ] && nohup /usr/bin/python3 "$f" --harvest-now 終端機 >>/tmp/recall_now.log 2>&1 </dev/null &
exit 0
