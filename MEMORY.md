- [Browser no full junction](feedback_browser_no_full_junction.md) — 瀏覽器絕不整個 junction，只搬書籤等增量檔案
- [跨機備份 SOP 提醒](feedback_cross_machine_backup_reminder.md) — 教練新電腦（含佩佩老師那台）要做增量備份（junction 搬家）時主動提醒，引用試金石 W03 完整生命週期 SOP
- [OpenClaw spool stuck fix](project_openclaw_spool_stuck_fix.md) — VPS 小龍蝦訊息卡住：檢查 .processing 檔案並清除即可修復
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

## Promoted From Short-Term Memory (2026-07-12 weekly distillation batch)

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:174:210 -->
- 🔴 P0 執行教訓（2 點半）：說了「立即修」沒真正 commit 就算沒做＝守則 #05 反面教材。執行過程沒每輪回報 Context %＝違反 HEARTBEAT.md 規定。執行中沒對照特助心法＝守則 #19 失職。教練原話：「每一輪你都要回報 context 百分之多少，為什麼你沒有回報呢？你在執行的過程當中，有時時刻刻對照『特助心法』嗎？」

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:294:364 -->
- 🦞 B 方案執行盤點（2026-06-04 02:20）：教練最終選 B「建立自動化流水線」，已具備組件：`scripts/fix-p0-findings.sh`、接力棒計劃（CONTEXT_OVERFLOW 版）、P0-4（自動 commit）已執行 `db88192a`。P0-1 原本假設「memsearch 會造成問題」是錯的——`memorySearch.provider = "memsearch"` 是預設值、實際正確。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:888:988 -->
- 🛠️ CRON 模型名稱格式教訓（試金石案例 006）：CRON isolated session 的 `payload.model` **只能寫純 ID**（如 `claude-opus-4-8`），**不能用顯示名稱**（`claude/Claude Sonnet`、`Claude Sonnet`、`claude/Claude Opus` 都會報 `Unknown model`）。6 次失敗嘗試全部記錄在試金石。Commit: `2ebc84ee`。SOP：新增 CRON 後**必須馬上手動觸發驗證**，不能等下次自動跑才發現錯。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:1494:1574 -->
- 🔴 緊急修復：模型鎖死 Opus 導致 Context Overflow 斷檔（17:30）：教練下令「除非手動更新模型，否則選擇哪一個就必須執行哪一個」。根因：commit `1d774d6` 把 main agent 永久鎖定 Opus，教練後來 `/model` 切到 M3，但 runtime `default_model` 跟 settings 沒同步 → context overflow 重啟時被拉回 Opus。修復：直接編輯 `openclaw.json`（先備份），確認 gateway 熱重載看到新值。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:1782:1832 -->
- 📜 海餅乾心法版權策略落定：採用 **CC BY-ND 4.0 創用 CC 姓名標示-禁止改作** 授權。白話：別人可以分享/轉載/列印/引用/標明出處散播；不可以改內容（變成「海餅乾心法 2.0」）、不可以截掉署名、不可以拿去做營利商品（要另外談）。落地三步：(1) 三個 repo 根目錄放 `LICENSE` 檔、(2) 每個重要 .md 頂部加版權頭、(3) 對外網頁加浮水印。Commit: `f7509728`（LICENSE 新增）、`f403508f`（WISDOM_CORES.md 標頭）。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:1882:2012 -->
- 🛡️ 教練原創舉證包（最強武器）：第一層鐵證——`shared-relay/bot_chat_2026-02-25_result.json`（11.6 MB Telegram 官方匯出，**不可竄改**）5,540 筆訊息、2,279 筆是教練親發（41%），發送者 ID `user6124913915` 與教練 Telegram Chat ID 完全一致。關鍵字密度：「海餅乾」1,797 次、「大樹教練」5,133 次、「十大守則」228 次、「三大信念」300 次。第二層鐵證：8 個核心檔 GitHub commit hash + GitHub 連結（任何人可驗證）。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:2046:2112 -->
- 💰 特助心法商業價值評估（守則 #16 應用）：教練「西洋棋比喻」＝**規則比棋手重要**＝21 條特助心法 + 海餅乾十大守則 ＞ 模型本身。給 AI 完善規則書，便宜模型（MiniMax）也能跑出世界級輸出（OPU 品質）。4 面向評估年化潛在天花板：**保守 NT$ 900 萬、樂觀 NT$ 3,800 萬**（知識產品線、B2B AI 導入、SaaS 訂閱、品牌聯名出版演講）。

<!-- openclaw-memory-promotion:memory:memory/2026-06-04.md:2151:2186 -->
- 🛠️ 蒸餾系統 C 選三件齊全落地（23:57 完成）：(1) 讀得到——強制重蒸餾卡 1 天的 `b701cc5f`（6/3 16:30 重新萃取後狀態檔沒更新，永久靜默跳過）。產出 `distill/terminal_2026-06-04.md` 905 bytes。(2) 自動觸發——原本 cron 就健康（每 30 分鐘），問題在腳本邏輯。(3) 犯錯自動入庫——修 `distill_terminal_llm.py`（偵測重新萃取自動強制重蒸餾，比對 mtime + size），新增 `distill_watchdog.sh`（每 15 分鐘掃 pending >2 小時 → 推 Telegram）。**根因教訓**：狀態檔記「已蒸餾」+ 重新萃取後狀態沒更新 = 永久靜默跳過 = 1 個月都不會有人發現。

<!-- openclaw-memory-promotion:memory:memory/2026-06-05.md:9:60 -->
- 🛠️ Hermit 桌面版「Always allow」解法：教練痛點——Hermit 桌面版 App 執行 Python `-e/-c` 每次跳「Always allow this command?」對話框。處理：備份 `~/.hermes/config.yaml` → `command_allowlist` 從 1 條擴充為 5 條（`python3 -e *`、`python3 -c *`、`python3 /Users/bymyway/.openclaw/**`、`python3 /tmp/**`）。守則 #16 應用：複雜的解法不一定是正確的解法（先解釋 macOS 安全機制 + 提三方案讓教練選 A）。

<!-- openclaw-memory-promotion:memory:memory/2026-06-05.md:60:106 -->
- 🤖 capability-evolver 第二次跑結果（軍師接手執行）：信號總數不變 6 個但**品質升級**（tool_bypass/repeated_tool_usage → user_feature_request/protocol_drift）。**Gene priority 0.667 → 0.800（+0.133）**，證實 MEMORY.md 餵法有效。MEMORY.md 從 11462 → 14757 bytes（多了 3,295 bytes），多了「📚 歷史素材索引（capability-evolver 專用）」區。下次迭代建議：加 cool-case 21 案例精煉摘要、加 failure-case-handbook 摘要、加 Top 10 errors 動態排名、單次別餵太多避免信號衝突。對比報告：`distill/evolver_run_compare_2026-06-05.md`，commit `01ca8def` / `40b4fe93`。

<!-- openclaw-memory-promotion:memory:memory/2026-06-05.md:388:507 -->
- 🔧 cron 模型自動同步機制建立：教練發現 9 個啟用 + 3 個停用 cron 全部仍寫 M2.7（已升 M3）。修法：(1) `scripts/sync_cron_models.sh` 讀 `~/.openclaw/openclaw.json` 的 main agent 模型，逐一比對所有啟用 cron `payload.model`，不一致就 `openclaw cron edit` 改掉。(2) 新 cron「🔄 cron 模型自動同步（每小時）」（id: `232918fb`）— 每小時 0 分自動跑，有變動才通知教練。**SOP**：下次升級到 M3.5/M4 只要教練改 `openclaw.json` 那一行，同步 cron 會自動更新其他任務。

<!-- openclaw-memory-promotion:memory:memory/2026-06-05.md:507:605 -->
- ☀️ 每日 06:00 起床摘要機制（commit `12973213`）：`scripts/morning_digest.sh` + cron 每天 06:00 掃前 12 小時 git commits，過濾掉 3 類自動備份（`auto-backup`、`[auto]`、`auto:`），剩餘列成 5-10 行摘要。**沒事就安靜**（純備份 cron 不叫教練），有事才推 Telegram。當下實測：35 commits → 過濾 25 個 auto → 剩 8 個值得看。

<!-- openclaw-memory-promotion:memory:memory/2026-06-05.md:605:753 -->
- ⚠️ 安全設定盤點（教練原以為有「只准本人下關鍵指令」）：實際掃 `openclaw.json` 後——`groupPolicy` 全部是 `"open"`、`groupAllowFrom` / `trustedUsers` 完全沒有、群組 `requireMention: false`。**真正有的防護**：(1) DM 只接收教練一人 chat_id 6124913915、(2) LINE 私訊是 "pairing" 模式、(3) 群組身份 hook 只判斷學長/學弟/學妹。教練回：「這個群組都是我的人，沒有風險」→ 收回 5 critical 警告。教練**真正擔心的是 LINE 群組**——但目前 LINE 群組沒在 OpenClaw 內。

<!-- openclaw-memory-promotion:memory:memory/2026-06-05.md:753:802 -->
- 📚 教訓上傳 SOP（守則 #07 應用）：教練說「納入自動學習」→ 寫入 `distill/failure-case-handbook.md` 案例 S（commit `80fb3ddb` / `50b12c13` / Deploy `6a22e040e17acd506b5bd447`）。教訓：問題定位 > 解法（X 太寬要分外框 vs 內部文字）、簡潔 = 對的（`max-width: fit-content; margin: 0 auto;` 一行就解決）、教練說不做就停。

<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:478:507 -->
- 📺 YouTube 31 頻道每日新片掃描 cron 救回路線（19:30 軍師 Opus 4.7 完成）：試跑 `fetch-youtube-rss.py --days 2` → 抓到 17 部新片（31 頻道，1 個失效 AI-Short-Taipei 404）。寫入 Hermes cron：ID `0863a681ec18`、名稱「📺 YouTube 31 頻道每日新片掃描（7:30）」、排程每天 7:30 台北時間（教練起床時段）、Model minimax/MiniMax-M3（零 token 成本）、Deliver telegram coach。**失敗靜默規則**：腳本失敗 → 「📺 今日無新片」一句話，禁推 traceback / FailoverError。SIGHUP gateway → launchctl 自動重啟（新 PID 12026）→ 新 jobs.json 已生效。待觀察：明早 7:30 看是否成功推播到教練 Telegram。

## Promoted From Short-Term Memory (2026-07-16)

<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:13:16 -->
- 📨 對話記錄 02:47（共約 62 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：[assistant turn failed before producing content] 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：[assistant turn failed before producing content] [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-07.md:13-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:17:20 -->
- 📨 對話記錄 02:47（共約 62 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：[assistant turn failed before producing content] 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK [score=0.886 recalls=0 avg=0.620 source=memory/2026-07-07.md:17-20]

---

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
