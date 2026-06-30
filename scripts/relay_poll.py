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
    # 2026-06-30 修：原本 marker 找到就 break+覆蓋，會把 marker 之後的教練待辦砍光。
    # 改：找到 marker 後不 break；若今天那行 (### YYYY-MM-DD) 已存在就替換、不存在就 append。
    # 學長體檢 P0-1 找出此 bug（症狀：09:17、09:20、18:29 三次教練待辦被吃掉）
    date_prefix = f"### {datetime.now().strftime('%Y-%m-%d')}"
    new_entry = f"{date_prefix} {ts} - relay poll OK"

    if marker not in content:
        content = content.rstrip('\n') + f"\n\n{marker}\n{new_entry}\n"
    else:
        lines = content.split('\n')
        out = []
        in_block = False
        today_replaced = False
        for line in lines:
            if marker in line:
                in_block = True
                out.append(line)
                continue
            if in_block:
                # 區塊結束條件：遇到下一個 ## heading
                if line.startswith('## ') and marker not in line:
                    if not today_replaced:
                        out.append(new_entry)
                        today_replaced = True
                    in_block = False
                    out.append(line)
                    continue
                # 區塊內找今天那行，存在則替換成當下時間
                if line.startswith(date_prefix):
                    if not today_replaced:
                        out.append(new_entry)
                        today_replaced = True
                    # 重複的今天行（保險）直接 skip
                    continue
            out.append(line)
        # 檔尾仍在 marker 區塊（沒下一個 ## heading）
        if in_block and not today_replaced:
            out.append(new_entry)
        content = '\n'.join(out)
        if not content.endswith('\n'):
            content += '\n'
    
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
