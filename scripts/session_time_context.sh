#!/bin/bash
# Session 時間覺察工具（Mac 版）——每次回應前/開工 hook 呼叫
# 對應 Windows session_time_context.ps1
# 用途：避免時間感腦補（v31 接力棒血淚：Windows 軍師把「教練 5 分鐘前說休息」腦補成「睡一整晚」）
# 一律輸出台灣時間（GMT+8）白話文
set -uo pipefail

PROJECT_DIR="/Users/bymyway/.claude/projects/-Users-bymyway--openclaw"

# 找最新 jsonl
LATEST_JSONL=$(ls -t "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1)

if [[ -z "$LATEST_JSONL" || ! -f "$LATEST_JSONL" ]]; then
  echo "[時間覺察] 現在：$(TZ=Asia/Taipei date '+%Y-%m-%d %H:%M:%S')（無 jsonl）"
  exit 0
fi

python3 - "$LATEST_JSONL" <<'PY'
import json, sys
from datetime import datetime, timezone, timedelta

tw = timezone(timedelta(hours=8))
weekday_tw = ['一','二','三','四','五','六','日']

first_ts = None
last_user_ts = None
last_user_preview = None

with open(sys.argv[1]) as f:
    for line in f:
        try:
            d = json.loads(line)
        except Exception:
            continue
        ts = d.get('timestamp')
        if not ts:
            continue
        if first_ts is None:
            first_ts = ts
        is_user = (d.get('type') == 'user' or d.get('message', {}).get('role') == 'user')
        if is_user:
            content = d.get('message', {}).get('content')
            real_text = None
            if isinstance(content, str):
                real_text = content
            elif isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get('type') == 'text':
                        real_text = part.get('text', '')
                        break
            if real_text is not None and real_text.strip():
                last_user_ts = ts
                last_user_preview = real_text.strip()[:30].replace('\n', ' ')

def parse(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(tw)

now = datetime.now(tw)
print(f"[時間覺察 · 台灣時間 GMT+8]")
print(f"  現在：{now.strftime('%Y-%m-%d %H:%M:%S')} 星期{weekday_tw[now.weekday()]}")

if first_ts:
    first = parse(first_ts)
    dur_h = (now - first).total_seconds() / 3600
    print(f"  Session 開始：{first.strftime('%Y-%m-%d %H:%M:%S')}（{dur_h:.1f} 小時前）")

if last_user_ts:
    last = parse(last_user_ts)
    since_min = (now - last).total_seconds() / 60
    if since_min < 1:
        ago = f"{int(since_min*60)} 秒前"
    elif since_min < 60:
        ago = f"{since_min:.1f} 分鐘前"
    else:
        ago = f"{since_min/60:.1f} 小時前"
    preview = f"「{last_user_preview}…」" if last_user_preview else ""
    print(f"  教練上次說話：{last.strftime('%H:%M:%S')}（{ago}）{preview}")
PY
