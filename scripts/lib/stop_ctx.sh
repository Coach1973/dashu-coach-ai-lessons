#!/bin/bash
# Stop hook 共用對話紀錄快取層（2026-08-12 全面體檢第2項）
#
# 用途：同一個 Stop 事件裡，10 支 rule hook 需要的 transcript 欄位只解析一次。
#       第一支呼叫的 hook 付解析成本並寫快取，後面 9 支直接讀快取。
#
# 用法：CTX=$(bash lib/stop_ctx.sh "$TRANSCRIPT_PATH" "$SESSION_ID")
#       欄位用 jq 取：printf '%s' "$CTX" | jq -r '.last_assistant_text'
#
# 快取鍵綁死 transcript 的「大小＋修改時間」——檔案只要有變動就重算，
# 不會拿到過期資料（寧可多算一次，不可判錯守則）。
set -uo pipefail

TRANSCRIPT_PATH="${1:-}"
SESSION_ID="${2:-nosession}"
EXTRACTOR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/stop_ctx_extract.py"

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 1
[[ -f "$EXTRACTOR" ]] || exit 1

SIZE=$(stat -f %z "$TRANSCRIPT_PATH" 2>/dev/null || echo 0)
MTIME=$(stat -f %m "$TRANSCRIPT_PATH" 2>/dev/null || echo 0)
SAFE_SESSION=$(printf '%s' "$SESSION_ID" | tr -c 'a-zA-Z0-9_-' '_')
CACHE="${TMPDIR:-/tmp}/stop_ctx_${SAFE_SESSION}_${SIZE}_${MTIME}.json"

# 快取命中（且不是空檔）→ 直接吐出，不再解析
if [[ -s "$CACHE" ]]; then
  cat "$CACHE"
  exit 0
fi

OUT=$(python3 "$EXTRACTOR" "$TRANSCRIPT_PATH" 2>/dev/null)
[[ -z "$OUT" ]] && exit 1

# 先寫暫存再 mv，避免另一支 hook 讀到寫一半的檔案
TMP="${CACHE}.$$"
printf '%s' "$OUT" > "$TMP" 2>/dev/null && mv -f "$TMP" "$CACHE" 2>/dev/null || rm -f "$TMP" 2>/dev/null

# 順手清掉兩天前的舊快取（同一個 session 每輪都會產生一份新鍵）
find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'stop_ctx_*.json' -mtime +2 -delete 2>/dev/null || true

printf '%s' "$OUT"
exit 0
