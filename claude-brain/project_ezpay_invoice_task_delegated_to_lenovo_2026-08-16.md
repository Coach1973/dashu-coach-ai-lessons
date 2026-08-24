---
name: project-ezpay-invoice-task-delegated-to-lenovo
description: 【已作廢2026-08-24】2026-08-16曾裁示改聯想負責，但08-18起Mac桌面版持續大量開票(38人培訓費批次全數由Mac完成)，現況是Mac照常開票
metadata: 
  node_type: memory
  type: project
  originSessionId: 7d4244d1-db9c-42f8-97ad-dc02499cbe41
  modified: 2026-08-24T11:08:10.576Z
---

2026-08-16教練親口裁示：ezPay電子發票開立（inv.ezpay.com.tw，帳號gtbctainan，商店337391376 BNI台南南區）這項工作以後交給聯想電腦做，Mac空出來做別的事。

**Why（08-16原始決策，已作廢）：** 教練問「同樣的任務讓聯想電腦執行，也可以像你一樣的效果嗎」，確認技術上可行（claude-in-chrome擴充功能哪台機器都能裝），差別只在登入狀態per機器不共通，教練接受這個前提後直接裁示交接。

**🔴🔴 此裁示已被08-18的實際情況推翻，現況是Mac主責，不是聯想。** 聯想08-18實際接手操作18人份培訓費發票，前2張(張騰文/陳佳玲)有成功，**第3張(林宜宏)開始卡在ezPay網站原生確認彈窗、分頁反覆凍結**（CDP逾時45秒，事後查證那張根本沒送出）。教練評估卡住浪費的token成本後，裁示改到Mac試試看（交接記錄見`cross-agent/outbox/2026-08/20260818-1516_lenovo-to-mac_ezpay-training-invoice-17-handoff.md`）。此後Mac一路把那批+後續多批全部開完（08-17/08-19/08-23…），查詢與開立目前都是Mac在做，不是「開立歸Mac、查詢歸聯想」這種乾淨的任務型分工。

**How to apply：** 教練提到要開/查ezPay發票，**預設是Mac的工作**，聯想不用主動接手，除非教練明確重新指定。完整操作SOP在 [[reference_ezpay_invoice_issuing_procedure]]。

**教訓：** 這份記憶在08-18被實際情況推翻後，一直沒人回頭更新，直到教練08-24主動追問才發現——任何「工作歸屬」類記憶一旦被後續事件推翻，要立刻回頭更新該記憶檔，不能只留一筆新記錄了事，否則下次任何機器讀到舊記憶還是會誤判責任歸屬。
