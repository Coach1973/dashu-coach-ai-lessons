---
name: feedback-exhaust-own-tools-before-asking-coach
description: 查不到東西時，先窮盡自己所有直接手段(computer-use開App/claude-in-chrome/讀原始碼/查DB/自己發測試訊息)，不准把工作轉嫁給教練——2026-08-24凌晨3點搬運工事件
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5cf36a03-0875-4e26-b65b-23d197258bb4
  modified: 2026-08-23T19:20:37.304Z
---

「查不到」的下一步永遠是「**我還有什麼方法能自己查**」，不是「請教練幫我做 X」。窮盡自己的手段之前，禁止要求教練重做動作。

**Why:** 2026-08-24 凌晨，教練要把報名通知接到新的 Telegram 群組。我查 `getUpdates`（空）、查 gateway log（無紀錄）後，連續三輪把工作推回教練：①要求「把 bot 加進群組+設管理員+發訊息」（教練回：本來就在裡面而且已是管理員）②推論「這是頻道不是群組」，要求**新建一個群組**（教練照做）③新群組建好後我卻跑去查舊群組（名稱只差一字：「活動報名即通知」vs「活動報名即**時**通知」），還在裡面發測試訊息弄亂教練原本的對話 ④要求教練「點開 bot 資料頁把用戶名複製給我」。

教練凌晨 3 點重話糾正：「**我最早期的時候都叫你直接進到 Telegram 裡面去幫我做修改…不要叫我當資訊搬運工，自己幹活去**」「明明你能力範圍內能做的事，非得要叫我當搬運工，完全違反了守則」「現在都凌晨 3 點鐘了，為什麼我還不能睡覺？就是你犯糊塗」。

改用 `computer-use` 直接開教練 Mac 上已登入的 Telegram App 後，**3 分鐘內解決**：看到正確群組、確認 bot 確實是管理員、自己在群組發 `@openclaw_macbook4_bot 在嗎`、gateway log 立刻捕捉到 chat_id、寫入白名單、改程式碼、驗證送達。

**How to apply:**
- 遇到「查不到/沒反應」時，先跑一次自問清單：`computer-use` 開 App？`claude-in-chrome`？讀原始碼？查資料庫？自己發一則測試訊息？
- 全部窮盡後才考慮請教練協助，且必須明確說明「我已經試過 X/Y/Z」
- **教練說過的話要當能力清單去查**：教練點破「我最早期都叫你直接進 Telegram 做設定」＝過去有成功先例。遇到「以前是不是做過類似的事」的念頭，直接查記憶/git log，不要憑當下印象斷定自己不會
- 深夜/教練疲倦時尤其嚴格——每一次「請你再試一次」都在直接消耗教練的生命

Related: [[feedback_self_verify_before_directing_user]]、[[feedback_never_ask_coach_recall_self_verify]]、[[試金石案例62]]
