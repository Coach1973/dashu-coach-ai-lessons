#!/bin/bash
# sync_cron_models.sh
# 用途：把 main agent 的模型同步到所有啟用中的 cron，避免「session 跑 M3 但 cron 還在 M2.7」這種資訊不同步
# 觸發：每小時執行一次（由 cron 排程，見 CRON_ID）
# 建立：2026-06-05 教練發現 M2.7→M3 沒同步後，立刻建立

set -e

# === 設定 ===
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.openclaw/workspace/state/sync_cron_models.log"
AGENT_ID="main"
STATE_DIR="$HOME/.openclaw/workspace/state"
mkdir -p "$STATE_DIR"

# 取得目前時間戳記
TS=$(date '+%Y-%m-%d %H:%M:%S')

# === 步驟一：讀取 main agent 的目標模型 ===
TARGET_MODEL=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        d = json.load(f)
    for a in d.get('agents', {}).get('list', []):
        if a.get('id') == '$AGENT_ID':
            print(a.get('model', ''))
            break
except Exception as e:
    print(f'ERROR:{e}', file=__import__('sys').stderr)
    exit(1)
" 2>/dev/null)

if [ -z "$TARGET_MODEL" ] || [[ "$TARGET_MODEL" == ERROR:* ]]; then
    echo "[$TS] ❌ 讀不到 main agent 的模型，停止同步" | tee -a "$LOG_FILE"
    exit 1
fi

echo "[$TS] 🎯 目標模型：$TARGET_MODEL" >> "$LOG_FILE"

# === 步驟二：列出所有啟用中的 cron ===
CRON_JSON=$(openclaw cron list --json --agent "$AGENT_ID" 2>/dev/null)
if [ -z "$CRON_JSON" ]; then
    echo "[$TS] ❌ openclaw cron list 失敗" | tee -a "$LOG_FILE"
    exit 1
fi

# === 步驟三：找出需要同步的 cron，並更新 ===
SYNCED=0
UNCHANGED=0
SKIPPED=0
SYNCED_NAMES=()

echo "$CRON_JSON" | python3 -c "
import json, sys, subprocess

d = json.load(sys.stdin)
target_model = '$TARGET_MODEL'
synced = 0
unchanged = 0
skipped = 0
synced_names = []

for job in d.get('jobs', []):
    if not job.get('enabled'):
        continue
    payload = job.get('payload') or {}
    cur = payload.get('model')
    jid = job['id']
    name = job.get('name', jid)
    kind = payload.get('kind', 'systemEvent')
    if kind != 'agentTurn':
        skipped += 1
        continue
    if cur == target_model:
        unchanged += 1
        continue
    # 需要更新
    try:
        result = subprocess.run(
            ['openclaw', 'cron', 'edit', jid, '--model', target_model],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            synced += 1
            synced_names.append(f'{name}（{cur}→{target_model}）')
        else:
            print(f'  ❌ {name}: {result.stderr.strip()}', file=sys.stderr)
    except Exception as e:
        print(f'  ❌ {name}: {e}', file=sys.stderr)

print(f'synced={synced} unchanged={unchanged} skipped={skipped}')
for n in synced_names:
    print(f'  - {n}')
" >> "$LOG_FILE" 2>&1

# === 步驟四：統計結果 ===
RESULT=$(tail -10 "$LOG_FILE" | grep -E "^synced=" | tail -1)
echo "[$TS] ✅ 同步完成：$RESULT" >> "$LOG_FILE"

# === 步驟五：如果有同步，輸出 announce 訊息（給 cron 用） ===
SYNCED_COUNT=$(echo "$RESULT" | sed -n 's/.*synced=\([0-9]*\).*/\1/p')
if [ "$SYNCED_COUNT" -gt 0 ] 2>/dev/null; then
    cat <<EOF
🔄 cron 模型自動同步完成

目標模型：$TARGET_MODEL
本次同步 $SYNCED_COUNT 個任務

詳見：$LOG_FILE
EOF
fi
