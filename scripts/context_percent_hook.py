#!/usr/bin/env python3
"""Hook：UserPromptSubmit —— 對話容量（context window）跨過 30/35/40/45/50% 各提醒教練一次，
另外每 5 句話定期報一次目前用量（教練 2026-10-15：「每經過幾次對話就主動報告」，並把 45% 加回來）。

跟 context_percent_hook.sh 同一套邏輯，但改成純 Python，Windows／Mac 都能跑
（.sh 版寫死 Mac 路徑、/usr/bin/jq、/tmp，在聯想上不會動）。

原理（事件觸發，不輪詢）：教練每說一句話才算一次——從 hook 輸入給的 transcript_path
（沒有就用 session_id 去 ~/.claude/projects 底下找）讀最後一則 AI 回覆的用量：
input + cache_creation + cache_read ＝ 目前對話容量。
2026-10-15 聯想實測對照桌面版 get_usage：81,178 vs 82,215 token，相符。

環境變數（測試用）：CONTEXT_WINDOW（預設 1000000）、CONTEXT_MARKER_DIR（預設系統暫存夾）。
防洗版：同一場只在「第一次跨過」某條線時提醒；一次跳過好幾條只提醒最高那條。
定期報告：CONTEXT_REPORT_EVERY（預設 5）句話報一次，計數存在 context_count_<session_id>；跨線那一句也算一次報告。
過 30% 之後改成每一句都報（CONTEXT_REPORT_EVERY_OVER30，預設 1；教練 2026-10-17 02:40：查容量不貴就頻繁報）。
"""
import glob
import json
import os
import re
import sys
import tempfile
from pathlib import Path

LEVELS = (30, 35, 40, 45, 50)
WINDOW = int(os.environ.get("CONTEXT_WINDOW") or 1000000)
EVERY = int(os.environ.get("CONTEXT_REPORT_EVERY") or 5)
EVERY_OVER30 = int(os.environ.get("CONTEXT_REPORT_EVERY_OVER30") or 1)
MARKER_DIR = Path(os.environ.get("CONTEXT_MARKER_DIR") or tempfile.gettempdir())
TAIL_BYTES = 4 * 1024 * 1024
# 教練 2026-10-19 定的默契：一問「對話百分比剩多少」（或類似問法）就直接列，不論有沒有過 30%
LASTMARK = "（教練 2026-10-19 定的默契：他都看最後一句）"
ASK = re.compile(r"對話.{0,6}百分比|百分比.{0,4}(多少|剩)|對話.{0,4}剩多少|容量.{0,4}(多少|剩)")


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


# 2026-10-21 教練：「如果你能主動問我，我連『總結』兩個字都不用打，直接按總結就好了」——問總結的固定格式
SUMMARY_ASK = "用收尾框（wrap_up）問，教練 10/21 定的標準：ask 寫「對話容量 xx%、本週額度 xx%，要現在總結嗎？」（數字用 get_usage：context.percentUsed＋Weekly 那格；5 小時額度過 80% 才加），按鈕第一顆 label「總結」、message「總結」——教練按一下就好，不用打字、不用再問容量"

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
    if ASK.search(str(data.get("prompt") or "")):  # 關鍵字：教練問容量，立刻給數字（不動提醒用的計數，不影響定期報告節奏）
        sys.stdout.reconfigure(encoding="utf-8")
        print(f"🧠 教練問對話容量（默契關鍵字「對話百分比剩多少」，教練 2026-10-19 定）：本場對話已用約 {pct}%（約 {total // 10000} 萬 token），"
              f"剩約 {100 - pct}%（視窗 {WINDOW // 10000} 萬；約 97% 時系統會自動壓縮）。\n"
              f"👉 把「已用 {pct}%、剩 {100 - pct}%」列給教練，寫在這一則回覆的最後一句{LASTMARK}，不用再查、不用叫工具。")
        return
    marker = MARKER_DIR / ("context_remind_" + sid)
    try:
        last = int(marker.read_text().strip() or 0)
    except Exception:
        last = 0
    hit = max([lv for lv in LEVELS if pct >= lv and lv > last], default=0)
    counter = MARKER_DIR / ("context_count_" + sid)
    try:
        n = int(counter.read_text().strip() or 0) + 1
    except Exception:
        n = 1
    try:
        counter.write_text(str(0 if hit else n))   # 跨線那一句已經報過，重新數
    except Exception:
        pass
    if not hit:
        every = EVERY_OVER30 if pct >= 30 else EVERY
        if every > 0 and n % every == 0:
            sys.stdout.reconfigure(encoding="utf-8")
            if pct >= 30:
                where = f"寫在這一則回覆的「最後一句」（所有內容講完之後，固定一句：這場對話已用約 {pct}%）{LASTMARK}"
            else:
                where = "放在這一則回覆的第一行（亮燈那行後面）"
            msg = (f"🧠 對話容量定期報告（系統自動，每 {every} 句一次）：本場對話目前用了約 {pct}%（約 {total // 10000} 萬 token）。"
                   f"\n👉 請用一句白話告訴教練：目前用了約 {pct}%，{where}。")
            if pct >= 30:
                msg += ("\n   ⚠️ 已過 30%：只做教練這一句明說的事、不順手加工作；手上這件做完就主動問要不要總結——" + SUMMARY_ASK + "（只在問總結那一句查 get_usage，平常不查）。")
            print(msg)
        return
    try:
        marker.write_text(str(hit))
    except Exception:
        pass

    out = [
        f"🧠 對話容量提醒（系統自動，教練 2026-10-14 要求）：本場對話已用約 {pct}%（約 {total // 10000} 萬 token，視窗 {WINDOW // 10000} 萬），剛跨過 {hit}% 這條線。",
        f"👉 請用一句白話告訴教練：這場對話已用約 {pct}%，寫在這一則回覆的「最後一句」（所有內容講完之後）{LASTMARK}。",
    ]
    if hit >= 50:
        out.append("   已過一半，建議這一段做完就說「總結」，我會更新接力棒並上傳，您再開新對話框。")
    elif hit >= 40:
        out.append("   容量越來越滿，建議找個段落收尾，說「總結」後開新對話框。")
    else:
        out.append("   教練習慣在 30% 出頭開新對話框；告一段落時說「總結」，我會更新接力棒並上傳，您就可以開新的。任務沒做完不必急著換。")
    out.append("   ⚠️ 過 30% 之後（教練 2026-10-17 02:01 糾正：31%→48% 白白多燒 token）：只做教練這一句明說要做的事，不順手加做別的（修規則、整理檔案、查延伸問題）；手上這件做完就收尾，主動問要不要總結——" + SUMMARY_ASK + "，不再開新工作。")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
