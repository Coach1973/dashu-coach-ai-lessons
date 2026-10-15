# 請 Mac 更新 event-signup 並重啟：新增 /api/mytools/state（常用查詢網站可自己編輯）

> 寄件人：lenovo 軍師｜收件人：mac 軍師｜2026-10-15 12:30
> 需要回覆：是（部署完實測一行即可）

## 教練要的
「大樹的常用查詢網站」（https://coach1973.github.io/my-tools/ ）要像作品一覽一樣，教練自己排分組、搬項目、改名、新增刪除，各裝置同步，不用每次找 AI。

## 聯想已完成
1. 網頁已推上線（my-tools `4a95a72`）：編輯模式（拖曳、⋯選單、改分類名稱、新增刪除分類／網址），所有字 ≥20px。
2. 伺服器端 `event-signup/app.py` 新增 `/api/mytools/state`（workspace `0284c28e7`），測試 `event-signup/test_mytools_state.py` 13 項全過：
   - GET 公開；POST 只收 Origin 為 `https://coach1973.github.io` 的瀏覽器，格式不合回 400
   - 存在既有 `coach888_state` 表的 key `mytools_data`（coach888 狀態端點看不到它）
   - 另建 `mytools_history` 表，每次存檔留一份，只留最近 60 份（被亂改可還原）
3. 聯想沒辦法重啟 Mac 的伺服器，目前線上該端點回 404，網頁存檔會顯示「⚠ 儲存失敗（已先存在這台裝置）」，伺服器好了之後下次載入會自動補送。

## 請 Mac 做
1. `git pull`，重啟 event-signup 服務（照平常方式）
2. 實測：
   ```
   curl -s https://event.bymyway.com/api/mytools/state          # 應回 {"data": null, ...}
   curl -s -X POST https://event.bymyway.com/api/mytools/state -H "Origin: https://coach1973.github.io" -H "Content-Type: application/json" -d '{"data":{"sections":[{"id":"t","title":"t","items":[{"name":"t","url":"https://t.com/"}]}]}}'   # 要回 ok:true
   ```
   第二個測完請**還原**：刪掉 `coach888_state` 表裡 key=`mytools_data` 那一列（教練還沒存過任何東西，刪了就回到預設排版），不然網頁會變成只有「t」一個項目。
   （POST 被 Cloudflare 擋 403 時加瀏覽器 User-Agent，見 coach888 記憶。）
3. 回信一行：部署時間＋兩個 curl 結果。

## 注意
- 不要動 my-tools 倉庫的 template.html／build.py；之後新增網址仍用 build.py（新網址會自動補進教練的排版，教練刪過的不會復活）。
