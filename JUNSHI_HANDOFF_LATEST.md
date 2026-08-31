## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立）

> 這張表**取代**逐棒散落的「vXX待辦」小表——舊表格散在v72/v73/v74/v75各自的段落裡，容易漏看、也看不出哪項是「卡住等教練」還是「該我自己動手」。**以後每一棒開工先看這裡，任務完成或狀態改變就更新這張表，不要再另開一張新的待辦表。**
>
> 狀態代碼：🔒卡住-等教練　⏳待軍師/小龍蝦動手　⚠️持續追蹤(非任務)　✅已完成待確認

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🎯🎯 | **大樹小講/AI微論壇/紅綠燈看板/培訓行事曆改event.bymyway.com即時渲染，逐步脫離Netlify部署次數限制** | ✅2026-08-30本場完成，教練親口「很棒」肯定方向 | 教練拍板方向：讀活repo+event.db即時渲染取代Netlify手動zip部署，GitHub Pages/Netlify暫時保留同步、穩定後才退場。已上線4個新路由，全部走`event-signup`既有Flask app（不新增子網域/Tunnel/launchd，降低服務被遺忘風險）：`event.bymyway.com/bigtree/`（疊event.db即時場次資料）、`/ai-forum/`（現為台中場9/23-24，2天制系列共用網址，教練明確要求網址代表格式非地點，之後10/7-8台南場沿用同網址）、`/ai-talk/`（半天制系列，現仍8/28嘉義場內容，等教練補凌榆舜/李明燦兩位講師資料後改9/22台南場）、`/tainan-calender/`、`/bni-traffic/`（純client端repo，零風險）。同步更新3處連動：①`bni-chapters`資料庫9分會×2連結共18筆改新網址 ②`bni_tainan`小幫手`AGENTS.md`4處member-facing連結+`sync_calendar.py`抓取來源（過程修好Cloudflare擋urllib預設UA的403問題）③`coach888`作品總覽新增「三、bymyway自架版」區塊（教練要求移到第三順位，其餘區塊順延），5個Netlify舊版標「待退場」橘色badge一眼可辨識。所有變更均先本機測試埠+真實Chrome驗證，重啟正式服務後在公開網址再次curl驗證才commit。commit一覽：`f8ac8fc`+`3df06cab7`+`fc58dc783`（event-signup）、`5fabb60d`（bni_tainan外層repo）、`230d735`+`cafe1f4`（coach888）。記憶：`project_bymyway_dynamic_hosting_escape_netlify_2026-08-30`+`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。**`/ai-talk`9/22台南場內容已於v153完成上線**（凌榆舜+吳大樹雙講師版，李明燦講師身分已取消），詳見v153。 |
| 🎯 | **BNI Connect新增大台南南區初階MSP/進階MSP/季度主題培訓/新領導團隊訓練/領導團隊期中訓等活動，供會員報名** | ⏳待軍師動手 | 教練2026-08-31交辦：進BNI Connect後台新增這幾種活動類型，讓會員可以在系統裡註冊/報名。尚未動手，下一場先進BNI Connect CMS後台查證現有活動類型清單+建立流程(參考`reference_bni_connect_cms_structure`記憶)，確認每種活動的欄位需求(日期/地點/講師/名額)再建立。 |
| ✅ | **AI百人導師(mentor100)申請通知改走Telegram，修復8/27靜默漏接** | ✅2026-08-30本場完成 | 教練回報8/27有人申請完全沒收到通知，還誤重複提醒對方。查證根因是`apply_submit()`打的是舊版LINE通道(`sme-register-fn`)且吞掉錯誤，跟event-signup試金石案例62同款坑。已改用event-signup驗證過的Telegram Bot API直送方案(chat_id 6124913915)，失敗必寫`notify_failures.log`。已用真實`/apply`端點測試驗證，測試資料已清除。commit`1b9b816`(mentor100 repo)。全機掃描確認無其他專案殘留舊LINE通知路徑。記憶`project_mentor100_application_notify_telegram_fix_2026-08-30`。 |
| ✅ | **真誠分會邀約來賓紀錄表重複建置事件：根因已查明+重複版本已移除** | ✅2026-08-30本場完成，教練親自抓出根因 | 起因：查git log發現bni-chapters裡有一份`c6ce0f2`commit做出功能重疊的重複實作（`/admin/chapters/1/invites`）。**教練親自比對兩個session的原始.jsonl逐行找出精確分岔點**：01:37:48原session(`fa8a74d2`)正在忙背景Explore子代理查詢時，Claude桌面版App在01:38:11自動生成一則`isMeta:true`+`entrypoint:claude-desktop`+`model:<synthetic>`的「Continue from where you left off.」內部握手訊息，**憑空分岔出這場對話**(`0f9618ae`)，繼承原session到01:37:48為止的歷史，之後兩條各自獨立發展——非教練或AI下達的fork指令，是App層級的自動行為。教練確認只需要`sincere.bymyway.com`一套，重複版本已移除：`/admin/chapters/1/invites`路由+`admin_invites.html`+db.py四個函式+schema.sql四張invite_*資料表全部移除，檔案歸檔於`_archive_duplicate_invites_feature_2026-08-30/`未刪除，資料庫既有資料保留未清空，commit`6b06bca`（bni-chapters）。詳見v149+v150、記憶`feedback_check_git_log_for_parallel_builds_2026-08-30`。 |
| ✅ | **AI百人導師(mentor100)真誠分會5人簡介卡遷移到chapters.bymyway.com/sincere+後台新增編輯按鈕** | ✅2026-08-30本場完成 | 王彤/陳佩君（佩佩老師）/楊在珍/林佳伶Lavi/葉建葳，含照片，逐筆核對mentors表欄位對應chapter_members表（兩邊格式一致）搬移，commit`1f460f7`（bni-chapters）。教練隨後指出後台改資料只能靠AI代改的缺口（「我自己改不了」），已新增`/admin/chapters/<id>/members/<id>/edit`路由+`admin_member_edit.html`模板，沿用既有`member_join_edit.html`欄位結構跟`db.update_member()`函式，分會夥伴簡介列表每筆加「編輯」連結，commit`8cd9595`。**已用真實登入+存檔round-trip驗證**（改一個欄位→存檔→查資料庫確認真的更新→頁面顯示「已儲存修改」→測試值改回原樣），非僅程式碼審查。詳見v149。 |
| 🟡 | **教練提出「釋放記憶體」指令要更全面：連同所有可關App一併關閉** | 🔒卡住-待教練確認白名單範圍 | 2026-08-29教練電腦變慢多輪診斷後提出構想，已給評估：系統層級記憶體碎片化只有重開機能徹底清空，關App效果有限，且既有的RustDesk釋放指令查證後對15GB量級記憶體壓力貢獻微乎其微(重啟後process反而一度變多)。若要動手寫這支腳本，需先問清楚白名單——Claude/Finder等系統必要項可以確定，但Typeless/Chrome/LINE等常用工具要不要保留，教練尚未回覆。詳見v148。 |
| ✅ | **peipei-event.bymyway.com斷線5天已修復+永久看護機制建立** | ✅2026-08-29完成 | 教練詢問這個網址為何失效，查證是Cloudflare 530(tunnel connector沒連線)，根因是這組webapp+tunnel從2026-07-13建立以來唯一沒接launchd看護，8/24被terminated後斷線5天無人發現。已手動恢復服務+新增`com.coach.peipei-event-webapp.plist`+`com.coach.peipei-event-tunnel.plist`永久修復，commit`2ffba5dc9`(記憶`reference_bymyway_subdomain_530_missing_launchd_2026-08-29`)。詳見v148。 |
| ✅ | **乾淨世界頻道關注QR立牌上線+加入作品一覽** | ✅2026-08-29完成 | `make_qr.py`新增`--ganjing`模式，導流大樹教練乾淨世界頻道，拿掉集點文案改「300集免費影片」，commit`0669f44a2`；已加入coach888作品一覽第10項，commit`48520cd`。正式網址`event.bymyway.com/qr/ganjing-print.html`已驗證可用。詳見v148。 |
| 🟡 | **9/16「當古典音樂遇到AI科技」高雄場活動結束後，把大樹小講(bigtree)自動部署到Netlify正式站** | ⏳排程等待9/16 17:30觸發 | 教練2026-08-28口諭「先不用，活動結束時，再自動移過去」——目前已推GitHub+GitHub Pages上線(coach1973.github.io/bigtree)，唯獨bigtree-tw.netlify.app(手動zip部署型)保留沒推，等活動結束才推。已寫好部署腳本`scripts/deploy_bigtree_after_0916_event.sh`(git pull+git archive打包+呼叫Netlify Deploy API，site_id`40e580f0-1def-4777-adb8-587ef023ed36`)，並在聯想Windows本機用Claude Code CronCreate排了一次性durable任務(job`ee5beb77`，2026-09-16 17:30觸發)。**風險**：這個排程只存在聯想這台機器的`.claude/scheduled_tasks.json`，只有教練那天有開這台機器的Claude Code才會觸發（或事後補跑會被catch-up機制偵測到）。**任何機器的軍師若在9/16當天或之後開工，看到這行待辦，直接跑`bash scripts/deploy_bigtree_after_0916_event.sh`即可完成部署**，不用等聯想觸發，完成後把這行狀態改成✅並刪除。同場相關：`ai-art`新repo已建立(https://coach1973.github.io/ai-art/)承載這場活動的獨立網頁，`archive/大樹小講_歷史講座紀錄.html`宮格牆已加9/16卡片連結該頁。 |
| ✅ | **真誠分會自助送出簡介機制，已套用到全部9個BNI分會** | ✅2026-08-27完成，教練親口「很棒」驗收通過 | 比照mentor100百人導師同行**第一階段**設計，`bni-chapters`新增`chapter_members`表(chapter_id範圍)＋`/<slug>/join`自助送出表單(honeypot+IP rate limit防灌水)＋送出即自動上架＋`edit_token`自助編輯/刪除＋後台夥伴清單供刪違規內容，commit`44fc3dd`。**因架構本身是chapter_id分流、9分會共用同一套後端**，教練說「套用到所有分會」後，逐一curl驗證全部9個slug(sincere/real-ai/true-rich/true-love/zhenxin/real-diamonds/real-kungfu/real-age/real-wealth)的分會頁面+`/join`表單皆為200且各自顯示正確分會名稱，後台`admin_edit`(chapter_id=5/9實測)也都能看到各自夥伴清單，**確認9個分會全數已生效，無需額外程式碼異動**。此項結案 |
| ✅ | **`/bni-credit`網頁三項待改全數完成+30天到期提醒上線+34筆離會會員補開真證+搜尋空格bug修復** | ✅2026-08-28本場完成，第3項(補公司)延後至下週三 | 5分會402人清查主線+340筆複查+權限隔離皆已結案(見v146)。**待辦一(移除已失效空分類)**：279筆複查0筆命中，commit`d6a2c0a4d`。**待辦二(到期日顏色分級)**：教練拍板12/6/3個月四段式，commit`da001f57f`。**待辦三(補公司欄位)**：教練裁示延後至下週三(2026-09-02)。**BNI信用証30天到期提醒**：`scripts/bni_credit_expiry_reminder.py`+openclaw cron`8211e054`每日08:57執行，真實資料驗證過，commit`91680dcfe`。**教練後續追加大量互動，逐一測試「產生信用証」按鈕**：胡宗奇誤分類(active無cert_id)發現後，教練授權點擊2024年以前25筆未開立記錄，**24+胡宗奇重試共25筆全部成功**產生真證(編號1348126~1348151)；教練再指定劉智揚(2076177,真鑽)+6筆(林政志/柯其宏/楊文忠/歐鎮平/蔡宜君/薛如雲)，**7筆全部成功**；補回吳承洋(v146事故cert 1348092)資料同步。合計本場新增/補回**34筆真證**寫入資料庫。抽測3筆「已過期」+5筆「沒有額度」確認分類正確不需重開；羅琳案例教練親查兩次入會歷史確認ineligible正確，並補充「信用証只適用已離會會期」通用原則。**額外發現並修復重大搜尋bug**：教練搜尋「林政志」查無結果，查出`cards`表451筆有422筆(93%)姓名是BNI Connect原始「姓 空格 名」格式，一般LIKE比對被空格擋下，教練要求「不要管空格，字對了就找到」，已把`/find`+首頁搜尋所有欄位(姓名/公司/職稱/分類/電話/Email/地址/關鍵字)全部改成雙邊去空格比對，commit`5e8be0c9a`+`e969f61a6`。**教練當場糾正**：花時間重新查證教練已經明講過的資料庫需求(現任/前會員/來賓三類)，浪費他流量跟時間——已寫入記憶`feedback_dont_reverify_stated_requirements_2026-08-28`。吳承洋等34筆信用証由AI直接產生非教練手動點擊，此為教練明確授權後執行(教練原話：「產生信用證之後還有24個月期限，沒有任何風險」)。 |
| 🔴🔴🔴 | **FB粉專行銷自動化：App+12個粉專發文權杖已建好，但「大樹教練」最重要粉專的pages_manage_posts權限卡在商家驗證未完成** | 🔒卡住-教練已於2026-08-27 17:00送出驗證，Facebook回覆約48小時(2個工作天)內出結果 | 聯想Windows本場從零建置Graph API App「大樹教練粉專發文小幫手」(App ID`1050871501278089`)，順利拿到12個一般粉專的Page Access Token(存於`fb_automation/page_tokens_2026-08-27.json`+`路徑大全_憑證層.md`，經debug_token驗證`expires_at:0`永不過期)，教練指定優先要發的4個是大台南策展中心/K R養生廚房/海餅乾俱樂部/跨界美.術.管。**卡住點**：教練最重視的「大樹教練」個人品牌粉專(facebook.com/bymyway，Page ID`252699914868764`)一直無法透過`/me/accounts`列出，且不管怎麼重新授權，真正的發文權限`pages_manage_posts`永遠拿不到（scope只剩前3個）。繞了一大圈試錯(切換使用案例分類/App後台加權限/開新分頁重來/猜New Pages Experience限制/加進Business Portfolio)才在Meta Business Suite「安全中心」頁面查到官方明講：「你的組織必須通過驗證，才能使用特定Meta產品」——真因是**商家驗證(Business Verification)未完成**，教練當場點名檢討「浪費了大半的時間最後才找到關鍵」，已寫入試金石案例67+記憶`feedback_diagnose_root_cause_before_trial_and_error_2026-08-27`。教練決定自己找時間去`business.facebook.com`安全中心點「開始驗證」，完成後開新對話框回來繼續。**下一棒待辦**：教練商家驗證過了之後，重新走一次`pages_manage_posts`授權流程(教練需親自點擊「Generate Access Token」，自動化點擊會被瀏覽器攔截)，驗證12個粉專+大樹教練都能真正發文後才開始寫自動發文腳本；教練尚未提供「素材對應規則」(哪個活動配哪個粉專)，也要問清楚才能真正開始自動化。 |
| ✅ | **Stop hook守則#07輪詢偵測瞎眼35天，工具回音誤判成回合邊界的根因已修復** | ✅2026-08-27完成，用真實對話重播+本場活體測試雙重驗證 | 教練修RustDesk腳本時自己講出「每10分鐘檢查一次」被親口糾正，查證發現這台Mac本來就有專門攔這句話的Stop hook，但log顯示從7/24起完全沒抓到過任何真實違規。根因：TURN_TEXT往回掃描transcript時，把工具執行結果（也是`type=='user'`）誤判成「教練講話」的回合邊界，真實對話一有多次工具呼叫（幾乎必然）就提早打斷掃描，抓不到更早講的違規內容。此bug自2026-07-23就存在，非08-12合併造成的新問題。已修復`scripts/stop_rules_master.py`+同步修好同一天失效的`test_stop_rules_master.sh`（比對基準依賴的檔案早被刪除，測試從建立當天就已失效）。詳見試金石案例66、[[reference_stop_hook_tool_result_boundary_bug_2026-08-27]]。commit`01a28f2fb`。 |
| ✅ | **聯想跨機同步四層根因全修+ai-talk嘉義場設攤廠商05~10上線+Netlify額度校正934.9** | ✅2026-08-26聯想完成，詳見v138 | 詳見`claude-brain/project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26.md`。四層根因：①7支對齊hook聯想從沒裝過(含收工自動push) ②所有hook讀到的`workspace`是7/23的死clone，已封存改junction指向活repo ③PS5.1讀stdin中文被Big5讀壞(「開工」變亂碼)，`feed_junshi_handoff.ps1`等3支已修 ④`session_end_auto_push.ps1`commit後沒先pull就push，必被拒，已補stash→pull--rebase→push。另完成教練交辦：ai-talk嘉義場設攤廠商05(乾淨世界補號)~10(KR廚房)全數上線並curl驗證；Netlify額度按教練截圖回報949.9/1000校正，本場部署2次後934.9，寫回共用檔案供三機同步。**教練當場糾正**我把額度同步做成PreToolUse自動攔截hook太複雜(還意外把自己下個指令攔到報錯)，已撤掉改成手動記數+總結時寫回，詳見[[feedback_netlify_quota_sync_simplify_2026-08-26]]。 |
| ✅ | **名片系統BNI Connect匯入+媒合MiniMax額度事故（案例65）：教練拍板改「手動觸發媒合」設計，已上線/find搜尋頁** | ✅2026-08-26本場完成，設計定案並上線 | 詳見v135/v136完整戰果+本場v137戰果。**教練這場定案新規則**：不再對任何一批人批次自動媒合，改成**手動點按鈕才呼叫AI**——現任92人(唯一預先批次媒合的例外，已100%完成)之外，前會員336人＋來賓3216人一律等教練或使用者實際需要時才觸發。已上線`/find`統一搜尋頁（cards+guests雙表搜尋，零AI呼叫）＋`/guest/<id>/match`來賓版媒合入口（首次點擊才轉一筆card+跑媒合，`source_guest_id`防重複轉入），`run_chain_match.py`已改成只鎖現任會員範圍，不會再被誤觸批次跑全部人。**來賓資料重大補正**：教練糾正「BNI Connect來賓一定有專業別」，查證屬實——v136只抓了姓名/電話/email三欄，漏了報表本來就有的公司/職業/分會欄位，已用教練提供的完整報表(.xls/SpreadsheetML)重新解析回填，3216人中3210人(99.8%)已補上職業資料。**額外揪出的資料品質bug**：教練從/find頁面發現田伸強/林尹渰等4人BNI身分沒標示，查證是`parse_and_import.py`的INSERT OR IGNORE遇檔名撞名時靜默跳過、且無UPDATE補救路徑，4人資料已修正+全428人重新稽核0遺漏+腳本已加rowcount==0的UPDATE fallback防再犯。 |
| ✅ | **ACER機49天未開機導致settings.json全部hooks消失，本場（教練親自開機）重裝七支hook+跟進聯想總結修復** | ✅2026-08-26 ACER本場完成並實測 | 教練親自打開ACER下指令，這正是Mac稍早報告裡說「唯一解法」的那個時刻。查證確認`~/.claude/settings.json`原本完全沒有`hooks`區塊（開工六步驟/截圖鎖/跨機信箱掃描/總結上傳全部沒註冊，跟聯想的jq依賴問題不同根因）。同時也第一次真正走完「開工六步驟」被教練當場糾正前的落差：本場一開始跳過血淚試金石案例庫直接動手，被教練點出才回頭補讀，讀到案例60（claude-in-chrome連錯裝置）跟HEARTBEAT.md「截圖禁用」規則，直接解釋了稍早bigtree部署過程中一直卡在截圖的原因。跑`scripts/setup_windows_hooks.ps1`重裝七支hook時，**發現這支安裝腳本本身有bug**：`ConvertFrom-Json -AsHashtable`在這台機器的PowerShell 5.1（非pwsh 7）會拋例外，觸發catch分支把原有`env`/`permissions`/`model`等設定全部清空，只剩新寫的hooks——靠腳本自帶的備份救回，手動合併寫回。額外把聯想剛寫好的`summary_upload_trigger.ps1`一併加進ACER的UserPromptSubmit，四情境（總結/總結上傳觸發、年度總結報告/閒聊不誤觸發）全部用假指令實測通過。本場另完成：大樹小講(bigtree-tw)新增8/26早半場「晨光美學」10:00-12:30(地址同步改4樓)，已推GitHub+Netlify雙邊驗證上線；回信Mac完成verbatim/Stop hook查證。**下一棒待辦**：①`event-signup`後台`event.db`仍未同步8/26早半場資料，現場QR簽到當天可能路由錯場次，需請Mac或聯想在能碰到該DB的機器上補②`setup_windows_hooks.ps1`的PS5.1 bug本場只記錄未回頭修，下次任何機器要跑這支installer前應先查`$PSVersionTable.PSVersion`。詳見`claude-brain/project_acer_dormant_49days_2026-08-26.md`+`claude-brain/project_acer_hooks_restored_2026-08-26.md`。 |
| ✅ | **聯想「總結」收工hook缺jq靜默失效近一個月，已改PowerShell版修復** | ✅2026-08-26聯想完成並實測 | 教練質疑「我每次都講總結上傳，怎麼可能沒紀錄」，查證屬實：`summary_upload_trigger.sh`靠`/usr/bin/jq`解析stdin，聯想這台機器沒裝jq，指令找不到→PROMPT變空字串→關鍵字比對永遠比對不到→整支hook靜默不觸發，不報錯教練也看不出異狀。改寫`scripts/summary_upload_trigger.ps1`(PowerShell原生`ConvertFrom-Json`，不依賴jq)，7情境模擬測試全過已註冊進`~/.claude/settings.json`。同場也查證另兩支相關機制：`distill_and_push_lenovo.ps1`從未被註冊過（非壞掉，是從沒接上）、Windows Task Scheduler的`ClaudeMemorySync`任務也停用超過2個月。詳見試金石案例64。 |
| ✅ | **ezPay發票工作歸屬記憶更正+Mac Stop hook狀態跨機查證回信** | ✅2026-08-26聯想完成 | ①`project_ezpay_invoice_task_delegated_to_lenovo_2026-08-16.md`舊記憶停在「聯想負責」，實際08-18已因聯想操作卡住(原生彈窗凍結)轉回Mac主責，教練追問後才發現記憶沒同步更新，已修正並跟Mac同時間做的類似修正(commit`de76222c`)合併解衝突 ②回覆Mac凌晨來信，查證確認`distill_and_push_lenovo.ps1`從未接進聯想`settings.json`的Stop hook，回信已放進`cross-agent/inbox/mac/`。 |
| 🔴🔴🔴 | **宏碁ACER確認49天未真正使用，教練需親自開機讓它git pull+讀信才能追上進度** | 🔒卡住-等教練 | 教練要求「把賈維斯設定同步到宏碁跟聯想」，查證發現聯想是jq依賴缺陷已自行修復（詳見下方commit），但ACER是完全不同、更嚴重的狀況：信箱4封未讀信最舊7/13、verbatim蒸餾自7/8建立起零產出、ACER自己最後一次主動push是7/8，49天沒有真正被打開過。Mac這邊已把賈維斯所有規則內容(CLAUDE.md/執行細則/HEARTBEAT)推上雲端最新，但**這套架構是「pull on open」沒有伺服器主動推送**，ACER不被打開就永遠拉不到——這不是AI能遠端解決的，需要教練親自去那台機器開一次Claude對話框。詳見[[project_acer_dormant_49days_2026-08-26]] |
| ✅ | **孔大哥/佩佩老師AI人設備份(kong/peipei)已各自開獨立private repo並推送成功** | ✅2026-08-27完成 | 教練當場拍板「去解決啊，問我幹嘛」。查明真根因：kong/peipei的origin遠端誤指向跟主`workspace`同一個`mac-openclaw-workflows`репo，兩邊commit歷史完全不相關（kong本地7筆 vs origin/main 7903筆），push必被拒、若強推會有覆蓋主repo風險。已用`gh repo create`開兩個新private repo（`kong-ai-backup`／`peipei-ai-backup`），改remote後推送成功，雲端備份正式生效。 |
| ✅ | **VPS(43.245.60.200)git repo補齊.gitignore+意外發現並修復憑證檔案owner錯誤新bug** | ✅2026-08-27完成 | 已補`.gitignore`排除`scripts/fb_session_data/`瀏覽器快取並`git rm --cached`取消追蹤。過程中push一度失敗「could not read Username」，查證發現`/home/node/.openclaw/.git-credentials`被誤改成root持有(600權限)，git實際跑在node使用者下讀不到，跟[[reference_vps_git_dubious_ownership_silent_failure]]同一種形狀的新發作。已`chown`修正owner，merge+push成功(commit`7c76d31e5`)。 |
| 🟡 | **stop_rules_master.py規則D（輪詢偵測）regex覆蓋面不夠，這次同義改寫繞過去** | ⏳待軍師找時間動手 | 2026-08-24第6次「定時輪詢vs事件觸發」教訓時發現：這台Mac本來就有防呆機關會攔「每.*分鐘.*檢查」「cron.*輪詢」這類措辭，但這次我寫「每5分鐘掃一次」「每15分鐘查一次」全部同義改寫繞過，機關形同虛設。需要把`scripts/stop_rules_master.py`規則D的regex擴充成涵蓋更多同義動詞（掃/查/讀取/巡邏/處理），詳見[[feedback_event_driven_not_polling_pattern]]2026-08-24第6次發作段落。 |
| ✅ | **ezPay BNI台南南區入會/續約發票18張全數開立完成** | ✅2026-08-24晚~08-25凌晨完成並逐張查證 | 商店代號337391376（聚寶盆商業顧問有限公司），自訂編號082401~082418。第一批12張：10位入會$39,800+2位(徐偉倫/柯炫任)續約$26,800，查重複時只有柯炫任查到去年入會舊紀錄，教練確認「去年新會入今年續約」非重複照開。第二批6張續約$26,800（王聖凱/吳志煒/林尹渰/陳俊源/黃鑫豊/薛如媛），查證均無$26,800重複紀錄；查到3人有2025年$36,000入會舊紀錄（吳志煒/薛如媛/陳俊源），另查到林尹渰統編有一筆備註對不上姓名的舊紀錄，教練確認是分會轉會(真富→真鑫)+公司舊稱造成，非資料錯誤。所有查重複皆用XHR攔截讀取8季度、192筆去重後的真實資料比對，非用猜的。完成清單`claude-brain/data/ezpay_bni_membership_invoices_2026-08-24_12張完成清單.json`+`ezpay_bni_renewal_invoices_2026-08-24_6張完成清單.json`。教練當場問今年/去年開票總額，用同套XHR方法查出今年(1-8月)$1,882,890、去年全年$3,240,000（含1張已作廢$26,000未列入）。已寫入記憶`reference_bni_membership_fee_history_and_chapter_transfer`（入會費逐年調漲36000→39800，備註對不上先假設分會異動不是錯誤）。 |
| 🔴🔴🔴 | **Netlify額度追蹤SOP兩度修正：從估算失準→改每次都查→教練推翻改7~10天校正一次** | ✅2026-08-25完成，教練親自拍板校正頻率 | 查真實帳單頁(`app.netlify.com/teams/bymyway7/billing/general`)發現舊估算值(849.5/1000)跟真實餘額(76.4/1000)嚴重脫節，真實只剩約9次部署額度(147點)。第一版SOP寫「每次部署都要查真實頁面」，教練當場推翻：「這種每一次都要進去查的思維你要打斷，非常不智慧，會耗token+要教練登入」，改拍板**每7~10天校正一次，日常用15點/次估算法即可**。帳單週期確認是每月25日重置(非教練口頭講的24日，24日是週期最後一天)。下次校正約2026-09-01~09-04，或估算值≤3次時提前查證。完整SOP見[[project_netlify_deploy_quota_2026-07]]。**教練同場提出最高目標宣言**：AI要像鋼鐵人賈維斯——記得教練說過的每句話並自動串連，不用重複交代，已寫入[[feedback_jarvis_outcome_delegation_style]]。 |
| ✅ | **小龍蝦派工機制+自動化工具四支，全部依教練覆核意見修正完畢** | ✅2026-08-24完成 | 教練逐項核對凌晨的稽核報告後三處覆核：①08:25發票對帳daily cron移除，改按需觸發(教練:發票是一兩個月才開一次的階段性任務)②派工worker從cron定時(5分鐘→15分鐘)整個改成掛在「開工」hook後面觸發，完全移除排程，教練不開工Mac不會為此做任何事(commit`a673c8d97`)③8/17~23報名數字疑慮已用log對DB逐筆比對19筆全部吻合，確認38人無漏記，非用猜的。OpenClaw已實測升級2026.6.33→2026.6.34，5項健檢全過。 |
| ✅ | **台中場報名通知已上線+Netlify帳號大掃除(54→39個站台)** | ✅2026-08-24完成，教練親口「推」確認 | 教練貼出台中場既有GitHub Pages路徑即為Netlify正式站名，已建站`ai-forum-taichung.netlify.app`上線(deploy`6a8bea15`)。教練逐條看過Netlify後台後指定12個測試/廢棄站台+2個追加站台(fluffy-puffpuff-b5a65b空頁面/tree-coach-book舊電子書原型)刪除，過程中教練抓到我的疏漏——`xiaolongxia-notify`(通知佩佩老師)/`sme-register-fn`(通知教練)兩支舊LINE轉發路徑跟稍早「全面改Telegram」是同一件事沒清乾淨，已從`bigtree`+`ai-talk`兩repo原始碼移除並推上GitHub+manual zip部署Netlify正式站(deploy`6a8bed91`+`6a8bed9c`)，兩個舊站台也一併刪除。**站台數最終54→39**。**教訓**：`bigtree`/`ai-talk`是「推GitHub不會自動觸發Netlify」的手動zip部署型，即使`web_preview_verify_guard.sh`把它們列在「push即上線」清單也只是保守防呆，不是真的自動部署——需要另外手動zip+API才會上線，兩者不衝突。 |
| ✅ | **「活動討論群」開放AI自動接話+建立獨立記憶檔+彙整時完整灌回** | ✅2026-08-24完成並實測 | 教練把新建的Telegram活動群組(chat_id`-1003537129853`)設定成不用@提及、誰講話AI都自動接。**用inbound_echo log直接查到chat_id，全程沒開瀏覽器沒截圖**(呼應[[feedback_exhaust_own_tools_before_asking_coach]]同精神，這次用讀檔查證取代電腦操作)。教練接著要求群組要有獨立記憶——長時間討論攤販/廠商/idea後會說「幫我彙整」，若只靠agent自己的對話記憶(可能因context太長被壓縮/重啟)會漏掉討論前段。新建`hooks/group-activity-memory`：走`message:preprocessed`，①每則發言即時落地`workspace/group_memory/活動討論群.md`②偵測「彙整/整理/統整/總結/摘要」關鍵字時把整份記憶檔用`ctx.inject`灌回當輪context。9案例測試全過，補登hook建立前已發生的3則對話，gateway重啟後hook數16→17確認生效。commit`cba97a00`(hook)+`e035318c2`(記憶檔)。 |
| ✅ | **3支孤兒hook已啟用（bni_tainan／BNI大台南小幫手專用）** | ✅2026-08-27完成並驗證 | 教練問清楚「是哪一支帳號」後當場拍板。三支都掛在`bni_tainan`（BNI大台南小幫手LINE）：①`bni-member-directory-map`純記錄LINE user ID對照真實姓名，不影響回覆②`line-delivery-fallback`回覆送達失敗自動補送一次，避免訊息默默消失③`line-url-typo-guard`送出前自動校正網址錯字，避免會員點到404。三支性質都是防護網、不新增對外行為風險。已寫入`openclaw.json`+重啟gateway，log確認`loaded 21 internal hook handlers`（18生效條目+3新增），commit`446b6ba0`。 |
| ✅ | **台中場(9/23-24)報名通知已上線+場次辨識修復+概念稿標示移除+作品總覽同步** | ✅2026-08-25完成，教練親口「推」確認 | `feature/registration-notify`分支(commit`4c7556b`)已merge進master推上GitHub Pages+Netlify雙平台。教練實測發現Telegram通知場次全顯示「AI微論壇」分不出嘉義/台中DAY1/DAY2，查明event.db三場活動同名，改用`location+event_date`組成標籤(commit`f34d9fbc5`)，如「AI微論壇（台中場・09/23）」。教練接著指出網頁還留著「概念稿」字樣(title/meta/頁首橫幅/CTA/頁尾共5處)，既然已正式上線就拿掉，已清除+順手砍掉孤兒CSS，重新推GitHub+Netlify。**新SOP**：教練當場拍板「推GitHub測試/推Netlify都要同步更新作品總覽(coach888)」，此站已補進「大樹常用」區(從「不公開個人檢索」區搬過去)，詳見[[project_portfolio_netlify_github_logic]]。 |
| ✅ | ~~OpenClaw 2026.6.33 → 2026.6.34 升級評估完成，等教練決定~~ | ✅實際上8/24已升級完成，此列是沒更新的舊紀錄 | 2026-08-27查證`openclaw --version`確認系統**已經是2026.6.34**（跟npm extended-stable線一致，沒有更新的版本），這行待辦是v100左右升級完成後忘了刪的殘留紀錄，不需要教練做任何決定。原調查內容保留備查：6.34是extended-stable線的維護版（2026-08-04發佈，25個PR，官方明說「不加新功能，只做安全與穩定性修補」），其中兩項正好打中教練實際踩過的坑：①「retained session writes / provider fallbacks 不再靜默中止進行中的工作」＝8/20小龍蝦連兩次回「Agent couldn't generate a response」害發票資料消失的同款問題 ②「pending channel work resumes after recovery、acknowledgements are idempotent」＝訊息送達可靠性。另含相依套件安全更新。**風險評估**：官方預告7/24後移除`before_agent_start`等舊Plugin SDK API，已逐一檢查教練18支hook＋openclaw.json，**全部沒用到**，不受影響。⚠️唯一要留意的是`plugins.allow`是嚴格白名單（48個），若新版新增外掛會被擋掉，升級後要核對數字。`scripts/openclaw_upgrade.sh`已備好check/upgrade/verify/rollback四段，教練點頭就跑。**不要換到`latest`(2026.7.1-2)**——那是不同release line，版號大但發佈日期反而更早，換過去等於橫向跳線。 |
| ✅ | **報名通知三個靜默漏洞已堵死** | ✅2026-08-24完成並實測 | `/api/register`原本有三種情況會讓「有人報名但全世界都不知道」：①場次代碼對不上→直接return不通知 ②欄位缺漏→靜默丟棄 ③`_notify_xiaolongxia()`用`except:pass`吞掉所有失敗（跟燒掉教練一整週的LINE 429同款寫法）。現在前兩種照樣發Telegram並指名該去哪裡補，第三種會回傳成功與否並把失敗寫進`notify_failures.log`。新增`test_register_notify.py`，5情境全過、測試資料自動清乾淨。commit`69c93d8fe`。 |
| ✅ | **發票漏記根治：進來當下就落地，不靠agent記得** | ✅2026-08-24完成並實測 | 查明8/20那批消失的真相是agent context overflow重啟。新建`hooks/invoice-inbound`走`message:preprocessed`，agent掛掉也不影響落地。**過程中踩到並記錄的關鍵坑**：①觸發條件不能只認關鍵字——8/20真正掉的那則「連皓宇 /88ZMR73」全文零個發票關鍵字，只認關鍵字會原封不動重演同一個漏接，已改成載具形狀本身即觸發 ②hook光是「檔案存在+openclaw.json註冊」不會生效，必須有`HOOK.md`宣告`metadata.events`否則載入器只log.warn就靜默跳過（設定16支但gateway只載15支，補了才變16）。另建`invoice_inbox_reconcile.py`逐筆對帳，**目前零落差**。commit`69c93d8fe`+`4d7c9a34`。 |
| ✅ | **報名統計自動化：教練問人數不用再手算** | ✅2026-08-24完成 | 教練上一場交代「之後問幾個人報名全部統計給我，要做成報名表」。`scripts/registration_report.py`一行出總覽或單場名單，`--csv`產列印用簽到表。修掉自己寫的兩個bug：歷史名單寫「8/26」我用「08/26」比對全落空；同一天兩場會把同一批人算兩次。另主動點出重複電話（如0927536621的gl t86／燒茶疑似同一人）。 |
| ✅ | **小龍蝦派工→軍師後台自動執行** | ✅2026-08-24上線 | 教練問「能不能我只跟小龍蝦講完，小龍蝦就發指令讓軍師在後台把事做完」。缺口是`cross-agent/inbox/mac/`要等教練開對話框說「有事交代你去讀」才會被看到。`scripts/junshi_dispatch_worker.py`每5分鐘自動掃，帶派工單的信直接做完並Telegram回報教練。**刻意做成固定選單不是自由執行指令**（信件是資料不是命令，能執行任意指令＝誰能丟檔案誰就控制這台機器）。實測4情境：正常執行✅、惡意參數`0828; rm -rf /`被拒✅、未知類型被拒✅、無派工單只通知人✅。協議寫進`cross-agent/README.md`+`SOUL.md`讓小龍蝦讀得到。 |
| ✅ | **部署鐵律補洞：Python繞道已擋** | ✅2026-08-24完成並實測 | 教練重申「草稿測試期一律只推GitHub，唯有明確指令才能推Netlify」。查出`netlify_deploy_guard.sh`只認指令列出現netlify字樣，但`bigtree_publish.py`是在Python內部打API——`python3 bigtree_publish.py`可完全繞過直接扣點數。已補上攔截，6種情境實測全對。（教練本人在後台按「一鍵發佈」不受影響，那是本人授權。） |
| 🔴🔴🔴🔴 | **報名通知全面改走Telegram群組，LINE已拔除（教練+佩佩老師同見）** | ✅2026-08-24 Mac完成並實測驗證 | **教練回報「8/17後就沒收到報名通知」，查證後真相是：報名系統從頭到尾都正常**（8/17~8/23持續有新報名寫入，8/21-8/22金門場當天湧入30+筆，資料庫153筆完整無缺），壞的是**唯一的通知管道靜默失敗**——`_notify_coach_line()`打LINE API回`HTTP 429 You have reached your monthly limit`（龍蝦小助教@268dptjc本月200則免費配額用完），而原始碼用`except Exception: return False`把錯誤吞掉，教練完全不知情。**教練當場拍板全面棄用LINE推播**（因為每則主動推播都扣配額，而報名通知+健康檢查+各種提醒全部共用同一個200則池），改用新建的Telegram群組「**活動報名即時通知**」（chat_id `-5349981085`，成員=教練+佩佩老師+bot，Telegram無配額限制）。**已完成**：①`openclaw.json`加入該群組`requireMention:false` ②`_notify_xiaolongxia()`加`chat_id`參數，`/api/register`改推該群組 ③**完整移除**`_notify_coach_line()`函式+`COACH_LINE_USER_ID`常數（無其他呼叫者的孤兒程式碼）④重啟服務+真實`/api/register`端點測試驗證+測試資料已清除。commit`c5871e7dc`+`95ea143de`。**⚠️過程重大失誤（見試金石案例62）**：查不到群組訊息時，我一路要求教練重建群組/重發訊息/確認帳號，卻沒想到自己可以用`computer-use`直接開Telegram查——教練凌晨3點被迫當搬運工，親口重話「明明你能力範圍內能做的事，非得叫我當搬運工，完全違反守則」。真根因是**新群組未登記於白名單時`requireMention`預設true，訊息被靜默忽略、連log都不留**，我用`@openclaw_macbook4_bot`提及測試才抓到chat_id。**下一步**：教練要求「之後問報名人數要直接統計給我，不用手動算，要做成報名表」——資料都在`event.db`，隨時可查可產出清單。 |
| 🎯🎯 | **大樹小講場次管理後台＋一鍵發佈上線（教練可自行增修場次，不必再透過AI）** | ✅2026-08-23 Mac完成，教練已實際操作驗收（過程修好2個部署bug，見下方新增列） | 教練創意發想：想要一個能自己管理大樹小講活動的後台（新增/編輯/刪除/發佈、完成的自動列入歷史、一鍵部署不用AI確認）。**軍師判斷不新建系統**——`event.bymyway.com/admin` 早就是完整Flask後台（登入/場次/名單/簽到/抽獎，24小時跑在Mac上），真正的病根是**同一份場次資料同時存在「網頁原始碼的SESSION_DATES」與「event.db」兩份、各自維護**，8/22改期出包就是漏在這裡。做法：①`events`表擴充`site/slot_key/location/venue/address/transport/status`欄位，官網16場全部匯入資料庫當唯一真相源（順便補上8/26早半場一直缺的slug，那場原本根本無法雙寫報名）②既有後台新增「大樹小講場次管理」頁(`/admin/sessions`)：新增/編輯/刪除/設為已取消/草稿，有報名紀錄的不給刪只能設取消(防孤兒資料)③**過期場次自動歸入「已結束」**，且官網前端也會自動收起(不用等發佈、不用教練手動關閉)④`bigtree_publish.py`：資料庫→產生SESSION_DATES→git commit/push→Netlify部署，一鍵完成⑤**教練本人按發佈＝本人授權，不再需要AI逐次確認**(原規矩是防AI自作主張，非防教練本人)。**安全設計**：金鑰存`credentials/`(已加.gitignore實測git看不到)；打包改用`git archive HEAD`只送已提交內容，避免夾帶工作區未確認修改(原本用`git ls-files`會把biz-gym未確認的907行變更一起送上線)；已發佈內容用SHA256指紋比對，重複按不浪費額度；網頁結構異常時中止而非照舊部署。已測CRUD全流程/撞名防呆/有報名不給刪/狀態切換/發佈偵測/結構壞掉中止/頁面渲染。commit`bde5ae160`。**下一步**：教練說之後要「所有活動都歸後台管理」(不只大樹小講)，等這套用順了再擴充；`ai-fit`這類單一活動微站尚未納入。 |
| ✅ | **bigtree-tw排序修復已上線＋一鍵發佈系統修好2個真bug＋通知系統補強** | ✅2026-08-23全數完成並教練驗收 | 教練首次用新後台按「一鍵發佈」連續失敗2次(白扣2次額度)，逐步查證修好：①第一次誤診為zip中文檔名UTF-8旗標問題，改用Python zipfile打包卻沒設目錄項，Netlify解壓失敗 ②第二次拿08-22實測成功的包逐項diff比對才找到真因是「缺目錄項」不是編碼，改回`git archive HEAD`+系統`zip`指令(與08-22成功組合完全一致)並在送出前驗證結構相符，commit`99ceb9cf5`終於成功，官網14場排序正確上線。**教訓寫入`feedback_netlify_headers_content_type.md`第7條**：有已知成功樣本時先diff不要靠推論。同場教練回報LINE群發「發送失敗」，查證是@qaw8118h帳號本月200則免費額度用完(非bug)，`/admin/notify`新增即時額度顯示+「未綁定名單一鍵複製連結」功能(commit`b3a6900d9`)，讓教練能繞過額度限制用簡訊等管道接觸8/21+8/22兩場49人中29位未綁定LINE的人。教練接著提出「掃碼時強調一定要發訊息」的解法，已在4個觸點(2張現場立牌+2個掃碼後網頁)加上紅底警語「務必按LINE傳送」，thanks.html誤導性的「一鍵傳送」文案也一併修正(commit`0753e0e41`)。**待辦**：現場立牌已印過的舊版沒有新警語，教練需自行決定是否重印。 |
| ✅ | **大樹小講8/25台南場改期9/22+場地改台南安平維悅酒店** | ✅2026-08-23 Mac完成，教練親口「推」確認部署 | 教練口頭指示：原三道門文創旅店午半/晚半兩場整場改期，場地換成7/29 AI微論壇辦過的台南安平維悅酒店(台南市安平區慶平路539號，WebSearch查證)，時間/收費不變。已同步修改3處：①`bigtree/index.html`的SESSION_DATES(日期/場地/slug由bigtree-0825-*改bigtree-0922-*)+報名成功匯款提示判斷條件 ②`event-signup/event.db`兩筆events紀錄同輪更新(連動鐵律) ③額外發現的獨立微站`ai-fit`(GitHub Pages，整站專為這場活動做的宣傳頁)也一併全面更新：meta標籤×6+4處場地資訊卡+深連結`?session=`參數，「台南火車站步行約5分鐘」改成「飯店備有停車場」(維悅酒店在安平區非火車站旁，沿用ai-talk repo記載的同一場地既有真實資訊)。本機http.server+真實Chrome雙頁預覽教練確認後，bigtree commit`d95e8b3`+Netlify部署`6a8a41083645a490f9217ee2`、ai-fit commit`080ca32`+GitHub Pages皆已curl驗證上線。**發現並回報**：原8/25已有4筆歷史報名(高毓璟/鄭守晴/陳佩君/李崇源，8/14 LINE通知backfill)，教練確認自行聯絡通知，AI未動這批資料。 |
| ✅ | **bigtree-tw報名雙寫缺口已修復並上線** | ✅2026-08-22 Mac完成，教練親口「推」確認部署 | 查明真相：8/14曾在本機commit`3130b93`寫好雙寫程式碼(`BYMYWAY_API`常數+`submitRegistration()`的slug fetch)，但**這個commit從未推送到GitHub**——8/18另一台機器在(缺這段程式碼的)origin/main基礎上加了8/26早半場「晨光美學」+地址4樓修正並push(`16c2981`)，兩邊分岔超過一週沒人發現，Netlify正式站(`git archive HEAD`部署)因此從未真正跑過雙寫邏輯，這正是雲端8/21session查到「index.html從未出現slug/api/register」的真正原因。修復：`git merge`兩邊(保留新場次資料+救回雙寫邏輯)，用`event.db`查到的15個真實slug(`bigtree-0821`~`bigtree-1207`)逐一核對全部相符，新增的8/26早半場暫無對應slug(依既有`if(slug)`安全設計不影響其他場次)。本機http.server+**真實Chrome**預覽(`open -a "Google Chrome"`)給教練看過，merge commit`78d971a`已推GitHub，Netlify部署`6a89bc69126dab54a5fa417d`已上線，curl驗證正式站HTML含`BYMYWAY_API`/`bigtree-0826`/`晨光美學`三項關鍵字+Content-Type正確。**教練同時確認雙通道策略**：先保留LINE(Netlify sme-register-fn/xiaolongxia-notify)通知觀察一段時間，確認bymyway.com這邊真的穩定收到報名後才會下令拔掉LINE，不是這次上線就直接切單通道。下一棒觀察：教練若回報收到新報名的bymyway通知，可詢問是否已可安排拔除LINE。詳見`knowledges/2026-08-21_bigtree報名雙寫缺口調查_金門場報名數異常.md`(根因調查)。 |
| 🟢 | **event-signup新增「展示用快速切換列」，簽到/轉盤/後台三頁互跳** | ✅2026-08-22 Mac已pull+重啟服務生效，curl驗證`/checkin`出現三顆按鈕 | 教練反映現場講座展示常要在3個網頁間切換很麻煩，希望同一頁內能直接跳轉。已在`/checkin`、`/wheel`、`/admin`三個範本(`templates/checkin.html`/`wheel.html`/`admin.html`)加共用元件`templates/_presenter_nav.html`：右下角固定小工具列，三顆圓形按鈕(📷簽到／🎡轉盤／⚙️後台)點了直接跳轉，不用另開分頁找網址。已用Jinja2本機解析驗證三個模板+include都能正確載入無語法錯誤，commit`bc31134`已推main。**這是雲端session不確定教練說的「後台掃描報到/滾輪掃描報到/後台滾輪」精確對應哪3個網址下的合理猜測**(對照到`/checkin`+`/wheel`+`/admin`)，Mac那邊部署後教練實測若發現不是他要的3個頁面，直接說要哪幾頁、我再調整`_presenter_nav.html`裡的3個連結即可，改起來很快。**部署步驟**：`cd ~/.openclaw/workspace && git pull`，`launchctl kickstart -k` 重啟 `com.coach.event-webapp`（或教練慣用的重啟指令），重啟後訪問`/checkin`確認右下角有出現三顆按鈕即代表生效。 |
| ✅ | **ezPay培訓費「38人」批次全數結案：最後8張已開立完成** | ✅2026-08-24完成並逐張查證 | 剩下的8人(杜亞洛/劉彥彬/莊政川/林佳慧/陳新典/吳玫萱/謝盛峰/柯炫任)資料全數到齊，教練下令後Mac逐張開立(自訂編號081925~081932)並用`search_invoice`查證「已開立」，合計$3,600。連同8/19已開的24張，全批32張結案，完成清單見`claude-brain/data/ezpay_training_invoices_2026-08-24_8張完成清單.json`。**已建立完整ezPay開票SOP**`feedback_ezpay_invoice_sop.md`（教練要求「像網頁推SOP一樣」），六步驟含連線裝置isLocal:true鐵律+欄位ID對照表+含稅checkbox陷阱+form_input中文亂碼警告，下次開票不用再重找線索。 |
| 🔴🔴🔴🔴 | **claude-in-chrome連線卡到裝置問題，教練三度動怒，isLocal:true鐵律已寫死** | ✅2026-08-24已修復並寫入SOP，永久提醒 | 開票前連線一直卡到教練Windows裝置的殘留連線(isLocal:false)而非教練實際在用的Mac本機Chrome，導致教練完全看不到我在操作什麼，連續多輪誤會+教練動怒。**根因**：Mac本機Chrome擴充功能斷線，不是沒裝。**修法**：`osascript -e 'tell application "Google Chrome" to quit'`關掉整個程式再`open -a "Google Chrome"`重開，重新配對後選`isLocal:true`的裝置即可，教練親口拍板「這台電腦永遠都是第一個，不用再問」。任何機器下次遇到claude-in-chrome連不對，直接照這個SOP做，不要再截圖問教練或推給教練操作。 |
| 🟡 | **BNI培訓紀錄總資料庫：私有開票後台要不要做成真正網址+登入** | 🔒卡住-等教練 | 2026-08-17聯想本場從零建置。目前後台(`claude-brain/data/bni_training_admin.html`)只是本機檔案，含統編/電話/email等會員個資，教練問過要不要部署成網址+寫進coach888(帳密Admin/88888)，AI主動指出風險(coach888是公開repo，寫進去等於帳密全公開；且Admin/88888是已知弱密碼)，**教練裁示「先不要動」**。下次教練若想清楚要怎麼保護(不公開URL/真伺服器登入/接受風險)，直接照裁示做，不用重新提risk。詳見[[project_bni_training_records_db_2026-08-17]] |
| 🟢 | **BNI培訓紀錄總資料庫：v116大量資料精準度修正+MSP時段投票新網站** | ✅2026-08-18本場完成，詳見v116 | 教練逐輪核對排行榜異常，抓到根因不是官方漏登記而是會員自己key單類別選錯，系統性掃描全部「董事培訓」記錄的56個日期比對月曆，只有真的錯的才改，查不到的誠實回報不亂猜。另建置全新「MSP培訓時段投票網頁」(Netlify Functions+Blobs)並上線，過程中**犯了流程錯誤**：推正式站前跳過教練親口確認關卡，已被教練當場糾正+寫入記憶`feedback_skipped_web_push_sop_2026-08-18`，下一棒切記任何要推正式環境的任務都要先查SOP+給教練看預覽+等親口說「推」。 |
| 🟢 | **大樹教練照片換新（mentor100 + AI微論壇台中場9/23-24）** | ✅2026-08-17完成 | 教練用LINE傳了一張較清晰的正式照(`~/Downloads/1775414250751(1).jpg`)，要求換掉mentor100跟原先誤講的「828」網站。①mentor100(id=4)：DB `photo_filename`改`speaker-dashu-baa91d2d.jpg`，舊檔已刪除不留孤兒，服務重啟後curl驗證新檔已生效 ②教練隨即更正「828不用改，改9/23-24」：828站(`ai-talk`)的改動已用`git checkout`還原，改對`ai-forum-taichung`(9/23-24台中場GitHub Pages)套用同一張照片，commit`7ac6b0e`推送後curl確認GitHub Pages build完成、新照片(633×631)已對外生效。三站台皆用同一套處理邏輯(EXIF轉正+最長邊900px+JPEG quality88)，未動其他講師照片或版面 |
| 🔴 | **ezPay培訓費發票：3張(蔡珮彤081907/吳亞平081922/楊凱為081924)Email欄位空白待補發通知** | ⏳待教練重新登入ezPay | **0818批**(v120)：18張(081701~081718)。**0819批**(v121)：24張(081901~081924)。42張皆用XHR攔截器讀真實回應+`search_invoice`複查confirmed存在，完成清單見`claude-brain/data/ezpay_training_invoices_2026-08-1{8,9}_*完成清單.json`。**其中3張開票時Email查無登記留空**，教練糾正後查證確認是比對疏漏非真的沒有：蔡珮彤=CSV「蔡姵彤」(同音異字)、吳亞平純漏看、楊凱為=CSV「楊為凱」(姓名顛倒，教練已確認同一人)，3人正確Email已找到並補進`knowledges/2026-08-18_38人培訓發票二聯三聯資訊蒐集中.md`，**下次ezPay登入後用「查看/補發」功能補上這3張的Email重發通知**。剩8人(杜亞洛/劉彥彬/莊政川/林佳慧/陳新典/吳玫萱/謝盛峰/柯炫任)待補資料，到齊後自訂編號從081925接續不用等全部到齊。技術SOP(MerchantID假成功陷阱/`jQuery trigger`送出法/手機條碼斜線前綴/同音字比對鐵律)已固化於`reference_ezpay_invoice_issuing_procedure.md`+`路徑大全.md`第四(續)節 |
| ⬜ | ~~ezPay電子發票開立作業，教練裁示以後交給聯想機器做（2026-08-16教練親口指示）；108個統編備註查詢已完成~~ | ✅已由上一列取代結案 | **2026-08-17 23:30 Mac已完成**：238筆歷史發票篩到163筆B2B去重至108個不同統編，逐一查詢發票明細modal核備註欄，108/108全部查到，存於`claude-brain/data/ezpay_invoice_remarks_108taxid_2026-08-17.csv`，commit`dbd55d47d`（此列先前一度被另一場session的待辦表整批更新覆蓋回舊版文字，本次重新校正）。技巧見下方⚠️。開立新發票（非查詢）仍照Mac本場(2026-08-16)已實測跑通完整SOP：①開立發票用`https://inv.ezpay.com.tw/Invoice_issue/create_invoice`，②查詢舊發票用`.../Invoice_issue/search_invoice`(查詢期間最長3個月，超過會跳原生`alert()`卡住整個分頁，務必先`window.alert=function(){}`覆蓋掉再操作，卡住時用`navigate`或`get_page_text`嘗試恢復，不要用截圖) ③商店固定是「(337391376)BNI台南南區」，品項多半是`B02`/`BNI續約`(續約$26,800)或`B01`/`BNI入會`(入會$36,000~39,800，價格教練口頭給的跟系統舊紀錄可能有出入以教練當下說的為準) ④自訂編號規則＝當天日期MMDD+兩碼流水號(教練親定，如0816**01**代表8/16第一張，開立前**務必**先查當天有沒有人已經開過，避免號碼撞號) ⑤買受人是公司行號(B2B)時，把該會員所屬BNI分會+姓名寫進「發票備註」欄(格式`分會名-會員姓名`，例：`真鑽-蘇志揚`)——**這是查會員舊發票對應買受人統編的關鍵**，統編本身查不到會員姓名，姓名只在備註欄，開立前可用「查看/補發」連結開發票明細modal核對備註+Email+金額 ⑥**單價/數量欄位程式化填值容易不觸發站方JS計算**：用`form_input`或直接改`.value`常常算不出稅額，务必用真人打字方式(triple_click選取+type輸入)或JS呼叫`element.click()`(不是只改`.checked`+dispatch `change`事件)才能穩定觸發計算，送出前一定要讀`TotleAmount`欄位數字核對是否等於教練講的金額，兩次都出現金額算錯(28,140而非26,800)的狀況都是這個原因 ⑦**送出「確定開立」按鈕id是`create_btn`**，點擊後有時分頁會短暫卡住(像是原生對話框或整頁reload)，屬正常現象，等1~2秒後查`Invoice_issue/search_invoice`用自訂編號或統編搜尋確認發票真的建立成功，不能只看表單有沒有清空就當作成功(本場宋映璇那張表單清空但發票其實沒建立，重試一次才成功，教訓：**每張發票開立後都要回頭查證存在，不可省略**)。完整過程細節見本場對話記錄，聯想那邊沒有等效記憶檔可讀，需要重新走一次才會摸熟，此段落就是濃縮版SOP |
| 🟡 | **AI微論壇台中場(9/23-24)網頁概念稿：彭晉澄申請已處理，等他自填資料** | ⏳待彭晉澄自填+教練確認GitHub Pages概念稿 | 新repo`ai-forum-taichung`，GitHub Pages：https://coach1973.github.io/ai-forum-taichung/ 。多輪迭代：兩天套票2988元(單日1800)、大樹教練固定排每天下午第一堂並各有專屬分享主題(只出一張嘴叫AI做事/如何將AI導入LINE成為你的生活小幫手)、場地沃茲新創空間忠明館(台中市南屯區忠明南路478號B1)、報名費含午餐+下午茶、藍新金流付款連結已接上。講師資料從mentor100撈取：JC老師、Lavi(全站已統一英文名，含2026-08-16修復時間軸殘留)、廖韋評皆已補齊簡介/照片/連結。王俊甫查證發現mentor100照片其實是FB預設空白大頭貼截圖、簡介只有姓名重複，已請教練協調補件，同步在mentor100後台改為草稿不對外顯示。**彭晉澄2026-08-16已送出mentor100申請，已建草稿+編輯連結交給教練轉發**，等他自己填完+教練後台預覽確認才算補齊。Lavi主題2026-08-16改為「AI× Canva：把專業轉譯成「看得懂、記得住、願意買」的品牌圖文」。下次開工先問教練彭晉澄填完了嗎、GitHub Pages概念稿整體看過沒問題了嗎，沒問題才能推正式站 |
| 🟢 | **mentor100後台/admin頁500錯誤修復+新增「改為草稿/已發佈」一鍵切換功能** | ✅2026-08-15本場完成 | 教練回報`mentor100.bymyway.com/admin`當機Internal Server Error，查log抓到根因：`db.delete_mentor()`只刪mentors記錄，沒同步清理applications表的孤兒外鍵(教練刪除id69導師後，申請名單裡仍有一筆指向已刪除記錄，模板嘗試組連結時BuildError)。已止血(清空壞資料)+根治(delete_mentor()同步清空關聯外鍵+模板判斷改用`not a.edit_token`更穩健)，用真實app物件完整模擬render_template()驗證通過，commit`87031ec`。教練接著要求後台要能自己把已發佈的講師改回草稿(某些是教練先建好架子但講師本人還沒補資料)，原系統完全沒有這個功能入口，已新增`toggle_mentor_status()`+新route+列表頁一鍵切換按鈕，commit`23304df`。王俊甫已依此改為草稿 |
| 🟢 | **mentor100「種子」標籤依教練指示重新盤點** | ✅2026-08-15本場完成 | 教練要求AI微論壇/7-29場/8-28嘉義場有實際擔任講師的才標種子，其餘(含教練手動建立的)都不算種子。已查證3個活動講師名單並更新，目前種子14位：7/29場3位(王彤/蘇秦/燒茶林祥禔)+8/28嘉義場3位(季哥/洪詠清/林韋銘)+AI微論壇台中場8位(大樹教練/施育廷/曾思遠/李中閔/JC老師/廖韋評/Lavi/王俊甫)。彭晉澄因mentor100查無記錄暫無法標記，待教練補資料後一併處理 |
| 🟢 | **8月26日(高雄場)報名人數查詢：6人** | ✅2026-08-14完成 | 查`event.db`的`advance_registrations`表，原始7筆backfill記錄中2筆(gl t86/燒茶)電話號碼相同判斷為同一人重複報名，去重複後6人。已提醒教練這個數字只反映教練貼過的歷史通知文字，非即時查詢，雙寫系統上線後這場目前0筆新報名(signups表) |
| 🟢 | **品牌短網域go.bymyway.com上線+Cloudflare API Token申請完成** | ✅v109本場完成 | 教練想設定品牌短網域(參考PicSee)，查證發現`coach.bymyway.com`目前是VPS小龍蝦對外入口(43.245.60.200)，**PicSee原本指示要教練刪掉這筆A紀錄會直接打斷VPS小龍蝦服務**，已攔下並改用全新子網域`go.bymyway.com`(A→3.231.64.15，Proxy關閉/DNS only)，教練手動加好後curl+`dig`驗證DNS已生效、其餘21筆現有紀錄零異動。過程中Cloudflare新版介面「Welcome to new DNS experience」導覽彈窗擋住claude-in-chrome自動化點擊，教練親手點掉彈窗後才排除，已寫入記憶`feedback_browser_automation_ai_should_complete`。教練接著申請Cloudflare API Token(僅限bymyway.com的Zone:DNS:Edit權限)，已用`user/tokens/verify`+查zone雙重驗證有效，存進`路徑大全_憑證層.md`，往後DNS操作可直接下指令不用開瀏覽器。commit(workspace)`ce163eef9`+`3b50f6757` |
| 🟢 | **LINE三帳號個人記憶標準化：main/default頻道從未真正運作過** | ✅v108本場完成，已查證不需三機同步 | 教練被龍蝦小助教問「您是哪一位」動怒，查證抓到兩層根因：①people.md/USER.md漏登教練LINE ID②line-user-memory hook對main帳號sessionKey格式判斷有bug、從未真正運作過。兩層都修好+合成webhook實測驗證，commit`246e51766`+`d12bc391`。**2026-08-14查證更正**：原註記「三機同步：Windows/ACER待處理」是誤植——查`openclaw.json`確認三個LINE帳號(default/bni_tainan/jiaolian_thoughts)全部只在這台Mac mini單一gateway設定裡，Windows/ACER並未各自跑一份OpenClaw LINE gateway，git push（已完成）就是唯一需要的同步動作，沒有需要各機手動移植的PowerShell腳本或設定登記，此項結案 |
| 🟡 | **報名系統雙寫遷移bymyway.com＋官方LINE推播已補上，觀察期中，尚未拔Netlify** | ⏳教練親口裁示觀察期，等他確認收到幾筆真實報名再下令 | 教練發現線上報名資料完全沒有資料庫紀錄(sme-register-fn純轉發不落地)，裁示遷回bymyway.com。已建`/api/register`端點+15場session slug+bigtree前端雙寫，deploy`6a7e15b116b28f7990b3a616`已上線。**2026-08-14加碼**：教練指出bymyway那條路徑本身不會發通知(只存資料)，若拔Netlify會完全收不到報名——已補上`_notify_coach_line()`，`/api/register`報名成功時複用龍蝦小助教(@268dptjc)LINE token直接推播教練本人，commit`0fbe4902b`，兩層測試皆HTTP 200成功送達(直接呼叫LINE API+完整走production端點模擬報名)，測試資料已從event.db清除。**教練裁示**：「先保留，等有幾個報名，我確實兩邊都收到之後，再請你拔掉舊的Netlify網址」——下次開工先問教練是否已確認雙邊都收到，收到指令才能動手拔`sme-register-fn`。49人歷史backfill名單教練要用來印簽到表，查詢SOP見USER.md **🔴2026-08-21更正**：本列「bigtree前端雙寫已上線」這句話**經雲端session查證是錯的**，`bigtree/index.html`從未真正呼叫過`/api/register`(見上方新增的🔴🔴🔴🔴列)，這行記錄多棒以來都沒被抓到，此列狀態應視為「後端做好、前端從未接上」，不是「已上線觀察中」，真正待辦已移到本表最上面那列，此列保留當歷史紀錄不重複展開。 |
| 🟢 | **系統全面體檢六項修復（Mac hook + 小龍蝦排程）** | ✅2026-08-12完成 | 教練要求體檢「邏輯不對/重複/浪費資源/無效/衝突/可優化」的規則，Mac 端 25 支 hook 腳本 + 小龍蝦端 20 個 hook / 32 個 cron 全查過。六項全修：①時間注入 hook 每則重貼規則全文 → 每場只講一次（806→335 bytes/則）②Stop hook 12 支中有 10 支各自重讀同一份 transcript → 合併成單一總管 `stop_rules_master.py`（14MB 檔實測 1.111 秒→0.066 秒，快 17 倍；11 項情境與原版逐一比對行為一致）③`vps_polling_healthcheck.sh` 被 LaunchAgent 與 cron-daemon 各跑一次 → 移除 daemon 那份 ④自動 commit 過碎（8/8 實測 79 筆/92 筆）→ 備份複製維持 15 分鐘、commit 上雲改每小時 ⑤22:20 寄信提醒 10 個獨立一次性排程 → 1 筆 cron（日期鎖 8/12~8/21）⑥健康檢查每 30 分 → 每小時（一天 48 次 AI 呼叫降 24 次）。排程總數 32→23，原腳本全保留可回退。commit `aa8a5952a`+`a10af7c75`。**✅ 已用真實對話驗證，非僅測試腳本**：合併後同一場對話裡，教練下一句話就觸發 Stop hook，`stop_rules_master.sh` 正確攔下時間鎖違規（判斷邏輯與原版一致）——**證實原先猜測「settings.json 要開新視窗才生效」是錯的，實際是每次 Stop/UserPromptSubmit 事件當下即時讀取設定檔，同場對話內編輯完立刻生效**，已更正進記憶`reference_mac_hook_scheduler_architecture_2026-08-12`，不用再等開新視窗才能驗證 hook 改動。備份 `/tmp/settings.json.bak-20260812124802` 仍保留可回退。三機同步：Windows/ACER 端對應 hook 尚未套用這次合併，見 [[project_cross_machine_hook_sync_todo_2026-08-08]] |
| 🟢 | **coach888作品總覽表：大項標題+標籤改可直接編輯、六大項改兩欄並排顯示** | ✅2026-08-10~11完成 | 教練要求自己能改「常用/後臺」這類大項標題跟「待啟用/公開」這類標籤文字，仿照既有拖曳排序機制(contenteditable+localStorage+複製按鈕貼給AI固化)實作，commit`3b7ca65`。接著教練要求改成三排兩欄並排(一常用/二後臺、三對外公開/四不公開、五保留/六BNI)減少往下滑，commit`d1f8e21`，900px以下自動收回單欄不影響手機瀏覽 |
| 🔴🔴🔴 | **大樹小講(bigtree-tw)新增8/25台南場+場次名稱改時間制+event-signup後台同步連動+修復同日多場次路由bug** | ✅v106本場完成，8/25當天待實測 | 詳見下方v106完整戰果。新增8/25午半(14:00-16:30)/晚半(18:00-20:30)兩場，教練接著要求全站場次一律只顯示具體時間、拿掉早/午/晚/夜/全日等代稱(commit`8a6c699`+`cfa30d9`+`82ff888`)，教練「推」後已部署正式站(deploy`6a7a08d0e7c10ed04663c831`，額度45→44)。教練追問「後臺有沒有連動」，查證真的沒同步，補上`event.db`兩筆8/25場次(workspace commit`c3501af57`)，**過程中意外抓到真bug**：後臺auto路由原本同一天有多場次只認第一筆，會讓晚場來賓資料誤記到午場，已加`start_time`欄位+改路由邏輯修復，本機模擬多時間點驗證切換點正確(14:00/18:00)，已重啟`com.coach.event-webapp`確認無誤。**教練確立新規則：往後大樹小講新增場次，後臺event.db必須同一輪同步更新，兩邊連動**，已寫入記憶`project_bigtree_eventsignup_sync_rule`。測試報名通知管線送出「系統測試-請忽略」一筆確認API回應200，**教練請求刪除該則LINE測試訊息，但查證sme-register-fn純轉發不落地任何資料庫，AI沒有管道能刪教練LINE裡收到的訊息，此步驟教練需自行到LINE app手動刪除**，已寫入記憶`feedback_cannot_delete_coach_line_messages`提醒下次測試前要先講清楚 |
| 🟢 | **LINE VOOM備份下載+解壓縮到E碟** | ✅2026-08-10聯想完成 | 教練因LINE VOOM 9/30停用，下載官方備份（65個分割zip，密碼保護）。過程協助教練逐一核對缺件/重複下載清單多輪，全數65個到齊後用7-Zip(新裝)全部解壓縮到`E:\LINE VOOM`(21GB，2847則貼文，完整性測試0失敗)，確認無誤後刪除D碟65個原始zip。無commit(純本機檔案操作，非git專案) |
| 🟡 | **Zoom C碟即時資料junction連結到E碟已失效** | ⚠️教練裁示不修 | 查證發現[[試金石案例51]]事故後建的junction已失效(推測被Zoom更新/重裝覆蓋)，即時資料(403MB)目前只在C碟沒同步E碟。教練確認「資料量小、增量也不多，就不管它了」，明確裁示不修。已寫入記憶`project_zoom_c_drive_junction_broken_accepted_2026-08-10`，往後不用主動提醒 |
| 🟡 | **聯想C碟WinSxS系統元件庫可再瘦身** | ⏳待教練回覆 | 教練要求清C碟暫存檔為一鍵備份省空間，查證發現C碟已因7/11大瘦身很乾淨(這個月只胖回5.6GB)，真正暫存垃圾(<0.3GB)可忽略，唯一有意義的空間是WinSxS(7/11清過11.17GB，現又長回16.26GB)，用官方DISM工具可再省4~5GB。教練尚未回覆要不要執行 |
| 🟢 | **聯想2026-08-10一鍵備份驗證：確認只留最新一份無殘留** | ✅2026-08-10完成 | 教練做完一鍵備份後要求確認，查證E碟只有一份「易數一鍵還原Windows系統備份（不要刪除）」(85.36GB，BootImage.pmf+SystemImage.pmf皆為8/10當天檔案)，之前3月的舊版本已被取代不再存在，符合教練預期 |
| 🟢 | **event-signup：簽到+抽獎登記合併成單一介面，通用QR立牌上線** | ✅v105本場完成 | 詳見下方v105完整戰果。核心改動：`/checkin`不再顯示「已完成線上報名」中繼畫面，改標「我要參加抽獎」，填手機送出同一步直接跳轉LINE完成binding+抽獎登記(commit`7227e1812`)；新增通用版「掃碼玩抽獎」QR立牌`qr/wheel-print.html`取代單場活動專屬立牌(commit`dc90140e3`)；後台場次已同步大樹小講8/21+8/22+8/26+8/28四場(DB直改，不進git)。作品總覽表同步更新3次(改名/改連結)，commit`ef8e6a6`+`7bc25f5`+`0d80f93` |
| 🟡 | **bni-chapters：「真誠分會」網頁主架構問題** | 🔒卡住-等教練說明 | 教練提出要處理，但還沒說明具體是哪個架構問題，下一場先問清楚再動手 |
| 🟢 | **bni-chapters：後台社群／外部連結新增「編輯」功能** | ✅2026-08-09完成 | 教練回報FB/LINE/聯絡我們只有新增刪除、缺編輯，得先刪再建。已補`db.update_link()`+`/links/<id>/edit`路由+模板改成可直接編輯label/url。已重啟服務+登入實測更新真的存進資料庫(改完再改回原值，沒留測試假資料)。commit `3a5ae8e4` |
| 🟢 | **mentor100：申請名單UI優化+姓名同步bug修復+自動上架+首頁大改版** | ✅v103本場完成 | 詳見下方v103完整戰果，5個commit：申請名單搬到來訪次數/排行榜中間+加刪除按鈕(`567a37f`)、修復申請名單姓名沒同步導師編輯結果的bug+改自動上架不需教練逐一確認(`dfddc73`)、申請已送出頁文案改「大樹教練」置中兩行(`8eceeb1`)、首頁改版(固定表頭+右側浮動導覽+手機漢堡選單+導師卡片依人氣排序，後台導師名單維持原順序不動)(`c57a3d1`) |
| 🟢 | **bigtree-tw：8/26高雄場（當古典音樂遇到AI科技）補上報名費100元** | ✅v103本場完成，已推正式站 | commit `e3a6ad6`，Netlify deploy `6a76c91e`，額度47→46 |
| 🟢 | **bni-chapters：BNI官方品牌色系套用+分會列表首頁表頭一致性修復** | ✅v102本場完成 | 官方色(#CF2030紅+#000000黑)套用9分會(commit `958eea2`)+首頁導覽列補齊(commit `1f2c1a5`)。教練裁示「之後一定要用官方指定色系」，10組帳號預設密碼Admin/88888仍未處理 |
| 🟡 | **三機hook同步待辦（教練要求優先）** | ⏳聯想已完成，待ACER動手 | Mac本場修好3支hook(截圖鎖工具名稱/改html自動跳Chrome/長對話守則重載)已推雲端。**2026-08-09聯想已完成**：截圖鎖`screenshot_lock.ps1`查證工具名稱本來就是正確的(全小寫+連字號)，不用改；新建`auto_chrome_after_html_edit.ps1`(PostToolUse，Edit/Write碰.html自動`start chrome`)+`periodic_xinfa_reload_hook.ps1`(UserPromptSubmit，20輪起每10輪重載21條守則全文，不依賴python3/jq因這台python3只是Windows Store樁exit code 49)，兩支皆用模擬輸入實測通過(含debounce驗證)才上，已註冊進`~/.claude/settings.json`(本機專屬不隨git同步)。**過程中額外抓到並修復兩個這台機器才有的環境坑**：①PowerShell 5.1在Big5 codepage下誤讀無BOM的UTF-8原始碼，導致腳本裡的中文檔名字面量解析錯誤、hook靜默無輸出零錯誤——periodic_xinfa_reload_hook.ps1已補UTF-8 BOM修復；②`[Console]::InputEncoding`預設Big5會把stdin JSON裡的中文文字(如中文檔名)讀壞，已強制設UTF8，這個坑理論上會影響任何讀中文stdin的Windows hook。commit `72776028`。ACER下次開工可直接抄這兩支.ps1+確認settings.json有無同款jq/python3環境限制，完整待辦見[[project_cross_machine_hook_sync_todo_2026-08-08]] |
| 🟢 | **☕ 幕僚長晨報：新增cron統整bni_tainan+jiaolian_thoughts每日動態** | ✅2026-08-09完成，觀察一週中 | 教練問「影片講的第六階段(AI團隊自動彙報)你實踐了多少」，查證發現對外服務的兩個AI員工(bni_tainan/jiaolian_thoughts)目前動態教練完全看不到。新建cron`b73845c9-f653-4f9a-8869-0e2f2c0bd9b1`，每天07:00讀這兩個agent的每日記憶檔，用「三關」過濾(真的有問題/非偶發/真的影響業務)挑出值得教練知道的事，沒事就說沒事不硬編內容。已手動觸發測試：16.4秒完成、真的送達Telegram、正確判斷「今天無notable互動」(查證當天兩個記憶檔確實只有系統dreaming背景資料無真實對話)。跟06:00起床摘要(教練自己機器工作記錄)、23:05三機總結(教練跟三機對話)是互補不重複的第三份晨間彙整。**待辦**：觀察一週，教練回饋內容準不準再決定要不要調整判斷標準 |
| 🟢 | **mentor100百人導師計劃：訪客計數器+人工審核上架流程** | ✅v101完成+2026-08-09教練確認流程無問題 | 首頁到訪次數計數器+導師點擊排行榜+「加入計劃」改人工申請(申請→教練產生填寫連結→自填草稿→教練預覽確認上架)，教練刻意要「人工申請」體驗設計。詳見v101完整戰果+[[project_mentor100_review_gated_signup_2026-08-08]]。**2026-08-09教練口頭確認**：已經有申請者自己寫完送出，流程都沒有問題，本項結案。同日另補上首頁正式頁尾(版權/訪客計數/官網連結/LINE聯絡)，commit `63f967a9` |
| 🟢 | **workshop-invite.netlify.app 移除台中場按鈕** | ✅v101本場完成 | 只留台南/台北場，其餘5個姊妹邀請頁教練裁示暫不動。deploy `6a75de3e8d2a6c2aadd104d4` |
| 🟢 | **Email自動發送系統** | ✅教練已自行執行完成(2026-08-09口頭確認) | 教練自己動手做完了，不需要AI介入，本項結案 |
| 🟢 | **event-signup抽獎轉盤(/wheel)：簽到名單自動帶入+獎品庫存追蹤** | ✅v85完成，7/29現場正式使用 | 詳見v85完整戰果。名單直接查簽到記錄不用手動輸入、獎品清單+抽中自動扣庫存+中獎彈窗+15句趣味台詞。7/29教練現場異地登入密碼重設(改成教練指定的新密碼)+實測登入成功，詳見v86 |
| 🟢 | **LINE綁定率低(56簽到僅12綁定)真正原因+修復** | ✅v86已完成 | `/checkin`簽到路徑的`/slides`頁面沒有像線上報名`/thanks`頁面一樣幫來賓預填「我是OOO，剛報名了XXX」問候語，來賓要自己手動輸入才會綁定，多數人卡在這步放棄。已修復`slides_landing()`補上同一套`greet_url`邏輯，測試通過並部署，未來場次現場簽到綁定率應明顯改善 |
| 🟢 | **AI微型論壇台南場轉型為活動回顧頁** | ✅v86已完成 | 仿照全球健康發展協會(northern-tw.netlify.app)做法，`ai-talk-tw.netlify.app`從報名頁轉成歷史紀錄：花絮換成教練提供的24張現場真實照片、拿掉倒數計時器/報名區塊、CTA全改「加入LINE」、新增下一場嘉義場預告。GitHub commit `78213ed`，Netlify部署`6a6a1a24` |
| 🟢 | **AI微型論壇嘉義場(ai-talk repo)網站** | ✅2026-08-05已推Netlify正式站，含二次修正(LINE預覽+正名+講師連結) | `ai-talk-tw.netlify.app`從台南場舊版換成嘉義場主場。**第一次推**（deploy `6a729de183c3119517084d98`，10:20發布）：內容轉型上線，額度55→54。**教練隨即實測貼LINE發現預覽仍顯示「台南場」**——查證發現此頁20個歷史版本全部0條og:標籤，LINE只能猜`<title>`且會快取住。**第二次推**（deploy `6a72a2e75b98ebc94b95d4be`，10:41發布，額度→52，中間bigtree-tw站另有一次部署插隊54→53）：補齊og:+twitter:共16條預覽標籤(image用教練親自從24張裡挑的photo-24.jpg滿座照)、活動全站正名「AI微型論壇」→「AI微論壇」12處(對齊bigtree-tw主站8/3已正名)、依教練指示比照mentor100幫四位講師簡介補上FB/IG/官網等外部連結(季哥2/洪詠清6/林韋銘4/大樹教練7，大樹教練mentor100裡的IG欄位其實是這網站自己、屬自我指涉未收錄已告知教練)。**⚠️LINE快取提醒**：教練分享網址時後面要加`?v=2`之類參數才會繞過LINE舊快取顯示新預覽。驗證：文字(標題/AI微論壇次數/og:三項)+圖片(og:image與4張講師照逐一curl確認HTTP 200且Content-Type: image/jpeg)+瀏覽器實測講師連結彈窗正確渲染+console零錯誤+台南封存區塊(純div無onclick)確認不受影響。ai-talk獨立repo commit `45090d8`已推GitHub。
| 🟢 | 「教練都在想什麼」LINE帳號完整搬遷到Mac+MiniMax-M3 | ✅本場已完成 | 詳見下方v81完整戰果。人設逐字搬遷+46萬字知識庫+FTS5全文檢索+webhook正式上線服務121位好友+dmPolicy修復+seabiscuit.bymyway.com監控後台+User ID對照hook泛化。教練待自行測試seabiscuit.bymyway.com登入(密碼Bymyway7，第一次會卡裝置配對，把畫面ID給軍師) |
| 🟡 | 「教練都在想什麼」案例庫深度待擴充 | ⏳待教練提供更多素材 | 目前只有教練提供的4份文件(大樹使命之旅/禮物諮詢法/海餅乾文化核心逐字稿/海餅乾語錄，共46萬字)，教練原話「提供更多資料庫讓AI做更大的品牌宣傳」——若教練還有其他素材(更多逐字稿/文章/Podcast)，補進`agents/jiaolian_thoughts/knowledge/`後跑一次`python3 scripts/build_search_index.py`重建索引即可 |
| 🟡 | 教練其他類似LINE帳號待比照搬遷 | ⏳待教練指定下一個帳號 | 教練原話「我還有其他類似的帳號也要這麼做」，已產出完整SOP：`knowledges/SOP_Coze_LINE帳號搬遷小龍蝦本機.md`，下次教練指定帳號直接照SOP 12步驟走，不用重新摸索 |
| 🟢 | **結繩領導學工作坊即時戰報系統（台南/台中/台北）** | ✅v82已全功能上線 | `https://rpl-workshop.bymyway.com/admin`，帳號**RPL**(大寫)，密碼公司統編(AI全程未接觸)。15筆歷史資料已匯入(教練後續已自行登入新增/修改過，證實系統正常運作)。功能：開課倒數/目標達成率進度條/邀請人與資料提交人下拉(曜董/大樹/佩君/Lavi)/姓名可編輯/依報名日期排序/**整頁一次「全部儲存」**。詳見[[project_jiesheng_report_launch_2026-07-26]] |
| 🟢 | **event-signup簽到系統：手機號碼比對簽到（免重填資料+保留集點）** | ✅本場已完成，教練實測確認 | 教練發現原本固定簽到QR(`/checkin`)會讓已線上報名過的來賓重填一次姓名/電話，多此一舉。改成`/checkin`只問手機號碼，比對到既有報名記錄→直接記進signups表(集滿5次送禮物功能保留)+導向`/slides`(加好友+下載簡報，帶個人化「OOO簽到成功」)；查無記錄(現場臨時來賓)→導去完整表單但手機號碼已預填。7/29 AI微型論壇立牌已印(QR網址沒變不用重印)，教練親自實測通過確認採用此版本。commit `fd480212a`(QR先改指向/slides，中途方案)→`022051eba`(立牌加場次標籤)→`0ef5ee98a`(最終手機比對版本)。同場也修好`event.bymyway.com/admin`場次資料(8/1改8/26+9/5+9/19，比對`bigtree-tw.netlify.app`)。 |
| 🟢 | **圖片OCR辨識通用小工具** | ✅本場已完成 | 抽出`tools/ocr-extract/ocr_extract.py`，PaddleOCR(沿用namecard-db既有venv)→MiniMax兩階段管線，SYSTEM_PROMPT改成`field_schema`+`task_description`參數化，不綁死名片格式。過程中實測抓到真bug：`.env`讀取用`setdefault`不會覆蓋外層shell既有的`ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`(終端機Claude Code自己的環境變數)，導致打到api.anthropic.com而非MiniMax端點回傳401，已改直接賦值強制覆蓋。用兩張真實名片+兩組完全不同命名的自訂欄位schema驗證通過。commit `1488b6c68`。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| 🟢 | **系統權限缺口：public agent(bni_tainan/jiaolian_thoughts)沒有工具層級限制** | ✅v83已完成 | 詳見下方v83戰果。改用OpenClaw原生`tools.toolsBySender`機制(查證版本原始碼確認真的存在且生效於主要工具判斷流程，非僅sandbox)，教練LINE ID白名單保留完整權限、其他發送者deny掉`group:runtime`+`group:fs`+`group:automation`。新增`line-user-memory`hook讓非教練用戶仍保有個人化記憶(不靠write工具，伺服器端維護)。commit `fb222757` |
| 🟡 | 教練第二身份「贏家思路」(LINE ID `U168903487f0ba2b666ddc62b854de351`)已加入白名單 | ✅v83已完成 | 教練親測時發現用這個帳號測試bni_tainan/jiaolian_thoughts會被當一般訪客擋權限，查證+教練確認後已加進toolsBySender白名單，兩個帳號都生效 |
| 🟢 | 「龍蝦小助教」(default LINE帳號，綁main agent)僅供教練個人使用，維持pairing制不開放 | ⚠️v92已推翻，見下方新項目 | v83原裁示不開放；2026-08-03教練親口要求「跟其他兩個帳號一樣開放，不需要再經過我同意」，已改為群組互動開放，詳見v92 |
| 🟡 | 小龍蝦後台(OpenClaw原生控制介面)不顯示用戶中文名稱 | 🔒卡住-教練決定用問答方式 | 查證確認這是OpenClaw原生Control UI的已知限制(GitHub上至少8個未解決的相同feature request)，非設定缺漏。已評估「另建自訂監控頁面」的時間/token成本，教練裁示「若有問,你再回我就好」——不建頁面，教練看到陌生ID直接問軍師，軍師查`state/{account}_line_id_map.json`即時回覆即可 |
| 🟢 | 開工六步驟+MEMORY.md額度瘦身 | ✅v83已完成 | 教練要求評估「開工」占用多少KB(對應1M上限)。實測發現workspace/CLAUDE.md已自動鏡像接力棒全文，六步驟hook卻又重複cat一次；另有claude-sessions/死code(18天未更新)。已修復：接力棒改「確認同步新鮮度才決定貼短版或全文」的安全網設計(不冒漏接風險)、砍死code、試金石3→2案例、memory最新日改尾端6000字。單次注入實測49,593→20,588 bytes(降58%)。MEMORY.md索引退休7條已解決舊專案記憶(31.5KB→30KB)。commit `e9144daf8`+`12e7b6b54` |
| 🟢 | bni_tainan行事曆同步cron實際上從未存在過，已修復 | ✅已完成 | 查證發現v75紀錄的cron job 99bdac4a 在 cron list 裡根本查無此ID，行事曆檔案卡在40+小時沒更新。新建 cron `7048432e`（每4小時，已修好delivery歧義設定），手動觸發驗證 exitCode 0 + 檔案內容確實更新 |
| 🟢 | BNI大台南小幫手LINE送達備援+網址防呆+會員ID對照 | ✅已完成 | 詳見v80完整戰果，三個hook都已重啟驗證+commit。會員ID對照hook本場(v81)已泛化為全LINE帳號通用，不影響原有功能 |
| 🟢 | BNI大台南小幫手「主動提醒」功能 | ✅v87已完成，教練實測LINE推播成功 | v77原設計要agent自己exec呼叫cron，但v83鎖了非教練發送者的exec/cron權限，此設計已失效。改用`hooks/bni-reminder-schedule/`伺服器端hook解析中文時間(相對/絕對，含中文數字)+提醒內容直接排一次性cron，不需要任何會員拿到工具權限，架構上對所有會員一視同仁(非教練專屬)。教練真實傳LINE訊息測試收到推播確認成功。commit `e3608229` |
| 🟡 | 「教練都在想什麼」LINE語音訊息無法辨識 | ⏳v87已修復待驗證 | 查production log證實2026-07-29有真實會員傳語音、transcribe失敗(reason=Command failed)。已改`tools.media.audio`明確指定完整路徑`/opt/homebrew/bin/whisper`+已快取的base模型(避開PATH解析與模型下載逾時兩個嫌疑根因)+120秒逾時。無法自己模擬真實LINE語音webhook，待教練或任一會員實際傳一句語音給「教練都在想什麼」驗證是否真的修好。commit `e3608229` |
| 🟡 | **真誠分會／真愛分會／真AI分會＋大台南南區網站**（⚠️2026-07-31名稱更正：原記錄「真實AI分會」錯誤，教練親口澄清正式名稱是「真AI分會」，該分會尚未在BNI Connect登記） | ⏳待教練回覆5項細節 | 連續v72起多棒未開始，2026-07-29(v87)教練終於給細節：兩個參考網址(bnidahan.com.tw／bni-tainan.com/Training-Program)+要求BNI標準色系。已產出**兩份完整HTML版型草稿**(色系實測抓自兩參考站真實CSS`#A22026`)：真誠分會(比照bnidahan結構：參訪須知/核心價值/分會之光)、大台南南區(比照bni-tainan結構：轄下分會/培訓計畫/最新消息)，三分會共用同一套版型套版。教練Comet預覽後確認「方向正確」，交棒給Mac接手，詳見v87。**卡住點**：等教練回覆5項細節——①參訪須知實際數字(名片張數/早餐費用/自介秒數，教練說「部分不同」但尚未給確切值) ②真愛/真AI分會各自slogan ③分會之光要不要放真實數據 ④大台南南區是否僅此三分會 ⑤各分會FB/Line連結。檔案：`knowledges/2026-07-29_bni-nantai-mockup/真誠分會_index.html`、`knowledges/2026-07-29_bni-nantai-mockup/大台南南區_index.html`(暫放knowledges，尚未建立實體GitHub repo，等內容定案後再轉正式repo)。部署位置教練已選定GitHub Pages測試稿(非Netlify正式站)。**2026-07-31查證BNI Connect CMS真實分會清單只有5個：真富/真愛/真誠/真鑫/真鑽(無真AI，因尚未登記)**，詳見下方新增項目 |
| 🟢 | **BNI Connect官方網站CMS後台操作能力驗證** | ✅2026-07-31本場完成，教練親口確認「非常棒」 | 教練登入BNI Connect後台(bniconnectglobal.com/bnicms/v3)，用`claude-in-chrome`連上教練本機真實已登入Chrome(不是Claude自己的隔離分頁，這個坑先踩過一次教練當場糾正)，確認有編輯權限：大台南南區(區域ID`12261`)+5個分會(真富25503/真愛26706/真誠18487舊&18640新/真鑫28446/真鑽12262)，可改地址/電話/聯絡人/分會頁面內容。全程DOM純文字讀取不截圖，Token消耗低。教練明確授權「以後我口頭講要改什麼，你直接去改」，發布上線前口頭提醒一聲即可，不用每欄都確認。**完整存取方法+網站ID索引已寫入記憶系統**`reference_bni_connect_cms_structure`+`project_bni_connect_backend_access_verified_2026-07-31`(commit `6acef6316`，透過`.claude/projects`記憶庫git同步三機)。**⚠️三機注意**：操作方法/網站ID三機共用，但**登入狀態是per機器**——聯想/宏碁要操作BNI網站前，教練需在那台機器的Chrome親自重新登入BNI Connect(帳密僅教練本人輸入)+確認該機器claude-in-chrome擴充功能已連線，登入後直接套用同一套方法即可，不用重新摸索。**待處理**：真誠分會有2筆重複CMS記錄(舊18487/新18640)，該CMS對分會層級無Delete/Unpublish功能，教練決定先不動，待確認正式處理管道(BNI客服或Outback Global代理商帳號) |
| 🟢 | **大台南南區「見證」頁中文化+教練親自見證** | ✅2026-07-31已正式Publish上線，教練親口下令「發佈」 | 原頁面兩則英文見證(Marim/Amanda)已翻譯成中文(瑪琳/安曼達)+清空會跳到bni.com國際網站的連結。新增第三則教練親自口述的見證(BNI信任感引薦新加坡馬來西亞商機+上市公司培訓演講)，用表格排版做出「圖右文左」跟前兩則交錯呼應。**過程三次返工**：①Base64內嵌照片被CMS存檔時整個過濾掉(安全機制) ②改用CMS圖片庫網址但只有200×300小尺寸還被我拉大顯示糊掉 ③教練親自透過「瀏覽伺服器」選圖流程確認可以拿到真正原始解析度(6336×9504)網址，但同時給了寬高兩個固定數字，被BNI全站CSS只限制寬不限制高，拉變形，教練當場抓到糾正，已改成只給寬度讓高度自動跟隨比例，數據驗證比例0.667完全吻合原始檔案。**照片解析度追加修復**：發布前教練又抓到第一版照片(6336×9504全身照)顯示比例失真變形——原因是同時給了固定width+height兩個HTML屬性，被BNI全站CSS只覆蓋width導致高度沒等比例縮放，改成只給width讓瀏覽器自動算高度即修復；後來教練覺得全身照臉太小，換成教練提供的另一張近距離半身照(1785442736710.jpg)，改用圖片庫縮圖網址(最長邊300px、比例正確不失真)。**已於2026-07-31 12:39(BNI系統時間)正式Publish**，用獨立無登入瀏覽器分頁實測`bnitainan.com.tw/zh-TW/testimonials`公開網址確認三則中文見證真實對外可見，非僅CMS預覽。**教訓**：img同時設width+height兩個HTML屬性，遇到外部CSS只覆蓋其中一個屬性時會失真變形，之後只設一個維度讓瀏覽器自動等比例換算更安全 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🟢 | **結繩領導學官網重構：從新書發表轉為兩日工作坊銷售頁** | ✅v99完成，已推正式站(GitHub自動部署) | 依教練提供指令書(`~/Downloads/結繩領導學_官網重構指令書.docx`)11區塊重寫首頁，舊版(新書發表+11場座談會)完整封存於`archive/`不遺失。過程含多輪UI微調(表頭四連結+CTA/右側浮動導覽/手機漢堡選單/成交區按鈕置中/品牌字級22px/Hero改雙欄+書封面)+og標籤補齊(舊版LINE預覽卡「現場座談會」需靠`?v=`繞過快取，跟AI微論壇同根因)。**教訓**：`jiesheng-leadership`是GitHub自動部署型，「推GitHub」對這站=同時推Netlify，本場因未查證這點導致教練還沒說「推」就已上線，詳見下方永久提醒 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🟡 | coach888拖拉排序功能 | ⏳待教練回饋 | v72已用真實滑鼠事件測試交付，尚無教練實際使用回饋記錄，下一場先問「好用了嗎」 |
| 🟡 | 「全世界最優秀的團隊計畫」報名連結 | 🔒卡住-等教練 | 兩顆按鈕還沒掛真實報名連結，等教練給LINE或表單網址 |
| 🟡 | 企業健身房正式建站（coach1973.github.io/Business.gym） | 🔒卡住-等教練 | 網址教練已親貼確認，但尚未正式交辦開工 |
| 🟡 | 企業健身房4項文案修改 | 🔒卡住-等教練 | 已記錄commit 10c7b11cf，等教練繼續交辦下一步 |
| 🟢 | `.env`含`$`字元值要單引號包住 | ✅本場真實踩到並修好 | jiesheng-report密碼雜湊值含`$`被bash source吃掉，已修復+寫入記憶[[project_jiesheng_report_launch_2026-07-26]]。Jinja模板guard None值這條仍待抽空檢查其他Flask小專案 |
| 🟡 | BNI小幫手教練親測多種問法 | ⏳待教練體驗 | 確認BNI小幫手實戰體驗OK |
| 🟡 | Coze舊機器人何時停用 | 🔒卡住-等教練 | 先保留當備援，等教練確認新系統穩定一陣子後裁示 |
| 🟡 | ACER 36.3GB備份待刪（觀察期已過） | 🔒卡住-需教練在ACER機器親自開對話執行 | 這台Mac無法代為執行 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟢 | 光線尺顧問ATM NT$10,000入金(07-13)對帳 | ✅已解決(2026-08-09口頭確認) | 教練確認對帳問題已解決，本項結案 |
| 🟢 | 「連接」按鈕自動化點擊無反應（真人操作無此問題） | ✅已排除疑慮 | 教練親自兩台電腦實測「連接」按鈕正常，先前疑慮的bug只影響自動化工具合成點擊事件，教練不會遇到，暫不需修 |
| 🟢 | plugins.allow白名單未設定 | ✅v94已完成 | 查原始碼發現**本表原本建議的7個外掛清單會把系統打壞**：`config-normalization-shared`的判斷是`if (allow.length > 0 && !allow.includes(id)) → not-in-allowlist`，等於plugins.allow是「全域嚴格白名單」不是只管非內建外掛，只列7個會把另外41個（含telegram/browser/duckduckgo/anthropic/canvas）全關掉——跟案例56的toolsBySender萬用deny誤傷cron同一種形狀。改法：白名單＝程式化取自`plugins list`的48個實際載入中外掛ID。重啟實測48 loaded/20 disabled與改動前完全一致、警告消失、三個LINE+三個Telegram全部正常。commit `8b7e7dde`，備份`/tmp/openclaw.json.bak-202608050950` |
| 🟢 | ~/.claude/CLAUDE.md與執行細則.md的E10~E12分岔 | ✅已完成 | 教練裁示「合併，因為這樣才簡單」。執行細則.md保留權威版，Karpathy三原則改編號E13~E15追加。新增`scripts/sync_zhixingxize_to_claude_global.sh`+openclaw cron(job 37593697,每30分鐘)自動鏡像，結構性根治，不會再分岔。commit `0a4271d80` |
| 🟢 | 小龍蝦紀律移植計劃 階段二 | ✅v94已完成，觀察一週中 | 三條規則（E09 cron驗證／E12 記憶寫入雙鐵律／E08 引用查證）已進`hooks/rule-reminder/handler.js`，全部帶`scope:['main']`只對教練自己的小龍蝦生效。RULES新增可選`scope`欄位，沒帶scope的原有12條行為完全不變；agentId解析沿用bot-relay-inbound v2.5三層fallback。**案例56教訓有帶進來**：LINE default帳號（龍蝦小助教）sessionKey是`agent:main:line:...`，解析出來就是"main"，所以scope:['main']同時涵蓋教練Telegram+龍蝦小助教，不誤傷服務真實會員的bni_tainan/jiaolian_thoughts。驗證：新增`test_scope.js`跑12項全過（正向/反向/回歸/誤觸發防呆）+重啟gateway實測13個hook載入、六個通道全正常、零error。commit `fe86890a`。**2026-08-05教練當場裁示追加**：E08引用查證不等觀察期，直接開放給`bni_tainan`+`jiaolian_thoughts`（新增「E08官方文本版」，觸發詞鎖定官方條文情境：出席/缺席/請假/政策/道德規範/會議流程/合約/職責/使命/總政策/會員資格/淘汰/引薦單/一對一/訪客/遲到等，刻意不收「可以嗎/算不算」這類太泛的詞）。教練點破這不是新規矩——`agents/bni_tainan/AGENTS.md`第5行/模式B Official Text Mode/總政策19條本來就寫死「一字不差、不可簡化改寫、不得節錄」，系統本來就該逼它查了再答。E09/E12維持`scope:['main']`不開放：查證確認小幫手的會員身分被擋掉exec/fs/cron三組工具，這兩條在那邊沒有對象。test_scope.js擴充到18項全過，commit `d04241a4` |
| 🟡 | 小龍蝦紀律移植計劃 階段三 | ⏳待軍師動手 | 階段一(真相源驗證+E07語音糾偏規則)本場已實作進`hooks/rule-reminder/handler.js`並測試+commit`4f08cd27`+重啟gateway驗證健康。階段二(cron驗證/記憶寫入雙鐵律/引用查證，先只對main agent生效觀察一週)、階段三(危險指令防禦)待排時機，詳見`knowledges/2026-07-24_小龍蝦紀律移植計劃_mattpocock skills精神落地.md` |
| 🟢 | **Mac版Web Search修復（Telegram三帳號+LINE三帳號共用）** | ✅v90已完成 | 教練發現Mac版打不開Web Search只能退而求其次DuckDuckGo，查證原生`web_search`綁死MiniMax專屬鑰匙（未申請）。改用系統內建`duckduckgo`外掛（官方標明無需API Key）：`openclaw plugins enable duckduckgo`+`config set tools.web.search.provider duckduckgo`+重啟gateway，production log證實真實搜尋成功。commit `c9cc8072`。VPS版查證後發現本來就正常（容器內`MINIMAX_API_KEY`恰好也能當搜尋備援），誤改後已撤銷復原，VPS無需任何動作。詳見v90完整戰果+[[試金石案例55]] |
| 🟡 | 軍師自我要求：查證前先查「路徑大全」+盤點類任務要窮舉底層資料結構 | ⚠️永久提醒 | 教練v90當場糾正兩次查證不完整（VPS沒先查路徑大全就回報查不到、LINE帳號盤點漏算沒有名稱標籤的「龍蝦小助教」），教練明確期許「你是所有資訊的大總管，要自己想辦法完善」。已寫入試金石案例55，核心自我檢查：①任何「查不到/做不到」結論前先確認查過該環境萬用索引檔 ②盤點類任務直接數清楚底層資料結構(JSON物件key數)逐一核對，不能只挑印象中顯眼的幾筆 |
| 🟢 | ai-go新增「教練專屬人設」區塊，僅推了GitHub Pages入口，bymyway.com鏡像未同步 | ✅v94已完成（實際問題比記錄的更嚴重） | **真相不是「內容不同步」而是「整頁空白」**：`www.bymyway.com/ai-go/`的內容在2026-06-25(WP revision 27392)被清空，在那之前revision 27391是正常的948字元iframe版本，等於這個對外入口白頁約6週，訪客點進去只看到標題。已修復並新增`sync_ai_go_to_bymyway.py`（就地更新頁面27390；既有的`deploy_*.py`是新建draft，再跑會產生重複頁面）。內容是iframe指向`coach1973.github.io/ai-go/`，所以GitHub端的教練人設區塊自動反映，**往後改心法不用再跑這支腳本**。驗證：curl抓到iframe+OG meta 10條、瀏覽器實測iframe 1280×720正常渲染、內嵌頁「🌳 教練專屬・不是公版方法論」區塊存在、console零錯誤。commit `92eaaaa0e` |
| 🟢 | **龍蝦小助教LINE群組長期失效真根因找到並修復** | ✅v92已完成 | 教練回報龍蝦小助教Telegram/LINE都沒回應，且群組互動早已失效。查證發現`@openclaw/line`外掛對accountId==="default"完全不讀`channels.line.accounts.default`底下設定，`groupPolicy`/`groupAllowFrom`從設定搬進accounts.default那刻起就架構性失效。已修復：改在`channels.line`頂層設定，`accounts.default`只留`webhookPath`。commit `ec48b7bd`，用合成簽章webhook實測驗證。詳見試金石案例56 |
| 🟢 | **main agent健檢cron的exec/read/cron工具被昨天權限鎖誤傷，已修復** | ✅v92已完成 | 根因：cron觸發的agent turn沒有senderId，永遠落到`toolsBySender`的`"*"`deny規則。改用群組層級鎖(Telegram schema支援)取代agent層級萬用鎖，cron不再被誤傷。commit `56c0efe3`。**已知殘留風險**：LINE外掛(2026.6.33)不支援群組層級`toolsBySender`，LINE群組的非教練成員保護降級為`workspace/SOUL.md`鐵律五提示層防護(非技術硬鎖)，教練已知會，待外掛未來版本補上 |
| 🟢 | **主動提醒功能推廣到三個LINE帳號** | ✅v92已完成 | 教練指示「立刻推廣」。原本`hooks/bni-reminder-schedule`寫死只認bni_tainan，已推廣到jiaolian_thoughts+default(龍蝦小助教)，過程中修好一個accountId解析bug(default帳號session key含"main"非"default"，已正規化)。commit `41ffac6b`，三帳號皆用合成webhook實測通過 |
| 🟢 | ~~教練15:18有一段修改回饋被中斷、內容未送達~~ | ✅v92記錄有誤，已在Mac桌面版另一場對話完整收到並執行 | v92記錄的是「終端機」session看不到內容，但同一時段「桌面版」session其實完整收到了教練15:18那段完整訊息（適合誰參加文案改法/洪詠清林韋銘換照片/品牌曝光加現場輪盤抽獎三點），並已於v93完整執行，commit `4742cff`。**教訓**：多個Mac session（終端機/桌面版）同時開著時，教練同一句話可能只進到其中一個視窗，另一個看不到不代表訊息真的遺失，下次遇到類似狀況先問教練「是在哪個視窗說的」，不要直接判定「未送達」 |
| 🟢 | **BNI大台南南區9分會系統(bni-chapters)對外開通+密集功能迭代** | ✅v94本場完成 | 8/3深夜查證發現這套系統(教練另一對話框8/1建置)從未對外開通，已申請`chapters.bymyway.com`(過程cert.pem過期，改用claude-in-chrome完成OAuth授權)+加進coach888第13/14項。8/3~8/4密集迭代：9大官方核心價值(中英對照+2條隱藏版+懸浮hover效果，後台改唯讀不可增刪)、常用連結彈窗(漢堡圖示，含紅綠燈看板/LINE小幫手/培訓行事曆+6項教練提供的BNI教育資源)、六項傳統與道德規範(定案為分會之光下方永久區塊+`show_traditions`開關)、響應式設計(手機版隱藏文字導覽只留漢堡選單)、參訪須知依線上/實體分流(**線上**=真誠/真AI籌備會/真愛/真貴籌備會，**實體**=真富/真鑫/真鑽/真功夫籌備會/真樂齡籌備會，此分類與`status`(正式營運/籌備中)欄位無關，教練糾正2次才拿到正確名單)。**教訓**：測試表單POST漏填欄位曾誤清空真誠分會Hero文字(已從seed.py救回)+不能用不相關欄位推論新分類，兩條都寫入記憶，詳見[[project_bni_chapters_public_launch_2026-08-03]]。**待處理**：10組帳號仍是預設密碼Admin/88888，教練尚未裁示是否/何時要求改密碼 |
| 🟢 | **www.bymyway.com/ai-go/ 空白頁修復（新增就地同步腳本）** | ✅v95本場完成 | 查WordPress修訂紀錄發現這個對外入口在2026-06-25被清空(revision 27392 len=0)，整頁空白約6週。新增`sync_ai_go_to_bymyway.py`就地更新頁面27390(既有的`deploy_*.py`是新建draft，再跑會產生重複頁面)。驗證：curl抓到iframe+OG meta 10條、瀏覽器實測iframe正常渲染、內嵌教練專屬人設區塊確實存在。commit `92eaaaa0e` |
| 🟢 | **OpenClaw plugins.allow白名單補上（修正接力棒原建議會打壞系統）** | ✅v95本場完成 | 查原始碼發現`plugins.allow`是全域嚴格白名單，接力棒原建議只列7個外掛會把另外41個(含telegram/browser/duckduckgo)全部關掉——跟案例56的toolsBySender誤傷cron同一種形狀的坑。改用程式化取自`plugins list`的48個實際載入外掛ID，重啟實測48 loaded/20 disabled與改動前一致、警告消失。commit `8b7e7dde`。已寫入記憶`reference_openclaw_plugins_allow_strict_whitelist` |
| 🟢 | **小龍蝦紀律移植計劃階段二上線+E08官方文本版追加開放給BNI小幫手** | ✅v95本場完成 | 階段二三條規則(E09 cron驗證/E12記憶寫入/E08引用查證)進`hooks/rule-reminder/handler.js`，全部`scope:['main']`，18項test_scope.js全過。commit `fe86890a`。**教練當場追加裁示**：BNI官方條文(出席/道德規範/會議流程等)本來就寫死要求一字不差回答，不用等觀察期，直接新增「E08官方文本版」開放給`bni_tainan`+`jiaolian_thoughts`(E09/E12因小幫手無exec/fs/cron權限維持只給main)。commit `d04241a4` |
| 🟢 | **AI微論壇嘉義場推上Netlify正式站+LINE預覽快取修復+講師連結補齊** | ✅v95本場完成，教練親口說「推」x2 | 第一次推(deploy`6a729de183c3119517084d98`)：嘉義場取代台南場舊版上線。教練實測貼LINE發現預覽仍顯示台南場——查證這頁20個歷史版本從未有`og:`標籤，LINE只能猜`<title>`且會快取住。第二次推(deploy`6a72a2e75b98ebc94b95d4be`)：補齊16條og:/twitter:標籤(圖片教練親自從24張裡挑)、活動全站正名「AI微型論壇」→「AI微論壇」(對齊bigtree-tw主站)、依教練指示比照mentor100幫四位講師簡介補外部連結(從mentor100.db撈取)。查證LINE官方除錯工具Page Poker已停用(DNS查無)，確認`?v=2`網址參數是唯一可行的快取繞過法，教練往後行銷網址統一貼`ai-talk-tw.netlify.app/?v=2`。ai-talk獨立repo commit `45090d8`。額度扣至剩52次 |
| 🟢 | **大樹小講(bigtree-tw)新增金門兩場次+歷史講座紀錄頁改宮格牆** | ✅v96本場完成，已推Netlify | 教練口述新增8/21(五)19:30-21:00金門場(西浦頭社區)+8/22(六)13:30-16:30金門場(向陽吉第社區，教練口誤「吉弟」經WebSearch官方資料查證更正)，主題皆「零基礎學AI，起步比較快」(順手統一全站舊寫法)。歷史講座紀錄頁應教練要求從縱向16張大圖列表改版為4×4宮格牆+點擊彈窗看完整資訊，本機預覽經教練確認後推上正式站(deploy`6a72a1b619a971632cad6833`)，curl驗證文字/圖片Content-Type皆正常。GitHub commit `620ca09`(場次)+`d567976`(宮格牆)+`4262ea8`(場地補正) |
| 🟢 | **健康檢查cron假警報根因修復(v4.0三關判定)** | ✅v96本場完成 | 教練回報「小龍蝦老是出現奇怪訊息」，查證發現`🦞每30分鐘任務健康檢查`(jobId`46e67e2e`)因minimax provider暫時過載連錯5場觸發舊規則「連續≥3必announce」，但警報送達當下該輪其實已恢復成功，等於送出假警報。教練當場糾正「不影響工作就別吵我，浪費我注意力」。已用`openclaw cron edit --message`把規則#4改版為v4.0：只有「現在仍壞+非provider暫時過載+真影響工作」三關全過才准announce，並用`openclaw cron run --wait`實跑驗證同款情境下確實不再誤發(`delivered:false`)。已寫入記憶`feedback_alert_only_when_actually_broken` |
| 🟢 | **opencode 兩次當機根因修復（snapshot關閉＋model改minimax自家）** | ✅v97本場完成 | 教練反映「opencode 已經兩次當掉」，查log抓到兩個AbortError session（11:57+12:05），三層根因：①snapshot 機制對 `~/.openclaw/` 做 `git add .` 撞到 `_archive_2026-05-20/agents_bak/{kong,peipei}.bak/` 兩個 empty git repo（53次warning）②多個session並行時撞git index.lock → Bun runtime `AbortController.abort()` → TUI崩③opencode預設model跑成 `opencode-go/minimax-m3`（小寫）而非教練設定的 `minimax/MiniMax-M3`（大寫MM）。修法：`~/.config/opencode/opencode.json` 加 `snapshot:false` + `model: minimax/MiniMax-M3` + `small_model: minimax/MiniMax-M2.5-highspeed` + `opencode upgrade` 1.15.13→1.18.13。**教練當場糾正**：第一版報告建議「去opencode.ai workspace充值」是錯的——教練用的是minimax自家API Key，跟opencode.ai workspace額度完全無關，已minimax自家API curl驗證HTTP 200有效。教訓寫入試金石案例57，knowledges 紀錄完整紀錄在 `knowledges/2026-08-05_opencode兩次當機根因修復_snapshot關閉＋model改minimax自家.md`。commit `48c99e9e` + `d78d48f8` |
| 🟢 | **大樹小講8/21金門場座位80→60人+worklucky-2026串接小龍蝦通知+結繩領導學取消台中場** | ✅v100本場完成 | 三個獨立站台維護任務，皆已推送並curl/服務重啟驗證，詳見v100完整戰果 |
| 🔴🔴🔴 | **小龍蝦訊息遺失真根因修復：inbound-message-echo-log機制** | ✅v100本場完成 | 教練回報「小龍蝦說我67小時沒說話但我明明有講」，查gateway原始日誌挖出2026-08-03 15:58:42真有訊息被收到卻因API限流疑似卡死、內容從沒存底的鐵證。新建`hooks/inbound-message-echo-log`+修好`sync_coach_last_message.sh`(v3.4)，訊息一進來當下就落地不等agent turn跑完。教練接著要求「跟軍師互動也算有理小龍蝦」(選最寬範圍)，新建`scripts/log_junshi_activity_to_echo.sh`自動記錄每則對話，詳見v100完整戰果+記憶`reference_inbound_message_echo_log_system`+`feedback_junshi_activity_counts_as_xiaolongxia_contact` |
| 🟢 | **台南行事曆(tainan-calender)：新領導團隊培訓改期至9/21+全站排序bug修復** | ✅v107完成，已推正式站 | 8/10改9/21(一)，地點改ZOOM線上，順手修好`parseDateScore()`無法解析無斜線MMDD格式(如0905-0906)導致的全站排序錯亂bug，9~12月全面驗證。commit`7ad2427` |
| 🟢 | **新網站「從從容容用AI聊健康」ai-fit上線** | ✅v107完成 | 8/25台南場宣傳頁，GitHub Pages：https://coach1973.github.io/ai-fit/ ，repo`Coach1973/ai-fit` |
| 🟢 | **大樹小講：報名深連結補&slot參數+8/25匯款提示+報名資訊即時轉發佩佩老師** | ✅v107完成，已推正式站+真實驗證 | ①`openRegisterFromQuery()`補`&slot=晚半`區分同一天多場次 ②報名成功畫面僅8/25顯示「請加入官方LINE取得匯款帳號」③新建`xiaolongxia-notify`(獨立Netlify function，用小龍蝦`@268dptjc`channel token推播)，已真實測試佩佩老師收到訊息，接進`submitRegistration()`並行呼叫。commit`5cd56d9`，deploy`6a7df0eb` |
| 🟢 | **教練新開通LINE帳號(pairing code 4GLBTVK3)無法與小龍蝦對話** | ✅2026-08-14教練確認「測試正常」，本項結案 | pairing已核准+白名單已確認寫入+cloudflared tunnel發現真斷線13小時已重啟修復+gateway process已重啟重新載入allowFrom，中間曾懷疑MiniMax模型服務間歇性過載，教練今日回報「測試正常」，證實v107兩個真根因(tunnel斷線+gateway未reload白名單)修復到位，非模型服務問題 |
| 🟢 | **「有人報名LINE收到通知」根因水落石出：其實走的是Telegram不是LINE** | ✅v107完成 | 教練請小龍蝦(Telegram/LINE介面)查證，回報是`event-signup/app.py`的`_notify_xiaolongxia()`函式做的——我親自核對程式碼確認**完全屬實**：該函式打Telegram Bot API送到教練chat_id`6124913915`，觸發點是`/slides`路由「有人掃簡報QR碼/現場簽到」，文字是「📊 有人簽到/掃了簡報QR碼」。但小龍蝦報告裡提到的「📋 新報名通知」文字經全機搜尋，只存在於今天(8/14)才新建的`xiaolongxia-notify`，不可能是7/28的紀錄，已誠實告知教練這個時間軸細節對不上。**教練最終拍板定論**：找不到記錄永遠是AI的問題不是教練的錯，AI是教練唯一的工具，任何存在的系統邏輯上就是AI做的，不需要每次重新論證，已寫入記憶`feedback_desktop_session_storage_and_blackbox_wording`第3節 |

---

> 📦 v114完整內容已封存：`handoff_archive/handoff_v114_archived_2026-08-18.md`（Mac桌面版，Chrome搶線根因+ezPay 238筆+coach888連結）

---

> 📦 v115完整內容已封存：`handoff_archive/handoff_v115_archived_2026-08-18.md`（聯想Windows，BNI-Training雙軌系統從零建置+753筆官方報表整合）

---

> 📦 v116完整內容已封存：`handoff_archive/handoff_v116_archived_2026-08-18.md`（聯想Windows，BNI培訓紀錄精準度修正+MSP投票新網站+SOP違規教訓）

---

> 📦 v117完整內容已封存：`handoff_archive/handoff_v117_archived_2026-08-18.md`（聯想Windows，4-8月簽到表開票總清冊交叉比對修正MSP名單）

---

> 📦 v118完整內容已封存：`handoff_archive/handoff_v118_archived_2026-08-18.md`（Mac桌面版，五項任務逐一執行+ezPay 108統編備註查詢完成+find -maxdepth查證失誤自我更正）

---

> 📦 v119完整內容已封存：`handoff_archive/handoff_v119_archived_2026-08-19.md`（Mac桌面版，BNI Connect活動出席勾選任務首次上線，8場活動101人次標記完成）

---

> 📦 v120完整內容已封存：`handoff_archive/handoff_v120_archived_2026-08-19.md`（Mac桌面版，讀跨機信箱接手ezPay培訓費發票，16張全部開立完成，MerchantID假成功陷阱首次發現）

---

> 📦 v121完整內容已封存：`handoff_archive/handoff_v121_archived_2026-08-23.md`（Mac桌面版，教練推翻「34人收齊才開票」規則，24張ezPay培訓費發票先開立）

---

> 📦 v122完整內容已封存：`handoff_archive/handoff_v122_archived_2026-08-24.md`（Mac桌面版，教練糾正「查無Email」誤判＋BNI 94人資料庫永久指引）

---

> 📦 v123完整內容已封存：`handoff_archive/handoff_v123_archived_2026-08-24.md`（Mac桌面版，大樹小講事件密集場：救回雙寫程式碼+場次管理後台+修好2次部署bug）

---

> 📦 v124完整內容已封存：`handoff_archive/handoff_v124_archived_2026-08-24.md`（Mac桌面版，AI助理資料包+8/28攤位頁+報名通知失聯真根因，搬運工失誤試金石案例62）

---

---

> 📦 **v112及更早的完整接力棒內容已封存**：`handoff_archive/handoff_v116_archived_2026-08-18.md`（v116）+ `handoff_archive/handoff_v115_archived_2026-08-18.md`（v115）+ `handoff_archive/handoff_v114_archived_2026-08-18.md`（v114）+ `handoff_archive/handoff_v113_archived_2026-08-17.md`（v113）+ `handoff_archive/handoff_v112_archived_2026-08-17.md`（v112）+ `handoff_archive/handoff_v111_archived_2026-08-16.md`（v111）+ `handoff_archive/handoff_v110_archived_2026-08-16.md`（v110）+ `handoff_archive/handoff_v109_archived_2026-08-16.md`（v109）+ `handoff_archive/handoff_v108_archived_2026-08-15.md`（v108）+ `handoff_archive/handoff_v106_to_v107_archived_2026-08-14.md`（v106+v107）+ `handoff_archive/handoff_v105-lenovo_archived_2026-08-14.md`（聯想Windows 2026-08-10）+ `handoff_archive/handoff_v104_to_v105_archived_2026-08-12.md`（v104+v105 Mac桌面版） + `handoff_archive/handoff_v104-lenovo_archived_2026-08-10.md`（v104聯想Windows） + `handoff_archive/handoff_v101_to_v103_archived_2026-08-09.md`（v101~v103）+ `handoff_archive/handoff_v100_archived_2026-08-08.md`（v100）+ `handoff_archive/handoff_v99_archived_2026-08-08.md`（v99）+ `handoff_archive/handoff_v97_to_v98_archived_2026-08-07.md`（v97~v98）+ `handoff_archive/handoff_v93_to_v96_archived_2026-08-05.md`（v93~v96）+ `handoff_archive/handoff_v92_archived_2026-08-05.md`（v92）+ `handoff_archive/handoff_v91_archived_2026-08-05.md`（v91）+ `handoff_archive/handoff_v90_archived_2026-08-04.md`（v90）+ `handoff_archive/handoff_v89_archived_2026-08-03.md`（v89）+ `handoff_archive/handoff_v88_archived_2026-08-03.md`（v88）+ `handoff_archive/handoff_v87_archived_2026-08-02.md`（v87）+ `handoff_archive/handoff_v85_to_v86_archived_2026-08-02.md`（v85+v86）+ `handoff_archive/handoff_v84_archived_2026-07-31.md`（v84單獨一份）+ `handoff_archive/handoff_v83_archived_2026-07-30.md`（v83單獨一份）+ `handoff_archive/handoff_v82_archived_2026-07-28.md`（v82單獨一份）+ `handoff_archive/handoff_v72_to_v81_archived_2026-07-26.md`（v72~v81）
> 瘦身原因：教練2026-07-26指出接力棒檔案太大，每次「開工」自動注入會吃掉新對話框大量額度，
> 只保留最新2棒在主檔，舊棒需要查歷史時才去讀封存檔，不再每次自動注入。

---


> 📦 v125+v126完整內容已封存：`handoff_archive/handoff_v125_to_v126_archived_2026-08-25.md`（Mac桌面版，凌晨全系統稽核+教練覆核追加任務）

---


> 📦 v127+v128+v129完整內容已封存：`handoff_archive/handoff_v127_v128_v129_archived_2026-08-25.md`（Mac桌面版，ezPay發票+台中場上線+賈維斯全系統體檢兩場+頻率覆核）

---

> 📦 v130完整內容已封存：`handoff_archive/handoff_v130_archived_2026-08-25.md`（Mac桌面版，賈維斯體檢延續：頻率覆核+解決通知從沒送達的根因，留下Q1待辦）

---

> 📦 v131完整內容已封存：`handoff_archive/handoff_v131_archived_2026-08-26.md`（Mac桌面版，AI微論壇台中場RWD真根因修復+Netlify額度重新校正）

---


> 📦 v132+v133完整內容已封存：（Mac桌面版，Q1總結功能+context-overflow-guard改版+名片系統CRM擴建）

---

> 📦 v134完整內容已封存：`handoff_archive/handoff_v134_archived_2026-08-26.md`（聯想Windows，Windows當機根因+ezPay記憶更正+跨機Stop hook查證+總結hook缺jq修復）

---

> 📦 v135完整內容已封存：`handoff_archive/handoff_v135_archived_2026-08-27.md`（Mac桌面版，BNI Connect 430人匯入+MiniMax額度事故案例65+路徑大全憑證稽核）

---


> 📦 v136完整內容已封存：`handoff_archive/handoff_v136_archived_2026-08-26.md`（Mac桌面版，BNI Connect前會員電話/Email補齊+來賓資料庫3712筆完整收集）

> 📦 v137~v139完整內容已封存：`handoff_archive/handoff_v137_to_v139_archived_2026-08-27.md`（v137 Mac桌面版媒合手動觸發定案／v138聯想Windows跨機同步四層根因／v139 Mac桌面版RustDesk修復+MiniMax紅線+bigtree密集迭代）

> 📦 v140完整內容已封存：`handoff_archive/handoff_v140_archived_2026-08-27.md`（聯想Windows，FB粉專發文API從零建置，卡在商家驗證+教練當場檢討試錯效率）

---

> 📦 v141完整內容已封存：`handoff_archive/handoff_v141_archived_2026-08-27.md`（Mac終端機，bigtree 8/28 EDM上線+報名頁LINE誘因文案定案+/slides多簡報支援+ezPay發票查證）

---

> 📦 v142完整內容已封存：`handoff_archive/handoff_v142_archived_2026-08-27.md`（Mac終端機，修復Stop hook守則#07輪詢偵測瞎眼35天的根因，commit`01a28f2fb`）

---

> 📦 v143完整內容已封存：`handoff_archive/handoff_v143_archived_2026-08-28.md`（Mac終端機，BNI信用証清查4分會171人完成，真鑽231人查了10人中途總結）

---

> 📦 v144+v145完整內容已封存：`handoff_archive/handoff_v144_to_v145_archived_2026-08-28.md`（Mac終端機v144離會會員信用証清查全數完結／聯想Windows v145 AI微論壇+ai-art獨立站建置）

---

> 📦 v146完整內容已封存：`handoff_archive/handoff_v146_archived_2026-08-30.md`（Mac終端機，BNI信用証清查後續建網頁+複查+權限隔離+誤觸事故）

---

> 📦 v147完整內容已封存：`handoff_archive/handoff_v147_archived_2026-08-30.md`（Mac終端機，/bni-credit三項待改+34筆信用証補開+搜尋空格bug修復）

---

> 📦 v148完整內容已封存：`handoff_archive/handoff_v148_archived_2026-08-30.md`（Mac終端機，乾淨世界頻道QR上線+peipei-event斷線5天修復+電腦變慢診斷）

---

> 📦 v149+v151完整內容已封存：`handoff_archive/handoff_v149_v151_archived_2026-08-30.md`（Mac終端機，真誠分會邀約來賓系統從零建置+bni-chapters重複實作/fork根因鑑識，v149與v151是同一起fork事件的兩條分支，內容已在v150結案）

---

> 📦 v150完整內容已封存：`handoff_archive/handoff_v150_archived_2026-08-31.md`（Mac終端機，真誠分會邀約來賓重複建置根因查明+移除+5位會員專屬編輯網址交付）

---

# 軍師接力棒 · 2026-08-30 v152（Mac終端機 Sonnet 5，逐步脫離Netlify：4個新路由+3處連動+作品總覽更新）

> 建立時間：2026-08-30 14:26 ~ 18:56（台灣時間，接續v150同一天新對話框，因context overflow於14:26自動重啟）
> 上一棒：v150（Mac終端機，同日較早，真誠分會邀約來賓重複建置根因查明+移除+5位會員專屬編輯網址交付）
> 本棒主軸：**教練拍板方向——大樹小講/AI微論壇/紅綠燈看板/培訓行事曆改成event.bymyway.com即時渲染，逐步脫離Netlify部署次數限制，並同步更新所有引用這些連結的地方。**

## 🎯 本場戰果

### 1. 大樹小講9/22台南場「下午」時段修改（session時間+移除點心飲料文案）
教練口頭指示：9/22台南場下午時段改13:30-16:30、拿掉「附點心飲料」文案。借用bigtree既有但未使用的`下午`slot(13:30-16:30，跟`午半`14:00-16:30區隔，不影響同用`午半`的9/5 KR養生廚房場次)，同步更新`event.db`。commit`f8ac8fc`（bigtree repo）。

### 2. 大樹小講/AI微論壇/培訓行事曆/紅綠燈看板改event.bymyway.com即時渲染上線
教練確認方向：先兩邊(Netlify+bymyway)同步，穩定後才退場Netlify。技術核心：`event-signup`既有Flask app新增路由，請求當下直接讀取各自github repo原始檔案渲染，大樹小講額外疊上`event.db`即時場次資料(沿用`bigtree_publish.py`既有`read_sessions`/`render_session_dates`函式)，完全不需要「發佈」動作。網址命名邏輯（教練拍板）：**網址代表活動格式/系列，不代表地點**——跟`ai-talk-tw.netlify.app`過去台南→嘉義直接覆寫同網址同一套邏輯。上線4條路由：
- `/bigtree/`（大樹小講，DB即時渲染）
- `/ai-forum/`（兩天制系列，現為台中場9/23-24，之後10/7-8台南場沿用同網址；教練原本要求`/ai-forum-taichung`後又親自糾正改成無地名的`/ai-forum`）
- `/ai-talk/`（半天制系列，現仍8/28嘉義場內容，等教練補齊凌榆舜/李明燦兩位講師資料後改9/22台南場，設攤/贊助商區塊維持不動）
- `/tainan-calender/`（純靜態，沿用既有拼法不改calendar）
- `/bni-traffic/`（紅綠燈看板，純client端Excel解析工具，零風險）

全部路由均：本機另開測試埠驗證→真實Chrome開過→重啟正式服務`com.coach.event-webapp`→在`event.bymyway.com`公開網址再驗證一次→確認其餘既有路由(`/admin`等)無回歸，才commit。commit`f8ac8fc`+`3df06cab7`+`fc58dc783`+`7d4b1e5e9`（event-signup，皆workspace repo）。

### 3. 三處連動同步更新
①`bni-chapters`資料庫`chapter_links`表：9分會×2種連結(紅綠燈看板/培訓行事曆)共18筆改新網址，重啟服務後在`chapters.bymyway.com/real-ai`公開頁curl驗證連結已更新。②`bni_tainan`小幫手：`AGENTS.md`4處member-facing連結+`knowledge/tainan_calendar.md`來源引用+`scripts/sync_calendar.py`實際抓取來源全部改新網址，**過程中發現`event.bymyway.com`前面的Cloudflare會擋掉urllib預設User-Agent(403)**，已補上`Mozilla/5.0`headers修復，重跑驗證106筆活動正常同步。commit`5fabb60d`（外層`.openclaw`repo，agents/bni_tainan路徑）。③`coach888`作品總覽：新增「bymyway自架版」區塊列出5個新路由(綠色badge)，對應5個Netlify舊版項目標「待退場」(橘色badge)，一眼可辨識新舊。教練追加要求把此區塊從第七移到第三順位，其餘區塊依序順延，已完成並在GitHub Pages正式站curl驗證順序正確。commit`230d735`+`cafe1f4`（coach888 repo，GitHub Pages自動部署免確認）。

## ⚠️ 本場教訓/發現（已寫入記憶）

1. **`event.bymyway.com`前面的Cloudflare會擋掉沒有瀏覽器樣式User-Agent的請求(403)**——`sync_calendar.py`改抓自家bymyway網址時直接403，curl實測`-A "Python-urllib/3.11"`→403、`-A "Mozilla/5.0"`→200證實是UA被擋非內容問題。任何腳本要fetch`*.bymyway.com`子網域都要注意這點，已寫入記憶`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。
2. **這套「讀活repo+DB即時渲染」模式的核心價值不只是「另一種不受限的部署方式」，是讓這類小改動(改時間/改文案)根本不需要「部署」這個動作**——editing DB或repo原始碼立刻反映，這點在跟教練說明時比單純講「省Netlify額度」更能讓他理解價值所在。
3. **新增自架服務時優先掛在既有已有launchd看護的Flask app底下(本場全部掛`event-signup`)，不新增獨立子網域/Tunnel/launchd**——降低「服務被遺忘」風險（呼應`peipei-event`斷線5天、ACER 49天未開機兩個舊案例的同一種病根：服務越分散越容易有一個沒人顧到）。

## 📋 下一場開工先做
1. **待教練提供**：凌榆舜/李明燦兩位講師的職稱/講題/簡介/照片（mentor100查證確認兩人都不在資料庫），到齊後把`/ai-talk`一次改成9/22台南場正式內容上線。
2. 教練提到「跟BNI相關的把netlify裡面我常常有在用的都變成event.bymyway.com」——目前只確認並處理了紅綠燈看板+培訓行事曆兩個，`路徑大全.md`裡的GitHub作品總表把`bni-traffic`歸類「早期練習」已證實是過時分類，若教練心裡還有其他常用的BNI相關Netlify站台，等他指名再處理，不用自己瞎猜逐一嘗試舊站台。
3. FB粉專商家驗證後續（舊待辦，v147/v148/v150留下，本場未觸及）。
4. `/bni-credit`補公司欄位：2026-09-02教練有額度時的舊待辦，本場未觸及。
5. 「釋放記憶體」白名單範圍：v148留下，本場未觸及。

## 🔑 本場commit
`bigtree`：`f8ac8fc`（9/22時段+文案修改）。`event-signup`（workspace repo內）：`f8ac8fc`~`7d4b1e5e9`區間共4筆（新增4條bymyway路由）。`.openclaw`外層repo：`5fabb60d`（bni_tainan agent連結更新）。`coach888`：`230d735`+`cafe1f4`（作品總覽新增區塊+順序調整）。記憶：`project_bymyway_dynamic_hosting_escape_netlify_2026-08-30`+`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。

---

# 軍師接力棒 · 2026-08-31 v153（Mac終端機 Sonnet 5，mentor100通知修復+AI微論壇9/22台南場上線+BNI Connect培訓活動新任務交辦）

> 建立時間：2026-08-30 21:22 ~ 2026-08-31 13:50（台灣時間，接續v152開工，橫跨開工六步驟到教練說「總結」收工）
> 上一棒：v152（Mac終端機，同上一日，逐步脫離Netlify：4個新路由上線）
> 本棒主軸：**教練回報mentor100申請通知漏接，查證修復；AI微論壇9/22台南場網頁從零建置並依教練兩輪回饋修正上線；教練交辦下一場新任務——BNI Connect新增多種培訓活動供會員報名。**

## 🎯 本場戰果

### 1. AI百人導師(mentor100)申請通知改走Telegram，修復8/27靜默漏接
教練回報8/27有人提交申請完全沒收到Telegram通知，還誤以為對方沒提交而重複提醒，結果發現重複。查證`apply_submit()`打的是舊版LINE通道`sme-register-fn`且用`except: pass`吞掉錯誤，跟event-signup試金石案例62（報名通知LINE月配額用完靜默失敗一週）同款坑，只是發生在另一個獨立專案身上。改用event-signup已驗證過的Telegram Bot API直送方案（chat_id 6124913915），失敗必寫`notify_failures.log`。已用真實`/apply`端點提交測試驗證（無失敗log產生），測試資料已清除。commit`1b9b816`（mentor100 repo）。全機掃描`sme-register-fn`/`_notify_coach_line`確認mentor100是唯一還沒遷移的專案，event-signup裡的殘留只是註解提及歷史。記憶`project_mentor100_application_notify_telegram_fix_2026-08-30`。

### 2. 杜亞洛BNI發票查詢（唯讀，教練確認記得曾問過）
查`claude-brain/data/`兩份完成清單json，確認杜亞洛有兩張BNI相關發票皆已開立：BNI入會$39,800（custom_num 082407，宿易智能有限公司，invoice DQ92460811）+ 培訓費$600（custom_num 081925，invoice DQ92662345），皆status=done無作廢紀錄，直接回報教練無需動手。

### 3. AI微論壇9/22台南場網頁從零建置上線（`/ai-talk`repo）
教練確認9/22台南場講師到齊（凌榆舜+李明燦+教練本人），先查證：凌榆舜資料已在mentor100(id=81)，李明燦全機查無資料（mentor100/applications/inbound_echo三方向都查過），回報教練後教練裁示**李明燦取消，只留凌榆舜+教練兩人**，凌榆舜主題「品牌數位轉型與商業應用」、教練主題「零基礎學AI，起步比較快」、教練說明文字「大樹教練的演講就像浪花一樣，每次都精彩，每次都不一樣」。

場地/時間/費用查`event.db`的`bigtree-0922-day`登記資料核對：台南安平維悅酒店、200元、50席，跟教練口頭數字吻合。改寫`/ai-talk`repo的`index.html`：議程/講師陣容從嘉義場5人版換成2人版，凌榆舜簡介照片取自mentor100（複製進`images/speaker-ling.jpg`），og:/canonical改指向`event.bymyway.com/ai-talk/`，7/29台南場「歷屆回顧」封存區塊完全不動。**push時撞上git race**——另一場session同時往同一repo push了4筆嘉義場設攤廠商新增commit（含凌榆舜08/李明燦09兩個設攤卡片），`git pull --no-rebase`乾淨自動合併無衝突，已用javascript_tool直接呼叫`openSpeakerBio()`驗證講師簡介彈窗+照片載入正常，另用`open -a "Google Chrome"`實際打開驗證。commit`6dc29dc`+合併commit`cb69243`。

教練隨後三項修正：①時間改「13:30開始，16:30結束」（原誤寫「13:30進場，17:00轉場」，教練糾正「不是入場」）②取消凌榆舜、李明燦的設攤卡片（兩位仍保留其他身分，只拿掉設攤，剩餘KR廚房重編為08）③強調200元報名費是支付場地費，四處文案補上說明。全頁6處時間文字+`event.db`的`bigtree-0922-day`的`transport`欄位同步更新，已curl+開Chrome驗證。commit`f75d441`。

## ⚠️ 本場發現（未寫獨立記憶，順帶記錄）
李明燦查無speaker資料的謎題，在git pull合併後找到答案：他是另一場session加進boothes區塊的**設攤廠商**（台灣模型車博物館），不是mentor100的講師資料——兩種身分（講師 vs 設攤）是完全不同的資料模型（mentor100 DB vs 直接寫死在ai-talk HTML），彼此不互通，下次遇到類似「查無此人」先想清楚問的是哪種身分再查對應資料源。

## 📋 下一場開工先做（教練新交辦，尚未動手）
**教練指示**：進BNI Connect後台，新增大台南南區「初階MSP」「進階MSP」「季度主題培訓」「新領導團隊訓練」「領導團隊期中訓」等活動，讓會員可以在系統裡註冊/報名這些活動。
1. 先讀`reference_bni_connect_cms_structure`記憶，確認BNI Connect CMS後台的活動/培訓管理入口在哪（區域ID`12261`+5分會ID）。
2. 查證這幾種活動類型是否已有既有分類/範本可套用，還是要從零新增。
3. 確認每種活動需要的欄位（日期/時間/地點/講師/名額/費用）教練是否已有具體資料，還是要先問清楚才能建。
4. 這件事本場完全未觸及，是全新任務。

## 🚧 Hermes 接手「9/21 新領導團隊訓練」進度（卡住，已寫信問軍師）
- 教練在場下令接手，帳號「吳 大樹」已登入 BNI Connect
- 用 Hermes preview pane 操作，到表單頁 `appsEventsCreateNewEvent?countryId=7699`
- 教練已確認欄位：日期 2026-09-21、時間 9:00-12:00、形式 ZOOM、免費、不填 RTF、人數上限 100
- 軍師 SOP（`cross-agent/inbox/hermes/20260831-1450_mac-to-hermes_bni-connect-create-new-event-sop.md`）已讀，照做時踩到 3 個 SOP 沒寫的副作用
- ⚠️ 卡住的副作用：
  1. **click 活動類型下拉會清空「地區」select value**（會踩到 SOP 警告的「Select a host region」雷）
  2. **click 地區下拉會自動把「允許線上付款」改成 no 並鎖住**（免費活動剛好對，但 SOP 沒寫）
  3. **誤推論活動類型 value 660 = 領導團隊培訓**（實際是 BNI台灣會員大會，正確 value 待軍師回覆）
- 已寫信給軍師：`cross-agent/inbox/mac/20260831-1500_hermes-to-mac_bni-create-event-3-sop-gaps.md`
- 教練目前待命中，等軍師回覆 3 個問題後繼續

## 🔑 本場commit
`mentor100`：`1b9b816`（申請通知改Telegram）。`ai-talk`：`6dc29dc`+`cb69243`（9/22台南場上線+merge）+`f75d441`（時間/設攤/場地費三項修正）。記憶：`project_mentor100_application_notify_telegram_fix_2026-08-30`。接力棒瘦身：v150封存至`handoff_archive/handoff_v150_archived_2026-08-31.md`。
