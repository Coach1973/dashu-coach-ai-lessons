---
name: feedback-system-notices-go-to-inbox-not-coach
description: 教練看不懂小龍蝦的技術通知，要求系統自己的通知不傳他、由軍師開工時自己處理；回報一律先講「你什麼都不用做」
metadata:
  type: feedback
---

教練 2026-11-01 原話：小龍蝦沒事不要講一大堆他看不懂的東西；開工或對話時軍師自己去巡視小龍蝦說了什麼、自動解決，不要來吵他。要我下次明確說：「教練，你什麼都不用做，這些我都來處理。」

**Why:** 技術通知（HTTP 404、P0、WAL…）對他是困擾，報了他也不能做什麼。我 11/01 解釋晨報時一開始沒先講結論，被罵「說得不清不楚」。

**How to apply:**
- 回覆教練第一句先講他要不要做事；沒事就寫「教練，你什麼都不用做，這些我都來處理。」
- 系統自我監控類通知已改進 `workspace/state/junshi_inbox.jsonl`（`scripts/notify_coach.sh` 依呼叫者判斷，名單 SYSTEM_CALLERS；要硬送加 NOTIFY_FORCE_COACH=1）。開工 hook 第 5.8 步會列出，我自己查、自己修，修完跑 `python3 scripts/junshi_inbox.py done`。
- 幕僚長晨報 cron（id 0d64be3c）已改成不傳教練、有事才寫進待處理匣。
- 放超過 48 小時沒處理，才會用一句白話提醒教練一次。
- 還沒處理的兩件（開機檔過長、Mac 備份 3 天沒跑）已放進待處理匣。
Related: [[feedback-rules-fewer-is-wiser]]
