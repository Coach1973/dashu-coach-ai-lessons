---
name: reference-macos-update-cli-apple-silicon-needs-user-stdinpass-2026-10-03
description: 蘋果晶片 Mac 用 softwareupdate 安裝 macOS 更新，只 sudo 不夠，要加 --user 帳號 --stdinpass；下載(-d)不用密碼；已寫 scripts/macos_update.sh
metadata:
  type: reference
---

2026-10-03 01:28 教練在跳出的密碼視窗輸入密碼後，`sudo -A softwareupdate -i "macOS Tahoe 26.7.1-25G241" -R` 仍停在 `Password:` → `Failed to authenticate`。原因：蘋果晶片安裝 macOS 更新時，softwareupdate 另外要驗「磁碟擁有者」，要 `--user <帳號> --stdinpass`（`softwareupdate --help` 寫 Apple Silicon only）。`softwareupdate -d`（只下載）不用密碼，可先預載。

**How to apply**：安裝 macOS 更新用 `bash ~/.openclaw/workspace/scripts/macos_update.sh "<softwareupdate -l 的 Label>"`（跳出視窗給教練輸入，密碼經 stdin、AI 看不到；第一次 01:15 視窗被取消就別自動重跳）。更新前 6 小時內要有時光機備份（反射 `R-BACKUP-BEFORE-UPGRADE`）。重開機會中斷對話，交接要先寫好。關聯：[[project_mac_backup_policy_good_state_and_pre_upgrade_2026-10-02]]。
