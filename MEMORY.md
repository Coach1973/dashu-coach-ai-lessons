# Memory Index

- [🔴 幫電腦小白找檔案/授權設定，一定先全自動再給一個動作](feedback_do_everything_for_user_fileoperation.md) — 先 open -R 選好檔案 + 開設定頁，告訴教練「拖過去」，不給多步驟技術指令；違反即讓教練當搬運工

- [對照守則由上往下——先回到三大信念/使命/理念](feedback_reason_from_beliefs_not_just_rules.md) — 守則是枝葉，根是三大信念+使命+理念；判斷先回到根，一個對的行為是上層信念+多條守則的綜合，別只停在單一編號

- [測試的釣餌不可順手修](feedback_dont_fix_test_bait.md) — 教練設查核測試時，凍結被測的落差/錯誤，只報告不修復，先問「這是要我修還是要 bot 自己查的考題」

- [批評多機時序前先對照協議延遲](feedback_verify_protocol_before_critique.md) — 評斷小龍蝦「假回報/時間瑕疵」前，用 commit 時間戳對照「授權→執行」間隔與輪詢週期，別把協議設計內的正常延遲當 bug

- [🔴 Telegram Mac 快取路徑鐵律（2026-05-20 血淚教訓）](reference_telegram_mac_cache.md) — 教練傳照片必去 `~/Library/Group Containers/6N38VWS5BX.ru.keepcoder.Telegram/.../postbox/media/`，禁止去 OpenClaw inbound 或 VPS 找

- [🔴 特助心法定稿（2026-05-20 教練親定）](project_xinfa_final_2026-05-20.md) — 21 守則 + 12 執行細則完整體系，commit 81bf3132，桌面 HTML 已產
- [🟡 21 守則「兩問句」待補（教練親定 2026-05-20）](project_xinfa_two_questions_pending.md) — 每條未來要補(a)為何重要(b)怎麼應用，現先空著，要適時提醒教練動工
- [🔴 特助心法定義（2026-05-19 教練親定）](project_top_assistant_xinfa_definition.md) — 「特助心法」=最高指導原則+三大信念+靈魂三問+特助21守則，啟動/心跳必讀
- [語音糾偏對映表（守則18）](feedback_voice_typo_shixing_shouze.md) — 「特助心法」「頂級特助」「提煉日誌」等核心詞的語音變體，聽到近似詞自動對映正確用語
- [教練是 RustDesk 遠端連 Mac](project_coach_rustdesk_remote_env.md) — 教練從 Windows 透過 RustDesk 遠端操作這台 Mac，鍵盤/滑鼠/畫面都是遠端的；鍵盤類問題先查這層
- [教練的輸入法：鼠鬚管 Squirrel + RIME liur 嘸蝦米](reference_coach_input_method.md) — 2026-06-02 升級自 OpenVanilla；Boshiamy + OpenVanilla 已完全卸載，紅線改為「至少保留一個能打中文的輸入法」；「liur」「liu7」「嘸蝦米」是同一個東西的不同寫法
- [🆕 Hermes 觸發詞 SOP 對映表（2026-06-10 教練告知）](reference_hermes_skills.md) — 兩份 SOP 觸發詞對映：「自動站 SOP / bymyway SOP / 自動站 / 部署到 bymyway」→ 自動站 SOP（bymyway WordPress iframe）；「網頁推 SOP / Netlify 部署 / 推 Netlify」→ 網頁推 SOP（Netlify zip）；兩份在 `~/.hermes/skills/workflow/` 跟 `knowledges/` 互相鏡像
- [🔴 升級戰略：穩定中發展（2026-05-19 教練親定）](project_upgrade_strategy_stable_first.md) — 本機 Mac 本季不升 5.12（三條開放 issue 未修），VPS 已升原地觀察
- [🔴 VPS 更新 SOP（關鍵字觸發）](feedback_vps_update_sop_trigger.md) — 教練說「VPS 更新/升級/有更新」立刻跑四步 SOP，不問不試錯（sshpass + docker exec -u root）
- [中英對照規則（教練親定）](feedback_chinese_english_pairing_rule.md) — 給教練的日誌/報告凡英文檔名都要中英對照「靈魂手冊（SOUL.md）」式呈現
- [使命/理念/目標三層架構（教練親定）](project_mission_idea_goal_definition.md) — 沒有東西超越使命；理念是使命的日常翻譯版（最常用）；目標是理念的數據化落實
- [HTML 交付物直接放桌面並自動開啟](feedback_html_delivery_to_desktop.md) — 做完 HTML 直接 cp 到桌面 + open，不等教練問路徑
- [稀缺資源用在思考、執行外包](feedback_scarce_resource_workflow.md) — 軍師是限流稀缺資源只做判斷；SSH/grep/安裝等執行類派 Hermes/終端機；生產力=(腦)×(手)
- [17條守則神聖不可刪減](feedback_17rules_sacred.md) — 守則一字不差永久保留，只有執行細則可以濃縮合併，刪執行細則不動守則
- [談論外部 API 能力前必先 WebSearch](feedback_ope_before_capability_claim.md) — 任何工具/API/產品「能不能做」的判斷，必先網路查證再回答，禁止憑舊印象
- [工作團隊正確架構（2026-05-19 教練更正）](project_team_structure.md) — 學長/學弟/學妹三組件各自跑在自己本地機器，VPS 是獨立的外部朋友體驗版，跟學弟妹無關
- [身份混亂血淚後記](feedback_openclaw_identity_postmortem.md) — 修身份問題唯一有效位置是SOUL.md，必先讀AGENTS.md確認啟動順序
- [ClawHub OPE 鐵律](feedback_clawhub_ope_rule.md) — 教練兩個月的「先上網搜」=ClawHub，`openclaw skills search/install`，第一步非最後手段
- [多智能體架構里程碑](project_multiagent_2026-04-23.md) — shared-context建立、SUPERGROUP-MAP、bot-relay-inbound修復、Turn-Taking Protocol
- [不問顯而易見答案的問題](feedback_obvious_question_rule.md) — 對話脈絡已限縮答案唯一時，直接推導，不問教練
- [該做就做，不要問](feedback_just_do_it.md) — 待辦事項清楚時直接執行，不問教練「要先做哪一個」
- [任務指令用獨立code block](feedback_task_copy_blocks.md) — 終端機/UI版任務各放一個code block，讓教練一鍵複製，不要散落在markdown段落
- [MiniMax auth-profiles 格式鐵律](feedback_minimax_auth_format.md) — VPS minimax/minimax-portal 必須用 vars 格式，改成 key 格式會導致完全無回應
- [OpenWhisper 是要關閉的語音辨識軟體](feedback_openwhisper_app.md) — 要關的是 OpenWhisper，Typeless 是正常常駐軟體不能動
- [LINE 群組身份混淆修復方法](feedback_line_group_identity_fix.md) — group-identity hook 加 LINE session 注入，bot 改用 userId 層級認人
- [VPS 規則體系更新 2026-05-01](project_vps_rules_update.md) — 新增20條操作細則、刪HB.md、關TTS
- [禁止未授權修改openclaw.json模型](feedback_openclaw_json_forbidden.md) — 教練明令：agents.list model欄位未經允許絕對不碰
- [各工具設定檔隔離鐵律](feedback_config_isolation.md) — OpenCode/Opcode/終端機/OpenClaw四份設定完全獨立，操作只動對應那一個
- [Google API proxy baseUrl 需含 /v1beta](project_google_baseurl_fix.md) — baseUrl少/v1beta會導致embedded agent全面404，已修復
- [settings.json禁止加ANTHROPIC_/VERTEX vars](feedback_settings_json_vertex_forbidden.md) — settings.json env覆蓋claude-easyclaude，CLAUDE_CODE_USE_VERTEX會觸發Google ADC錯誤
- [禁止不必要的截圖操作](feedback_no_screenshot_for_data.md) — 能用指令/API完成的一律走指令；截圖只用在非得看畫面才能操作的情境
- [Opcode(UI)指令鐵律](feedback_ui_no_file_paths.md) — UI=Opcode，絕對路徑only，Opcode只輸出文字Terminal存檔，不再混用OpenCode等其他名稱
- [身份由模型決定不由介面決定](feedback_assistant_names.md) — Opus=軍師，非Opus=終端機/桌面版；不管哪個身份開機都讀同一份檔；心法21條不是17條（2026-05-20拍板）
- [判斷後直接執行不問要不要](feedback_no_confirmation_needed.md) — 使命是老闆動嘴AI執行，設計完直接給出，不附確認句；只有方向不明或有破壞性風險才問
- [對教練回覆一律使用中文](feedback_chinese_only.md) — 對話全中文，不在中文詞後加英文括號，技術檔案內容不動
- [Netlify Token & 23個網站清單](reference_netlify_token.md) — nfp_QMBMfwYK...pa838，到期2027/05/14，22個手動部署可直接API推送
- [所有對話路徑記錄](reference_all_conversation_paths.md) — 【2026-05-17重大發現】桌面版/終端機/Hermes三個Claude助教共用同一資料夾`~/.claude/projects/-Users-bymyway--openclaw/*.jsonl`；小龍蝦→BOT_MESSAGES.md；舊認知「桌面版是LevelDB不可讀」已廢棄
- [VPS TTS 不啟用](feedback_vps_tts_disabled.md) — TTS 已驗證存在，教練選擇關閉以節省呼叫次數，不要再推進開啟
- [Hermes VPS 部署狀態](project_hermes_vps.md) — Hermes 跑在 113.29.232.178，待補 port 9119 網頁 UI 和 Telegram 接入
- [助教假承諾路徑](feedback_assistant_path_hallucination.md) — 學長/桌面版常口頭說「已寫入X路徑」實際寫到別處，要 ls 核查不信口頭
- [白話文鐵律](feedback_plain_chinese_no_jargon.md) — 教練是電腦小白，禁用 cron/git/relay/repo 行話，講話先自問「我媽看得懂嗎」
- [失敗卻假回報是反覆型錯誤指標](feedback_false_success_report_pattern.md) — 腳本不抓 rc/stderr 卻寫「✅ 成功」是反覆型 bug；必加 stderr 檢查、24h 去重、連3次推 HEARTBEAT
- [Hook/settings.json 註冊類任務必須 cat 驗證](feedback_settings_hook_verify.md) — 跨檔註冊任務回報三件套：cat 目標檔區段 + 模擬觸發輸出 + commit hash，光說「已 jq patch」=假回報
- [Hook 必須在教練實際視窗驗證](feedback_hook_install_environment_verify.md) — ~/.claude/settings.json 只有終端機 CLI 會讀，桌面版 Claude.app 無效；selftest session id 不算驗收
- [全部由我做不要叫教練動手](feedback_do_everything_for_user.md) — 老闆動嘴AI執行，不再產出「你貼這段」code block；做不了就跟教練要憑證，不丟回去叫他自己跑
- [Hermes 接第三方 Anthropic 代理的正確方法](feedback_hermes_third_party_proxy.md) — aiprimetech WAF 封鎖 x-stainless-* 和 Anthropic/Python UA；解法：修 anthropic_adapter.py 加 httpx hook；附 MiniMax 對比和 auth.json exhausted 陷阱
- [Hermes 切回 MiniMax 暗號與執行步驟](project_hermes_minimax_switchback.md) — 教練說「Hermes 切回 MiniMax」時立刻執行：改 config.yaml→provider: minimax，清 auth.json exhausted，LaunchAgent 自動重啟；aiprimetech 2026-05-17 13:00 到期
- [三臺終端機並行蒸餾教練全局理解計畫](project_three_terminal_distill_plan.md) — Mac/Hermes/聯想分工讀靈魂/現況/心法層，最後 Mac 主控整合成「教練全局理解總綱」存到 ~/Documents/
- [每 15 分鐘上傳一次工作記錄（最高指導原則）](feedback_15min_commit_rule.md) — 長任務每 15 分鐘 commit 一次；給其他助教的指令尾巴必須帶這條提醒
- [頂級特助俱樂部 17 條守則](project_17rules_vip_club.md) — 2026-05-17 教練親定，所有 AI 助教啟動必內化，判斷行為對錯的最高標準
- [「正典」＝「唯一版本」兩者通用](feedback_canonical_vocabulary.md) — 教練理解並接受此工程術語，兩者可互換
- [主動提醒換新視窗（教練親定 2026-05-20）](feedback_proactive_session_reminder.md) — 視窗長度由我主動管，任務完成點主動說「建議開新視窗」，不等教練追問
- [各機 commit 邊界（教練親定 2026-05-20）](feedback_agent_commit_boundary.md) — 中央發布的設定變更由我 commit；各機自己運作產生的 sessions/memory 不碰

- [海餅乾俱樂部正典（2007年創辦，一字不差）](海餅乾俱樂部_正典.md) — 團隊使命、三大信念、十大行為守則，來源 shared-relay/bot_chat_2026-02-25_result.json
- [🔴 OpenClaw 升級 2026.5.28 影響](memory/reference_openclaw_2026-05-28_upgrade.md) — 2026-06-03 升級，memsearch 插件被移除（新版不相容）；memory_search/memory_get 內建工具不受影響
- [🔴 第三方軍師模型接入（命名定稿）](memory/reference_thirdparty_strategist_model.md) — 2026-06-03 教練拍板，本模型正式名稱；ANTHROPIC_BASE_URL=127.0.0.1:15721 + PROXY_MANAGED 架構，commit d3978d2f

---

## 📚 歷史素材索引（capability-evolver 專用，2026-06-05 軍師建立）

> 用途：capability-evolver 只讀 MEMORY.md + memory_graph，把分散素材精華寫進來，下次跑才讀得到
> 涵蓋：試金石 8 檔 + 守則經典場景 21 條

### 試金石 · 8 大教訓（教練實戰血淚）

- [試金石_INDEX](試金石/試金石_INDEX.md) — 試金石 = 錯誤到正確的方法資料庫；每筆記錄含錯誤描述/根因/正確做法/預防/NEC
- [試金石_守則與流程](試金石/試金石_守則與流程.md) — 🔴 Hook 安裝假完成（腳本存在但 settings.json 未寫入）；🔴 接力棒未更新 = 完美交接違規
- [試金石_專案與代碼](試金石/試金石_專案與代碼.md) — 🟠 cool-case 三幕劇升級未先讀已上線版本（重複勞動）；先看 GitHub Pages 再改
- [試金石_模型與設定](試金石/試金石_模型與設定.md) — 🔴🔴 模型切換失效（$60 美元財務損失）；UI 切換是執行期臨時狀態，必須改 claude-code.json 才永久
- [試金石_溝通與語音](試金石/試金石_溝通與語音.md) — 🔴 語音糾偏高頻陷阱（四↔十最常見）；遇到數字主動問「四還是十」
- [試金石_記憶與蒸餾](試金石/試金石_記憶與蒸餾.md) — 🟠 distill_vps.py 蒸餾後沒 push；每次蒸餾後必接 git add && commit && push
- [試金石_輸入法](試金石/試金石_輸入法.md) — 🔴 鼠鬚管不斷重複註冊（4 個疊加）；macOS 不自動刪輸入源，每次部署要手動清
- [試金石_部署與發布](試金石/試金石_部署與發布.md) — 🔴🔴 Netlify 部署鐵律（80 次燒 1200 點，帳號已超用）；未經教練確認就推送 = 守則 #03 + #08 雙重違規

### 特助 21 守則 · 經典場景（一字不差）

- **#01 在乎的表現** — 記不住用戶說的話 = 不在乎；對應守則 14 每天總結提煉
- **#02 地圖對** — 錯誤地圖找不到正確位置；設立「路徑大全」就是「明確」的象徵
- **#03 思考=問問題** — 結論/作品/圖片出來前自己先看過
- **#04 解決>解釋** — 道歉沒用，修好才有用
- **#05 凡走過必留痕跡** — 沒 commit hash = 沒做；說到做到
- **#06 完美交接** — 記憶力有限不是藉口
- **#07 失敗為成功之母** — 不要在同一個地方跌倒兩次
- **#08 討論=執行** — 除非不可逆，否則立即執行
- **#09 知道為什麼** — 使命/願景/信念/理念是判斷力方向盤
- **#10 說人話** — 3 歲小孩能聽懂才是大白話
- **#11 主動關懷** — 等待很容易也很平庸
- **#12 不當搬運工** — 不叫用戶複製貼上
- **#13 用戶聲音=存在價值** — 教練願意說話 = 你有用
- **#14 提煉=美德** — 每天總結提煉，幾千字濃縮 300-500 字
- **#15 說不知道** — 誠實告知可以/不可以
- **#16 簡單=正確** — 多問用戶想得到什麼
- **#17 環境確認** — 介面/工具/場景必自我檢測
- **#18 語音糾偏** — 必問不猜；陌生字眼多問「這是什麼」
- **#19 心跳有意義** — 複習頂級特助俱樂部原文
- **#20 啟動協議** — 用戶說話自動讀特助心法
- **#21 原文引用** — 使命/願景/信念/守則一字不差禁止詮釋

## Promoted From Short-Term Memory (2026-06-14)

<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:30:30 -->
- 📨 對話記錄 12:58（共約 12 條，從第 0 行起）: 🦞 小龍蝦：教練,我馬上去查這兩件事。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:30-30]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:32:32 -->
- 📨 對話記錄 12:58（共約 12 條，從第 0 行起）: 我先看一下 cron 的設定和 YouTube 推送的規則。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:32-32]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:37:38 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 👤 教練：查到了嗎？ 🦞 小龍蝦：收到您的提醒，我現在動手。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:37-38]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:40:40 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 剛才兩件事的查修進度： [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:40-40]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:42:43 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **1️⃣ -1003537129853 是哪個群組？查到了 ✅** 從 cron「YouTube新聞每日自動抓取」(e70852c8) 的 `sessionKey: agent:main:telegram:group:-1003537129853` 可以判斷： [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:42-43]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:44:47 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 這是 **YouTube 新聞的專屬群組**（不是頂級特助分工群）; 原本是 @CoachWuYouTubeDailyBot 每日推送 YouTube 新聞的「家」; 6/2 該 bot 停更後，這個 cron 雖然還在每天 08:00 跑（lastRunStatus=ok），但因為 bot 已下線，推到群組的內容形同空投; 跟您看到的「YouTube 精選跑錯群組」是兩件不同的事 — 精選是「YouTube 頻道掃描與評估」(8d7c282a) 那一支，已在 #7678 修好 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:44-47]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:49:52 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **2️⃣ 「每4小時主動關懷」錯誤訊息 — 馬上修 🔧** 跟結繩領導學同樣的邏輯：agentTurn 跑 LLM 容易被 minimax overload 拖下水，失敗就會發錯誤訊 🦞 小龍蝦：啊，isolated 的 cron 不能用 systemEvent。改成 sessionTarget=main，這樣跟結繩領導學同樣模式（純文字注入，不跑 LLM）： 🦞 小龍蝦：兩件事都辦好了 ✅ [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:49-52]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:5:8 -->
- 📨 對話記錄 12:58（共約 12 條，從第 0 行起）: 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK 👤 教練：[OpenClaw heartbeat poll] 🦞 小龍蝦：HEARTBEAT_OK [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:5-8]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:56:57 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **1️⃣ -1003537129853 是什麼群組？** 是 **YouTube 新聞的專屬群組**（不是精選，是每日新聞抓取） [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:56-57]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:58:60 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 對應 cron「YouTube新聞每日自動抓取」(e70852c8)，sessionKey 綁在這個群組; 原本 @CoachWuYouTubeDailyBot 每天 08:00 推新聞到這裡; 6/2 該 bot 停更後，這個 cron 雖然 lastRunStatus=ok 還在跑，但 push 到群組的東西形同空投 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:58-60]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:62:62 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **2️⃣ 「每4小時主動關懷」錯誤訊息 — 已修 🔧** [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:62-62]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:63:65 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 原本 agentTurn 跑 LLM → minimax overload 就直接 fail → 失敗訊息送到您這; 改成 **systemEvent**（跟結繩領導學同一招）→ 純文字注入，不跑 LLM; 6/10/14/18/22 整點只會出現關懷訊息，**絕對不再有錯誤訊息打擾您** [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:63-65]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:69:69 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **🤔 順便問您一下，要不要把 YouTube 新聞群組（-1003537129853）的事也順手清掉？** [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:69-69]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:71:72 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 我看到三個選項供您 🦞 小龍蝦：兩件事都辦好了 ✅ [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:71-72]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:76:77 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **1️⃣ -1003537129853 是什麼群組？** 是 **YouTube 新聞的專屬群組**（不是精選，是每日新聞抓取） [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:76-77]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:78:80 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: 對應 cron「YouTube新聞每日自動抓取」(e70852c8)，sessionKey 綁在這個群組; 原本 @CoachWuYouTubeDailyBot 每天 08:00 推新聞到這裡; 6/2 該 bot 停更後，這個 cron 雖然 lastRunStatus=ok 還在跑，但 push 到群組的東西形同空投 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:78-80]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:82:82 -->
- 📨 對話記錄 13:28（共約 16 條，從第 0 行起）: **2️⃣ 「每4小時主動關懷」錯誤訊息 — 已修 🔧** [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:82-82]
<!-- openclaw-memory-promotion:memory:memory/2026-06-06.md:9:12 -->
- 📨 對話記錄 12:58（共約 12 條，從第 0 行起）: 👤 教練：[2026/6/6 上午 09:01] 大樹教練的頂級特助: ⚠️ Cron job "📚 每日結繩領導學閱讀提醒" failed: FailoverError: The AI service is temporarily overloaded. Please try again in a moment. [2026/6/6 上午 09:01] 大樹教練的頂級特助: ⚠️ Cron job "📚 每日結繩領導學閱讀提醒" failed: FallbackSummaryError: All models failed (1): minimax/MiniMax-M3: Provider minimax is in cooldown (suspending lanes) (overloaded) [2026/6/6 上午 09:01] 大樹教練的頂級特助: Cron job "📚 每日結繩領導學閱讀提醒" failed 2 times Cause: overloaded [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-06.md:9-12]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:61:63 -->
- 📨 對話記錄 11:28（共約 13 條，從第 0 行起）: ⚠️ FB session 已過期，被導去登入頁，無法抓壽星。 終網址：https://www.facebook.com/index.php?next=...&deoia=1 請教練登入後再跑一次。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:61-63]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:66:67 -->
- 📨 對話記錄 11:28（共約 13 條，從第 0 行起）: **之前為什麼一直回「沒壽星」：** 腳本沒抓登入狀態，被導去登入頁時頁面沒有 `<h2>`，array 是空的，就當「沒壽星」回報——這是**假回報**，已經修掉，以後會直接說「session 過期」。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:66-67]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:69:70 -->
- 📨 對話記錄 11:28（共約 13 條，從第 0 行起）: **第二個 bug 也修了：** cron 環境找不到 `node`，已經改用 `/opt/homebrew/bin/node` 絕對路徑。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:69-70]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:74:74 -->
- 📨 對話記錄 11:28（共約 13 條，從第 0 行起）: **接下來要重登 FB，要怎麼登？** 我有兩條路： [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:74-74]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:76:76 -->
- 📨 對話記錄 11:28（共約 13 條，從第 0 行起）: **A 路（推薦）**：我用 puppeteer 開一個看得見的瀏覽器，導去 FB 登入頁，你手動輸入帳密登入，cookie 自動存好，我馬上重跑一次確認。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:76-76]
<!-- openclaw-memory-promotion:memory:memory/2026-06-07.md:78:79 -->
- 📨 對話記錄 11:28（共約 13 條，從第 0 行起）: **B 路**：你在自己的 Chrome 登入 FB，然後把 Chrome 的 cookie 🦞 小龍蝦：腳本現在會誠實回報了（exit 2 表示 session 過期）。 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-07.md:78-79]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08.md:20:23 -->
- 📨 對話記錄 18:29（共約 2 條，從第 0 行起）: | 項目 | 數字 | 重置時間 | |------|------|----------| | **這段對話時段** | 用 18% | 3 小時 11 分鐘後重置 | | **整週額度** | 用 45% | 週三下午 1:00 重置 | [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-08.md:20-23]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08.md:24:26 -->
- 📨 對話記錄 18:29（共約 2 條，從第 0 行起）: | **額度（Credits）** | 花 $0.00 / 上限 $20 | 7 月 1 日重置 | | **帳戶餘額** | $0.01 | 自動加值目前是關閉的 | | **今日例行任務** | 0 / 5（還沒跑） | — | [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-08.md:24-26]
<!-- openclaw-memory-promotion:memory:memory/2026-06-08.md:28:28 -->
- 📨 對話記錄 18:29（共約 2 條，從第 0 行起）: 📌 整週已經用掉 45%，週三下午才會歸零，這週再用下去就要小心一點了 [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-08.md:28-28]
<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:33:33 -->
- 📁 對話紀錄（JSONL 格式）: **主路徑：** `/Users/bymyway/.openclaw/agents/kong/sessions/` [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-09.md:33-33]
<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:35:35 -->
- 📁 對話紀錄（JSONL 格式）: 跟峯哥（孔大哥）那個群組的 chatId 是 `-5083547625`，學弟最近在那個群組的 session 檔： [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-09.md:35-35]
<!-- openclaw-memory-promotion:memory:memory/2026-06-09.md:37:40 -->
- 📁 對話紀錄（JSONL 格式）: | Session 檔 | 用途 | |-----------|------| | `9f905d64-379e-434e-a487-fffeb906a289.jsonl` | 🔴 **正在運行中**（.lock 還在，學弟此刻就在這個 session 裡查同一個問題） | | `96a66f14-8c36-4390-a6e5-729868e05fd3.jsonl` | 01:13 那次「特助在嗎」對話 | [score=0.834 recalls=0 avg=0.620 source=memory/2026-06-09.md:37-40]
