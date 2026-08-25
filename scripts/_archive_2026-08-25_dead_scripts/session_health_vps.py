#!/usr/bin/env python3
"""
Session 健康度檢查 — VPS赫茲米專用版

這是赫茲米 VPS 的蒸餾 cron job 的一部分，
在每次 distill 蒸餾完成後，自動檢查 session 健康度。

使用方式（由 systemd timer 或 cron 觸發）：
  python3 /root/.hermes/github-sync/scripts/session_health_vps.py

輸出寫入日誌：
  /root/.hermes/github-sync/distill/distill.log

⚠️ 赫茲米沒有直接計數 CLI 對話輪數，
本腳本用「上次蒸餾到現在的時間」來推估：
  - 蒸餾間隔 < 2小時 → 假設 session 仍有內容
  - 蒸餾間隔 > 6小時 → 建議 reload
"""

import os
import sys
import json
import glob
from datetime import datetime, timedelta

# ─── 設定 ───────────────────────────────────────────────
DISTILL_LOG = '/root/.hermes/github-sync/distill/distill.log'
SESSION_COUNTER = '/root/.hermes/github-sync/distill/session_count.json'
MEMORY_DIR = '/root/.hermes/github-sync/memory'

# 門檻（赫茲米蒸餾 session）
VPS_THRESHOLDS = {
    'green': (0, 15),      # 🟢 正常
    'yellow': (16, 25),     # 🟡 警戒
    'orange': (26, 40),     # 🟠 警告
    'red': (41, 60),       # 🔴 危急
    'critical': (61, 9999), # 🚨 已超載
}

def get_status(turns):
    for status in ('critical', 'red', 'orange', 'yellow', 'green'):
        lo, hi = VPS_THRESHOLDS[status]
        if lo <= turns <= hi:
            return status
    return 'green'

def read_counter():
    """讀取蒸餾輪數計數器"""
    try:
        if os.path.exists(SESSION_COUNTER):
            with open(SESSION_COUNTER) as f:
                data = json.load(f)
                return data.get('count', 0)
    except:
        pass
    return 0

def increment_counter():
    """每次蒸餾後呼叫，計數器+1"""
    try:
        count = read_counter()
        count += 1
        with open(SESSION_COUNTER, 'w') as f:
            json.dump({'count': count, 'updated': datetime.now().isoformat()}, f)
        return count
    except:
        return None

def reset_counter():
    """Session reload 時呼叫，重置計數器"""
    try:
        with open(SESSION_COUNTER, 'w') as f:
            json.dump({'count': 0, 'updated': datetime.now().isoformat()}, f)
        return 0
    except:
        return None

def last_distill_time():
    """讀取上次蒸餾時間（從 distill.log 最後一行）"""
    try:
        if os.path.exists(DISTILL_LOG):
            with open(DISTILL_LOG) as f:
                lines = f.readlines()
            for line in reversed(lines):
                # 找時間戳記 "2026-05-25 10:30:00"
                if len(line) > 18 and line[0:4].isdigit():
                    return datetime.fromisoformat(line[:19])
    except:
        pass
    return None

def check_and_log():
    """主要檢查並寫入日誌"""
    turns = read_counter()
    status = get_status(turns)
    last_dist = last_distill_time()
    emoji = {'green': '🟢', 'yellow': '🟡', 'orange': '🟠', 'red': '🔴', 'critical': '🚨'}

    lines = [f"[Session健康度] {emoji[status]} #{turns}輪"]
    action = None

    if status == 'green':
        lines.append(f"✅ 正常")
    elif status == 'yellow':
        lines.append(f"💡 已{turns}輪，建議下次蒸餾後reload")
        action = "watch"
    elif status == 'orange':
        lines.append(f"⚠️ 即將超載，應立即蒸餾並reload")
        action = "warn"
    elif status == 'red':
        lines.append(f"🚨 超載，需立即reload")
        action = "urgent"
    else:
        lines.append(f"💥 已過度壓縮，內容可能已損失")
        action = "critical"

    if last_dist:
        ago = datetime.now() - last_dist
        lines.append(f"(上次蒸餾：{int(ago.total_seconds()/60)}分鐘前)")

    msg = ' '.join(lines)
    print(msg)

    # 寫入日誌
    try:
        os.makedirs(os.path.dirname(DISTILL_LOG), exist_ok=True)
        with open(DISTILL_LOG, 'a') as f:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{ts} {msg}\n")
    except:
        pass

    return action

def main():
    args = sys.argv[1:]

    if '--reset' in args:
        c = reset_counter()
        print(f"計數器已重置（{c}）")
        return

    if '--inc' in args:
        c = increment_counter()
        print(f"計數器+1 → {c}")
        check_and_log()
        return

    # 預設：檢查並回報
    check_and_log()

if __name__ == '__main__':
    main()