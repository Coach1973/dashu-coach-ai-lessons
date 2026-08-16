---
name: project-jarvis-plan-2026-08-16
description: 賈維斯計畫（教練用鋼鐵人比喻拋出的三合一總管家構想）通盤規劃報告+全四階段已同場落地完成
metadata: 
  node_type: memory
  type: project
  originSessionId: 16cac4d5-bb2d-43bb-a4de-1097183fbf09
  modified: 2026-08-16T12:23:30.050Z
---

2026-08-16教練用Fable 5拋出「賈維斯計畫」：希望軍師像鋼鐵人的賈維斯一樣，開口就懂，不用每次交代背景。通盤規劃報告存於`~/.openclaw/workspace/knowledges/2026-08-16_賈維斯計畫_三合一智能管家系統通盤規劃.md`（commit`5fd6bf8e0`），核心診斷：知識過去是「按時間存」（接力棒/memory都是日記），教練要的是「按主題存」（病歷）。

教練說「做」後，同一場session內完整落地四階段：

1. **Phase 1 專案卡+自動接線員**：`projects/cards/`11張核心專案病歷（大樹小講/AI微論壇嘉義+台中/mentor100/event-signup/bni-chapters/BNI Connect/結繩領導學/tainan-calender/LINE三帳號/VPS），`projects/INDEX.md`別名路由表，`scripts/project_card_router.sh`做UserPromptSubmit hook自動接線員。commit`70fa68ef7`。**已在真實對話中驗證觸發成功**（教練提「大樹小講」「臺中論壇」「百人導師」「簽到系統」時卡片皆正確自動注入）。

2. **Phase 2 Token每月自動體檢**：`scripts/monthly_token_healthcheck.sh`驗證9項憑證，openclaw cron`5d7acd65`每月1日09:20跑，全綠靜默、壞了才通知。commit`cacef61f5`。

3. **Phase 3 待辦到期提醒**：`scripts/todo_staleness_check.py`+`.sh`掛進`morning_digest.sh`，卡住≥7天或3天內到期日期會浮出06:00晨報。commit`83adc0381`。

4. **Phase 4 小龍蝦背景研究派工**：`knowledges/SOP_小龍蝦背景研究派工.md`+首航驗證（派工找5個BNI參考網站，真實產出`knowledges/研究_BNI分會參考網站_2026-08-16.md`）。commit`289b83c17`。

**Why**：教練26年培訓經驗中反覆感受到「每次都要精確交代指令」的疲勞，賈維斯是他心中理想協作模式的具象化比喻——見[[feedback_jarvis_outcome_delegation_style]]記錄的深層溝通偏好。

**How to apply**：往後任何「怎麼讓AI更懂教練」類需求，先檢查這四個機制有沒有涵蓋，不要重新發明；新增專案時記得同步在`projects/cards/`建卡+`projects/INDEX.md`加路由，否則自動接線員不會生效。

Related: [[feedback_jarvis_outcome_delegation_style]]
