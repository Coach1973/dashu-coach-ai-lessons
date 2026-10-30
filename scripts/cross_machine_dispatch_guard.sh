#!/bin/bash
# ============================================================
# 📬🔒 跨機指令鎖（PreToolUse hook，2026-07-02 教練親定）
#
# 起因：軍師建好「心跳燈塔+三機互查」後，未經教練拍板就
#       直接發信給 ACER、聯想要求他們照辦，教練事後才發現，
#       質問「我有說 OK 嗎？你不就是私自做決定了嗎？」
#       （見 memory: feedback_retract_crossmachine_instruction_on_reversal）
#
# 原理：任何要在 cross-agent/inbox/{acer,lenovo,hermes}/ 底下
#       新建檔案（= 發信給其他軍師）的動作，先檢查通行證。
#       通行證 = state/CROSS_MACHINE_APPROVED
#       沒有通行證 → 寫入被擋下，逼軍師先跟教練口頭核對。
#       通行證有效 30 分鐘（教練口頭同意一次，30 分鐘內可發，過期重新問）。
#
# 發通行證（教練親口說「可以發」「OK」「去發」之後才能執行）：
#   touch ~/.openclaw/workspace/state/CROSS_MACHINE_APPROVED
# ============================================================

INPUT=$(cat)
export HOOK_INPUT="$INPUT"

python3 - <<'PYEOF'
import json, os, sys, time

try:
    data = json.loads(os.environ.get("HOOK_INPUT", "{}"))
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}

if tool not in ("Write", "Edit"):
    sys.exit(0)

path = ti.get("file_path", "") or ""

import re
m = re.search(r"cross-agent/inbox/(acer|lenovo|hermes)/", path)
if not m:
    sys.exit(0)

# 2026-09-25教練親自糾正：這道鎖原本不分「軍師主動發號施令」跟「回覆對方主動
# 來信求助、信裡自己寫『回覆要求：需要回覆』」——後者本來就該做，教練原話：
# 「你本來就應該回信給赫米斯，幹嘛還要問過我？」。07-02原始案例是軍師自己
# 決定要建機制、要求ACER/聯想照辦（沒人先問），跟「對方來信、我方回覆」是
# 完全不同方向的動作，鎖只該擋前者。
target_agent = m.group(1)
inbox_mac = os.path.expanduser("~/.openclaw/workspace/cross-agent/inbox/mac")
is_reply_to_pending_request = False
if os.path.isdir(inbox_mac):
    for fname in os.listdir(inbox_mac):
        if re.match(rf"^\d{{8}}-\d{{4}}_{re.escape(target_agent)}-to-mac_.*\.md$", fname):
            is_reply_to_pending_request = True
            break
if is_reply_to_pending_request:
    sys.exit(0)

token = os.path.expanduser("~/.openclaw/workspace/state/CROSS_MACHINE_APPROVED")
MAX_AGE = 1800  # 30 分鐘

if os.path.exists(token):
    age = time.time() - os.path.getmtime(token)
    if age <= MAX_AGE:
        sys.exit(0)
    try:
        os.remove(token)
    except OSError:
        pass

print("", file=sys.stderr)
print("📬🔒 跨機指令鎖：這次發信已被擋下。", file=sys.stderr)
print("", file=sys.stderr)
print("教練明令（2026-07-02）：任何要指揮/通知 ACER、聯想、Hermes 做事的信，", file=sys.stderr)
print("必須是教練叫你寫的，或你自己想發時先得到教練拍板。", file=sys.stderr)
print("", file=sys.stderr)
print("🔴 教練這一輪的話裡已經叫你寫信（例如「寫信給聯想」「寫信給宏碁」「叫赫米斯…」）", file=sys.stderr)
print("   ＝ 就是同意。不要回頭問教練、不要複述信的內容等拍板（2026-10-31 教練第二次糾正：", file=sys.stderr)
print("   「我們以前都是一句話：寫信給聯想，然後叫誰去讀信」）。直接：", file=sys.stderr)
print("   touch ~/.openclaw/workspace/state/CROSS_MACHINE_APPROVED 再重試（30分鐘有效）", file=sys.stderr)
print("   信寫進主工作區 workspace/cross-agent/inbox/<收信人>/、commit＋push 主線，對方 git pull 才讀得到。", file=sys.stderr)
print("", file=sys.stderr)
print("只有「教練沒叫你寫、是你自己想發號施令」的信，才先停下跟教練說明內容，等拍板。", file=sys.stderr)
sys.exit(2)
PYEOF
