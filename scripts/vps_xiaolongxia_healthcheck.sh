#!/bin/bash
# VPS 小龍蝦每日健康檢查
# 由 LaunchAgent ai.openclaw.vps-healthcheck.plist 排程，每天 08:00 跑
# 教練 2026-06-09 親令：每天測 + 回報，避免外部體驗用戶踩雷
#
# 檢查項目：
# 1. SSH 連通性
# 2. Docker 容器狀態
# 3. Gateway log 過去 24 小時是否有 ERROR
# 4. Gateway 是否回應 health endpoint
# 5. Telegram bot 是否在跑
#
# 結果推送：學長透過 OpenClaw 主軌通知教練 Telegram

VPS_HOST="root@43.245.60.200"
VPS_PASS="9kdxvQN2"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10"
LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/vps_healthcheck.log"
STATE_FILE="/Users/bymyway/.openclaw/workspace/logs/vps_healthcheck_state.json"
TS=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$(dirname "$LOG_FILE")"

# 結果累積
RESULTS=()
STATUS="OK"

# 1. SSH 連通性
SSH_OUT=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "uptime" 2>&1)
if echo "$SSH_OUT" | grep -q "load average"; then
  RESULTS+=("✅ SSH 連通")
else
  RESULTS+=("❌ SSH 失敗: $SSH_OUT")
  STATUS="DOWN"
fi

# 2. Docker 容器狀態（若 SSH 通才檢）
if [ "$STATUS" = "OK" ]; then
  CONTAINER=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker ps --filter name=openclaw --format '{{.Status}}'" 2>&1)
  if echo "$CONTAINER" | grep -q "Up"; then
    RESULTS+=("✅ Docker 容器: $CONTAINER")
  else
    RESULTS+=("❌ Docker 容器狀態: $CONTAINER")
    STATUS="DOWN"
  fi

  # 3. Gateway 過去 24 小時 ERROR 數量
  ERR_CNT=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker logs openclaw --since 24h 2>&1 | grep -iE 'error|failed|exception' | grep -viE 'embeddings unavailable|node-llama-cpp|memory pressure|edit failed' | wc -l" 2>&1)
  ERR_CNT=${ERR_CNT:-0}
  if [ "$ERR_CNT" -lt 50 ]; then
    RESULTS+=("✅ Gateway 24h 錯誤數: $ERR_CNT（< 50 容忍值）")
  else
    RESULTS+=("⚠️ Gateway 24h 錯誤數: $ERR_CNT（超過容忍值）")
    [ "$STATUS" = "OK" ] && STATUS="WARN"
  fi

  # 3b. 硬碟用量（2026-10-28 VPS 曾因 .git 堆積用到 81%，超過 70% 就預警）
  DISK_PCT=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "df / | awk 'NR==2{gsub(\"%\",\"\",\$5); print \$5}'" 2>/dev/null)
  DISK_PCT=${DISK_PCT:-0}
  if [ "$DISK_PCT" -lt 70 ]; then
    RESULTS+=("✅ 硬碟用量: ${DISK_PCT}%")
  else
    RESULTS+=("⚠️ 硬碟用量: ${DISK_PCT}%（超過 70%）")
    [ "$STATUS" = "OK" ] && STATUS="WARN"
  fi

  # 4. 使用量（排除教練本人）。原本「過去1小時沒活動就WARN」已拿掉：沒人用不等於故障，
  #    2026-09-24體檢發現它天天誤報。改成純記錄人數，由每日全隊點名彙報。
  SENDERS_24H=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker logs openclaw --since 24h 2>&1 | grep -a -i 'inbound message' | grep -a -o 'telegram:[0-9-]*' | grep -v 'telegram:6124913915'" 2>/dev/null)
  SENDERS_7D=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker logs openclaw --since 168h 2>&1 | grep -a -i 'inbound message' | grep -a -o 'telegram:[0-9-]*' | grep -v 'telegram:6124913915'" 2>/dev/null)
  MSGS_24H=$(printf '%s\n' "$SENDERS_24H" | grep -c .)
  USERS_24H=$(printf '%s\n' "$SENDERS_24H" | grep . | sort -u | grep -c .)
  USERS_7D=$(printf '%s\n' "$SENDERS_7D" | grep . | sort -u | grep -c .)
  RESULTS+=("ℹ️ 使用量：近24小時${USERS_24H}人（${MSGS_24H}則），近7天${USERS_7D}人")
  # 正式服務跑的是映像檔內 /app 這份（容器裡另有一份 openclaw CLI 版本號不同，不能拿來當準）
  APP_VERSION=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker exec openclaw sh -c 'grep -m1 \"\\\"version\\\"\" /app/package.json'" 2>/dev/null | grep -oE '[0-9]{4}\.[0-9]+\.[0-9]+[^"]*' | head -1)

  # 5. 確認模型載入成功（找 'agent model: minimax')
  MODEL_OK=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker logs openclaw --since 24h 2>&1 | grep 'agent model: minimax' | tail -1" 2>&1)
  if [ -n "$MODEL_OK" ]; then
    RESULTS+=("✅ 模型已載入: $(echo $MODEL_OK | grep -oE 'minimax/[^ ]*')")
  else
    # 沒看到 'agent model' 不代表壞，可能上次啟動 > 24h
    RESULTS+=("ℹ️ 24h 內未見模型載入訊息（可能容器穩定運行 > 24h）")
  fi
fi

# 輸出結果
{
  echo "===== [$TS] VPS 小龍蝦健康檢查 ====="
  echo "整體狀態: $STATUS"
  for r in "${RESULTS[@]}"; do
    echo "  $r"
  done
  echo ""
} >> "$LOG_FILE"

# 寫狀態檔（供其他系統讀）
cat > "$STATE_FILE" <<JSONEOF
{
  "lastCheckAt": "$TS",
  "status": "$STATUS",
  "users_24h": ${USERS_24H:-0},
  "msgs_24h": ${MSGS_24H:-0},
  "users_7d": ${USERS_7D:-0},
  "app_version": "${APP_VERSION:-}",
  "results": [$(printf '"%s",' "${RESULTS[@]}" | sed 's/,$//')]
}
JSONEOF

SUMMARY="🩺 VPS 小龍蝦健康檢查 [$STATUS] $TS"$'\n\n'
for r in "${RESULTS[@]}"; do
  SUMMARY+="$r"$'\n'
done

# 平安的每日回報改由 daily_team_rollcall.py（08:10）統一彙報，這裡只在異常時立刻通知。
# 原本打 127.0.0.1:18789/api/v1/messages/send，2026-09-24 查證該端點回 404 不存在，
# curl 沒加 -f 所以 404 也算成功、失敗紀錄從沒寫出來，每天的回報全部無聲消失。
if [ "$STATUS" != "OK" ]; then
  /Users/bymyway/.openclaw/workspace/scripts/notify_coach.sh "$SUMMARY" \
    || echo "[$TS] 推 Telegram 失敗（詳見 notify_coach.log）" >> "$LOG_FILE"
fi

exit 0
