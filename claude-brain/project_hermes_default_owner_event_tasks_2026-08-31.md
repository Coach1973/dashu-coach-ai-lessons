---
name: project-hermes-default-owner-event-tasks-2026-08-31
description: 教練拍板大樹小講/近期活動網站內容維運類任務預設交Hermes負責，BNI Connect等需JS操作的第三方後台仍歸軍師
metadata: 
  node_type: memory
  type: project
  originSessionId: 6febc53c-7b34-441c-83bf-76715b21a20f
  modified: 2026-08-31T07:32:33.897Z
---

教練 2026-08-31 15:26 親口拍板：往後只要是跟「大樹小講」以及近期辦活動這一類的任務，盡可能丟給 Hermes（同一台 Mac 上的獨立桌面 AI 代理，見 [[project_hermes_desktop_agent_verified_2026-08-31]]）運作，並要求兩邊透過既有系統通訊（`cross-agent/inbox`/`outbox`），Hermes 卡住時軍師立刻給指導，直到 Hermes 能完全接手網站活動建置任務。

**Why**：8/31 當天已經走完一輪完整教學迴圈——軍師寫 SOP → Hermes 試做 → 回信問卡點 → 軍師答覆 → Hermes 再試 → 遇到工具集結構性限制（desktop preview pane 沒有 js evaluate/fill_input/screenshot，無法程式化操作原生 `<select>`）才投降，最終裁示 BNI Connect 後台任務轉軍師（詳見 [[project_hermes_bni_connect_task_routing_2026-08-31]]）。教練看完這個迴圈真的能運作，決定把它從「這週三額度用完前的備援」升級成常態預設分工，不用每次重新交辦。

**How to apply**：
- 大樹小講／ai-talk／ai-forum-taichung／tainan-calender 這幾個網站的**內容維運**（改場次時間地點費用、改文案版面、查報名人數、event.db 操作、接力棒、SOP、蒸餾）→ 預設 Hermes，操作手冊在 `knowledges/2026-08-31_大樹小講四場活動維運SOP_備援指令給Hermes.md`
- BNI Connect 等第三方官方後台，需要 js/程式化 select/截圖的任務 → 仍歸軍師
- 涉及 Netlify 正式站部署（扣額度）的動作，不論誰執行，都要教練親口說「推」才能做——換執行者不代表放寬這條鐵律
- Hermes 卡住時走 `cross-agent/inbox/mac/` 寫信，軍師開工讀到後除了回信，**要同步把答案補進對應 SOP 文件**，這才是「教到完全能接手」的實際機制——SOP 越補越完整，Hermes 卡住頻率會隨時間下降
- 政策已寫入 `cross-agent/README.md`「任務分工鐵律」章節（永久協議，不只是這則記憶）+ `projects/cards/bigtree.md`/`ai-talk.md`/`ai-forum-taichung.md`/`tainan-calender.md`（owner:Hermes）+ `projects/cards/bni-connect.md`（owner:軍師）
- 若未來 Hermes 工具集升級（例如教練幫忙裝 Browser Use 雲端瀏覽器），BNI Connect 這類任務的分工可重新評估，不是永久鎖死
