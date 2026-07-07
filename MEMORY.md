- [Browser no full junction](feedback_browser_no_full_junction.md) — 瀏覽器絕不整個 junction，只搬書籤等增量檔案
- [跨機備份 SOP 提醒](feedback_cross_machine_backup_reminder.md) — 教練新電腦（含佩佩老師那台）要做增量備份（junction 搬家）時主動提醒，引用試金石 W03 完整生命週期 SOP
- [OpenClaw spool stuck fix](project_openclaw_spool_stuck_fix.md) — VPS 小龍蝦訊息卡住：檢查 .processing 檔案並清除即可修復
- [ACER post-restore TODO](project_acer_post_restore_todo.md) — 一鍵還原後開工時必須主動提醒執行還原步驟
- [VPS 連線資訊](reference_vps_connection.md) — 小龍蝦與赫茲米 VPS 的 IP/帳密/指令，任何電腦都能直接連
- [先問再改](feedback_ask_before_reversing_unusual_config.md) — 發現軟體設定跟預期不同，先問是不是教練故意的，別自己當錯誤修正
- [5月還原大測試](project_may_2026_restore_test.md) — C槽退回5月+6套軟體重裝+D槽junction重接的完整SOP

## Promoted From Short-Term Memory (2026-07-04)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:273:276 -->
- 📨 對話記錄 12:41（共約 14 條，從第 0 行起）: 👤 教練：幫我看一下VPS出了什麼問題了為什麼我跟他對話沒有反應？ 🦞 小龍蝦：教練，我先去查 VPS 狀況，不是一直在問你。 🦞 小龍蝦：找到了 VPS 健康檢查腳本，原來 VPS IP 是 `43.245.60.200`（113.29.232.178 是 aiprimetech 代理）。先用這個去查 VPS 狀態： 🦞 小龍蝦：VPS 跟容器都還活著，問題在裡面。我繼續挖： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-23.md:273-276]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:277:280 -->
- 📨 對話記錄 12:41（共約 14 條，從第 0 行起）: 🦞 小龍蝦：找到核心問題了。繼續挖細節： 🦞 小龍蝦：繼續確認教練訊息到底有沒有送進 VPS： 🦞 小龍蝦：注意：過去 12 小時 VPS 根本**沒收到教練任何訊息**（沒有 chatId=612 的 inbound）。再查 Telegram polling 狀態： 🦞 小龍蝦：確認容器內部到底是什麼，並看 VPS 到底有沒有收到教練的訊息： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-23.md:277-280]

## Promoted From Short-Term Memory (2026-07-05)

<!-- openclaw-memory-promotion:memory:memory/2026-06-24.md:278:278 -->
- 📨 對話記錄 08:42（共約 1 條，從第 0 行起）: 👤 教練：[cron:5d687b38-5627-4087-ae3e-ddd0bb12127e 🦞 每30分鐘任務健康檢查] 你是健康檢查助理。安靜執行以下檢查並自動修復，不需要通知教練（除非發現無法自動修復的嚴重問題）： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-24.md:278-278]
<!-- openclaw-memory-promotion:memory:memory/2026-06-24.md:282:282 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openclaw cron list` 或 cron tool 檢查所有任務的 consecutiveErrors 與 lastStatus。 [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-24.md:282-282]

## Promoted From Short-Term Memory (2026-07-06)

<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:268:270 -->
- 📨 對話記錄 03:42（共約 19 條，從第 0 行起）: 👤 教練：確認一下執行網頁推SOP有沒有問題 🦞 小龍蝦：教練，收到。我立刻去把網頁推 SOP 翻出來，逐項對照最近的執行紀錄，給您一份「確認結果」。 🦞 小龍蝦：教練，確認完畢。**有一個問題**，報告如下： [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-25.md:268-270]
<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:278:281 -->
- ✅ 沒問題的部分: | 檢核項 | ai-go | consultant | |--------|-------|-----------| | 站台分流（GitHub Pages 走 git push，符合 SOP）| ✅ | ✅ | | 一次性推送（不分批，符合守則 #08）| ✅ 1 commit | ✅ 1 commit | [score=0.886 recalls=0 avg=0.620 source=memory/2026-06-25.md:278-281]

## Promoted From Short-Term Memory (2026-07-07)

<!-- openclaw-memory-promotion:memory:memory/2026-06-28.md:273:274 -->
- 📨 對話記錄 11:15（共約 3 條，從第 0 行起）: 👤 教練：這裡並沒有蒸餾的任務，如果要執行，應該是請學弟及學妹回報服務的情況，學長這裡每天也都有蒸餾報告，只是沒有同步到這裡來 🦞 小龍蝦：收到教練 👌 [score=0.876 recalls=0 avg=0.620 source=memory/2026-06-28.md:273-274]

## Promoted From Short-Term Memory (2026-07-08)

<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:37:40 -->
- ⚠️ 教訓記錄（給未來的我）: **過度依賴 USER.md 對照表**：看到「真鑽」就聯想到「真鑫」是 BNI 語音誤判，沒先求證。; **教練沒否認 ≠ 默認**：「提醒就好」只是要我不煩他，不是對「真鑫/真鑽」的答覆。我以為「未否認就是默認」是過度解讀。; **正確做法**：遇到 USER.md 沒列的陌生詞，**就算對方不回應，也要標註「未確認」而不是預設成某個值**。本次教訓要寫進 .learnings/。; **守則 #18「語音糾偏必問不猜」**：我問了，但問完又自己猜了，這還是猜。 [score=0.919 recalls=0 avg=0.620 source=memory/2026-06-30.md:37-40]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:80:83 -->
- 📨 對話記錄 09:15（共約 13 條，從第 0 行起）: 👤 教練：提醒事項： 1.我的個人介紹頁面要加上媒體報導 2.大樹教練的活動頁面要列舉近期活動紀錄 3.去雲端讀取開工資料就知道這幾天我都是用acer筆電在完成工作 [score=0.919 recalls=0 avg=0.620 source=memory/2026-06-30.md:80-83]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:87:87 -->
- 📨 對話記錄 09:15（共約 13 條，從第 0 行起）: ✅ **1. 小龍蝦個人介紹頁** → 等您說「做介紹頁」時，會主動補上媒體報導區塊（我會用您校正過的品牌資料，不上網亂抄）。 [score=0.919 recalls=0 avg=0.620 source=memory/2026-06-30.md:87-87]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:13:15 -->
- 大樹教練的活動頁面要列舉近期活動紀錄: 觸發時機：教練下令「做活動頁」「更新活動紀錄」時; 動作：列舉近期講座 / 演講 / 活動紀錄; 提醒：只列教練親自參與或主辦的活動，別亂湊 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:13-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:18:21 -->
- 情境事實：這幾天教練是用 ACER 筆電在完成工作: **這是已驗證事實**，從雲端接力棒鏈可以確認：; `9376e6f3 講座行銷頁 v5 + 接力棒（明早 ACER 開工自動接住）`; `34f169ce 講座行銷頁 v6 + EDM 7/1 上線 + 收工接力棒`; `cfdc898b EDM 報名表單上線總結接力棒` [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:18-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:22:23 -->
- 情境事實：這幾天教練是用 ACER 筆電在完成工作: 影響：開工讀接力棒時，這幾天的工作多半由 ACER 端發起；接力棒同步 bug 修了之後（grep -vF + 自動 pull），ACER 動作可被小龍蝦這邊即時看到; 後續：教練下次到 Mac 端開工時，主動告知「這幾天 ACER 端已有 X 個動作，內容包括⋯⋯」 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:22-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:27:27 -->
- 提醒 #4（09:11 教練新增 → 09:15 教練決定只設提醒 → 09:19 教練糾正「真鑽≠真鑫」）: > 提醒我「**真鑽**領導團隊遴選要盡快完成，找上屆及本屆三長討論」 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:27-27]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:29:32 -->
- 提醒 #4（09:11 教練新增 → 09:15 教練決定只設提醒 → 09:19 教練糾正「真鑽≠真鑫」）: **09:15 教練回覆**：「提醒就好，細節我知道就行」; **09:19 教練糾正**：我誤把「真鑽」猜成「真鑫」（BNI），教練明說是「真鑽」→ 已修正; ✅ Cron Reminder 已設定：2026-07-01 09:00 台北時間觸發; ID: e6ddab8f-09d0-402f-b42b-18d67186e59a [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:29-32]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:33:34 -->
- 提醒 #4（09:11 教練新增 → 09:15 教練決定只設提醒 → 09:19 教練糾正「真鑽≠真鑫」）: 一次性，跑完即刪; 提醒內容已改為：⏰ 真鑽領導團隊遴選。教練今天要跟上屆及本屆三長討論嗎？需要我幫您做什麼？ [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:33-34]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:44:47 -->
- 待辦總表（截至 09:12）: | # | 事項 | 狀態 | 等什麼 | |---|------|------|-------| | 1 | 小龍蝦個人介紹頁加媒體報導 | 待辦 | 教練下令做介紹頁 | | 2 | 大樹教練活動頁列活動紀錄 | 待辦 | 教練下令做活動頁 | [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:44-47]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:48:51 -->
- 待辦總表（截至 09:12）: | 3 | 跨機 verbatim 讀取架構（A/B/C） | 提案已交 | 教練拍板 | | 4 | 真鑽領導團隊遴選 | ⏰ 提醒已設，明天 09:00 | 教練說細節他自己處理，我只負責提醒 | | 5 | 聯想/ACER 自動蒸餾對話紀錄到雲端 | 📝 備忘已寫好 `knowledges/2026-06-30_跨機verbatim蒸餾備忘.md` | 教練開工時轉交軍師執行 | | 5 | #8242–#8250 蒸餾連續 4 天無新對話 | 暫停 | 教練下令排查 | [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:48-51]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:5:5 -->
- 🔴 教練提醒事項（09:05 Telegram 主對話框交付）: 教練丟了三條備忘性質的提醒，**未下令立刻執行**，等教練真的要做的時候再拿出來： [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:52:52 -->
- 待辦總表（截至 09:12）: | 6 | 提醒 #5 續：軍師執行狀態追蹤 | 待教練開工 | 教練開工後學長追進度 | [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:52-52]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:56:59 -->
- 開工當下狀態: 時間：2026-06-30 09:17; 收到教練三條提醒，已寫入 HEARTBEAT.md + 本檔; 早上的對話蒸餾（08:05）已正常運作，最近一次蒸餾是 6/26，主要內容是「ACER 接力棒同步修 bug」的故事; 起床摘要（06:03）正常：過去 12 小時 29 個純自動備份 commit，0 個值得教練看（合理） [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:56-59]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:64:66 -->
- 待辦（被教練暫停的，不是空轉）: #8242–#8250：蒸餾進程連續 4 天無新對話，已多次回報教練「待人工確認」，沒有看到教練下令排查 → 等教練下令再處理; 媒體報導區塊：等教練下令做個人介紹頁時補; 活動紀錄區塊：等教練下令做活動頁時補 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:64-66]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:70:70 -->
- 提醒 #5 備忘指令詳情（09:16）: 教練說：「你寫一個備忘指令給軍師，我開工時，請他寫指令讓聯想及acer工作除了接力棒之外也要自動蒸餾對話紀錄到雲端，以收集試金石檔案」 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:70-70]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:72:75 -->
- 提醒 #5 備忘指令詳情（09:16）: ✅ 備忘已寫：`knowledges/2026-06-30_跨機verbatim蒸餾備忘.md`（3.5KB）; 含：教練原始口諭 / 背景 / 軍師交付物 A–E / 風險 / 驗收標準 / 相關 commit 索引; 軍師開工時 AGENTS.md 規定會讀 `knowledges/` 新檔 → 會自動看到; 備忘架構選擇：直接走 B 路線（改 ACER/聯想端推 verbatim 上雲端），這跟 09:10 教練追問時我提的 B 選項一致 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:72-75]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:8:10 -->
- 小龍蝦個人介紹頁面要加上媒體報導: 觸發時機：教練下令「做個人介紹頁」或相關指令時; 動作：補上媒體報導區塊（媒體名稱、報導連結、日期）; 提醒：媒體資料只信 `user_coach_brand_data.md`，不要上網抄 [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:8-10]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:84:85 -->
- 📨 對話記錄 09:15（共約 13 條，從第 0 行起）: 🦞 小龍蝦：收到教練的提醒事項，馬上記下來，並主動去雲端確認一下 ACER 那邊的脈絡。 🦞 小龍蝦：教練，三件事我都記下了： [score=0.887 recalls=0 avg=0.620 source=memory/2026-06-30.md:84-85]
