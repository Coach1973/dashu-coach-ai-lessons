---
name: project-coach-todo-reminder-system-2026-09-02
description: 教練專屬待辦提醒系統（仿Microsoft To Do），掛在event.bymyway.com/todo，程式碼完成待Mac部署上線
metadata:
  type: project
  originSessionId: cbe8bfb7-5b8c-497d-b87b-3acdaf73d1b4
  modified: 2026-09-02T05:08:04.550Z
---

教練2026-09-02交辦：想要一個像Microsoft To Do的個人待辦提醒系統，要嵌進「作品總覽」（coach888）+主動用Telegram提醒。三個關鍵決定教練當場拍板：

1. **顯示位置**：coach888新增一個獨立分頁/連結（不是塞進首頁），已放進「四、bymyway自架版」分區第6項
2. **功能範圍**：先做核心夠用版——標題/到期日/提醒時間/完成勾選/備註，不做子步驟、不做重複規則，教練說「先做核心夠用版，做好之後再依實際使用感覺加功能」
3. **提醒通道**：沿用教練個人專屬Telegram通道（`chat_id 6124913915`，跟mentor100申請通知/BNI信用証到期提醒同一條），不另建新群組/新bot

**技術做法**：沒有另外申請新子網域/Tunnel/launchd，掛在既有24小時跑的`event-signup`這支Flask app底下（`/todo`路由+`todos`表+四個CRUD路由），reminder邏輯獨立成`scripts/todo_reminder_check.py`，比照`bni_credit_expiry_reminder.py`同款設計（查到期未通知項目→`notify_coach.sh`發送→成功才寫回`reminder_sent`）。這是[[project_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]同一套「掛在既有服務底下降低被遺忘風險」邏輯的延伸應用。

**Why**：教練原話「我一定會打開作品總覽這個頁面，如果能在這裡面直接看到我的待辦事項，這樣會很方便」——核心需求是「省一個開別的App的動作」+「主動提醒不用自己記得檢查」。

**How to apply**：
- 待辦資料只存在`event.db`的`todos`表，不是獨立系統，日後若要擴充子步驟/重複規則等進階功能，直接加欄位/加路由即可，不用另起爐灶
- **這台聯想Windows機器碰不到Mac上活的`event.db`跟OpenClaw cron系統**，2026-09-02當場只能寫完程式碼+本機測試，真正上線（git pull+重啟launchd服務+註冊15分鐘一次的提醒cron）要等有Mac終端機存取權限的軍師執行，詳細部署步驟寫在`JUNSHI_HANDOFF_LATEST.md`v165
- 教練目前還沒輸入任何真實待辦事項，上線後畫面會是空的，這是正常狀態不是bug

Related: [[project_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]、[[reference_bni_membership_fee_history_and_chapter_transfer]]（同款notify_coach.sh模式的另一個真實案例可對照）
