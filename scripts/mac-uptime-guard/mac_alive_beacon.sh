#!/bin/bash
# Mac 存活心跳燈塔
# 每 5 分鐘寫時間戳進 monitoring/mac_alive.txt 並推 GitHub
# 其他機器（ACER/聯想/VPS）看到超過 15 分鐘沒更新就知道 Mac 掛了

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

cd "$WORKSPACE"
git add monitoring/mac_alive.txt >/dev/null 2>&1
git commit -m "beacon: Mac alive $(date +%H:%M)" --no-verify >/dev/null 2>&1 && \
  git push origin main >/dev/null 2>&1
