---
name: feedback-check-downstream-references-when-fixing-compat-2026-09-25
description: 修好一個相容性/格式問題時，只治了入口(status.md→status.html)，沒順手檢查同一頁面引用出去的其他資源(coach-persona.md/system-prompt.md)是不是同一個病，教練追問才抓到
metadata:
  node_type: memory
  type: feedback
  originSessionId: 88a8b6c3-e631-4390-8d89-3c37d65f917b
  modified: 2026-09-25T06:18:41.114Z
---

教練原話（2026-09-25）：「你的這個網址裡面有兩個你叫他們讀取的資料。這也是我想問你的：如果他們連上一個網址的 .md 檔案都讀不到，那我們又怎麼能奢望他們能透過這個網頁，讀取到這兩個 .md 的檔案呢？」

**背景**：查出 GitHub Pages 對 `.md` 回傳 `text/markdown`、多數 AI 讀網頁工具只認 `text/html` 這個真因後，只把 `status.md` 轉成 `status.html` 修好了，但 `status.html` 內文裡叫其他 AI 去讀的另外兩份文件（`coach-persona.md`、`system-prompt.md`）是完全一樣的檔案類型、完全一樣的病，卻沒有一起檢查。是教練自己想到、反問回來才抓到的，不是我自己查全的。

**Why**：找到根因、修好一個具體症狀後，很容易滿足於「這個問題解決了」，忘記同一個根因可能還連著其他還沒檢查過的地方——尤其是被修好的頁面本身「引用/連結」出去的其他資源，最容易被漏掉，因為它們不在當下盯著的那個檔案裡。

**How to apply**：
- 修好一個相容性/格式類問題（content-type、編碼、瀏覽器相容、API格式變更等）之後，多問自己一句：「這個根因還影響到哪些我沒直接動手的地方？」尤其是被修檔案本身「連結/引用/嵌入」出去的其他資源。
- 具體檢查法：`grep` 同類副檔名／同類格式在整個相關目錄或頁面裡還出現在哪，逐一確認是否受同一個根因影響，不要只看「教練specifically提到的那一個檔案」。
- 對應[[reference_github_pages_md_content_type_ai_compat_2026-09-25]]（這次的技術根因記錄）。
