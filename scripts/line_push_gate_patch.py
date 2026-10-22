#!/usr/bin/env python3
"""LINE 推播閘門安裝器（教練 2026-10-20 常設禁令）

教練禁令：「所有的 LINE 小龍蝦，沒有經過我的允許，永遠不得使用會扣額度的方式來工作。」
LINE 官方帳號每月只有 200 則；推播（push／multicast／broadcast／narrowcast）按收件人數扣，群組＝人數，
回覆（reply）免費。小龍蝦對 LINE 的所有推播，最後都經過 LINE 外掛 send-*.js 裡的
sendLineProviderMessages() 這一個函式（已查證：外掛內沒有別的推播出口）。本腳本在函式開頭插入閘門：
  - 回覆（operation = "reply"）永遠放行，不受影響
  - 其他（push）→ 沒有「教練許可旗標」就丟錯、不送出、寫一行到 state/line_push_blocked.log
許可旗標：~/.openclaw/workspace/state/LINE_PUSH_APPROVED
  檔案「內容」＝許可當下的 Unix 秒數時間戳，10 分鐘內有效；只看內容，不看檔案修改時間
  （V2，2026-10-22：自動暫存還原、touch 都會刷新修改時間，殘檔不能因此復活）。
  空檔、舊時間戳、未來時間戳、非數字一律當沒許可。
  教練口頭同意後才建立：scripts/line_push_approve.sh；用完 scripts/line_push_approve.sh --revoke 刪檔作廢。

外掛更新（npm 換世代目錄）會把補丁洗掉，所以本腳本可重複執行（冪等）；舊版 V1 的檔案會自動升級成 V2：
  python3 line_push_gate_patch.py            # 套用（已套過的跳過；V1 升級成 V2）
  python3 line_push_gate_patch.py --check    # 只檢查；有任何一份沒套到 V2，結束碼 1
  python3 line_push_gate_patch.py --revert   # 還原成原版（教練明說才用）
"""
import glob
import os
import re
import shutil
import sys

PROJECTS = os.path.expanduser("~/.openclaw/npm/projects")
MARK = "LINE_PUSH_GATE_V2"
OLD_MARK = "LINE_PUSH_GATE_V1"

HELPER = '''// ==== LINE_PUSH_GATE_V2 (教練 2026-10-20 常設禁令：沒有教練許可，LINE 不得使用會扣額度的推播；只看旗標檔內容的時間戳，不看修改時間) ====
import { readFileSync as __lpgRead, appendFileSync as __lpgAppend } from "node:fs";
import { homedir as __lpgHome } from "node:os";
function __lineQuotaPushGate(operation, request) {
	const base = __lpgHome() + "/.openclaw/workspace/state/";
	try {
		const raw = String(__lpgRead(base + "LINE_PUSH_APPROVED", "utf8")).trim();
		if (/^\\d{9,12}$/.test(raw)) {
			const age = Date.now() / 1000 - Number(raw);
			if (age >= 0 && age < 600) return;
		}
	} catch {}
	try {
		const first = request?.messages?.[0];
		const preview = String(first?.text ?? first?.type ?? "").replace(/\\s+/g, " ").slice(0, 40);
		const ts = new Date(Date.now() + 8 * 3600 * 1000).toISOString().replace("T", " ").slice(0, 19);
		__lpgAppend(base + "line_push_blocked.log", `${ts}\\tgateway\\t${operation}\\t${request?.to ?? ""}\\t${preview}\\n`);
	} catch {}
	throw new HTTPFetchError("403 - LINE 推播（會扣額度）已被教練常設禁令擋下，需教練同意才可送", { status: 403, statusText: "Forbidden", headers: new Headers(), body: "" });
}
// ==== /LINE_PUSH_GATE_V2 ====
'''

ANCHOR = "async function sendLineProviderMessages(operation, token, request, retryKey) {\n"
CALL = '\tif (operation !== "reply") __lineQuotaPushGate(operation, request); // LINE_PUSH_GATE_V2\n'

# V1（看檔案修改時間）的舊區塊與呼叫行：升級時先拿掉，再套 V2
OLD_BLOCK_RE = re.compile(r"// ==== LINE_PUSH_GATE_V1 .*?// ==== /LINE_PUSH_GATE_V1 ====\n", re.S)
OLD_CALL = '\tif (operation !== "reply") __lineQuotaPushGate(operation, request); // LINE_PUSH_GATE_V1\n'


def targets():
    return sorted(glob.glob(os.path.join(PROJECTS, "openclaw-line-*", "node_modules", "@openclaw", "line", "dist", "send-*.js")))


def has_function(text):
    return ANCHOR in text or MARK in text or OLD_MARK in text


def apply(path):
    text = open(path, encoding="utf-8").read()
    if MARK in text:
        return "已套過"
    upgraded = False
    if OLD_MARK in text:
        text = OLD_BLOCK_RE.sub("", text, count=1).replace(OLD_CALL, "", 1)
        if OLD_MARK in text:
            return "舊版 V1 區塊拆不乾淨（外掛或補丁被人改過，要人看）"
        upgraded = True
    if ANCHOR not in text:
        return "找不到 sendLineProviderMessages（外掛版本改了寫法，要人看）"
    bak = path + ".bak-before-line-push-gate-20261020"
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    new = text.replace(ANCHOR, HELPER + ANCHOR + CALL, 1)
    tmp = path + ".tmp-gate"
    open(tmp, "w", encoding="utf-8").write(new)
    os.replace(tmp, path)
    return "已升級 V1→V2" if upgraded else "已套用"


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
            text = open(f, encoding="utf-8").read()
            ok = MARK in text
            label = "✅ 有閘門 V2 " if ok else ("❌ 舊版 V1（要升級） " if OLD_MARK in text else "❌ 沒閘門 ")
            print(label + short)
            bad += 0 if ok else 1
        elif mode == "--revert":
            print(revert(f), short)
        else:
            r = apply(f)
            print(r, short)
            bad += 0 if r in ("已套用", "已套過", "已升級 V1→V2") else 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
