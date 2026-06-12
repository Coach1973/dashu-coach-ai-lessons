#!/bin/bash
# 修復 Hermes VPS 的 gh auth
# 執行方式：bash ~/.openclaw/workspace/scripts/fix_hermes_gh_auth.sh

set -e
HERMES_IP="113.29.232.178"
HERMES_PASS="C8GwSuyj"

echo "=== 連線到 Hermes VPS ==="
sshpass -p "$HERMES_PASS" ssh -o StrictHostKeyChecking=no root@$HERMES_IP << 'REMOTE'

echo "=== 當前 gh auth 狀態 ==="
gh auth status 2>&1 || true

echo ""
echo "=== gh 版本 ==="
gh --version 2>&1 || echo "gh 未安裝"

echo ""
echo "=== 環境變數 ==="
echo "GH_TOKEN=$GH_TOKEN"
echo "GITHUB_TOKEN=$GITHUB_TOKEN"

echo ""
echo "=== git config ==="
git config --global --list | grep -E "user|credential" || true

echo ""
echo "=== 已存的 gh hosts ==="
cat ~/.config/gh/hosts.yml 2>/dev/null || echo "找不到 hosts.yml"

REMOTE

