#!/usr/bin/env python3
"""UserPromptSubmit（聯想／Windows）：每句話注入一行台灣時間＋本場開始時間＋教練上次說話。
2026-11-11 賈維斯體檢合併取代 inject_taiwan_time.ps1＋session_time_context.ps1：
  - 兩支 PS 5.1 都沒設輸出編碼→中文整段亂碼、`u{1f550} 印成字面，等於從沒生效
  - session_time_context 每句翻整個 projects 資料夾找「最新 jsonl」→開場抓到別場（說本場 130 小時前開始）
  - 改用 hook 給的 transcript_path（逐行字串快篩，2MB 約 0.1 秒），一行輸出（原本兩支約 600 字）
時間鐵律（教練 2026-06-09）保留成一句：看到結尾 Z 的 ISO 時間＝UTC，+8 再講。
"""
import datetime, json, os, sys

TW = datetime.timezone(datetime.timedelta(hours=8))
WEEK = "一二三四五六日"


def ts(line):
    try:
        t = json.loads(line).get("timestamp")
        return datetime.datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(TW) if t else None
    except Exception:
        return None


def is_user_text(line):
    try:
        o = json.loads(line)
    except Exception:
        return False
    if o.get("type") != "user":
        return False
    c = (o.get("message") or {}).get("content")
    if isinstance(c, str):
        return bool(c.strip())
    return isinstance(c, list) and any(b.get("type") == "text" for b in c) and not any(b.get("type") == "tool_result" for b in c)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        data = {}
    now = datetime.datetime.now(TW)
    parts = [f"🕐 台灣時間 {now:%Y-%m-%d}（{WEEK[now.weekday()]}）{now:%H:%M}"]
    path = data.get("transcript_path") or ""
    try:
        if path and os.path.isfile(path):
            start = last_user = None
            with open(path, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f):
                    if i < 30 and not start:
                        start = ts(line)
                    if '"type":"user"' in line and is_user_text(line):  # 字串快篩，工具輸出佔大宗不解析
                        last_user = ts(line) or last_user
            if start:
                mins = int((now - start).total_seconds() // 60)
                parts.append(f"本場 {start:%m/%d %H:%M} 開始（{mins // 60} 小時 {mins % 60} 分前）" if mins >= 60 else f"本場 {start:%H:%M} 開始（{mins} 分前）")
            if last_user:
                gap = int((now - last_user).total_seconds() // 60)
                parts.append(f"教練上次說話 {last_user:%H:%M}（{gap} 分前）")
    except Exception:
        pass
    print("｜".join(parts) + "。看到結尾 Z 的 ISO 時間＝UTC，+8 再講給教練。")


if __name__ == "__main__":
    main()
