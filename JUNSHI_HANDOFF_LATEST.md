## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 13:06 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5→Opus 5.5；教練說「總結」收工；本段 02:31～13:06，對話容量約 47%）

**主軸：①開工交辦兩件做完（預約頁週四時段生效、雲端軍火庫設計稿驗收並交付）②10/16 早上十幾個網站斷線：查出根因、補完手機修復漏掉的、裝上守門員。全部實測。**
- **預約頁週四**：02:32 重啟 com.coach.event-webapp，10/22、10/29 晚上＝19:30＋21:00（本機與公開網址一致），聯想信歸檔＋回信（`66a865b91`）。
- **軍火庫設計稿**（rongtree 分支 `claude/arsenal-entry-design` `0c08858`，未併 main）：單檔 git show 到暫存區＋本機伺服器驗收（桌機 1440／手機 400：無橫向捲動、字 ≥20px、100 格亮 37、DEMO 0 請求、不同意公開者不外洩）。私人頁交付 https://claude.ai/artifact/VvLFrV8He1qA3fnScPTSm3 （auto_register_artifact hook 實測自動收進大樹常用）。雲端點數 US$44→US$36（這件約 US$8）；方案週用量 32%，系統預警週一早上用盡。雲端信第六節 11 點待決（真公益 9 大領域、site 名稱、許願池聯絡欄、名冊 API 形狀…）。
- **網站斷線根因**：`~/Library/LaunchAgents` 的 com.coach.* 設定檔在 10/3 01:42～10/4 14:07 被刪——**是清理軟體 CleanerCat 的「已解除安裝 App 殘留檔」清理刪的**（10/04 手動清理 4 次、13:42 有動作；它認得 openclaw／hermes 所以那些沒事，不認得 com.coach／cloudflared 就當殘留清掉；無自動排程；教練 13:19 確認是他本人清理時按的，以前 4～6 月用時這些設定檔還沒建，所以沒出事），服務靠記憶體撐 12 天；10/16 08:44:55 Mac 登出（聯想 RustDesk 遠端操作中，08:44:28 有遠端點擊），08:45 再登入後全沒起來。event 斷約 3 小時、其他 11 站約 3.5 小時、真鑽約 4 小時。教練手機開的對話（33476b01，`723d246f4`）接回 12 站，但 5 站漏 `source .env`、真鑽被誤判「9/18 停用」（原文「解真鑽 DB 停擺」）、名片監看說找不回。12:50 用 Time Machine 10/03 01:10 原檔還原這 8 個，12 個網域實測 OK，資料沒外洩。
- **守門員**：`scripts/launchagents_guard.sh`＋`ai.openclaw.launchagents-guard`（WatchPaths＋登入時跑），以 `ops/launchagents_backup/`（完整 25＋1）為準；實測刪檔 10 秒補回、卸載自動重載、電報通知 10 分鐘節流。**要停服務＝同時從備份刪掉，否則會被補回。** `f90ba2012` `e75b4e3c1`；試金石 122、反射 R-LAUNCHAGENTS-PLIST-MISSING（實測會跳）、記憶 reference_launchagents_plists_deleted_outage_2026-10-16（`5a99e45b2`）。教練 12:57 授權本場用終端機寫正式目錄。
- **我的疏失**：02:32 重啟 event-webapp 時 ls 已找不到設定檔，沒當警訊（寫進案例 122）。
- **教練原話線索**：「我後來才知道」→ 網站掛了要有人主動通知他，不能等他自己發現；「簡單說，什麼原因」→ 先一句白話結論，再講細節。

### 📋 下一場開工先做
1. 教練看過軍火庫設計稿 https://claude.ai/artifact/VvLFrV8He1qA3fnScPTSm3 後的回應 → 企劃書 4 件＋雲端另 3 件要不要開（點數剩 US$36、週用量預警）→ 照做；不主動追問。
2. 🔧 AI 自己：①網站「掛了主動通知教練」的外部偵測還沒有（這次教練 3 小時後才從手機發現）→ 設計事件式做法（例如通道或網站程式結束時 launchd 觸發通知），做完實測。②下次真實登入後看 `~/Library/Logs/openclaw/launchagents_guard.log` 有沒有登入時那筆紀錄。③想縮小刪檔兇手時間窗：掛 TM 10/04 08:17 備份比對（目前只自動掛上 10/03 那份）。
3. 志工頁有人加入後教練報人數 → 改 `volunteer.html` 的 `JOINED`。
4. 🔧 承接：gateway 啟動的 `providers.nvidia.models[17].input` 設定驗證錯誤；新 LINE 群歡迎詞沒送出原因；策展 GitHub 化收尾；聯想 `/api/mytools/state` 放行 8765 建議拿掉；worktree 分支 `claude/kaigong-424fd5` 兩個 commit（交辦單、產生器腳本）要不要搬進 master。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：social-club 頁尾寫「TAVA AI 設計」不是「製作」；吳錦昌沒有個人頁；預約頁「只開固定時段」；南應大 /tut/team 要不要加入口；真貴 5 位要不要從真鑽拿掉；Podcast 快取改 1 分鐘；TAVA 備份頁放哪一類；GitHub 404 三個（joseph-cloth／social-good 私有倉庫不能開 Pages、Business.gym 沒有倉庫，event 上的版本正常）。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 02:10 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5；教練說「總結」收工；本段 01:24～02:10，對話容量約 41%）

**主軸：開工交辦兩件查完；軍火庫總入口設計稿開到雲端；真公益俱樂部頁新增「首批足跡夥伴」7 位並補齊五位個人頁頁尾；座位圖改照實況 7 席。全部實測、已推送。**
- **開工交辦兩件做完**：①新 LINE 群「榮樹下-訪談預約系統」真實路徑走通（台灣時間 10/15 20:53 教練問週四時段，分身 20:56 依總表回答；20:50 沒 @ 的那則被擋＝requireMention 設計，不是壞掉）。②雲端點數剩 **US$44／共 100**（11/5 15:59 到期；claude.ai/settings/usage），頁面不拆單一對話花費；方案本週用量 28%。三個自動機制（`auto_register_artifact`、`all_works_repo_hook`、容量提醒 Python 版）已確認掛在 `~/.claude/settings.json`，**但本場沒遇到事件，還沒驗到會跳**。
- **雲端「軍火庫總入口＋入選卡」設計稿**（教練：「先開這 1 件，其他 3 件等看過成果再決定」）：對話 https://claude.ai/code/session_018mtZLomzGSG6BQk4axWPMg ，Opus 5.5，借用 rongtree 倉庫，只准推分支 `claude/arsenal-entry-design`（新增 `arsenal-design/index.html`＋信 `docs/to_junshi/2026-10-16_arsenal_entry_design.md`），全用「示範」資料、`DEMO=true` 不送出、字 ≥20px，信裡要貼 `ROSTER/COUNTERS/WISHES` 資料形狀（給名冊引擎接）。標題與目標數字用我建議的暫定值（「你要的資源，這裡找得到」、對外 200）。交辦單 `workspace/state/cloud_briefs/arsenal_entry_design_2026-10-16.md`（worktree 分支 `claude/kaigong-424fd5` `d0abd57a7`，未進 master）。**還在跑、未驗收；開跑前點數 US$44，做完要查差額。** 開法與坑已寫進記憶 reference_move_to_cloud 第 6 節。
- **真公益俱樂部頁**（教練 01:39：牧師＝何瑞峰 `ruifeng`；名單陳顯立、何瑞峰、張麗蝶、朱元中、陳淑玲、大樹教練、吳錦昌）：social-club `3e228da` 新增 `#peers`「首批足跡夥伴」6 張卡（數字／足跡時間軸共 62 則／出處連結由程式逐字從各人頁抽出；吳錦昌連到原有 `#sunfar`）；導覽加「足跡夥伴」，**漢堡選單門檻 1180→1260**（CSS＋nav-burger `data-bp` 兩處，否則 1181–1234px 時「加入俱樂部」被擠出畫面）。五位個人頁頁尾補「招募志工團隊／真公益／真公益・企業家俱樂部」：ruifeng `2f6241fcd`、lidie `4ae55378c`、angel-sister `e3d6d6a21`、andy-chen `805fa3876`、patrick-chu `33d5a7a2e`（TAVA AI 製作五頁本來就有；教練說的「Tapa」＝TAVA；五頁字級本來就 ≥20px）。產生器 `workspace/scripts/peers_footprints/`（`1a68f81cd`，同在 worktree 分支）。座位圖「已有 50 席」→「已有 7 席」`e0d9aaeb8`（教練：原本前面席位保留給順發董事長邀請的 40 位上市櫃老闆，改照時間線「一步一腳印」）。記憶 project_peers_footprint_section_social_club_2026-10-16。
- **踩到的坑**：worktree 對話 Edit/Write 不能寫 `~/.openclaw`（只能走教練授權的終端機補丁）；內建瀏覽器要先 `resize_window` 才有版面（預設 innerWidth=0）；Python urllib 打正式站被 403，改 curl；`rm -rf` 被刪檔鎖擋（改用新資料夾名）；截圖被鎖，用 DOM 量尺寸。
- **教練原話線索**：「我們不是要找 100 家公益來參與嗎？目前就已經收集到這麼多了」→ 已做好的人當戰績先秀出來，不等湊滿；「按照目前這 7 位，一步一腳印」→ 對外數字一律照實況，不預留空號；「銷險整合計畫」疑為「策展整合計畫」（語音），後台 `event.bymyway.com/curation/admin`。

### 📋 下一場開工先做
1. **雲端軍火庫設計稿**：`git -C ~/github_repos/rongtree fetch && git branch -r | grep claude`，等 `claude/arsenal-entry-design` 出現（教練電報會收到通知）→ 讀信 → 用 `git worktree add` 驗收，**不要在 `~/github_repos/rongtree` checkout（會直接上線）**，也不併進 rongtree main，驗完搬到軍火庫自己的倉庫；到 claude.ai/settings/usage 查點數差額（開跑前 US$44）。
2. **Mac**（承接聯想棒第 1 項）：讀 `cross-agent/inbox/mac/` 聯想來信 `20261016-0155`，重啟 `com.coach.event-webapp`（預約頁週四新時段程式已 pull 未載入），驗證 10/22、10/29 晚上起點＝19:30 與 21:00；處理完信 mv 到 `outbox/2026-10/`。
3. 教練回應軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）→ 照做；教練已改用「目前 7 位、一步一腳印」的節奏，對外目標數字可能要比原建議 200／300 保守，等教練說。
4. 志工頁有人加入後教練報人數 → 改 `volunteer.html` 的 `JOINED`。
5. 🔧 AI 自己：新對話確認 `auto_register_artifact`／`all_works_repo_hook`／容量提醒會自動跳；gateway 每次啟動有一則無關的 `providers.nvidia.models[17].input` 設定驗證錯誤；新 LINE 群歡迎詞沒送出的原因；策展 GitHub 化收尾（聯想／宏碁貼網址觸發、projects/INDEX 策展卡）；聯想 `/api/mytools/state` 放行 8765 建議拿掉；worktree 分支 `claude/kaigong-424fd5` 上有兩個 commit（交辦單、產生器腳本）看要不要搬進 master。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內（「牧師是哪位」已解：何瑞峰）
🤫 等教練自己提起：social-club 頁尾寫「TAVA AI 設計」不是「製作」；吳錦昌沒有個人頁；預約頁「只開固定時段」；南應大 /tut/team 要不要加入口；真貴 5 位要不要從真鑽拿掉；Podcast 快取改 1 分鐘；TAVA 備份頁放哪一類。

---

> 📦 10/16 01:55 聯想 v259 棒已封存：`handoff_archive/handoff_2026-10-16_0155_聯想v259_archived.md`

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
- 模組化下一步 4 項（名冊引擎／預約引擎／通用短網址／報名接口收斂）｜只有教練能做：會改到 BNI、南應大、預約頁等夥伴正在用的系統，要教練拍板｜卡住名冊引擎開工｜問過：2026-10-14 報告第六節
