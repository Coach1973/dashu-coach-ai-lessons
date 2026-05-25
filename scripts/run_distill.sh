#!/bin/bash
# 增量蒸餾 wrapper：cd 到 workspace 再跑，防止路徑問題
cd /Users/bymyway/.openclaw/workspace
/opt/homebrew/bin/node scripts/distill_incremental.js >> /tmp/distill_incremental.log 2>&1
