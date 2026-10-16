#!/bin/bash
# launchagents_guard.sh — 網站自動啟動設定檔守門員
#
# 起因（2026-10-16）：~/Library/LaunchAgents 裡的 com.coach.* 設定檔在 10/3～10/4 之間被刪，
#   服務靠記憶體裡的設定撐了 12 天沒人發現；10/16 08:44 Mac 登出再登入，記憶體清空、
#   找不到設定檔，event／chapters／namecard／真鑽等十幾個網站斷線 3～4 小時。
#   詳見記憶 reference_launchagents_plists_deleted_outage_2026-10-16。
#
# 觸發（事件，不輪詢）：ai.openclaw.launchagents-guard 用 launchd WatchPaths 監看
#   ~/Library/LaunchAgents，資料夾一有變動就跑；每次登入也跑一次（RunAtLoad）。
#
# 做的事：以 git 裡的 ops/launchagents_backup/com.coach.*.plist 為準——
#   1) ~/Library/LaunchAgents 少了 → 複製回去並載入
#   2) 檔案在、但沒載入 → 載入
#   有補任何東西就通知教練＋寫紀錄；全部正常就安靜結束。
#
# 要正式停掉某個服務：把它從 ops/launchagents_backup/ 刪掉並 commit，否則會被補回來。

set -uo pipefail
BACKUP=/Users/bymyway/.openclaw/workspace/ops/launchagents_backup
LA=/Users/bymyway/Library/LaunchAgents
LOG=/Users/bymyway/Library/Logs/openclaw/launchagents_guard.log
NOTIFY=/Users/bymyway/.openclaw/workspace/scripts/notify_coach.sh
U=$(id -u)
mkdir -p "$(dirname "$LOG")"
ts() { TZ=Asia/Taipei date '+%Y-%m-%d %H:%M:%S'; }
is_loaded() { launchctl list | awk '{print $3}' | grep -qx "$1"; }

# 等一下：大批搬移／刪除還在進行，或剛登入、launchd 還在逐一載入
sleep "${GUARD_WAIT_SEC:-10}"

[ -d "$BACKUP" ] || { echo "[$(ts)] ❌ 找不到備份資料夾 $BACKUP" >> "$LOG"; exit 1; }

FIXED=()
for src in "$BACKUP"/com.coach.*.plist "$BACKUP"/ai.openclaw.*.plist; do  # 10/16 盤查：小龍蝦本體(gateway)等 ai.openclaw.* 也要保護
  [ -e "$src" ] || continue
  f=$(basename "$src"); label=${f%.plist}; dst="$LA/$f"
  if [ ! -e "$dst" ]; then
    if cp -p "$src" "$dst"; then FIXED+=("補回設定檔 $label"); else echo "[$(ts)] ❌ 複製失敗 $label" >> "$LOG"; continue; fi
  fi
  if ! is_loaded "$label"; then
    out=$(launchctl bootstrap "gui/$U" "$dst" 2>&1)
    if is_loaded "$label"; then FIXED+=("重新載入 $label"); else echo "[$(ts)] ❌ 載入失敗 $label：$out" >> "$LOG"; fi
  fi
done

if [ ${#FIXED[@]} -gt 0 ]; then
  msg="🛡️ 網站自動啟動設定檔有 ${#FIXED[@]} 件不對，已自動補好（$(ts) 台灣時間）"$'\n'"$(printf '・%s\n' "${FIXED[@]}")"
  echo "[$(ts)] $msg" >> "$LOG"
  "$NOTIFY" "$msg" 600 launchagents_guard >/dev/null 2>&1 || echo "[$(ts)] ❌ 通知送出失敗" >> "$LOG"
else
  echo "[$(ts)] ✅ 全部 $(ls "$BACKUP"/com.coach.*.plist "$BACKUP"/ai.openclaw.*.plist | wc -l | tr -d ' ') 個設定檔都在、都已載入" >> "$LOG"
fi
# 登入／設定檔變動後，實測各網站公開網址真的連得到（530／1033／連不上＝掛了）。事件觸發，不輪詢。
SITES=(chapters trust event shops mentor100 namecard peipei-event sincere team team01 real-wealth zhenxin real-diamonds)
DOWN=()
for round in 1 2 3 4 5 6; do
  DOWN=()
  for h in "${SITES[@]}"; do
    code=$(curl -s -o /dev/null -m 10 -w '%{http_code}' "https://$h.bymyway.com/" 2>/dev/null)
    case "$code" in 2*|3*|4*) ;; *) DOWN+=("$h.bymyway.com（${code}）") ;; esac
  done
  [ ${#DOWN[@]} -eq 0 ] && break
  [ "$round" -lt 6 ] && sleep 15
done
if [ ${#DOWN[@]} -gt 0 ]; then
  msg="🚨 網站連不上（$(ts) 台灣時間，等了約 75 秒仍不通）"$'\n'"$(printf '・%s\n' "${DOWN[@]}")"
  echo "[$(ts)] $msg" >> "$LOG"
  "$NOTIFY" "$msg" 600 sites_down >/dev/null 2>&1 || echo "[$(ts)] ❌ 通知送出失敗" >> "$LOG"
else
  echo "[$(ts)] ✅ ${#SITES[@]} 個網站公開網址實測都連得到" >> "$LOG"
fi
exit 0
