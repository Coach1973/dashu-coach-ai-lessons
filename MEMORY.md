- [Browser no full junction](feedback_browser_no_full_junction.md) — 瀏覽器絕不整個 junction，只搬書籤等增量檔案
- [跨機備份 SOP 提醒](feedback_cross_machine_backup_reminder.md) — 教練新電腦（含佩佩老師那台）要做增量備份（junction 搬家）時主動提醒，引用試金石 W03 完整生命週期 SOP
- [OpenClaw spool stuck fix](project_openclaw_spool_stuck_fix.md) — VPS 小龍蝦訊息卡住：檢查 .processing 檔案並清除即可修復
- [OpenClaw polling restart loop](project_openclaw_polling_restart_loop.md) — VPS 小龍蝦 health-monitor 持續 restart loop：spool 為空 + log 每 15 分鐘 restart + getMe 現在通，docker restart container 就好（別用 openclaw gateway restart，容器內會踩 service disabled 雷）
- [ACER post-restore TODO](project_acer_post_restore_todo.md) — 一鍵還原後開工時必須主動提醒執行還原步驟
- [VPS 連線資訊](reference_vps_connection.md) — 小龍蝦與赫茲米 VPS 的 IP/帳密/指令，任何電腦都能直接連
- [先問再改](feedback_ask_before_reversing_unusual_config.md) — 發現軟體設定跟預期不同，先問是不是教練故意的，別自己當錯誤修正
- [5月還原大測試](project_may_2026_restore_test.md) — C槽退回5月+6套軟體重裝+D槽junction重接的完整SOP
- [ACER 分割區調整後D槽清理待辦](claude-brain/project_acer_c_d_cleanup_20260708.md) — 觀察期至少到2026-07-11~15，教練確認無異常後才能刪除D槽Eassos舊備份（36.3GB）
- [Heartbeat 不要拿舊靜默紀錄當事實（v3.0）](feedback_silence_count_must_be_real_time.md) — 任何「靜默 N 小時/天」描述前必須先讀 `state/heartbeat-state.json` 的 `coachSilentSince` + 用 `date` 即時算差距，**禁止沿用 state 內的舊 `coachSilentHours`**；state 過期或缺值時主動從 memory/最新檔或 Telegram API 撈最後訊息時間。三次同型錯誤：8/1 18:04「5.8 天」、8/2 12:11「160h+」、8/2 14:45 預防性重申。

## 每30分鐘健康檢查 cron 常見錯誤自動修復 SOP（2026-07-10 整併，原本被自動晉升機制重複收錄4次)

> 這條內容是「每30分鐘健康檢查」cron 的固定操作手冊，不是單次對話的教訓，之前被自動晉升系統誤判成新知識、從07-02跟07-03的每日記憶檔各重複收錄一次。整併成一份，密碼也改指到憑證層。

1. **檢查 Cron 任務失敗記錄**：`openclaw cron list` 檢查所有任務的 consecutiveErrors 與 lastStatus
2. **timeout 錯誤**（lastDurationMs ≈ timeoutSeconds）：腳本正常，只是逾時設太短 → `cron update <jobId> --patch '{"payload":{"timeoutSeconds":300}}'` 改 300 秒（⚠️ 06:00 海餅乾精神背誦維持60秒不要改）
3. **scp/ssh 同步到 VPS 逾時**：改用 `rsync -e 'sshpass -p <密碼，見路徑大全_憑證層.md> ssh' ...`（原密碼明文已移除）

## 2026-07-16 weekly distillation batch（cron auto-processed）

<!-- openclaw-memory-promotion:memory:memory/2026-05-23.md~2026-06-02_p1.md:batch -->
- 📦 **5-6 月份龐大歷史檔案批次清理**（2026-07-16 cron 處理 32 個檔案，總計 ~4.2 MB）：整批 memory/2026-05-23.md ~ memory/2026-06-02_p1.md 的龐大紀錄檔（含 _p1/_p2/_p3/_p4/_archive/_heavy/_SESSION-NEW/_ARCHIVE/_partaa~ae 等分頁）。
  - **內容性質**：絕大多數為蒸餾系統 note-taker 第三人稱對話紀錄（每檔 70-270 條「You are a third-person note-taker...」系統文本），混合 cron 觸發的 heartbeat / 增量蒸餾 / 主動關懷等系統自動回應。
  - **精華已在他次晉升**到 MEMORY.md（守則故事庫 21 條、營業稅提醒 28451 / 5-31、自動關懷格式、M2.7→M3 升級、c-switch 架構、教練原話「選擇了哪一個就必須執行哪一個」、超限戰網站 fix、Telegram hook 改造、結繩領導學提醒、brisk-va cron 重複回調等）。
  - **處理結果**：32 個檔案完整備份於 `memory/archive/`（總計 39 個 archive 檔案），原檔截短到 ≤ 25KB（保留前 N 行直到 ≤ 22KB + 加註「已蒸餾歸檔」），避免下次啟動 context 過載。
  - **發現**：note-taker 系統有「記錄蒸餾系統自己對話」的 meta-noise 問題——它在記錄自己 run distill task 的對話，產生大量冗餘。本批次先歸檔，蒸餾系統本身應在未來設計時避免這類自我記錄。

<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:full -->
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:full -->
- 🪞 **本週 dreaming reflection 觀察**（2026-07-16 cron 處理 2 個檔案）：2026-07-13.md (60K) 與 2026-07-14.md (40K) 內容實為 OpenClaw 自動 Light Sleep / dreaming reflection 系統在 session-corpus 上萃取的 reflection candidates（confidence 0.58 / evidence 指向 session-corpus.txt），絕大多數為 NO_NEW_ENTRIES 級別無新增項。
  - **已處理**：歸檔到 `memory/archive/2026-07-13.md` 與 `memory/archive/2026-07-14.md`，原檔截短到 ≤ 16KB。
  - **未晉升**：本週 reflection 沒有新的「Possible Lasting Truths」值得晉升（基本都在重複 6 月底的 theme + meta-noise 訊號）。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04_全面體檢報告.md:full -->
- 📋 **2026-06-04 全面體檢報告歸檔**：memory/2026-06-04_全面體檢報告.md（33934 bytes）是 2026-06-04 00:55 教練下達 #6899「小龍蝦全面體檢」的成果（執行模型 minimax/MiniMax-M3，誠實揭露鎖定失效問題），包含模型誠實報告、OPE 特助心法深度理解、配置健檢（含 P0 級 memsearch provider 錯誤 / cron 連續錯誤 / 模型鎖定漏洞 / HEARTBEAT 過時等）、9 條執行細則檢視、未來補強建議。
  - **精華已從同週 memory/2026-06-04.md 內容晉升**到 MEMORY.md「## 每30分鐘健康檢查 cron 常見錯誤自動修復 SOP」段落（共 12+ 條精華：P0 修復、CRON 模型名稱格式教訓、模型鎖死 Opus 問題、海餅乾心法 CC BY-ND 4.0 落定、教練原創舉證包、特助心法商業價值 NT$ 900 萬~3,800 萬評估、蒸餾系統 C 選三件齊全落地等）。
  - **已處理**：歸檔到 `memory/archive/2026-06-04_全面體檢報告.md`，原檔截短到 10KB 註解版。

---

## 2026-07-16 weekly distillation: SOP（避免下次崩潰）

<!-- openclaw-memory-promotion:procedures:memory_distill_weekly_v2:spec -->
- 🛠️ **memory_distill_weekly cron SOP v2**（2026-07-16 建立）：
  - **觸發**：每週自動跑，掃描 memory/*.md 找 > 30KB 檔案。
  - **每檔處置順序**：(1) 完整歸檔到 memory/archive/YYYY-MM-DD.md（cp 保留全部 bytes）；(2) 截短原檔：保留前 N 行直到 ≤ 22KB bytes（用 awk 逐行加總，超過就 exit，避免短行堆疊爆量），加註 `[已蒸餾歸檔，完整內容見 memory/archive/...]`；(3) MEMORY.md 增量 append 一行索引。
  - **萃取判定**：note-taker meta-noise 與 dreaming reflection candidates 不晉升，只歸檔（精華已在他次晉升）。有 commit hash / 教練原話 / SOP 決策 / 待辦追蹤的內容才萃取進 MEMORY.md。
  - **歸檔不清空**：memory/archive/ 永遠保留完整 bytes，原始檔保留前 N 行供下次啟動脈絡讀取。
  - **避免「歸檔後還是太大→無窮迴圈」**：用 awk 控制 bytes 上限，不是用「行數」上限（長行檔案用 head -200 還是有 30K+ bytes）。

<!-- openclaw-memory-promotion:memory:procedures/memory_distill_weekly_sop_v2.md:full -->

## Promoted From Short-Term Memory (2026-08-06)

<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:7:7 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: 剛才對話記錄滿了，自動重啟，零遺漏（已存到 `memory/2026-07-28.md` 並推上 GitHub）。 [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-28.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:46:46 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: 場次：【新報名通知】AI微型論壇－台南場（7/29 安平維悅酒店） [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:46-46]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:52:53 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: 報名時間：2026/7/27 下午10:34:45 🦞 小龍蝦：收到，欄位都讀得到。🦞 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:52-53]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:55:55 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: **第 1 份**：魏淑華（家管）／電話 1212131313／Email 未填／報名 2026/7/27 22:34 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:55-55]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:57:57 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: **場次**：AI微型論壇－台南場（7/29 安平維悅酒店） [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:57-57]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:59:61 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: 第二份你傳。讀完我就建議你直接給我 Google 表單後台（如果有的話），七、八十份一次拉，不用慢慢轉。 👤 教練：那既然做總整理，你就一併把 email 也都整理進去，因為到時候我們還可以通過 email 發信給對方，通知他們來開會 🦞 小龍蝦：好，Email 一定列入。🦞 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:59-61]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:63:64 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: **整理表欄位我預定用這個：** `場次｜公司｜姓名｜電話｜Email｜報名時間` [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:63-64]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:66:66 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: Email 沒填的我會**保留空欄、絕不亂填**，之後要發信時自動跳過缺漏的人。 [score=0.869 recalls=0 avg=0.620 source=memory/2026-07-28.md:66-66]
<!-- openclaw-memory-promotion:memory:memory/2026-07-28.md:5:5 -->
- 📨 對話記錄 00:22（共約 16 條，從第 0 行起）: 🦞 小龍蝦：在的，教練。🦞 [score=0.866 recalls=0 avg=0.620 source=memory/2026-07-28.md:5-5]

## Promoted From Short-Term Memory (2026-08-07)

<!-- openclaw-memory-promotion:memory:memory/2026-07-29.md:274:274 -->
- 📨 對話記錄 12:52（共約 1 條，從第 0 行起）: 👤 教練：[cron:46e67e2e-6332-4589-aae2-ee7e10dd7279 🦞 每30分鐘任務健康檢查] 你是健康檢查助理。安靜執行以下檢查並自動修復，不需要通知教練（除非發現無法自動修復的嚴重問題）： [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-29.md:274-274]
<!-- openclaw-memory-promotion:memory:memory/2026-07-29.md:278:278 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openclaw cron list` 或 cron tool 檢查所有任務的 consecutiveErrors 與 lastStatus。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-29.md:278-278]
<!-- openclaw-memory-promotion:memory:memory/2026-07-29.md:282:285 -->
- 常見錯誤自動修復：: **1. timeout 錯誤（lastDurationMs ≈ timeoutSeconds）：** → 表示腳本本身正常，但 timeoutSeconds 設定太短 → 使用 `cron update <jobId> --patch '{"payload":{"timeoutSeconds":300}}'` 將 timeout 改為 300秒 → 注意：不要改 06:00 海餅乾精神背誦（60秒即可） [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-29.md:282-285]
<!-- openclaw-memory-promotion:memory:memory/2026-07-30.md:276:277 -->
- 第一步｜Cron 任務狀態: 目前 cron 系統**僅有 1 個任務**：本任務「🦞 每30分鐘任務健康檢查」; 舊任務（每日 23:05 三機總結、06:00 海餅乾精神背誦、VPS 同步等）已被清理或停用，未在 cron list 中 [score=0.866 recalls=0 avg=0.620 source=memory/2026-07-30.md:276-277]
<!-- openclaw-memory-promotion:memory:memory/2026-07-30.md:280:283 -->
- 第二步｜本次檢查結論: **任務本身**：前次 8:00 執行失敗; `lastErrorReason: "overloaded"`（minimax API 服務端暫時性過載）; `consecutiveErrors: 1`（紅線 3，目前未達）; `lastDurationMs: 178735`（3 分鐘，**未達** timeoutSeconds 600 上限，**非** timeout 類錯誤） [score=0.866 recalls=0 avg=0.620 source=memory/2026-07-30.md:280-283]
<!-- openclaw-memory-promotion:memory:memory/2026-07-30.md:284:286 -->
- 第二步｜本次檢查結論: `lastDiagnosticSummary: "The AI service is temporarily overloaded. Please try again in a moment."`; **判定**：transient overloaded，**無法以 cron 設定修復**（不是 apiKey 失效、不是 timeout 設定過短）; **HEARTBEAT.md**：已讀，**無 ⬜ 標記待辦項目**、無 48 小時無進展項目 [score=0.866 recalls=0 avg=0.620 source=memory/2026-07-30.md:284-286]
<!-- openclaw-memory-promotion:memory:memory/2026-07-30.md:289:291 -->
- 第三步｜處置: ✅ 不自動修復（overloaded 是服務端暫時問題，非設定問題）; ✅ 不通知教練（CE=1 < 3，未達紅線）; ⏰ 下次 8:30 再觀察，若仍 overload 則 CE=2、仍<3；若 9:00 仍失敗則 CE=3 → 通知教練裁決 [score=0.866 recalls=0 avg=0.620 source=memory/2026-07-30.md:289-291]
