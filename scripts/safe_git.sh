#!/bin/bash
# safe_git.sh — thin wrapper around safe_git.py（給 cron 較友善的介面）
# 用法：safe_git.sh <workspace_path> "<commit message>" [files...]
exec /opt/homebrew/bin/python3 /Users/bymyway/.openclaw/workspace/scripts/safe_git.py "$@"
