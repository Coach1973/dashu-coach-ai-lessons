---
name: feedback-claude-in-chrome-wrong-device
description: claude-in-chrome連線的是目前配對成功的瀏覽器，不是這段對話跑在哪台電腦——跨機任務前必須先確認裝置
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7ed2146b-db6f-4aab-9f0f-32b45b9ab8c0
  modified: 2026-08-17T21:01:46.839Z
---

`claude-in-chrome` MCP連線的是「目前配對成功的瀏覽器」，不是「這段Claude Code對話目前跑在哪台電腦」。2026-08-18教練指派在Mac測試BNI Connect頁面（比對Windows碰到的503問題），我直接呼叫`navigate`並回報「Mac測試成功」，教練當場糾正：「你在Mac電腦上面要物理隔離，你現在跑開到我的Windows電腦去了」。查`list_connected_browsers`才發現當下只有一台Windows裝置連線(`isLocal:false`)，Mac的Chrome根本沒開過、沒配對過。

**Why**：教練用RustDesk遠端從Windows操作Mac時，物理上人坐在Windows電腦前，瀏覽器擴充功能配對的是慣用的Windows Edge，不是Mac的Chrome。頁面渲染正常只證明claude-in-chrome連線本身是通的，完全不能證明連的是哪一台裝置。詳見試金石案例60。

**How to apply**：任何「跨機比較」「這台機器操作是否正常」類任務，動手前先跑`list_connected_browsers`，確認回傳的裝置`isLocal:true`且名稱/deviceId是預期那台。若目標機器的Chrome沒開，先`open -a "Google Chrome"`啟動，讓擴充功能主動連線，再用`select_browser`指定正確deviceId。BNI Connect等網站的登入狀態是per機器獨立的，切到正確裝置後還需要教練親自在該Chrome重新登入（帳密不可代打）。
