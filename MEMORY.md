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

## 2026-08-09 weekly distillation batch（cron auto-processed）

<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:full -->
- 📦 **memory/2026-08-02.md 龐大週檔處理**（2026-08-09 cron 處理 1 個檔案，73392 bytes → 18040 bytes 截短版 + 歸檔）：
  - **內容性質**：週六整天高密度對話，主要議題 = (1) 教練追查每月 $10 美金刷卡；(2) v3.0 silence count 第三次糾正 + 防呆機制建置（已在他次晉升）；(3) 20 天工作坊邀請信提醒 cron 建置；(4) 健康檢查 cron + dreaming reflection meta-noise。
  - **不重複晉升**：v3.0 silence count（已在 MEMORY.md 開頭條目）、cron 健康檢查 SOP（已在 SOP 段落）、dreaming reflection candidates（NO_NEW_ENTRIES 級別，meta-noise 不晉升）。

<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:393:420 -->
- 💵 **OpenCode Go = 教練唯一真正的 $10/月美金訂閱**（2026-08-02 追查結果）：
  - 教練 2026-05-31 親自下單 `brew install --cask opencode-desktop`，Anomaly 同日開立首張發票（Stripe 收據 #2354-7682）
  - 首月 50% off = **$5**，原價 **$10/月**（其他 Netlify $9、Coze 3 次扣款全失敗皆不符）
  - ⚠️ 6/27 15:03 那筆 $10.24 USD（台幣 NT$333，富邦卡）金額對不上 OpenCode Go $10，需後續從富邦 7 月對帳單（已寄 2026-07-20 21:45，Gmail msg 19f7fc61b94ad9d6）確認商家英文名稱才能完全定論
  - 教練 2026-06-02 22:28 已把 `opencode-go` 加入 `/model` 選單；2026-06-06 14:56 設定「流量 open go」指令

<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:50:52 -->
- 💳 **教練的兩張信用卡 · 千萬不要再搞混**（2026-08-02 教練明示糾正）：
  - **玉山 Pi 信用卡**（5242-XXXX-XXXX-0043）—— **主要台幣消費用**（2026-06 月帳單看到 6/7 全支付 $39,800、6/11 桂田酒店 $13,800、6/25 中華電信 $50 都是台幣）
  - **台北富邦信用卡** —— **美金刷卡的應該是這張**（每月 20 號左右收到對帳單，富邦 7 月帳單已於 2026-07-20 21:45 寄出）
  - 8/2 教練糾正：「**富邦銀行**」（不是玉山），美金刷卡查詢都從富邦開始

<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:115:117 -->
- 📧 **Email OAuth 現況（2026-08-02 確認）**：
  - `bymyway7@gmail.com` ✅ **已授權 gog** —— 主信箱，可用 `gog` 工具查所有信件
  - `seabiscuitclub@gmail.com` ❌ **未授權 OAuth** —— 小龍蝦查不到，要教練跑 OAuth 授權流程（`gog auth add` + `export GOG_CREDENTIALS_FILE=...`）才能代查
  - 工具失敗記錄：`gmail.py` 互動式 stdin 命令遇到 `json.load` 解析錯誤（exitCode=1），推測 gmail.py 不支援互動 stdin
  - 富邦網銀登入頁面（`fbmbill.taipeifubon.com.tw`）需身分證+民國生日+驗證碼，無法直接讀

<!-- openclaw-memory-promotion:memory:memory/2026-08-02.md:1025:1040 -->
- 🔔 **20 天工作坊邀請信提醒 cron · 已上線**（2026-08-02 12:53 教練下令建置）：
  - 起點：**2026-08-02 22:20**（今晚台北時間）→ 終點：**2026-08-21 22:20**
  - 共 **20 個一次性 cron**（`deleteAfterRun: true`），跑完自動清掉不堆在排程清單
  - 每天 22:20 推播「今天要發 50 封工作坊邀請信 (N/20)」
  - 最後一天（8/21）會加一句「恭喜完成連續 20 天寄信任務」幫您打氣
  - 已刪除舊的 12:10 提醒（教練本來要中午推，但 8/2 中午 12:10 該推沒推，教練糾正後改為晚間 22:20）
  - 教練原話（8/2 12:53）：「晚上 10:20 通知我寄 50 封邀約工作坊的信，每天提醒，提醒 20 天」

<!-- openclaw-memory-promotion:procedures:memory_distill_weekly_v3:spec -->
- 🛠️ **memory_distill_weekly cron SOP v3 觀察**（2026-08-09 跑後補註）：
  - 200 行截短對一般對話檔已足夠（73392 → 18040 bytes，遠低 30KB 紅線）；若未來某檔 200 行仍 > 30KB，需改用 awk 控制 bytes 而非行數（沿用 v2 SOP）
  - 週檔若 v3.0 silence count 之類鐵律已在 MEMORY.md 開頭晉升過，weekly batch 不重複晉升，只記歸檔摘要
  - 萃取判定：note-taker meta-noise / dreaming reflection / cron 自動健康檢查對話 → 不晉升；教練原話 + 信用卡/Email/排程類結構性事實 + commit hash → 晉升

## Promoted From Short-Term Memory (2026-08-16)

<!-- openclaw-memory-promotion:memory:memory/2026-08-08.md:325:327 -->
- 第零步：🔴 v3.0 鐵律 — 教練最後訊息時間真相源（2026-08-02 教練拍板）: exit 0 → state 已用 Telegram API 真實時間回寫; exit 1 → 手動從 memory/最新檔撈，禁止沿用舊 `coachSilentHours`; exit 2 → TELEGRAM_BOT_TOKEN 沒設，記到 HEARTBEAT 待辦，下次跑前手動處理 [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-08.md:325-327]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08.md:329:329 -->
- 第零步：🔴 v3.0 鐵律 — 教練最後訊息時間真相源（2026-08-02 教練拍板）: 跑完才開始下面的檢查。所有寫到回報的「教練沉默了 N」必須是當下 `date` 算的新鮮值，**絕對不可用 state 裡面的舊值**。 [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-08.md:329-329]
<!-- openclaw-memory-promotion:memory:memory/2026-08-08.md:333:333 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openc [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-08.md:333-333]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09.md:267:267 -->
- 📨 對話記錄 07:25（共約 1 條，從第 0 行起）: 👤 教練：[cron:46e67e2e-6332-4589-aae2-ee7e10dd7279 🦞 每30分鐘任務健康檢查] 你是健康檢查助理。安靜執行以下檢查並自動修復，不需要通知教練（除非發現無法自動修復的嚴重問題）： [score=0.854 recalls=0 avg=0.620 source=memory/2026-08-09.md:267-267]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09.md:271:271 -->
- 第零步：🔴 v3.0 鐵律 — 教練最後訊息時間真相源（2026-08-02 教練拍板）: **每次開工第一步**先執行： [score=0.854 recalls=0 avg=0.620 source=memory/2026-08-09.md:271-271]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09.md:273:273 -->
- 第零步：🔴 v3.0 鐵律 — 教練最後訊息時間真相源（2026-08-02 教練拍板）: bash ~/.openclaw/workspace/scripts/sync_coach_last_message.sh [score=0.854 recalls=0 avg=0.620 source=memory/2026-08-09.md:273-273]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09.md:275:277 -->
- 第零步：🔴 v3.0 鐵律 — 教練最後訊息時間真相源（2026-08-02 教練拍板）: exit 0 → state 已用 Telegram API 真實時間回寫; exit 1 → 手動從 memory/最新檔撈，禁止沿用舊 `coachSilentHours`; exit 2 → TELEGRAM_BOT_TOKEN 沒設，記到 HEARTBEAT 待辦，下次跑前手動處理 [score=0.854 recalls=0 avg=0.620 source=memory/2026-08-09.md:275-277]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09.md:279:279 -->
- 第零步：🔴 v3.0 鐵律 — 教練最後訊息時間真相源（2026-08-02 教練拍板）: 跑完才開始下面的檢查。所有寫到回報的「教練沉默了 N」必須是當下 `date` 算的新鮮值，**絕對不可用 state 裡面的舊值**。 [score=0.854 recalls=0 avg=0.620 source=memory/2026-08-09.md:279-279]
<!-- openclaw-memory-promotion:memory:memory/2026-08-09.md:283:283 -->
- 第一步：檢查 Cron 任務失敗記錄: 使用 `openc [score=0.854 recalls=0 avg=0.620 source=memory/2026-08-09.md:283-283]

---

<!-- openclaw-memory-promotion:memory:memory/2026-08-14.md:3:181 -->
- 🏗️ **event.bymyway.com 報名通知系統真相（2026-08-14 教練深夜追查結果）**：
  - **教練原問題（00:13 終端機）**：「請幫我完成『有人報名，我的 LINE 就可以收到通知』這個功能」
  - **真相**：實際走 Telegram Bot API，不是 LINE Notify。教練以為是 LINE 通知，但實作是「通知到小龍蝦（Telegram）」，命名落差。LINE Notify token recall 搜不到也合理——因為根本沒用。
  - **完整技術棧**：Python Flask + Cloudflare Tunnel + Telegram Bot API 三件套
    - Flask 後端：`/Users/bymyway/.openclaw/workspace/event-signup/app.py`（最後修改 2026-08-10，23,438 bytes，預設 port 5060）
    - Cloudflare Tunnel：`event-app`（與 line-bot-relay、card-share 獨立）
    - 推播機制（app.py 第 57 行附近）：透過 Telegram Bot API 把「📋 新報名通知」送到教練 chat_id `6124913915`
  - **軍師做的時間軸**：
    - 2026-07-12 18:41 event-signup 目錄建立
    - 2026-07-12 21:07 切到 `event.bymyway.com/line/`（LINE 端點）
    - 2026-07-28 00:14 第一筆「📋 新報名通知」送達（魏淑華）
    - 2026-07-28 00:21~22 連續 3 筆（潘作薇、侯小姐、林群翔）
  - **教練原話（8/14 00:49 終端機）**：「event.bymyway.com 這套系統也是你去幫我建的，在建置的過程當中，你多次要求我登入這個雲端的帳號，cloudflared 通道這也是你去做的」
  - **未完成（教練原始問題的延伸）**：佩佩老師（贏家思維）LINE 群發權限——現有機制只推 Telegram 個人 chat_id，教練要的 LINE OA multicast/push 還沒做（教練確認才開工）

<!-- openclaw-memory-promotion:memory:memory/2026-08-14.md:104:112 -->
- 🗣️ **教練問「是不是軍師做的？跑了哪個程式？」的回答 SOP（2026-08-14 教練明示）**：
  - **要的是**：具體技術棧 + 檔案 + 程式碼佐證（行號、函數名、路徑）
  - **不要**：模糊的「是的 / 不是的」
  - **找不到程式碼佐證時**：直接讀 `app.py` 等源碼比 recall.py 更快（程式碼本身就是最權威的「實作證據」）
  - **教練糾正訊號**：「宕機了就不會自己回復嗎？這麼被動？」→ 中途不能空窗，必須持續回報進度；「你到底可不可以正常工作了？」→ LINE 對話 session 失憶直接觸發

<!-- openclaw-memory-promotion:memory:memory/2026-08-14.md:113:128 -->
- 🌐 **cloudflared 通道家族（2026-08-14 盤點 · 三條獨立 tunnel）**：
  - `event-app`：event.bymyway.com 報名系統
  - `line-bot-relay`：LINE 通道
  - `card-share`：名片通道
  - 三條獨立運作，設定檔在 `~/.cloudflared/event-config.yml`
  - ⚠️ 「LINE 通知」的命名落差：event 系統裡的 LINE 端點（`event.bymyway.com/line/`）≠ 推播到 LINE OA；實作是推到 Telegram chat_id 6124913915
