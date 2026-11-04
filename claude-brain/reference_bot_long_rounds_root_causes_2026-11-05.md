---
name: reference_bot_long_rounds_root_causes_2026-11-05
description: 分身一輪做 10～17 分鐘的真因（11/04 四輪拆解）：沒一行指令就亂找、傳檔資料夾不對試 5 次、答完被過期「Exec completed」叫醒再空轉；傳檔只能放 ~/.openclaw/media/outbound/
metadata:
  node_type: memory
  type: reference
  originSessionId: ce89e39c-b559-4b27-a874-d36e700da544
  modified: 2026-11-04T16:17:31.476Z
---

11/04 超過 10 分鐘的四輪（gateway log 依 traceId 分組＋各分身 sqlite transcript_events）：

- **10:32 佩佩（佩君老師要 KR 養生廚房 7 月至今名單）**：10:43 才答（11 分）。①前 5 分：沒有「依場地查報名」的一行指令，event.db 7 月場次 venue 欄是空的，只好翻 memory、備份 db、日曆、官網猜場地。②10:37～10:41：傳 CSV 一直報 `Local media path is not under an allowed directory`，試了 agents/peipei/media、workspace/media、~/.openclaw/media、/tmp/openclaw 都失敗，還去讀 openclaw 原始碼；最後成功的是 `~/.openclaw/media/outbound/`。③10:43 答完後，被過期的背景通知「Exec completed」叫醒，再空轉 8 分鐘（工具名錯、參數型別錯），進度鎖還逼它在答完後又發一則進度。
- **09:17 小龍蝦（教練丟 TAVA 出圖清單）**：說 3～5 分、實際 10 分。run_img_list 本身約 4.5 分正常；多出來的是 IMG-001「實景修飾」清單沒附參考照，自己找＋像素比對約 3 分。
- **22:17 榮樹下（教練 LINE 丟 19MB PDF、沒交辦）**：看圖模型失敗（Claude 401、pages 不支援）、OCR 路徑錯；答「沒交辦」後又被過期 Exec completed 叫醒空轉。
- **07:00 小龍蝦**：無人等待的自動巡檢，MiniMax 429 兩次（等 89s＋151s），最後 NO_REPLY，不影響人。

**已修（11/05 00:15 gateway 重載，台灣時間）**：①safety-locks v1.11 傳檔不在 outbound 就自動複製過去（~/.openclaw commit 96f4a1706）②`scripts/venue_signups.py "<場地>" --since YYYY-MM-DD` 一行查名單、場地未登記照實列＋反射 R-VENUE-SIGNUP-LIST（workspace 8345e6bf4）；event.db 補 ai-talk-0729 場地＝台南安平維悅酒店（備份 event.db.bak-20261105-before-0729-venue）③叫醒鎖：prompt 開頭是「Exec completed (」且沒有聊天信封＝背景通知叫醒，那輪非傳訊工具超過 4 次就擋。都只做過單元測試，**真實對話還沒碰到**，看日誌「📎 傳檔自動搬到 outbound」「⏰ 背景通知叫醒」「⏰🔒 叫醒鎖觸發」字樣驗證。

讀法注意：zsh 裡 `set -- $a` 不會切字，迴圈傳參要分開寫；python sqlite3 打不開就用 `sqlite3 -json "file:...?mode=ro"`。

相關：[[reference_openclaw_stale_main_session_wakeup_wrong_group_2026-11-01]] [[reference_bahai_poster_30min_slow_progress_lock_v19_2026-11-03]] [[reference_turn_budget_lock_bots_silent_loop_2026-10-30]]
