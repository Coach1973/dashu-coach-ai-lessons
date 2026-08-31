---
name: project-hermes-bni-connect-task-routing-2026-08-31
description: BNI Connect等需要JS/程式化select/截圖的網頁後台操作任務不交給Hermes，改交軍師；Hermes專做讀寫類任務
metadata: 
  node_type: memory
  type: project
  originSessionId: d418529b-adbf-434c-886c-6ef93e708a64
  modified: 2026-08-31T07:13:20.158Z
---

Hermes（MiniMax-M3桌面版，用desktop preview pane操作瀏覽器）嘗試建BNI Connect「9/21新領導團隊訓練」活動時卡住，寫了完整投降書分析根因：desktop preview pane工具集沒有JS執行(js evaluate)、沒有程式化設定原生`<select>`值的能力、沒有截圖功能，這三項是均仕（軍師這邊用Browser Use/claude-in-chrome）本來就有的能力，差距是**結構性工具限制**不是模型能力問題。教練當場說「均仕一次就到位，Hermes太多麻煩，以後這類任務不交給Hermes」。

軍師裁示採Hermes自己提出的「方案D」：BNI Connect這類需要操作原生網頁表單（尤其是select下拉選單程式化選值）的後台任務，一律轉給軍師處理；Hermes繼續專注讀寫類任務（改event.db/改文案/查報名/接力棒更新/寫SOP/蒸餾），不需要為此給Hermes裝雲端瀏覽器工具鏈——這類任務頻率低（一季幾次），投資新工具鏈的ROI不划算。

**Why**：教練明確表態偏好均仕處理這類任務，且Hermes自己的能力落差分析扎實可信，不是隨便放棄；避免過度工程化去解決低頻任務。

**How to apply**：往後教練或Hermes提到要在BNI Connect（或其他需要操作原生select/需要JS/需要截圖驗證的網頁後台）建活動、改資料等任務，直接由軍師接手，不用讓Hermes重新嘗試一輪才發現做不到。若教練之後改變心意要投資雲端瀏覽器給Hermes，那是全新決策，這份記憶只反映2026-08-31當下的分工裁示。

相關案例：這場BNI Connect大台南南區培訓活動建置任務本身，見同日建立的7場活動（初階MSP×2/進階MSP×2/主題培訓×2/領導團隊期中訓×1）+ 教練手動建立的9/21領導團隊培訓(eventId 533117)。
