#!/bin/bash
# ============================================================
# 📦🔒 交付自檢門（Stop hook，2026-06-11 軍師建立，教練拍板）
#
# 起因：試金石案例 2/6/12/14/20——AI 說「完成了」但沒自己看過、
#       沒數過、沒驗過，全靠教練人工抓錯。教練原話：
#       「我真的不想當監工，都是很基本的問題，我卻要人工發現。」
#
# 原理：AI 回覆裡宣稱「完成了/做好了/已上線」但整段找不到任何憑證
#       （commit hash / 測試結果 / 驗證輸出）→ 擋下，叫它先驗證再交付。
#       對應守則 #03（結論出來之前自己先看過）+ #05（hash 才算憑證）。
#
# 沿用案例 F 的防誤殺三件套：只讀最後一條訊息、剝引號、白名單。
# ============================================================
set -uo pipefail

INPUT=$(cat)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)
[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0

TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json, re

path = sys.argv[1]
try:
    lines = [l for l in open(path) if l.strip()]
except Exception:
    sys.exit(0)

text = ""
for line in reversed(lines):
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get("type") == "assistant":
        contents = evt.get("message", {}).get("content", [])
        text = "\n".join(c.get("text", "") for c in contents if c.get("type") == "text")
        break

if not text:
    sys.exit(0)

# 交付宣稱句型（只認「已經做完」的口氣，不抓未來式）
CLAIM = re.compile(r"(完成了|做好了|已完成|已上線|已部署|已修復|修好了|大功告成|全部搞定|已交付|上線了|搞定了)")
# 憑證特徵（整段訊息任何一處有就算）
EVIDENCE = re.compile(
    r"(commit|hash|\b[0-9a-f]{8,40}\b|✅|測試|驗證|通過|結果代碼|HTTP[ /]|exit 0|全過|憑證|跑過|實測|對比|du -sh)",
    re.IGNORECASE)
# 行級白名單：討論/否定/條件/未來式，不是真的在交付
WHITELIST = re.compile(r"(還沒|尚未|未完成|不算|將會|預計|待|如果|等教練|要怎麼|怎麼樣才|是否|嗎[?？]|案例|守則|句型|偵測|hook|測試)")

claimed = False
for ln in text.split("\n"):
    if WHITELIST.search(ln):
        continue
    clean = re.sub(r"「[^」]*」", "", ln)
    if CLAIM.search(clean):
        claimed = True
        break

if not claimed:
    sys.exit(0)
if EVIDENCE.search(text):
    sys.exit(0)

msg = """
📦🔒 交付自檢門（守則 #03 + #05 自動對照）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
剛才的回覆宣稱「完成了」，但整段找不到任何憑證。
教練原話：「我真的不想當監工，都是很基本的問題，我卻要人工發現。」

交付前先回答三問，並把證據放進回覆：
  ① 我自己打開/跑過/看過成果了嗎？→ 附上輸出或測試結果
  ② 數量、編號、規格跟教練要求的一致嗎？→ 數過再說
  ③ 有 commit hash 或可驗證的痕跡嗎？→ 沒有 hash 不算完成（守則 #05）

請先實際驗證，把憑證補進回覆再交付。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
print(msg, file=sys.stderr)
sys.exit(2)
PYEOF
