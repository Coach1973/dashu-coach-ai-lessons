#!/usr/bin/env python3
"""
LINE@「教練都在想什麼」使用情況回報
- 來源：/Users/bymyway/.openclaw/agents/jiaolian_thoughts/sessions/*.jsonl
- 對齊 Asia/Taipei（UTC+8）
- 輸出：純文字報告（給小龍蝦貼 Telegram 用）
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# ===== 設定 =====
SESSIONS_DIR = "/Users/bymyway/.openclaw/agents/jiaolian_thoughts/sessions"
TZ = timezone(timedelta(hours=8))  # Asia/Taipei
NOW = datetime.now(TZ)
TODAY_START = NOW.replace(hour=0, minute=0, second=0, microsecond=0)
YESTERDAY_START = TODAY_START - timedelta(days=1)
MONTH_START = NOW.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
SEVEN_DAYS_AGO = NOW - timedelta(days=7)


def collect_sessions():
    sessions = {}
    for fn in os.listdir(SESSIONS_DIR):
        if not fn.endswith(".jsonl") or ".trajectory" in fn:
            continue
        sid = fn.replace(".jsonl", "")
        info = {
            "sid": sid,
            "session_start": None,
            "user_messages": 0,
            "first_user_at": None,
            "last_user_at": None,
            "last_any_at": None,
        }
        with open(os.path.join(SESSIONS_DIR, fn)) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                ts = obj.get("timestamp")
                if not ts:
                    continue
                try:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)
                except Exception:
                    continue
                if info["last_any_at"] is None or dt > info["last_any_at"]:
                    info["last_any_at"] = dt
                t = obj.get("type")
                if t == "session":
                    if info["session_start"] is None or dt < info["session_start"]:
                        info["session_start"] = dt
                elif t == "message":
                    msg = obj.get("message", {})
                    if isinstance(msg, dict) and msg.get("role") == "user":
                        info["user_messages"] += 1
                        if info["first_user_at"] is None or dt < info["first_user_at"]:
                            info["first_user_at"] = dt
                        if info["last_user_at"] is None or dt > info["last_user_at"]:
                            info["last_user_at"] = dt
        sessions[sid] = info
    return sessions


def fmt_dt(dt):
    if dt is None:
        return "—"
    return dt.strftime("%m-%d %H:%M")


def main():
    sessions = collect_sessions()

    today_sessions = []  # 今日有新對話
    yesterday_sessions = []
    seven_day_sessions = []
    month_sessions = []
    today_user_msgs = 0
    yesterday_user_msgs = 0
    seven_day_user_msgs = 0
    month_user_msgs = 0
    last_activity = None

    for info in sessions.values():
        if info["session_start"] is None:
            continue
        if info["session_start"] >= TODAY_START:
            today_sessions.append(info)
            today_user_msgs += info["user_messages"]
        elif info["session_start"] >= YESTERDAY_START:
            yesterday_sessions.append(info)
            yesterday_user_msgs += info["user_messages"]
        if info["session_start"] >= SEVEN_DAYS_AGO:
            seven_day_sessions.append(info)
            seven_day_user_msgs += info["user_messages"]
        if info["session_start"] >= MONTH_START:
            month_sessions.append(info)
            month_user_msgs += info["user_messages"]
        if info["last_user_at"] and (last_activity is None or info["last_user_at"] > last_activity):
            last_activity = info["last_user_at"]

    total_sessions = len([s for s in sessions.values() if s["session_start"]])

    report = []
    report.append("📊 LINE@「教練都在想什麼」使用情況")
    report.append(f"🕐 回報時間：{NOW.strftime('%Y-%m-%d %H:%M')}（台北）")
    report.append("")
    report.append("📈 今日（00:00 至今）")
    report.append(f"  • 新對話：{len(today_sessions)} 人 / {today_user_msgs} 則訊息")
    report.append("📈 昨日（整日）")
    report.append(f"  • 新對話：{len(yesterday_sessions)} 人 / {yesterday_user_msgs} 則訊息")
    report.append("📈 近 7 日")
    report.append(f"  • 新對話：{len(seven_day_sessions)} 人 / {seven_day_user_msgs} 則訊息")
    report.append(f"📅 本月累計（{MONTH_START.strftime('%m/%d')} 至今）")
    report.append(f"  • 新對話：{len(month_sessions)} 人 / {month_user_msgs} 則訊息")
    report.append(f"🗄 總累積對話數：{total_sessions} 場")
    report.append(f"⏰ 最後一則訊息：{fmt_dt(last_activity)}")
    report.append("")

    # 列出最近 5 場對話
    recent = sorted(
        [s for s in sessions.values() if s["session_start"]],
        key=lambda x: x["session_start"],
        reverse=True,
    )[:5]
    if recent:
        report.append("🔍 最近 5 場對話：")
        for s in recent:
            start = fmt_dt(s["session_start"])
            n = s["user_messages"]
            last = fmt_dt(s["last_user_at"])
            report.append(f"  • {start}  起，{n} 則訊息，最後 {last}")
        report.append("")

    note = NOW.strftime("%Y-%m-%d")
    if len(today_sessions) == 0 and len(yesterday_sessions) == 0:
        report.append("💤 教練都在想什麼 過去 24 小時無新對話。")
    elif last_activity and (NOW - last_activity).total_seconds() > 6 * 3600:
        gap = NOW - last_activity
        hours = int(gap.total_seconds() // 3600)
        report.append(f"⚠️ 已 {hours} 小時無新訊息（最後一則 {fmt_dt(last_activity)}）")

    print("\n".join(report))


if __name__ == "__main__":
    main()
