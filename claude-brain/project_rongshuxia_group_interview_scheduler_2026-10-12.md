---
name: project-rongshuxia-group-interview-scheduler-2026-10-12
description: 「龍馥夏」＝榮樹下（語音）；LINE 小龍蝦在「榮樹下談公益」群組排訪談：專屬分身 rongshuxia＋教練行程總表 json＋schedule-context 外掛，巴哈助理共用同一份行程
metadata:
  node_type: memory
  type: project
  originSessionId: d2f1840b-1c75-4eb2-bd6d-77e9cb276c66
  modified: 2026-10-12T01:05:19.803Z
---

2026-10-12 教練要 LINE 小龍蝦在「榮樹下談公益 Run for Future」群組（LINE 群 C2f85a1e6010c4be676b93c5386da3d66，17 人）幫他整理對話、記錄行程、排訪談；對方丟時間就回答行不行。教練語音說「龍馥夏」＝榮樹下（[[reference-brand-name-rong-shu-xia-2026-10-12]]）。

**教練定的規則：**
- 不是看教練個人行事曆。來源是：①大台南培訓行事曆（tainan-calender.netlify.app）只算 ZOOM 線上場次（MSP、DnA 月例會、LTRT、執董與新會員有約等）；北科大 M1/M2 等實體場不是教練的行程 ②教練交給佩佩老師的「巴哈助理」（Telegram 群 -5115910257，agent peipei）的行程
- 訪談幾乎都在晚上（預設 19:00-22:00，這個時段是我定的，教練沒指定）
- 10/17 台北演講、10/18 整天在台北（教練 10/12 親口說的，巴哈那邊原本沒有記錄）

**怎麼做的：**
- 唯一真相源 `workspace/knowledges/教練行程總表.json`，只能用 `workspace/scripts/coach_schedule.py` 增刪（add／add-weekly／remove／check／list／sync-tainan；add 加 `--notify-baha` 會通知巴哈群組）
- 外掛 `extensions/schedule-context`：rongshuxia 群組有人提到日期或時間 → 先算好行不行再附給模型，外人只看到「已有安排」；peipei／main 聽到教練講行程時，提醒順手寫進總表；大台南行事曆超過 24 小時就在有人說話時順手同步
- 分身 `agents/rongshuxia`：綁定這個群組；只有教練的 LINE 編號 U895a… 能讓它執行指令，其他成員一律不能動電腦

**Why:** 群組裡有外人。原本 main 在 LINE 群組沒有限制誰能叫它執行指令，所以改用專屬分身。

**How to apply:** 教練說「那天有行程」或改期時 → 寫進總表，不要只設提醒。哪天要擴充到其他群組 → 照 rongshuxia 再做一份，換 GROUP_AGENT。RPL 週日 20:00 是 8 月舊紀錄，標了「待確認」；10/22、11/19 主持搭檔場的時間未定，也標「待確認」。

**2026-10-13 教練更新：**
- 行程已公開：群組外人也看得到行程名稱（不給地點、備註）；撞期時一定要講撞到什麼，撞到「榮樹下訪談」要說「已經排了榮樹下 Podcast 訪談」，不能只說「行程已滿」（`coach_schedule.py describe(private)`＋外掛規則＋rongshuxia SOUL.md）。
- 預約頁不填姓名電話：點空檔→四個按鈕，「榮樹下訪談」＝邱裕榮；「咖啡會議／電話回訪／入會訪談」＝陳佩君老師（BNI）。其他類型（諮詢會議、分享會、線上學習、戰報）不開放。教練語音「錄會訪談」＝入會訪談（BNI 12 項實戰學能之一）。類型表在 `event-signup/coach_schedule_view.py` 的 `BOOKING_TYPES`。
- **登記訪談對象（10/13）**：邱裕榮先定時間、對象之後才定。群組小龍蝦列「🎙️ 榮樹下已預約」；邱裕榮／教練說「哪場訪問誰」→ 模型在回覆尾巴寫 `⟦登記對象⟧ id｜對象｜類別`，外掛 message_sending 送出前真的跑 `coach_schedule.py set-guest`（通知巴哈群組＋排開始前 1 小時 openclaw cron 提醒，cron 要 `--no-deliver`），暗號換成登記結果；外人說的不登記。LINE 不支援快速回覆按鈕（OpenClaw 沒有），選時間靠預約頁。
- **巴哈群組（10/13）**：每天 07:00 `daily-report --send`（cron id ed6ef8a3）；預約頁通知改送巴哈群組（bot_peipei），失敗才退回活動報名群；佩佩老師（8786886419）問行程也注入今日報告。網站服務／cron 呼叫 openclaw 要直接用 node＋openclaw.mjs（PATH 沒 node）。
