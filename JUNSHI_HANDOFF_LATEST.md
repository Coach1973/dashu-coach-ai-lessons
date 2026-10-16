## 🔴 給跨對話框軍師讀的總結摘要（2026-10-17 02:42 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Opus 5.5→Sonnet 5.5；教練說「回答完我這個問題之後就可以總結了」；本段 02:04～02:42，對話容量約 27～30%（get_usage 27%、hook 估 30%），Pro 5 小時額度 97%（04:20 重置））

**主軸：教練交辦「把特助守則 21 條納入賈維斯」→ 研究完成、教練選定方案、已動手一半；5 小時額度用到 97% 而中斷，審查員等新對話做。**
- **研究報告**（`ad1b887ca`）：`knowledges/守則納入賈維斯_研究與方案_2026-10-17.md`。查到 5 個原因：①守則提醒看教練說的字、不看 AI 行為；②143 條反射只有 11 條標守則編號；③違規最多的 #03／#15／#18 是判斷類、關鍵字抓不到；④守則淹在 732 行／6 萬字背景裡；⑤`periodic_xinfa_reload_hook.sh` 寫死對話資料夾，「開工」worktree 對話從沒重貼過守則（已修，實測舊版 0 字、新版貼出 21 條）。
- **Haiku 審查員實測**：拿上一場真實對話，4 個真錯抓到 3 個（沒裝 Discord、Copilot 沒先問、「登出會全清掉」），漏 1 個（手機遙控預測）；每次 12～20 秒、牌價每次 US$0.0014～0.0045；會漏、會邊界誤抓 → 先「只記錄 3 天」。教練 02:25 選「照推薦做（B 審查員＋修重貼漏洞＋看提醒次數）」，授權終端機改正式檔案（改前備份：`state/backup_2026-10-17_rules_reviewer/`）。
- **教練 02:26 新要求：規則自動體檢**（過時／重複／沒必要，精簡加精準，越用越好用，將來可商業化）。查到教練問過至少 6 次（8/9、9/19 三次、10/1、10/14），之前的檢查都只查「有沒有載入」、從沒量「有沒有照做」。初步設計在交辦檔。
- **案例128**（`b0702cea7`）：問教練要不要總結卻沒附對話容量 % → 反射 R-ASK-SUMMARY-WITH-CONTEXT-PCT 擋下；`reflex_router.py` 回話檢查原本讀不到收尾框，已補（實測 3 種情況正確）。
- **容量與額度怎麼讀（教練 02:40 問，已答）**：容量 % 由 `context_percent_hook.py` 在本機讀對話檔算，不花模型 token，只有出聲時（跨 30/35/40/45/50% 與每 5 句）各約 100 token 進對話；`get_usage` 是工具呼叫＝多一趟來回（整段對話再讀一次快取）＋結果數百 token，佔額度多少 % 沒量到。**5 小時額度 % 只有 get_usage 看得到**（hook 看不到；有沒有本機來源沒查）。兩個容量來源差 3%（hook 30%／get_usage 27%，切 Sonnet 後），原因沒查。
- **教練原話線索**：「我雖然在意額度，但面對精準、高效率的工作，我寧可多花一點額度，因為我已經 53 歲了，沒有那麼多體力每天熬夜在那邊等待、抓錯」「改三次以上的額度比做對一次還要更多」→ 判斷標準＝一次做對優於單次省額度；「那之前都幹嘛去了？」→ 主動體檢，不等教練問；「我們是越來越有默契」。

### 📋 下一場開工先做（以本棒為準）
1. **🎯 先 Read `knowledges/TASK_守則審查員與規則體檢_接續_2026-10-17.md` 照做**：①`scripts/rules_reviewer_hook.py`（Stop，async，只記錄 3 天，壞了放行）②`rules_reminder_count.py` 教練提醒次數＋接進開工注入 ③規則自動體檢先提設計。Sonnet 5.5 就能做；5 小時額度 04:20 後重置。
2. **🔧 容量回報（教練 02:40 答案：查容量不貴就頻繁報）**：`context_percent_hook.py` 過 30% 後改成每句都報（現在每 5 句；`CONTEXT_REPORT_EVERY`），問總結時附額度 %（get_usage 只在問總結那一句查一次）；順便查 hook 30% 與 get_usage 27% 為何差 3%。
3. 🔧 `session_length_hook.sh` 也寫死對話資料夾（與守則無關，沒動）。
4. 承接舊清單：軍火庫設計稿 https://claude.ai/artifact/VvLFrV8He1qA3fnScPTSm3 教練回應後照做；志工頁有人加入後改 `volunteer.html` 的 `JOINED`；gateway `providers.nvidia.models[17].input` 設定驗證錯誤；新 LINE 群歡迎詞沒送出原因；策展 GitHub 化收尾；聯想 `/api/mytools/state` 放行 8765 建議拿掉；worktree 分支 `claude/kaigong-424fd5` 兩個 commit 要不要搬進 master；`namecard-db/namecards.db.backup-…20260712` 含個資只留本機；angel-sister 頁 10.6MB 可考慮壓；`ai.hermes.desktop.plist` 沒有登入啟動條件（未處理）；看「先查再答」E2 有沒有誤擋（`grep -A2 "E2 判斷題零查證" distill/rule03_verify_violations.log`）；修憑證層「Claude（主力 UNLIMITED）」過時（aiprimetech 金鑰 401）。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：（沿用上一棒 🤫 清單，見本檔下一棒；N3 兩段順序打架、Discord 後續、香檳下午茶 4 點等）。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-17 02:05 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5；教練說要登出再登入，順手收工；本段 00:53～02:05，對話容量約 50%）

**主軸：教練要弄懂 Discord 對工作的用處、跟 LINE 差在哪、App／網頁與記憶體；查證後把「榮樹下」伺服器頻道開通（教練 01:19 實測有回）。我講錯一次（「這台沒裝 Discord App」，其實是指令報錯被我當成查不到），已更正並加防呆。收工前健康檢查 🟢 全部正常。**
- **Discord vs LINE 查證**（教練原話：朋友說高手都用 Discord、比 LINE 好太多）：結論＝不搬家、分工——LINE 對外（夥伴／學員／預約），Discord 當教練＋小龍蝦＋助理的內部工作台。查到：頻道分主題不洗版（TVBS 2026/8/26）；LINE 照片約 30 天、文件 7 天過期（報導，LINE 官方沒明確公布）；Discord 免費單檔 20MB（Dexerto 2026/8/13）→訪談錄音原檔不走 Discord；LINE 官方帳號免費推播 200 則／月（第三方整理）、LINE Notify 2025/3/31 已終止；小龍蝦官方文件有 Discord 語音逐字稿＋自動會議記錄（要設語音轉文字、先告知與會者、摘要不自動貼回；本機 2026.9.4 有、設定檔未開）。「談完自動上 Podcast／YouTube」目前沒現成路：YouTube API 未審核專案上傳會被鎖私人、SoundOn 沒查到公開上傳功能、路徑大全沒 YouTube 授權；網頁上架技能已有（換入口而已，Discord 內未實測）。教練說 Discord 語音不如 Typeless → 語音頻道不用，實測「之後我再說」。
- **榮樹下頻道開通**（`46900b190`，~/.openclaw master）：原因＝`channels.discord.groupPolicy` 是 `disabled` 且無 `guilds`（只開私訊）；改 `allowlist`＋`guilds["1560663537527820298"]={requireMention:false, users:[教練ID]}`，dry-run→套用→重啟 gateway（CLI 與服務同為 2026.9.4）。伺服器只有教練＋機器人，新頻道自動生效；**只限 MiniMax 版**，切 Claude 版時伺服器頻道未設定。已給教練白話三步驟（頻道打字即回、私訊也行、新頻道不用再加）。
- **錯誤更正**（試金石126、反射 R-ERROR-IS-NOT-NOT-FOUND，`2b5caefb2`）：`ls -d /Applications/Discord* ~/Applications/Discord*` 第二路徑沒東西，zsh 報 `no matches found` 整行中止，我當成「沒裝」並標【查到】；教練：「我有裝，而且正開著呢」。實際 `/Applications/Discord.app` 存在。同類「否定結論沒驗證查法」第二次（記憶 reference_windows_file_scan_silent_zero_traps 只寫記憶）→ 這次進機制，回測 291／45,234。
- **Discord App 與記憶體**：「App 比網頁省記憶體」查不到根據（App 是 Electron／Chromium、無並排實測）；App 開 45 秒實際佔用約 500MB（RSS 加總 920MB 偏高）；網頁版沒量。Mac mini 16GB，系統可用比例約 55%、交換檔 135MB，壓力正常；教練活動監視器的數字（用量 12.92GB、快取 3.08、核心 2.35、壓縮 3.89）與我量的吻合，要看的是「記憶體壓力」圖與交換檔，不是用量。已驗證 computer-use 能控制 Discord App（full，讀到畫面與 113 個元素；沒點擊／打字），建議機器人 API 即可。
- **登出前查證（01:46 被教練抓到自相矛盾，已更正）**：38 個自動服務設定檔都在、都已載入沒錯；但我說「登出後 tmux `remote-control` 會消失、登入後要重開」是沒查證的推論、**錯的**——查到 `last` 顯示教練 10/16 08:44 登出、08:45 登入，而 tmux `remote-control`（10/3 10:30 起）與 `claude rc` 一路活到現在（7 個手機舊對話約 1.1GB，最舊 13 天），登出不會清掉它們，原因沒查到。要清只能明確重開 `bash scripts/restart_remote_control.sh`（會結束手機上那些對話，只有教練知道哪些要留，已問一次、等回）。
- **手機遙控重開失敗（01:51，我的疏忽）**：教練同意後我跑 `restart_remote_control.sh`，舊 `claude rc` 與 7 個手機舊對話已清掉（教練活動監視器記憶體用量 12.92→10.83GB），但新的 `claude rc` 報「You must be logged in」：鑰匙圈 `Claude Code-credentials` 的 accessToken／refreshToken 長度 0、expiresAt＝0（01:38:20 被清空；refreshTokenExpiresAt 10/16 23:04 已過），`claude auth status`（四個版本都是）loggedIn:false，Chrome 的 claude.ai 也是登出狀態（登入頁網址帶 from=logout）。舊 rc 能活 13 天是靠記憶體裡的令牌。**我重開前沒先驗證「新的能登入」**→ 教訓：重開長壽的已登入程序前，先跑 `claude auth status` 確認新實例登得上。**01:57 已修好**：教練登入 Claude 帳號、把授權驗證碼貼進終端機（驗證碼我不代輸入）→ `claude auth status` loggedIn:true（claude.ai／pro，憑證到 10/17 09:56 為 access token 期限、refresh token 在）→ 我 `tmux kill-server` 後用「拔掉 CLAUDE_*／ANTHROPIC_* 環境變數」重跑 `restart_remote_control.sh`（避免桌面版的環境變數混進手機對話）→ 看到 `Connected · mac-openclaw-workflows · master`、Capacity 0/32、舊對話程序 0 個；Chrome 的 claude.ai/code 也列出 `mac-openclaw-workflows · wudashudeMac-mini` 環境。手機端「真的看到」只有教練手機能確認（我驗不到）。**注意：下次 `claude rc` 重開若再報「必須登入」，先 `claude auth status`；refresh token 會過期，約兩週要重登一次。**
- **Plaud 已關**（教練 01:46：「Plaud 我確實不常用，我要用的時候再打開就可以了」）：用 `claude mcp remove plaud -s user` 從 `~/.claude.json` 移除，並結束 14 個 Plaud 小程式（約 380MB）；要用再裝回（無金鑰）：`claude mcp add plaud -s user -- ~/.hermes/node/bin/npx -y @plaud-ai/mcp@latest`。REA 教練沒回，仍在。
- **陌生詞先問（教練 01:37 親口要求，試金石127）**：教練問「Copilot 覆蓋率」（語音錯誤），我沒先問就去查；教練要我寫進檢查清單。已做：反射 R-UNFAMILIAR-TERM（reflex_router `unfamiliar_terms`，教練話裡出現歷史上沒用過的英文詞→提醒「先問是不是語音輸入錯誤、不先查」，同詞只提醒一次，回測短句 6% 會跳）＋執行合約加一行＋skill 改成先問再查。限制：中文陌生詞程式抓不到。
- **手機遙控收尾＋容量與收工口令（02:01～02:03 教練糾正）**：手機遙控已修好驗證（`c26e9369a`，細節見上一條）。教練抓到我過了 30% 還繼續加做事（31%→48%、約 17 萬 token 白燒），已在容量提醒加一句「過 30% 只做教練明說的事、不順手加工作、做完主動問要不要總結」（`abc426348`）。教練再問「你總結了嗎？」→ 定下**口令默契：只有我說「總結已完成（commit hash）」才代表總結好了；沒總結完不准說「可以開新的對話框」**（已寫進 junshi-shutdown-summary 技能第 6 步，兩份）。TGONDeviceInferenceProviderService＝Apple 系統程式（`com.apple.tgondeviceinferenceproviderservice`，5MB，不用管）。
- **教練原話線索**：「你怎麼可以在沒有查證的時候就說沒裝這件事呢？」→案例125／126 一線：否定結論前先驗證查法（三大信念一「真誠：說真話，辦真事，一切歸於真實。」）。「我要的是在不同的頻道當中它都可以發揮作用，不是嗎？」「有沒有很簡單、很簡單的使用說明書」→ 要的是「任何頻道叫得動小龍蝦」＋白話說明。「我不想刪了之後到時候又重裝，先這樣子吧」「我希望這台電腦可以輕鬆完成任務，不要因為記憶體不夠而顯得笨重」→ 取捨偏保留；在意的是「用得順」，數字只是手段。

### 📋 下一場開工先做（以本棒為準）
1. **🎯 教練交辦（10/17 02:25 選定方案）：做「守則審查員」（AI 回話前小模型拿 21 條審一次，先只記錄 3 天）＋「教練親口提醒守則次數」統計；接著設計「規則自動體檢」（過時／重複／沒必要，教練 02:26 新要求）**。研究已完成、重貼漏洞已修（10/17 Opus）。開工先 Read `knowledges/TASK_守則審查員與規則體檢_接續_2026-10-17.md`（步驟、驗收、教練原話、授權）。Sonnet 5.5 就能做；中斷原因是 5 小時額度 91%（04:20 重置）。
2. **手機遙控已修好（見上）**：只需在下次開工 `tmux ls` 看 `remote-control` 還在、`claude auth status` 仍 loggedIn:true；另看 `~/Library/Logs/openclaw/launchagents_guard.log` 有沒有登入時那筆、跑 `python3 scripts/system_health_check.py`。
3. 🔧 承接（19:45 棒清單已併入此處）：軍火庫設計稿 https://claude.ai/artifact/VvLFrV8He1qA3fnScPTSm3 教練回應後照做；志工頁有人加入後改 `volunteer.html` 的 `JOINED`；gateway 啟動的 `providers.nvidia.models[17].input` 設定驗證錯誤；新 LINE 群歡迎詞沒送出原因；策展 GitHub 化收尾；聯想 `/api/mytools/state` 放行 8765 建議拿掉；worktree 分支 `claude/kaigong-424fd5` 兩個 commit 要不要搬進 master；52 筆舊 stash 留在清單（內容已封存）；`namecard-db/namecards.db.backup-…20260712` 含個資只留本機；`memory/` 有 2 個記憶檔放錯位置（應在 claude-brain/）；angel-sister 頁 10.6MB 可考慮壓；`ai.hermes.desktop.plist` 沒有登入啟動條件（可能本來手動，未處理）。
4. 🔧 看「先查再答」E2 有沒有誤擋：`grep -A2 "E2 判斷題零查證" distill/rule03_verify_violations.log`；修憑證層「Claude（主力 UNLIMITED）」過時（aiprimetech 金鑰 401）。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：執行細則 N3 第一段「陌生檔名／術語：先搜尋驗證」與第二段「陌生詞主動問」順序打架（教練欽定原文，我沒改，我照第一段先查了；要不要改成先問再查）；Discord 語音頻道自動會議記錄實測（教練「先不用實測，之後我再說」）；Claude 版的伺服器頻道、朋友加入伺服器時改 `users`／`requireMention`；Discord Claude「說新對話就自動重開」、開機自動啟動；後台應用程式名稱改成龍蝦特助；Claude 線（aiprimetech）新金鑰；香檳下午茶頁 4 點確認（戰績只用原頁、理事長林家旭查無資料、照片人物依檔名推斷、類別被分成「食」）；social-club 頁尾寫「TAVA AI 設計」不是「製作」；吳錦昌沒有個人頁；預約頁「只開固定時段」；南應大 /tut/team 要不要加入口；真貴 5 位要不要從真鑽拿掉；Podcast 快取改 1 分鐘；TAVA 備份頁放哪一類；GitHub 404 三個（joseph-cloth／social-good 私有倉庫不能開 Pages、Business.gym 沒有倉庫，event 上的版本正常）。

---

> 📦 10/17 00:50 棒（Discord 兩種腦、先查再答、教練原話線索）已封存：`handoff_archive/handoff_2026-10-17_0050_Discord先查再答_archived.md`

> 📦 10/16 19:45 棒（workspace 被拉錯分支事件、守門員與技能、盤查救回）已封存：`handoff_archive/handoff_2026-10-16_1945_軍師棒_archived.md`（待辦清單已併入新一棒）

> 📦 10/16 23:55 棒（Discord 建置過程、被糾正的兩個低級錯、金鑰防護、教練原話線索）已封存：`handoff_archive/handoff_2026-10-16_2355_Discord建置_archived.md`

> 📦 10/16 15:10 追加棒（網站斷線通知、香檳下午茶頁上架）已封存：`handoff_archive/handoff_2026-10-16_1510_香檳下午茶追加_archived.md`

> 📦 10/16 01:55 聯想 v259 棒已封存：`handoff_archive/handoff_2026-10-16_0155_聯想v259_archived.md`

> 📦 10/16 02:10 棒、13:06 棒已封存：`handoff_archive/handoff_2026-10-16_0210_1306_網站斷線守門員_archived.md`

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
