#!/usr/bin/env python3
"""
distill_terminal_llm.py — 終端機對話自動蒸餾
讀 pending_distill/*.txt，呼叫 MiniMax LLM 蒸餾成精華，寫入 distill/terminal_YYYY-MM-DD.md
處理完的檔案移到 distilled/（留存檔）
軍師建立 2026-05-30
"""
import os
import sys
import json
import shutil
import requests
from datetime import datetime, timezone, timedelta

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
PENDING_DIR = os.path.join(WORKSPACE, "terminal-notes/pending_distill")
DISTILLED_DIR = os.path.join(WORKSPACE, "terminal-notes/distilled")
OUTPUT_DIR = os.path.join(WORKSPACE, "distill")
STATE_FILE = os.path.join(WORKSPACE, "terminal-notes/.distill_llm_state.json")

MINIMAX_BASE_URL = "https://api.minimax.io/anthropic/v1/messages"
MINIMAX_API_KEY = "sk-cp-0_iW72rvuoBmDucQXmRaSAUmcrjXTzZCpIxQt7xgKX_ImdeMkhGmgEV9QBzMNwH87jP-VLIXDNC8VqdgJmntnj5M9gJfTJFiveu9fWuXyQHnW9Z8EQnvlC8"
MODEL = "MiniMax-M3"

TWN = timezone(timedelta(hours=8))

DISTILL_PROMPT = """你是一位蒸餾專家。請把以下終端機對話精華濃縮為 300-500 字的總結。

規則：
1. 教練說的每一句原話，用「👤 教練：」標記完整保留（一字不改）
2. AI 的回應只保留最終結論和關鍵決策，省略中間過程
3. 按時間順序排列
4. 標記 session ID 和日期
5. 如果教練沒說有意義的話（只有「開工」或指令類），直接寫「本 session 為例行開工，無需蒸餾」
6. 跳過系統指令（<local-command>、<command-name> 等標籤內容）
7. 輸出格式為 Markdown

以下是待蒸餾的對話：

"""


def twn_now():
    return datetime.now(TWN)


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"distilled_sessions": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def call_llm(content):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": MINIMAX_API_KEY,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": DISTILL_PROMPT + content}],
    }

    try:
        resp = requests.post(MINIMAX_BASE_URL, headers=headers, json=payload, timeout=120)
        if resp.status_code != 200:
            print(f"  ❌ LLM API 回傳 {resp.status_code}: {resp.text[:200]}")
            return None
        data = resp.json()
        result = data.get("content", [])
        if isinstance(result, list):
            for block in result:
                if block.get("type") == "text" and block.get("text"):
                    return block["text"]
        return None
    except Exception as e:
        print(f"  ❌ LLM 呼叫失敗: {e}")
        return None


def main():
    os.makedirs(DISTILLED_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    state = load_state()
    distilled_set = set(state.get("distilled_sessions", []))
    now_str = twn_now().strftime("%Y-%m-%d %H:%M")
    today_str = twn_now().strftime("%Y-%m-%d")

    print(f"[distill_terminal_llm {now_str}] 掃描 {PENDING_DIR}")

    if not os.path.isdir(PENDING_DIR):
        print(f"[INFO] pending_distill 目錄不存在，結束")
        return

    pending_files = sorted([
        f for f in os.listdir(PENDING_DIR)
        if f.endswith(".txt")
    ])

    if not pending_files:
        print("[INFO] 無待蒸餾檔案，結束")
        return

    print(f"[INFO] 找到 {len(pending_files)} 個待蒸餾檔案")

    success_count = 0
    skip_count = 0

    stale_warnings = []  # 收集卡住的檔案（pending 比 distilled 新但 state 說已蒸餾）

    for fname in pending_files:
        session_id = fname[:-4]
        fpath = os.path.join(PENDING_DIR, fname)

        # 🔴 修復：檢查是否被重新萃取（pending 比 distilled 新）
        distilled_path = os.path.join(DISTILLED_DIR, fname)
        re_extracted = False
        if session_id in distilled_set:
            if os.path.exists(distilled_path):
                pending_mtime = os.path.getmtime(fpath)
                distilled_mtime = os.path.getmtime(distilled_path)
                pending_size = os.path.getsize(fpath)
                distilled_size = os.path.getsize(distilled_path)
                if pending_mtime > distilled_mtime or pending_size > distilled_size * 1.2:
                    re_extracted = True
                    print(f"  ♻️  {session_id[:8]} 偵測到重新萃取（pending {pending_size}B > distilled {distilled_size}B 或 mtime 新），強制重蒸餾")
            if not re_extracted:
                skip_count += 1
                # 檢查是否卡太久（>6 小時）— 可能是 state 與檔案不同步
                age_hours = (os.path.getmtime(fpath) - os.path.getmtime(distilled_path)) / 3600 if os.path.exists(distilled_path) else 999
                if age_hours > 6:
                    stale_warnings.append(f"{session_id[:8]} 卡在 pending {age_hours:.1f} 小時（distilled 已存在但內容可能更舊）")
                continue

        try:
            with open(fpath, encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"  ⚠️ 讀取失敗 {fname}: {e}")
            stale_warnings.append(f"{session_id[:8]} 讀取失敗: {e}")
            continue

        if len(content.strip()) < 50:
            print(f"  ⏭ {session_id[:8]} 內容太短，跳過")
            distilled_set.add(session_id)
            continue

        print(f"  🔄 蒸餾中 {session_id[:8]}...（{len(content)} 字元）")

        distilled = call_llm(content)
        if distilled is None:
            print(f"  ❌ {session_id[:8]} 蒸餾失敗，保留在 pending")
            continue

        output_path = os.path.join(OUTPUT_DIR, f"terminal_{today_str}.md")
        header = f"\n\n---\n## 📍 Session {session_id[:8]}（蒸餾時間 {now_str}）\n\n"

        with open(output_path, "a", encoding="utf-8") as out:
            if os.path.getsize(output_path) == 0:
                out.write(f"# 終端機對話蒸餾 {today_str}\n\n> 自動蒸餾，由 distill_terminal_llm.py 產生\n")
            out.write(header + distilled + "\n")

        shutil.copy2(fpath, os.path.join(DISTILLED_DIR, fname))
        os.remove(fpath)

        distilled_set.add(session_id)
        success_count += 1
        print(f"  ✅ {session_id[:8]} 蒸餾完成 → terminal_{today_str}.md")

    state["distilled_sessions"] = list(distilled_set)
    state["last_run"] = now_str
    state["stale_warnings"] = stale_warnings
    save_state(state)

    # 🔴 犯錯自動入庫：把卡住警告寫到專用 log，教練下次啟動會看到
    if stale_warnings:
        warn_log = "/tmp/distill_stuck_warnings.log"
        with open(warn_log, "a", encoding="utf-8") as f:
            f.write(f"\n=== {now_str} ===\n")
            for w in stale_warnings:
                f.write(f"  ⚠️  {w}\n")
        print(f"[ERROR] 發現 {len(stale_warnings)} 個卡住檔案，已寫入 {warn_log}")
        # 嘗試推 Telegram 通知（如果 openclaw CLI 可用）
        try:
            import subprocess
            msg = f"🦞 蒸餾卡住警報\n\n{now_str}\n" + "\n".join(f"• {w}" for w in stale_warnings)
            subprocess.run(
                ["openclaw", "message", "send", "-t", "6124913915", "-m", msg],
                capture_output=True, timeout=10
            )
        except Exception:
            pass  # 推失敗不影響主流程，下次心跳會被發現

    print(f"[完成] 蒸餾 {success_count} 個，跳過 {skip_count} 個{'，警告 ' + str(len(stale_warnings)) + ' 個' if stale_warnings else ''}")


if __name__ == "__main__":
    main()
