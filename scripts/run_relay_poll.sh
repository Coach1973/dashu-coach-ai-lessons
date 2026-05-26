#!/bin/bash
# Python3 cron wrapper：cd 到 workspace 再跑，防止路徑問題
cd /Users/bymyway/.openclaw/workspace
/opt/homebrew/bin/python3 /Users/bymyway/.openclaw/workspace/scripts/relay_poll.py >> /tmp/relay_poll.log 2>&1
