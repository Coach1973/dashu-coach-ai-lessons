#!/bin/bash
# Mac 存活心跳燈塔（v2：只寫本地檔，不推 GitHub）
# 每 30 分鐘寫時間戳進 monitoring/mac_alive.txt
# ACER/聯想 用 SSH 讀這個檔案即可判斷 Mac 是否活著

WORKSPACE=/Users/bymyway/.openclaw/workspace
mkdir -p "$WORKSPACE/monitoring"
FILE="$WORKSPACE/monitoring/mac_alive.txt"

{
  echo "last_seen: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "hostname: $(hostname)"
  echo "uptime: $(uptime | sed 's/^[[:space:]]*//')"
  echo "loadavg: $(sysctl -n vm.loadavg)"
  echo "hermes_gateway_pid: $(pgrep -f 'hermes_cli.main gateway' | head -1)"
  echo "openclaw_gateway_pid: $(pgrep -f 'openclaw/dist/index.js gateway' | head -1)"
  echo "cron_daemon_pid: $(pgrep -f 'openclaw_cron_daemon.sh' | head -1)"
  echo "epoch: $(date +%s)"
} > "$FILE"
