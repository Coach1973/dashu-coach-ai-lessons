# Windows 軍師 SOP v1.1 簽署確認

## 1. 本人已讀完

- `knowledges/SOP_windows_mac_kickoff_protocol.md` **v1.1**（含危險指令鐵律整章）
- `knowledges/IDENTITY_windows_desktop.md`（Windows 桌面版 GUI 身份卡）
- 試金石案例 24 完整剖析（636 GB E 槽蒸發，JUNSHI_HANDOFF_LATEST.md v27 第 2 節）

## 2. 承諾遵守

- **commit 前綴 `[Win]`**——區分 Mac 軍師的 `[Mac]`
- **任何刪除走 `Safe-Remove`**——禁止直接 `Remove-Item -Recurse -Force`
- **超過 1 GB 任何身份不得自主刪除**——必須教練親口此刻授權
- **Bash 呼叫 PowerShell 絕不用 `$variable` 傳路徑**——路徑必須硬編碼進 PowerShell 字串（案例 24 根因鐵律）

## 3. 案例 24 根因複述

跨 shell 跳脫：Bash 先解析 `$temp`，PowerShell 收到空字串，`Remove-Item -Recurse -Force` 沒有參數時 fallback 從當前目錄（`E:\`）遞迴刪，636 GB 蒸發。

## 4. 簽署時間

2026-06-17 20:30 台灣時間

## 5. 簽署人

Windows 桌面版軍師，Claude Sonnet 4.6（claude-sonnet-4-6）
