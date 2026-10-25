# 大樹作品頁留資料（含顧問師天團 skyteam）通知同步一份到教練個人對話

> **寄件人**：Mac mini 小龍蝦（MiniMax-M3，1號機）
> **收件人**：Mac 軍師（Claude Code）
> **時間**：2026-10-25 18:50 台灣時間
> **教練是否在場**：是（教練 18:34 在 Telegram 本人對話親口交辦，18:26 亦在「活動報名即時通知」群親口問過）
> **回覆要求**：需要回覆（回報 commit hash、push 結果、測試結果）

## 內容

### 教練原話（逐字）

> 「剛才我有跟活動報名即時通知那邊說，如果顧問師天團那邊有任何回覆的話，希望我們這裡也能同步有一份，我怕那邊訊息太多會沒看到」

> 「為什麼我沒有得到通知？我問你我才看到，還是其實有通知但我沒看到？下次遇到這種商品的時候，能不能同步在我的個人訊息，或者頂級特助那邊也同步通知一下？」（18:26，在「活動報名即時通知」群）

### 目標

`event-signup/app.py` 的 `/api/works/contact`（大樹作品頁通用留資料表單，skyteam 顧問師天團頁面也走這支）**目前只通知「活動報名即時通知」群（-5349981085）**，教練個人對話（6124913915）完全收不到。

請改成：**群組照舊通知，同步再送一份到教練個人對話**。

具體改動（最小幅度，不要動其他任何路徑）：

1. `app.py` 常數區已有 `TELEGRAM_NOTIFY_CHAT_ID = "6124913915"`（教練個人對話）與 `TELEGRAM_REGISTRATION_GROUP_CHAT_ID = "-5349981085"`（報名群組），直接沿用，不要新增常數、不要改這兩個值。
2. `api_works_contact()` 成功路徑（DB 寫入成功後的那次 `_notify_xiaolongxia(..., chat_id=TELEGRAM_REGISTRATION_GROUP_CHAT_ID)`）**之後**，補一次同內容的 `_notify_xiaolongxia(..., chat_id=TELEGRAM_NOTIFY_CHAT_ID)`。
3. `api_works_contact()` 的「資料庫寫入失敗」分支（`⚠️【{title}・留資料寫入失敗】` 那次群組通知）**之後**，同樣補一次到教練個人對話——寫入失敗更要讓教練第一時間知道。
4. 同步給教練的那份開頭加一個標記（例如 `📩【{title}】有人留資料（同步給教練）`），讓教練一眼分辨這是同步副本、不是漏發的群組訊息。
5. **其他通知路徑一律不動**：`/api/register`（大樹小講報名）、`/api/tut/alumni`（校友會召集令）維持只發群組，這是 2026-08-24 教練裁示的既有行為，不要順手改。

### 已完成的部分請勿重做

- skyteam 頁面本身早已上線並在線（`https://event.bymyway.com/curated/skyteam/`，registry slug `skyteam`、`status: live`、`repo: Coach1973/skyteam`）。
- 2026-10-25 09:21:05 那筆「陳瑋琳 id=6」已確實進了 `works_contact_leads`（site=skyteam），**通知也確實有送到群組**（`notify_failures.log` 當天無失敗紀錄＝送達成功）。教練是「沒看到」，不是「沒送到」。所以**不需要補發任何歷史通知**，也不用查漏資料。
- 不要去動 `works_contact_leads` 既有資料，也不要清資料。

### 要避開的坑

1. 🔴 **絕對不要新增任何 LINE 推播**。教練 2026-10-20 常設禁令：所有 LINE 小龍蝦沒有教練許可不得使用會扣額度的推播。本次的同步一律走 Telegram。（`_notify_xiaolongxia` 只在 `chat_id == TELEGRAM_REGISTRATION_GROUP_CHAT_ID` 時才會觸發 LINE 關鍵字轉發，新增的教練個人對話呼叫不會觸發，不要去動那條機制。）
2. 🔴 **`event-signup/app.py` 一旦被 `git add`，pre-commit 會自動跑 `event-signup/test_line_group_forward.py`，沒過會擋 commit。** 必須讓它過。
3. 🔴 **現有測試 `event-signup/test_works_contact.py` 會被你這次改動打破**（它現在斷言「通知只發到『活動報名即時通知』群」、且用 `len(SENT) == 1` 計數）。請**同步更新這個測試**成新的正確行為：
   - 正常送出後應該是 **2 則**通知：`SENT[0].chat_id == TELEGRAM_REGISTRATION_GROUP_CHAT_ID`、`SENT[1].chat_id == TELEGRAM_NOTIFY_CHAT_ID`。
   - 兩則的內容都要含作品名、姓名、電話、項目。
   - 後面所有「被擋就不通知」「Email 那筆正常通知 1 則」「機器人隱藏欄位不通知」「同一 IP 超過 10 次被擋」等計數斷言，要跟著改成新的每筆 2 則的正確數字，不要放寬成模糊斷言。
   - 建議再加一條：教練個人對話那則的開頭含「（同步給教練）」標記。
4. 🔴 **不要順手改其他服務、其他 repo、其他策展頁 HTML**，也不要改 `curated_sites_registry.json`（本次只動通知目的地，跟 registry 無關）。
5. 🔴 測試跑完請確認 `works_contact_leads` 沒有被測試污染（測試用暫存庫，正式 event.db 不該多出測試資料）。
6. ⚠️ `app.py` 是正式線上服務（launchd `com.coach.event-webapp`）。**改完不要自己去重啟服務**——由小龍蝦負責重啟與線上實測，你只負責改檔、測試、commit、push。

## 對應檔案

- `/Users/bymyway/.openclaw/workspace/event-signup/app.py`：要改的主程式（`api_works_contact()` 在第 2786 行附近；常數在第 63–64 行）
- `/Users/bymyway/.openclaw/workspace/event-signup/test_works_contact.py`：要同步更新的測試
- `/Users/bymyway/.openclaw/workspace/event-signup/test_line_group_forward.py`：pre-commit 會自動跑，必須維持全過
- `/Users/bymyway/.openclaw/workspace/event-signup/test_register_notify.py`：`/api/register` 路徑的測試，本次不應受影響（跑一次確認沒壞）
- repo：`/Users/bymyway/.openclaw/workspace`（branch `main`，event-signup 是這個 repo 底下的目錄，**沒有獨立 .git**）
- 教練個人對話 chat_id：`6124913915`　　報名群組 chat_id：`-5349981085`
- 線上服務：launchd `com.coach.event-webapp`（port 5060）

## 完成後請做

- [x] 讀完
- [ ] 在 `event-signup/app.py` 完成最小改動（教練個人對話同步通知，含寫入失敗分支）
- [ ] 更新 `event-signup/test_works_contact.py` 的斷言
- [ ] 跑過：`cd event-signup && ./venv/bin/python test_works_contact.py`（全過）
- [ ] 跑過：`cd event-signup && ./venv/bin/python test_line_group_forward.py`（全過，pre-commit 會擋）
- [ ] 跑過：`cd event-signup && ./venv/bin/python test_register_notify.py`（全過，確認沒誤傷）
- [ ] commit（只 stage `event-signup/app.py`、`event-signup/test_works_contact.py`）＋ push 到 `origin main`
- [ ] 用 `git ls-remote origin main` 確認遠端 hash 真的更新（commit ≠ push）
- [ ] **不要**重啟 event-webapp 服務（由小龍蝦做）
- [ ] 回報：commit hash、push 結果、三支測試的通過結果、git diff 摘要
- [ ] 把本檔移到 `cross-agent/outbox/2026-10/`（加 `done_` 前綴）
