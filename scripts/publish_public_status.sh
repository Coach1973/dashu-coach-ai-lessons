#!/bin/bash
# 發布公開交接棒：機密掃描 → 產生 status.html → commit → push → 確認網站真的換成新版本。
# 主要網址（HTML，貼給任何 AI 都讀得到）：https://coach1973.github.io/ai-go/status.html
# 純文字備用：https://coach1973.github.io/ai-go/status.md
REPO="/Users/bymyway/github_repos/ai-go"
URL="https://coach1973.github.io/ai-go/status.html"

cd "$REPO" || exit 1

# system-prompt.md（外帶版21條+N1~N9）改成從 特助心法.md／執行細則.md 自動重新產生，
# 不再靠人手動同步——2026-09-25教練發現外帶版停在9/14舊版E01~E13，內部早就併成N1~N9，
# 兩邊分岔了十幾天沒人發現。每次「總結」發布都順便重跑，來源沒變就不會產生新commit。
python3 "$(dirname "$0")/render_public_system_prompt.py" "$REPO/system-prompt.md" || exit 1

# status.md 每次都可能變（由「總結」改寫）；coach-persona.md 教練親自改才會變，
# system-prompt.md 現在是自動產生；但每次都重轉一遍不會有害（沒變動git就不會產生新commit），
# 順便保證三份.md/.html永遠不分岔
for f in status coach-persona system-prompt; do
  bash "$(dirname "$0")/public_status_guard.sh" "$REPO/$f.md" || exit 1
  python3 "$(dirname "$0")/render_public_status_html.py" "$f.md" "$f.html" || exit 1
  bash "$(dirname "$0")/public_status_guard.sh" "$REPO/$f.html" || exit 1
done

git add status.md status.html coach-persona.md coach-persona.html system-prompt.md system-prompt.html
if git diff --cached --quiet; then
  echo "status.md / status.html 沒有變動，不用發布"
  exit 0
fi
git commit -q -m "公開交接棒更新 $(date '+%Y-%m-%d %H:%M')" || exit 1
git push -q origin main || { echo "❌ push 失敗"; exit 1; }
HASH=$(git rev-parse --short HEAD)

# push 才是真正決定成敗的動作，已經成功；以下只是「順便確認CDN換版了沒」，
# GitHub Pages CDN偶爾要等超過5分鐘才會全球生效(2026-09-25實測遇過2次)，
# 查不到不代表沒發布成功，所以這裡不再用exit 1嚇人，只如實回報快取狀態。
STAMP=$(grep -m1 '最後更新' status.md)
TRIES=30; WAIT_SEC=$((TRIES * 10))
for _ in $(seq 1 $TRIES); do
  if curl -s "$URL?v=$(date +%s)" | grep -qF "$STAMP"; then
    echo "✅ 已推送且確認上線 commit $HASH：$URL"
    exit 0
  fi
  sleep 10
done
echo "✅ 已推送 commit $HASH（push本身成功）：$URL"
echo "⏳ 但等了 ${WAIT_SEC} 秒，GitHub Pages CDN 還沒換成新版，是快取延遲，不是發布失敗，稍後自然會更新"
exit 0
