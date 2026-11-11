#!/usr/bin/env python3
"""查 Claude 訂閱額度（教練問「流量使用情況」時跑這支）。2026-11-11 建。
用鑰匙圈裡 Claude Code 的登入憑證打 oauth/usage，印白話：5 小時、7 天用了幾 %、台灣時間幾點重置。不印憑證。"""
import json, subprocess, urllib.request
from datetime import datetime, timezone, timedelta
raw = subprocess.run(["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
                     capture_output=True, text=True, check=True).stdout
tok = json.loads(raw)["claudeAiOauth"]["accessToken"]
req = urllib.request.Request("https://api.anthropic.com/api/oauth/usage",
                             headers={"Authorization": "Bearer " + tok, "anthropic-beta": "oauth-2025-04-20"})
d = json.load(urllib.request.urlopen(req, timeout=20))
tw = timezone(timedelta(hours=8))
for key, name in (("five_hour", "5 小時額度"), ("seven_day", "本週額度")):
    v = d.get(key) or {}
    if v.get("utilization") is None:
        continue
    t = datetime.fromisoformat(v["resets_at"]).astimezone(tw).strftime("%m/%d %H:%M")
    print(f"{name}：已用 {v['utilization']:.0f}%，台灣時間 {t} 重置")
