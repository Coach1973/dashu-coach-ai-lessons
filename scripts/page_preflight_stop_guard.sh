#!/bin/bash
# Hook：Stop
# 用途：這一輪對話改過「網站倉庫裡的 .html」，卻沒有在最後一次修改「之後」跑過 page_preflight.js，就不准收尾。
# 起因（2026-11-04 教練）：網頁字看不清、表頭不見、圖太大，一再被教練親眼抓到；只寫提醒沒用，改成程式鎖。
# 查的是「事實」（對話紀錄裡真的有沒有跑過自檢），不是 AI 自稱；
# 設計成「出錯就放行」（2026-10-16 教訓：檢查程式自己壞掉不能把教練每句話擋掉）。
# 只確保「有跑」；🔴 要不要修由「改網頁」技能規定。
set -uo pipefail

INPUT=$(cat 2>/dev/null || true)
[ -z "$INPUT" ] && exit 0

# 已經被這個鎖擋過一次、AI 正在補做時，不再擋第二次（防無限迴圈）
ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)
[ "$ACTIVE" = "true" ] && exit 0

TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
[ -z "$TRANSCRIPT_PATH" ] && exit 0
[ ! -f "$TRANSCRIPT_PATH" ] && exit 0

RESULT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF' 2>/dev/null
import sys, json, re

path = sys.argv[1]
try:
    with open(path, encoding='utf-8') as f:
        lines = [l for l in f if l.strip()]
except Exception:
    print("ok")
    sys.exit(0)

# 只看「網站倉庫」裡的 html（~/github_repos/ 底下、非備份檔）
SITE = re.compile(r'/github_repos/[^/]+/.*\.html$', re.I)
last_edit = -1
last_check = -1
edited = []

for i, line in enumerate(lines):
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get('type') != 'assistant':
        continue
    content = (evt.get('message') or {}).get('content')
    if not isinstance(content, list):
        continue
    for c in content:
        if not isinstance(c, dict) or c.get('type') != 'tool_use':
            continue
        name = c.get('name', '')
        tin = c.get('input') or {}
        if name in ('Edit', 'Write'):
            fp = str(tin.get('file_path', ''))
            if SITE.search(fp) and '.bak' not in fp:
                last_edit = i
                if fp not in edited:
                    edited.append(fp)
        elif name == 'Bash':
            if 'page_preflight.js' in str(tin.get('command', '')):
                last_check = i

if last_edit >= 0 and last_check < last_edit:
    print("need|" + ";".join(edited[-3:]))
else:
    print("ok")
PYEOF
)

case "$RESULT" in
  need\|*)
    FILES="${RESULT#need|}"
    cat >&2 <<GUARD_EOF

🔴 網頁交付前自檢鎖
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
這一輪改過網站的 html，但在最後一次修改之後，沒有跑過交付前自檢。
改過的檔案：$FILES

請先跑一次（頁面要已上線，或在本機開 8791 埠，不要用 8765）：
  node ~/.openclaw/workspace/scripts/page_preflight.js <網址>

有 🔴 就先修好再交付；🟡 偏淡只提醒、不擋。
（這個鎖只查「有沒有跑過」，查的是對話紀錄，不是自稱。）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GUARD_EOF
    exit 2
    ;;
esac

exit 0
