- [Browser no full junction](feedback_browser_no_full_junction.md) — 瀏覽器絕不整個 junction，只搬書籤等增量檔案
- [跨機備份 SOP 提醒](feedback_cross_machine_backup_reminder.md) — 教練新電腦（含佩佩老師那台）要做增量備份（junction 搬家）時主動提醒，引用試金石 W03 完整生命週期 SOP
- [OpenClaw spool stuck fix](project_openclaw_spool_stuck_fix.md) — VPS 小龍蝦訊息卡住：檢查 .processing 檔案並清除即可修復
- [OpenClaw polling restart loop](project_openclaw_polling_restart_loop.md) — VPS 小龍蝦 health-monitor 持續 restart loop：spool 為空 + log 每 15 分鐘 restart + getMe 現在通，docker restart container 就好（別用 openclaw gateway restart，容器內會踩 service disabled 雷）
- [ACER post-restore TODO](project_acer_post_restore_todo.md) — 一鍵還原後開工時必須主動提醒執行還原步驟
- [VPS 連線資訊](reference_vps_connection.md) — 小龍蝦與赫茲米 VPS 的 IP/帳密/指令，任何電腦都能直接連
- [先問再改](feedback_ask_before_reversing_unusual_config.md) — 發現軟體設定跟預期不同，先問是不是教練故意的，別自己當錯誤修正
- [5月還原大測試](project_may_2026_restore_test.md) — C槽退回5月+6套軟體重裝+D槽junction重接的完整SOP
- [ACER 分割區調整後D槽清理待辦](claude-brain/project_acer_c_d_cleanup_20260708.md) — 觀察期至少到2026-07-11~15，教練確認無異常後才能刪除D槽Eassos舊備份（36.3GB）

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

## Promoted From Short-Term Memory (2026-07-26)

<!-- openclaw-memory-promotion:memory:memory/2026-07-17.md:282:282 -->
- 🚗 8036 車貸繳費資訊（教練原話）: > 「我的8036車號的車貸，我溢交四個月的費用，所以下次交費是12月1日。」 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-17.md:282-282]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:13:16 -->
- 常見錯誤自動修復：: **1. timeout 錯誤（lastDurationMs ≈ timeoutSeconds）：** → 表示腳本本身正常，但 timeoutSeconds 設定太短 → 使用 `cron update <jobId> --patch '{"payload":{"timeoutSeconds":300}}'` 將 timeout 改為 300秒 → 注意：不要改 06:00 海餅乾精神背誦（60秒即可） [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-18.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:18:19 -->
- 常見錯誤自動修復：: **2. scp/ssh 同步到 VPS 逾時：** → 改用 `rsync -e 'sshpass -p 9kdxvQN2 ssh' --p [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-18.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:5:5 -->
- 📨 對話記錄 00:19（共約 1 條，從第 0 行起）: 👤 教練：[cron:46e67e2e-6332-4589-aae2-ee7e10dd7279 🦞 每30分鐘任務健康檢查] 你是健康檢查助理。安靜執行以下檢查並自動修復，不需要通知教練（除非發現無法自動修復的嚴重問題）： [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-18.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-18.md:9:9 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openclaw cron list` 或 cron tool 檢查所有任務的 consecutiveErrors 與 lastStatus。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-18.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:328:340 -->
- 📊 VPS 小龍蝦（對外體驗版）活躍用戶盤點（2026-07-20 教練原話）: > 「我問一個問題，就是我們的 VPS 版小龍蝦，你能否知道現在活躍的用戶有哪些？我知道其中有一個叫 East 的用戶⋯」 → 小龍蝦 SSH 到 43.245.60.200 實測查到 8 個 agent（1 main + 7 trial），最近一週（2026-07-13 之後）還在用的只有 3 個：(1) **杉榕 陳** trial-8626705510（心好公益平台創辦人，業務「您消費，我捐錢」，heartgood.lovable.app）；(2) CHIU YuJung trial-8364394153（一般體驗用戶）；(3) 8820573555（測試/剛接觸）。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-20.md:328-340]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:457:476 -->
- 🗣️ 語音糾偏慘痛教訓「East」四次才搞對（2026-07-20）: 教練語音說「East」，小龍蝦：(1) 先猜 Esther（語音諧音，方向走偏）；(2) 又翻到杉榕陳 7/4 上傳 17 張圖就改猜杉榕陳；(3) 教練糾正「不是山姆/大A三姆，是 Easter，提到安東尼·羅賓」，小龍蝦又挖 Esther 7/14 session 上傳 21 張安東尼·羅賓圖卡確認 Easter=Esther；(4) 教練第三次糾正「不是這『三』，是『杉林溪』的『杉』」，小龍蝦才恍然大悟。**教訓**：語音諧音不要硬湊外國名字，先確認中文同音（杉→三→East 全是 s 開頭）。Easter 是錯的，Esther 也是錯的，最後答案是「杉」。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-20.md:457-476]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:511:529 -->
- 🔴 VPS 小龍蝦記憶搜尋功能實測結果（壞消息，2026-07-20，教練原話）: > 「如果資料存放了一個外部署或兩個月，當我們這些『vps 小龍蝦』的用戶想要搜尋過去的對話紀錄，是否也都能找得到？⋯小龍蝦目前的記憶搜尋功能，是不是處於一種最佳的狀態？」 → 小龍蝦實測結果：VPS 蒸餾記憶庫 chunks 僅 103 條（只到 5/7，**停了 73 天**）；VPS trial-8970866856（Esther）SQLite 0 條 chunks；VPS trial-8626705510（杉榕陳）SQLite 0 條 chunks。**結論：VPS trial 用戶完全沒有記憶搜尋能力**；Mac 主機雖有 4,228 chunks 也卡了。已派軍師 Task ID `20260720-084757` 找出 73 天停止真因，4 個推測根因：memsearch provider、模型切換、trial 路徑、cron 失敗；4 個改進方案 A/B/C/D 請軍師評估優先順序。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-20.md:511-529]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:756:777 -->
- 📮 軍師任務派遣（2026-07-20 教練原話）: > 「你寫一封信給蘋果電腦的軍師，問他一下這個問題怎麼解決？」 → 小龍蝦派出 Task ID `20260720-084757` 給軍師，要求用 `claude -p` 執行、SSH 到 VPS（密碼見路徑大全）、找出 73 天停止的真因，再回 Telegram 給教練。小龍蝦這邊會自動讀 `state/JUNSHI_TASK_RESULT` 結果。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-20.md:756-777]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:686:719 -->
- 💡 心好公益平台業務模式（杉榕陳 trial-8626705510，2026-07-20）: 杉榕陳的業務是 **心好公益平台**（heartgood.lovable.app），口號是「**您消費，我捐錢**」。7/4 那 17 張圖不是教材，而是**教店家導入這套銷售模式的整套行銷視覺系統**（立牌設計 / 玻璃門 LOGO + QR Code / 屋頂招牌 / 合作夥伴合影 SOP 等 4 條主線）。7/14 Esther 21 張圖則是 **安東尼·羅賓「21 步驟公眾銷售演說成交術」**（5 大區塊：開場 → 鋪墊 → 痛點 → 解方 → 成交；三條成交曲線：情緒、信任、價值）。已存到 VPS workspace 供教練參考。 [score=0.876 recalls=0 avg=0.620 source=memory/2026-07-20.md:686-719]

## Promoted From Short-Term Memory (2026-07-29)

<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:13:16 -->
- 常見錯誤自動修復：: **1. timeout 錯誤（lastDurationMs ≈ timeoutSeconds）：** → 表示腳本本身正常，但 timeoutSeconds 設定太短 → 使用 `cron update <jobId> --patch '{"payload":{"timeoutSeconds":300}}'` 將 timeout 改為 300秒 → 注意：不要改 06:00 海餅乾精神背誦（60秒即可） [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-20.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:18:19 -->
- 常見錯誤自動修復：: **2. scp/ssh 同步到 VPS 逾時：** → 改用 `rsync -e 'sshpass -p 9kdxvQN2 ssh' --p [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-20.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:5:5 -->
- 📨 對話記錄 00:50（共約 1 條，從第 0 行起）: 👤 教練：[cron:46e67e2e-6332-4589-aae2-ee7e10dd7279 🦞 每30分鐘任務健康檢查] 你是健康檢查助理。安靜執行以下檢查並自動修復，不需要通知教練（除非發現無法自動修復的嚴重問題）： [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-20.md:5-5]
<!-- openclaw-memory-promotion:memory:memory/2026-07-20.md:9:9 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openclaw cron list` 或 cron tool 檢查所有任務的 consecutiveErrors 與 lastStatus。 [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-20.md:9-9]
