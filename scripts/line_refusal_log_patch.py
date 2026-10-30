#!/usr/bin/env python3
"""LINE 推播被拒的原因記錄補丁（教練 2026-10-30「加記錄」）

問題：LINE 回 400／429 時，日誌只寫「400 - Bad Request」，看不出 LINE 回傳的內容，
無法判斷原因（10/30 12:57 rongshuxia 群組 400 就是這樣查不出來）。

做法：在外掛 send-retry-*.mjs 的 runLinePushWithRetries 每次嘗試失敗時，
把 HTTP 狀態、statusText、LINE 回傳的 body（截 500 字）寫一行 JSON 到
~/.openclaw/workspace/state/line_refusal.log。只記錄，不改變送出或重試行為。

用法（冪等，可重複執行；外掛更新後補丁會被洗掉，重跑即可）：
  python3 line_refusal_log_patch.py           # 套用
  python3 line_refusal_log_patch.py --check   # 只檢查
  python3 line_refusal_log_patch.py --revert  # 還原（教練明說才用）

生效：補丁只改檔案，閘道程序要重啟才會載入新程式碼。
"""
import glob
import os
import shutil
import sys

PROJECTS = os.path.expanduser("~/.openclaw/npm/projects")
MARK = "LINE_REFUSAL_LOG_V1"
BAK_SUFFIX = ".bak-before-line-refusal-log-20261030"
ANCHOR = "const runLinePushWithRetries = (fn, label) => {"
OLD_CATCH = "\t\t} catch (error) {\n\t\t\tsawAmbiguousAttempt ||="
NEW_CATCH = "\t\t} catch (error) {\n\t\t\t__lineRefusalLog(error, label);\n\t\t\tsawAmbiguousAttempt ||="

HELPER = '''// ==== LINE_REFUSAL_LOG_V1 (教練 2026-10-30：LINE 被拒時記下回傳內容，只記錄不改行為) ====
import { appendFileSync as __lrlAppend } from "node:fs";
import { homedir as __lrlHome } from "node:os";
function __lineRefusalLog(error, label) {
	try {
		const http = findLineHttpError(error);
		if (!http) return;
		const line = JSON.stringify({
			at: new Date().toISOString(),
			label,
			status: http.status,
			statusText: http.statusText,
			body: String(http.body ?? "").slice(0, 500)
		}) + "\\n";
		__lrlAppend(__lrlHome() + "/.openclaw/workspace/state/line_refusal.log", line);
	} catch {}
}
// ==== /LINE_REFUSAL_LOG_V1 ====
'''


def targets():
    pattern = os.path.join(PROJECTS, "openclaw-line-*", "node_modules", "@openclaw", "line", "dist", ".setup", "send-retry-*.mjs")
    return [p for p in glob.glob(pattern) if ANCHOR in open(p, encoding="utf-8").read()]


def apply(path):
    text = open(path, encoding="utf-8").read()
    if MARK in text:
        return "已套用，跳過"
    if text.count(ANCHOR) != 1 or text.count(OLD_CATCH) != 1:
        return "錨點對不上（外掛版本變了？），未修改"
    bak = path + BAK_SUFFIX
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    text = text.replace(OLD_CATCH, NEW_CATCH, 1)
    text = text.replace(ANCHOR, HELPER + ANCHOR, 1)
    tmp = path + ".tmp-refusal-log"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)
    return "已套用"


def revert(path):
    bak = path + BAK_SUFFIX
    if os.path.exists(bak):
        shutil.copy2(bak, path)
        return "已還原"
    return "沒有備份，未還原"


def main():
    files = targets()
    if not files:
        print("找不到任何 send-retry-*.mjs（外掛路徑變了？）")
        return 1
    if "--check" in sys.argv:
        bad = [p for p in files if MARK not in open(p, encoding="utf-8").read()]
        for p in files:
            print(("未套用" if p in bad else "已套用"), p)
        return 1 if bad else 0
    for p in files:
        print((revert(p) if "--revert" in sys.argv else apply(p)), p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
