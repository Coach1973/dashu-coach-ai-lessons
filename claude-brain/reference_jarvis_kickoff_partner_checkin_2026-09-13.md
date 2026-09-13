---
name: jarvis-kickoff-partner-checkin
description: 賈維斯每次開工時核對小龍蝦一代/Hermes/小二三方動態的具體查法，事件觸發非輪詢
metadata:
  type: reference
---

# 賈維斯開工檢查：三方動態核對SOP（2026-09-13教練拍板）

教練裁示：軍師扮演賈維斯角色統籌小龍蝦一代/Hermes/小二三方後，**每次教練下「開工」指令時**，順手檢查三方是否有回覆/新動態，不另設定時輪詢排程。這是掛在「開工」既有事件上的例行動作，非新增背景任務。

## 三方具體查法

**① 小龍蝦一代**：讀 `HEARTBEAT.md` 最新的「賈維斯派工」區塊——它靠自己既有的心跳cron機制自動讀取任務並執行，完成後會在HEARTBEAT.md留下狀態＋Telegram回報教練，軍師不用主動介入。

**② Hermes**：讀 `cross-agent/outbox/2026-09/`（或當月對應資料夾）裡最新一封`hermes-to-mac`開頭的回信——Hermes讀信是「教練說一句『讀信』」觸發，回信會`git push`後出現在outbox，軍師`git pull`後直接讀取即可，不用登入VPS。

**③ 小二（OpenClaw 2.0隔離測試環境）**：**禁止**用Telegram Bot API的`getUpdates`去查——已證實會把offset搶先消費掉，害gateway自己的長輪詢永久跳過那批訊息（2026-09-13案例，詳見接力棒v201）。改查本機gateway原始log：
```bash
grep -i "inbound\|outbound send ok" /tmp/openclaw/openclaw-test2-$(date +%Y-%m-%d).log | tail -20
```
看`Inbound message`（教練傳給小二）+`telegram outbound send ok`（小二回覆）的時間戳是否連續、有沒有斷點，藉此判斷小二是否正常收發，不需要也不應該主動發API訊息去「測試」它。

## 為什麼這樣設計

- 事件驅動（掛在「開工」上）而非輪詢，呼應[[feedback_event_driven_not_polling_pattern]]、[[feedback_liveness_check_not_polling_violation]]同一套原則。
- 教練沒開工時，三方不會被無意義打擾；教練一開工，代表教練現在真的要看結果，時機吻合。
- 小二查法特別排除Telegram API直查，是因為這正是2026-09-13造成小二輪詢異常的根因，查證方法本身不能重蹈覆轍。

## 相關
- [[reference_hermes_gateway_hang_watchdog_2026-09-08]]（Hermes另一種卡住模式，非本SOP範圍）
- 接力棒v201「軍師接力棒 · 2026-09-13 v201」完整記錄三方首輪派工實測過程
