# 軍師接力棒 · 2026-08-09（聯想 Windows 終端機 Sonnet 5，補齊三機hook同步待辦）

> 建立時間：2026-08-09 台灣時間
> 本棒執行者：聯想 Windows 終端機 Sonnet 5
> 上一棒：v103（Mac桌面版 Sonnet 5，mentor100密集迭代五連發+bigtree-tw收費更新）
> 本棒主軸：**教練說「開工」，走完六步驟開工協議後，優先處理教練要求優先的三機hook同步待辦([[project_cross_machine_hook_sync_todo_2026-08-08]])——Mac 8/8修好的3支hook裡，聯想只欠2支(截圖鎖工具名稱查證後發現本來就是對的，不用改)。**

## 🎯 本場戰果

### 1. 🎯 補上Windows版兩支hook：auto_chrome_after_html_edit.ps1 + periodic_xinfa_reload_hook.ps1
仿Mac版邏輯用純PowerShell重寫（這台python3只是Windows Store執行別名樁，exit code 49無真直譯器，不能shell out）：
- `auto_chrome_after_html_edit.ps1`：PostToolUse(matcher: Edit|Write)，碰.html檔自動`start chrome file://...`
- `periodic_xinfa_reload_hook.ps1`：UserPromptSubmit，對話滿20輪起每10輪重載21條守則全文（讀session jsonl算真實user turn數，含band去重debounce）

兩支都寫合成JSON模擬輸入實測驗證過（非只憑寫完就當生效）：html/非html分流、Edit/Write以外工具不觸發、20輪門檻/debounce邏輯用25行合成jsonl驗證curBand正確計算+第二次同band不重複輸出。已在`~/.claude/settings.json`(本機專屬，不隨git同步)註冊。

### 2. 🔴🔴 過程中額外抓到兩個這台機器才有的環境坑（模擬測試實際踩到，非憑印象）
①**PowerShell 5.1 + Big5 codepage誤讀無BOM的UTF-8原始碼**：`periodic_xinfa_reload_hook.ps1`裡有中文檔名字面量(`特助心法.md`)，第一版寫完模擬測試發現hook永遠靜默無輸出、exit 0零報錯——追查發現`Test-Path`對這個被誤讀成亂碼的路徑永遠回傳False，整支hook形同虛設。修法是給.ps1檔案本身補UTF-8 BOM（`printf '\xEF\xBB\xBF'`接原始內容），跟`screenshot_lock.ps1`原本靠「維持ASCII-only」繞開同一個坑是同根因、不同修法。
②**`[Console]::InputEncoding`預設Big5**：stdin JSON若含中文文字(例如中文檔名的`file_path`)，讀進來就先壞掉，跟腳本自身編碼問題是兩個獨立層次的同根因坑。已在兩支新hook開頭強制`[Console]::InputEncoding = UTF8`。這個坑理論上會影響任何讀stdin JSON又可能碰到中文內容的Windows PowerShell hook，值得其他機器之後寫類似hook時留意。

commit `72776028`(mac-openclaw-workflows)，已push。已同步更新接力棒狀態總表第14項。

## 📋 下一場直接開工任務
- 三機hook同步待辦剩ACER：可直接抄這兩支.ps1，但要先確認ACER的python3/jq環境限制是否跟聯想相同(這台的坑是機器特有的環境問題，不確定ACER是否也有同款python3 Windows Store樁)
- bni-chapters「真誠分會」網頁主架構問題：教練仍未說明具體是什麼，見到教練先問清楚
- 其餘卡住項目本場未觸碰，狀態不變（見狀態總表）

## 🔑 本場關鍵檔案索引
- `scripts/auto_chrome_after_html_edit.ps1`：新建
- `scripts/periodic_xinfa_reload_hook.ps1`：新建，含UTF-8 BOM
- `C:\Users\bymyw\.claude\settings.json`：新增PostToolUse+UserPromptSubmit兩處註冊（本機專屬，不隨git同步）
- commit(mac-openclaw-workflows workspace)：`72776028`
