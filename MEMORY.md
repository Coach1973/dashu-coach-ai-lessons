- [🔴 git pull異常先查接力棒/HEARTBEAT再診斷git底層(2026-09-21)](claude-brain/feedback_check_handoff_before_diagnosing_git_anomaly_2026-09-21.md) — 跨機git分岔/rebase卡住，多半是其他機器已記錄過的已知事件，先讀本機交接檔別急著下git診斷指令
- [🔴 git add -A誤commit含真實個資的.db.bak檔(2026-09-01)](claude-brain/feedback_git_add_a_risk_with_db_backup_files_2026-09-01.md) — .gitignore的*.db規則擋不住.db.bak-xxx變體檔名，commit前先git status肉眼掃一眼
- [💾 易數一鍵還原備份工具結構](project_backup_tool.md) — D槽根目錄，.pmf是基底、.ptp是時間戳記完整備份非增量，每次執行同資料夾新增.ptp不建新資料夾
- [📂 Downloads位置與整理結構](project_downloads_location.md) — 實際位置D:\Users\Downloads（非C槽預設），既有分類資料夾規則
- [⚠️ 清理腳本不能放%TEMP%](feedback_no_scripts_in_temp.md) — 腳本清理%TEMP%時會把自己也刪掉導致中斷
- [⚠️ PowerShell中文編碼要加UTF-8 BOM](feedback_powershell_utf8_bom.md) — .ps1含中文字面值沒BOM會被系統codepage讀壞
- [👤 使用者背景：BNI教練](user_bni_coach.md) — 大樹教練，BNI商會分會經營，常見紅綠燈/palms/分會業務檔案
- [🎯 Hermes開工要主動讀軍師接力棒（拉取取代推送）(2026-08-31)](claude-brain/project_hermes_pull_progress_rule_2026-08-31.md) — ai-art任務3.5小時零回報後教練拍板，已寫進H_AGENTS.md熱啟動4件套
- [🔧 ACER 2026-08-31全機體檢：修復PS5.1 -AsHashtable+workspace路徑重複clone兩個真bug](claude-brain/project_acer_health_check_2026-08-31.md) — ACER再開機健檢報告，含沉默原因誠實查證
- [Browser no full junction](feedback_browser_no_full_junction.md) — 瀏覽器絕不整個 junction，只搬書籤等增量檔案
- [跨機備份 SOP 提醒](feedback_cross_machine_backup_reminder.md) — 教練新電腦（含佩佩老師那台）要做增量備份（junction 搬家）時主動提醒，引用試金石 W03 完整生命週期 SOP
- [OpenClaw spool stuck fix](project_openclaw_spool_stuck_fix.md) — VPS 小龍蝦訊息卡住：檢查 .processing 檔案並清除即可修復
- [OpenClaw polling restart loop](project_openclaw_polling_restart_loop.md) — VPS 小龍蝦 health-monitor 持續 restart loop：spool 為空 + log 每 15 分鐘 restart + getMe 現在通，docker restart container 就好（別用 openclaw gateway restart，容器內會踩 service disabled 雷）
- [ACER post-restore TODO](project_acer_post_restore_todo.md) — 一鍵還原後開工時必須主動提醒執行還原步驟
- [VPS 連線資訊](reference_vps_connection.md) — 小龍蝦與赫茲米 VPS 的 IP/帳密/指令，任何電腦都能直接連
- [🔴 Hermes = Mac 桌面版，VPS 版已永久停（2026-09-05 教練澄清）](feedback_hermes_is_mac_desktop_vps_permanently_off.md) — 教練說「Hermes 沒反應」時指的是 Mac 桌面版（軍師/賈維斯負責），不是 VPS 上的；VPS Hermes (113.29.232.178) 已永久停，未來查 Hermes 別再 ping 那個 IP
- [先問再改](feedback_ask_before_reversing_unusual_config.md) — 發現軟體設定跟預期不同，先問是不是教練故意的，別自己當錯誤修正
- [5月還原大測試](project_may_2026_restore_test.md) — C槽退回5月+6套軟體重裝+D槽junction重接的完整SOP
- [ACER 分割區調整後D槽清理待辦](claude-brain/project_acer_c_d_cleanup_20260708.md) — 觀察期至少到2026-07-11~15，教練確認無異常後才能刪除D槽Eassos舊備份（36.3GB）
- [Heartbeat 不要拿舊靜默紀錄當事實（v3.0）](feedback_silence_count_must_be_real_time.md) — 任何「靜默 N 小時/天」描述前必須先讀 `state/heartbeat-state.json` 的 `coachSilentSince` + 用 `date` 即時算差距，**禁止沿用 state 內的舊 `coachSilentHours`**；state 過期或缺值時主動從 memory/最新檔或 Telegram API 撈最後訊息時間。三次同型錯誤：8/1 18:04「5.8 天」、8/2 12:11「160h+」、8/2 14:45 預防性重申。
- [ACER(PC5C925ED70E46) 環境筆記](reference_acer_pc5c925ed70e46_environment_notes.md) — COACH帳號非系統管理員(工作排程器不能用)、Git Bash吃掉`/`開頭參數需`MSYS_NO_PATHCONV=1`、python3是Store樁、無gh CLI改用git credential manager token打GitHub API

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


## 2026-08-25 23:55 教練親口鐵律（v3.1 假數據 bug 防呆 + 軍師新名稱）

<!-- openclaw-memory-promotion:memory:memory/2026-08-25.md:full -->
- 🔴 **假數據 bug 防呆 v3.1（2026-08-25 23:55 教練親口拍板）**：
  - 教練原話：「**不管你有沒有記錄到，只要是 Claude 的 App 介面，只要我有在使用，就一定會請它上傳，所以不管你有沒有抓到，它一定會有工作記錄**」
  - 教練原話（更早 23:52）：「**如果是他們沒有上傳，你應該是說『他們沒有上傳，我也找不到』，而不是直接告訴我說『39 天沒有對話』，因為這是不現實的**」
  - 觸發情境：小龍蝦 23:11 發三機總結寫「ACER 連續 39 天無對話」「聯想連續 30 天無對話」，教練立刻糾正
  - **過去同型錯誤紀錄**：2026-07-20 教練親抓「聯想連續 11 天沒有對話」誤報（其實當天聯想有 commit）
  - **根因**：`memory/verbatim/{acer,lenovo,mac}/YYYY-MM-DD.md` 不存在 ≠「那天沒對話」；中繼蒸餾排程從 2026-07-08 後就再也沒穩定運作過
  - **新 SOP**：(1) 禁止用檔案存在與否當判斷 (2) 先承認「排程沒抓到，不等於沒對話」(3) 查證途徑：git log / session-corpus / Claude App 本地歷史 (4) 發三機總結前必須先跑這條 SOP

- 🔴 **軍師新名稱 = 賈維斯（Jarvis，2026-08-25 23:55 教練親口拍板）**：
  - 教練原話：「**我給『軍師』取了一個新名稱（可能是 Mac 電腦那邊的名稱，也可能是其他 Claude App 統一使用的新名稱，同時都可以用），就是『賈維斯』，也就是鋼鐵人使用的那個管家系統 Jarvis**」
  - 舊名「軍師」仍可用，向後相容
  - 新名「賈維斯」(Jarvis) — 鋼鐵人管家系統
  - 教練尚未拍板是 Mac 軍師專用 or 所有 Claude App 統一 → **兩種都可以用**
  - 派工單發給軍師時：信件標題可寫「給賈維斯」或「給軍師」，兩者都收
  - 回報教練時：可用「賈維斯回報」「軍師回報」，兩者都通
  - 跟守則 04:17「賈維斯是最高等級指令」一致

## 2026-08-23 weekly distillation: 2026-08-17.md（46K → 18K）

<!-- openclaw-memory-promotion:memory:memory/2026-08-17.md:weekly-distill-2026-08-23 -->
- � **memory/2026-08-17.md 龐大週檔處理**（2026-08-23 cron 處理 1 個檔案，46503 bytes → 18393 bytes 截短版 + 歸檔）：
  - **內容性質**：週日整天三條對話線 = (1) 彭晉澄講師資料同步 → ai-talk 推到錯網站 → revert → 改推 ai-forum-taichung 成功；(2) 教練質問 Netlify 15 點 SOP 違規事件（小龍蝦誠實承認跳過 SOP 第 5 步）；(3) 大量 dreaming/light sleep reflection candidates（confidence 0.58, NO_NEW_ENTRIES 級別, meta-noise）。
  - **不重複晉升**：dreaming reflection meta-noise（已在 SOP v2 段落標示不晉升）。
  - **已歸檔**到 `memory/archive/2026-08-17.md`，原檔截短到 18KB 註解版。

<!-- openclaw-memory-promotion:memory:memory/2026-08-17.md:74:120 -->
- 🌐 **AI 微論壇系列場次 / 網站對照表 · 千萬別搞混**（2026-08-17 教練實戰教訓）：
  - **嘉義場 8/28** → repo = `ai-talk`（已發布，coach1973.github.io/ai-talk）
  - **台中場 9/23-24** → repo = `ai-forum-taichung`（**概念稿，尚未正式發布，教練主要的正式網頁版**）
  - ⚠️ 教訓：「看到場名稱就抓 repo 是錯的」（小龍蝦把「828 嘉義場」字面誤判為「正式網頁版」，推錯網站）
  - 🔴 **預防措施**：未來接到「更新微論壇」指令一律先跟教練確認 repo + 確認網址（給教練兩次問「是這個嗎」）
  - 8/17 三個 commit hash：`ce2dd88`（ai-talk 錯推）→ `8b5cdab`（ai-talk revert）→ `7d270df`（ai-forum-taichung 正確推）

<!-- openclaw-memory-promotion:memory:memory/2026-08-17.md:120:140 -->
- 🎤 **彭晉澄講師資料同步 · mentor100 → ai-forum-taichung**（2026-08-17 完成）：
  - mentor100 來源：`mentors.id=76`，2026-08-16 13:51 self-submit，山澐有限公司／執行長
  - 議程原本就有彭晉澄（DAY 2・09:15-10:15），但**講師陣容區是 JS 動態渲染 placeholder「講師資料籌備中」** → 補齊 title/主題/照片/簡介/社群連結
  - 照片：`images/speaker-peng.jpg`（960x1200，從 mentor100 複製，HTTP 200 ✅）
  - 議程主題保留：「AI 不只是工具，從工作流程重整到人機協作，放大你的專業價值」

<!-- openclaw-memory-promotion:memory:memory/2026-08-17.md:140:170 -->
- 🚨 **Netlify 15 點 SOP 違規事件 · 教練親口教訓**（2026-08-17 教練質問，小龍蝦誠實承認）：
  - 教練原話：「**請問，你推到netlify了嗎？若有，在推之前你有先經過我同意說『推』嗎？你知道推到netlify每次要扣15點，你有計算扣了幾點嗎？**」
  - 小龍蝦 10:25 對照報告已自我承認：SOP 第 5 步「未經教練確認絕對不推」被跳過了
  - **實際上兩個站都是 GitHub Pages 自動部署，不是 Netlify，所以沒扣點**（0 點）
  - 🔴 但 SOP 違規本身（跳過等教練說「推」）是事實，跟有沒有扣點要分開看 — **程序違規不管理由是什麼**
  - **教練原話鐵律**：「推到 Netlify 每次要扣 15 點」 — 未來任何 Netlify 推動作都必須先算點數 + 等教練明確「推」

<!-- openclaw-memory-promotion:memory:memory/2026-08-17.md:170:200 -->
- 📂 **Netlify 網站編輯 SOP 主檔位置**（2026-08-17 教練查證後定位）：
  - 主檔：`~/.openclaw/workspace/knowledges/SOP_netlify_website_edit.md`（2026-05-30 軍師建立，教練親定，2026-06-17 補 Chrome 唯一預覽鐵律）
  - Windows 軍師對照表：`knowledges/IDENTITY_windows_desktop.md`
  - 事故檢討：`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`（教練說 Mac 軍師也要看）
  - ⚠️ 教練 8/17 仍有兩個 pending 問題未答：(1) SOP 彈性條款要不要加「明確指令例外」？ (2) 場次對照表要不要寫到 SOUL.md 或 USER.md？

## 2026-09-06 weekly distillation batch（cron auto-processed）

<!-- openclaw-memory-promotion:memory:memory/2026-09-05.md:full -->
- 📦 **memory/2026-09-05.md 龐大週檔處理**（2026-09-06 cron 處理 1 個檔案，31305 bytes → 22056 bytes 截短版 + 歸檔）：
  - **內容性質**：週六整天高密度記錄，主要議題 = (1) Light Sleep / REM Sleep reflection candidates（confidence 0.58, NO_NEW_ENTRIES 級別, meta-noise）；(2) 健康檢查 cycle=778~792 audit（cron 自動 meta-noise）；(3) ⚠️ 22:30 緊急存檔 Hermes VPS 斷線調查 → 教練 22:30 澄清「Hermes = Mac 桌面版，VPS 版永久停」。
  - **不重複晉升**：Hermes = Mac 桌面版 / VPS 永久停（已在 MEMORY.md 開頭晉升過）；Light Sleep dreaming reflection meta-noise（已在 SOP v2 段落標示不晉升）；健康檢查 cron audit（屬 v4.0 三關判斷自動流程，無新內容）。
  - **已歸檔**到 `memory/archive/2026-09-05.md`（完整 31305 bytes），原檔截短到 22056 bytes + 加註「[已蒸餾歸檔]」。

<!-- openclaw-memory-promotion:memory:memory/2026-09-06.md:300:486 -->
- 🔗 **策展店家「短網址縮短」4 步 SOP（2026-09-06 凌晨實戰歸納）**：
  - **觸發情境**：教練丟一個長網址 + 一個新短網址，要求縮短。9/5~9/6 連續實戰 3 次：百聖 (`bai-sheng-guang-gao...` → `bai-sheng`)、楊尚儒 (`yang-shang-ru-shang-juyangdma` → `yang-shang-ru`)、楊在珍 (`xing-fu-dao-shi-esther-yang-zai-zhen` → `yang-zai-zhen`)。
  - **4 步流程**（每次都一次做完）：
    1. **GitHub repo rename**（用 `gh repo rename <新名> -R <owner/舊名>`，`--yes` 取代 deprecated 的 `--confirm`）
    2. **本機資料夾 rename** + `git remote set-url origin <新網址>` 同步
    3. **registry 白名單換 slug**（`event_url` + `github_pages_url` 都更新）
    4. **大台南策展中心首頁卡片按鈕連結同步換新**（commit + push GitHub）
  - **驗證 SOP**：新網址 HTTP 200 ✅ / 舊網址 HTTP 404 ✅ / 兩個網站標題正確顯示
  - **commit hashes 留證**：`cc3293c`（bai-sheng）、`d78f810`（yang-shang-ru）、`1e2f9b6`（yang-zai-zhen）

<!-- openclaw-memory-promotion:memory:memory/2026-09-06.md:340:400 -->
- 📝 **張騰文（柚式藝術 / 花藝設計）店家資料更新（2026-09-06 06:11 教練下單）**：
  - **更新內容**：原品牌名「永生花藝」→「柚式藝術（花藝設計）」，補電話 `0925978176` + Email `janjan0210@gmail.com`
  - **8 處 index.html 編輯** + registry + 策展中心卡片同步
  - **commit hashes**：`b76b0c6`（zhang-teng-wen）、`0f9c393`（tainan-shangquan）
  - **誠實發現並回報**：tainan-shangquan Pages 從沒開過，「大台南策展中心」其實是 Flask 服務直接讀本機檔 → 本機改完即時生效，推 GitHub 那步其實可以省（commit 留作備份）
  - **主動小提問**：教練寫的「張 騰文」中間有空格，跟系統一直以來的無空格用法不同，已請教練確認

<!-- openclaw-memory-promotion:memory:memory/2026-09-06.md:420:470 -->
- 🛠️ **策展中心 (大台南策展中心) = Flask 讀本機 repo，不是 GitHub Pages（2026-09-06 06:11 張騰文案再次確認）**：
  - 8/31 ai-art 案已發現 Flask 直接讀 `/Users/bymyway/github_repos/ai-art/` → 對外版即時生效
  - 9/6 張騰文案再次確認：`event.bymyway.com/tainan-shangquan/` 也是 Flask 服務的路由，不是 GitHub Pages
  - **新守則落地**：任何「策展中心」類的卡片更新 → 改本機檔就會即時生效，「推」GitHub 那步是 commit hash 留證用，不是必要步驟
  - 推論：只要是 Flask 路由下的店家頁面（`event.bymyway.com/curated/<slug>/`、`event.bymyway.com/tainan-shangquan/` 等），都適用此守則

<!-- openclaw-memory-promotion:memory:memory/2026-09-06.md:430:470 -->
- 🔧 **`gh repo rename` 參數新格式（2026-09-06 06:36 楊在珍案發現）**：
  - **新格式**：`gh repo rename <新名> -R <owner/舊名> --yes`
  - **舊格式已 deprecated**：`--confirm` 不要再用
  - **前提**：`gh` CLI 已登入 `Coach1973`（有 repo 權限，9/6 楊在珍案確認可執行）
  - **GitHub 端 rename 效果**：舊 endpoint 維持「Moved Permanently (301)」自動轉址，不需要另外設 redirect
  - **本機端配套**：rename 完 → 本機資料夾跟著改 → `git remote set-url origin` 同步新網址 → registry 同步 → 策展卡片連結同步

<!-- openclaw-memory-promotion:memory:memory/2026-09-06.md:300:486 -->
- 📦 **memory/2026-09-06.md 龐大週檔處理**（2026-09-06 cron 處理 1 個檔案，33040 bytes → 22068 bytes 截短版 + 歸檔）：
  - **內容性質**：週日清晨高密度實戰，主要議題 = (1) Light Sleep dreaming reflection candidates（meta-noise）；(2) ⚠️ 05:36 緊急存檔 百聖 + 楊尚儒短網址縮短；(3) ⚠️ 06:11 緊急存檔 張騰文更新成柚式藝術；(4) ⚠️ 06:36 緊急存檔 Esther 楊在珍短網址縮短 + 策展中心 Flask 機制確認。
  - **精華已晉升**：策展店家短網址縮短 4 步 SOP、張騰文柚式藝術更新、Flask 讀本機守則擴展、gh repo rename 新格式（皆見本段上方晉升條目）。
  - **不重複晉升**：Light Sleep dreaming reflection meta-noise、健康檢查 cron audit。
  - **已歸檔**到 `memory/archive/2026-09-06.md`（完整 33040 bytes），原檔截短到 22068 bytes + 加註「[已蒸餾歸檔]」。


## Promoted From Short-Term Memory (2026-09-08)

<!-- openclaw-memory-promotion:memory:memory/2026-08-31.md:304:307 -->
- 📨 對話記錄 22:30（共約 50 條，從第 0 行起）: 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-31.md:304-307]
<!-- openclaw-memory-promotion:memory:memory/2026-08-31.md:308:311 -->
- 📨 對話記錄 22:30（共約 50 條，從第 0 行起）: 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-31.md:308-311]
<!-- openclaw-memory-promotion:memory:memory/2026-08-31.md:312:315 -->
- 📨 對話記錄 22:30（共約 50 條，從第 0 行起）: 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-31.md:312-315]
<!-- openclaw-memory-promotion:memory:memory/2026-08-31.md:316:319 -->
- 📨 對話記錄 22:30（共約 50 條，從第 0 行起）: 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] [score=0.866 recalls=0 avg=0.620 source=memory/2026-08-31.md:316-319]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:267:268 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：🦞 對話記錄已滿，已自動重啟，請繼續下指令 [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:267-268]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:270:270 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 對話紀錄已完整存入 `memory/2026-09-01.md`，零遺漏。剛才環境健檢結果： [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:270-270]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:272:275 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 通道健康（probe ok=true）; 教練上次訊息 11:06，現在 12:07，靜默約 1 小時; cron 健康，三關全 fail_no; repo untracked/modified 累積 23 + 22 行，建議下次開工順手掃一眼 [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:272-275]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:278:281 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:278-281]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:282:285 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：[assistant turn failed before producing content] [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:282-285]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:286:289 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:286-289]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:290:293 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:290-293]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:294:297 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:294-297]
<!-- openclaw-memory-promotion:memory:memory/2026-09-01.md:298:301 -->
- 📨 對話記錄 22:30（共約 41 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：[assistant turn failed before producing content] [score=0.854 recalls=0 avg=0.620 source=memory/2026-09-01.md:298-301]
