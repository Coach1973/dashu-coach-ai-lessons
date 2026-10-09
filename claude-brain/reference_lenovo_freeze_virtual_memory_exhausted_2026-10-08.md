---
name: reference-lenovo-freeze-virtual-memory-exhausted-2026-10-08
description: 聯想 10/08 22:45 當機＝虛擬記憶體用完（分頁檔被手動固定 4GB、自動管理關閉，上限只有 43.7GB）；Chrome/畫面程式跟著崩，教練 Ctrl+Alt+Del 登出才恢復；登入後閃過的視窗是開機自動啟動的約 20 個程式，不是病毒
metadata:
  node_type: memory
  type: reference
  originSessionId: aea70816-8830-4634-a095-50f304ccfa8f
  modified: 2026-10-08T14:57:39.214Z
---

**事件（2026-10-08，聯想）**
- 22:45:43 系統跳「虛擬記憶體用完」警告（事件記錄 Application Popup 26）。
- 22:51 Chrome 開不起來（0xc000012d＝記憶體上限用完）、Lenovo Vantage 崩潰、畫面程式 dwm 結束重啟（0xc00001ad）、LogiOverlay 崩潰。
- 22:52:24 教練登出，22:52:29 登入後恢復。之後沒有任何錯誤彈窗紀錄。

**根因線索**
- 分頁檔 `C:\pagefile.sys` 被手動固定 4096 MB、`AutomaticManagedPagefile=False`；實體 39.7GB＋分頁 4GB＝上限 43.7GB。某個程式把記憶體吃滿就會撞上限。
- 是哪個程式吃掉的**查不到**：系統的記憶體不足偵測（Resource-Exhaustion-Detector 2004）沒有留紀錄，工作排程器紀錄也沒開。恢復後前幾名：claude 1.8GB、comet 1.7GB、LINE 1.4GB，都正常。

**登入後閃過的視窗**
- 不是排程腳本（登入後只有 Comet／Google 更新程式、iTop 錄影自動啟動，沒有會開黑窗的工作）。
- 是開機自動啟動的程式一次全開（Run 機碼＋啟動資料夾約 20 個：LINE、Signal、Typeless、Gemini、Edge、OneDrive、Comet、CountdownAnniversary、Sidebar110、RustDesk、Tailscale、中華電信 HiCOS、跨平台網頁元件、合庫 TCB×3、玉山 ATM、羅技等）。

**How to apply**
- 再當機先查：`Get-WinEvent` System/Application 找 Application Popup 26「虛擬記憶體用完」。
- 建議分頁檔改「系統自動管理」或加大；這是系統設定，AI 不能代改，只能打開到那一格給教練按。
- PowerShell 腳本含中文必須加 UTF-8 BOM，否則被當 cp950 讀壞（同 [[reference_windows_file_scan_silent_zero_traps_2026-10-06]]）。
