#!/bin/bash
# Hook：UserPromptSubmit — 時間注入（合併版，2026-08-12 全面體檢後）
#
# 取代原本兩支各自啟動的腳本：
#   inject_taiwan_time.sh   （時間鐵律 + 當下台灣時間）
#   session_time_context.sh （session 開始多久、教練上次說話多久前）
#
# 為什麼要改：
#   1. inject_taiwan_time.sh 原本「每則訊息」都把 5 行時間鐵律全文重貼一次，
#      對話越長重複越多次，白白吃掉 context。教練 2026-08-12 全面體檢時抓到。
#      → 改成規則全文「每場 session 只講一次」（marker 防重），之後只留一行當下時間。
#   2. 兩支都在講時間，合併成一支可以少啟動一個程序。
#
# 保留不變：時間鐵律原文一字不差（教練 2026-06-09 親罵後寫死的內容不動），
#          每則訊息仍然看得到「當下台灣時間」跟「教練上次說話多久前」。
#
# 原本兩支腳本保留在本目錄不刪除，可比對／可回退。
set -uo pipefail

INPUT=$(cat 2>/dev/null || true)
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
TRANSCRIPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)

# 強制 Asia/Taipei，不管系統時區是什麼
TW_NOW=$(TZ='Asia/Taipei' date '+%Y-%m-%d %A %H:%M:%S')

# ── 第一段：時間鐵律全文（每場 session 只講一次）──────────────
MARKER="/tmp/time_rule_injected_${SESSION_ID:-nosession}"
if [[ ! -f "$MARKER" ]]; then
  touch "$MARKER" 2>/dev/null || true
  cat <<INJECT
🕐 **當下台灣時間：${TW_NOW}（GMT+8）**

🔴 **時間鐵律（教練 2026-06-09 親罵後寫死，違反 = 守則 #07 同處跌倒）**：
- 跟教練講時間 → **永遠先換算成台灣時間**（Asia/Taipei，UTC+8）
- 看到 ISO 字串「\`2026-06-09T06:25:36.752Z\`」→ Z = UTC → **+8 變 14:25:36（下午 2:25）**
- 禁止口語講「06:24」「06:25」等 Z 時間——這是 UTC，不是台灣時間
- 對教練講「上午 6 點半」「下午 2 點半」用白話，不用 24 小時制更好
（本規則每場對話只提示一次，之後只報當下時間）
INJECT
else
  printf '🕐 **當下台灣時間：%s（GMT+8）**\n' "$TW_NOW"
fi

# ── 第二段：session 時間覺察（每則訊息都要，內容會變動）────────
# 用途：避免時間感腦補（v31 接力棒血淚：Windows 軍師把「教練 5 分鐘前說休息」
#       腦補成「睡一整晚」）。一律輸出台灣時間（GMT+8）白話文。
PROJECT_DIR="/Users/bymyway/.claude/projects/-Users-bymyway--openclaw"

# 優先用本場 session 自己的對話檔（教練常同時開多個視窗，抓「最新 mtime」
# 可能抓到別場的檔案）；payload 沒給才退回原本的「找最新 jsonl」邏輯
TARGET_JSONL="$TRANSCRIPT"
if [[ -z "$TARGET_JSONL" || ! -f "$TARGET_JSONL" ]]; then
  TARGET_JSONL=$(ls -t "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1)
fi

if [[ -z "$TARGET_JSONL" || ! -f "$TARGET_JSONL" ]]; then
  exit 0
fi

python3 - "$TARGET_JSONL" <<'PY'
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

exit 0
