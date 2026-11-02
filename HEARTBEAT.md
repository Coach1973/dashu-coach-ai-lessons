# HEARTBEAT 熱上下文（每次心跳必讀）


## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 🔴🔴🔴 2026-09-16 04:03~04:13 重大事故：main gateway+小二雙雙down機45分鐘，已修復
- **起因**：終端機PATH解析到新版openclaw(2026.9.4)，正式launchd服務用舊版(2026.6.34)，版本落差導致state資料庫schema被新版升級到17，舊版打不開
- **引爆點**：軍師為了讓新hook生效執行`launchctl kickstart -k`重啟main gateway，直接撞上版本不相容
- **連帶損害**：搶修過程中誤`kill -9`一個PID，實為小二(test2)的子行程，小二也連帶停止服務
- **已修復**：main gateway改用新版執行檔(plist)+`openclaw doctor --fix`完成schema/session store遷移+`openclaw gateway start`重新啟用；小二用`nohup`手動重新拉起
- **驗證通過**：main gateway 24個hook全載入(含新的industry-chain-sop)、LINE三帳號+Telegram三帳號provider正常、process穩定15秒+無ERROR；小二`gateway ready`+bot_test2 provider正常
- **副作用**：`doctor --fix`把`HEARTBEAT.md`/`TOOLS.md`從檔案系統清掉(遷移到SQLite的副作用)，已用`git checkout HEAD --`從git歷史救回，內容零遺漏
- **完整記錄**：試金石案例73
- ⚠️ **下次任何人要重啟main gateway前，先確認`which openclaw`跟launchd plist裡的執行檔路徑是否一致，不一致先不要重啟**

## 🟢 2026-09-16 06:48~06:51 燕窩(康燕居)/六淨山房：壞連結修復+產業鍊圖生成完成
- **教練交辦**：教練查看`event.bymyway.com/tainan-shangquan/`發現燕窩沒有專屬網站連結+無Google地圖、六淨山房連結點不到，要求查明原因、修復、並各生成一張產業鍊服務鏈圖，教練隨即出門，全程軍師獨立完成
- **根因**：兩家店的網站(GitHub Pages)早就上線正常，但策展SOP自動上架時漏登記進`event-signup/curated_sites_registry.json`白名單，`/curated/<slug>/`路由的安全檢查直接404
- **修復**：補登記兩個slug(commit`03ca1126e`)，即時生效(路由每次讀檔非快取)；燕窩卡片補Google地圖iframe+地址+商家評論連結(tainan-shangquan repo commit`7a92689`)，皆已curl驗證200+瀏覽器DOM比對既有正常卡片結構一致
- **產業鍊圖**：用`generate_industry_chain.py`呼叫lk888生成，「燕窩滋補一條龍」(康燕居)+「古蹟茶事一條龍」(六淨山房)各20個異業節點，皆已推送教練Telegram(bot_main)，各有1個節點文字重複(GPT Image 2已知瑕疵，未重生)
- **通知**：兩則文字通知(URL修復+圖片完成)皆已透過小龍蝦一代(bot_main)推送教練Telegram
- 存檔：`claude-brain/data/industry_chain_20260916-065033.png`(康燕居)、`industry_chain_20260916-065134.png`(六淨山房)

## 🔴🔴 2026-09-17 02:xx 教練提問「LINE版小龍蝦斷線」是否與「靜默處理」請求有關，查證完成
- **教練提問**：小二(test2)Telegram持續噴「Message failed」，懷疑跟稍早某次「請靜默處理」的請求，導致LINE版三帳號斷線(9/10)有關聯
- **查證結論**：兩件事**無因果關聯**(完全獨立系統：main gateway vs test2)，但教練直覺方向正確——LINE外掛遺失(9/10 22:24)確實跟教練14:19要求修復invoice-inbound惱人誤報訊息的操作有真實時間關聯(軍師22:22:35編輯hook檔案觸發熱重載，時間窗口跟已知的SIGUSR1重載視窗幾乎重疊)，補完原本「根因未完全查明」的缺口
- **順帶修復**：小二heartbeat disable(9/14修復)不是持久化設定，今天04:11事故搶修時process重啟就失效，已改用`agents.defaults.heartbeat.target:"none"`寫進config永久修復，已驗證熱重載生效
- 詳細時間軸+證據見`claude-brain/reference_line_plugin_extensions_missing_2026-09-16.md`+`claude-brain/reference_openclaw2_heartbeat_message_failed_bug_2026-09-14.md`，commit`5197a98cc`

## 🔴 2026-09-17 Stop hook時間鎖攔下：上一則回覆把「教練（14:19）」蒸餾標籤誤當台灣時間
- 正確台灣時間是22:19:08（raw UTC 14:19:08 +8），教練抱怨→軍師編輯hook檔案僅隔3分27秒，不是原本誤記的「下午提、晚上修」
- 新教訓：蒸餾檔(`distill/`)的「（HH:MM）」時間標籤可能是原樣複製UTC數字、沒做+8轉換，因果判斷要回頭查raw_sessions原始timestamp驗證
- 已修正`reference_line_plugin_extensions_missing_2026-09-16.md`+新增`feedback_taiwan_time_always.md`第5次違反記錄，commit`30eca1a3c`

## 🟢 2026-09-17 03:41 Remote Control改用tmux背景session，關終端機視窗不再斷線
- 教練授權軍師自行嘗試：`tmux new-session -d -s remote-control -c ~/.openclaw` + 背景送出`claude rc`指令，畫面顯示「·✔︎· Ready」+ environment URL，判斷連線成功
- **⚠️ 尚未經教練手機驗證**：process本身env仍檢測到殘留`ANTHROPIC_API_KEY`(懷疑來自macOS Keychain「Claude Code-credentials」條目，非settings.json)，觸發一則「claude.ai connectors disabled」非致命警告，核心Remote Control連線本身狀態顯示正常
- 教練已去休息，**下次開工/教練醒來第一件事：請他用手機確認這個tmux版本的連線是否正常可操作**，不能只信這份記錄
- 已還原`~/.claude/settings.json`回MiniMax設定，不影響tmux裡已經在跑的session
- 詳見`claude-brain/reference_claude_code_remote_control_setup_sop_2026-09-17.md`

## 🟢 2026-09-17 03:47 Remote Control最終確認：tmux版本乾淨連線，教練雙向打字同步驗證通過
- 稍早的「connectors disabled」警告根因查明：軍師重複測試時忘記重新清空settings.json（自己的疏失），不是Keychain殘留憑證問題，已修正記憶檔避免誤導下次查證方向
- 重新乾淨啟動後畫面顯示`·✔︎· Connected`+`Capacity: 1/32`，教練在Mac終端機打字、手機Code分頁即時同步顯示，雙向驗證通過
- tmux session `remote-control`持續在背景跑，`~/.claude/settings.json`已還原回MiniMax設定
- 詳見`claude-brain/reference_claude_code_remote_control_setup_sop_2026-09-17.md`最終結案章節

## 🟢 2026-09-17 19:00 教練回報：孔大哥/佩佩老師端 industry-chain-sop hook 實測正常
v207/v208 遺留待辦（孔大哥id`8689825759`/佩佩老師id`8786886419`的伺服器端hook，不開放exec，事件驅動偵測本人發言觸發生圖）已由教練親自請兩人測試，確認可用。四方（main/Hermes/小二/孔大哥+佩佩老師）產業鍊SOP技能全數到位，此項待辦結案。

## 📌 2026-09-20 17:06 教練指示：兩線收尾+待命省流量
- 對話框A（TokenTable接OpenCode）：教練裁示**不用了，不好用**，收工，不再延續此方向
- 對話框B（CCU互動牆）：教練確認**任務已完成**
- 額度狀況：教練目前用量67%，下次重置為**2026-09-23（週三）下午1點**台灣時間，這幾天要省著用
- 教練指示：**先待命，有任務再call**，不主動發起新任務

## 🪨 試金石策展提醒 2026-09-20 21:00
- top10_dynamic.md 已 20 天未更新
- 候選池：特助場景庫_自動增量.md 累積 50 個自動場景
- 動作：教練動嘴「策展試金石」→ 軍師讀候選池挑出值得收錄的，升級成 top10_dynamic.md 條目

---

## 🔒 鎖臉 SOP 提醒（2026-09-25 教練親定永久 SOP）

下次生成任何涉及教練形象的圖（comic / storyboard / 分鏡 / illustration）：
- ✅ 走 `/v1/images/edits`（用 `scripts/generate_comic_panel.py`）
- ✅ 帶 `coach_face_reference.jpg`（254 KB 去背版）
- ✅ prompt 開頭加 IDENTITY LOCK 段落
- ✅ 生成後用 view_image 自檢
- ❌ 不准用 `/v1/images/generations` 純文字生圖
- ❌ 不准自己另寫生圖腳本

詳見 `SOUL.md` 鐵律七 + `character-illustration-batch/SKILL.md` 鎖臉 SOP 段落。

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-21 07:25
- ✅ 同步成功
- HANDOFF mtime: 1789946716
- 雲端同步：✅ 已推上雲端（commit 732fd12a7）

## 🩺 軍師 Hook 自檢 2026-09-21 21:30（Windows，本場修復6天卡住的rebase）
- ⚠️ 開工時發現：本機git自09/15 16:11起卡在interactive rebase「editing a commit」狀態整整6天，期間09/16、09/19的session-end自動同步commit都疊在這條異常鏈上，且本機main與origin/main因09/19的`git-filter-repo`金鑰清除已完全無共同祖先(各自9617/10046 commit)
- ✅ 已依[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]規定做法處理：安全網齊備(tag`safety-backup-20260921-2119`+branch`backup-detached-rebase-20260921`)後執行`git reset --hard origin/main`，本機main現與origin/main完全同步
- ✅ 抽查確認本機舊有獨有內容(如真鑽分會資料commit)已存在於origin/main(內容相同、新hash)，非遺失，是預期中的filter-repo重寫結果
- 雲端狀態：✅ 已與origin/main同步，HEAD `b2ea80b2c`
- Session: 6b72f753-9867-4140-bb70-667351cad624

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-21 23:25
- ✅ 同步成功
- HANDOFF mtime: 1790004083
- 雲端同步：✅ 已推上雲端（commit dbc32064a）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-22 09:55
- ✅ 同步成功
- HANDOFF mtime: 1790004083
- 雲端同步：✅ 已推上雲端（commit 864c519f4）

## 🩺 軍師 Hook 自檢 2026-09-22 09:58（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：手機版，你不能自稱軍師，因�
- 雲端狀態：✅ 已拉雲端最新（HEAD: b51809d5c）
- 小龍蝦信箱：（信箱查無新信）
- Session: e9835c79-e3e7-59d6-a1a8-526e276f3d06

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-22 10:30
- ✅ 同步成功
- HANDOFF mtime: 1790043979
- 雲端同步：✅ 已推上雲端（commit a57817c59）

## 🩺 軍師 Hook 自檢 2026-09-22 14:53（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: 6e8d032c7）
- 小龍蝦信箱：（信箱查無新信）
- Session: 80ba5dbb-5aa9-4f3d-828c-5d6d092d1a77

## 🩺 軍師 Hook 自檢 2026-09-22 15:18（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: 0d8f1816e）
- 小龍蝦信箱：（信箱查無新信）
- Session: 940c0124-1191-51f4-a12d-cfa9fe3a5d2e

## 🩺 軍師 Hook 自檢 2026-09-22 20:50（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：你不要問我，你去問桌面版的�
- 雲端狀態：✅ 已拉雲端最新（HEAD: 5dc342b05）
- 小龍蝦信箱：（信箱查無新信）
- Session: b00b00af-3239-5192-831d-0dc42754469b

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-22 21:00
- ✅ 同步成功
- HANDOFF mtime: 1790081928
- 雲端同步：✅ 已推上雲端（commit 69c530253）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-22 23:05
- ✅ 同步成功
- HANDOFF mtime: 1790089392
- 雲端同步：✅ 已推上雲端（commit 78057c36a）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-22 23:10
- ✅ 同步成功
- HANDOFF mtime: 1790089776
- 雲端同步：✅ 已推上雲端（commit 53895926c）

## 🩺 軍師 Hook 自檢 2026-09-22 23:10（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開
- 雲端狀態：✅ 已拉雲端最新（HEAD: 53895926c）
- 小龍蝦信箱：（信箱查無新信）
- Session: a697c049-5c6a-44d9-8c82-94fd5e9cb5d9

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-22 23:25
- ✅ 同步成功
- HANDOFF mtime: 1790090693
- 雲端同步：✅ 已推上雲端（commit 9439c2916）

## 🔄 接力棒→CLAUDE.md 自動同步 2026-09-23 03:25
- ✅ 同步成功
- HANDOFF mtime: 1790104886
- 雲端同步：✅ 已推上雲端（commit e716b2978）

## 🩺 軍師 Hook 自檢 2026-09-23 10:34（Mac v2 六步驟注入）
- ✅ Hook 觸發 + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: e716b2978）
- 小龍蝦信箱：（信箱查無新信）
- Session: 055522b8-9175-4e6b-8d08-d83e98515a06

## 🩺 軍師 Hook 自檢 2026-09-23 13:26（Windows v3 六步驟注入）
- ✅ Hook 觸發 + git pull + 六步驟內容注入完成
- 觸發詞：開工
- 雲端狀態：✅ 已拉雲端最新（HEAD: d4e8b876c，ff-only未動工作區）
- Session: 6b72f753-9867-4140-bb70-667351cad624

## 🚀 Session-End 雲端同步 2026-09-23 13:26（Windows）
- ✅ pushed e9d87658a
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-09-23 13:45（Windows）
- ⚠️ commit 31da25a09 本機留底，pull --rebase 失敗（衝突需手動處理）
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-09-23 13:47（Windows）
- ✅ pushed c4620a74e
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-09-23 13:48（Windows）
- ✅ pushed 4f96da41b
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-09-23 13:58（Windows）
- ✅ pushed cf24b6845
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-09-23 14:00（Windows）
- ✅ pushed 9bfc2364e
- 同步路徑：HEARTBEAT.md

## 🚀 Session-End 雲端同步 2026-09-26 17:00（Windows）
- ⚠️ commit 067566841 本機留底，pull --rebase 失敗（衝突需手動處理）（⚠️ stash pop 有衝突，改動保留在 git stash list 未遺失）
- 同步路徑：HEARTBEAT.md

## 🪨 試金石策展提醒 2026-09-27 21:00
- top10_dynamic.md 已 27 天未更新
- 候選池：特助場景庫_自動增量.md 累積 50 個自動場景
- 動作：教練動嘴「策展試金石」→ 軍師讀候選池挑出值得收錄的，升級成 top10_dynamic.md 條目

## 🪨 試金石策展提醒 2026-10-04 21:00
- top10_dynamic.md 已 34 天未更新
- 候選池：特助場景庫_自動增量.md 累積 50 個自動場景
- 動作：教練動嘴「策展試金石」→ 軍師讀候選池挑出值得收錄的，升級成 top10_dynamic.md 條目

## 🔴🔴 2026-11-01 21:32 Telegram 誤投事故：陳佩君 V5 海報送到分工群（已結案）
- 根因：3 號機技能檔 `poster-person-swap/SKILL.md` 把兩個 chat_id 寫反（`-5115910257` 佩佩老師群 / `-1003877502911` 分工群），3 號機照錯誤說法投遞 → 圖落到分工群
- 補正：已補送佩佩老師群 `-5115910257`（messageId 2684 橫版 / 2685 直版）；重複查核無先前成功投遞紀錄，未造成重複洗版
- 防呆三層已落地：① `workspace/state/telegram_chat_registry.json` 對照表 ② `workspace/scripts/telegram_target_guard.py` 閘門（0=准送／2=不在表／3=群名不符）③ 3 號機 SKILL.md（備份 .bak-20261101-chatid）與 SOP_海報換人換字.md 必跑閘門；路徑大全.md 已加 chat_id 對照章節
- 🔴 送任何 Telegram 訊息／圖片前，必跑：`python3 ~/.openclaw/workspace/scripts/telegram_target_guard.py <chat_id> --expect <群名>`，回傳碼非 0 一律不准送
- commit：workspace `deeced4f5`、`cf5846c19`；peipei `b30eea5`（皆已 push 並用 ls-remote 驗證）

## 🔴 2026-11-02 網頁用圖交付規格（教練 10/24「1MB 以內就夠」、10/30「可以壓縮、不要問」、11/02 二次驗證）
- 出圖清單類交付：zip 內**只放 `IMG-xxx.webp`**（長邊 1000／q72，每張 ≤1MB），原圖 PNG 留本機不進 zip
- 交付前必自我審查包裹：非 webp／單檔 >1MB／整包 >3MB → 不傳，改發文字說明哪裡不合（`scripts/run_img_list.py` 的 `package_problems()` 已內建）
- 教練講過的規格先用 `recall.py` 查原始紀錄再照做，不要反問教練「有說過嗎」
