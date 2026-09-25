#!/bin/bash
# 發布公開交接棒：機密掃描 → 只 commit status.md → push → 確認網站真的換成新版本。
# 網址：https://coach1973.github.io/ai-go/status.md（GitHub Pages，push 就上線，不耗 Netlify 點數）
REPO="/Users/bymyway/github_repos/ai-go"
URL="https://coach1973.github.io/ai-go/status.md"

bash "$(dirname "$0")/public_status_guard.sh" "$REPO/status.md" || exit 1

cd "$REPO" || exit 1
git add status.md
if git diff --cached --quiet; then
  echo "status.md 沒有變動，不用發布"
  exit 0
fi
git commit -q -m "公開交接棒更新 $(date '+%Y-%m-%d %H:%M')" || exit 1
git push -q origin main || { echo "❌ push 失敗"; exit 1; }
HASH=$(git rev-parse --short HEAD)

STAMP=$(grep -m1 '最後更新' status.md)
for _ in $(seq 1 18); do
  if curl -s "$URL?v=$(date +%s)" | grep -qF "$STAMP"; then
    echo "✅ 已上線 commit $HASH：$URL"
    exit 0
  fi
  sleep 10
done
echo "⚠️ 已 push（commit $HASH），但 3 分鐘內網站還沒換成新版，稍後再查 $URL"
exit 1
