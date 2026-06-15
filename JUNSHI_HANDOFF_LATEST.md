# 軍師接力棒 · 2026-06-15 v21（Opus 4.6 終端機 session）

> 建立時間：2026-06-15 上午 8:06 台灣時間
> 本棒執行者：Opus 4.6
> 上一棒：v20 超限戰復原＋個人品牌網站改版

---

## 🎯 本場成果

### bymyway.com/coach/ 個人品牌網站 iframe 嵌入修復

教練反映三大問題，全部修復完成：

1. **Hero 區塊大片空白**（commit fa0e86c）
   - 原因：`min-height: 100vh` 在 iframe 裡撐到 4500px
   - 修法：改成 `min(100vh, 800px)`

2. **學員見證排版跑掉**（commit fa0e86c）
   - 原因：`IntersectionObserver` fade 動畫在 iframe 不觸發，卡片全部 opacity:0
   - 修法：偵測 iframe 環境直接顯示，跳過 fade 動畫

3. **LINE 按鈕不出現 + anchor 連結失效**（commit fa0e86c → 863e620）
   - 原因：`position: fixed` 在大型 iframe 裡固定在 iframe 頂部而非螢幕
   - 修法：改 iframe 為 `height:100vh`（自帶滾動），fixed 定位正確運作

4. **導覽列不固定**（commit 863e620 + WordPress API 更新）
   - 原因：iframe min-height:4500px 時 fixed navbar 跟著 iframe 頂部跑
   - 修法：iframe 改 `height:100vh`，navbar fixed 正確固定在可見區域頂部
   - 教練確認：所有導覽項目點擊後表頭都固定不動 ✅

### WordPress 頁面更新
- 頁面 ID：27374（slug: coach）
- iframe style：`width:100%;height:100vh;border:none;display:block;`
- 快取破除：`?v=20260615c`

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| 🔴 | bymyway 網站繼續改版 | 教練看完後根據回饋調整 |
| 🟡 | 客戶見證區塊 | 教練說他有不少客戶見證，要找出來後再做 |
| 🟡 | H 的 gh auth 修復 | H 無法 push |
| 🟡 | jiesheng-leadership 金流就緒時 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| fa0e86c | iframe 嵌入三大修復（hero/fade/anchor） | bymyway-website |
| 863e620 | LINE 浮動按鈕改回 fixed（配合 100vh iframe） | bymyway-website |

---

## 📌 重要路徑

- bymyway 網站 repo：`/Users/bymyway/github_repos/bymyway-website/`
- 線上版：https://coach1973.github.io/bymyway-website/
- bymyway.com 嵌入頁：https://www.bymyway.com/coach/（WordPress 頁面 ID 27374）
- 自動站 SOP：`~/.openclaw/workspace/knowledges/SOP_bymyway_auto_site.md`
- 網頁推 SOP：`~/.openclaw/workspace/knowledges/SOP_netlify_website_edit.md`

---

## ⚠️ 本場教訓

1. **iframe 內 `100vh` 會撐滿整個 iframe 高度**——用 `min(100vh, 800px)` 封頂
2. **iframe 內 `IntersectionObserver` 不可靠**——偵測 iframe 環境跳過 fade 動畫
3. **iframe 內 `position: fixed` 要搭配 `height:100vh` iframe 才正確**——大型 iframe（4500px）的 fixed 等於 absolute
4. **改 iframe style 要同步更新 WordPress 頁面**——用 bymyway-bridge wp_client.py REST API
