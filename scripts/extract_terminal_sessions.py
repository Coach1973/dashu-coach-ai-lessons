#!/usr/bin/env python3
"""
extract_terminal_sessions.py — 終端機對話提取器
用途：從 Claude Code .jsonl 提取教練原話，寫入 pending_distill/，不呼叫 LLM
執行：Mac crontab 每 30 分鐘，不消耗 Claude Code Token
軍師建立 2026-05-28
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

# 路徑設定
SRC = os.path.expanduser("~/.claude/projects/-Users-bymyway--openclaw")
WORKSPACE = os.path.expanduser("~/.openclaw/workspace/terminal-notes")
PENDING_DIR = os.path.join(WORKSPACE, "pending_distill")
STATE_FILE = os.path.join(WORKSPACE, ".extract_state.json")

# 台灣時區
TWN = timezone(timedelta(hours=8))

def twn_now():
    return datetime.now(TWN)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except:
            pass
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def extract_text_from_content(content):
    """從 message.content 提取純文字，跳過 tool_result 等系統區塊"""
    if isinstance(content, str):
        text = content.strip()
        return text if len(text) > 0 else None
    elif isinstance(content, list):
        texts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type", "")
            if btype == "text":
                t = block.get("text", "").strip()
                if t:
                    texts.append(t)
            elif btype == "tool_result":
                # 跳過工具回傳，不是教練說的話
                pass
            elif btype == "tool_use":
                # 跳過工具呼叫
                pass
        return "\n".join(texts) if texts else None
    return None

def is_hook_injection(text):
    """排除 hook 自動注入的系統訊息（不是教練真實說的話）"""
    if not text:
        return True
    prefixes = [
        "🔴 軍師接力棒",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n🎯 執行合約",
        "🌱 守則提醒",
        "UserPromptSubmit hook",
        "You are a third-person note-taker",
    ]
    for p in prefixes:
        if text.startswith(p):
            return True
    return False

def extract_session(jsonl_path):
    """
    解析一個 .jsonl 檔案，提取教練原話和 AI 重點回應
    回傳 list of dict: [{timestamp, role, text}]
    """
    entries = []
    try:
        with open(jsonl_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_type = d.get("type", "")
                if msg_type not in ("user", "assistant"):
                    continue

                msg = d.get("message", {})
                role = msg.get("role", "")
                content = msg.get("content", "")
                ts_str = d.get("timestamp", "")

                if role not in ("user", "assistant"):
                    continue

                text = extract_text_from_content(content)
                if not text:
                    continue

                if role == "user" and is_hook_injection(text):
                    continue

                # 只保留 assistant 回應的前 300 字（節省蒸餾 token）
                if role == "assistant" and len(text) > 300:
                    text = text[:300] + "…（略）"

                entries.append({
                    "timestamp": ts_str,
                    "role": role,
                    "text": text,
                })
    except Exception as e:
        print(f"[ERROR] 讀取 {jsonl_path}: {e}", file=sys.stderr)
    return entries

def format_output(session_id, entries):
    """格式化成給 LLM 蒸餾用的文字"""
    lines = [
        f"# 終端機對話萃取 — Session {session_id}",
        f"# 提取時間：{twn_now().strftime('%Y-%m-%d %H:%M')} (台灣時間)",
        f"# 共 {len([e for e in entries if e['role']=='user'])} 條教練原話",
        "",
        "---",
        "",
    ]
    for e in entries:
        ts = e["timestamp"][:16].replace("T", " ") if e["timestamp"] else ""
        if e["role"] == "user":
            lines.append(f"【教練 {ts}】")
            lines.append(e["text"])
            lines.append("")
        else:
            lines.append(f"　▶ AI 回應：{e['text']}")
            lines.append("")
    return "\n".join(lines)

def main():
    os.makedirs(PENDING_DIR, exist_ok=True)
    state = load_state()
    now_str = twn_now().strftime("%Y-%m-%d %H:%M")

    print(f"[extract_terminal {now_str}] 掃描 {SRC}")

    # 找近 7 天有更新的 jsonl
    updated = 0
    skipped = 0

    if not os.path.isdir(SRC):
        print(f"[ERROR] 來源目錄不存在: {SRC}")
        sys.exit(1)

    for fname in os.listdir(SRC):
        if not fname.endswith(".jsonl"):
            continue

        fpath = os.path.join(SRC, fname)
        session_id = fname[:-6]  # 去掉 .jsonl

        try:
            file_size = os.path.getsize(fpath)
        except OSError:
            continue

        # 增量：只處理有新增內容的 session
        last_size = state.get(session_id, 0)
        if file_size <= last_size:
            skipped += 1
            continue

        # 提取對話
        entries = extract_session(fpath)
        user_entries = [e for e in entries if e["role"] == "user"]

        if not user_entries:
            # 更新 state 但不寫 pending（沒有教練發言）
            state[session_id] = file_size
            continue

        # 寫入 pending_distill/
        output_path = os.path.join(PENDING_DIR, f"{session_id}.txt")
        content = format_output(session_id, entries)

        with open(output_path, "w", encoding="utf-8") as out:
            out.write(content)

        state[session_id] = file_size
        updated += 1
        print(f"  ✅ {session_id[:8]}：{len(user_entries)} 條教練原話 → pending_distill/")

    save_state(state)
    print(f"[完成] 新增/更新 {updated} 個，跳過 {skipped} 個（未變動）")

if __name__ == "__main__":
    main()
