#!/usr/bin/env python3
"""Hook：UserPromptSubmit —— 對話容量（context window）跨過 30/35/40/50% 各提醒教練一次。

跟 context_percent_hook.sh 同一套邏輯，但改成純 Python，Windows／Mac 都能跑
（.sh 版寫死 Mac 路徑、/usr/bin/jq、/tmp，在聯想上不會動）。

原理（事件觸發，不輪詢）：教練每說一句話才算一次——從 hook 輸入給的 transcript_path
（沒有就用 session_id 去 ~/.claude/projects 底下找）讀最後一則 AI 回覆的用量：
input + cache_creation + cache_read ＝ 目前對話容量。
2026-10-15 聯想實測對照桌面版 get_usage：81,178 vs 82,215 token，相符。

環境變數（測試用）：CONTEXT_WINDOW（預設 1000000）、CONTEXT_MARKER_DIR（預設系統暫存夾）。
防洗版：同一場只在「第一次跨過」某條線時提醒；一次跳過好幾條只提醒最高那條。
"""
import glob
import json
import os
import sys
import tempfile
from pathlib import Path

LEVELS = (30, 35, 40, 50)
WINDOW = int(os.environ.get("CONTEXT_WINDOW") or 1000000)
MARKER_DIR = Path(os.environ.get("CONTEXT_MARKER_DIR") or tempfile.gettempdir())
TAIL_BYTES = 4 * 1024 * 1024


def find_transcript(data):
    p = data.get("transcript_path")
    if p and os.path.isfile(p):
        return p
    sid = data.get("session_id")
    if not sid:
        return None
    roots = [os.environ.get("CLAUDE_CONFIG_DIR"), str(Path.home() / ".claude")]
    for root in filter(None, roots):
        hits = glob.glob(os.path.join(root, "projects", "*", sid + ".jsonl"))
        if hits:
            return hits[0]
    return None


def usage_of(line):
    try:
        o = json.loads(line)
    except Exception:
        return None
    if o.get("type") != "assistant":
        return None
    m = o.get("message") or {}
    u = m.get("usage")
    if not u or m.get("model") == "<synthetic>":
        return None
    return (u.get("input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0) + (u.get("cache_read_input_tokens") or 0)


def latest_total(path):
    """最後一則 AI 回覆的用量。先只讀檔尾（大檔很快），找不到才整檔掃。"""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        f.seek(max(0, size - TAIL_BYTES))
        tail = f.read().decode("utf-8", errors="ignore").splitlines()
    for line in reversed(tail):
        t = usage_of(line)
        if t:
            return t
    if size > TAIL_BYTES:
        total = 0
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                total = usage_of(line) or total
        return total
    return 0


def main():
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return
    sid = data.get("session_id") or ""
    path = find_transcript(data)
    if not sid or not path:
        return
    total = latest_total(path)
    if total <= 0:
        return
    pct = total * 100 // WINDOW
    marker = MARKER_DIR / ("context_remind_" + sid)
    try:
        last = int(marker.read_text().strip() or 0)
    except Exception:
        last = 0
    hit = max([lv for lv in LEVELS if pct >= lv and lv > last], default=0)
    if not hit:
        return
    try:
        marker.write_text(str(hit))
    except Exception:
        pass

    out = [
        f"🧠 對話容量提醒（系統自動，教練 2026-10-14 要求）：本場對話已用約 {pct}%（約 {total // 10000} 萬 token，視窗 {WINDOW // 10000} 萬），剛跨過 {hit}% 這條線。",
        f"👉 請在這一則回覆的「最前面」用一句白話告訴教練：目前用了約 {pct}%。",
    ]
    if hit >= 50:
        out.append("   已過一半，建議這一段做完就說「總結」，我會更新接力棒並上傳，您再開新對話框。")
    elif hit >= 40:
        out.append("   容量越來越滿，建議找個段落收尾，說「總結」後開新對話框。")
    else:
        out.append("   教練習慣在 30% 出頭開新對話框；告一段落時說「總結」，我會更新接力棒並上傳，您就可以開新的。任務沒做完不必急著換。")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
