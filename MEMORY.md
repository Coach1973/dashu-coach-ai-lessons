- [🔴 Claude 額度燒光主因＝Claude Desktop 內建 worktree 分身，不是排程也不是 hook(2026-10-26)](claude-brain/reference_claude_desktop_worktree_quota_2026-10-26.md) — 教練在 Claude Desktop 打「開工＋時分」→ Desktop 自己 git worktree add → hook 注入接力棒 → 場次跨夜 → 94.9% 加權額度燒掉；查「誰發起的」必看首則 user 事件的 `userType=external`/`isMeta=null`/`hookEventName=null` 簽章
- [🔴 curation_check_result 回 found:false 不等於上架失敗，可能是「根本沒做」(2026-10-27)](claude-brain/feedback_curation_found_false_means_not_done_2026-10-27.md) — hsiuli 拖 23 天沒動就是這樣誤判；先分「上架失敗」vs「從來沒上過」（看 log 關鍵字＋incoming/processing/failed 三目錄），是後者就直接做；收件匣未結案信件＝待辦不是垃圾 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- [🔴 解析 HTML 清單頁前先剝掉 <script>，髒資料先查「髒在哪一層」(2026-10-27)](claude-brain/feedback_strip_script_before_html_parse_2026-10-27.md) — bni_tainan 行事曆 `${time}` 髒值根因是頁尾 JS 模板被當成活動內容；含 ~/.openclaw 推 master、workspace 推 main 的分支對照 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- [🔧 派工橋 claude -p 要加 --add-dir 才讀得到 github_repos(2026-10-25)](claude-brain/reference_junshi_bridge_add_dir_fix_2026-10-25.md) — 軍師卡關「For security, Claude Code may only list files in the allowed working directories」的根因就是沙盒只開 workspace；`scripts/junshi_task_worker.sh` 已加 `--add-dir /Users/bymyway/github_repos`（+ .claude-code/workspace + .openclaw/workspace），實測可列出 charles-lin 檔名 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- [🎙️ 教練語音諧音 BB / MM = MiniMax-M3(2026-10-17 拍板)](memory/reference_model_alias_bb_mm_minimax_2026-10-17.md) — 教練說 BB / MM / MiniMax / Minimax 一律當 MiniMax-M3 接，不要反問是哪個模型、不要提切換
- [🔴🔴🔴 「小龍蝦」≠「Hermes」，是這台Mac上兩套獨立Telegram系統(2026-09-22)](claude-brain/feedback_xiaolongxia_vs_hermes_different_systems_2026-09-22.md) — 故障診斷前先確認教練指的是哪個對話框顯示名稱，別憑印象套用上次查過的系統；process沒在跑比process卡住更隱蔽，先查launchctl state
- [🔴 EM 模式 = 1M context window，教練內部簡寫「e」= 數字「1」(2026-09-22)](memory/reference_em_mode_definition_1m_context_2026-09-22.md) — 不是 Extended Mode/Enterprise Mode；對應 model name [1m] 後綴、`--print` 測試 CTX=1000000、CLAUDE_CODE_AUTO_COMPACT_WINDOW=1000000；v227 完整機制：`claude-sonnet-5[1m]` 走 Anthropic 原生 OAuth → 真 1M
- [🔴 檔案「看起來重複下載」要刪先MD5比對(2026-09-21)](claude-brain/feedback_verify_before_deleting_assumed_duplicates_2026-09-21.md) — 不能只看檔名帶數字就當作重複，NotebookLM等工具匯出命名習慣本來就會帶數字
- [🔧 「BNI PPT SOP」＝PDF轉品牌底圖PPT流程簡稱(2026-09-21)](claude-brain/reference_bni_ppt_sop_alias_2026-09-21.md) — 教練喊這個詞直接對應SOP文件+腳本，不用重新解釋流程
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

## 📦 已封存的舊段落
- 2026-07-16、2026-08-09 每週蒸餾（含健康檢查 SOP）→ `memory/MEMORY_archive_2026-07_to_08_distillation.md`（2026-10-14 搬出，避免超過 2 萬字上限）

## 每30分鐘健康檢查 cron 常見錯誤自動修復 SOP（2026-07-10 整併，原本被自動晉升機制重複收錄4次)

> 這條內容是「每30分鐘健康檢查」cron 的固定操作手冊，不是單次對話的教訓，之前被自動晉升系統誤判成新知識、從07-02跟07-03的每日記憶檔各重複收錄一次。整併成一份，密碼也改指到憑證層。

1. **檢查 Cron 任務失敗記錄**：`openclaw cron list` 檢查所有任務的 consecutiveErrors 與 lastStatus
2. **timeout 錯誤**（lastDurationMs ≈ timeoutSeconds）：腳本正常，只是逾時設太短 → `cron update <jobId> --patch '{"payload":{"timeoutSeconds":300}}'` 改 300 秒（⚠️ 06:00 海餅乾精神背誦維持60秒不要改）
3. **scp/ssh 同步到 VPS 逾時**：改用 `rsync -e 'sshpass -p <密碼，見路徑大全_憑證層.md> ssh' ...`（原密碼明文已移除）

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


## Promoted From Short-Term Memory (2026-10-26)

<!-- openclaw-memory-promotion:memory:memory/2026-10-12.md:1:28 -->
- ## 02:12~02:38 約瑟布 v2 推圖（災難+修復紀錄） ### 任務 教練 01:51 下令：v2_01-40 共 40 張，但前 6 張重複，所以實際要跑 v2_07-40 共 34 張。 ### 過程失誤（鐵律二違規） 1. 教練已給清楚 if-else 條件「如果前 6 張重複了，就出剩下 34 張」，我多嘴問「要我馬上開跑嗎？還是要先看哪幾張停一下？」→ 違鐵律二「直接行動不問確認」 2. 用 background exec 一直被教練的訊息打斷 → 應一開始就 foreground 3. Gateway 中間重啟兩次，所有 background exec 全清空 4. 第三次醒來後用「撈磁碟 + 推 Telegram」路線完成 ### 最終結果 - 34 張全部 cache hit 存到磁碟（本次重跑 0 點） - 9 推 4+4+4+4+4+4+4+4+2 全送到 Telegram（messageId 12314-12346） ### 教訓 🔴 批量圖任務鐵律（記住）： - 「全部出圖」= 立即跑，不問確認 - 一開始就 foreground，不要 background - Gateway 重啟後第一件事是「撈磁碟 + 補推」，不要盲重跑 - lk888 cache 機制 24h 內免費重複回傳，重跑成本 0 ### 磁碟狀態 -... [score=0.604 signals=2 recalls=2 avg=0.509 source=memory/2026-10-12.md:1-28] <!-- trigger: gateway, v2-01-40, v2-07-40 --> <!-- importance: 6 -->

## 結繩領導學每日 LINE 行銷（2026-11-01 建置）
<!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- 🔧 **LINE 推播的 `to` 必須是 `^U[0-9a-f]{32}$`**：event.db 的 `line_user_id` 欄位混有使用者自填的 LINE 帳號 ID（Jerry、kksasa0430…），直接送會回 HTTP 400 `The property, 'to', in the request body is invalid`。名單建置時就要 regex 驗證並把不合格者回流到人工通道。 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- 🔧 **每日輪轉名單不可用「未發過」清單當索引基準**：有人被標記已發後清單縮減會造成索引位移、跳過沒發到的人。輪轉池要用全部候選 + `day_index * size` 取視窗，再濾掉已發。 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- 🔧 **LINE 月配額 200 則是硬上限，批次要按「成功 N 則」設計**：寫「取 N 位送 N 位」遇失敗就白耗名額；改成目標成功 N 則 + 失敗自動續下一位 + 最多嘗試 M 次。 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- 📌 **教練手機人脈的真實來源**：`namecard-db/namecards.db`（cards 466 張名片／451 手機、guests 3,222 來賓），加上 `event-signup/event.db` attendees（369／105 有 LINE ID）與 `jiesheng-report/jiesheng_report.db` registrants（29，含台北場 20 已報名）。本機 AddressBook 與 iCloud 通訊錄皆無資料，Mac 端拿不到 iPhone 同步的聯絡人。 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->
- 📌 **排程**：`每日12:15-結繩領導學LINE行銷`，cron `15 12 * * *` Asia/Taipei，command payload 跑 `scripts/jiesheng_daily_push.sh`（重建→開 10 分鐘推播許可→推播→撤銷→產手機名單→Telegram 回報）。commit `f642cbbba` 已 push 驗證。 <!-- project: github.com/Coach1973/mac-openclaw-workflows -->

## OpenClaw 訊息工具的本機媒體允許目錄（2026-11-01 實測）
- 🔧 **只有 `~/.openclaw/media/` 根層能被 `message` 工具讀取**。實測被拒（LocalMediaAccessError: path is not under an allowed directory）的位置：`~/.openclaw/agents/main/media/`、`~/.openclaw/agents/peipei/media/`、`~/.openclaw/media/store/`、`~/.openclaw/workspace/`、`~/.openclaw/media/peipei_out/`。
- 🔧 **`openclaw.json` 沒有任何媒體允許目錄欄位**（allowedDirs / mediaRoot / mediaStore 全查無），這是 OpenClaw 內建預設，不需設定；要傳本機圖給其他 agent 時，直接放 `~/.openclaw/media/` 根層。
- 🔧 **Telegram 群組遷移後 ID 會變**：佩佩老師群組 `-5115910257` 已遷移，真實 chat_id 為 `-1003877502911`。舊 ID 送會回 `chat not found`。
- 🔧 **`bot_main` 不在佩佩老師群組**，要投遞該群需用 `bot_peipei` 帳號；否則必定 `chat not found`（此錯誤是帳號/群組問題，不是路徑問題，不要誤判成媒體路徑錯誤）。
- 🔧 **另一個同樣被允許的媒體目錄：`~/.openclaw/media/tool-image-generation/`**（2026-11-01 由 3 號機實測、1 號機驗證）。與 `~/.openclaw/media/` 根層並列，同樣可被 `message` 工具讀取。分辨技巧：**「Local media file not found」代表目錄被允許但檔案不在；「path is not under an allowed directory」代表目錄被拒** —— 兩者語意相反，可用來快速判斷。
- 🔧 **`scripts/coach_schedule.py add` 沒有去重機制**（2026-11-01 實測）：直接 add 會在同一天同一時段產生第二筆重複行程，並讓可訪談時段計算錯亂（腳本只用 `data["events"]` append）。加入行程前必須先 `check --date` 並直接看 `knowledges/教練行程總表.json` 的 `events` 陣列，比對「時段＋參與者＋note」是否已被既有事件涵蓋。
- 🔧 **兩種媒體錯誤的語意差異（2026-11-01 實測，重要）**：「Local media file not found」＝ 路徑通過允許目錄檢查、但**檔案在該路徑不存在**（常見原因是實測時間點早於複製落地）；「path is not under an allowed directory」＝ **目錄本身不被允許**。兩者指向完全不同的修法，不要混為一談。
- 🔧 **`message` 工具的 `dryRun: true` 只驗「允許目錄＋路徑」，不會真的讀檔**：所以 dryRun 通過 ≠ 檔案存在。檔案存在性要另外用 `os.path.exists`／MD5 驗，不能只靠 dryRun 推論。
