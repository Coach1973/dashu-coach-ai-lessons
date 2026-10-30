---
name: nmda-home-opening-animation-integration
description: NMDA 官網首頁換成開場動畫包的做法與踩坑（站內全域 CSS 蓋到動畫、第一屏要扣固定標頭、導覽擠成多行、影片跳播要 Range、倒數 10/31 後自動移除）
metadata:
  node_type: memory
  type: reference
  originSessionId: 862b2c28-55c0-4581-a7d4-9c8acde85681
  modified: 2026-10-30T09:06:34.869Z
---

2026-10-30 把教練給的 `nmda-hero-opening.zip`（index.html 內以註解分 CSS／HTML／JS 三段，樣式都加 `nh-` 開頭）套進 nmda 首頁（nmda `c6a0da8`、`abcf2fb`）。

**做法**：三段逐字從壓縮檔抽出再用整合 CSS 覆寫；資源放 `assets/logo.png`、`assets/video/`；先在暫存區組好、本機量過才複製進 `~/github_repos/nmda`（改了就是上線）。

**踩坑**：
- 站內原有全域規則會蓋到動畫：`section{padding:110px 0}`、`nav{min-height:72px;display:flex}`、`h1{max-width:10ch}` → 用 `.nh{padding:0}`、`.nh-chap{min-height:0}`、`.nh h1{max-width:none}` 覆寫。
- 動畫第一屏高度要扣固定標頭高度（`calc(100svh - 85px)`），不是 `--nh-top`（那個給「浮在上面」的導覽列）。
- 標頭加 logo＋名稱放大後，900～960 寬導覽會把名稱擠成很多行：1100 以下縮 gap、940 以下只留「立即加入」。
- 影片要主機支援 Range 才能跳播：Python 內建 `http.server` 不支援，播完 `currentTime` 會回 0；本機測試改用自寫 Range 伺服器（正式站 206 已驗）。
- 內建瀏覽器窗格隱藏時 `requestAnimationFrame` 被暫停，章節字／時間碼不會動，不代表壞；只能以 `ended` 事件、影片取樣亮度驗證。
- 倒數計時：10/31 13:30 起顯示「大會進行中」、21:30 後整條資訊列 `remove()`；用假 `Date` 類別覆寫可測這兩種狀態。

**教練語意**：他給的包內註解就是施工說明；「10/31 過後變歷史紀錄」＝首頁不留過期倒數；導覽「立即加入」要導向會員方案（`#vip`）而不是聯絡區。

相關：[[project-nmda-members-page-and-staff-login-2026-10-30]]
