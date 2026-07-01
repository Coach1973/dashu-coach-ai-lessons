---
name: project-vps-client-isolation-fix-2026-07-01
description: VPS小龍蝦(43.245.60.200)9位新用戶記憶隔離漏洞修復——client-memory hook原本把教練內部資訊+其他用戶隱私整份注入給每個人
metadata: 
  node_type: memory
  type: project
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-01，ACER 開通 VPS 小龍蝦（`@coach_bymyway_bot`，43.245.60.200）9 個新帳號（8 位外部體驗用戶 + 教練本人），教練要求驗證這些對話「是否獨立、可以長期被記憶」。

**發現的真實漏洞**：`hooks/client-memory/handler.js` 原本無條件把 `workspace/CLIENT_PROFILE.md` 整份內容注入每一個對話者的 system prompt，而這份檔案裡混著：① 不同外部客戶各自的隱私資料（CHIU YuJung、Esther 的姓名/背景/偏好）② 教練自己的內部系統架構（海餅乾俱樂部、學長/學弟/學妹三機分工、內部工程鐵律）。也就是說，任何一個外部體驗用戶跟小龍蝦講話，理論上都會被灌入教練的內部業務資訊和其他客戶的隱私。

**Why**：這是要規模化服務多位外部用戶前的關鍵前提——沒有這層隔離，教練沒辦法安全地開放更多體驗名額，一旦被任何用戶問出來（"你剛剛是不是提到另一個叫 Esther 的人？"）會是嚴重的信任事故。

**修復方式**：
1. 統一成「每位外部用戶一個獨立檔案」`workspace/clients/{telegram_id}.md`（Lin Yu Ju 原本就有這個慣例，只是命名用姓名拼音不是 ID，已改成 ID 命名以利程式比對）
2. `CLIENT_PROFILE.md` 收斂成「僅教練本人專用」，拿掉其他客戶的區塊
3. `handler.js` 改成依 `event.sessionKey`（格式 `agent:main:telegram:direct:{id}`）判斷發話者：教練 ID（6124913915）→ 注入 `CLIENT_PROFILE.md`；其他人 → 只找 `clients/{自己的id}.md`，找不到就不注入（fail-closed，寧可什麼都不給也不能給錯人）
4. 部署後用 node 直接模擬 4 種身份（教練/CHIU/Esther/無檔案新用戶）呼叫 handler 驗證：各自只拿到自己的資料，互不外洩——不是「檔案存在就當作修好」，是真的餵假事件跑過一次（呼應案例 29 的教訓）

**How to apply**：以後任何新開通的 VPS 小龍蝦帳號，其個人化資訊一律寫入 `workspace/clients/{telegram_id}.md`，不可以再寫進共用檔案。若之後要開放更多體驗用戶（教練提到的「12 個」目標與現有 9 個有落差，可能含 Mac 端學長/學弟/學妹），同樣的隔離模式要套用到每一台新機器。

Related: [[reference_vps_connection]], [[feedback_truth_over_reassurance_backup_nuance]]
