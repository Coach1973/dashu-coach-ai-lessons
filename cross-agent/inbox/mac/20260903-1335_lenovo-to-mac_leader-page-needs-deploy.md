# 聯想交接：/leader 報名頁已寫好待部署，需Mac側 git pull + 重啟 event-webapp

> 寄件人：聯想Windows Sonnet 5
> 收件人：Mac
> 時間：2026-09-03 13:35 台灣時間
> 教練是否在場：是（教練親自交辦，等著看正式站生效）

## 內容

教練提供`design (4).html`（「領導人溝通的藝術」9/10邀請函稿），交辦做成`event.bymyway.com/leader`報名頁，需求：
1. 移除文案「（映璇公司一樓會議室）」
2. 報名成功同時：①推送通知到教練+佩佩老師共見的Telegram群組（沿用`TELEGRAM_REGISTRATION_GROUP_CHAT_ID`）②導流佩佩老師LINE官方帳號（`PEIPEI_LINE_OA_ID`）

已完成並推上GitHub（commit`9dc78d09`）：
- `event-signup/templates/leader.html`：邀請函頁面+報名表單（姓名/手機）
- `event-signup/app.py`：新增`/leader/`路由 + `/api/leader/join`端點（比照`/api/tut/join`同一套模式，CORS開放）
- `event-signup/schema.sql`：新增`leader_workshop_signups`表（`CREATE TABLE IF NOT EXISTS`，重啟服務會自動建表，不用手動migrate）

**已在聯想本機用8899埠+獨立測試DB完整驗證**：頁面渲染正確（地址文案已移除、控制台零錯誤）、表單送出→200→DB正確寫入→成功畫面顯示LINE OA連結，測試產物已清除不留痕。

**卡住的地方**：這台Windows沒有`~/.openclaw/openclaw.json`（Telegram bot token來源），也沒有`com.coach.event-webapp`這個launchd服務，所以無法讓正式站`event.bymyway.com/leader`真正生效，需要Mac這邊`git pull` + 重啟`com.coach.event-webapp`。

## 完成後請做

- [ ] `git pull` + 重啟`com.coach.event-webapp`
- [ ] curl驗證`event.bymyway.com/leader`正常顯示、地址文案已移除
- [ ] 若教練或你本人方便，跑一次真實表單送出測試，確認Telegram群組真的收到通知（記得跟教練說一聲這是測試訊息，或送出後主動告知教練可忽略）
- [ ] 完成後把本檔移到`outbox/2026-09/`
