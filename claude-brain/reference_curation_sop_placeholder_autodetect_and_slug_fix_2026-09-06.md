---
name: reference-curation-sop-placeholder-autodetect-and-slug-fix-2026-09-06
description: 策展SOP兩項根因修復（2026-09-06凌晨）：slug只取品牌名不取整句標題+暫代頁自動偵測讓上傳網址統一取代手動七步驟
metadata: 
  node_type: memory
  type: reference
  originSessionId: e90bf397-abf3-4d08-9605-9c270e331b1f
  modified: 2026-09-05T20:11:09.735Z
---

2026-09-06凌晨教練驗收「牛市町」上架案例時，連續發現並推動兩項架構修正：

**1. slug命名根因**：`curation_process.py`原本把`<title>`標籤整句轉拼音當網址，遇到「品牌名｜行銷標語」這種常見標題格式（如「牛市町｜只漲不跌的美味 — 品牌理念」）會產生超長網址。修法：新增`primary_title_segment()`只取分隔符號（｜/—/：等）前的品牌名稱去轉拼音，commit`82b7a2a2c`。

**2. 暫代頁自動偵測**：原SOP規定「有終端機能力的AI（軍師/Hermes/OpenCode/小龍蝦）要手動做七步驟，不要走`/curation/upload`」，理由是上傳網址原本不會判斷店家是否已有`shops.bymyway.com`暫代頁、會誤建重複站。教練追問「為什麼不乾脆都走上傳網址，明明比手動快」後，直接把這個判斷寫進背景腳本：`find_existing_shop_slug()`+`overwrite_shop_placeholder()`，比對到既有slug就自動SCP覆蓋暫代頁（tar打包+遠端解壓，網址不變），查無記錄才走全新GitHub Pages流程，commit`4de7aeb3c`。**因此撤回「有能力AI要手動做」的規則**，SOUL.md(commit`3df878f1a`)+Hermes的`H_HANDOFF_LATEST.md`(commit`3d91d8e`)+SOP文件全部同步改成「不分身分一律上傳網址」。

**Why**：手動七步驟存在的唯一理由已經消失（暫代頁判斷自動化了），繼續要求有能力的AI手動做只是白白多花時間跟他們自己的token/資源。

**How to apply**：
- 之後任何「AI要不要自己動手做 vs 用自動化捷徑」的判斷，先問「捷徑功能不足的地方能不能直接補進自動化本身」，而不是預設「AI比較聰明所以要手動」——把判斷邏輯內建進系統，比每個AI各自判斷更一致、更省資源。
- `curation-prompt.md`（策展一鍵注入實際複製文字）從一開始就只寫「上傳就好，不用自己建站」，跟這次的簡化方向完全一致，不需要修改——查證後才確認，不是憑印象假設一致。
- 殘餘限制：`huitou`/`kr`兩筆最早期手動命名的暫代頁slug沒有跟著`_shop_slug()`演算法走，自動比對抓不到，未來若店家名稱剛好轉拼音撞名需人工確認一次。

相關：[[project_claude_quota_conservation_until_wednesday_2026-09-06]]（同一場對話也釐清了「觸發動作的執行者是誰」對token消耗的影響）
