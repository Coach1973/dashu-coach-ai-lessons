#!/bin/bash
# vps_polling_healthcheck.sh — VPS 小龍蝦（43.245.60.200）polling 健康檢查
#
# 觸發：ai.openclaw.vps-healthcheck.plist（launchd，純 bash，不經過LLM/agent層，
#       所以不會像openclaw agent cron那樣被model_not_found/provider過載打斷）每 15 分鐘執行
# 用途：早於朋友發現 VPS polling 卡住（案例 50，2026-07-14）
# 設計：小龍蝦學長（1號機）
#
# 原理：抓容器內 spool 狀態 + polling log，最後判斷是否卡住，寫結果到
#       state/vps_polling_healthcheck.state.json。
#
# 🔴 2026-07-17 教練要求「自動偵測+自動修復，不要再讓我操心」新增：
#       偵測到「health-monitor restart loop」這個已知模式（見
#       project_openclaw_polling_restart_loop.md 4訊號判斷）時，
#       腳本自己執行docker restart openclaw修復，重新驗證，
#       修好才通知教練（輕量通報，不是求救）；修不好才發原本的求救警報。
#       自動修復有2小時冷卻，避免無限重試同一個修不好的問題洗版。
#
# 憑證：見 ~/.openclaw/workspace/路徑大全_憑證層.md（不硬編碼，從檔案抓）

set -euo pipefail

WS="/Users/bymyway/.openclaw/workspace"
STATE_DIR="$WS/state"
LOG="$STATE_DIR/vps_polling_healthcheck.log"
STATE_FILE="$STATE_DIR/vps_polling_healthcheck.state.json"
LAST_ALERT_FILE="$STATE_DIR/vps_polling_healthcheck.last_alert"
LAST_AUTOFIX_FILE="$STATE_DIR/vps_polling_healthcheck.last_autofix"

mkdir -p "$STATE_DIR"

VPS_IP="43.245.60.200"
SSHPASS_BIN="/opt/homebrew/bin/sshpass"
CREDS_FILE="$WS/路徑大全_憑證層.md"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

write_state() {
    STATUS="$1" ALERT="$2" REASON="$3" SPOOL_COUNT_VALUE="${4:-0}" PROCESSING_COUNT_VALUE="${5:-0}" LAST_INBOUND_VALUE="${6:-}" LAST_INBOUND_AGE_VALUE="${7:-0}" LAST_RESTART_AGE_VALUE="${8:-999999}" CONTAINER_UPTIME_VALUE="${9:-}" \
    python3 - <<'PY'
import json, os

def as_int(name, default=0):
    try:
        return int(str(os.environ.get(name, default)).strip() or default)
    except ValueError:
        return default

data = {
    "ts": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip(),
    "status": os.environ.get("STATUS", "unknown"),
    "alert": os.environ.get("ALERT", "false") == "true",
    "reason": os.environ.get("REASON", ""),
    "spool_count": as_int("SPOOL_COUNT_VALUE"),
    "spool_processing": as_int("PROCESSING_COUNT_VALUE"),
    "last_inbound": os.environ.get("LAST_INBOUND_VALUE", "")[:300],
    "last_inbound_age_minutes": as_int("LAST_INBOUND_AGE_VALUE"),
    "last_restart_age_minutes": as_int("LAST_RESTART_AGE_VALUE", 999999),
    "container_uptime": os.environ.get("CONTAINER_UPTIME_VALUE", ""),
}
with open(os.environ["STATE_FILE"], "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
PY
}
export STATE_FILE

if [ ! -x "$SSHPASS_BIN" ]; then
    log "❌ 找不到 sshpass：$SSHPASS_BIN"
    write_state "ssh_failed" "false" "找不到 sshpass，無法連線 VPS"
    exit 0
fi

if [ ! -f "$CREDS_FILE" ]; then
    log "❌ 找不到憑證層檔案"
    write_state "ssh_failed" "false" "找不到憑證層檔案"
    exit 0
fi

VPS_PASS=$(grep -A 3 "VPS 小龍蝦（對外體驗版）" "$CREDS_FILE" | grep -oE '\`[A-Za-z0-9]{8}\`' | head -1 | tr -d '`')
if [ -z "$VPS_PASS" ]; then
    log "❌ 抓不到 VPS 密碼"
    write_state "ssh_failed" "false" "抓不到 VPS 密碼"
    exit 0
fi

vps_ssh() {
    SSHPASS="$VPS_PASS" "$SSHPASS_BIN" -e ssh -o ConnectTimeout=10 root@"$VPS_IP" "$1" 2>&1
}

safe_int() {
    printf '%s' "${1:-0}" | tr -cd '0-9' | head -c 12
}

NOW=$(date +%s)

SPOOL_RAW=$(vps_ssh "docker exec openclaw sh -c 'ls -la /home/node/.openclaw/telegram/ingress-spool-default/ 2>/dev/null | tail -n +2'" || true)
SPOOL_COUNT=$(echo "$SPOOL_RAW" | grep -c '\.json$' || true)
SPOOL_COUNT=${SPOOL_COUNT:-0}
PROCESSING_COUNT=$(echo "$SPOOL_RAW" | grep -c '\.processing$' || true)
PROCESSING_COUNT=${PROCESSING_COUNT:-0}
SPOOL_NEWEST_NAME=$(echo "$SPOOL_RAW" | awk '{print $NF}' | grep '\.json$' | grep -v '\.processing$' | sort -r | head -1 || true)

SPOOL_STALE_AGE=0
if [ -n "$SPOOL_NEWEST_NAME" ]; then
    SPOOL_NEWEST_EPOCH=$(vps_ssh "docker exec openclaw stat -c %Y /home/node/.openclaw/telegram/ingress-spool-default/$SPOOL_NEWEST_NAME 2>/dev/null" | tr -cd '0-9' || true)
    if [ -n "$SPOOL_NEWEST_EPOCH" ]; then
        SPOOL_STALE_AGE=$((NOW - SPOOL_NEWEST_EPOCH))
    fi
fi

LATEST_LOG=$(vps_ssh "docker exec openclaw sh -c 'ls -t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -1'" | tail -1 || true)
CONTAINER_UPTIME=$(vps_ssh "docker inspect openclaw --format='{{.State.StartedAt}}' 2>/dev/null" | tail -1 || true)

if [ -z "$LATEST_LOG" ] || [ -z "$CONTAINER_UPTIME" ]; then
    log "⚠️ SSH 或 Docker 檢查失敗（VPS 網路問題、容器不存在或 Docker 無回應）"
    write_state "ssh_failed" "false" "無法取得 VPS Docker 狀態，請檢查 VPS 或 openclaw 容器"
    exit 0
fi

LAST_INBOUND=$(vps_ssh "docker exec openclaw sh -c \"grep 'Inbound message' '$LATEST_LOG' 2>/dev/null | tail -1\"" || true)
LAST_RESTART=$(vps_ssh "docker exec openclaw sh -c \"grep 'health-monitor: restarting' '$LATEST_LOG' 2>/dev/null | tail -1\"" || true)

parse_log_age() {
    local line="$1"
    local ts epoch
    ts=$(echo "$line" | grep -oE '"date":"[^"]*"' | head -1 | cut -d'"' -f4 || true)
    if [ -z "$ts" ]; then
        echo 0
        return
    fi
    epoch=$(date -j -u -f "%Y-%m-%dT%H:%M:%S" "${ts:0:19}" "+%s" 2>/dev/null || echo 0)
    if [ "$epoch" -gt 0 ]; then
        echo $((NOW - epoch))
    else
        echo 0
    fi
}

LAST_INBOUND_AGE=0
if [ -n "$LAST_INBOUND" ]; then
    LAST_INBOUND_AGE=$(parse_log_age "$LAST_INBOUND")
fi

LAST_RESTART_AGE=999999
if [ -n "$LAST_RESTART" ]; then
    parsed_restart_age=$(parse_log_age "$LAST_RESTART")
    if [ "$parsed_restart_age" -gt 0 ]; then
        LAST_RESTART_AGE="$parsed_restart_age"
    fi
fi

ALERT=false
ALERT_REASON=""

if [ "$SPOOL_COUNT" -gt 5 ] && [ "$SPOOL_STALE_AGE" -gt 600 ]; then
    ALERT=true
    ALERT_REASON="Spool 堆積 ${SPOOL_COUNT} 條未處理，最新檔 $((SPOOL_STALE_AGE/60)) 分鐘前沒動靜"
fi

if [ "$LAST_RESTART_AGE" -lt 1800 ]; then
    ALERT=true
    REASON_B="最後一次 polling restart 在 $((LAST_RESTART_AGE/60)) 分鐘前（polling 還在反覆重啟 = stale state 卡住）"
    ALERT_REASON="${ALERT_REASON:+$ALERT_REASON；}${REASON_B}"
fi

if [ "$LAST_INBOUND_AGE" -gt 3600 ] && [ "$SPOOL_COUNT" -gt 0 ]; then
    ALERT=true
    REASON_C="最後 inbound $((LAST_INBOUND_AGE/60)) 分鐘前，但 spool 有 ${SPOOL_COUNT} 條沒消化"
    ALERT_REASON="${ALERT_REASON:+$ALERT_REASON；}${REASON_C}"
fi

# 🔴 自動修復判斷：只有「health-monitor restart loop」這個已知模式才自動修，
# 符合 project_openclaw_polling_restart_loop.md 的適用條件（訊號1+訊號2）：
# restart loop 訊號成立 且 spool 沒有堆積（spool堆積是另一種問題，要走.processing SOP，不能亂docker restart）
AUTOFIX_ELIGIBLE=false
if [ "$LAST_RESTART_AGE" -lt 1800 ] && [ "$SPOOL_COUNT" -le 5 ]; then
    AUTOFIX_ELIGIBLE=true
fi

AUTOFIX_COOLDOWN_SECS=7200
AUTOFIX_ATTEMPTED=false
AUTOFIX_SUCCESS=false
if [ "$ALERT" = "true" ] && [ "$AUTOFIX_ELIGIBLE" = "true" ]; then
    AUTOFIX_OK_TO_TRY=true
    if [ -f "$LAST_AUTOFIX_FILE" ]; then
        LAST_AUTOFIX_TS=$(safe_int "$(cat "$LAST_AUTOFIX_FILE" 2>/dev/null || echo 0)")
        LAST_AUTOFIX_TS=${LAST_AUTOFIX_TS:-0}
        if [ $((NOW - LAST_AUTOFIX_TS)) -lt $AUTOFIX_COOLDOWN_SECS ]; then
            AUTOFIX_OK_TO_TRY=false
        fi
    fi

    if [ "$AUTOFIX_OK_TO_TRY" = "true" ]; then
        AUTOFIX_ATTEMPTED=true
        echo "$NOW" > "$LAST_AUTOFIX_FILE"
        log "🔧 偵測到 restart loop 模式（訊號1+2符合），嘗試自動修復：docker restart openclaw"
        vps_ssh "docker restart openclaw" >/dev/null 2>&1 || true
        sleep 20

        POST_LOG=$(vps_ssh "docker logs --tail 60 openclaw 2>&1" || true)
        POST_HEALTHY=$(vps_ssh "docker inspect openclaw --format='{{.State.Health.Status}}' 2>/dev/null" | tail -1 || true)

        if echo "$POST_LOG" | grep -q "isolated polling ingress started" && [ "$POST_HEALTHY" = "healthy" ]; then
            AUTOFIX_SUCCESS=true
            log "✅ 自動修復成功：容器healthy，polling ingress已重新啟動"
        else
            log "❌ 自動修復嘗試後仍未恢復（healthy=$POST_HEALTHY），需要人工介入"
        fi
    else
        log "⏸ 自動修復冷卻中（2小時內已嘗試過，避免對修不好的問題無限重試）"
    fi
fi

COOLDOWN_SECS=3600
SHOULD_ALERT="$ALERT"
if [ "$AUTOFIX_SUCCESS" = "true" ]; then
    SHOULD_ALERT="false"
fi
if [ "$ALERT" = "true" ] && [ "$AUTOFIX_SUCCESS" != "true" ] && [ -f "$LAST_ALERT_FILE" ]; then
    LAST_TS=$(safe_int "$(cat "$LAST_ALERT_FILE" 2>/dev/null || echo 0)")
    LAST_TS=${LAST_TS:-0}
    if [ $((NOW - LAST_TS)) -lt $COOLDOWN_SECS ]; then
        SHOULD_ALERT="false"
    fi
fi

STATUS="ok"
if [ "$SHOULD_ALERT" = "true" ]; then
    STATUS="alert"
elif [ "$AUTOFIX_SUCCESS" = "true" ]; then
    STATUS="auto_fixed"
fi
write_state "$STATUS" "$SHOULD_ALERT" "$ALERT_REASON" "$SPOOL_COUNT" "$PROCESSING_COUNT" "$LAST_INBOUND" "$((LAST_INBOUND_AGE/60))" "$((LAST_RESTART_AGE/60))" "$CONTAINER_UPTIME"

LOCAL_BOT_TOKEN=$(grep -oE '"botToken"[[:space:]]*:[[:space:]]*"[^"]*"' "$HOME/.openclaw/openclaw.json" | head -1 | sed -E 's/.*"([^"]*)"/\1/' || true)
COACH_CHAT_ID="6124913915"

if [ "$AUTOFIX_SUCCESS" = "true" ]; then
    log "📨 發送輕量通報（已自動修復，非求救）"
    FIXED_MSG="🤖【賈維斯自動通知】
🔧 VPS 小龍蝦剛才 polling 卡住，已自動修復

原因：${ALERT_REASON}
處置：自動執行 docker restart openclaw，已確認 polling 恢復正常，不需要您動手

時間：$(date '+%Y-%m-%d %H:%M:%S')"
    if [ -n "$LOCAL_BOT_TOKEN" ]; then
        curl -sS -X POST "https://api.telegram.org/bot${LOCAL_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${COACH_CHAT_ID}" \
            -d "text=${FIXED_MSG}" \
            --max-time 10 > /dev/null 2>&1 && \
            log "✅ Telegram 通報成功" || \
            log "⚠️ Telegram 通報失敗"
    fi
fi

if [ "$SHOULD_ALERT" = "true" ]; then
    log "🚨 ALERT: $ALERT_REASON (spool=$SPOOL_COUNT processing=$PROCESSING_COUNT)"
    echo "$NOW" > "$LAST_ALERT_FILE"

    if [ "$AUTOFIX_ATTEMPTED" = "true" ]; then
        AUTOFIX_NOTE="⚠️ 已嘗試自動修復（docker restart openclaw）但沒有恢復，需要您協助查看。"
    elif [ "$AUTOFIX_ELIGIBLE" = "true" ]; then
        AUTOFIX_NOTE="（自動修復冷卻中，2小時內已試過一次未成功）"
    else
        AUTOFIX_NOTE="這個症狀不符合已知的自動修復條件（可能是 spool 堆積類問題，需要不同的排查方式）。"
    fi

    ALERT_MSG="🤖【賈維斯自動通知】
🚨 VPS 小龍蝦（對外體驗版）polling 異常！

原因：${ALERT_REASON}

狀態：
• Spool 待處理：${SPOOL_COUNT} 條（${PROCESSING_COUNT} 個 processing）
• 容器啟動時間：$(echo "$CONTAINER_UPTIME" | head -c 19)

${AUTOFIX_NOTE}

建議處置：
sshpass -p '<路徑大全_憑證層.md查密碼>' ssh root@43.245.60.200 'docker restart openclaw'（詳見 project_openclaw_polling_restart_loop.md，不要用 openclaw gateway restart，容器內沒 systemd 會踩坑）

警報時間：$(date '+%Y-%m-%d %H:%M:%S')"

    if [ -n "$LOCAL_BOT_TOKEN" ]; then
        curl -sS -X POST "https://api.telegram.org/bot${LOCAL_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${COACH_CHAT_ID}" \
            -d "text=${ALERT_MSG}" \
            --max-time 10 > /dev/null 2>&1 && \
            log "✅ Telegram 推送成功" || \
            log "⚠️ Telegram 推送失敗"
    else
        log "⚠️ 抓不到本地 bot token，無法推 Telegram"
    fi
elif [ "$ALERT" = "true" ]; then
    log "⚠️ 冷卻中（60 分鐘內已 alert 過）：$ALERT_REASON"
else
    log "✅ OK: spool=$SPOOL_COUNT processing=$PROCESSING_COUNT last_inbound_age=$((LAST_INBOUND_AGE/60))m last_restart_age=$((LAST_RESTART_AGE/60))m"
fi

tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
