#!/bin/bash
# ============================================================
# 🗑️🔒 刪檔鎖（PreToolUse Bash hook，2026-06-11 軍師建立，教練拍板）
#
# 起因：試金石案例 23——rsync & rm & wait 死亡組合，21GB 資料蒸發。
#       教練鐵律：珍貴資料只搬不刪；搬完刪源頭前必須 du -sh 比對。
#
# 原理：AI 要執行「危險刪除」指令前，先查通行證。
#       危險刪除 = rm -r 系列／find -delete／git clean -f／rsync --delete
#       （/tmp 暫存區的刪除不擋，正常工作不受影響）
#       通行證 = ~/.openclaw/workspace/state/DELETE_APPROVED（10 分鐘有效）
#
# 發通行證（教練親口同意刪除之後才能執行）：
#   touch ~/.openclaw/workspace/state/DELETE_APPROVED
# ============================================================

INPUT=$(cat)
export HOOK_INPUT="$INPUT"

python3 - <<'PYEOF'
import json, os, re, sys, time

try:
    data = json.loads(os.environ.get("HOOK_INPUT", "{}"))
except Exception:
    sys.exit(0)

if data.get("tool_name") != "Bash":
    sys.exit(0)
cmd = (data.get("tool_input") or {}).get("command", "") or ""

# 危險刪除特徵
DANGER = [
    r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*\b|--recursive)",  # rm -r / -rf / -fr / --recursive
    r"\bfind\b.*-delete\b",
    r"\bfind\b.*-exec\s+rm\b",
    r"\bgit\s+clean\b.*-[a-zA-Z]*f",
    r"\brsync\b.*--delete",
    r"\bshred\b",
    # —— PowerShell / Windows 刪除（2026-06-25 案例 29：LINE 4GB 丟失，舊鎖完全沒收 Remove-Item）——
    r"(?i)\bRemove-Item\b[^|;\n]*-(Recurse|Force)\b",  # Remove-Item -Recurse/-Force
    r"(?i)\bri\b[^|;\n]*-(Recurse|Force)\b",           # ri 別名 + -Recurse/-Force
    r"(?i)\b(rmdir|rd)\b[^\n]*/s\b",                    # cmd rmdir /s / rd /s
    r"(?i)\bdel\b[^\n]*/[sq]\b",                        # cmd del /s | /q
]
# 安全白名單：只動暫存區/快取的刪除不擋
SAFE_TARGETS = re.compile(
    r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*\s+(\"|')?(/tmp/|/private/tmp/|\$TMPDIR|~/Library/Caches/|/Users/[^ ]+/Library/Caches/|node_modules\b)"
)

# 案例 F 教訓：先剝掉「字面文字」再判斷（grep "rm -rf"、heredoc 文件內容都不是真的在刪）
cmd_stripped = re.sub(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?[\s\S]*?\n\1(?=\s|$)",
                      " HEREDOC ", cmd)  # 剝 heredoc 內文（2026-06-11 實戰誤殺後補）
cmd_stripped = re.sub(r'"[^"]*"', '""', cmd_stripped)
cmd_stripped = re.sub(r"'[^']*'", "''", cmd_stripped)

hit = any(re.search(p, cmd_stripped) for p in DANGER)
if not hit:
    sys.exit(0)
if SAFE_TARGETS.search(cmd):
    sys.exit(0)

token = os.path.expanduser("~/.openclaw/workspace/state/DELETE_APPROVED")
MAX_AGE = 600
if os.path.exists(token):
    if time.time() - os.path.getmtime(token) <= MAX_AGE:
        sys.exit(0)
    try:
        os.remove(token)
    except OSError:
        pass

print("", file=sys.stderr)
print("🗑️🔒 刪檔鎖：這個刪除指令已被擋下。", file=sys.stderr)
print("", file=sys.stderr)
print("教練鐵律（案例 23，21GB 血淚）：珍貴資料只搬不刪；搬移後必須 du -sh 比對一致才能刪源頭。", file=sys.stderr)
print("教練已經親口同意這次刪除了嗎？", file=sys.stderr)
print("  是 → 先 du -sh 比對貼出結果，再執行：touch ~/.openclaw/workspace/state/DELETE_APPROVED 後重試（10 分鐘有效）", file=sys.stderr)
print("  否 → 改用「搬到存檔區」代替刪除，或先問教練。", file=sys.stderr)
sys.exit(2)
PYEOF
