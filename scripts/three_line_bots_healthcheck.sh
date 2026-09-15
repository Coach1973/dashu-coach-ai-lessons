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
# 3. LINE webhook 公開端對端路徑是否有回應（event.bymyway.com/line/webhook，測整條Cloudflare tunnel路徑）
#
# 結果推送：Telegram 通知教練（不論健康與否，教練要求每天都要回報）

LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/line_bots_healthcheck.log"
STATE_FILE="/Users/bymyway/.openclaw/workspace/logs/line_bots_healthcheck_state.json"
GATEWAY_LOG="/Users/bymyway/Library/Logs/openclaw/gateway.log"
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

# 3. LINE webhook 公開端對端路徑（測整條 DNS→Cloudflare→tunnel→gateway）
HTTP_CODE=$(curl -s -o /dev/null -m 10 -w "%{http_code}" -X POST https://event.bymyway.com/line/webhook -H "Content-Type: application/json" -d '{}' 2>/dev/null)
if [ "$HTTP_CODE" = "400" ] || [ "$HTTP_CODE" = "403" ]; then
  RESULTS+=("✅ webhook 對外路徑正常（HTTP $HTTP_CODE，代表請求有到gateway並被正確拒絕，這是預期行為）")
elif [ -z "$HTTP_CODE" ] || [ "$HTTP_CODE" = "000" ]; then
  RESULTS+=("❌ webhook 對外路徑無回應（逾時/連不上，可能是 Cloudflare tunnel 斷線）")
  STATUS="DOWN"
else
  RESULTS+=("⚠️ webhook 對外路徑回應異常 HTTP $HTTP_CODE（非預期狀態碼，需人工查證）")
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

curl -sS -X POST "http://127.0.0.1:18789/api/v1/messages/send" \
  -H "Content-Type: application/json" \
  -d "{\"channel\":\"telegram\",\"to\":\"6124913915\",\"text\":$(printf '%s' "$SUMMARY" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')}" \
  > /dev/null 2>&1 || echo "[$TS] curl 推 Telegram 失敗（log 已存於 $LOG_FILE）" >> "$LOG_FILE"

exit 0
