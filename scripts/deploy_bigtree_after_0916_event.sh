#!/bin/bash
# 一次性排程：9/16「當古典音樂遇到AI科技」高雄場活動結束後，把 bigtree repo 部署到 Netlify 正式站
# 教練 2026-08-28 口諭：「先不用，活動結束時，再自動移過去」
set -e

REPO="/e/Claude-Data/github_repos/bigtree"
SITE_ID="40e580f0-1def-4777-adb8-587ef023ed36"
TOKEN="nfp_QMBMfwYKEGqxokQ2WU9CERSRwLp4yVapa838"
ZIP="/tmp/bigtree-deploy-$(date +%s).zip"

cd "$REPO"
git pull origin main

git archive HEAD --format=zip -o "$ZIP"

RESULT=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/zip" \
  --data-binary "@$ZIP" \
  "https://api.netlify.com/api/v1/sites/$SITE_ID/deploys")

rm -f "$ZIP"

echo "$RESULT"
