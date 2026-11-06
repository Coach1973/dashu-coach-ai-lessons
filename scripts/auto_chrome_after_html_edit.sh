#!/bin/bash
# ============================================================
# 🔴 HTML 編輯後自動跳 Chrome（PostToolUse hook，2026-08-08）
#
# 起因：「改完HTML跳Chrome給教練看」這條規則30天內被教練親口提醒7次，
#       Stop hook(rule_html_chrome_check.sh)雖然每次都攔得到，但只是
#       事後補救——每次都要教練等到被攔下來才想起，沒有真正解決問題。
#       守則#04「解決問題比解釋問題更重要」：不要再靠記憶，直接自動化。
#
# 原理：Edit/Write 工具只要碰過 .html 檔，馬上（不用等 Stop）自動執行
#       open -a "Google Chrome" file://<改動的檔案路徑>，保證教練眼前
#       一定會跳出真實 Chrome 視窗，不會再有「完全忘記跳」的情況。
#
# 限制：Jinja/樣板類 .html（如 Flask templates）file://本機開不會套用
#       後端渲染，畫面可能不完整——這種情況仍建議額外手動開真正的
#       server網址(如 chapters.bymyway.com)，這支hook只保證「基本一定
#       會跳出東西」，不取代判斷該開哪個網址。
# ============================================================

INPUT=$(cat)
export HOOK_INPUT="$INPUT"

python3 - <<'PYEOF'
import json, os, sys, subprocess

try:
    data = json.loads(os.environ.get("HOOK_INPUT", "{}"))
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}

if tool not in ("Edit", "Write"):
    sys.exit(0)

file_path = ti.get("file_path", "")
if not file_path.lower().endswith(".html"):
    sys.exit(0)

# 2026-11-06 教練：一份報告邊寫邊跳 5～6 次，要一個個關掉。改成寫的過程一律不跳，
# 寫完交付時由 deliver_open.sh（或收尾的 Chrome 查證鎖）只跳一次。
sys.exit(0)

if not os.path.isabs(file_path):
    sys.exit(0)

try:
    subprocess.Popen(
        ["open", "-a", "Google Chrome", f"file://{file_path}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    print(f"🔴 已在 Mac 螢幕開啟 Chrome：{file_path}（只有坐在 Mac 前才看得到；教練用手機或遠端時這不算交付，要給 https 網址並用 curl 驗證）。", file=sys.stderr)
    print("若這是樣板檔(Jinja/後端渲染)，畫面可能不完整，記得額外開真正的server網址驗證。", file=sys.stderr)
except Exception as e:
    print(f"⚠️ 自動跳Chrome失敗：{e}", file=sys.stderr)

sys.exit(0)
PYEOF
