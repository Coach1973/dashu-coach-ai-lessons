#!/bin/bash
# Hermes(Mac桌面版) gateway卡住自動偵測+重啟（2026-09-08教練交辦）
#
# 背景：教練回報手機Telegram傳訊給Hermes沒反應，已出現多次。查證發現Hermes的
# gateway process(ai.hermes.gateway，launchd KeepAlive管理)可能在不crash的情況下
# 內部事件迴圈卡死——process還活著、launchd看不出異常所以不會重啟，但Telegram
# 訊息處理迴圈已經停擺。gateway.log最後一筆活動停在04:00，直到教練10:38發現
# 沒反應，已經卡了6.5小時沒人知道。
#
# 解法：Hermes自己會把event loop存活訊號寫進gateway.heartbeat(每~30秒更新一次，
# 跟訊息量無關，比對gateway.log活動更精準——沒訊息不代表卡住，但heartbeat該跳
# 卻沒跳就是真卡住)。這支腳本檢查heartbeat新鮮度，太久沒更新就強制重啟。
#
# 由launchd每5分鐘觸發一次(ai.hermes.gateway-watchdog.plist)，非本腳本自己輪詢。

HEARTBEAT_FILE="/Users/bymyway/.hermes/state/gateway.heartbeat"
LOG_FILE="/Users/bymyway/.openclaw/workspace/logs/hermes_gateway_watchdog.log"
THRESHOLD_SECONDS=300

mkdir -p "$(dirname "$LOG_FILE")"

python3 - "$HEARTBEAT_FILE" "$THRESHOLD_SECONDS" <<'PYEOF' >> "$LOG_FILE" 2>&1
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

heartbeat_file, threshold = sys.argv[1], int(sys.argv[2])
now = datetime.now(timezone.utc)


def log(msg: str) -> None:
    print(f"[{now.isoformat(timespec='seconds')}] {msg}")


stale = False
reason = ""
if not os.path.isfile(heartbeat_file):
    stale = True
    reason = "heartbeat檔案不存在"
else:
    try:
        data = json.loads(open(heartbeat_file, encoding="utf-8").read())
        updated_at = datetime.fromisoformat(data["updated_at"])
        age = (now - updated_at).total_seconds()
        if age > threshold:
            stale = True
            reason = f"heartbeat已{age:.0f}秒沒更新(門檻{threshold}秒)"
    except Exception as e:  # noqa: BLE001
        stale = True
        reason = f"heartbeat檔案讀取失敗: {e!r}"

if not stale:
    sys.exit(0)

log(f"⚠️ 偵測到Hermes gateway卡住：{reason}，執行強制重啟")
subprocess.run(
    ["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/ai.hermes.gateway"],
    check=False,
)
log("✅ 已送出launchctl kickstart -k重啟指令")

try:
    with open(os.path.expanduser("~/.openclaw/openclaw.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    token = cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
    text = (
        "🔧 偵測到Hermes(Mac桌面版)gateway卡住已自動重啟\n"
        f"原因：{reason}\n"
        "如果剛才有交辦Hermes做事，可能需要重新確認進度。"
    )
    body = json.dumps({"chat_id": "6124913915", "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, method="POST", headers={"Content-Type": "application/json"},
    )
    urllib.request.urlopen(req, timeout=10)
    log("✅ 已通知教練")
except Exception as e:  # noqa: BLE001
    log(f"⚠️ 通知教練失敗（不影響重啟本身）: {e!r}")
PYEOF
