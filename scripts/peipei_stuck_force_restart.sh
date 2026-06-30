#!/bin/bash
# peipei channel-stop bug 自動偵測 + force-restart（教練 2026-06-30 18:38 親口
# 「找到問題就要解決問題，不然為什麼要同意 Bug 的存在呢？又不是修不了。」）
#
# 背景：OpenClaw 2026.6.1 在 peipei bot 遇 Telegram Bad Gateway 時，
#       internal channel-stop 卡住沒響應，等內部 9 小時 timeout 才放行。
#       連續 6 天（6/25–6/30）每天上午 9:12 都中招。
# 對策：每 5 分鐘檢查；發現 peipei stopped 累計 > 15 分鐘 + 同期沒 inbound
#       → kickstart 整個 gateway（中斷 1–2 分鐘 < 9 小時失聯）
# 節流：1 小時內最多 restart 一次，避免反覆暴打
set -uo pipefail

LOG="/tmp/peipei_stuck_monitor.log"
LOCK="/tmp/peipei_force_restart.lock"   # 1 小時節流
GATEWAY_LOG="$HOME/Library/Logs/openclaw/gateway.log"
HEARTBEAT="$HOME/.openclaw/workspace/HEARTBEAT.md"

ts() { date '+%Y-%m-%d %H:%M:%S'; }

# 節流檢查
if [[ -f "$LOCK" ]]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$LOCK") ))
    if (( AGE < 3600 )); then
        exit 0   # 安靜退出
    fi
fi

[[ ! -f "$GATEWAY_LOG" ]] && exit 0

# 條件 1：最近 15 分鐘是否看到 "restarting (reason: stopped)" for bot_peipei
NOW_MIN=$(date '+%H:%M' | awk -F: '{print $1*60+$2}')
RECENT_STOPPED=0
while read -r line; do
    LOG_MIN=$(echo "$line" | grep -oE '^2026-[0-9-]+T([0-9]{2}):([0-9]{2})' | awk -F'[T:]' '{print $2*60+$3}')
    if [[ -n "$LOG_MIN" ]]; then
        DIFF=$(( NOW_MIN - LOG_MIN ))
        (( DIFF < 0 )) && DIFF=$(( DIFF + 1440 ))
        if (( DIFF <= 20 )); then
            RECENT_STOPPED=1
            break
        fi
    fi
done < <(grep "bot_peipei.*restarting (reason: stopped)" "$GATEWAY_LOG" | tail -5)

# 條件 2：最近 15 分鐘 peipei 沒收到任何 Inbound message
RECENT_INBOUND=0
while read -r line; do
    LOG_MIN=$(echo "$line" | grep -oE '^2026-[0-9-]+T([0-9]{2}):([0-9]{2})' | awk -F'[T:]' '{print $2*60+$3}')
    if [[ -n "$LOG_MIN" ]]; then
        DIFF=$(( NOW_MIN - LOG_MIN ))
        (( DIFF < 0 )) && DIFF=$(( DIFF + 1440 ))
        if (( DIFF <= 15 )); then
            RECENT_INBOUND=1
            break
        fi
    fi
done < <(grep -E "Inbound message.*@coachwu_lenovo_bot" "$GATEWAY_LOG" | tail -3)

# 判定：stopped 訊號出現 + 沒 inbound → 卡住
if (( RECENT_STOPPED == 1 && RECENT_INBOUND == 0 )); then
    echo "[$(ts)] DETECTED stuck: stopped=1 inbound=0 → kickstarting gateway" >> "$LOG"
    {
        echo ""
        echo "## ⚠️ peipei 自動 force-restart $(ts)"
        echo "- 偵測條件：最近 20 分鐘 stopped 訊號 + 最近 15 分鐘無 inbound"
        echo "- 動作：launchctl kickstart -k ai.openclaw.gateway（節流 1 小時）"
    } >> "$HEARTBEAT"
    launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway" 2>>"$LOG"
    touch "$LOCK"
    sleep 5
    if launchctl list | grep -q ai.openclaw.gateway; then
        echo "[$(ts)] kickstart OK, gateway re-loaded" >> "$LOG"
    else
        echo "[$(ts)] kickstart FAILED, gateway 未重啟" >> "$LOG"
    fi
else
    echo "[$(ts)] healthy: stopped=$RECENT_STOPPED inbound=$RECENT_INBOUND" >> "$LOG"
fi

exit 0
