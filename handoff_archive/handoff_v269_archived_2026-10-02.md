## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 07:10 台灣時間，Mac 桌面版 Opus 5.5→Sonnet 5.5，v269）

**主軸：賈維斯成長計畫第四步③④完成——四位夥伴分身有了「三種標準」，記憶 127 條全部轉進反射系統（未處理 0）。**

### 做了什麼
1. **四位夥伴分身（peipei／kong／yijing／yang）SOUL.md 最前面加「🧭 三種標準（夥伴版）」**：先看紀錄與記憶、能推斷不問、說「做不到」前先看工具清單、語音錯字照最合理意思做、不答應做不到的事（例：不能主動傳訊息就別說「到時候提醒您」）；教練的公開活動直接查單場頁 `https://event.bymyway.com/curated/bigtree-月日/`（首頁「近期場次」是 JS 畫的，抓網頁看不到，別用首頁判斷）；yang 稱呼一律「Simona」。四群 session 已封存，gateway 真實路徑四位都逐字貼出第 3 點。**行為前後對照**（楊老師 10/1 真實語音句「大肅執動拜六那場AI課是幾點」）：改前叫「楊老師」並反問「您手邊有資料嗎」；改後叫 Simona、自己開 bigtree-1003，答出 14:00–16:30、13:40 入場、KR 養生廚房、免費（與網頁一致）。commit：peipei `cf586c1`、kong `9ff7bb119`、yijing `c9346f4`（三個獨立 repo，peipei／kong 含 09-24 未提交的「大樹作品 kind 分流」段一起存）、外層 `e6f5f4993`（yang）。測試對話 7 個已刪並 `memory forget`。
2. **記憶 127 條 → 反射系統**：新反射 13 條（git rebase 卡住、git 分岔先讀接力棒、改 coach888、寫 SOP 要寫口語別名、「全面X」範圍、BNI PPT SOP、claude rc 不 unset、sendBeacon CORS、策展刪除＝退役、git add -A 個資、MiniMax guard、大樹小講場次連動 event.db、台灣重心），每條都用歷史資料回測並收窄（coach888 408→135 次；台灣重心改抓 09-30 真實刺激「上海／廈門／中國商業」，命中正好是寫錯那一刻）；其餘 111 條登記 `memory_ledger`（併入哪條／參考資料／判斷類／已有程式／已退役）。`scripts/reflex_coverage.py` 新增記憶檢查：171 條未處理 0、索引斷鏈 0；補建從未寫入的 `feedback_no_wrong_posts_no_action_2026-09-18.md`、補收 `reference_openclaw_hook_inject_format`（標⛔過時）。`reflex_router.py` post_tool 自我排除也看指令（回測輸出曾誤觸）。commit `dfe39d869`、`bc0c25a79`、`e036177f6`，本次總結另計。

### 卡在哪／發現
- **楊老師（Simona）週六 AI 課提醒（07:08 教練原話：「要嘛讓小龍蝦能主動提醒，要嘛你幫忙提醒，對他來說只要有提醒就好」＝同意）**：yang 分身沒排程工具（安全鎖禁 exec），改由 Mac 端 `openclaw cron add` 代排兩個一次性工作，delivery 走 bot_main 投到她的群組 -5405039910：`08f1`→已換成 `4c706494-…`（10/2 12:00 台灣時間）、`e5fac0d4-…`（10/3 12:00 最後一次）。實測踩到 2 個坑：`--exact` 不能配 `--at`；分身若自己呼叫 message 工具發訊息，系統還會把它最後那句「已送出」再轉送一次（群組會多一則怪訊息）→指示改成「最終回覆就是提醒本文、不准用 message 工具」。已用只送教練的測試工作跑兩次，第二次確認最終回覆＝提醒本文、狀態 delivered，測試工作已刪。**12:00 後要確認**：`openclaw cron list --json` 看 `4c706494` 是否已消失/lastDelivered=true；教練說過「她說我知道了就停」，分身會先讀 MEMORY.md 判斷，她回「我知道了」時分身要把這句寫進 MEMORY.md。
- `state/member_context.log` 仍只有 03:34 兩筆測試，沒有真實 LINE 流量（龍蝦小助教認人未驗證）；聯想／宏碁沒回信（`cross-agent/inbox/mac/` 資料夾不存在）。
- 發現 kong 的 SOUL.md 寫「唯一指定模型 MiniMax M2.7」，但 `openclaw.json` kong 是 `minimax/MiniMax-M3`（peipei 的 SOUL 06-03 已升 M3），兩處矛盾；沒動（模型鎖需教練授權日期），記在 🔧 清單。

### 📋 下一場開工先做
賈維斯成長計畫第四步剩兩項，都在等外面（10-02 07:10 查過仍無動靜）：①看 `state/member_context.log` 有沒有真實 LINE 流量、第 4 欄是不是 `sender:u…`（龍蝦小助教認人）；②`cross-agent/inbox/mac/` 有聯想／宏碁回信就驗收（反射畫面原文＋開工🎯＋commit）。兩項都沒動靜就問教練今天從哪件事開始，不要空轉。

