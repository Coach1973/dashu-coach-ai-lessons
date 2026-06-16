#!/usr/bin/env python3
"""
sync_jsonl_to_pending_distill.py

把 Claude 桌面版/終端機的 jsonl 對話紀錄轉成可讀 .txt，
倒進 ~/.openclaw/workspace/terminal-notes/pending_distill/，
讓 OpenClaw cron 的「終端機對話蒸餾（每4小時）」任務有東西可抓。

排程：launchd plist 每 4 小時的 :55 分觸發（OpenClaw cron 整點 :00 觸發前 5 分鐘投遞完成）。
狀態：~/.openclaw/workspace/scripts/.sync_jsonl_state.json（記每個 session 處理到哪個 timestamp）

設計者：軍師 Opus 4.7（2026-06-16 12:20）
背景：教練 2026-06-16 中午發現「終端機蒸餾」連續兩次回報「無對話」，
      根因——cron 看的是 pending_distill/（手動投遞夾），對話真實在
      ~/.claude/projects/-Users-bymyway--openclaw/*.jsonl，兩邊沒接起來。
      此腳本即為橋接層。
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

HOME = Path(os.path.expanduser("~"))
JSONL_DIR = HOME / ".claude/projects/-Users-bymyway--openclaw"
OUT_DIR = HOME / ".openclaw/workspace/terminal-notes/pending_distill"
STATE_FILE = HOME / ".openclaw/workspace/scripts/.sync_jsonl_state.json"
LOG_FILE = HOME / ".openclaw/workspace/scripts/.sync_jsonl.log"
TW_TZ = timezone(timedelta(hours=8))

# 第一次跑時的回溯門檻：6 小時前（足以涵蓋一次 4 小時 cron 週期）
DEFAULT_LOOKBACK_HOURS = 6


def log(msg: str) -> None:
    ts = datetime.now(TW_TZ).strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def extract_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for blk in content:
            if not isinstance(blk, dict):
                continue
            t = blk.get("type")
            if t == "text":
                parts.append(blk.get("text", ""))
            elif t == "tool_use":
                parts.append(f"[工具呼叫:{blk.get('name', '?')}]")
            elif t == "tool_result":
                # 工具結果通常太雜，只標一行
                parts.append("[工具結果]")
        return "\n".join(p for p in parts if p).strip()
    return ""


def process_jsonl(path: Path, last_ts: str):
    """
    讀 jsonl，回傳 (對話段落 list, 新的最後 timestamp)
    只取 message.role in {user, assistant} 且 text 非空者。
    """
    convos = []
    new_last_ts = last_ts
    try:
        with open(path) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                ts = obj.get("timestamp", "")
                if not ts or ts <= last_ts:
                    if ts > new_last_ts:
                        new_last_ts = ts
                    continue
                msg = obj.get("message")
                if not isinstance(msg, dict):
                    new_last_ts = max(new_last_ts, ts)
                    continue
                role = msg.get("role")
                if role not in ("user", "assistant"):
                    new_last_ts = max(new_last_ts, ts)
                    continue
                text = extract_text(msg.get("content"))
                if not text:
                    new_last_ts = max(new_last_ts, ts)
                    continue
                tag = "教練" if role == "user" else "軍師"
                # ts 是 UTC，註明 +8 換算給人看
                try:
                    dt_utc = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    dt_tw = dt_utc.astimezone(TW_TZ)
                    ts_tw = dt_tw.strftime("%Y-%m-%d %H:%M:%S 台灣")
                except Exception:
                    ts_tw = ts
                convos.append(f"[{ts_tw}] {tag}：\n{text}")
                new_last_ts = max(new_last_ts, ts)
    except OSError as e:
        log(f"⚠️ 讀檔失敗 {path.name}: {e}")
    return convos, new_last_ts


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    state = {}
    if STATE_FILE.exists():
        try:
            state = json.load(open(STATE_FILE))
        except Exception:
            state = {}

    default_cutoff = (
        datetime.now(timezone.utc) - timedelta(hours=DEFAULT_LOOKBACK_HOURS)
    ).isoformat().replace("+00:00", "Z")

    if not JSONL_DIR.exists():
        log(f"⚠️ jsonl 來源目錄不存在：{JSONL_DIR}")
        return 1

    total_sessions = 0
    total_segments = 0
    skipped = 0

    for jsonl in sorted(JSONL_DIR.glob("*.jsonl")):
        sid = jsonl.stem
        last_ts = state.get(sid, default_cutoff)
        convos, new_last_ts = process_jsonl(jsonl, last_ts)
        if not convos:
            # 仍然更新 state（讓未來不重掃整個檔）
            if new_last_ts != last_ts:
                state[sid] = new_last_ts
            skipped += 1
            continue

        stamp_tw = datetime.now(TW_TZ).strftime("%Y%m%d_%H%M%S")
        out_file = OUT_DIR / f"session_{sid[:8]}_{stamp_tw}.txt"
        header = (
            f"# 來源 session：{sid}\n"
            f"# jsonl 路徑：{jsonl}\n"
            f"# 投遞時間：{datetime.now(TW_TZ).strftime('%Y-%m-%d %H:%M:%S 台灣')}\n"
            f"# 對話段數：{len(convos)}\n"
            f"# 區間：{last_ts}  →  {new_last_ts}\n"
            f"\n---\n\n"
        )
        out_file.write_text(header + "\n\n---\n\n".join(convos))
        state[sid] = new_last_ts
        total_sessions += 1
        total_segments += len(convos)
        log(f"✅ {jsonl.name} → {out_file.name}（{len(convos)} 段）")

    json.dump(state, open(STATE_FILE, "w"), indent=2, ensure_ascii=False)
    log(f"📊 完成：投遞 {total_sessions} 個 session、{total_segments} 段對話；無新增 {skipped} 個")
    return 0


if __name__ == "__main__":
    sys.exit(main())
