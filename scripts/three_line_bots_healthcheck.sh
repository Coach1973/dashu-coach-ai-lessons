#!/bin/bash
# 三個LINE小幫手每日健康檢查（大台南南區AI小幫手/教練都在想什麼/龍蝦小助教）
# 由 LaunchAgent ai.openclaw.line-bots-healthcheck.plist 排程，每天 08:05 跑
# 教練 2026-09-16 親令：每天回報，避免像這次「三個同時當掉5天多沒人發現」再度發生
#
# 起因：2026-09-10 22:24 gateway熱重載時，@openclaw/line外掛套件檔案遺失
# （plugins.entries.line: plugin not installed），三個LINE帳號從此靜默斷線，
# 直到2026-09-16教練自己動手測試才發現，已用「openclaw plugins install @openclaw/line」修復。
# 這次檢查刻意不只測process是否活著（process活著≠外掛真的載入成功），照試金石教訓多測兩層。
#
# 檢查項目：
# 1. gateway process 是否存活
# 2. gateway 最近一次啟動的 plugin 清單是否真的包含 line（不是只看config，是看實際載入結果）
# 3. LINE webhook 公開端對端路徑是否有回應（用正確簽章測真正的路徑，非隨便測一個回應碼就當過）
#
# 🔴 2026-09-16 教練當場抓到的血淚教訓：第一版腳本測的是 event.bymyway.com/line/webhook，
# 這個網址其實是完全不相關的另一個LINE官方帳號「大樹教練」(event-signup報名系統專用)在用，
# 跟這三個帳號完全無關——測到403以為「有回應=正常」，實際上教練發真訊息給「教練都在想什麼」
# 完全沒收到回覆。真正這三個帳號共用的tunnel(小龍蝦專線,id e35d30ec-...)對應的公開網址是
# bni/media/openclaw/rpl-workshop/seabiscuit.bymyway.com這五個(用Cloudflare API查DNS CNAME
# 找到的)，逐一測試後確認bni/openclaw/seabiscuit三個能正確路由到gateway。
# 改用「真的帶正確HMAC簽章」的合成webhook打openclaw.bymyway.com，收到200才代表
# 簽章驗證通過、訊息真的能被處理，不能再只看「有沒有回應」這種弱驗證。
#
# 結果推送：Telegram 通知教練（不論健康與否，教練要求每天都要回報）

LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/line_bots_healthcheck.log"
STATE_FILE="/Users/bymyway/.openclaw/workspace/logs/line_bots_healthcheck_state.json"
GATEWAY_LOG="/Users/bymyway/Library/Logs/openclaw/gateway.log"
LINE_WEBHOOK_HOST="openclaw.bymyway.com"
LINE_SECRET_FILE="/Users/bymyway/.openclaw/credentials/line-jiaolian_thoughts-secret.txt"
TS=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$(dirname "$LOG_FILE")"

RESULTS=()
STATUS="OK"

# 1. gateway process 是否存活
if pgrep -f "openclaw.*gateway --port 18789" > /dev/null 2>&1; then
  RESULTS+=("✅ Gateway process 存活")
else
  RESULTS+=("❌ Gateway process 沒有在跑")
  STATUS="DOWN"
fi

# 2. 最近一次啟動的 plugin 清單是否真的包含 line
LAST_PLUGIN_LINE=$(grep "http server listening" "$GATEWAY_LOG" 2>/dev/null | tail -1)
if echo "$LAST_PLUGIN_LINE" | grep -q ", line,"; then
  RESULTS+=("✅ line 外掛已成功載入（最近一次啟動記錄有 line）")
else
  RESULTS+=("❌ line 外掛沒有載入！最近啟動記錄：$(echo "$LAST_PLUGIN_LINE" | grep -oE '\([0-9]+ plugins:.*\)')")
  STATUS="DOWN"
fi

# 3. LINE webhook 公開端對端路徑：帶正確HMAC簽章的合成webhook，測真正的 bni/openclaw/seabiscuit.bymyway.com
if [ -f "$LINE_SECRET_FILE" ]; then
  LINE_SECRET=$(cat "$LINE_SECRET_FILE")
  BODY="{\"destination\":\"Uhealthcheck\",\"events\":[{\"type\":\"message\",\"message\":{\"type\":\"text\",\"id\":\"healthcheck\",\"text\":\"每日健檢-請忽略\"},\"webhookEventId\":\"healthcheck-$(date +%s)\",\"deliveryContext\":{\"isRedelivery\":false},\"timestamp\":$(date +%s000),\"source\":{\"type\":\"user\",\"userId\":\"Uhealthcheck\"},\"replyToken\":\"healthcheckreplytoken\",\"mode\":\"active\"}]}"
  SIG=$(printf '%s' "$BODY" | openssl dgst -sha256 -hmac "$LINE_SECRET" -binary | base64)
  HTTP_CODE=$(curl -s -o /dev/null -m 10 -w "%{http_code}" -X POST "https://${LINE_WEBHOOK_HOST}/line/webhook" \
    -H "Content-Type: application/json" -H "X-Line-Signature: $SIG" -d "$BODY" 2>/dev/null)
  if [ "$HTTP_CODE" = "200" ]; then
    RESULTS+=("✅ webhook 對外路徑正常（${LINE_WEBHOOK_HOST}，帶正確簽章測試，HTTP 200代表簽章驗證通過、訊息真的能被處理）")
  elif [ -z "$HTTP_CODE" ] || [ "$HTTP_CODE" = "000" ]; then
    RESULTS+=("❌ webhook 對外路徑無回應（${LINE_WEBHOOK_HOST} 逾時/連不上，可能是 Cloudflare tunnel 斷線）")
    STATUS="DOWN"
  else
    RESULTS+=("❌ webhook 對外路徑異常（${LINE_WEBHOOK_HOST} 回應 HTTP $HTTP_CODE，正確簽章應該回200，其他都代表沒有真的處理成功）")
    STATUS="DOWN"
  fi
else
  RESULTS+=("⚠️ 找不到 $LINE_SECRET_FILE，無法做簽章測試")
  [ "$STATUS" = "OK" ] && STATUS="WARN"
fi

# 輸出結果
{
  echo "===== [$TS] 三個LINE小幫手健康檢查 ====="
  echo "整體狀態: $STATUS"
  for r in "${RESULTS[@]}"; do
    echo "  $r"
  done
  echo ""
} >> "$LOG_FILE"

cat > "$STATE_FILE" <<JSONEOF
{
  "lastCheckAt": "$TS",
  "status": "$STATUS",
  "results": [$(printf '"%s",' "${RESULTS[@]}" | sed 's/,$//')]
}
JSONEOF

# 教練2026-09-16親令：每天都要回報，不論健康與否（跟VPS健檢的「OK靜默」不同，這是新規則）
SUMMARY="🩺 三個LINE小幫手健康檢查 [$STATUS] $TS"$'\n'
SUMMARY+="（大台南南區小幫手／教練都在想什麼／龍蝦小助教）"$'\n\n'
for r in "${RESULTS[@]}"; do
  SUMMARY+="$r"$'\n'
done

# 原本打 127.0.0.1:18789/api/v1/messages/send，2026-09-24 查證該端點回 404 不存在，
# curl 沒加 -f 所以 404 也算成功，自 09-16 上線起每天的回報全部無聲消失。
/Users/bymyway/.openclaw/workspace/scripts/notify_coach.sh "$SUMMARY" \
  || echo "[$TS] 推 Telegram 失敗（詳見 notify_coach.log）" >> "$LOG_FILE"

exit 0
