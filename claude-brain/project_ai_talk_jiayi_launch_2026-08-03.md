---
name: project-ai-talk-jiayi-launch-2026-08-03
description: AI微型論壇嘉義場(ai-talk repo)網站build完成，台南場改為northern-tw式完整封存，等講師確認後才推Netlify
metadata: 
  node_type: memory
  type: project
  originSessionId: 9911d787-45a4-4790-8678-ef746e2505a6
  modified: 2026-08-03T16:24:21.127Z
---

`github_repos/ai-talk` 這個單頁網站（原本是台南場7/29的報名頁，活動結束後轉成回顧頁）已改版成以嘉義場（2026年8月28日週五14:00-17:00，再耕園404演講廳，嘉義市西區玉康路160號）為主場，台南場完整保留成「歷屆回顧」封存區塊。

**嘉義場內容：** 5大主題議程（季哥Eric Chi/洪詠清/林韋銘/吳大樹4位講師+1個中小微企業補助神秘嘉賓）、講師卡片點擊彈窗顯示完整簡介（比照教練另一個專案 mentor100「AI百人導師」的 `openBio()` 互動模式）、報名費100元（園遊券制，可在現場攤位全額折抵消費）、報名人數上限100席、以2026-08-03為基準每天+3人動態計算、報名表單新增「公司統一編號」選填欄位、現場設攤方案2000元含專屬桌+加碼1000元園遊券（100元x10張）。

**台南場歷屆回顧：** 教練指定參考 northern-tw.netlify.app 的真實結構（完整保留每場當天版面，不是精簡摘要），所有id加`tn-`前綴避免與嘉義場現役id衝突，內容忠實保留7/29當天原文（含王彤/蘇秦/燒茶/大樹教練4位講師、9家設攤廠商、13位贊助人、當天FAQ）。

**部署狀態：** 已推GitHub（`Coach1973/ai-talk`），GitHub Pages預覽網址 `https://coach1973.github.io/ai-talk/` 會自動跟main分支同步。教練刻意分兩階段——先讓講師透過GitHub Pages確認內容無誤，**確認沒問題後才會請軍師推Netlify**（正式站`ai-talk-tw.netlify.app`目前仍是台南場舊版）。

**Why:** 教練的固定操作模式——重要對外內容先給關係人（這次是講師）預覽確認，避免定稿後才發現內容有誤，Netlify部署又要消耗credit（[[project_netlify_deploy_quota_2026-07]]）。

**How to apply:** 若教練後續說「講師確認了，推Netlify」，直接走既有Netlify zip+API部署SOP（[[feedback_netlify_headers_content_type]]），不用重新確認內容細節。若教練提到「嘉義場」相關任何調整，直接改`github_repos/ai-talk/index.html`裡對應區塊（id="agenda"/"speakers"/"sponsor"/"faq"/"signup"是現役嘉義場，id前綴`tn-`的是台南場封存區塊，兩者互不影響）。

Related: [[feedback_verify_reference_url_before_building]]（本場的方法論教訓）
