---
name: openclaw2-heartbeat-message-failed-bug
description: OpenClaw 2.0內建heartbeat每30分鐘插進教練Telegram主對話，永久關法是openclaw.json設heartbeat.every=0m（system heartbeat disable重開就失效，09-25已改）
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

## 🔴 2026-09-17 追加：`system heartbeat disable`不是持久化設定，process重啟就會失效

**現象**：9/14修好之後，用`cron_run_receipts`資料表逐筆核對，確認9/15 16:37~9/16 03:37這35小時心跳確實每次都正確顯示`skipped: disabled`。但9/16 04:11（main gateway+小二雙雙down機事故搶修期間，見試金石案例73）起，心跳又恢復`error: heartbeat failed: agent-tool-failure`並持續到教練9/17回報為止。

**根因**：徹底查過`openclaw.json`（含`.bak`/`.bak.1~4`/`.last-good`五份備份）跟`openclaw.sqlite`所有資料表（`config_machine_state`/`user_preferences`/`cron_jobs.job_json`），`system heartbeat disable`的「已停用」狀態**完全沒有寫進任何一個可查的持久化位置**——`cron_jobs`表裡這個job的`enabled`欄位本身仍然是`1`，停用效果應該是靠一個只存在gateway process記憶體裡的旗標判斷。這代表**任何讓gateway process重啟的動作（launchd重啟、nohup手動拉起、`doctor --fix`後的自動重起）都會讓這個旗標打回預設值（啟用）**，9/16事故裡對小二做的`nohup`手動重啟正是觸發點。

**更根本的修法（已改用，2026-09-17驗證生效）**：不要只用`system heartbeat disable`這個CLI指令（僅記憶體生效、不耐重啟），改在`openclaw.json`寫死持久化設定：
```json
{ "agents": { "defaults": { "heartbeat": { "target": "none" } } } }
```
這個路徑正是心跳失敗訊息本身附帶的官方提示文字：「Set agents.defaults.heartbeat.target: "none" to keep these internal.」。寫入後gateway會自動偵測到設定檔變動並熱重載（log出現`config hot reload applied (agents.defaults.heartbeat)`），不需要手動重啟，且因為寫在設定檔裡，process重啟也不會被清空。

## 悟到什麼（追加）
3. **CLI指令回傳`{"ok":true}`不代表這個狀態一定有持久化到磁碟——**沒去查證儲存位置，就不知道這個「修好了」在下一次process重啟後還算不算數。這次代價是教練又忍受了近22小時的噪音才發現。以後遇到「用指令關掉某個功能」，若時間允許，應該多問一句「這個設定存在哪裡，重啟後還在嗎」，能找到對應的設定檔寫法就優先用設定檔（天然持久化），不要只依賴CLI的runtime toggle。

## 相關
- [[reference_jarvis_kickoff_partner_checkin_2026-09-13]]（小二本機log查法的既有SOP，本案例是同一套查法的延伸發現）
- [[reference_line_plugin_extensions_missing_2026-09-16]]（教練9/17提問促成的回頭查證，發現這次心跳regression跟LINE外掛遺失是兩個完全獨立的系統/事件，沒有因果關係，但都指向「gateway重啟/熱重載本身有風險」同一個主題）

## ✅ 2026-09-25 永久修法（取代上面的 `system heartbeat disable`）

上面 9/17 記下「重開就失效」卻沒改成永久設定，9/22 23:20 gateway 重開後心跳復活，每 30 分鐘插進教練的 Telegram 主對話（一天 70~110 次），帶著「不要接續舊任務、回 NO_REPLY」指令，小龍蝦因此嘴上說好卻不動（試金石案例83）。

**正確做法**：`openclaw config set agents.defaults.heartbeat.every 0m`（寫進 openclaw.json，官方文件 `docs/gateway/config-agents/heartbeat-compaction-and-streaming.md`：`0m disables recurring cadence`，不用重開 gateway）。驗證：`openclaw cron list --json` 裡 declarationKey 以 `heartbeat` 開頭的排程應為 0 筆。背景 exec 完成的事件喚醒仍會運作。若將來要恢復心跳，改用 `isolatedSession: true`（每次在獨立對話跑，不碰教練的對話）＋`target: "none"`，不要用預設值。
