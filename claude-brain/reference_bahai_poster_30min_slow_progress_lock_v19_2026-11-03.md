---
name: reference_bahai_poster_30min_slow_progress_lock_v19_2026-11-03
description: 巴哈(peipei)11/03 13:26~13:56 改海報版面拖30分鐘沒出圖、只送出1則進度；查到的原因與 safety-locks v1.9（時間版進度鎖＋參數自動修正）；還沒修的部分
metadata:
  node_type: memory
  type: reference
  originSessionId: 8f583093-6086-42e2-8bfa-75232ec6f5d3
  modified: 2026-11-03T06:13:44.112Z
---

**事件**：教練 11/03 13:26 在群組丟海報＋要「時間地點區塊搬左邊、左下角照片換本人」，巴哈 13:56 才回「還沒出成品」，期間幾乎沒有進度。

**查到的（peipei sqlite transcript＋gateway log）**：
- 這不是 SOP 一行指令 `poster_new_person.py` 的範圍（那只管「換人」），巴哈沒有現成指令就自己摸索：33 步、中位數每步 38 秒（對話已 150K～185K token，MiniMax 變慢），其中 view_image 18 次。
- 7 次工具因型別打錯被擋（view_image paths 寫成 {"item":[…]}、sessions_search limit "8"、message final "false"）；13:34、13:54 的進度訊息就是因 final:"false" 被擋，沒送出。
- 13:47 對話超過預算(185K)→強制壓縮，空白約 3 分半，13:50 被「Continue the current task」叫醒。
- view_image 的模型鏈 MiniMax-VL-01 空白／Claude 401／Google 金鑰無效，**當天只整串失敗 1 次**（13:31），不是主因。
- 原有「悶頭鎖」是按次數（30 次）且失敗的 message 也會把計數歸零，所以沒擋到。

**修法（commit ec59cc22a，11/03 14:13 gateway 重載）**：`extensions/safety-locks/index.js` v1.9
1. 時間版進度鎖：telegram/line/discord 的一輪裡 3 分鐘沒對外講話，擋一次工具、要它先講「現在在做什麼／做到哪／還要幾分鐘」。
2. 參數自動修正（hook 回傳 params）：paths 物件/字串→陣列、limit/maxImages/maxBytesMb 數字字串→數字、final 等 "true"/"false"→布林。已用巴哈當天的 4 種真實錯誤單元測試通過。
- 備份 `index.js.bak-20261103-before-silent-time-coerce`。

**還沒驗證／沒修**：真實對話裡 hook 回傳 params 是否被 gateway 採用（要等巴哈下次實際出錯或測試）；超出 SOP 的海報改版面仍沒有一行指令；長對話(150K+)每步慢；壓縮空白期。

相關：[[reference_turn_budget_lock_bots_silent_loop_2026-10-30]] [[reference_img_list_one_command_deliver_first_lock_2026-11-02]] [[feedback_bot_instructions_must_block_old_path_and_measure_tokens_2026-10-25]]

**後續（11/03 14:35 收工時）**：教練要「丟檔案就調 LK888 出圖、成品傳回群組不貼給他看」。已寫 `workspace/scripts/lk888_edit_image.py`（Claude 拆工單→LK888 只重畫要改的塊→貼回；`--send-to` 傳群組；成品字逐行比對把關）。真圖測 5 輪未過關：LK888 畫小字會錯（2:30／缺字／亂碼）。下一步＝日期時間地點用電腦字體貼、LK888 只畫人物。**學到**：不要拿 LLM 的「看起來 OK」當核對，用「抄字＋程式比對」才抓得到錯（舊核對連 2:30 都放行）。
