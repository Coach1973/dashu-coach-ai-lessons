#!/bin/bash
# ============================================================
# 📷🔒 截圖鎖（PreToolUse hook，2026-06-11 軍師建立，教練拍板）
#
# 起因：AI 多次未經教練同意就截圖（耗 token + 教練明令禁止，
#       見 memory: feedback_no_screenshot_terminal /
#                  feedback_no_screenshot_without_permission）
#
# 原理：AI 按下任何「截圖類」工具之前，系統先檢查通行證。
#       通行證 = ~/.openclaw/workspace/state/SCREENSHOT_APPROVED
#       沒有通行證 → 截圖直接被擋下，按不下去。
#       通行證有效 10 分鐘（教練同意一次，10 分鐘內可截，過期重新問）。
#
# 發通行證（教練親口說「可以截圖」之後才能執行）：
#   touch ~/.openclaw/workspace/state/SCREENSHOT_APPROVED
# ============================================================

INPUT=$(cat)
export HOOK_INPUT="$INPUT"

python3 - <<'PYEOF'
import json, os, sys, time

try:
    data = json.loads(os.environ.get("HOOK_INPUT", "{}"))
except Exception:
    sys.exit(0)  # 解析不了就放行，不誤殺其他工具

tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}

SHOT_ACTIONS = ("screenshot", "zoom")

def wants_screenshot():
    # 直接的截圖工具
    if tool in ("mcp__computer-use__screenshot",
                "mcp__computer-use__zoom",
                "mcp__Claude_Preview__preview_screenshot"):
        return True
    # Chrome 的 computer 工具：只有 action 是截圖/放大才算
    # 2026-08-08 教練抓到：實際MCP工具名稱是全小寫連字號 claude-in-chrome，
    # 不是 Title_Case 底線的 Claude_in_Chrome，比對從沒對上過，鎖形同虛設
    if tool == "mcp__claude-in-chrome__computer":
        return ti.get("action") in SHOT_ACTIONS
    # Browser pane 的 computer 工具：同樣只有 action 是截圖/放大才算
    # 2026-07-13 教練抓到：這支工具當時完全沒被鎖檢查到，重複截圖沒被擋
    if tool == "mcp__Claude_Browser__computer":
        return ti.get("action") in SHOT_ACTIONS
    # 批次工具：掃裡面有沒有夾帶截圖動作
    if tool in ("mcp__computer-use__computer_batch",
                "mcp__computer-use__teach_step",
                "mcp__computer-use__teach_batch"):
        items = ti.get("actions") or ti.get("steps") or []
        for a in items:
            if not isinstance(a, dict):
                continue
            if a.get("action") in SHOT_ACTIONS:
                return True
            for sub in (a.get("actions") or []):
                if isinstance(sub, dict) and sub.get("action") in SHOT_ACTIONS:
                    return True
        return False
    if tool == "mcp__claude-in-chrome__browser_batch":
        for a in (ti.get("actions") or []):
            if not isinstance(a, dict):
                continue
            inner = a.get("input") or {}
            if isinstance(inner, dict) and inner.get("action") in SHOT_ACTIONS:
                return True
        return False
    return False

if not wants_screenshot():
    sys.exit(0)

token = os.path.expanduser("~/.openclaw/workspace/state/SCREENSHOT_APPROVED")
MAX_AGE = 600  # 10 分鐘

if os.path.exists(token):
    age = time.time() - os.path.getmtime(token)
    if age <= MAX_AGE:
        sys.exit(0)  # 通行證有效，放行
    try:
        os.remove(token)  # 過期銷毀
    except OSError:
        pass

print("", file=sys.stderr)
print("📷🔒 截圖鎖：這次截圖已被擋下。", file=sys.stderr)
print("", file=sys.stderr)
print("教練明令：未經同意不可截圖（截圖耗 token，能用指令/讀檔完成的一律不截圖）。", file=sys.stderr)
print("教練已經親口同意截圖了嗎？", file=sys.stderr)
print("  是 → 執行：touch ~/.openclaw/workspace/state/SCREENSHOT_APPROVED 再重試（10 分鐘有效）", file=sys.stderr)
print("  否 → 改用指令或讀檔案的方式完成任務，或先問教練。", file=sys.stderr)
sys.exit(2)
PYEOF
