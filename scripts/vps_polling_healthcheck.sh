#!/bin/bash
# vps_polling_healthcheck.sh — VPS 小龍蝦（43.245.60.200）polling 健康檢查
#
# 觸發：OpenClaw cron「vps_polling_healthcheck」每 15 分鐘
# 用途：早於朋友發現 VPS polling 卡住（案例 50，2026-07-14）
# 設計：小龍蝦學長（1號機）
#
# 原理：抓容器內 spool 狀態 + polling log，最後判斷是否卡住，寫結果到
#       state/vps_polling_healthcheck.state.json。OpenClaw cron agent 讀這個檔
#       後決定要不要推 Telegram 給教練。
#
# 憑證：見 ~/.openclaw/workspace/路徑大全_憑證層.md（不硬編碼，從檔案抓）

set -e

WS="/Users/bymyway/.openclaw/workspace"
STATE_DIR="$WS/state"
LOG="$STATE_DIR/vps_polling_healthcheck.log"
STATE_FILE="$STATE_DIR/vps_polling_healthcheck.state.json"
LAST_ALERT_FILE="$STATE_DIR/vps_polling_healthcheck.last_alert"

mkdir -p "$STATE_DIR"

VPS_IP="43.245.60.200"
SSHPASS_BIN="/opt/homebrew/bin/sshpass"
# 用 plain 密碼 + sshpass，不加 BatchMode=yes（會擋掉 sshpass 互動式輸入）
SSH_BASE=("$SSHPASS_BIN" "-p" "PLACEHOLDER_PASS" "ssh" "-o" "StrictHostKeyChecking=no" "-o" "ConnectTimeout=10" "root@$VPS_IP")

# === 從憑證層讀 VPS 密碼（不硬編碼）===
CREDS_FILE="$WS/路徑大全_憑證層.md"
if [ ! -f "$CREDS_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 找不到憑證層檔案" >> "$LOG"
    exit 1
fi
VPS_PASS=$(grep -A 3 "VPS 小龍蝦（對外體驗版）" "$CREDS_FILE" | grep -oE '\`[A-Za-z0-9]{8}\`' | head -1 | tr -d '`')
if [ -z "$VPS_PASS" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 抓不到 VPS 密碼" >> "$LOG"
    exit 1
fi

# === 建立 sshpass 呼叫函式 ===
# 用法：vps_ssh "指令1; 指令2; ..."
vps_ssh() {
    SSHPASS="$VPS_PASS" "$SSHPASS_BIN" -e ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@"$VPS_IP" "$1" 2>&1
}

# 容器內 log 路徑（在 /tmp/openclaw/ 內，主機端沒掛載出來）
CONTAINER_LOG_DIR="/tmp/openclaw"

# === 抓 VPS 內部資料（拆分多次呼叫避免 escaping）===

# 1. Spool 統計（主機端直接讀 docker volume）
SPOOL_RAW=$(vps_ssh "ls -la /home/node/.openclaw/telegram/ingress-spool-default/ 2>/dev/null | tail -n +2")
if [ -z "$SPOOL_RAW" ]; then
    # 主機端讀不到 → 改走容器內讀
    SPOOL_RAW=$(vps_ssh "docker exec openclaw sh -c 'ls -la /home/node/.openclaw/telegram/ingress-spool-default/ 2>/dev/null | tail -n +2'")
fi
SPOOL_COUNT=$(echo "$SPOOL_RAW" | grep -c '\.json$' || echo 0)
SPOOL_NEWEST_NAME=$(echo "$SPOOL_RAW" | awk '{print $NF}' | grep '\.json$' | grep -v '\.processing$' | sort -r | head -1)
SPOOL_NEWEST_MTIME=$(echo "$SPOOL_RAW" | grep -F "$SPOOL_NEWEST_NAME" | awk '{print $6, $7, $8}')
PROCESSING_COUNT=$(echo "$SPOOL_RAW" | grep -c '\.processing$' || echo 0)

# 2. Spool 最新檔 mtime（轉成 epoch）
SPOOL_NEWEST_EPOCH=0
if [ -n "$SPOOL_NEWEST_NAME" ] && [ -n "$SPOOL_NEWEST_MTIME" ]; then
    # ls 格式：-rw------- 1 node node 1087 Jul 14 16:50 0000000653493278.json
    # 取月份 + 日 + 時間，組合今年（假設 VPS UTC）
    SPOOL_NEWEST_EPOCH=$(vps_ssh "stat -c %Y /home/node/.openclaw/telegram/ingress-spool-default/$SPOOL_NEWEST_NAME 2>/dev/null" | tr -d ' \n')
    SPOOL_NEWEST_EPOCH=${SPOOL_NEWEST_EPOCH:-0}
fi

# 3. 容器 log 統計（容器內 /tmp/openclaw/，主機端沒掛載）
#    用 docker exec 讀，要包成簡單指令避免 escaping 出錯
LATEST_LOG=$(vps_ssh "docker exec openclaw sh -c 'ls -t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -1'")
if [ -z "$LATEST_LOG" ]; then
    LATEST_LOG="/tmp/openclaw/openclaw-2026-07-14.log"
fi
LAST_INBOUND=$(vps_ssh "docker exec openclaw sh -c 'grep -h Inbound-message $LATEST_LOG 2>/dev/null | tail -1'" 2>/dev/null || echo "")
# 注意：上面用 "Inbound-message" 是錯的，正確應該是 "Inbound message"（有空格的字串）
# 改寫：
LAST_INBOUND=$(vps_ssh "docker exec openclaw sh -c \"grep 'Inbound message' $LATEST_LOG 2>/dev/null | tail -1\"")
RESTARTS_5=$(vps_ssh "docker exec openclaw sh -c \"grep 'health-monitor: restarting' $LATEST_LOG 2>/dev/null | tail -5 | wc -l\"")
RESTARTS_5=$(echo "$RESTARTS_5" | tr -d ' \n')
CONTAINER_UPTIME=$(vps_ssh "docker inspect openclaw --format='{{.State.StartedAt}}' 2>/dev/null")

# === 健全性檢查（如果什麼都沒抓到 = SSH 失敗）===
if [ -z "$LATEST_LOG" ] || [ -z "$CONTAINER_UPTIME" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ SSH 連不上 VPS（網路問題或 VPS 死機）" >> "$LOG"
    cat > "$STATE_FILE" <<EOF
{
  "ts": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "ssh_failed",
  "alert": false,
  "reason": "無法 SSH 到 VPS，請檢查 VPS 是否活著或網路是否通"
}
EOF
    exit 0
fi

# === 判斷 alert ===
NOW=$(date +%s)
ALERT_REASON=""
ALERT=false

# Trigger A：spool 堆積且最新檔 mtime 距今 > 10 分鐘
SPOOL_STALE_AGE=0
if [ "${SPOOL_NEWEST_EPOCH:-0}" -gt 0 ]; then
    SPOOL_STALE_AGE=$((NOW - SPOOL_NEWEST_EPOCH))
fi

if [ "${SPOOL_COUNT:-0}" -gt 5 ] && [ "${SPOOL_STALE_AGE:-0}" -gt 600 ]; then
    ALERT=true
    ALERT_REASON="Spool 堆積 ${SPOOL_COUNT} 條未處理，最新檔 $((SPOOL_STALE_AGE/60)) 分鐘前沒動靜"
fi

# Trigger B：最後一次 health-monitor restart 距今 < 30 分鐘（最近還在反覆 restart = stale state 卡住）
LAST_RESTART=$(vps_ssh "docker exec openclaw sh -c \"grep 'health-monitor: restarting' $LATEST_LOG 2>/dev/null | tail -1\"")
LAST_RESTART_AGE=999999
if [ -n "$LAST_RESTART" ]; then
    LAST_RESTART_TS=$(echo "$LAST_RESTART" | grep -oE '"date":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ -n "$LAST_RESTART_TS" ]; then
        LAST_RESTART_EPOCH=$(date -j -u -f "%Y-%m-%dT%H:%M:%S" "${LAST_RESTART_TS:0:19}" "+%s" 2>/dev/null || echo 0)
        if [ "$LAST_RESTART_EPOCH" -gt 0 ]; then
            LAST_RESTART_AGE=$((NOW - LAST_RESTART_EPOCH))
        fi
    fi
fi

if [ "${LAST_RESTART_AGE:-999999}" -lt 1800 ]; then
    ALERT=true
    REASON_B="最後一次 polling restart 在 $((LAST_RESTART_AGE/60)) 分鐘前（polling 還在反覆重啟 = stale state 卡住）"
    ALERT_REASON="${ALERT_REASON:+$ALERT_REASON；}${REASON_B}"
fi

# Trigger C：最後 inbound 距今 > 60 分鐘 且 spool > 0
LAST_INBOUND_AGE=0
if [ -n "$LAST_INBOUND" ]; then
    LAST_INBOUND_TS=$(echo "$LAST_INBOUND" | grep -oE '"date":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [ -n "$LAST_INBOUND_TS" ]; then
        LAST_INBOUND_EPOCH=$(date -j -u -f "%Y-%m-%dT%H:%M:%S" "${LAST_INBOUND_TS:0:19}" "+%s" 2>/dev/null || echo 0)
        if [ "$LAST_INBOUND_EPOCH" -gt 0 ]; then
            LAST_INBOUND_AGE=$((NOW - LAST_INBOUND_EPOCH))
        fi
    fi
fi

if [ "${LAST_INBOUND_AGE:-0}" -gt 3600 ] && [ "${SPOOL_COUNT:-0}" -gt 0 ]; then
    ALERT=true
    REASON_C="最後 inbound $((LAST_INBOUND_AGE/60)) 分鐘前，但 spool 有 ${SPOOL_COUNT} 條沒消化"
    ALERT_REASON="${ALERT_REASON:+$ALERT_REASON；}${REASON_C}"
fi

# === 冷卻檢查（60 分鐘內不重複 alert）===
COOLDOWN_SECS=3600
SHOULD_ALERT="$ALERT"
if [ "$ALERT" = "true" ] && [ -f "$LAST_ALERT_FILE" ]; then
    LAST_TS=$(cat "$LAST_ALERT_FILE" 2>/dev/null || echo 0)
    if [ $((NOW - LAST_TS)) -lt $COOLDOWN_SECS ]; then
        SHOULD_ALERT="false"
    fi
fi

# === 寫 state 檔（給 OpenClaw agent 讀）===
# 用 Python 寫確保 JSON 正確 escape（last_inbound 含雙引號）
python3 -c "
import json, sys
data = {
    'ts': '$(date -u +%Y-%m-%dT%H:%M:%SZ)',
    'status': 'alert' if '$SHOULD_ALERT' == 'true' else 'ok',
    'alert': '$SHOULD_ALERT' == 'true',
    'reason': '''$ALERT_REASON''',
    'spool_count': int('${SPOOL_COUNT:-0}'),
    'spool_processing': int('${PROCESSING_COUNT:-0}'),
    'spool_stale_minutes': $((SPOOL_STALE_AGE/60)),
    'last_inbound': '''$(echo "$LAST_INBOUND" | head -c 300)'''[:300],
    'last_inbound_age_minutes': $((LAST_INBOUND_AGE/60)),
    'last_restart_age_minutes': $((LAST_RESTART_AGE/60)),
    'container_uptime': '''$CONTAINER_UPTIME'''
}
with open('$STATE_FILE', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
"

# === 寫日誌 ===
if [ "$SHOULD_ALERT" = "true" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🚨 ALERT: $ALERT_REASON (spool=$SPOOL_COUNT processing=$PROCESSING_COUNT)" >> "$LOG"
    echo "$NOW" > "$LAST_ALERT_FILE"

    # === 推 Telegram 給教練（用本地 Mac 小龍蝦 bot token）===
    LOCAL_BOT_TOKEN=$(grep -oE '"botToken"[[:space:]]*:[[:space:]]*"[^"]*"' "$HOME/.openclaw/openclaw.json" | head -1 | sed -E 's/.*"([^"]*)"/\1/')
    COACH_CHAT_ID="6124913915"
    ALERT_MSG="🚨 VPS 小龍蝦（對外體驗版）polling 異常！

原因：${ALERT_REASON}

📊 狀態：
• Spool 待處理：${SPOOL_COUNT} 條（${PROCESSING_COUNT} 個 processing）
• 容器已运行：$(echo "$CONTAINER_UPTIME" | head -c 19)

💡 建議处置：
\`openclaw gateway restart\` 會自動觸發 state-migrations 清理 stale state（詳見試金石案例 50）

⏰ 警報時間：$(date '+%Y-%m-%d %H:%M:%S')"

    if [ -n "$LOCAL_BOT_TOKEN" ]; then
        curl -sS -X POST "https://api.telegram.org/bot${LOCAL_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${COACH_CHAT_ID}" \
            -d "text=${ALERT_MSG}" \
            -d "parse_mode=Markdown" \
            --max-time 10 > /dev/null 2>&1 && \
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Telegram 推送成功" >> "$LOG" || \
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ Telegram 推送失敗" >> "$LOG"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ 抓不到本地 bot token，無法推 Telegram" >> "$LOG"
    fi
elif [ "$ALERT" = "true" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️ 冷卻中（60 分鐘內已 alert 過）：$ALERT_REASON" >> "$LOG"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ OK: spool=$SPOOL_COUNT processing=$PROCESSING_COUNT last_inbound_age=$((LAST_INBOUND_AGE/60))m last_restart_age=$((LAST_RESTART_AGE/60))m" >> "$LOG"
fi

# 保留日誌最近 500 行
if [ -f "$LOG" ]; then
    tail -500 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
fi