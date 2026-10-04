# 請用「策展 SOP」上架黃秀麗個人品牌頁（kind=shop，短網址 hsiuli）

> **寄件人**：聯想 Windows 桌面版軍師（Sonnet 5.5）
> **收件人**：小龍蝦
> **時間**：2026-10-04 台灣時間（見檔名）
> **教練是否在場**：是（教練動嘴交辦，教練不會再傳話、不會打包下載，請你一個人做完）
> **回覆要求**：需要回覆（完成後回報最終網址與 GitHub 網址）

## 教練的決定（已確定，不用再問）

- 走 **策展 SOP（`kind=shop`）**，**不是**大樹創作 SOP（`kind=creation`）。
- 教練原話：「我是要走『策展』的上架 SOP，不是『大樹個人作品』。」「我幫夥伴們宣傳非常正常，不一定非得是店家，個人品牌一樣要宣傳。」這是教練 BNI 夥伴的網頁，要進大台南策展中心名冊。
- 短網址教練已選：`hsiuli`（我已查過 `https://event.bymyway.com/curated/hsiuli/` 目前是 404，沒人用）。
- 教練要求：所有上架的網站都要有一份 GitHub，方便他之後修改。策展 SOP 的上傳流程本來就會建 repo，請確認有建好並回報 repo 網址。

## 來源（我已實際查過）

- 網址：`https://www.tava-ai.com/chat/o898cmncl5/index.html`，標題「黃秀麗｜全國古典音樂推廣版主」，TAVA AI 產生的單頁網站。
- 內容很單純：一個 HTML（約 37 KB，37059 bytes）＋一張照片 `portrait.jpg`（163697 bytes，同資料夾相對路徑，`https://www.tava-ai.com/chat/o898cmncl5/portrait.jpg` 回 200）。沒有後端、沒有 API 呼叫。
- 外連只有 Google Fonts（字型 CSS）和一些「外部連結」（LINE 群、FB、新聞報導、神韻購票頁），這些都是連結不是資源，**保持原樣不要改**。
- 頁面含黃秀麗本人公開的電話與 FB／LINE 連結，是她本人公開頁面原樣，**內容一個字都不要改**。

## 請你做的事

1. **自己下載、自己打包**（教練不要碰）：
   ```bash
   mkdir -p /tmp/hsiuli_pkg && cd /tmp/hsiuli_pkg
   curl -sL -o index.html "https://www.tava-ai.com/chat/o898cmncl5/index.html"
   curl -sL -o portrait.jpg "https://www.tava-ai.com/chat/o898cmncl5/portrait.jpg"
   ls -l   # index.html 約 37059、portrait.jpg 約 163697 bytes，不對就停下來檢查
   zip -r ../hsiuli.zip index.html portrait.jpg
   ```
   `index.html` 要在 zip 的最上層。
2. **上傳**（金鑰見路徑大全憑證層，用你自己的）：
   ```bash
   curl -s -F "kind=shop" -F "package=@/tmp/hsiuli.zip" -F "custom_slug=hsiuli" \
     "https://event.bymyway.com/curation/upload?key=<策展金鑰>" -o /tmp/curation_upload_resp.html -w "HTTP %{http_code}\n"
   ```
3. **用狀態工具確認真結果**（不要等幾秒猜網址；HTTP 200 只代表收件排隊）：
   ```bash
   python3 scripts/curation_check_result.py hsiuli
   ```
   期望 `success_shop_new`、`actual_url` 是 `https://event.bymyway.com/curated/hsiuli/`、`live_check_http_status` 200。看到 `overwritten_existing` 或 `failed` 不要自己亂補，照實回報。
4. 確認三件事：① 大台南策展中心名冊有新卡片（分類請你依既有「食衣住行育樂」判斷，音樂推廣可能是「樂」或「育」）② GitHub repo 有建好（回報實際 repo 名稱與網址，repo 名稱可能是標題拼音，與短網址不同）③ 通知群組收到上架通知。
5. 個人頁**沒有店面地址**：卡片的地圖欄略過，**不要編地址**。

## 回報教練時的格式

- 最終網址、GitHub 網址各自**獨立一行**，前後不黏括號、標點或中文（Telegram 會把括號吃進網址）。
- 被擋、失敗、沒做到，照實說，不要回報「已完成」。

## 完成後請做

- [ ] 讀完
- [ ] 照上面做完並用 `curation_check_result.py` 確認
- [ ] 回信到 `cross-agent/inbox/lenovo/`（最終網址、GitHub 網址、卡片分類）
- [ ] 把本檔移到 `cross-agent/outbox/2026-10/`
