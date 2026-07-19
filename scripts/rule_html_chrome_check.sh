#!/bin/bash
# Hook：Stop（Claude Code 在回應結束前觸發）
# 用途：這一輪若用 Edit/Write 改過 .html 檔，強制查證「.html改動之後」
#       是否真的執行過 `open -a "Google Chrome"` 開給教練看——
#       命中缺失就 exit 2 攔截，不讓「已看過/已驗證」這種回報送到教練眼前。
# 起因（2026-07-11 案例46，鐵律2026-06-17定稿後至少第四次犯）：
#       軍師只用 Claude Code 內建無頭瀏覽器工具（preview_screenshot/
#       preview_snapshot）自己截圖確認畫面正確，就跟教練回報「已看過」，
#       沒有額外執行 open -a "Google Chrome"。教練重話：「講多少次你沒跳HTML給我看。」
#       跟簡體字案例44、context預警案例45同一條根：靠自覺記得檢查不可靠，
#       必須做確定性 grep/parse 檢查，不看模型會不會自己想起來。
# 設計原則：只認「open -a "Google Chrome"」這種明確指令為證據，
#       無頭瀏覽器工具（preview_screenshot/preview_snapshot等）一律不算——
#       那是 AI 自我除錯用，不是教練親眼看過的替代品，兩者不可混淆。
# 保護機制：偵測 stop_hook_active=true 時放行，避免無限迴圈
# 軍師建立 2026-07-11（案例46後，教練口頭指示「做」）
set -uo pipefail

INPUT=$(cat)
TRANSCRIPT_PATH=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.transcript_path // ""' 2>/dev/null)
STOP_HOOK_ACTIVE=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.stop_hook_active // false' 2>/dev/null)

[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0
[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

RESULT=$(python3 - "$TRANSCRIPT_PATH" <<'PYEOF'
import sys, json, re

path = sys.argv[1]
try:
    with open(path, encoding='utf-8') as f:
        lines = [l for l in f if l.strip()]
except Exception:
    print(json.dumps({'html_files': [], 'has_chrome_evidence': False}))
    sys.exit(0)

# 只看最近 100 筆事件（這一輪對話的範圍已經足夠，避免抓到很久以前的舊改動）
recent = lines[-100:]

html_edit_idx = -1
html_files = []
chrome_evidence_idx = -1

for i, line in enumerate(recent):
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

        if name in ('Edit', 'Write'):
            fp = str(tin.get('file_path', ''))
            if fp.lower().endswith('.html'):
                html_edit_idx = i
                if fp not in html_files:
                    html_files.append(fp)

        if name == 'Bash':
            command = str(tin.get('command', ''))
            # 只認明確的 open -a "Google Chrome"（或不帶引號版本），
            # 不接受無頭預覽工具當證據
            if re.search(r"open\s+-a\s+\"?Google Chrome\"?", command, re.IGNORECASE):
                chrome_evidence_idx = i

            # 2026-07-20 案例52後補：Edit/Write 只抓得到「直接編輯 .html」，
            # 但用 Bash 把 .html 複製/部署到別的 repo 再 push 上線（cp/mv/rsync/
            # git add 動作）完全繞過上面的偵測，導致教練看到的是「已上線」文字
            # 回報而不是真的被跳 Chrome 出來驗證。
            # 2026-07-20 同日修正：原正則太寬——只要整段指令字串「同時含 .html
            # 字樣」與「cp/mv/git 等關鍵字」就誤判，導致連 commit message 裡
            # 用文字描述「用cp把index.html複製」這種純說明文字都被誤抓成真的
            # 執行過複製。改成要求動詞後面緊接著一個真正的檔案路徑（前面必須
            # 是空白或路徑符號，不能是中文字或其他字元直接黏著），只認得
            # cp/mv/rsync/git add 這種「後面帶檔名參數」的指令，拿掉純字面
            # 存在的 git commit / git push 關鍵字比對（這兩個動作本身不帶檔名）。
            m = re.search(
                r'\b(?:cp|mv|rsync|git\s+add)\s+(?:[\w.-]+\s+)*([~./][\w./~-]*\.html)\b',
                command
            )
            if m:
                html_edit_idx = i
                if m.group(1) not in html_files:
                    html_files.append(m.group(1))

print(json.dumps({
    'html_edit_idx': html_edit_idx,
    'html_files': html_files,
    'chrome_evidence_idx': chrome_evidence_idx,
}))
PYEOF
)

[[ -z "$RESULT" ]] && exit 0

HTML_EDIT_IDX=$(printf '%s' "$RESULT" | /usr/bin/jq -r '.html_edit_idx')
CHROME_EVIDENCE_IDX=$(printf '%s' "$RESULT" | /usr/bin/jq -r '.chrome_evidence_idx')
HTML_FILES=$(printf '%s' "$RESULT" | /usr/bin/jq -r '.html_files | join("、")')

# 這一輪沒改過 .html，不干預
[[ "$HTML_EDIT_IDX" -lt 0 ]] && exit 0

# 有在「最後一次 html 改動之後」執行過 open -a "Google Chrome"，放行
[[ "$CHROME_EVIDENCE_IDX" -gt "$HTML_EDIT_IDX" ]] && exit 0

cat >&2 <<GUARD_EOF

🔴🔒 HTML 預覽 Chrome 查證鎖（deterministic check，非自稱，案例46）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
這一輪對話改過 .html 檔（$HTML_FILES），
但找不到「這次改動之後執行過 open -a "Google Chrome"」的紀錄。

2026-06-17 教練親口定稿：唯一指定開啟 HTML 的瀏覽器 = Google Chrome，
絕不依賴 Claude Code 內建無頭瀏覽器工具（preview_screenshot/preview_snapshot）
的截圖當作「教練已看過」的證據——那是 AI 自我除錯用，不是教練親眼看過的替代品。
2026-07-11 案例46：這條鐵律定稿後至少第四次被踩。

✅ 停下來立刻執行：
  1. open -a "Google Chrome" <改動後的檔案路徑或網址>
  2. 確認畫面正確後，再回覆教練「已改好，已用 Chrome 開給您看」
  3. 不要用「我已經截圖確認過」取代這一步——兩者不是同一件事
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GUARD_EOF

exit 2
