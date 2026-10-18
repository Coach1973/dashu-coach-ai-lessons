---
name: reference-lenovo-rustdesk-stop-service-blocked-incoming-2026-10-19
description: "聯想 RustDesk 設定檔 stop-service='Y'（至少從 9/28 起）讓別人完全連不進來；10/19 教練外出連不進來才查到，已拿掉＋加登入自動啟動；驗證要看 21118 有沒有在聽"
metadata:
  node_type: memory
  type: reference
  originSessionId: 66367ffd-1b3b-42d9-b554-6fe136f806a6
  modified: 2026-10-18T17:28:05.556Z
---

2026-10-19 01:23 教練人在外面，用 RustDesk 連不進聯想（tree，ID 535109367，Tailscale 100.95.122.29）。

**根因（查到的）**：`%APPDATA%\RustDesk\config\RustDesk2.toml` 的 `[options]` 有 `stop-service = 'Y'`（＝介面上的「服務已停止」），9/28 的備份就有。RustDesk 1.5.0 裝在 `D:\Program Files\RustDesk`，但**沒有 Windows 服務**（sc query RustDesk → 1060），伺服器是跟著介面程式跑；stop-service=Y 時不登記櫃台、不開 21118，所以 ID 和 Tailscale IP 兩條路都不通。10/01 設定 `direct-server = 'Y'` 時沒驗證 21118 有沒有在聽，以為好了。
同時還有兩件事：iPhone 的 Tailscale 離線（教練自己關的就別當故障）；官方中繼 rs-ny 21117 到 10/19 還是不通，聯想 NAT 是 ASYMMETRIC，出門用 ID 大多要靠中繼 → **出門一律用 Tailscale IP**。

**反覆發生的證據（10/19 補查）**：①8/1 同症狀已修過一次（服務裝好 RUNNING），沒撐住；②RustDesk 自己的日誌 `%APPDATA%\RustDesk\log/tray\` 有 `Uninstalling service...` 共 9 次（04/13、04/14、06/14、07/10、08/01×3、09/05 03:09、10/14 22:56），09/05 與 10/14 兩次剛好等於設定檔最後修改時間；③推論（未證實）：是 RustDesk「停止服務」動作，日誌看不出誰按的；④10/18 Mac 已測到 21118 被拒、寫了要管理員的腳本卻從沒人跑，沒有任何東西通知教練——「沒有主動預警」是教練 10/19 的主要不滿；⑤`rustdesk.exe --tray` 只開托盤、**不開 21118**，一定要普通啟動。
**根治（10/19 01:41 裝好）**：`scripts/lenovo_rustdesk_guard.ps1`（副本 `%APPDATA%\RustDesk\guard/rustdesk_guard.ps1`，HKCU Run 登入自動執行，不用管理員）。事件觸發不輪詢：等 RustDesk 程式結束或 RustDesk2.toml 變動，就拿掉 stop-service、確保 direct-server、重開、驗 21118；紀錄 `guard\guard.log`、`guard\last_repair.txt`。實測：砍程式與寫回 Y 都 15 秒內自癒。**還沒有的**：自癒失敗時主動通知教練手機（目前只留紀錄）。宏碁 10/19 離線沒檢查。
**修法（不用管理員）**：備份設定 → 關掉 RustDesk → 刪掉 stop-service 那一行 → 用 `explorer.exe "D:\Program Files\RustDesk\rustdesk.exe"` 重開（用 explorer 啟動，對話結束時才不會跟著被關掉）。另外加了 `HKCU\...\Run\RustDesk`（登入後自動啟動）。備份：`RustDesk2.toml.bak-20261019-012638`。

**驗證三件**：①`Get-NetTCPConnection -State Listen` 看到 21118；②日誌 `log/rustdesk_rCURRENT.log` 有 `Direct server listening on [::]:21118` 和 `start rendezvous mediator`；③`Test-NetConnection 100.95.122.29 -Port 21118` 是 True，而且日誌出現 `direct access from 100.95.122.29`。
**防火牆不是兇手**：這台三個設定檔的防火牆全關，另外也有 RustDesk Service 放行規則。10/01 記憶說「Windows 端防火牆只放行 100.64.0.0/10」，這台實際上沒有這條規則。

**還沒做（要教練在機器旁按「是」）**：安裝 RustDesk 系統服務，裝好後才能看到 UAC 視窗和登入畫面；現在的版本重開機後，要等有人登入 Windows 才會自動啟動。相關：[[reference-lenovo-rustdesk-no-autostart]]、[[reference-tailscale-rustdesk-direct-network-2026-10-01]]。
