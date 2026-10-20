#!/usr/bin/env python3
"""LINE 推播閘門安裝器（教練 2026-10-20 常設禁令）

教練禁令：「所有的 LINE 小龍蝦，沒有經過我的允許，永遠不得使用會扣額度的方式來工作。」
LINE 官方帳號每月只有 200 則；推播（push／multicast／broadcast／narrowcast）按收件人數扣，群組＝人數，
回覆（reply）免費。小龍蝦對 LINE 的所有推播，最後都經過 LINE 外掛 send-*.js 裡的
sendLineProviderMessages() 這一個函式（已查證：外掛內沒有別的推播出口）。本腳本在函式開頭插入閘門：
  - 回覆（operation = "reply"）永遠放行，不受影響
  - 其他（push）→ 沒有「教練許可旗標」就丟錯、不送出、寫一行到 state/line_push_blocked.log
許可旗標：~/.openclaw/workspace/state/LINE_PUSH_APPROVED（touch 一下，10 分鐘內有效；教練口頭同意後才建立）

外掛更新（npm 換世代目錄）會把補丁洗掉，所以本腳本可重複執行（冪等）：
  python3 line_push_gate_patch.py            # 套用（已套過的跳過）
  python3 line_push_gate_patch.py --check    # 只檢查；有任何一份沒套到，結束碼 1
  python3 line_push_gate_patch.py --revert   # 還原成原版（教練明說才用）
"""
import glob
import os
import shutil
import sys

PROJECTS = os.path.expanduser("~/.openclaw/npm/projects")
MARK = "LINE_PUSH_GATE_V1"

HELPER = '''// ==== LINE_PUSH_GATE_V1 (教練 2026-10-20 常設禁令：沒有教練許可，LINE 不得使用會扣額度的推播) ====
import { statSync as __lpgStat, appendFileSync as __lpgAppend } from "node:fs";
import { homedir as __lpgHome } from "node:os";
function __lineQuotaPushGate(operation, request) {
	const base = __lpgHome() + "/.openclaw/workspace/state/";
	try {
		const age = Date.now() - __lpgStat(base + "LINE_PUSH_APPROVED").mtimeMs;
		if (age >= 0 && age < 600000) return;
	} catch {}
	try {
		const first = request?.messages?.[0];
		const preview = String(first?.text ?? first?.type ?? "").replace(/\\s+/g, " ").slice(0, 40);
		const ts = new Date(Date.now() + 8 * 3600 * 1000).toISOString().replace("T", " ").slice(0, 19);
		__lpgAppend(base + "line_push_blocked.log", `${ts}\\tgateway\\t${operation}\\t${request?.to ?? ""}\\t${preview}\\n`);
	} catch {}
	throw new HTTPFetchError("403 - LINE 推播（會扣額度）已被教練常設禁令擋下，需教練同意才可送", { status: 403, statusText: "Forbidden", headers: new Headers(), body: "" });
}
// ==== /LINE_PUSH_GATE_V1 ====
'''

ANCHOR = "async function sendLineProviderMessages(operation, token, request, retryKey) {\n"
CALL = '\tif (operation !== "reply") __lineQuotaPushGate(operation, request); // LINE_PUSH_GATE_V1\n'


def targets():
    return sorted(glob.glob(os.path.join(PROJECTS, "openclaw-line-*", "node_modules", "@openclaw", "line", "dist", "send-*.js")))


def has_function(text):
    return ANCHOR in text or MARK in text


def apply(path):
    text = open(path, encoding="utf-8").read()
    if MARK in text:
        return "已套過"
    if ANCHOR not in text:
        return "找不到 sendLineProviderMessages（外掛版本改了寫法，要人看）"
    bak = path + ".bak-before-line-push-gate-20261020"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    new = text.replace(ANCHOR, HELPER + ANCHOR + CALL, 1)
    tmp = path + ".tmp-gate"
    open(tmp, "w", encoding="utf-8").write(new)
    os.replace(tmp, path)
    return "已套用"


def revert(path):
    bak = path + ".bak-before-line-push-gate-20261020"
    if os.path.exists(bak):
        shutil.copy2(bak, path)
        return "已還原"
    return "沒有備份可還原"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    files = [f for f in targets() if has_function(open(f, encoding="utf-8").read())]
    if not files:
        print("找不到任何 LINE 外掛的 send-*.js（外掛路徑變了？）")
        return 1
    bad = 0
    for f in files:
        short = f.replace(os.path.expanduser("~"), "~")
        if mode == "--check":
            ok = MARK in open(f, encoding="utf-8").read()
            print(("✅ 有閘門 " if ok else "❌ 沒閘門 ") + short)
            bad += 0 if ok else 1
        elif mode == "--revert":
            print(revert(f), short)
        else:
            r = apply(f)
            print(r, short)
            bad += 0 if r in ("已套用", "已套過") else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
