---
name: project_lenovo_nonpaged_pool_leak_2026-09-04
description: 聯想Windows記憶體洩漏根因確診：Windows Update會自動把已解除安裝的Nahimic驅動裝回去，需群組原則封鎖才能斷根
metadata: 
  node_type: memory
  type: project
  originSessionId: 1583342f-6c6a-4f3a-85c0-5749ee197c32
  modified: 2026-09-04T10:53:19.359Z
---

教練回報這台聯想Windows開機後記憶體飆到98%，懷疑中毒，要求安全排查+網路流量檢查。全面排查（Defender即時防護開啟/病毒碼最新/零威脅紀錄、前25大耗記憶體程式全是教練平常在用的Comet/LINE/Claude/Typeless/Signal、對外連線埠全是443+高位隨機埠、無Temp/Public資料夾藏匿程式）排除中毒可能。

真正元凶：核心層 Nonpaged Pool（驅動程式專用記憶體，正常僅幾百MB）暴增到29GB，全部process加總記憶體只有10GB卻對不上系統回報用掉38GB，落差全在這裡。鎖定嫌疑是 **Nahimic 音效驅動**（NahimicBTLink.sys+Nahimic_Mirroring.sys，檔案日期2022/8/18已4年沒更新，只存在於裝置管理員「音效/軟體元件」分類，不在新增/移除程式清單），已教練手動從裝置管理員解除安裝3個Nahimic裝置+勾選刪除驅動程式軟體+重開機的步驟。

重開機驗證：記憶體從97.76%瞬間降到33.1%，Nonpaged Pool歸零，證實診斷方向正確。但約1h56m後（教練同時段新裝了Intel顯示卡驅動31.0.101.4255/NVIDIA GeForce Experience 3.27.0.114/聯想電競功能修補程式，且**尚未確認是否已移除Nahimic**），Nonpaged Pool又衝到22GB，比第一次21.5小時才洩漏到29GB快了近10倍。教練一度誤以為是「Claude Code開Chrome瀏覽器做網頁」造成——查證系統當時根本沒有chrome.exe在跑，Comet+Claude合法用量僅約4GB，跟22GB缺口對不上，已澄清仍是驅動層洩漏非瀏覽器/AI工具造成。

**Why**：教練半夜擔心中毒想直接用「一鍵還原」重灌，已用證據排除中毒疑慮改走驅動除錯路徑，避免不必要的大動作。

**How to apply**：下次教練提到這台機器記憶體又飆高，先問「Nahimic移除了嗎／重開機後多久又飆高」；用 `powershell -NoProfile -Command 'Get-Counter "\Memory\Pool Nonpaged Bytes" | Select-Object -ExpandProperty CounterSamples | Select-Object CookedValue'` 快速確認是否為同一種洩漏（正常應僅幾百MB，超過1-2GB即視為異常）。若確認Nahimic已移除但洩漏仍快速復發，嫌疑轉移到新裝的Intel/NVIDIA/聯想電競驅動，可建議逐一解除安裝排除測試。參見 [[reference_gitbash_powershell_dollar_underscore_quoting_2026-09-04]]（本次診斷用到的PowerShell指令技巧）。

---

**2026-09-04 下午補充：真正根因確診——Windows Update自動把已解除安裝的Nahimic驅動裝回去**

教練回報「沒開幾個網站記憶體就65%」，重新排查發現：這台機器當天下午3:42才剛開機，開機僅44分鐘Nonpaged Pool就已飆到10.1GB，比先前任何一次洩漏速度都快。查`Get-PnpDevice`/`Win32_SystemDriver`確認Nahimic兩支驅動(NahimicBTLink/Nahimic_Mirroring)當下仍是Running/OK狀態——**並未真正移除**。

進一步查`Microsoft-Windows-Kernel-PnP/Configuration`事件記錄+`Microsoft-Windows-Servicing`記錄，抓到同一天完整時間軸：15:09裝上→15:13被解除安裝→**15:42開機那一刻自動裝回來**，事件記錄明確寫著「符合Windows更新更新ID 61ec07d9-d2a3-4531-9b0b-b8a62718311e」。結論：Nahimic驅動已被Windows Update登記為這張內建Realtek音效卡(INTELAUDIO\FUNC_01&VEN_10EC&DEV_0257)的驅動更新項目，**每次裝置管理員解除安裝之後，只要重開機/裝置重新列舉，Windows Update就會自動重裝**。這才是先前「重開機驗證有效但2小時內更快復發」的真正機制——不是解除安裝沒生效，是Windows主動裝回去的。

**正確解法（比單純裝置管理員解除安裝多一步）**：這台是Windows 11專業工作站版，需先用`gpedit.msc`（電腦設定→系統管理範本→Windows元件→Windows Update）啟用「不要在Windows品質更新中包含驅動程式」，封鎖Windows Update推送驅動更新的管道，**再**重開機+裝置管理員解除安裝3個Nahimic裝置（勾選刪除驅動程式軟體），這樣才能真正斷根。此為系統設定變更，屬於AI不可自主執行的類別，已交由教練親自操作，待教練完成後需再次查Nonpaged Pool確認是否維持正常。

---

**2026-09-04 晚間：教練推翻驅動診斷，改採一鍵還原+觀察，AI不再堅持**

教練晚間直接把整台機器用「易數一鍵還原」復原到8/10備份狀態（非單獨解除驅動），理由：「用了這麼久都沒有問題，昨天才出問題，一直認為是昨天瀏覽了一些網站有問題」，且不想再經歷「移除驅動、重開機、又這又那」的反覆流程。復原後記憶體持續在50%以下，教練要求觀察到當晚12點，確認穩定後**再對這個9/4現況做一次新的一鍵備份**取代舊基準。

**Why**：教練明確表態「不想跟你爭論」——即使AI手上有Windows事件記錄的具體證據（Windows Update於15:42開機時自動重裝Nahimic驅動），教練仍優先選擇「重灌更省事」的路徑，且觀察結果（復原後穩定）本身就是最終的驗證標準。

**How to apply**：這件事到此為止，除非記憶體洩漏症狀真的復發，否則不要再主動提起Nahimic/驅動層根因。教練觀察到12點沒事就會另外做新備份，AI沒有背景監測能力，不用承諾「幫忙盯到12點」，等教練回報結果即可。
