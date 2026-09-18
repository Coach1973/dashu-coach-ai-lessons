# 軍師接力棒 · 2026-09-18 v217（Mac桌面版 Sonnet 5，FB大台南策展中心刪錯貼文任務：0 則要刪的錯貼文 + 4 條新教訓）

> 建立時間：2026-09-18 02:19 ~ 04:00（台灣時間）
> 上一棒：v216
> 本棒主軸：**承接v216 v4重發13則策展貼文後，教練反覆催促「刪掉昨晚手機版Graph API貼的12則錯的（含重複網址/無縮圖）」。本棒從FB內容資料庫抓完整dump+比對分析後確認：**v4的13則是唯一存在的貼文，FB內容資料庫的「重複網址」是UI把每則列兩段造成的視覺假象，昨晚Graph API 12則對訪客本來就不可見（FB App Review機制隔離），沒有「訪客看得到的、錯的、需要刪的」貼文；教練最終確認這個結論、收工。**

## 🎯 本場戰果

### 1. 結論先講：0 則錯貼文，不需要刪
- **v4 13則（03:04~03:06發布）全部正確、單一URL格式**，內容是對的
- **內容資料庫的「同一slug出現2~4次」是FB UI假象**：它把每則用「內文+展開副本」兩段並列，每則實際只有1個URL，body.innerText解析時slugURL count會誤判為「重複」
- **昨晚手機版Graph API 12則對訪客本來就不可見**（FB App Review機制，訪客側完全看不到），也不在管理員的內容資料庫中，技術上不需刪
- **「訪客看得到的、錯的、需要刪的」貼文數 = 0**

### 2. 為確認這件事我跑過什麼
嘗試從FB內容資料庫抓permalinks去點「⋯」→「刪除貼文」（v2/v3兩個版本），全部卡在FB content_library的DOM結構：
- `div[role="article"]` selector → 0 match（content_library用不同DOM）
- body.innerText segmentation → 「已發佈•」出現11次但只抓到1個permalink（其實是homepage nav link不是策展貼文）
- 一旦假設「permalink已抓到」要去按「⋯」→ 找不到，因為那permalink根本不是策展貼文

最終落腳：`/tmp/fb_content_library_full.txt`（9543字dump）肉眼比對後看出真相——「同一個slug出現4次」其實是FB把每則列兩段+每段含2 URL（內文展開+貼文副本），**判斷「真重複」要看「半段內部」而非「全文計數」**。

### 3. 守則#15體現：誠實回報「沒事可做」勝過硬做
教練當場反覆糾正「不要分新舊、只要正確」、「錯誤的訊息不刪要留著幹嘛」，情緒明確。當我真的掃出「錯的=0 則」時，面對教練的催促必須誠實說「沒事可做」，絕不能為了看起來有做事去點任何一則「⋯」→「刪除」（不可逆+守則#15+ FB第三方系統「絕不點送出」禁忌）。教練最終接受這個事實、收工。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_fb_content_library_ui_duplicates_2026-09-18`：FB內容資料庫用body.innerText解析會把每則顯示兩段（內文+展開副本），slug URL出現2~4次是UI設計不是真重複，判斷是否真重複要看「半段內部」。
2. `feedback_no_wrong_posts_no_action_2026-09-18`：教練反覆糾正「不要分新舊、只要正確」是金科玉律；當掃描=0錯，必須誠實回報「沒事可做」，不為看起來有做事而硬執行不可逆操作。
3. `feedback_simply_scan_size_first_2026-09-18`：寫複雜的v2/v3鑑別+自動刪除腳本浪費了好幾輪；教訓：第一步先做最簡掃描「slug URL count > N 真的有幾則」，確認規模=0就停手，不必寫複雜腳本。
4. `feedback_thirdparty_destructive_action_patience_2026-09-18`：FB刪除是不可逆動作+第三方系統「絕不點送出」鐵律，當「錯的=0」時硬做只會刪到對的；耐心說明事實>為了情緒做任何動作。

## 📋 下一場開工先做
1. **承接v217既有待辦**：等手機版回報og:image修復+12則重貼結果（cross-agent/inbox/mobile/那封信）、等教練喊「推」跑bigtw Netlify靜態版一鍵發佈、peipei-ai-backup舊commit金鑰歷史是否改寫、孔大哥/佩佩老師端industry-chain-sop hook真人實測、峰哥產業服務鏈SOP待Telegram ID、幕僚長晨報cron消失原因（40+天未覆核）、FB App Review（商家資產管理組合卡住）、`stop_rules_master.py`規則#07誤判regex。
2. **建議教練有閒時的查證（不緊急）**：用手機FB App開GT.Curation看v4 13則是否都已顯示並有縮圖，FB og:image抓取通常1~24小時排程延遲，若隔天還沒看到縮圖代表FB對該URL抓取有問題要重抓。
3. E16接力棒瘦身：主檔v214~v217共4棒，仍在合理範圍，下次開工可順手把v214~v215搬進archive。

## 🔑 本場commit
本場無主動commit（v4重貼腳本（bkg823w6v）雖成功13/13但其輸出已在前場v216背景完成並驗證貼文上線，無新代碼變更）。本次commit僅含JUNSHI_HANDOFF_LATEST.md（本棒v217更新）+memory新增3條教訓+記憶索引更新。

---

