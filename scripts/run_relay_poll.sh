#!/bin/bash
# Python3 cron wrapper：cd 到 workspace 再跑，防止路徑問題
# 使用 python3.13（python3.14 有路徑問題）
cd /Users/bymyway/.openclaw/workspace
/opt/homebrew/Cellar/python@3.13/3.13.12_1/bin/python3.13 /Users/bymyway/.openclaw/workspace/scripts/relay_poll.py >> /tmp/relay_poll.log 2>&1
