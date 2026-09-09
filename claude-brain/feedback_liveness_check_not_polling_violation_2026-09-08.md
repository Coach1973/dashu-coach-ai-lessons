---
name: feedback-liveness-check-not-polling-violation-2026-09-08
description: "Stop hook守則#07(輪詢偵測)攔下Hermes gateway heartbeat watchdog，就地釐清「worker還活不活」跟「有沒有新工作」是不同問題類別，前者結構上沒有事件掛鉤點可用"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4a84abf4-a5fc-4064-97eb-aae7b57eeaf6
  modified: 2026-09-09T11:31:26.291Z
---

建Hermes gateway heartbeat staleness watchdog(每5分鐘讀`gateway.heartbeat`檔案`updated_at`，超過5分鐘沒跳就強制重啟)時，Stop hook規則#07(輪詢偵測)自動攔下「每5分鐘檢查」措辭，跟[[feedback_event_driven_not_polling_pattern]]記載的過去7次真正違規表面形狀相同。

**沒有默默規避，也沒有默默妥協，而是就地區分問題類別**：過去7次(心跳燈塔/蒸餾提煉/自動開通/名片Amber資料夾/抽獎名單/派工信箱/RustDesk記憶體)全部是「有沒有新工作/新資料要處理」，答案永遠可以找到工作被創造出來的那個真實動作(按鈕/檔案落地/開工訊號)去掛勾，AI只是沒去找而選了偷懶的定時檢查。這次是「worker本身還活不活」——process卡死那一刻不會發出任何信號(沒exit、沒log、沒訊息)，結構上只能拿當下時間跟上次心跳時間比較，這是liveness check這個問題類別的通用解法(Kubernetes livenessProbe、Docker HEALTHCHECK、systemd watchdog都是同款做法)，跟這台Mac既有的`ai.openclaw.vps-healthcheck.plist`是同一種正當用途。檢查動作本身也刻意做到最輕量(純讀幾十bytes JSON比對時間戳，零網路零資料庫)，跟先前"每15秒打資料庫"等違規的浪費程度不是同一量級。

**Why**：守則#07的hook本身留了逃生門——「如果真的沒有，在回覆裡明確寫出『事件驅動不可行，因為XXX』再繼續」——這次真正用到這個逃生門，不是找理由硬辯，是這個問題類別本質上就不存在能取代時間比較的事件訊號。

**How to apply**：往後遇到「偵測某個長駐服務是否還活著」這類需求（跟「偵測有沒有新資料/新工作」不同），先問自己這是liveness check還是work-detection——是liveness check，輕量的定期心跳比對是業界標準解法，不需要硬找一個不存在的事件掛鉤點；是work-detection，才要照[[feedback_event_driven_not_polling_pattern]]先找天然觸發動作。判斷關鍵字：檢查對象是「有沒有新東西發生」(work-detection，優先事件驅動) vs 「這個東西還在正常運作嗎」(liveness check，定期輕量檢查可接受)。

Related: [[feedback_event_driven_not_polling_pattern]]、[[reference_hermes_gateway_hang_watchdog_2026-09-08]]
