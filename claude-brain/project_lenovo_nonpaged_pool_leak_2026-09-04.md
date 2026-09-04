---
name: project_lenovo_nonpaged_pool_leak_2026-09-04
description: 聯想Windows記憶體98%滿載查明是核心層Nonpaged Pool驅動洩漏(非病毒)，重開機後2小時內又更快復發，待確認Nahimic驅動是否已移除
metadata: 
  node_type: memory
  type: project
  originSessionId: 1583342f-6c6a-4f3a-85c0-5749ee197c32
  modified: 2026-09-04T05:51:07.961Z
---

教練回報這台聯想Windows開機後記憶體飆到98%，懷疑中毒，要求安全排查+網路流量檢查。全面排查（Defender即時防護開啟/病毒碼最新/零威脅紀錄、前25大耗記憶體程式全是教練平常在用的Comet/LINE/Claude/Typeless/Signal、對外連線埠全是443+高位隨機埠、無Temp/Public資料夾藏匿程式）排除中毒可能。

真正元凶：核心層 Nonpaged Pool（驅動程式專用記憶體，正常僅幾百MB）暴增到29GB，全部process加總記憶體只有10GB卻對不上系統回報用掉38GB，落差全在這裡。鎖定嫌疑是 **Nahimic 音效驅動**（NahimicBTLink.sys+Nahimic_Mirroring.sys，檔案日期2022/8/18已4年沒更新，只存在於裝置管理員「音效/軟體元件」分類，不在新增/移除程式清單），已教練手動從裝置管理員解除安裝3個Nahimic裝置+勾選刪除驅動程式軟體+重開機的步驟。

重開機驗證：記憶體從97.76%瞬間降到33.1%，Nonpaged Pool歸零，證實診斷方向正確。但約1h56m後（教練同時段新裝了Intel顯示卡驅動31.0.101.4255/NVIDIA GeForce Experience 3.27.0.114/聯想電競功能修補程式，且**尚未確認是否已移除Nahimic**），Nonpaged Pool又衝到22GB，比第一次21.5小時才洩漏到29GB快了近10倍。教練一度誤以為是「Claude Code開Chrome瀏覽器做網頁」造成——查證系統當時根本沒有chrome.exe在跑，Comet+Claude合法用量僅約4GB，跟22GB缺口對不上，已澄清仍是驅動層洩漏非瀏覽器/AI工具造成。

**Why**：教練半夜擔心中毒想直接用「一鍵還原」重灌，已用證據排除中毒疑慮改走驅動除錯路徑，避免不必要的大動作。

**How to apply**：下次教練提到這台機器記憶體又飆高，先問「Nahimic移除了嗎／重開機後多久又飆高」；用 `powershell -NoProfile -Command 'Get-Counter "\Memory\Pool Nonpaged Bytes" | Select-Object -ExpandProperty CounterSamples | Select-Object CookedValue'` 快速確認是否為同一種洩漏（正常應僅幾百MB，超過1-2GB即視為異常）。若確認Nahimic已移除但洩漏仍快速復發，嫌疑轉移到新裝的Intel/NVIDIA/聯想電競驅動，可建議逐一解除安裝排除測試。參見 [[reference_gitbash_powershell_dollar_underscore_quoting_2026-09-04]]（本次診斷用到的PowerShell指令技巧）。
