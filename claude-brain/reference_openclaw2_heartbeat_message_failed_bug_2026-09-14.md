---
name: openclaw2-heartbeat-message-failed-bug
description: OpenClaw 2.0內建heartbeat:main排程約半數機率失敗並發「Message failed」到Telegram，修法是system heartbeat disable非cron disable
metadata:
  type: reference
---

# OpenClaw 2.0內建心跳排程bug：間歇性發「⚠️ Message failed」到Telegram（2026-09-14，小二環境發現）

## 現象
小二（`~/.openclaw-test2`，OpenClaw 2026.9.4）的Telegram對話裡，每隔約30分鐘~1.5小時，會收到一則`小龍蝦2.0助教: ⚠️ Message failed`的訊息，教練回報「看了有點煩」。

## 根因（已用`openclaw --profile test2 cron get`+`cron runs`查證）
OpenClaw 2.0建立新profile時會**自動內建**一個系統保護排程`heartbeat:main`（declarationKey，非教練或軍師自建），每30分鐘觸發一次agent turn。設計上這個心跳應該是**安靜的**（`deliveryStatus: not-requested`），但實際運作約有一半機率以`agent-tool-failure`失敗收場——查`/tmp/openclaw/openclaw-test2-<日期>.log`發現失敗那次內部觸發了28次`Telegram sendMessage was suppressed before delivery`重試迴圈（模型輸出`NO_REPLY`被框架的NO_REPLY偵測機制攔下，但重試邏輯沒有把NO_REPLY當作正常結束、反而不斷重打模型），最終判定`heartbeat failed: agent-tool-failure`，並在這個失敗時機把「⚠️ Message failed」發到教練的Telegram，跟`成功`(`ok-empty`,`silent:true`)的情況形成對比。

**這是OpenClaw 2.0產品本身（發布僅12天）的內部bug，不是小二/教練配置錯誤，也不是我們自建的cron。**

## 修法（已驗證有效）
1. **一般`openclaw cron disable <jobId>`對這個排程無效**，會回傳`Error: system-owned monitor jobs cannot be edited by cron clients`——因為它是受保護的系統監控排程，cron子系統故意擋掉一般編輯。
2. **正確指令**：`openclaw --profile <profile> system heartbeat disable`，回傳`{"ok":true,"enabled":false}`即成功。查看用`openclaw --profile <profile> system heartbeat last`可看最近一次心跳狀態。
3. 這個指令是**全域關閉該profile的心跳功能**，不是只關這一個排程實例——若之後想恢復（例如想利用心跳做小二的自我監控），用`system heartbeat enable`。

## 悟到什麼
1. **查log只看到「message failed」字樣、判斷「這是良性噪音不影響真實訊息送達」是不夠的**——一開始只查了log檔案，沒有實際確認這段文字有沒有真的送到教練的Telegram，被教練親自貼出聊天截圖打臉後才重新查證。**判斷一個錯誤訊息是否要緊，要查它有沒有真的送達使用者能看到的地方，不能只看log等級或字面意思猜測。**
2. **OpenClaw官方CLI對「系統保護排程」跟「一般排程」用不同的管理指令**（`cron disable` vs `system heartbeat disable`），排查陌生CLI工具時，遇到「操作被拒絕/被保護」的錯誤訊息，要往上一層找專屬子命令（`--help`逐層展開：`system` → `heartbeat` → `disable`），而不是假設某功能完全無法關閉。

## 相關
- [[reference_jarvis_kickoff_partner_checkin_2026-09-13]]（小二本機log查法的既有SOP，本案例是同一套查法的延伸發現）
