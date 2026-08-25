#!/usr/bin/env python3
"""
distill_all_complete.py — 把 done_distill/ 全部 88 個 session 通過 MiniMax 蒸餾
輸出到 distill/terminal_2026-05-30_complete.md（完整版，不覆蓋 manual 版）
"""
import os, json, shutil, requests, time
from datetime import datetime, timezone, timedelta

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
DONE_DIR  = os.path.join(WORKSPACE, "terminal-notes/done_distill")
OUTPUT    = os.path.join(WORKSPACE, "distill/terminal_2026-05-30_complete.md")
STATE_FILE= os.path.join(WORKSPACE, "terminal-notes/.distill_complete_state.json")

MINIMAX_BASE_URL = "https://api.minimax.io/anthropic/v1/messages"
MINIMAX_API_KEY  = "sk-cp-0_iW72rvuoBmDucQXmRaSAUmcrjXTzZCpIxQt7xgKX_ImdeMkhGmgEV9QBzMNwH87jP-VLIXDNC8VqdgJmntnj5M9gJfTJFiveu9fWuXyQHnW9Z8EQnvlC8"
MODEL = "MiniMax-M2.7"
TWN = timezone(timedelta(hours=8))

PROMPT = """你是一位蒸餾專家。請把以下終端機對話精華濃縮為 300-500 字的總結。

規則：
1. 教練說的每一句原話（非系統指令、非工具呼叫），用「👤 教練：」標記完整保留（一字不改）
2. AI 的回應只保留最終結論和關鍵決策，省略中間過程
3. 按時間順序排列，開頭標記 session 日期（格式：YYYY-MM-DD）
4. 如果教練沒說有意義的話（只有「開工」或純指令），直接寫「本 session 為例行開工，無需蒸餾」
5. 跳過系統指令（<local-command>、<command-name>、<command-args> 等標籤內容）
6. 輸出格式為 Markdown，必須包含 ### 教練關心的重點、### 解決的問題、### 重要教訓 三段

以下是待蒸餾的對話：

"""

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f: return json.load(f)
        except: pass
    return {"done": []}

def save_state(state):
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2)

def call_llm(content):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": MINIMAX_API_KEY,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": PROMPT + content}],
    }
    try:
        resp = requests.post(MINIMAX_BASE_URL, headers=headers, json=payload, timeout=120)
        if resp.status_code != 200:
            print(f"  ❌ API {resp.status_code}: {resp.text[:200]}")
            return None
        data = resp.json()
        blocks = data.get("content", [])
        if isinstance(blocks, list):
            for b in blocks:
                if b.get("type") == "text": return b["text"]
        return None
    except Exception as e:
        print(f"  ❌ 例外: {e}")
        return None

def main():
    state = load_state()
    done_set = set(state["done"])
    now_str = datetime.now(TWN).strftime("%Y-%m-%d %H:%M")

    files = sorted([f for f in os.listdir(DONE_DIR) if f.endswith(".txt")])
    total = len(files)
    print(f"[{now_str}] 共 {total} 個 session，已完成 {len(done_set)} 個")

    # 初始化輸出檔
    if not os.path.exists(OUTPUT):
        with open(OUTPUT, "w") as f:
            f.write(f"# 終端機對話蒸餾 2026-05-30（完整版，共 {total} sessions）\n\n")
            f.write(f"> 由 distill_all_complete.py 使用 MiniMax {MODEL} 全量蒸餾\n\n---\n")

    ok, skip, fail = 0, 0, 0
    for i, fname in enumerate(files, 1):
        sid = fname[:-4]
        if sid in done_set:
            skip += 1
            continue

        fpath = os.path.join(DONE_DIR, fname)
        with open(fpath, encoding="utf-8") as f:
            content = f.read()

        if len(content.strip()) < 100:
            print(f"  [{i}/{total}] ⏭ {sid[:8]} 太短跳過")
            done_set.add(sid)
            continue

        print(f"  [{i}/{total}] 🔄 {sid[:8]}...（{len(content)} chars）", flush=True)
        result = call_llm(content)

        if result is None:
            fail += 1
            print(f"  [{i}/{total}] ❌ 失敗，下次重試")
            continue

        header = f"\n\n---\n\n## 📍 Session {i}（{sid[:8]}）\n\n"
        with open(OUTPUT, "a", encoding="utf-8") as out:
            out.write(header + result + "\n")

        done_set.add(sid)
        ok += 1
        state["done"] = list(done_set)
        if ok % 5 == 0:
            save_state(state)
            print(f"  💾 checkpoint saved（{ok} 完成）")

    save_state(state)
    print(f"\n[完成] ✅ {ok} 蒸餾，⏭ {skip} 跳過，❌ {fail} 失敗")

if __name__ == "__main__":
    main()
