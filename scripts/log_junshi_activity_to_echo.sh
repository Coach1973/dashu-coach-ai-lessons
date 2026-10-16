#!/bin/bash
# Hook：UserPromptSubmit（終端機/桌面版 軍師 專用）
# 用途：教練 2026-08-07 拍板——只要有跟軍師互動，就算「教練有在跟小龍蝦系統互動」，
#       不要讓小龍蝦誤以為教練好幾天沒理它（其實教練正在用軍師這條線處理事情）。
#       每則教練發給軍師的訊息，都同步寫一筆進 state/inbound_echo/YYYY-MM-DD.jsonl
#       （跟 hooks/inbound-message-echo-log 寫的是同一份檔案格式，
#       sync_coach_last_message.sh 已經會讀這份檔案，不用再改那支腳本）。
# 範圍：教練親口選「不限，只要是跟軍師互動就算」——不篩選內容，每輪都記。
set -uo pipefail

INPUT=$(cat)
PROMPT=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.prompt // ""' 2>/dev/null)

[[ -z "$PROMPT" ]] && exit 0

ECHO_DIR="$HOME/.openclaw/workspace/state/inbound_echo"
mkdir -p "$ECHO_DIR"

PROMPT_TEXT="$PROMPT" ECHO_DIR="$ECHO_DIR" /usr/bin/python3 <<'PYEOF'
import json, os, re, time
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
echo_dir = os.environ.get("ECHO_DIR", "")
today_file = os.path.join(echo_dir, now.strftime("%Y-%m-%d.jsonl"))

# 2026-10-16 教練貼機器人金鑰被原樣記進這份檔（會被自動同步推上 GitHub）：寫入前先遮蔽常見金鑰格式。
# 先對整句遮蔽再截 200 字，避免金鑰剛好被截斷而漏網。
SECRET_PATTERNS = [
    re.compile(r"[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{5,8}\.[A-Za-z0-9_-]{25,}"),  # Discord 機器人金鑰／JWT
    re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}"),                                # Telegram 機器人金鑰
    re.compile(r"\b(?:sk|pk|rk)-[A-Za-z0-9_-]{20,}"),                             # sk- 開頭的 API 金鑰
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}"),                                  # GitHub token
]


def mask_secrets(text):
    for pat in SECRET_PATTERNS:
        text = pat.sub("[金鑰已遮蔽]", text)
    return text


entry = {
    "ts": int(time.time() * 1000),
    "iso": now.isoformat(),
    "agentId": "junshi",
    "channel": "junshi-terminal",
    "chatId": "6124913915",
    "source": "junshi-relay",
    "text": mask_secrets(os.environ.get("PROMPT_TEXT", ""))[:200],
}

try:
    with open(today_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
except Exception:
    pass
PYEOF

exit 0
