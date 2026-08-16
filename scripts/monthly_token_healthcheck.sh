#!/bin/bash
# monthly_token_healthcheck.sh — 賈維斯計畫 Phase 2
# 用途：逐一驗證所有還在服役的API Token/憑證是否還活著，只回報壞掉的
# 設計：全綠不輸出任何東西（by design，遵守「不影響工作就別吵教練」鐵律）；
#       有紅才印出來，讓外層的cron isolated agent turn判斷要不要announce
# 建立：2026-08-16 賈維斯計畫Phase2
set -uo pipefail

FAIL_COUNT=0
RESULTS=""

check() {
  local name="$1"
  local status="$2"  # "ok" or "fail" or "skip"
  local detail="${3:-}"
  if [ "$status" = "fail" ]; then
    FAIL_COUNT=$((FAIL_COUNT+1))
    RESULTS="${RESULTS}❌ ${name}：${detail}\n"
  fi
}

# 1. Netlify Token
NETLIFY_TOKEN="nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838"
NETLIFY_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
  -H "Authorization: Bearer ${NETLIFY_TOKEN}" "https://api.netlify.com/api/v1/sites?per_page=1")
if [ "$NETLIFY_CODE" = "200" ]; then check "Netlify Token" "ok"
else check "Netlify Token" "fail" "HTTP ${NETLIFY_CODE}（預期200），token可能過期或被撤銷"; fi

# 2. Cloudflare API Token
CF_TOKEN="cfut_9rJE0124qbS8T7msli9ZIy59QlBDcOlnUkm08DDTdf141237"
CF_VALID=$(curl -s --max-time 10 "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer ${CF_TOKEN}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('success', False))" 2>/dev/null)
if [ "$CF_VALID" = "True" ]; then check "Cloudflare Token" "ok"
else check "Cloudflare Token" "fail" "驗證失敗，可能過期/撤銷/網路異常"; fi

# 3. WordPress bymyway.com 應用程式密碼
WP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
  -u "bymyway7:Gqx6 0c9r JRW9 vOgA sxCB 0ywX" "https://www.bymyway.com/wp-json/wp/v2/posts?per_page=1")
if [ "$WP_CODE" = "200" ]; then check "WordPress應用程式密碼" "ok"
else check "WordPress應用程式密碼" "fail" "HTTP ${WP_CODE}（預期200）"; fi

# 4. event-signup 專用 LINE OA（@qaw8118h）
EVENT_LINE_TOKEN=$(python3 -c "
import json
with open('/Users/bymyway/.openclaw/openclaw.json') as f:
    c = json.load(f)
print(c.get('channels', {}).get('line', {}).get('channelAccessToken', ''))
" 2>/dev/null)
if [ -n "$EVENT_LINE_TOKEN" ]; then
  LINE_DEFAULT_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
    -H "Authorization: Bearer ${EVENT_LINE_TOKEN}" "https://api.line.me/v2/bot/info")
  if [ "$LINE_DEFAULT_CODE" = "200" ]; then check "LINE 龍蝦小助教/教練都在想什麼共用token" "ok"
  else check "LINE 龍蝦小助教token" "fail" "HTTP ${LINE_DEFAULT_CODE}"; fi
else
  check "LINE 龍蝦小助教token" "fail" "openclaw.json讀不到channels.line.channelAccessToken"
fi

# 5. bni_tainan / jiaolian_thoughts 各自的tokenFile
for pair in "bni_tainan:BNI大台南小幫手" "jiaolian_thoughts:教練都在想什麼"; do
  acct="${pair%%:*}"; label="${pair##*:}"
  TOKFILE="/Users/bymyway/.openclaw/credentials/line-${acct}-token.txt"
  if [ -f "$TOKFILE" ]; then
    TOK=$(cat "$TOKFILE" | tr -d '\n')
    CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 \
      -H "Authorization: Bearer ${TOK}" "https://api.line.me/v2/bot/info")
    if [ "$CODE" = "200" ]; then check "LINE ${label}" "ok"
    else check "LINE ${label}" "fail" "HTTP ${CODE}"; fi
  else
    check "LINE ${label}" "fail" "tokenFile不存在：${TOKFILE}"
  fi
done

# 6. Telegram 三帳號
for pair in "bot_main:小龍蝦/軍師主通道" "bot_kong:kong" "bot_peipei:peipei"; do
  acct="${pair%%:*}"; label="${pair##*:}"
  TOK=$(python3 -c "
import json
with open('/Users/bymyway/.openclaw/openclaw.json') as f:
    c = json.load(f)
print(c.get('channels', {}).get('telegram', {}).get('accounts', {}).get('${acct}', {}).get('botToken', ''))
" 2>/dev/null)
  if [ -n "$TOK" ]; then
    OK=$(curl -s --max-time 10 "https://api.telegram.org/bot${TOK}/getMe" | python3 -c "import json,sys; print(json.load(sys.stdin).get('ok', False))" 2>/dev/null)
    if [ "$OK" = "True" ]; then check "Telegram ${label}" "ok"
    else check "Telegram ${label}" "fail" "getMe回應異常"; fi
  else
    check "Telegram ${label}" "fail" "openclaw.json讀不到botToken"
  fi
done

# 輸出
if [ "$FAIL_COUNT" -eq 0 ]; then
  echo "OK: 全部9項憑證健在（Netlify/Cloudflare/WordPress/LINE×3/Telegram×3）"
  exit 0
else
  echo "FAIL: ${FAIL_COUNT} 項憑證異常"
  echo -e "$RESULTS"
  exit 1
fi
