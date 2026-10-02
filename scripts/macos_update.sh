#!/bin/bash
# 安裝 macOS 更新並自動重開機（2026-10-03）
# 為什麼不能只用 sudo：蘋果晶片的 Mac 安裝 macOS 更新時，softwareupdate 還要驗證「磁碟擁有者」，
#   只用 `sudo -A softwareupdate -i` 會停在 "Password:" 然後 "Failed to authenticate"（10/03 01:28 實測）；
#   要加 `--user <帳號> --stdinpass`，密碼從 stdin 給。
# 用法：bash ~/.openclaw/workspace/scripts/macos_update.sh "macOS Tahoe 26.7.1-25G241"
#   更新名稱用 `softwareupdate -l` 看 Label。更新前必須 6 小時內有時光機備份（反射 R-BACKUP-BEFORE-UPGRADE 會擋）。
# 密碼：只由教練在跳出的視窗輸入，只放在這支腳本的變數裡，透過 stdin 交給 sudo 與 softwareupdate，
#   不進指令列、不印出、不寫紀錄；AI 看不到。
set -u

LABEL="${1:-}"
[ -n "$LABEL" ] || { echo "用法：macos_update.sh \"<更新名稱，例如 macOS Tahoe 26.7.1-25G241>\""; exit 2; }

DIALOG="/Users/bymyway/.openclaw/workspace/scripts/coach_password_dialog.sh"
LOG="/Users/bymyway/.openclaw/workspace/state/macos_update_$(date +%Y%m%d).log"
ME="$(id -un)"

PW="$(COACH_PW_MSG="要安裝 $LABEL。請輸入 Mac 開機密碼後按「確定」（不要按取消）；約 15~30 分鐘後電腦會自動重開機。" "$DIALOG")" \
  || { echo "❌ 密碼視窗被取消，沒有做任何事"; exit 1; }
[ -n "$PW" ] || { echo "❌ 沒有輸入密碼，沒有做任何事"; exit 1; }

echo "[$(date '+%H:%M:%S')] 開始安裝 $LABEL（帳號 $ME）" | tee -a "$LOG"
# 兩行密碼：sudo 若要密碼就吃第一行，softwareupdate 吃剩下那行；sudo 若已有授權，softwareupdate 就吃第一行
printf '%s\n%s\n' "$PW" "$PW" | sudo -S -p '' softwareupdate -i "$LABEL" -R --user "$ME" --stdinpass 2>&1 | tee -a "$LOG"
rc=${PIPESTATUS[1]}
unset PW
echo "[$(date '+%H:%M:%S')] softwareupdate 結束，代碼 $rc" | tee -a "$LOG"
exit "$rc"
