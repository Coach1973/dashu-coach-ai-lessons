---
name: project-coolcase-xinfa-website
description: 「頂級特助的心法實踐」案例網站（cool-case.netlify.app）的站台資訊、部署流程、案例結構
metadata: 
  node_type: memory
  type: project
  originSessionId: 6d045433-c07e-4194-8146-7178d4ce8a81
---

「頂級特助的心法實踐」案例網站，2026-05-30 建立並上線。

**Why:** 教練要將 AI 助教的真實失敗與覺醒案例集結成網頁，供後續持續新增案例使用。

**How to apply:** 終端機蒸餾出新案例後，按相同 HTML 模板格式加入，編號從 #008 開始往後排。

---

## 站台資訊

- 正式版 Site ID：`d1817032-8b89-4ca2-98ed-1d4607533404`
- 正式版網址：https://cool-case.netlify.app
- Netlify Token：見 [[reference-netlify-token]]
- 本機最新版：`/tmp/final_v8.html`（重開機會消失，需從 Netlify 重拉）
- 桌面預覽：`~/Desktop/心法實踐_預覽.html`

## 部署鐵律

手動上傳型，必須帶 `_headers` 檔案（否則 Content-Type 會變成 text/plain，顯示原始碼）：

```bash
cp 最新版.html /tmp/index.html
printf "/*\n  Content-Type: text/html; charset=UTF-8\n" > /tmp/_headers
cd /tmp && zip -r deploy.zip index.html _headers
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/zip" \
  --data-binary "@/tmp/deploy.zip" \
  "https://api.netlify.com/api/v1/sites/d1817032-8b89-4ca2-98ed-1d4607533404/deploys"
```

## 🔴 Content-Type 血淚教訓

至少三次以上出現「推上去顯示 HTML 原始碼」的問題。根因是 Netlify 手動上傳型預設 Content-Type 為 text/plain。**必須在 zip 裡包含 `_headers` 檔案**，寫死 `Content-Type: text/html`。

## 當前案例結構（7 個，2026-05-30）

| 編號 | 標題 | 守則 |
|------|------|------|
| 01 | 鬧鐘響了，卻沒起床 | #09, #17, #03, #15 |
| 02 | 沒有經我同意，為何截圖？ | #03, #09 |
| 03 | 交接，不是一道選擇題 | #08, #06 |
| 04 | 你搞清楚你是誰好不好？ | #12, #10 |
| 05 | 第五條，原話是什麼？ | #21, #15 |
| 06 | 你老是忘，我不高興 | #05, #13 |
| 07 | 邏輯推就知道要做 | #08, #09 |

## 圖片壓縮（2026-05-30 教練親定）

原版 1,706 KB，壓縮後 58 KB（節省 96.6%）。做法：
1. 頭像從 500px 壓到 80px，JPEG quality 40
2. 用 JS 變數引用一次（DOMContentLoaded 填入），不重複內嵌 base64
3. 壓縮版已存在 `/tmp/cool-case/index.html`，作為後續加案例的底版

相關記憶：[[image-compression-by-scenario]]

## 案例 HTML 模板要素

每個案例必須包含：
1. **對話氣泡**（一來一往，至少 2 輪）——頭像由頂部 JS 變數統一填入，img src 用透明 1px GIF 佔位
2. **根因區塊**（橙色框，大字標題「根因」）
3. **悟區塊**（wu-badge 圖由 JS 統一填入）
4. **rule-chip 守則標籤**（字體 16px）

## 頁面功能

- 首頁 hero 下方：7 個圓形 icon 跳轉
- 右側浮動 Tab：▲ 回頂部 + 01-07 案例跳轉（JS 頁內滾動，不開新頁）
- DNA 區塊：只顯示「使命、願景、理念」三個橫排對齊

## 設計決策（教練親定）

- 名稱統一用「小龍蝦 AI 特助」，禁用「軍師」
- 案例 1（鬧鐘）和案例 2（截圖）排最前面——教練認為最精彩
- 版型參考 whimsical-smakager（暖色系），排版參考 vip-club
- 對話要有層次感，至少兩輪一來一往
- 精簡利索，不要形容詞和場景鋪墊（案例 3-7）

相關記憶：[[feedback-netlify-deploy-zip-api]]、[[reference-netlify-token]]
