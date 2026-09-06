---
name: reference-owner-username-hardcoded-separate-from-db
description: 改帳號登入名稱時，要搜尋程式碼裡有沒有獨立寫死的owner/admin常數跟資料庫分開維護，否則登入成功但功能被擋
metadata: 
  node_type: memory
  type: reference
  originSessionId: adb89531-8a13-4899-b053-2fd921d969f6
  modified: 2026-09-06T00:00:30.078Z
---

`namecard-db/app.py`第69行有一個獨立的`OWNER_USERNAME = "bymyway"`常數，跟`team_members`資料庫表完全分開維護，專門用來判斷「誰是教練本人」(`owner_only_required`裝飾器)。2026-09-06把教練的登入帳號從`bymyway`改成手機號碼`0901056777`時，只改了資料庫，沒注意到這個寫死的常數——結果教練登入成功(session驗證通過)，但一進`/bni-credit`、`/invoice-admin`這類「僅限本人」頁面就被擋下顯示「此頁面僅限教練本人查看」，因為`session.get("team_username") != OWNER_USERNAME`比對失敗。

**Why**：這種「登入資料庫」跟「權限判斷常數」分開兩處維護的設計，在教練要求「換掉某個帳號的登入名稱」這類需求裡是常見地雷——改帳密直覺只會想到改資料庫/`.env`，很少會想到程式碼裡可能還有一個寫死字串在做額外比對。

**How to apply**：任何時候要修改一個系統的登入帳號(不限使用者名稱，含owner/admin判斷邏輯)，動手前先`grep`整個repo找有沒有這個舊帳號名稱的字面字串出現在別的地方(不只是資料庫/`.env`)，改完後不能只測試「登入成功」，要測試「登入後能不能真的用到原本該有的權限」(完整流程：登入→帶cookie訪問受保護頁面→確認內容正確，不是只看302跳轉)。
