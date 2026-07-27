---
name: project-jiesheng-report-launch-2026-07-26
description: 結繩領導學工作坊即時戰報系統(jiesheng-report)正式上線於rpl-workshop.bymyway.com，完整功能清單與帳密
metadata: 
  node_type: memory
  type: project
  originSessionId: fd094a96-8867-4bdc-a472-49dd84f00d25
  modified: 2026-07-26T10:06:01.149Z
---

結繩領導學工作坊（台南/台中/台北）報名+繳費戰報系統，2026-07-26由聯想機寫程式碼、Mac部署上線。

**Why**：教練要工作人員能即時看到三場工作坊誰報名、誰繳費，比照mentor100模式純手動輸入，不接LINE/Google表單。

**How to apply**：
- 網址：`https://rpl-workshop.bymyway.com/admin`，帳號 **RPL**（大寫，區分大小寫），密碼是公司統一編號（AI全程未經手真實密碼）
- 部署：Mac本機`/Users/bymyway/.openclaw/workspace/jiesheng-report/`，LaunchAgent `com.coach.jiesheng-webapp.plist` 常駐於port 5063，Cloudflare Tunnel（`openclaw-macmini`同一顆）加Route
- 功能：開課倒數(台南8/19、台中9/23、台北11/25)、目標達成率進度條(25/20/50人)、邀請人下拉(曜董/大樹/佩君/Lavi固定四選一)、資料提交人欄(同帳號共用登入，用這欄記錄實際操作人，同樣固定四選一)、姓名可直接編輯（改錯字不用另開編輯按鈕）、依報名日期排序(舊到新，序號#對應報名先後)、**整頁一次「全部儲存」**（改完所有欄位按一次鈕，不用每格分開按存，刪除維持各自獨立按鈕）
- 歷史資料：15筆已於本場手動匯入（台南4/台中1/台北10，其中2筆"追款中"未繳費），教練後續已自行登入新增/修改過資料，證實系統正常運作

**踩過的坑**：`.env`密碼雜湊值含`$`符號，被LaunchAgent的`bash -c "source .env"`當成shell變數吃掉一截，導致密碼永遠登不進去——**任何`.env`檔案裡有`$`字元的值都要用單引號包住**，這條試金石早有記錄但這次是真的踩到才發現新專案沒套用。

**下一步（若教練提及）**：把「邀請人/資料提交人四選一」的名單、目標人數等寫死在程式碼裡的參數，若教練要調整（增減人選/改目標數）需要改`db.py`的`REFERRERS`常數跟`app.py`的`WORKSHOP_TARGETS`字典。
