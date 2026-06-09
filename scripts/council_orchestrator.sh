#!/bin/bash
# 方案 A：cron 每 2 分鐘巡邏 + 方案 B：bot-relay hook 即時觸發共用本腳本
# 用途：學長派議程 + 學弟學妹發完 → 自動代學長發 Council Mode 三段收尾
# 教練 2026-06-09 下午 2:40 親令：A+B 雙保險
# 軍師建立 2026-06-09 下午 2:42 台灣時間
set -uo pipefail

# ── 設定 ────────────────────────────────────────────────
LOG=/Users/bymyway/.openclaw/workspace/BOT_MESSAGES.md
CHAT_ID=-1003877502911
MAIN_BOT_TOKEN="8758843664:AAE4W-hGh2mPxNt89b2donZ0Q--YZ9uwdsA"
TRIGGER_LOG=/Users/bymyway/.openclaw/workspace/logs/council_orchestrator.log
LOCK=/tmp/.council_orchestrator.lock
LOCK_TTL=300   # 5 分鐘內已觸發過就 skip
MIN_WAIT=60    # 議程派發後至少等 60 秒讓學弟學妹有時間發言
MAX_WAIT=300   # 派發後 5 分鐘超時：學弟學妹沒發也要收尾

MINIMAX_KEY=$(jq -r '.profiles["minimax:default"].key' /Users/bymyway/.openclaw/workspace/agent/auth-profiles.json 2>/dev/null)
[[ -z "$MINIMAX_KEY" || "$MINIMAX_KEY" == "null" ]] && { echo "$(TZ=Asia/Taipei date '+%F %T') no minimax key, skip" >> "$TRIGGER_LOG"; exit 0; }

mkdir -p "$(dirname "$TRIGGER_LOG")"
NOW_TS=$(TZ=Asia/Taipei date '+%F %T')

# ── 防重複觸發 ──────────────────────────────────────────
if [[ -f "$LOCK" ]]; then
  AGE=$(($(date +%s) - $(stat -f %m "$LOCK" 2>/dev/null || echo 0)))
  if [[ $AGE -lt $LOCK_TTL ]]; then
    exit 0
  fi
fi

# ── 讀 BOT_MESSAGES 最近 50 條 ───────────────────────────
[[ ! -f "$LOG" ]] && exit 0
RECENT=$(tail -50 "$LOG" | grep -E '^\{' || echo "")
[[ -z "$RECENT" ]] && exit 0

# ── 找最後一次學長派議程 ────────────────────────────────
LAST_AGENDA=$(echo "$RECENT" | jq -c 'select(.botId=="main" and (.text | test("議程派發|📋")))' 2>/dev/null | tail -1)
[[ -z "$LAST_AGENDA" ]] && exit 0

AGENDA_TS=$(echo "$LAST_AGENDA" | jq -r .ts)
# 把 ISO Z 時間轉成 epoch (Mac date 不支援 Z，剝掉)
AGENDA_EPOCH=$(date -u -j -f '%Y-%m-%dT%H:%M:%S' "${AGENDA_TS%.*}" +%s 2>/dev/null || echo 0)
[[ $AGENDA_EPOCH -eq 0 ]] && exit 0
NOW=$(date +%s)
ELAPSED=$((NOW - AGENDA_EPOCH))

# 太新就不動（讓學弟學妹發完）
[[ $ELAPSED -lt $MIN_WAIT ]] && exit 0

# ── 找派發後的所有訊息 ──────────────────────────────────
AFTER_AGENDA=$(echo "$RECENT" | jq -c "select(.ts > \"$AGENDA_TS\")" 2>/dev/null)

# 學長已收尾就 skip（包含三段任一字眼）
ALREADY_COUNCILED=$(echo "$AFTER_AGENDA" | jq -c 'select(.botId=="main" and (.text | test("三方共識|主要分歧|獨特發現")))' 2>/dev/null | head -1)
[[ -n "$ALREADY_COUNCILED" ]] && exit 0

KONG_COUNT=$(echo "$AFTER_AGENDA" | jq -c 'select(.botId=="kong")' 2>/dev/null | wc -l | tr -d ' ')
PEIPEI_COUNT=$(echo "$AFTER_AGENDA" | jq -c 'select(.botId=="peipei")' 2>/dev/null | wc -l | tr -d ' ')

# 觸發條件：學弟學妹都發過 OR 派發後超過 MAX_WAIT 秒
SHOULD_TRIGGER=0
[[ $KONG_COUNT -gt 0 && $PEIPEI_COUNT -gt 0 ]] && SHOULD_TRIGGER=1
[[ $ELAPSED -gt $MAX_WAIT ]] && SHOULD_TRIGGER=1
[[ $SHOULD_TRIGGER -eq 0 ]] && exit 0

# ── 觸發 Council Mode：呼叫 minimax 生三段收尾 ──────────
echo "$NOW_TS triggered: agenda=$AGENDA_TS elapsed=${ELAPSED}s kong=$KONG_COUNT peipei=$PEIPEI_COUNT" >> "$TRIGGER_LOG"

# 收集材料：議程+各方發言
AGENDA_TEXT=$(echo "$LAST_AGENDA" | jq -r .text)
KONG_LATEST=$(echo "$AFTER_AGENDA" | jq -c 'select(.botId=="kong")' 2>/dev/null | tail -1 | jq -r .text 2>/dev/null || echo "（學弟未發言）")
PEIPEI_LATEST=$(echo "$AFTER_AGENDA" | jq -c 'select(.botId=="peipei")' 2>/dev/null | tail -1 | jq -r .text 2>/dev/null || echo "（學妹未發言）")

# 寫 prompt（守則 #08 直接執行不問）
PROMPT_BODY=$(cat <<PROMPT
你是大樹教練的特助學長（main）。剛剛在「頂級特助分工群」派了議程，學弟學妹也分別發言了。現在請依「Council Mode 三段收尾」鐵律寫一條回應呈給教練。

【你派的議程】
${AGENDA_TEXT}

【學弟最新發言】
${KONG_LATEST}

【學妹最新發言】
${PEIPEI_LATEST}

【寫作要求】
- 全文繁體中文，禁止英文
- 不超過 300 字
- 必須包含三段：
  ✅ 三方共識：⋯
  ⚠️ 主要分歧：⋯
  💡 獨特發現：⋯
- 開頭加一行：「🎯 Council Mode 三段收尾（系統超時自動觸發，學長未及時收尾）」
PROMPT
)

# 呼叫 minimax anthropic-compatible API
RESPONSE=$(curl -sS -X POST 'https://api.minimax.io/anthropic/v1/messages' \
  -H "x-api-key: $MINIMAX_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  --max-time 60 \
  -d "$(jq -n --arg p "$PROMPT_BODY" '{
    model: "MiniMax-M3",
    max_tokens: 800,
    messages: [{role: "user", content: $p}]
  }')")

COUNCIL_TEXT=$(echo "$RESPONSE" | jq -r '.content[]? | select(.type=="text") | .text' 2>/dev/null | head -100)

if [[ -z "$COUNCIL_TEXT" || "$COUNCIL_TEXT" == "null" ]]; then
  echo "$NOW_TS llm failed, response=$(echo "$RESPONSE" | head -c 200)" >> "$TRIGGER_LOG"
  exit 0
fi

# ── Telegram sendMessage 到分工群（用 main bot token）────
TG_RESPONSE=$(curl -sS -X POST "https://api.telegram.org/bot${MAIN_BOT_TOKEN}/sendMessage" \
  --max-time 15 \
  -d "chat_id=${CHAT_ID}" \
  --data-urlencode "text=${COUNCIL_TEXT}")

OK=$(echo "$TG_RESPONSE" | jq -r '.ok' 2>/dev/null)
if [[ "$OK" != "true" ]]; then
  echo "$NOW_TS tg send failed: $(echo "$TG_RESPONSE" | head -c 200)" >> "$TRIGGER_LOG"
  exit 0
fi

# 成功 → 手動寫一筆到 BOT_MESSAGES 標記學長已收尾（直發 API 不經 gateway，hook 不會自動寫）
TG_MSG_ID=$(echo "$TG_RESPONSE" | jq -r '.result.message_id' 2>/dev/null)
COUNCIL_ENTRY=$(jq -nc --arg text "${COUNCIL_TEXT:0:200}" --arg msgId "$TG_MSG_ID" --arg chatId "$CHAT_ID" '{
  ts: (now | strftime("%Y-%m-%dT%H:%M:%S.000Z")),
  botId: "main",
  botName: "🦞學長",
  text: $text,
  msgId: ($msgId | tonumber? // 0),
  chatId: $chatId
}')
echo "$COUNCIL_ENTRY" >> "$LOG"

touch "$LOCK"
echo "$NOW_TS ✅ council sent successfully (msgId=$TG_MSG_ID)" >> "$TRIGGER_LOG"
exit 0
