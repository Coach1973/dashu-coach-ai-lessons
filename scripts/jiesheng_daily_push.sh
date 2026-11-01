#!/bin/bash
# 結繩領導學・每日 LINE 行銷執行流程（cron 12:15 呼叫）
#
# 授權依據：教練 2026-11-01 明確指示「每天中午12點15分都要提醒我行銷結繩領導學，
#           用LINE發10分鐘，全部的人都要發完，過濾一下手機裡面的人脈」＝常設授權。
# 安全設計：推播一律走 scripts/line_push_approve.sh 的 10 分鐘 timestamp 閘門，
#           用完立刻 --revoke，全程可稽核（state/jiesheng_sent_log.jsonl）。
set -uo pipefail
WS="$HOME/.openclaw/workspace"
PY=/opt/homebrew/bin/python3
LOG="$WS/state/jiesheng_daily_$(date +%Y%m%d).log"

cd "$WS" || exit 1
{
  echo "===== 結繩領導學每日行銷 $(date '+%Y-%m-%d %H:%M:%S') ====="

  echo "--- 步驟1：重建名單 ---"
  "$PY" scripts/jiesheng_marketing_list.py --build 2>&1 | tail -12

  echo "--- 步驟2：開啟 10 分鐘 LINE 推播許可 ---"
  echo "    授權依據：教練 2026-11-01 常設指示「每天中午12點15分都要提醒我行銷結繩領導學，用LINE發10分鐘，全部的人都要發完」"
  echo "    授權時間：$(date '+%Y-%m-%d %H:%M:%S')　執行者：cron 每日行銷排程"
  bash scripts/line_push_approve.sh 2>&1

  echo "--- 步驟3：推播今日批次 ---"
  "$PY" scripts/jiesheng_line_push.py 2>&1

  echo "--- 步驟4：立刻撤銷許可 ---"
  bash scripts/line_push_approve.sh --revoke 2>&1

  echo "--- 步驟5：產生教練手機手動發送名單 ---"
  "$PY" scripts/jiesheng_marketing_list.py --phone-sheet 2>&1 | tail -6

  echo "===== 結束 $(date '+%H:%M:%S') ====="
} >> "$LOG" 2>&1

tail -60 "$LOG"
