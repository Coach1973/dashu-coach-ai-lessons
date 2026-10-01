# 線上報名 SOP（2026-10-02 教練命名）

> **教練口語別名（聽到任一句就是這份）**：「線上報名 SOP」「網路報名 SOP」「加上線上報名」「加上網路報名」「幫我加報名」「加一個立即報名」
> 標準範本：10/3「用手機就能玩 AI」https://event.bymyway.com/curated/bigtree-1003/ 的報名機制。
> 第一個套用案例：https://event.bymyway.com/curated/ema1017/ （2026-10-02）

## 這套 SOP 做到什麼
任何活動網頁，訪客按「立即報名」→ 跳到頁面裡的報名表（姓名、電話、人數）→ 送出 → 跳出「報名資料已送出！」視窗＋「加入 LINE 並傳送報名資料」按鈕。
同一時間：資料存進 event.bymyway.com 資料庫，**「活動報名即時通知」Telegram 群（教練＋佩佩老師）立刻收到**。

## 步驟（AI 照做，不用問教練）
1. **建場次**：`event-signup/event.db` 的 `events` 表新增一列，`slug` 跟網頁短網址一樣（例：`ema1017`），填 `name`（活動名）、`event_date`、`start_time`、`location`（如「台北場」）、`venue`、`address`、`event_url`、`site='curated'`。
   ⚠️ 沒建這一列，報名照樣會通知，但會變成「場次代碼對不上、資料沒入庫」的警告。
2. **改網頁**：
   - 所有「立即報名」按鈕改成 `href="#signup"`。
   - 報名區（`id="signup"`）放入表單 `#regForm`（姓名*／電話*／人數）。
   - `</body>` 前放成功視窗 `#okModal` 和送出程式；程式裡改兩個值：`SLUG`（=場次 slug）、`SESSION`（顯示在 LINE 訊息裡的場次說明）。
   - 程式碼直接照抄 `knowledges/templates/線上報名_範本片段.html`，顏色用該網頁自己的變數。
   - 送出是 `POST https://event.bymyway.com/api/register`，內容 `{slug,name,phone,company:人數,source}`。
3. **策展網頁放在哪**：`/curated/<slug>/` 直接讀 `~/github_repos/<slug>/index.html`，改完立刻生效，不用重新上傳。改之前先備份原檔。
4. **驗證（不准吵到教練的群）**：
   - 後端：用 `event-signup/venv/bin/python3` 開 Flask test client，把 `_notify_xiaolongxia` 換成假函式，打一次 `/api/register` → 確認回 `ok:True`、通知文字正確 → **刪掉測試的 attendees＋signups**。
   - 前端：瀏覽器裡先把 `window.fetch` 換成假的，再點「立即報名」→ 空白送出要出現紅字 → 填好送出要跳成功視窗、且送出內容的 slug 正確。手機寬度 375 也要量一次沒有左右捲動。
   - 真的送一筆＝群組會收到通知，只有教練說可以才做。
5. **回報教練**：網址自己一行（不要在網址後面黏任何字）。

## 注意
- LINE 按鈕目前用大樹教育官方 LINE `https://lin.ee/o5pODV8`（跟 10/3 一樣）；主辦方另有 LINE 時，教練說了再換。
- 通知標題目前固定是「【大樹小講・官網報名】」，人數會顯示在「公司」那一行（跟 10/3 一樣）。
