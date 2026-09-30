#!/usr/bin/env python3
"""開工注入用：列出最近24小時教練跟其他AI（小龍蝦各頻道、Hermes桌面版）說過的話。

2026-09-30 起因：教練早上叫Hermes、小龍蝦跑產業鏈SOP都出包，下午軍師開工，
開工六步卻完全看不到這些事——memory/HEARTBEAT都沒人寫，接力棒也沒人交。
所以不靠別的AI記得交接，直接讀它們的原始對話記錄。
"""
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path

HOURS = 24
MAX_ROWS = 15
WIDTH = 90
now = time.time()
since = now - HOURS * 3600
rows = []

echo_dir = Path.home() / ".openclaw" / "workspace" / "state" / "inbound_echo"
for day_file in sorted(echo_dir.glob("*.jsonl"))[-2:]:
    for line in day_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        ts = rec.get("ts", 0) / 1000
        # junshi＝軍師自己（Claude Code），不是「其他AI」
        if ts < since or rec.get("agentId") == "junshi":
            continue
        text = rec.get("text", "")
        # 去掉「[Telegram coach id:... GMT+8] coach: 」這種頻道前綴
        if "] " in text[:120]:
            text = text.split("] ", 1)[1]
        rows.append((ts, f"小龍蝦/{rec.get('agentId', '?')}/{rec.get('channel', '?')}", text))

hermes_db = Path.home() / ".hermes" / "state.db"
if hermes_db.is_file():
    try:
        con = sqlite3.connect(f"file:{hermes_db}?mode=ro", uri=True, timeout=2)
        for ts, content in con.execute(
            "select timestamp, content from messages where role='user' and timestamp>=? order by timestamp",
            (since,),
        ):
            # Hermes排程任務自己送的指令不是教練說的話
            if (content or "").startswith("[IMPORTANT: You are running as a scheduled cron job"):
                continue
            rows.append((ts, "Hermes桌面版", content or ""))
        con.close()
    except sqlite3.Error as e:
        print(f"（Hermes記錄讀取失敗：{e}）")

if not rows:
    print("（最近24小時教練沒有跟其他AI說話）")
else:
    rows.sort()
    if len(rows) > MAX_ROWS:
        print(f"（共{len(rows)}則，只列最近{MAX_ROWS}則）")
    for ts, who, text in rows[-MAX_ROWS:]:
        one_line = " ".join(text.split())
        if len(one_line) > WIDTH:
            one_line = one_line[:WIDTH] + "…"
        print(f"- {datetime.fromtimestamp(ts).strftime('%m-%d %H:%M')}［{who}］{one_line}")
