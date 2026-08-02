#!/usr/bin/env bash
# 教練最後訊息時間真相源 — v3.2 (2026-08-02 健檢修復)
# 用途：任何要寫「教練沉默 N 小時/天」之前，必須先跑這支腳本
#       把教練最後一則「真正」訊息時間，從 OpenClaw 自動寫的 memory/YYYY-MM-DD.md
#       找出來，寫回 state/heartbeat-state.json
#       然後才用 `date` 即時算差
#       **禁止**沿用舊 coachSilentHours 數字（8/1/8/2 三次犯錯的根因）
#
# 🔴 v3.2 修復（v3.1 遺留的致命 bug，健檢時發現）：
#   memory/YYYY-MM-DD.md 裡「## 📨 對話記錄 HH:MM」段落標題，代表的是
#   「cron/心跳觸發 snapshot 寫入的時間」，不是「教練真正說話的時間」——
#   每 30 分鐘健康檢查 cron、每 4 小時主動關懷 cron 都會被記成
#   「👤 教練：[cron:xxx] ...」或「👤 教練：[OpenClaw heartbeat poll]」，
#   v3.1 版只看段落標題時間、不看段落內容，代表只要 cron 還在跑，
#   就算教練真的沉默 3 天，也會被算成「剛剛才說話」——
#   跟原本「誤報沉默好幾天」的 bug 方向相反，但一樣是假數字。
#   v3.2 改成：逐段檢查段落內容，只採計「真的有非中括號開頭的
#   👤 教練：訊息」的那個段落時間，過濾掉 cron/心跳的系統注入訊息。
#
# 觸發方式：
#   1. cron 開工前自動跑（每4小時主動關懷 + 每30分鐘健康檢查）
#   2. 手動開工第一步（任何 agent 拿到任務時先跑一次）
#   3. 教練連發 2 則訊息時主動跑（未來可加 monitor hook）
#
# 為什麼不用 Telegram API：
#   OpenClaw bot 走 webhook delivery，getUpdates 撈不到已被 webhook 收走的訊息。
#   Telegram Bot API 沒有「查 user 最後一則訊息」endpoint。
#   唯一可靠來源是 OpenClaw 自己每次對話都寫的 memory/YYYY-MM-DD.md。

set -euo pipefail

MEMORY_DIR="$HOME/.openclaw/workspace/memory"
STATE_FILE="$HOME/.openclaw/workspace/state/heartbeat-state.json"
LOG_PREFIX="[sync_coach_last_message]"

if [[ ! -d "$MEMORY_DIR" ]]; then
  echo "$LOG_PREFIX ⚠️ 找不到 memory 目錄（$MEMORY_DIR）" >&2
  exit 1
fi

# === 逐天往回找，直到找到真的有教練訊息的那一天（最多回溯7天） ===
REAL_LAST_DATE=$(python3 << PYEOF
import re, os
from datetime import datetime, timezone, timedelta, date

memory_dir = "$MEMORY_DIR"
tz = timezone(timedelta(hours=8))
today = datetime.now(tz).date()

header_re = re.compile(r'## 📨 對話記錄 (\d{2}):(\d{2})')
# 真正教練訊息：行首「👤 教練：」且緊接著不是「[」（排除 cron/心跳系統注入）
real_msg_re = re.compile(r'^👤 教練：(?!\[)\S', re.MULTILINE)

result = ""
for back in range(7):
    d = today - timedelta(days=back)
    path = os.path.join(memory_dir, d.strftime("%Y-%m-%d.md"))
    if not os.path.isfile(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    headers = list(header_re.finditer(content))
    latest_real = None
    for idx, m in enumerate(headers):
        start = m.end()
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(content)
        body = content[start:end]
        if real_msg_re.search(body):
            hh, mm = int(m.group(1)), int(m.group(2))
            dt = datetime(d.year, d.month, d.day, hh, mm, 0, tzinfo=tz)
            if latest_real is None or dt > latest_real:
                latest_real = dt

    if latest_real is not None:
        result = latest_real.strftime('%Y-%m-%dT%H:%M:%S+08:00')
        break

print(result)
PYEOF
)

if [[ -z "$REAL_LAST_DATE" ]]; then
  echo "$LOG_PREFIX ⚠️ 回溯7天都找不到真正的教練訊息（排除cron/心跳系統注入後）" >&2
  echo "  → 請手動從 Telegram 確認教練最後訊息時間，不要編數字" >&2
  exit 1
fi

echo "$LOG_PREFIX 真正教練最後訊息時間：$REAL_LAST_DATE"

# === 寫回 state ===
python3 << PYEOF
import json, os
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=8))
state_path = "$STATE_FILE"
real_date_str = "$REAL_LAST_DATE"

if os.path.exists(state_path):
    with open(state_path, 'r') as f:
        state = json.load(f)
else:
    state = {'lastChecks': {}, 'systemSnapshot': {}}

state.setdefault('systemSnapshot', {})['coachSilentSince'] = real_date_str
real_dt = datetime.fromisoformat(real_date_str)
now_dt = datetime.now(tz)
diff_hours = round((now_dt - real_dt).total_seconds() / 3600, 1)
state['systemSnapshot']['coachSilentHours'] = diff_hours

state.setdefault('lastChecks', {})['coach_silence_sync'] = datetime.now(tz).isoformat()

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"✅ coachSilentSince = {real_date_str}（已排除cron/心跳系統注入訊息）")
print(f"✅ coachSilentHours = {diff_hours}")
PYEOF

exit 0
