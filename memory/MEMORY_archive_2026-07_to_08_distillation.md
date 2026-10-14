# MEMORY.md 封存：2026-07～08 每週蒸餾（2026-10-14 搬出）

> 原因：MEMORY.md 超過小龍蝦開機檔 2 萬字上限，尾段被截斷。內容一字未改搬到這裡，需要時讀這份。

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


