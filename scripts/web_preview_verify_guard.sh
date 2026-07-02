#!/bin/bash
# Hook：PreToolUse（matcher: Bash）
# 用途：git push 到「push即上線」網站 repo 前，強制查證——
#       不是查「有沒有通行證」（那是 AI 自己 touch 的，等於自稱），
#       是查「這一輪對話的操作紀錄裡，真的有沒有打開過 Chrome / 本機預覽」。
# 起因（2026-07-02 教練親口）：一個月內 6 次「怎麼沒有照SOP出現html讓我看」，
#       查出根因——現有推送鎖 pre-push 只驗證 PUSH_APPROVED 檔案存在，
#       那張通行證是 AI 自己 touch 出來的自稱，不是真的驗證過教練看過。
#       案例29「opt-in鎖=廢紙」同一種病——鎖住了「觸發點」，沒鎖住「事實」。
set -uo pipefail

INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.tool_input.command // ""' 2>/dev/null)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)

# 只攔 git push
echo "$CMD" | grep -qE '(^|&&|\||;)\s*git\s+push' || exit 0

# 「push即上線」網站清單（GitHub Pages / GitHub 自動部署型）
WEBSITE_REPOS='cool-case|theunrestrictedwar|jiesheng-leadership|bymyway-website|government-grow|ai-go|consultant|government-subsidies'

echo "$CMD" | grep -qE "$WEBSITE_REPOS" || {
  # command 本身沒提到站名，改用目前工作目錄判斷
  CWD=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.cwd // ""' 2>/dev/null)
  echo "$CWD" | grep -qE "$WEBSITE_REPOS" || exit 0
}

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# 在 transcript 裡查最近 80 筆 tool_use，找「真的開過 Chrome / 用過本機預覽工具」的證據
HAS_PREVIEW_EVIDENCE=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json

path = sys.argv[1]
try:
    with open(path, encoding='utf-8') as f:
        lines = [l for l in f if l.strip()]
except Exception:
    print("unknown")
    sys.exit(0)

recent = lines[-80:]
evidence = False

for line in recent:
    try:
        evt = json.loads(line)
    except Exception:
        continue
    if evt.get('type') != 'assistant':
        continue
    for c in evt.get('message', {}).get('content', []):
        if not isinstance(c, dict) or c.get('type') != 'tool_use':
            continue
        name = c.get('name', '')
        tin = c.get('input', {})
        if name == 'Bash':
            command = str(tin.get('command', ''))
            if 'open -a' in command and ('Chrome' in command or 'chrome' in command):
                evidence = True
            if 'http.server' in command or 'preview' in command.lower():
                evidence = True
        if name.startswith('mcp__Claude_Preview__preview_') or 'preview_screenshot' in name or 'preview_snapshot' in name:
            evidence = True

print("yes" if evidence else "no")
PYEOF
)

[[ "$HAS_PREVIEW_EVIDENCE" == "yes" || "$HAS_PREVIEW_EVIDENCE" == "unknown" ]] && exit 0

cat >&2 <<'GUARD_EOF'

🔴🔴🔴 網頁預覽查證鎖（deterministic check，非自稱）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
偵測到要 git push 到「push即上線」網站，但這一輪對話裡
找不到任何「真的打開過 Chrome / 本機預覽伺服器」的操作紀錄。

2026-07-02 教練親口：一個月內 6 次「照SOP該給我看HTML卻沒給」。
根因：舊的推送鎖只驗證 PUSH_APPROVED 檔案存在——但那張通行證是
AI 自己 touch 出來的自稱，不是真的驗證教練看過。這次要查真證據。

✅ 停下來自問：
  1. 我這一輪真的用 open -a "Google Chrome" 或本機 http.server 打開過改動後的頁面嗎？
  2. 教練真的親口看過、說「推」了嗎？
  3. 如果都是 → 先執行一次真的預覽動作（open -a "Google Chrome" <path>），
     讓證據留在這輪對話紀錄裡，再重新嘗試 push。
  4. 如果教練還沒看過 → 停下，先給教練看，不要用「應該沒問題」取代查驗。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GUARD_EOF

exit 2
