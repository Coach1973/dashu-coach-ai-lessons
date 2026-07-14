---
name: project-peipei-art-redesign-2026-07-14
description: 佩佩老師個人品牌行銷頁改版進行中——測試站已上線，版面骨架完成等文字/照片，之後推正式peipei-event.netlify.app
metadata: 
  node_type: memory
  type: project
  updated: 2026-07-14
  originSessionId: 4c6a6979-8ca3-4896-a8bb-5e0a26b406b5
---

# 佩佩老師個人品牌頁改版（2026-07-14 開始）

## 背景與流程（教練親定三步驟）

教練要重新設計 `peipei-event.netlify.app`（目前顯示的是舊的、不相關的「4/11台中AI實戰論壇」內容），流程是：
1. 舊內容備份 → 已確認不用做，本來就已經躺在 `Coach1973/peipeievent-411`（archived repo，內容逐字比對相符）
2. 新版先在GitHub Pages測試 → 已建立 `Coach1973/peipei-art` repo + GitHub Pages，測試網址：**https://coach1973.github.io/peipei-art/**
3. 教練確認滿意後 → 才推正式 `https://peipei-event.netlify.app/`（用Netlify API zip部署，記得用自製的forward-slash zip工具，不要用PowerShell Compress-Archive，會產生反斜線路徑導致Netlify上子資料夾404，見bigtree案例血淚教訓）

## 命名注意

`peipei-event` 這個名字已經被佔用（`Coach1973/peipei-event` 私有repo，是Mac做的活動報到系統後端Flask程式，跟這次行銷頁完全無關），所以新站改名 `peipei-art`，教練已確認這個名字。

## 已完成：版面骨架（commit `de91ae3`）

色系**完全沿用**peipei-event.netlify.app現有的紫色系（CSS變數已直接複製）：
```
--bg:#f8f0f7  --accent:#9872a4  --accent-2:#c2709b  --gold:#b88ab8  --text:#2c1f2e
```
字體同樣是 Noto Sans TC。

版面參考教練bymyway.com個人頁的邏輯，規劃了以下區塊（全部是**佔位內容**，文字用『【...待補】』標記，照片用虛線框占位）：

1. **Hero主視覺**：招牌文案（教練提兩個選項待定：「感性的背後是理性」／「音樂就是邏輯」）、25年音樂資歷+2000場演出數據卡
2. **創業的過程與創辦理念**（story區塊，圖文並排）
3. **媒體報導**（media區塊，3欄卡片）
4. **常見問答 Q&A**（qa區塊）
5. **最近活動**（events區塊，3欄卡片，未來可考慮串接peipei-event報到系統）

教練明確說**除了線上課程，其他都可以放**。

## 下一步（教練說會陸續提供文字）

1. 等教練提供各區塊實際文字內容，逐一填入佔位處
2. 教練還沒決定用哪句招牌文案，兩個選項都先放在hero，等教練拍板
3. 照片：教練說會陸續給，目前都是虛線占位框
4. 版面本身（欄位配置、卡片數量）教練還沒給回饋，可能還會調整
5. 全部確認後，才問教練要不要推正式 `peipei-event.netlify.app`（照SOP要教練親口說「推」才動）

## 關鍵檔案

- repo: `E:\Claude-Data\github_repos\peipei-art\index.html`（本機clone）
- 線上測試：https://coach1973.github.io/peipei-art/
- 參考站色碼來源：https://peipei-event.netlify.app/（現存內容其實是`peipeievent-411`舊案，跟佩佩老師無關，等這次改版完成會被取代）
