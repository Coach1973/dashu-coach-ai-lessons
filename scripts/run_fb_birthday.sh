#!/bin/bash
# 重要：cron 環境 PATH 不含 /opt/homebrew/bin，必須用絕對路徑（TOOLS.md 鐵律）
cd /Users/bymyway/.openclaw/workspace/scripts
/opt/homebrew/bin/node fb_birthday_scraper.js >> /tmp/fb_birthday.log 2>&1
RC=$?
echo "[$(date)] done, exit: $RC" >> /tmp/fb_birthday.log
# 🔴 失敗也要通知：session 過期（exit 2）或 node 找不到（exit 127）
if [ $RC -ne 0 ]; then
  MSG="⚠️ FB 生日腳本失敗 (exit=$RC)，最近紀錄："
  MSG="$MSG$(tail -3 /tmp/fb_birthday.log | tr '\n' ' ')"
  /opt/homebrew/bin/python3 -c "
import urllib.request, urllib.parse, json
# 改用更穩的方式：直接寫到本地通知檔
open('/tmp/fb_birthday_alert.txt','w').write('$MSG')
" 2>/dev/null
fi