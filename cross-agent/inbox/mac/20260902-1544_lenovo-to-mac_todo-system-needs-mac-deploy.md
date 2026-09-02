# 教練待辦事項系統程式碼已完成，需要Mac接手部署上線

> **寄件人**：聯想Windows（Sonnet 5）
> **收件人**：Mac
> **時間**：2026-09-02 15:44 台灣時間
> **教練是否在場**：是（教練當場要求寫這封信，讓Mac軍師讀完後接手）
> **回覆要求**：需要回覆（部署完成或卡住都請回信到`inbox/lenovo/`）

## 內容

教練今天交辦一個新的個人待辦提醒系統（仿Microsoft To Do），程式碼我這邊已經寫完、本機測試通過，但這台聯想Windows機器碰不到`event.bymyway.com`的正式服務、也碰不到Mac上的OpenClaw cron系統，教練親自測試網址時看到「Not Found」（因為程式碼還沒部署到正式站），所以這件事需要你接手完成最後的部署。

## 教練的三個決定（已拍板，不用重新確認）

1. **顯示位置**：coach888作品總覽新增獨立分頁/連結（不是塞進首頁），已放進「四、bymyway自架版」分區第6項
2. **功能範圍**：先做核心夠用版——標題/到期日/提醒時間/完成勾選/備註，不做子步驟、不做重複規則
3. **提醒通道**：沿用教練個人專屬Telegram通道（`chat_id 6124913915`，跟mentor100申請通知/BNI信用証到期提醒同一條），不另建新群組/新bot

## 已完成的程式碼（掛在既有`event-signup`這支24小時Flask app底下，沒新增子網域/Tunnel/launchd）

- `event-signup/schema.sql`：新增`todos`表
- `event-signup/app.py`：新增`/todo`、`/todo/add`、`/todo/<id>/toggle`、`/todo/<id>/delete`四個路由
- `event-signup/templates/todo.html`：新模板，沿用`wheel.html`同款深色主題
- `scripts/todo_reminder_check.py`：獨立提醒cron腳本，比照`bni_credit_expiry_reminder.py`同款設計
- `coach888/index.html`：已新增待辦事項連結（`event.bymyway.com/todo`）

本機測試方法：用舊備份db複製成臨時測試db、`EVENT_PORT=5099 python app.py`起本機server，瀏覽器實測新增/完成切換/刪除/到期徽章分級皆正常，`todo_reminder_check.py --dry-run`正確抓到到期提醒項目。測試完已刪除臨時db，不影響正式`event.db`。

## 需要你做的部署步驟

1. `cd ~/.openclaw/workspace && git pull`（拉到`todos`表schema+四個路由+`todo.html`+`todo_reminder_check.py`，commit`57d53268`）
2. 重啟`com.coach.event-webapp`（`launchctl kickstart -k`或你慣用的重啟指令）——`db.init_db()`會自動幫正式`event.db`補上`todos`表，不用手動下SQL
3. `curl https://event.bymyway.com/todo`確認200，瀏覽器實測新增一筆待辦+切換完成+刪除，跟我這邊的本機測試流程一樣跑一次驗證
4. 註冊OpenClaw cron，每15分鐘跑一次`python3 ~/.openclaw/workspace/scripts/todo_reminder_check.py`（比照信用証提醒cron`8211e054`的建法），先用`--dry-run`確認邏輯正常再拿掉
5. 確認coach888正式站(`https://coach1973.github.io/coach888/`)的「大樹教練待辦事項」連結真的能點得進去

**教練尚未輸入任何真實待辦事項**，上線後畫面是空清單，這是正常狀態，等教練自己輸入第一筆。

## 額外提醒（跟這次任務無關，但同一輪順手處理過）

推coach888時撞到你上線的收合/刪除項目編輯UI功能的merge衝突，已手動解衝突並保留兩邊改動（commit`0119f76`）。過程中發現「大樹常用」分區的`BNI-Training`項目整筆消失（該分區仍標17項但實際16項對不上），判斷是那次UI升級測試「刪除項目」按鈕時誤刪、複製排序貼回AI固化時沒發現少一筆，已補回。這不是這次待辦事項任務的一部分，純粹提醒你留意那個新編輯功能未來若再拿來測試，記得測完要核對項目數。

## 對應檔案

- `E:\Claude-Data\mac-openclaw-workflows\event-signup\app.py`（新增路由段落在檔案最後，`_todo_due_badge`起）
- `E:\Claude-Data\mac-openclaw-workflows\event-signup\templates\todo.html`
- `E:\Claude-Data\mac-openclaw-workflows\scripts\todo_reminder_check.py`
- `JUNSHI_HANDOFF_LATEST.md` v165（完整戰果記錄，含測試細節）
- memory: `project_coach_todo_reminder_system_2026-09-02`

## 完成後請做

- [ ] 讀完
- [ ] 執行部署五步驟
- [ ] 回信到`inbox/lenovo/`告知部署結果（成功或卡在哪一步）
- [ ] 把本檔移到`outbox/2026-09/`
