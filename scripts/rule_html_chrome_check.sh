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

# 2026-08-12 體檢第2項：偵測邏輯整段搬進 lib/stop_ctx_extract.py 的 html_chrome()，
# 語意逐字不變——包含「只看最近 100 筆事件」、「只認明確的 open -a Google Chrome
# 不收無頭預覽工具」、以及案例52 同日兩次調校後的部署指令正則（要求 cp/mv/rsync/
# git add 後面緊接真正的檔案路徑，避免 commit message 裡的純文字描述被誤抓）。
SESSION_ID=$(printf '%s' "$INPUT" | /usr/bin/jq -r '.session_id // ""' 2>/dev/null)
CTX=$(bash /Users/bymyway/.openclaw/workspace/scripts/lib/stop_ctx.sh "$TRANSCRIPT_PATH" "$SESSION_ID" 2>/dev/null) || exit 0
[[ -z "$CTX" ]] && exit 0

HTML_EDIT_IDX=$(printf '%s' "$CTX" | /usr/bin/jq -r '.html_edit_idx' 2>/dev/null)
CHROME_EVIDENCE_IDX=$(printf '%s' "$CTX" | /usr/bin/jq -r '.chrome_evidence_idx' 2>/dev/null)
HTML_FILES=$(printf '%s' "$CTX" | /usr/bin/jq -r '.html_files | join("、")' 2>/dev/null)

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
