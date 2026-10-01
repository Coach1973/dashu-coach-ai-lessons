---
name: feedback-remote-connect-do-it-for-coach-no-jargon
description: 遠端連線/需管理員權限的事，替教練做完（桌面捷徑、剪貼簿指令），不叫他找欄位、不講術語、不提密碼
metadata:
  type: feedback
---
教練 2026-10-01 在宏碁因連不上 Mac 發火：同一件事一直叫他做、說不清欄位在哪、一直提密碼。
**Why**：他把電腦主控權都給軍師了，期待能自動化的就自動化；RustDesk 連失敗真因是他點到「ID」卡片走了壞掉的官方 21116，不是他不會用。
**How to apply**：
- RustDesk 一律建桌面捷徑 `rustdesk.exe --connect <Tailscale IP>`（Mac=100.91.228.91、宏碁=100.78.106.14、聯想=100.95.122.29），不叫他輸入「遠端ID」。
- 需管理員權限：背景 `Start-Process -Verb RunAs` 會靜默失敗；改請他「開始→PowerShell→右鍵系統管理員身分執行」，指令用 `clip` 放進剪貼簿。
- 不說 UAC 等術語、不主動提密碼（固定密碼早設好）。
- 連線除錯先讀 `%APPDATA%\RustDesk\log`。
相關：[[feedback-chapter-dashboards-record-only-no-stats]]
