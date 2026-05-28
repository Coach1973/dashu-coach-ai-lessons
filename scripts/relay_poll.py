#!/opt/homebrew/bin/python3
"""
relay_poll.py — 學弟/學妹 讀取學長的 RELAY_QUEUE 並執行任務
觸發：學弟 OpenClaw cron（每10秒）+ 系統 crontab（每分鐘 backup）
用途：學弟收到學長指派任務後，從 relay queue 讀取並執行
路徑：~/.openclaw/workspace/scripts/relay_poll.py
設計：Hao Chen，2026-05-24（軍師重建）
"""
import json
import sys
import os
from datetime import datetime

# 路徑設定（集中在這裡，方便學弟學妹各自修改）
WS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # scripts/.. = workspace
RELAY_QUEUE = os.path.join(WS_DIR, "shared-context", "RELAY_QUEUE.json")
HEARTBEAT = os.path.join(WS_DIR, "HEARTBEAT.md")
LOG_DIR = "/tmp"

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] relay_poll: {msg}")

def record_heartbeat(workspace_name):
    """記錄心跳到 HEARTBEAT.md"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    marker = f"## {workspace_name} relay poll"
    try:
        with open(HEARTBEAT, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
    except FileNotFoundError:
        content = f"# {workspace_name} HEARTBEAT\n"
    
    # 追加 relay poll 心跳（每天一個區段）
    date_marker = f"### {datetime.now().strftime('%Y-%m-%d')}"
    new_entry = f"{date_marker} {ts} - relay poll OK\n"
    
    if marker not in content:
        content += f"\n{marker}\n{new_entry}"
    else:
        lines = content.split('\n')
        out = []
        in_block = False
        for line in lines:
            out.append(line)
            if marker in line:
                in_block = True
                out.append(new_entry)
                break
        content = '\n'.join(out) + '\n'
    
    try:
        with open(HEARTBEAT, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        log(f"HB 寫入失敗: {e}")

def process_queue():
    """處理 RELAY_QUEUE 任務"""
    if not os.path.exists(RELAY_QUEUE):
        return  # 沒有 queue 就安靜退出
    
    try:
        with open(RELAY_QUEUE, "r") as f:
            queue = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return
    
    tasks = queue.get("tasks", [])
    if not tasks:
        return
    
    completed = 0
    for task in tasks:
        if task.get("status") == "pending":
            # 標記為 processing
            task["status"] = "processing"
            task["processed_at"] = datetime.now().isoformat()
            completed += 1
    
    if completed > 0:
        with open(RELAY_QUEUE, "w") as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        log(f"處理了 {completed} 個 pending 任務")

def main():
    workspace_name = os.path.basename(os.path.dirname(WS_DIR))
    # 從路徑猜 workspace 名稱（學弟=.openclaw-kong, 學妹=.openclaw-peipei, 學長=.openclaw）
    if "kong" in WS_DIR:
        workspace_name = "學弟"
    elif "peipei" in WS_DIR:
        workspace_name = "學妹"
    else:
        workspace_name = "學長"
    
    process_queue()
    record_heartbeat(workspace_name)

if __name__ == "__main__":
    main()
