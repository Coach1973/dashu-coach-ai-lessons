---
name: reference-event-signup-deploy-only-on-mac
description: event-signup這套Flask app（event.bymyway.com）正式站只跑在Mac(com.coach.event-webapp launchd)，非Mac機器改完程式碼push上去後還需要Mac那邊git pull+重啟服務才會生效
metadata:
  type: reference
---

`event-signup`（`event.bymyway.com`所有路由：`/checkin`、`/admin`、`/tut`、`/bigtree`、`/todo`、`/leader`等）這套Flask app，**正式對外服務只跑在Mac一台機器上**，由`com.coach.event-webapp`這支launchd管理，SQLite資料庫(`event.db`)也只有Mac那份是真的正式資料。

**Why:** 2026-09-03在聯想Windows這台幫教練做`/leader`報名頁（design(4).html邀請函+表單），程式碼（`app.py`路由、`schema.sql`新表、`templates/*.html`）在聯想本機寫完、用本機8899埠+獨立測試DB驗證過、推上GitHub後，才意識到**這個repo在非Mac機器上只是原始碼倉庫，不是活的伺服器**——聯想這台沒有`com.coach.event-webapp`服務、也沒有`~/.openclaw/openclaw.json`（Telegram bot token來源，所以本機測試時Telegram通知會安全失敗、不會誤發真訊息），因此無法讓正式站`event.bymyway.com/leader`真正生效，必須寫信交接給Mac讀信後`git pull`+重啟服務才算真正上線。

**How to apply:**
- **任何非Mac機器（聯想/ACER）要幫`event.bymyway.com`加新路由/改功能**：程式碼可以在本機寫完、測試（本機開個安全埠如8899跑`python app.py`，因為`DB_PATH`是寫死在`db.py`裡指向本地`event.db`，不會碰到Mac的正式資料，測完記得把本機產生的`event.db`/`notify_failures.log`等測試產物清掉不要commit進去），推上GitHub後**還需要一步：寫信到`cross-agent/inbox/mac/`交接，或直接告知教練需要Mac那邊`git pull`+重啟`com.coach.event-webapp`才會生效**，不能自己說「已經上線了」。
- 本機測試時打Telegram會因為缺`openclaw.json`裡的bot token而安全失敗（寫進`notify_failures.log`，不會误发真訊息到教練/佩佩老師的群組），這是非Mac機器測試這類通知功能時的安全網，不用刻意迴避測試。
- 相對地，純靜態網站（自己開新GitHub repo+GitHub Pages，例如`tut-alumni`、`ai-art`）**不受此限**，任何機器都能獨立完成從建repo到上線的全流程，不需要Mac配合。差別在於：GitHub Pages是靜態內容直接由GitHub serve；`event.bymyway.com`是動態Flask app+SQLite，只有Mac在跑那個process。

相關：[[project_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]（event.bymyway.com這套即時渲染架構的由來）
