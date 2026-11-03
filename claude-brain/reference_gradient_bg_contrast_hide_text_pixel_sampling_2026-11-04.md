---
name: reference-gradient-bg-contrast-hide-text-pixel-sampling-2026-11-04
description: 字壓在漸層或光暈背景上時，page_contrast_scan.js 讀不出真實底色（只讀祖先 background-color）；改用「字設透明→截圖→取字框下方像素算對比」，rebreathe Chapter 06 實例
metadata:
  type: reference
---

page_contrast_scan.js 只往上找祖先的 background-color，遇到 linear-gradient／radial-gradient／疊圖時讀不到真實底色，會漏報（rebreathe `.sunrise` 掃描沒報、實際對比 1.0～1.6）。

做法：用 playwright 開頁，注入 `color:transparent!important;text-shadow:none!important` 把字藏起來，捲到該區塊截圖，取每個文字框範圍內像素，對字色算 WCAG 對比取最小值。改完用同法對線上版再量一次（rebreathe 修後最低 4.74）。

修法選擇：字跨過整段漸層時單一字色解不了（標題框同時蓋到深紫與亮桃），改在文字容器後面加 `::before` 深色徑向暗幕（z-index:-1，容器自己有 z-index 形成堆疊層），不動原配色。rebreathe 51e9161。

**How to apply:** 教練說「字跟背景太接近」且該區是漸層／光暈／疊圖時，先用此法量，不要只跑 page_contrast_scan.js。
