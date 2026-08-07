#!/usr/bin/env bash
# 教練最後訊息時間真相源 — v3.4 (2026-08-07 補強：echo log 優先於 memory 掃描)
# 用途：任何要寫「教練沉默 N 小時/天」之前，必須先跑這支腳本
#       把教練最後一則「真正」訊息時間，從 OpenClaw 自動寫的 memory/YYYY-MM-DD.md
#       找出來，寫回 state/heartbeat-state.json
#       然後才用 `date` 即時算差
#       **禁止**沿用舊 coachSilentHours 數字（8/1/8/2 三次犯錯的根因）
#
# 🔴 v3.4 修復（2026-08-06 教練回報「明明有說話」查證發現的真根因）：
#   2026-08-03 15:58:42 教練從 Telegram 傳訊息，gateway log 證實收到了，
#   但那輪 agent turn 疑似被 API 429 卡死，訊息內容從沒寫進 memory/YYYY-MM-DD.md，
#   導致這支腳本（只掃 memory）完全找不到，算出錯誤的沉默時數。
#   新增 hooks/inbound-message-echo-log 在訊息「一進來」當下就同步落地存檔
#   （不等 agent turn 跑完），這支腳本現在優先讀 echo log，
#   跟 memory 掃描兩邊取「更新的那個」，不會再因為某輪 agent turn 死掉而漏算。
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
# 🔴 v3.3修復（2026-08-02 18:03「7天沒互動」誤報血淚）：
#   系統裡實際存在兩份 heartbeat-state.json（state/ 和 memory/ 各一份，
#   彼此互不同步）。之前v3.0~v3.2的修復只碰了 state/ 那份，但18:03那次
#   agent turn（context overflow重啟+API 429限流+config reload三重疊加
#   導致執行環境不穩定）讀到的卻是 memory/ 那份——它從7/26後就沒再被
#   更新過，166.2小時換算下來剛好是「7天」，誤報就是這樣產生的。
#   不確定 agent 未來還會讀哪一份，兩份都寫，才不會再被舊值咬到。
STATE_FILE_LEGACY="$HOME/.openclaw/workspace/memory/heartbeat-state.json"
LOG_PREFIX="[sync_coach_last_message]"

if [[ ! -d "$MEMORY_DIR" ]]; then
  echo "$LOG_PREFIX ⚠️ 找不到 memory 目錄（$MEMORY_DIR）" >&2
  exit 1
fi

# === v3.4 新增：先掃 inbound-message-echo-log（訊息一進來當下就落地，不受 agent turn 死掉影響） ===
ECHO_DIR="$HOME/.openclaw/workspace/state/inbound_echo"
ECHO_LAST_DATE=$(python3 << PYEOF
import json, os
from datetime import datetime, timezone, timedelta

echo_dir = "$ECHO_DIR"
tz = timezone(timedelta(hours=8))
today = datetime.now(tz).date()

# 教練本人的識別碼（Telegram chatId + LINE 兩組帳號），避免把其他發送者的訊息誤算進來
COACH_IDS = {"6124913915", "u895a0ad8e49d75f8303dc3d067282dc0", "u168903487f0ba2b666ddc62b854de351"}

latest = None
if os.path.isdir(echo_dir):
    for back in range(7):
        d = today - timedelta(days=back)
        path = os.path.join(echo_dir, d.strftime("%Y-%m-%d.jsonl"))
        if not os.path.isfile(path):
            continue
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                chat_id = str(entry.get('chatId', '')).lower()
                if chat_id not in COACH_IDS:
                    continue
                ts_ms = entry.get('ts')
                if not ts_ms:
                    continue
                dt = datetime.fromtimestamp(ts_ms / 1000, tz=tz)
                if latest is None or dt > latest:
                    latest = dt

print(latest.strftime('%Y-%m-%dT%H:%M:%S+08:00') if latest else "")
PYEOF
)

# === 逐天往回找，直到找到真的有教練訊息的那一天（最多回溯7天，memory 掃描作為備援） ===
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

# === 取 echo log 與 memory 掃描兩邊「較新」的那個，不因單一來源漏算而錯報沉默 ===
if [[ -n "$ECHO_LAST_DATE" ]]; then
  if [[ -z "$REAL_LAST_DATE" || "$ECHO_LAST_DATE" > "$REAL_LAST_DATE" ]]; then
    REAL_LAST_DATE="$ECHO_LAST_DATE"
  fi
fi

if [[ -z "$REAL_LAST_DATE" ]]; then
  echo "$LOG_PREFIX ⚠️ 回溯7天都找不到真正的教練訊息（echo log + memory 掃描皆無，排除cron/心跳系統注入後）" >&2
  echo "  → 請手動從 Telegram 確認教練最後訊息時間，不要編數字" >&2
  exit 1
fi

echo "$LOG_PREFIX 真正教練最後訊息時間：$REAL_LAST_DATE"

# === 寫回 state（兩份都寫，不確定 agent 實際讀哪一份） ===
python3 << PYEOF
import json, os
from datetime import datetime, timezone, timedelta
tz = timezone(timedelta(hours=8))
real_date_str = "$REAL_LAST_DATE"
real_dt = datetime.fromisoformat(real_date_str)
now_dt = datetime.now(tz)
diff_hours = round((now_dt - real_dt).total_seconds() / 3600, 1)
sync_ts = datetime.now(tz).isoformat()

for state_path in ["$STATE_FILE", "$STATE_FILE_LEGACY"]:
    if os.path.exists(state_path):
        with open(state_path, 'r') as f:
            state = json.load(f)
    else:
        state = {'lastChecks': {}, 'systemSnapshot': {}}

    state.setdefault('systemSnapshot', {})['coachSilentSince'] = real_date_str
    state['systemSnapshot']['coachSilentHours'] = diff_hours
    state.setdefault('lastChecks', {})['coach_silence_sync'] = sync_ts

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

print(f"✅ coachSilentSince = {real_date_str}（已排除cron/心跳系統注入訊息，state/與memory/兩份都已同步）")
print(f"✅ coachSilentHours = {diff_hours}")
PYEOF

exit 0
