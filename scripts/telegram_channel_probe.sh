#!/bin/bash
# telegram_channel_probe.sh — Telegram 通道健康「真相源」探針
# 建立：軍師 Fable 5，2026-07-22（試金石案例 53：假警報憋住關懷 5.5 天）
#
# 用途：任何要判斷「Telegram 通道死活」的地方（心跳、健康檢查），
#       都必須先跑這支腳本拿「真相源」，禁止盲信 heartbeat-state.json 裡的舊旗標。
#
# 判斷方式（確定性，非 AI 臆測）：
#   1. getMe   → bot token 本身活著？
#   2. getChat → bot 到教練本人對話 6124913915 的通道通？
#   兩者都過 = 通道健康（exit 0, 印 OK）
#   任一失敗 = 真的有問題（exit 1, 印 FAIL + 原因）
#
# 用法：bash telegram_channel_probe.sh [--json]

CONFIG="$HOME/.openclaw/openclaw.json"
COACH_CHAT="6124913915"
JSON_MODE=0
[ "$1" = "--json" ] && JSON_MODE=1

# 從設定檔取 bot_main token（真相源，不寫死）
TOKEN=$(python3 -c "
import json
d=json.load(open('$CONFIG'))
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='botToken' and isinstance(v,str): return v
            r=walk(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=walk(v)
            if r: return r
    return None
# 優先抓 accounts.bot_main
ch=d.get('channels',{}).get('telegram',{})
acc=ch.get('accounts',{})
if 'bot_main' in acc and acc['bot_main'].get('botToken'):
    print(acc['bot_main']['botToken'])
else:
    print(walk(ch) or '')
" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    [ $JSON_MODE -eq 1 ] && echo '{"ok":false,"reason":"no_token_in_config"}' || echo "FAIL: 設定檔找不到 bot_main token"
    exit 1
fi

# 1. getMe
ME=$(curl -s --max-time 60 "https://api.telegram.org/bot${TOKEN}/getMe")
ME_OK=$(echo "$ME" | python3 -c "import sys,json;print('1' if json.load(sys.stdin).get('ok') else '0')" 2>/dev/null)
BOT_NAME=$(echo "$ME" | python3 -c "import sys,json;print(json.load(sys.stdin).get('result',{}).get('username',''))" 2>/dev/null)

if [ "$ME_OK" != "1" ]; then
    REASON=$(echo "$ME" | python3 -c "import sys,json;print(json.load(sys.stdin).get('description','unknown'))" 2>/dev/null)
    [ $JSON_MODE -eq 1 ] && echo "{\"ok\":false,\"reason\":\"getMe_failed: $REASON\"}" || echo "FAIL: getMe 失敗 — $REASON"
    exit 1
fi

# 2. getChat 教練對話
CHAT=$(curl -s --max-time 60 "https://api.telegram.org/bot${TOKEN}/getChat?chat_id=${COACH_CHAT}")
CHAT_OK=$(echo "$CHAT" | python3 -c "import sys,json;print('1' if json.load(sys.stdin).get('ok') else '0')" 2>/dev/null)

if [ "$CHAT_OK" != "1" ]; then
    REASON=$(echo "$CHAT" | python3 -c "import sys,json;print(json.load(sys.stdin).get('description','unknown'))" 2>/dev/null)
    [ $JSON_MODE -eq 1 ] && echo "{\"ok\":false,\"bot\":\"$BOT_NAME\",\"reason\":\"getChat_failed: $REASON\"}" || echo "FAIL: bot @$BOT_NAME 活著，但到教練對話失敗 — $REASON"
    exit 1
fi

# 兩者都過
[ $JSON_MODE -eq 1 ] && echo "{\"ok\":true,\"bot\":\"$BOT_NAME\",\"chat\":\"$COACH_CHAT\"}" || echo "OK: Telegram 通道健康（bot=@$BOT_NAME → 教練 $COACH_CHAT 通道正常）"
exit 0
