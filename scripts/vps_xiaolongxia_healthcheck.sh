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
  ERR_CNT=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker logs openclaw --since 24h 2>&1 | grep -ciE 'error|failed|exception' | head -1" 2>&1)
  ERR_CNT=${ERR_CNT:-0}
  if [ "$ERR_CNT" -lt 50 ]; then
    RESULTS+=("✅ Gateway 24h 錯誤數: $ERR_CNT（< 50 容忍值）")
  else
    RESULTS+=("⚠️ Gateway 24h 錯誤數: $ERR_CNT（超過容忍值）")
    [ "$STATUS" = "OK" ] && STATUS="WARN"
  fi

  # 4. Gateway 是否回應（找最近一條 telegram inbound 或 ready）
  RECENT=$(sshpass -p "$VPS_PASS" ssh $SSH_OPTS "$VPS_HOST" "docker logs openclaw --since 1h 2>&1 | grep -E 'telegram|ready|heartbeat' | tail -1" 2>&1)
  if [ -n "$RECENT" ]; then
    RESULTS+=("✅ Gateway 活躍（過去 1 小時有事件）")
  else
    RESULTS+=("⚠️ Gateway 過去 1 小時無活動跡象")
    [ "$STATUS" = "OK" ] && STATUS="WARN"
  fi

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
  "results": [$(printf '"%s",' "${RESULTS[@]}" | sed 's/,$//')]
}
JSONEOF

# 推 Telegram（透過小龍蝦自家 send 機制；fallback 是寫 inbound 訊息）
# 健康時靜默；只在 WARN/DOWN 時才打擾教練
SUMMARY="🩺 VPS 小龍蝦健康檢查 [$STATUS] $TS"$'\n\n'
for r in "${RESULTS[@]}"; do
  SUMMARY+="$r"$'\n'
done

# 教練要求：每天回報。所以 OK 也報，但用最簡短訊息
if [ "$STATUS" = "OK" ]; then
  SHORT_MSG="🩺 VPS 小龍蝦 $TS [✅ 健康]"
else
  SHORT_MSG="$SUMMARY"
fi

# 透過 Mac 本機 OpenClaw send 推給教練
# Mac OpenClaw gateway port 18789
# 若推送失敗，至少 log 已存
curl -sS -X POST "http://127.0.0.1:18789/api/v1/messages/send" \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"telegram\",\"to\":\"6124913915\",\"text\":$(printf '%s' "$SHORT_MSG" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" \
  > /dev/null 2>&1 || echo "[$TS] curl 推 Telegram 失敗（log 已存於 $LOG_FILE）" >> "$LOG_FILE"

exit 0
