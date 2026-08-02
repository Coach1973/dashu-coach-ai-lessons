#!/usr/bin/env bash
# 教練最後訊息時間真相源 — v3.1 (2026-08-02 教練拍板)
# 用途：任何要寫「教練沉默 N 小時/天」之前，必須先跑這支腳本
#       把教練最後一則訊息時間，從 OpenClaw 自動寫的 memory/YYYY-MM-DD.md
#       找出來，寫回 state/heartbeat-state.json
#       然後才用 `date` 即時算差
#       **禁止**沿用舊 coachSilentHours 數字（8/1/8/2 三次犯錯的根因）
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

CHAT_ID="6124913915"
MEMORY_DIR="$HOME/.openclaw/workspace/memory"
STATE_FILE="$HOME/.openclaw/workspace/state/heartbeat-state.json"
LOG_PREFIX="[sync_coach_last_message]"

# === 第一步：找最新的 memory 檔 ===
LATEST_MEMORY=""
if [[ -d "$MEMORY_DIR" ]]; then
  # 找最後修改且檔名是 YYYY-MM-DD.md 的檔
  LATEST_MEMORY=$(find "$MEMORY_DIR" -maxdepth 1 -name "20[0-9][0-9]-[0-1][0-9]-[0-3][0-9].md" -type f 2>/dev/null \
    | xargs ls -t 2>/dev/null \
    | head -1)
fi

if [[ -z "$LATEST_MEMORY" || ! -f "$LATEST_MEMORY" ]]; then
  echo "$LOG_PREFIX ⚠️ 找不到最新 memory 檔（$MEMORY_DIR/YYYY-MM-DD.md）" >&2
  echo "  → 請從 Telegram 手動查教練最後訊息時間" >&2
  exit 1
fi

echo "$LOG_PREFIX 使用 memory 檔：$LATEST_MEMORY"

# === 第二步：從 memory 檔中找出教練最後一則訊息 ===
# 教練訊息的特徵：「👤 教練：」開頭（OpenClaw note-taker 統一格式）
REAL_LAST_DATE=$(python3 << PYEOF
import re, os, json
from datetime import datetime, timezone, timedelta

memory_path = "$LATEST_MEMORY"
tz = timezone(timedelta(hours=8))

# 讀檔，找出所有「👤 教練：[...]  或 👤 教練：YYYY-MM-DD HH:MM」這類時間戳
# 然後挑最大（最新）那一個
with open(memory_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 模式 1：OpenClaw note-taker 的對話紀錄格式：「🕐 HH:MM」「📅 YYYY-MM-DD HH:MM」「👤 教練：」
# 例如：「🕐 14:45」或「Sun 2026-08-02 14:45:25 GMT+8」
time_patterns = [
    # match "[Day] YYYY-MM-DD HH:MM[:SS] GMT+8"
    (r'(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})\s*GMT\+8', 'full_with_sec'),
    (r'(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})\s*GMT\+8', 'full_minute'),
    # match \"HH:MM\" 單獨出現
    (r'🕐\s*(\d{2}):(\d{2})', 'short'),
    # 對話記錄區塊：「👤 教練：[Ymd] HH:MM」常見格式
    (r'## 📨 對話記錄 (\d{2}):(\d{2})', 'section'),
]

# 取檔案中所有 timestamp，找最大的（最新）
all_ts = []

# 完整時間戳（最可靠）
for pat, kind in time_patterns:
    for m in re.finditer(pat, content):
        try:
            if kind == 'full_with_sec':
                dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                              int(m.group(4)), int(m.group(5)), int(m.group(6)), tzinfo=tz)
            elif kind == 'full_minute':
                dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                              int(m.group(4)), int(m.group(5)), 0, tzinfo=tz)
            elif kind == 'short':
                # 只取檔案日期 + 時分
                file_date = datetime.fromtimestamp(os.path.getmtime(memory_path), tz).date()
                dt = datetime(file_date.year, file_date.month, file_date.day,
                              int(m.group(1)), int(m.group(2)), 0, tzinfo=tz)
            elif kind == 'section':
                file_date = datetime.fromtimestamp(os.path.getmtime(memory_path), tz).date()
                dt = datetime(file_date.year, file_date.month, file_date.day,
                              int(m.group(1)), int(m.group(2)), 0, tzinfo=tz)
            all_ts.append(dt)
        except Exception:
            pass

if not all_ts:
    print("")
else:
    # 挑最大的（最新）
    latest = max(all_ts)
    print(latest.strftime('%Y-%m-%dT%H:%M:%S+08:00'))
PYEOF
)

if [[ -z "$REAL_LAST_DATE" ]]; then
  echo "$LOG_PREFIX ⚠️ 從 $LATEST_MEMORY 找不到任何教練訊息時間戳" >&2
  echo "  → 檔案可能太小或格式異常，請手動確認" >&2
  exit 1
fi

# === 第三步：寫回 state ===
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
try:
    real_dt = datetime.fromisoformat(real_date_str)
    now_dt = datetime.now(tz)
    diff_hours = round((now_dt - real_dt).total_seconds() / 3600, 1)
    state['systemSnapshot']['coachSilentHours'] = diff_hours
except Exception as e:
    print(f"計算差時數失敗: {e}")

# 記錄這次同步時間
state.setdefault('lastChecks', {})['coach_silence_sync'] = datetime.now(tz).isoformat()

with open(state_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"✅ coachSilentSince = {real_date_str}")
print(f"✅ coachSilentHours = {state['systemSnapshot'].get('coachSilentHours', '?')} （即時算）")
PYEOF

exit 0
