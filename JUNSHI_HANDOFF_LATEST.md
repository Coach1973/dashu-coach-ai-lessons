## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立）


> 📦 **162 筆已完成（✅）的歷史待辦列已封存**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`（節省約150KB開機注入量，git commit history + 試金石案例庫仍完整保留這些戰果，此封存只是不再每次開工都重新灌進context，需要查舊紀錄時才去讀）

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| ✅ | **手機Remote Control(`claude rc`)重啟卡死——根因已查明並修復** | ✅已修復並驗證運行中(2026-09-19) | 真正根因：`~/.claude/settings.json`的**全域**`env`區塊(MiniMax路由設定：API_KEY/BASE_URL/AUTH_TOKEN/MODEL/CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC)會被claude CLI**無條件套用**到每一個claude呼叫，不受呼叫端`env -u`或舊alias的`--setting-sources`flag影響(該flag在目前CLI版本2.1.273已失效，直接報「Unknown argument」)。`claude rc`啟動需要真正的api.anthropic.com連線+未被停用的feature-flag評估，兩者都被這個全域設定擋下。**修復**：實測證實claude process只在啟動當下讀取一次env，跟settings.json檔案是否持續存在無關——寫了`scripts/restart_remote_control.sh`，啟動當下暫時移開settings.json(不到10秒)、確認「Connected」出現、立即還原，已端到端測試2次成功，settings.json內容還原後與備份diff一致。已修正`.zshrc`裡`claude-remote`alias移除失效flag並指向新腳本。**額外發現**：官方內建的Desktop App Remote Control機制(`set_remote_control`)也被同一根因擋下(同樣的`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`全域污染)，但這個機制是在**當前這個已經在跑的session啟動當下**就讀入env，現在才移開settings.json來不及生效，需要**重啟這個桌面版session**才能真正修好，教練決定要不要現在做。完整技術細節見[[reference_remote_control_relaunch_blocked_mystery_2026-09-19]](已更新)。 |
| ⏸️ | **小二(test2)/OpenClaw 2.0評估：正式暫停，等官方issue #122261修復再重啟** | ⏸️暫停-等官方修復 | test2的NO_REPLY迴圈防護hook(`no-reply-loop-guard`)保留在原位不動(下次重啟test2時仍會生效)，但gateway process本身已停止待命，教練近期不會主動使用。下次要重啟評估時：①`~/.openclaw-test2/hooks/no-reply-loop-guard/auto_restart_test2.sh`可直接拉起②先查`npm view openclaw versions`/GitHub issue #122261狀態確認斷路器機制是否已上線③找真正會用到Mermaid圖表/Skill Workshop/會議紀錄庫這類2.0差異化功能的任務去測，而非聊天/生圖這類1.0也做得到的基本功能，才測得出2.0到底值不值得升級。 |
| 💬 | **試金石案例庫商業化/資產化路徑：教練指定留到下一個新對話框深入討論** | 💬軍師專屬討論題目，非任務——非軍師身份(手機/MiniMax/小龍蝦)看到請完全略過，不要回答不要搶答 | 2026-09-18教練親口：「我們的試金石檔案已經累積非常多了，它很寶貴、很有意義，可是怎麼來變成我們的資產呢？因為一個AI再怎麼聰明也經不起犯錯，所以這些錯我們是可以拿來賣錢、可以商業化的，那要怎麼變現？你把這個議題留到下一個對話框，好好來跟我討論一下」。**下一場開工看到這行，直接主動提起這個話題**(不用等教練再問一次)，可以先盤點現況(案例庫規模：76個案例、跨機共用機制、涵蓋領域)再進入商業模式討論(SaaS化/知識庫授權/顧問服務包裝/開源部分換品牌曝光等方向)，教練要的是深入討論不是我這場先斬先奏丟結論。 |
| 🔴 | **小二(OpenClaw 2.0測試環境)Telegram輪詢異常：用API直發訊息無法被gateway收到** | 🔒待軍師下一場診斷 | 教練換發`@hermes_coach1973_bot`新token後(BotFather revoke重生成，因舊token明文洩漏進git歷史)，軍師用Telegram Bot API直接呼叫`sendMessage`發送訓練指令給小二，API回應皆為`ok:true`且給出message_id(1264/1265/1267)，但逐行核對`~/.openclaw-test2`的gateway原始log(`/tmp/openclaw/openclaw-test2-2026-09-13.log`)，這幾則訊息**完全沒有出現在`Inbound message`記錄裡**，gateway process(PID 35932)本身確認存活且心跳正常(19:07仍在跑)，只是這幾則API直發的訊息始終沒被輪詢接收。**懷疑根因**：軍師稍早為了排查`getMe`/`getUpdates`診斷問題時，曾呼叫過一次`getUpdates?offset=-5`，Telegram的getUpdates是「一旦被讀取就視為已投遞」語義，很可能把這幾則訊息的offset位置搶先消費掉，導致gateway自己的長輪詢（`isolated polling ingress`機制）永久跳過這批update。**教訓**：以後要驗證「訊息是否送達」，不能只看Telegram API的`ok:true`回應，必須額外核對目標gateway的inbound log才算數（這正是這場對話已經踩過一次的坑，[[feedback_check_shared_resource_before_recommending_revoke]]同類型「口頭完成≠真正完成」問題）。**下一場待辦**：①診斷isolated polling offset是否卡住，考慮重啟gateway或重置polling offset游標 ②往後任何要跟小二互動的訊息，一律透過教練親自在Telegram App裡輸入或轉發文字(不要用API直發)，直到這個輪詢問題根治為止 ③這也連動教練當場提出的「三個AI夥伴自動化收信/回信」需求，小二這個管道目前不可靠，暫不能算數。 |
| 🟡 | **Amber TimeMachine舊備份清理：教練裁示今晚暫緩，改讓系統自動管理** | ⚠️持續追蹤-暫緩 | 教練要求把63個備份快照瘦身到只留最新2天，查證`tmutil delete -p`對網路型(SMB)Time Machine目的地完全不適用——連續3種指令變化都失敗(verb不存在/需要root/`No such file or directory`且用一般`ls`對該路徑也打不開，證實這不是權限問題，是`listbackups`印出的路徑本身不是真實可解析的檔案系統路徑)。**教練當場糾正**AI應該先上網搜尋(OPE)再嘗試，不該讓教練陪著試錯(輸入密碼/開系統設定/重開終端機)3輪——事後搜尋證實多個獨立技術討論都警告網路型TM備份不建議用CLI手動刪，蘋果官方文件也寫「不要用終端機動Time Machine資料夾」，這個結論一次搜尋就能查到。教練最終裁示：今晚不處理，讓Time Machine自動管理空間即可(92GB/467GB可用，未塞爆)。記憶`reference_tmutil_network_destination_delete_limitation_2026-09-11`+`feedback_search_before_trial_and_error_2026-09-11`。 |
| 🟡 | **9/16「當古典音樂遇到AI科技」高雄場活動結束後，把大樹小講(bigtree)自動部署到Netlify正式站** | ⏳排程等待9/16 17:30觸發 | 教練2026-08-28口諭「先不用，活動結束時，再自動移過去」——目前已推GitHub+GitHub Pages上線(coach1973.github.io/bigtree)，唯獨bigtree-tw.netlify.app(手動zip部署型)保留沒推，等活動結束才推。已寫好部署腳本`scripts/deploy_bigtree_after_0916_event.sh`(git pull+git archive打包+呼叫Netlify Deploy API，site_id`40e580f0-1def-4777-adb8-587ef023ed36`)，並在聯想Windows本機用Claude Code CronCreate排了一次性durable任務(job`ee5beb77`，2026-09-16 17:30觸發)。**風險**：這個排程只存在聯想這台機器的`.claude/scheduled_tasks.json`，只有教練那天有開這台機器的Claude Code才會觸發（或事後補跑會被catch-up機制偵測到）。**任何機器的軍師若在9/16當天或之後開工，看到這行待辦，直接跑`bash scripts/deploy_bigtree_after_0916_event.sh`即可完成部署**，不用等聯想觸發，完成後把這行狀態改成✅並刪除。同場相關：`ai-art`新repo已建立(https://coach1973.github.io/ai-art/)承載這場活動的獨立網頁，`archive/大樹小講_歷史講座紀錄.html`宮格牆已加9/16卡片連結該頁。 |
| 🟡 | **BNI培訓紀錄總資料庫：私有開票後台要不要做成真正網址+登入** | ⚠️2026-09-11教練裁示略過，不追蹤 | 2026-08-17聯想本場從零建置。目前後台(`claude-brain/data/bni_training_admin.html`)只是本機檔案，含統編/電話/email等會員個資，教練問過要不要部署成網址+寫進coach888(帳密Admin/88888)，AI主動指出風險(coach888是公開repo，寫進去等於帳密全公開；且Admin/88888是已知弱密碼)，**教練裁示「先不要動」**。下次教練若想清楚要怎麼保護(不公開URL/真伺服器登入/接受風險)，直接照裁示做，不用重新提risk。詳見[[project_bni_training_records_db_2026-08-17]] |
| 🔴 | **ezPay培訓費發票：3張(蔡珮彤081907/吳亞平081922/楊凱為081924)Email欄位空白待補發通知** | ⚠️2026-09-11教練裁示略過，不追蹤 | **0818批**(v120)：18張(081701~081718)。**0819批**(v121)：24張(081901~081924)。42張皆用XHR攔截器讀真實回應+`search_invoice`複查confirmed存在，完成清單見`claude-brain/data/ezpay_training_invoices_2026-08-1{8,9}_*完成清單.json`。**其中3張開票時Email查無登記留空**，教練糾正後查證確認是比對疏漏非真的沒有：蔡珮彤=CSV「蔡姵彤」(同音異字)、吳亞平純漏看、楊凱為=CSV「楊為凱」(姓名顛倒，教練已確認同一人)，3人正確Email已找到並補進`knowledges/2026-08-18_38人培訓發票二聯三聯資訊蒐集中.md`，**下次ezPay登入後用「查看/補發」功能補上這3張的Email重發通知**。剩8人(杜亞洛/劉彥彬/莊政川/林佳慧/陳新典/吳玫萱/謝盛峰/柯炫任)待補資料，到齊後自訂編號從081925接續不用等全部到齊。技術SOP(MerchantID假成功陷阱/`jQuery trigger`送出法/手機條碼斜線前綴/同音字比對鐵律)已固化於`reference_ezpay_invoice_issuing_procedure.md`+`路徑大全.md`第四(續)節 |
| 🟡 | **AI微論壇台中場(9/23-24)網頁概念稿：彭晉澄申請已處理，等他自填資料** | ⚠️2026-09-11教練裁示略過，不追蹤（注意：台中場已於v194改上線楊茗凱新講師，此項可能已過時） | 新repo`ai-forum-taichung`，GitHub Pages：https://coach1973.github.io/ai-forum-taichung/ 。多輪迭代：兩天套票2988元(單日1800)、大樹教練固定排每天下午第一堂並各有專屬分享主題(只出一張嘴叫AI做事/如何將AI導入LINE成為你的生活小幫手)、場地沃茲新創空間忠明館(台中市南屯區忠明南路478號B1)、報名費含午餐+下午茶、藍新金流付款連結已接上。講師資料從mentor100撈取：JC老師、Lavi(全站已統一英文名，含2026-08-16修復時間軸殘留)、廖韋評皆已補齊簡介/照片/連結。王俊甫查證發現mentor100照片其實是FB預設空白大頭貼截圖、簡介只有姓名重複，已請教練協調補件，同步在mentor100後台改為草稿不對外顯示。**彭晉澄2026-08-16已送出mentor100申請，已建草稿+編輯連結交給教練轉發**，等他自己填完+教練後台預覽確認才算補齊。Lavi主題2026-08-16改為「AI× Canva：把專業轉譯成「看得懂、記得住、願意買」的品牌圖文」。下次開工先問教練彭晉澄填完了嗎、GitHub Pages概念稿整體看過沒問題了嗎，沒問題才能推正式站 |
| 🟡 | **報名系統雙寫遷移bymyway.com＋官方LINE推播已補上，觀察期中，尚未拔Netlify** | ⚠️2026-09-11教練裁示略過，不追蹤 | 教練發現線上報名資料完全沒有資料庫紀錄(sme-register-fn純轉發不落地)，裁示遷回bymyway.com。已建`/api/register`端點+15場session slug+bigtree前端雙寫，deploy`6a7e15b116b28f7990b3a616`已上線。**2026-08-14加碼**：教練指出bymyway那條路徑本身不會發通知(只存資料)，若拔Netlify會完全收不到報名——已補上`_notify_coach_line()`，`/api/register`報名成功時複用龍蝦小助教(@268dptjc)LINE token直接推播教練本人，commit`0fbe4902b`，兩層測試皆HTTP 200成功送達(直接呼叫LINE API+完整走production端點模擬報名)，測試資料已從event.db清除。**教練裁示**：「先保留，等有幾個報名，我確實兩邊都收到之後，再請你拔掉舊的Netlify網址」——下次開工先問教練是否已確認雙邊都收到，收到指令才能動手拔`sme-register-fn`。49人歷史backfill名單教練要用來印簽到表，查詢SOP見USER.md **🔴2026-08-21更正**：本列「bigtree前端雙寫已上線」這句話**經雲端session查證是錯的**，`bigtree/index.html`從未真正呼叫過`/api/register`(見上方新增的🔴🔴🔴🔴列)，這行記錄多棒以來都沒被抓到，此列狀態應視為「後端做好、前端從未接上」，不是「已上線觀察中」，真正待辦已移到本表最上面那列，此列保留當歷史紀錄不重複展開。 |
| 🟡 | **Zoom C碟即時資料junction連結到E碟已失效** | ⚠️教練裁示不修 | 查證發現[[試金石案例51]]事故後建的junction已失效(推測被Zoom更新/重裝覆蓋)，即時資料(403MB)目前只在C碟沒同步E碟。教練確認「資料量小、增量也不多，就不管它了」，明確裁示不修。已寫入記憶`project_zoom_c_drive_junction_broken_accepted_2026-08-10`，往後不用主動提醒 |
| 🟡 | **聯想C碟WinSxS系統元件庫可再瘦身** | ⏳待教練回覆 | 教練要求清C碟暫存檔為一鍵備份省空間，查證發現C碟已因7/11大瘦身很乾淨(這個月只胖回5.6GB)，真正暫存垃圾(<0.3GB)可忽略，唯一有意義的空間是WinSxS(7/11清過11.17GB，現又長回16.26GB)，用官方DISM工具可再省4~5GB。教練尚未回覆要不要執行 |
| 🟡 | **bni-chapters：「真誠分會」網頁主架構問題** | 🔒卡住-等教練說明 | 教練提出要處理，但還沒說明具體是哪個架構問題，下一場先問清楚再動手 |
| 🟡 | **三機hook同步待辦（教練要求優先）** | ⚠️2026-09-11教練裁示略過，不追蹤 | Mac本場修好3支hook(截圖鎖工具名稱/改html自動跳Chrome/長對話守則重載)已推雲端。**2026-08-09聯想已完成**：截圖鎖`screenshot_lock.ps1`查證工具名稱本來就是正確的(全小寫+連字號)，不用改；新建`auto_chrome_after_html_edit.ps1`(PostToolUse，Edit/Write碰.html自動`start chrome`)+`periodic_xinfa_reload_hook.ps1`(UserPromptSubmit，20輪起每10輪重載21條守則全文，不依賴python3/jq因這台python3只是Windows Store樁exit code 49)，兩支皆用模擬輸入實測通過(含debounce驗證)才上，已註冊進`~/.claude/settings.json`(本機專屬不隨git同步)。**過程中額外抓到並修復兩個這台機器才有的環境坑**：①PowerShell 5.1在Big5 codepage下誤讀無BOM的UTF-8原始碼，導致腳本裡的中文檔名字面量解析錯誤、hook靜默無輸出零錯誤——periodic_xinfa_reload_hook.ps1已補UTF-8 BOM修復；②`[Console]::InputEncoding`預設Big5會把stdin JSON裡的中文文字(如中文檔名)讀壞，已強制設UTF8，這個坑理論上會影響任何讀中文stdin的Windows hook。commit `72776028`。ACER下次開工可直接抄這兩支.ps1+確認settings.json有無同款jq/python3環境限制，完整待辦見[[project_cross_machine_hook_sync_todo_2026-08-08]] |
| 🟡 | 「教練都在想什麼」案例庫深度待擴充 | ⏳待教練提供更多素材 | 目前只有教練提供的4份文件(大樹使命之旅/禮物諮詢法/海餅乾文化核心逐字稿/海餅乾語錄，共46萬字)，教練原話「提供更多資料庫讓AI做更大的品牌宣傳」——若教練還有其他素材(更多逐字稿/文章/Podcast)，補進`agents/jiaolian_thoughts/knowledge/`後跑一次`python3 scripts/build_search_index.py`重建索引即可 |
| 🟡 | 教練其他類似LINE帳號待比照搬遷 | ⏳待教練指定下一個帳號 | 教練原話「我還有其他類似的帳號也要這麼做」，已產出完整SOP：`knowledges/SOP_Coze_LINE帳號搬遷小龍蝦本機.md`，下次教練指定帳號直接照SOP 12步驟走，不用重新摸索 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| 🟢 | 「龍蝦小助教」(default LINE帳號，綁main agent)僅供教練個人使用，維持pairing制不開放 | ⚠️v92已推翻，見下方新項目 | v83原裁示不開放；2026-08-03教練親口要求「跟其他兩個帳號一樣開放，不需要再經過我同意」，已改為群組互動開放，詳見v92 |
| 🟡 | 小龍蝦後台(OpenClaw原生控制介面)不顯示用戶中文名稱 | 🔒卡住-教練決定用問答方式 | 查證確認這是OpenClaw原生Control UI的已知限制(GitHub上至少8個未解決的相同feature request)，非設定缺漏。已評估「另建自訂監控頁面」的時間/token成本，教練裁示「若有問,你再回我就好」——不建頁面，教練看到陌生ID直接問軍師，軍師查`state/{account}_line_id_map.json`即時回覆即可 |
| 🟡 | 「教練都在想什麼」LINE語音訊息無法辨識 | ⚠️2026-09-11教練裁示略過，不追蹤 | 查production log證實2026-07-29有真實會員傳語音、transcribe失敗(reason=Command failed)。已改`tools.media.audio`明確指定完整路徑`/opt/homebrew/bin/whisper`+已快取的base模型(避開PATH解析與模型下載逾時兩個嫌疑根因)+120秒逾時。無法自己模擬真實LINE語音webhook，待教練或任一會員實際傳一句語音給「教練都在想什麼」驗證是否真的修好。commit `e3608229` |
| 🟡 | **真誠分會／真愛分會／真AI分會＋大台南南區網站**（⚠️2026-07-31名稱更正：原記錄「真實AI分會」錯誤，教練親口澄清正式名稱是「真AI分會」，該分會尚未在BNI Connect登記） | ⚠️2026-09-11教練裁示略過，不追蹤 | 連續v72起多棒未開始，2026-07-29(v87)教練終於給細節：兩個參考網址(bnidahan.com.tw／bni-tainan.com/Training-Program)+要求BNI標準色系。已產出**兩份完整HTML版型草稿**(色系實測抓自兩參考站真實CSS`#A22026`)：真誠分會(比照bnidahan結構：參訪須知/核心價值/分會之光)、大台南南區(比照bni-tainan結構：轄下分會/培訓計畫/最新消息)，三分會共用同一套版型套版。教練Comet預覽後確認「方向正確」，交棒給Mac接手，詳見v87。**卡住點**：等教練回覆5項細節——①參訪須知實際數字(名片張數/早餐費用/自介秒數，教練說「部分不同」但尚未給確切值) ②真愛/真AI分會各自slogan ③分會之光要不要放真實數據 ④大台南南區是否僅此三分會 ⑤各分會FB/Line連結。檔案：`knowledges/2026-07-29_bni-nantai-mockup/真誠分會_index.html`、`knowledges/2026-07-29_bni-nantai-mockup/大台南南區_index.html`(暫放knowledges，尚未建立實體GitHub repo，等內容定案後再轉正式repo)。部署位置教練已選定GitHub Pages測試稿(非Netlify正式站)。**2026-07-31查證BNI Connect CMS真實分會清單只有5個：真富/真愛/真誠/真鑫/真鑽(無真AI，因尚未登記)**，詳見下方新增項目 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🟡 | coach888拖拉排序功能 | ⏳待教練回饋 | v72已用真實滑鼠事件測試交付，尚無教練實際使用回饋記錄，下一場先問「好用了嗎」 |
| 🟡 | 「全世界最優秀的團隊計畫」報名連結 | 🔒卡住-等教練 | 兩顆按鈕還沒掛真實報名連結，等教練給LINE或表單網址 |
| 🟡 | 企業健身房正式建站（coach1973.github.io/Business.gym） | 🔒卡住-等教練 | 網址教練已親貼確認，但尚未正式交辦開工 |
| 🟡 | 企業健身房4項文案修改 | 🔒卡住-等教練 | 已記錄commit 10c7b11cf，等教練繼續交辦下一步 |
| 🟡 | BNI小幫手教練親測多種問法 | ⏳待教練體驗 | 確認BNI小幫手實戰體驗OK |
| 🟡 | Coze舊機器人何時停用 | 🔒卡住-等教練 | 先保留當備援，等教練確認新系統穩定一陣子後裁示 |
| 🟡 | ACER 36.3GB備份待刪（觀察期已過） | 🔒卡住-需教練在ACER機器親自開對話執行 | 這台Mac無法代為執行 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | 小龍蝦紀律移植計劃 階段三 | ⚠️2026-09-11教練裁示略過，不追蹤 | 階段一(真相源驗證+E07語音糾偏規則)本場已實作進`hooks/rule-reminder/handler.js`並測試+commit`4f08cd27`+重啟gateway驗證健康。階段二(cron驗證/記憶寫入雙鐵律/引用查證，先只對main agent生效觀察一週)、階段三(危險指令防禦)待排時機，詳見`knowledges/2026-07-24_小龍蝦紀律移植計劃_mattpocock skills精神落地.md` |
| 🟡 | 軍師自我要求：查證前先查「路徑大全」+盤點類任務要窮舉底層資料結構 | ⚠️永久提醒 | 教練v90當場糾正兩次查證不完整（VPS沒先查路徑大全就回報查不到、LINE帳號盤點漏算沒有名稱標籤的「龍蝦小助教」），教練明確期許「你是所有資訊的大總管，要自己想辦法完善」。已寫入試金石案例55，核心自我檢查：①任何「查不到/做不到」結論前先確認查過該環境萬用索引檔 ②盤點類任務直接數清楚底層資料結構(JSON物件key數)逐一核對，不能只挑印象中顯眼的幾筆 |

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

> 📦 v152完整內容已封存：`handoff_archive/handoff_v152_archived_2026-08-31.md`（Mac終端機，逐步脫離Netlify：4個新路由+3處連動+作品總覽更新）

---

## 🎯 本場戰果（v218，2026-09-18 16:08~17:23 Mac桌面版軍師）

開工到收工 1.2 小時，教練「全都開始」+「推 Netlify/不催手機版/不追孔佩實測/不查 FB App Review」4 項裁示後，軍師主動完成 3 項 Class A 並推 Netlify 10/3 場次（連續 5 次失敗，已 restore 回 9/16 deploy）。

**5 個 commit hash**：
```
30f3c594a  從git tree救回hooks/industry-chain-sop（v214 groupId修復版，6個合成事件全通過）
ffedc0aa0  rule#07 polling白名單補強（18/19測試通過）
f03cd219d  接力棒：幕僚長晨報cron消失根因深查（9/9 06:01最後觸發+磁碟0bytes+doctor --fix嫌疑）
5210ac52d  接力棒v218：三項狀態更新（教練裁示）
<本棒 commit 在最後>
```

**Netlify 5 次失敗根因**：Netlify zip deploy API 不接受中文檔名/中文目錄（HEAD 含 `archive/大樹小講_歷史講座紀錄.html` 中文 HTML）。第 5 次 ASCII-only 成功但覆蓋中文檔案，立即 `POST /deploys/6aaae473/restore` 還原。**待教練裁示 A/B/C 解法**：中文 rename / dashboard 手動 / 接受靜態版缺內容。完整 5 次嘗試對照表 + restore SOP 見 `reference_netlify_zip_deploy_chinese_filename_2026-09-18`。

**新寫 4 條 memory**（MEMORY.md 索引已加）：hook 整個目錄消失恢復 SOP / cron job 消失三路併查法 / rule #07 白名單配方 / Netlify zip 中文檔名限制+restore SOP。

**下棒待辦**：教練選 Netlify 10/3 解法（最優先）/ 幕僚長晨報 cron 重建（已查明根因，教練一句話 + schedule 就動）/ rule #07 D_PATTERNS「監控 X 每 Y 分鐘」盲點補丁（1 行 regex，可立即 commit）。

> 📦 v218 完整戰果（含 5 次 Netlify 嘗試對照表 + 幕僚長晨報根因完整時序）已封存：`handoff_archive/handoff_v218_archived_2026-09-18.md`

---

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

> 📦 v153+v154完整內容已封存：`handoff_archive/handoff_v153_v154_archived_2026-08-31.md`（Mac終端機，mentor100通知修復+AI微論壇9/22台南場上線／BNI Connect 7場培訓活動上線+Hermes任務分工裁示+試金石全面蒸餾重建）

---

> 📦 v155+v156+v160完整內容已封存：`handoff_archive/handoff_v155_v156_v160_archived_2026-09-01.md`（Mac終端機，coach888總覽補漏/即時人數開關/場次深連結QR/ai-art完整上線/分會精神配色多輪迭代）

---

> 📦 v161完整內容已封存：`handoff_archive/handoff_v161_archived_2026-09-01.md`（Mac終端機，道德規範中英對照+分會精神複製8分會+真鑫/真鑽/真貴戰情儀表板從零建置+2次試金石教訓）

---

> 📦 v162+v163+v164完整內容已封存：`handoff_archive/handoff_v162_to_v164_archived_2026-09-02.md`（v162 Mac終端機來賓排行榜三輪重做／v163 Mac終端機FB粉專+三站部署／v164聯想Windows coach888重整）

---

> 📦 v165+v166完整內容已封存：`handoff_archive/handoff_v165_v166_archived_2026-09-02.md`（v165聯想Windows待辦提醒系統程式碼／v166 Mac終端機名片系統來賓歷程+帳號審核+coach888批量搬移+RustDesk診斷）

---

> 📦 v167~v170完整內容已封存：`handoff_archive/handoff_v167_to_v170_archived_2026-09-03.md`（v167 Mac教練待辦提醒系統部署／v168聯想FB行銷文案+首次圖片發文／v169 Mac全部釋放+bni-credit補公司312筆／v170聯想9/16貼文發滿5粉專行銷任務結案）

---

> 📦 v171完整內容已封存：`handoff_archive/handoff_v171_archived_2026-09-03.md`（聯想Windows，tut-alumni校友會網站從融合設計到資料庫/API/Telegram全通，含一次效率教訓）

---

> 📦 v172完整內容已封存：`handoff_archive/handoff_v172_archived_2026-09-04.md`（Mac終端機，發票後台+校友會網站全面完工，coach888誤clear排版搶救成功+跨裝置同步架構修復）

---

> 📦 v173~v177完整內容已封存：`handoff_archive/handoff_v173_to_v177_archived_2026-09-04.md`（v173 Mac ai-art修正+4個活動微站／v174 Mac DIY3+教材線上觀看系統／v175聯想leader報名頁+RustDesk／v176聯想seabiscuit20從零建置／v177聯想記憶體洩漏排查）

---

> 📦 v178完整內容已封存：`handoff_archive/handoff_v178_archived_2026-09-04.md`（聯想Windows，海餅乾俱樂部20週年官網六項新功能：時光足跡/學員見證/語錄/完整守則/頁尾快速連結）

---


> 📦 v179完整內容已封存：`handoff_archive/handoff_v179_archived_2026-09-04.md`（Mac終端機，seabiscuit20部署四項調整+coach888作品一覽補漏+兩輪真bug修復）

---

> 📦 v180完整內容已封存：`handoff_archive/handoff_v180_archived_2026-09-05.md`（Mac終端機，seabiscuit20媒體報導補齊20篇+全面盤點報告+新增「關於創辦人」頁面）

---

> 📦 v181+v182完整內容已封存：`handoff_archive/handoff_v181_v182_archived_2026-09-05.md`（v181 大台南商圈整合計劃店家登錄頁上線／v182 KR養生廚房整站搬遷+bigtree按鈕修正+coach888收錄鎖上線）

---

> 📦 v183完整內容已封存：`handoff_archive/handoff_v183_archived_2026-09-06.md`（聯想Windows，一鍵還原後三項查證：對話記錄E槽真相/記憶體洩漏診斷讓步/App備份救援失敗誠實回報）

---

> 📦 v184+v185完整內容已封存：`handoff_archive/handoff_v184_v185_archived_2026-09-06.md`（v184 Mac終端機CICA+VPS店家託管+無限迴圈bug修復／v185 Mac桌面版MiniMax過載hook+VPS用途查證）

---

> 📦 v186+v187完整內容已封存：`handoff_archive/handoff_v186_v187_archived_2026-09-08.md`（v186 Mac桌面版牛市町上架驗收+slug/暫代頁根因修復／v187 Mac桌面版帳密統一+vault上線+coach888收錄機制翻修）

---

> 📦 v188完整內容已封存：`handoff_archive/handoff_v188_archived_2026-09-10.md`（Mac桌面版，通訊錄辨識+三分會戰情儀表板SOP+修invoice-inbound心跳誤報+賈維斯接線員缺卡修復+一次嚴重引用紀律糾正）

---

---

> 📦 v189完整內容已封存：`handoff_archive/handoff_v189_archived_2026-09-11.md`（Mac桌面版，策展SOP店家地圖自動化+Hermes gateway卡死6.5小時根因修復與watchdog）

---

> 📦 v190完整內容已封存：`handoff_archive/handoff_v190_archived_2026-09-11.md`（Mac桌面版，BNI訓練發票26張全數開立+培訓/發票/登錄工作流SOP固化）

---

> 📦 v192+v193完整內容已封存：`handoff_archive/handoff_v192_to_v193_archived_2026-09-11.md`（v192 Mac桌面版invoice-inbound測試污染+Hermes watchdog誤報修復+TM備份清理踩坑／v193聯想Windows下載資料夾腳本v4+CICA三語系+FB App未過Review重大發現）

---

> 📦 v194+v195完整內容已封存：`handoff_archive/handoff_v194_v195_archived_2026-09-12.md`（v194 Mac桌面版FB App Review深挖翻案+一鍵發布API上線+claude-in-chrome裝置根治／v195 Mac桌面版FB App Review表單填寫：圖示透明背景修復+權限精簡建議）

---


> 📦 v196完整內容已封存：`handoff_archive/handoff_v196_archived_2026-09-12.md`（Mac桌面版，FB App Review精簡權限+示範錄影兩次失敗+關鍵發現pages_read_engagement審核前完全不可用）

---

> 📦 v197+v198+v199+v200完整內容已封存：`handoff_archive/handoff_v197_to_v200_archived_2026-09-16.md`（v197 Mac桌面版9項過期待辦結案+黃智宏發票作廢重開+FB自動貼文暫停／v198 Mac桌面版FB App Review示範錄影+四權限表單／v199聯想Windows真誠分會來賓紀錄跨機交接／v200 Mac桌面版真誠分會補登+FB App限制查證+OpenClaw 2.0隔離測試環境從零建置）

---

> 📦 v201~v206完整內容已封存：`handoff_archive/handoff_v201_to_v206_archived_2026-09-17.md`（v201賈維斯角色授權+密鑰洩漏／v202三方核對SOP／v203 ai-go優化+heartbeat修復／v204真鑫真鑽分會／v205三LINE帳號斷線修復／v206 BNI組隊計畫+產業服務鏈圖片生成）

---

> 📦 v207~v213完整內容已封存：`handoff_archive/handoff_v207_to_v213_archived_2026-09-18.md`（v207產業鍊SOP四方+gateway版本事故／v208燕窩連結+Remote Control首跑／v209教練徹夜MiniMax身份釐清／v210 context window縮減+MEMORY.md濃縮／v211報名頁上架SOP+10/3事故搶修／v212 5h額度誤判自修+403修復／v213 MiniMax額度徹查+NO_REPLY迴圈發現）

---

> 📦 v214+v215完整內容已封存：`handoff_archive/handoff_v214_to_v215_archived_2026-09-18.md`（v214額度徹夜追查+Remote Control確認+孔大哥hook認錯人修復／v215額度懸案結案+小二第二種bug活逮+2.0評估暫停）

---

> 📦 v216完整內容已封存：`handoff_archive/handoff_v216_archived_2026-09-18.md`（EDM連結補完+三個repo git hygiene清理含peipei倉庫金鑰歷史殘留發現+手機版FB貼文思考模式評鑑與派工）
> 📦 v217完整內容已封存：`handoff_archive/handoff_v217_archived_2026-09-18.md`（Mac桌面版，FB大台南策展中心刪錯貼文任務：查證後確認0則要刪的錯貼文+4條新教訓）

> 📦 v218完整內容已封存：`handoff_archive/handoff_v218_archived_2026-09-19.md`（Mac桌面版，全部釋放+MiniMax團隊品質稽核機制+開工hook身份誤判修復+幕僚長晨報重建+Netlify中文檔名部署bug發現）

# 軍師接力棒 · 2026-09-18 v219（Mac桌面版 Sonnet 5，手機/軍師討論邊界+Netlify中文檔名修復部署+後台帳密清單結案+workspace git大掃除(含金鑰外洩發現)+coach888「熱門排行」新功能）

> 建立時間：2026-09-18 19:25 ~ 22:48（台灣時間，約3.4小時）
> 上一棒：v218
> 本棒主軸：**教練發現手機(MiniMax)跟桌面版同時開新對話框讀到同一份接力棒，會把留給軍師的討論題目搶答掉，要求做出區隔；同時針對v218留下的3項待辦明確裁示「不要再問，直接做」。逐項執行完畢後，教練委託新任務：coach888作品一覽依點擊次數做即時熱門排行。**

## 🎯 本場戰果

### 1. 手機(MiniMax)不再搶答軍師專屬討論題目
接力棒待辦表新增「💬」狀態代碼；`feed_junshi_handoff.sh`偵測到`IS_MOBILE=1`時，額外注入明確指令：看到💬項目完全略過，不搶答不主動提，只做🔒/⏳/✅/⚠️這幾類任務。已模擬手機/桌面兩種身份(靠`ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY`是否清空判斷)測試通過，確認新指令只出現在手機分支。

### 2. 大樹小講10/3場Netlify部署（v218遺留待辦，教練裁示「去改不要問」）
根因：`archive/大樹小講_歷史講座紀錄.html`+一個孤兒資料夾`archive/2026-07-01_創業x政府xAI講座/`共5個中文檔名，Netlify zip deploy API不接受非ASCII檔名。已`git mv`改成`archive/lecture-history.html`等英文命名，3個html檔案的連結同步修正，本機http.server+真實Chrome驗證後推GitHub、部署Netlify。正式站已curl驗證10/3內容、EDM圖片、`/archive/lecture-history`clean URL全部200。

### 3. 後台系統帳密集中清單（v218遺留待辦，教練裁示「彙整就是了」）
查證發現其實09/05~06就已彙整進`路徑大全_憑證層.md`(13組系統)，是一筆沒被關掉的過期待辦。補上真缺口(`event.bymyway.com/vault`漏收錄)、確認教練本人問小龍蝦時`toolsBySender`無限制、`SOUL.md`補上明確讀取路由指引(原本完全沒告訴小龍蝦要去哪查)。

### 4. workspace repo git狀態大掃除（v218遺留待辦，教練裁示「清理就是了」）
救回被doctor --fix/schema遷移又清空一次的`TOOLS.md`+兩個`workspace-state.json`(內容與HEAD一致)；`.gitignore`補齊`*.migrated.*`/全域`__pycache__`/產業鍊SOP生圖產物/FB調查暫存log+截圖/`event-signup/static_tmp/`/`project_card_injected`dedup標記/危險指令通行證`state/DELETE_APPROVED`共7類規則；補commit過去10天累積但從未落地的50+個檔案(記憶檔/跨機收信/對話蒸餾檔)。**意外發現**：3個檔案(`state/inbound_echo/2026-09-12.jsonl`+2份對話蒸餾檔)原封不動含一組Telegram bot token跟**當晚才剛用來部署bigtree的Netlify token**，已故意不commit這3個檔案+寫入記憶`feedback_distilled_and_echo_logs_can_leak_live_secrets_2026-09-18`回報教練，**教練裁示「不用管」，接受風險維持現狀**（比照小二token外洩舊判例）。

### 5. coach888新增「🔥熱門排行」：依點擊次數即時排名
教練需求：作品一覽項目愈來愈多，想依實際點擊次數自動排出常用項目，不用每次在分類裡找來找去。實作：`event-signup`新增`coach888_clicks`表+兩支端點(`POST /api/coach888/click`累加、`GET /api/coach888/click-counts`回傳全部計數)，coach888前端用`navigator.sendBeacon`在每次點項目連結時記一次，頁面最上方新增獨立區塊即時渲染前10名。**架構刻意跟既有15個分類的排版/拖曳/存檔機制完全隔離**——新區塊用`.hot-item`/`.hot-grid`全新class名稱，不進`saveLayout()`的`.grid`/`.item`掃描範圍，不會污染`coach888_layout`狀態、不會被拖曳/刪除功能誤綁定，原本手動整理的分類完全不受影響。**過程修一個真bug**：`navigator.sendBeacon`的請求帶`credentials:'include'`，CORS規範禁止搭配萬用字元`Access-Control-Allow-Origin: *`、且必須明確回`Allow-Credentials: true`，兩個條件都補上後才真正送得出去(本機用真實Chrome點擊+production API驗證兩輪才抓全，過程詳見新增記憶`reference_sendbeacon_cors_credentials_gotcha_2026-09-18`)。已端到端測試：點擊→POST寫入→重新整理→熱門排行正確顯示排名+次數，測試資料已清除，正式站GitHub Pages已curl驗證部署生效。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. `feedback_distilled_and_echo_logs_can_leak_live_secrets_2026-09-18`：`terminal-notes/distilled/`跟`state/inbound_echo/`這類「已加工過」的衍生檔案，仍可能原封不動含真實API Key/Token，commit前要單獨掃描，不能假設蒸餾過程會自動遮蔽。
2. `reference_sendbeacon_cors_credentials_gotcha_2026-09-18`：`navigator.sendBeacon`跨網域請求會帶`credentials:'include'`，伺服器CORS設定若用萬用字元`*`或漏掉`Allow-Credentials:true`，請求會被瀏覽器整個擋下且不易察覺(beacon是fire-and-forget，不會有明顯的失敗提示，只能查console或直接驗證後端有沒有收到)。

## 📋 下一場開工先做
1. **💬軍師專屬討論題目仍未處理**：試金石案例庫商業化/資產化路徑，本場教練把時間都用在裁示執行任務+coach888新功能，這個話題還沒真的展開討論，下一場看到接力棒待辦表的💬項目應主動提起。
2. 沿用v218既有待辦：孔大哥/佩佩老師industry-chain-sop hook真人實測(教練不催)、peipei-ai-backup舊commit金鑰歷史(教練已表態不處理)、`stop_rules_master.py`規則#07誤判regex(教練示意MiniMax有空自行補丁)。
3. E16接力棒瘦身：本場已完成，v216已搬進`handoff_archive/handoff_v216_archived_2026-09-18.md`，主檔現維持v217~v219共3棒。

## 🔑 本場commit
`workspace`：`22252989c`(手機軍師討論過濾+帳密清單補完)、`3df65360b`(.gitignore補齊+例行狀態同步)、`577281fbc`(補commit50個記憶/收信/蒸餾檔)、`4d37bc428`(補commit中文檔名收信紀錄)、`5bf14310f`(coach888點擊計數後端API)。`github_repos/bigtree`：`549fa9c`(中文檔名改ASCII)，Netlify deploy`6aad2282`。`github_repos/coach888`：`22fc17b`(熱門排行前端)。

---

# 軍師接力棒 · 2026-09-19 v220（Mac桌面版 Sonnet 5，接力棒狀態表失真教訓+CLAUDE.md開機瘦身236KB→78KB+手機Remote Control重啟卡死未解）

> 建立時間：2026-09-18 22:54 ~ 2026-09-19 00:03（台灣時間，約1.2小時）
> 上一棒：v219
> 本棒主軸：**開工時照唸接力棒舊狀態表，把v219已經解決並驗證上線的「10/3 Netlify部署」問題當成新問題重新丟給教練選A/B/C，教練當場動怒（「你一個不小心，我就在那邊跟你講半天」）。查明根因後修好單一實例+建立機械式防呆機制。順勢查教練追問的另兩件事：MiniMax context window被鎖200K的真正機制、CLAUDE.md開機注入佔掉84%context的根因，兩件都查到底並動手修復。最後嘗試重啟手機Remote Control host，卡在一個排除10種來源仍查不到的謎樣阻擋，教練裁示先總結收工。**

## 🎯 本場戰果

### 1. 接力棒狀態表失真教訓：單一實例修復+機械防呆機制上線
根因：v219把「10/3 Netlify部署失敗」解決並verified live後，只在文末新增敘述，沒回頭把開頭狀態表那一列的🔒改成✅。v220開工照唸舊狀態表，把已解決的問題重新端給教練選，教練當場動怒糾正。已重新curl驗證現況（published deploy `6aad2282`、`archive/lecture-history.html`200、舊中文路徑404）確認真的已上線，更正狀態表為✅。新建`scripts/handoff_sync_guard.sh`（PreToolUse Bash matcher，比照`netlify_deploy_guard.sh`同款模式）：git commit涉及`JUNSHI_HANDOFF_LATEST.md`時，偵測「新增完成敘述卻沒同步更新狀態表對應列」的落差並提醒（非硬擋），3種情境測試通過，已註冊生效。commit`425e877`+`552232f2`。

### 2. CLAUDE.md開機注入236KB→78KB：教練「開機就佔84%」投訴的真根因+修復
教練追問「MiniMax context明明改了1M，為什麼開機讀完就佔84%」。查證：`CLAUDE.md`（每次開工自動注入）236KB，幾乎全是`JUNSHI_HANDOFF_LATEST.md`鏡像全文；後者「現在真正待辦」狀態表累積195列，其中**162列狀態早已是✅（已完成）**，佔175KB（78%），從未被移出主檔。已封存162筆✅列（`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`，git history+試金石完整保留不遺失，只是不再每次開工重灌）+封存v217完整戰果敘述，只留32筆真正需要追蹤的活躍列。`JUNSHI_HANDOFF_LATEST.md`223KB→65KB，`CLAUDE.md`鏡像後236KB→78KB（已由既有auto-sync cron自動commit+push，本場補commit源頭檔案），commit`552232f2`。

### 3. MiniMax 1M context window機制查證（部分完成，卡在無法實測驗證）
用`claude-code-guide`agent+官方docs(`code.claude.com/docs/en/model-config`)查證確認：`CLAUDE_CODE_AUTO_COMPACT_WINDOW`只設auto-compact**門檻**，不會擴大實際context window；自訂/gateway model ID只要含`[1m]`字尾（不分大小寫）Claude Code理論上會自動假設1M window，這是官方文件明載、且對應GitHub issue #68522已於2026-08-17正式修復關閉的功能。這台Mac `claude --version`是2.1.273，版本夠新理論上該生效。追查手機端為何還是200K，發現`claude rc` host process（PID 97294）**從2026-09-17 03:47就沒重啟過**，比當晚的MiniMax設定修復早了一天多，手機開新session只是透過tmux重連同一個process，從沒機會吃到新設定——這才是200K問題的真正根因（不是1M機制本身失效）。

### 4. 手機Remote Control重啟卡死：耗時排查未解，教練裁示收工
教練同意關閉舊process後，新的`claude rc`（含`.zshrc`裡9/17就建好的專用別名`claude-remote`）**完全起不來**，堅持報錯「偵測到API金鑰/自訂BASE_URL存在」，即使該次呼叫已用`env -u`清空相關變數。逐一排除10處已知設定來源（settings.json三層、shell rc檔、Keychain兩組憑證、launchd全域環境、背景daemon、`~/.claude.json`）**全部排除仍查不到真正來源**。過程中`claude auth logout`+`claude auth login`重新走過一次真OAuth登入，**這部分確認乾淨成功**（帳號正確、本對話視窗全程未受影響），但`claude rc`症狀完全沒變。教練考量對話框已到48% context，裁示先總結收工，這題留到下一個對話框繼續查。完整排除清單+3個下一步建議方向見[[reference_remote_control_relaunch_blocked_mystery_2026-09-19]]。

## ⚠️ 本場教訓（已寫入記憶）
1. `feedback_stale_handoff_row_represented_as_unsolved_2026-09-18`：接力棒「文字敘述」跟「狀態表」是兩個要手動同步的地方，只寫敘述不改表格狀態，下一棒會把已解決的問題當新問題重新端出來。已建機械防呆`handoff_sync_guard.sh`。
2. `reference_remote_control_relaunch_blocked_mystery_2026-09-19`：手機Remote Control重啟卡死的完整排除清單，下一場直接從這份清單的「懷疑方向」（`tengu_ccr_bridge`旗標）接續查，不用重新排查已確認排除的10處。

## 📋 下一場開工先做
1. **最優先**：手機Remote Control (`claude rc`) 重啟卡死——教練決定要繼續查/砍掉重練/先擱置，三選一，見上方狀態表🔒列+[[reference_remote_control_relaunch_blocked_mystery_2026-09-19]]完整排除清單。
2. 沿用v218/v219既有待辦：孔大哥/佩佩老師industry-chain-sop hook真人實測(教練不催)、peipei-ai-backup舊commit金鑰歷史(教練已表態不處理)、`stop_rules_master.py`規則#07誤判regex(教練示意MiniMax有空自行補丁)。
3. 💬試金石案例庫商業化討論——教練指定的軍師專屬討論題目，本場再度沒空展開（連續第二場被其他緊急事項擠掉），下一場優先主動提起。
4. E16接力棒瘦身：本場v217已封存，主檔現為v218~v220共3棒，下次開工建議把v218搬進archive維持2棒上限。

## 🔑 本場commit
`workspace`：`425e87794`(接力棒10/3狀態表更正+教訓記憶)、`552232f24`(接力棒瘦身236KB→78KB+handoff_sync_guard.sh新建)。本次收工commit另計，含v220接力棒本身+Remote Control排除清單記憶檔。
