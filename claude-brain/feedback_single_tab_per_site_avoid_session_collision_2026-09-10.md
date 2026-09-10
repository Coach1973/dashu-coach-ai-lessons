---
name: feedback-single-tab-per-site-avoid-session-collision-2026-09-10
description: 用claude-in-chrome操作同一個需要登入的網站(ezPay)時，同時開多個分頁會互搶session，導致教練反覆被踢出登入畫面——一律只用一個分頁，不要因重試/加速而開新分頁
metadata:
  type: feedback
---

開ezPay培訓費發票時，因為連線逾時/CDP timeout而多次用`tabs_create_mcp`開新分頁重試，加上一度誤判裝置連線問題又切換瀏覽器，最終同時有3~4個分頁都連著ezPay。教練說「已經登了8次了」，動怒質問「怎麼回事」——查證後才發現：不是ezPay不穩，是自己開的多個分頁互相搶同一個帳號的session，每次新分頁的活動都可能讓其他分頁的登入狀態失效，教練越重新登入越被自己(AI)的其他分頁踢出去。

**修法**：關掉所有多餘分頁，只留一個，教練最後一次登入立刻穩定，之後全程只用這一個分頁操作，即使該分頁偶爾CDP timeout，也是`navigate`回同一個分頁重試，不再新開分頁。

**How to apply**：往後用claude-in-chrome操作任何「需要登入狀態」的網站（ezPay、BNI Connect、後台系統等），全程只用一個分頁，不要因為想加速、想重試、或懷疑連線裝置不對就開新分頁——開新分頁前先確認舊分頁真的用不了(如`tabs_context_mcp`看不到)，而不是預防性地多開一個備用。連線逾時時的正確處理是對同一個tabId重新`navigate`，不是換分頁。

Related: [[reference_bni_training_invoice_registration_workflow_2026-09-10]]（工作流SOP裡已記錄這條規則）
