---
name: browser-no-full-junction
description: 瀏覽器絕對不能整個 AppData 做 junction，只能搬書籤等增量資料檔
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a4314073-04dc-4cea-ae43-48543d5ca592
---

瀏覽器（Chrome、GanJing、Perplexity、Comet）絕對不能整個 AppData 資料夾做 junction 搬移。

**Why:** 教練從一開始就明確說過「像 LINE 一樣只搬增量資料」，聯想測試紀錄也寫了瀏覽器只做備份未啟用 junction。我沒聽，整個搬了，導致三個瀏覽器帳號全部遺失，教練要全部重新登入。同樣的錯犯了兩次。

**How to apply:**
- 絕對不對瀏覽器的整個 `AppData\Local\<瀏覽器>` 資料夾建 junction（裡面混了 Application 程式本體，搬了會炸）
- **可以**只 junction 裡面的 `User Data`（或同等的 profile 子資料夾）——這才是真正的「增量資料」，跟 LINE 只搬 Data/Cache、Zoom 只搬 data/logs/reports 是同一個邏輯，程式本體資料夾（Application、bin）永遠留在 C 碟
- 2026-06-25 Chrome 已用這個縮小範圍做法（`Local\Google\Chrome\User Data` → `Google-Chrome-UserData`）穩定運作至今，2026-07-02 比照做了 GanJing（`Local\GanJing\User Data` → `GanJing-Local`，程式本體其實在 `AppData\Roaming\Gan Jing Browser`，跟 User Data 完全分開，搬完免重裝免重登入）
- 搬移前務必先找到該瀏覽器「profile 資料夾」和「程式執行檔」實際分別放在哪裡，兩者混在同一層（像舊版整包搬法）才是真正的地雷，分層以後 junction 到 profile 那層是安全的
- 聯想信裡寫「備份已做，junction 未啟用」的軟體，是指還沒驗證安全範圍前的保守做法，驗證過範圍安全（比照 Chrome/GanJing）後可以啟用

Related: [[line-bin-stay-c-drive]]
