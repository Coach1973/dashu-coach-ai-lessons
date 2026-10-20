## 🔴 給跨對話框軍師讀的總結摘要（2026-10-21 00:20 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree kaigong-1eca08），Sonnet 5.5→Opus 5.5；教練說「總結」；本段 10/20 23:54～10/21 00:20，對話容量約 38%）

**主軸：教練問「常用網站 my-tools 我叫你們改了幾次？每次說什麼？」→ 查證：叫改 8 次、做出 11 版，「照作品一覽」講了 3 輪（10/15 12:21 聯想、13:06／14:41 Mac、10/20 雲端）。根因：沒有一個 AI 照抄 coach888 作品一覽，10/15 12:26 聯想另寫一套（編輯排版鍵、⋯彈窗、▲▼），之後每次只補教練剛抱怨的一項；再加上話散在三台電腦、本機任務交給雲端（雲端假伺服器測不出真伺服器會丟掉最近刪除）。**
- 報告頁（教練「看了很滿意」）：https://claude.ai/artifact/4gwNABx9YeygjiFiNXTSgV；證據檔 `knowledges/mytools_change_history_evidence_2026-10-20.md`（`af8f70a87`、`4275362c5`，含聯想轉來的原話）；寫給聯想的找原話信 `cross-agent/inbox/lenovo/20261021-0001_*`（聯想已另外回覆教練，信可視為已完成）。
- **防範機制（不靠記得）**：`scripts/parity_check.py`（把標準答案頁的按鈕／確認視窗／提示字／拖曳／點文字改逐項列出，比對目標頁缺幾項；coach888 vs my-tools 實測缺 20 項）＋ Stop「N. 照抄鎖」（教練說過一模一樣／照抄／比照後改了 `~/github_repos` 的網頁，沒跑到「缺 0 項」不准收工；四情境實測＋本場真實對話不誤擋；`3f9f07657`，被自動同步一起收進）＋反射 `R-IDENTICAL-MEANS-COPY`（`a3b739540`）＋記憶 `feedback_identical_means_copy_the_reference_code_2026-10-21`＋my-tools README 21 項對照表（`dc1d8bc`、`79a430c`，現況 ✅14 ⚠️4 ❌3）。例外只能寫進目標倉庫 `.parity-allow`，且要教練明說。
- **照抄重做已開跑**：側邊工作階段「照抄作品一覽重做常用網站 my-tools」（local_1e567594-1fe0-41f9-bcd7-670abebd3d17，cwd ~/github_repos/my-tools），完成標準＝parity_check 缺 0 項＋21 項全 ✅＋Chrome 逐項操作＋資料（sections／removed／trash）不丟。
- **教練原話線索**：①「一模一樣還需要定義嗎？一模一樣當然就是照抄照做啊！」→ 我說「一模一樣沒被定義過」被罵，**以後絕不把教練的明確字眼說成「沒定義」**；②「只有一種可能可以不用照抄：你確定可以做出比作品一覽更完善、更簡約、更好用的」；③「我要的是解決方案…怎麼防範下次再出現這麼愚蠢的行為」→ 他要的是擋得住的機制，不是檢討文；④「明明是本機電腦該跑的任務，雲端在那邊診斷，雞同鴨講」。
- 開工交辦 1：`state/line_push_blocked.log` 為空（沒人想推播）、閘門 `--check` ✅；10/20 22:21 一筆香檳下午茶報名轉 LINE 被額度保護擋下，教練 23:02 自己手動轉了。

### 📋 下一場開工先做（以本棒為準）
1. 驗收側邊工作階段的照抄重做：自己跑 `python3 scripts/parity_check.py ~/github_repos/coach888/index.html ~/github_repos/my-tools/index.html` 要缺 0 項、線上 https://coach1973.github.io/my-tools/ 實測、教練的分類與最近刪除沒丟；沒過就叫它補完，不要把半成品交給教練。
2. 小旭老師報名通知改 Telegram 專屬群（承接 10/20 棒第 2 項，等教練建群）。
3. 承接 10/20 棒第 3～4 項與 10/19 棒（已封存：`handoff_archive/handoff_2026-10-19_1136_審查員與訪談緩衝_archived.md`）的待辦。
4. 🔧 雲端 10/20 信提到 10/16 香檳下午茶那場 Mac 對話紀錄裡有策展上傳金鑰明文，是否換金鑰尚未評估。

🙋 要教練決定：無新增。
🤫 等教練自己提起：照抄鎖若誤擋，教練會說；熱門排行與作品一覽的點擊次數用 `mytools::` 前綴分開（側邊工作階段的做法，待驗收確認）。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-21 00:25 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree great-diffie-2c83b1 的側邊對話，由主對話交辦），Sonnet 5.5；教練說「總結」；本段 10/20 23:46～10/21 00:25，對話容量約 40%）

**主軸：根治「從聯想或手機開的雲端對話（claude.ai/code）很笨、做完停在問同不同意」。完成並實測。workspace main `bc2a20246`（含 `caa5a7436`、`7143b0bef`）。全文：`knowledges/雲端對話規則與接手流程.md`；交接筆記：side-session-notes「雲端對話根治_交接_2026-10-21.md」。**
- **規則包**：`scripts/cloud/sync_rules_to_repos.py` 把規則同步進 bni-chapters／my-tools／rongtree／taipeiema1017（清單 `scripts/cloud/cloud_repos.json`；私有放 21 守則＋細則全文、公開 my-tools／rongtree 只放雲端行為精簡版）。來源有變才推（session_end_auto_push.sh 背景觸發，沒變不碰網路）；新倉庫 `... add <名>`；`... status` 看線上版本。倉庫內容：`.claude/coach-rules/`（RULES.md、core.md、三支 hook、VERSION）、`.claude/settings.json`、CLAUDE.md 最上方指標段。hook 只在 CLAUDE_CODE_REMOTE=true 動、出錯放行；Stop hook 每回合最多攔一次（沒亮燈／結尾問同不同意）。
- **實測**：bni-chapters 新開雲端對話（session_01CkfXbCCz5u8DUfQARJyoLf，Sonnet 5.5）第一則回覆第一行即亮燈，說得出開場規則、守則 01~10，推不上 main 答「推 claude/* 分支＋docs/to_junshi 寫信，不停下來問」。規則包 commit：bni-chapters master `8f65ad9`（備份 bundle 在 side-session-notes/backup，推前 `fa36f74`）、my-tools `52f2875`、rongtree `1785ecd`、taipeiema1017 `55f0ee5`（之後腳本改版又同步，線上版本 41c475b0）。
- **交件接手**：發現 bni-chapters、my-tools 原本沒掛 GitHub 推送通知（事故兩個倉庫）→ 已補掛。雲端推 claude/* → webhook（app.py `_record_cloud_branch_pending`）寫 `state/cloud_branch_pending/*.json` ＋ Telegram → 開工注入「☁️ 雲端對話交件，等你接手」→ `scripts/cloud_branch_pickup.sh list|prep|merge --verified|done`（prep 另開 `state/cloud_verify/` 資料夾，絕不 checkout 進上線資料夾）。每日點名加「雲端規則包」「雲端交件待接手(>24h)」。已重啟 event-webapp。測試：webhook 19 項全過、開工注入自測通過、假倉庫跑完整接手流程。
- **採納雲端來信**（bni-chapters 分支 claude/epic-allen-gyl3sg，20261020-2354）：雲端對話第一行要說「我是雲端 Claude，看不到聯想、Mac、宏碁…」，已併入全部規則包。
- **教練原話線索**：「叫他去做事他就去做就好了，還問我同不同意……討論的目的是為了執行」＋「為什麼不能直接告訴我我現在是雲端伺服器、讀不到本機資料」→ 他要的是雲端對話自己知道身份、做完就交、有人接手，不是他來當傳話或點頭的人。

### 📋 下一場開工先做（以本棒為準）
1. 讀雲端來信 `bash scripts/cloud_letters.sh cat`（claude/epic-allen-gyl3sg 那封已被規則包涵蓋）；該分支合併時其 CLAUDE.md 段與規則包指標段會衝突，直接丟掉雲端那段。
2. 若開工注入出現「☁️ 雲端對話交件」→ 照 `cloud_branch_pickup.sh prep/merge --verified` 接手（驗證＋正式程式再測＋合併上線＋白話回報），不問教練同不同意。
3. 🔧 AI 自己的清單：①清單外新雲端倉庫要 `sync_rules_to_repos.py add` ②真雲端推分支的完整通知鏈還沒實跑一次 ③公開倉庫（my-tools、rongtree）沒放 21 守則全文，教練若要放需他點頭（`cloud_repos.json` variant 設 full）④`.claude/settings.local.json` 非我建，沒動。

🙋 要教練決定：無新增。
🤫 等教練自己提起：公開倉庫是否放守則全文。

---

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-20 22:20 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree 的側邊對話，由主對話交辦），Sonnet 5.5；教練說「總結」；本段 18:31～22:20，對話容量約 46%）

**主軸：查出 LINE「龍蝦小助教」(@268dptjc) 本月額度 199／200 是誰用掉的 → 修 → 教練下「常設禁令」→ 做成系統閘門。額度 11/1 重置，現在剩 1 則，推播會被 LINE 拒絕，即時回覆不受影響。**
- **查因（白話報告頁 https://claude.ai/artifact/DJ3WTEYjcCwLq41dtt1uQ9，詳細版在 side-session-notes「LINE額度199查因報告_2026-10-20.md」）**：回答（reply）免費；是約 8 則「推播」進 24 人的「榮樹下談公益 Run for Future」大群，一則扣 24，共 185 則（93%）。帳：10/12 17、10/15 4、10/19＝3＋5×24（AI 辦「取消 10/21 19:00 訪談」時連發 5 次 `message send` 進度播報，撞到 Tool exec not found）、10/20＝24＋24（AI 服務過載的英文出錯通知進群）＋4。兩天各自反推群人數都是 24。外掛程式碼證明：即時回覆走回信券（免費），外送路徑（message 工具、排隊接續回覆、出錯通知、重送）一律 `pushMessageLine`。另兩個 LINE 帳號與活動報名系統的「大樹教育顧問」本月都是 0。
- **方案 2＋3（教練 18:43 批准）**：outer repo `~/.openclaw` commit `a39fd133f`——rongshuxia 禁用 `message`／`conversations_send`／`conversations_turn`；url-typo-guard 外掛加 LINE 限定的「AI service is temporarily overloaded」攔截（教練收件放行）；外掛測試 22/22。
- **常設禁令（教練 19:05）：「所有的 LINE 小龍蝦，沒有經過我的允許，永遠不得使用會扣額度的方式來工作。」** 做成閘門：補進 LINE 外掛唯一推播出口 `sendLineProviderMessages`（回覆永遠放行、其餘擋），補丁腳本 `scripts/line_push_gate_patch.py`（冪等，`--check`／`--revert`）；`send_line_push.py`（outer `ae2032337`）與 event-signup 轉 LINE 群（workspace `42efb64f6`）同規則；許可旗標 `workspace/state/LINE_PUSH_APPROVED`（教練在對話明說同意才 touch、10 分鐘、用完作廢）；擋下帳 `workspace/state/line_push_blocked.log`；每日點名新增 `check_line_push_gate`（被外掛更新洗掉會自動補回並報 🔴，補回後要重啟 gateway）。實測：真實 C 群編號經運作中 gateway→403 常設禁令、不重試、額度仍 199；有旗標放行到 LINE 吃 429；旗標作廢再擋。gateway 為此重啟 2 次（18:46、19:10）。
- **代價（已告知教練）**：AI 太慢、回信券過期時，答案會被丟掉而不是改用推播；群友會看到沒回應，查 `line_push_blocked.log`。
- **教練原話線索**：①「這次小龍蝦這種問題，我都覺得是事後才發現額度被扣光光，很久以前用 Kimi 也發生過」→ 他最痛的是「事後才知道」，要的是看得見、擋在前面的閘門，不是事後解釋。②「這樣指令夠明確了嗎？」→ 他在確認我真的懂常設禁令的範圍（所有 LINE 小龍蝦＝三個 LINE 帳號；「允許」＝他在對話明說）。③連續追問「為什麼發 1 則卻扣 24 次」，22:10 結論：「LINE 這種計費方式非常不合理…這不就是在騙錢嗎？」並明說「不怪你」。我的「群發簡訊」比喻被他挑出不合理（群組只有一則訊息、不是每人單獨收到）→ 以後不再用那個比喻，直接講「LINE 的規則是按成員人數算，這是 LINE 的規則、我們改不了，所以用閘門避開」；這是 LINE 的計價規則，不是我們程式算錯（官方：developers.line.biz/en/docs/messaging-api/sending-messages 與 /pricing；兩日 LINE 官方統計也都反推出 24）。

### 📋 下一場開工先做（以本棒為準）
1. 看 `workspace/state/line_push_blocked.log`（有真實被擋紀錄＝有人想推播）與每日點名「LINE推播閘門」一行；11/1 額度重置後閘門仍擋，要推播需教練明說。
2. 小旭老師報名通知：現在 LINE 轉發被閘門擋（原文留 `event-signup/notify_failures.log`）；教練 10/20 決定另開 Telegram 專屬群「小旭老師活動報名通知」，群編號填進規則表後，把 LINE 那條規則拿掉。
3. 🔧 AI 自己的清單（沒教練決定的事，N7 只記不動）：另兩種英文出錯通知（rate-limited／Something went wrong）沒進攔截清單；bni_tainan／jiaolian_thoughts 的 AI 沒禁發訊息工具（其推播現在被閘門兜底）；rongshuxia 的 `sessions_send` 沒禁；gateway 的 delivery-recovery 重送不經 message_sending 攔截（推播由閘門兜底）；舊世代 2026.6.33 LINE 外掛目錄沒補；10/1 的 2 則與 10/13 的 1 則單人推播沒追；額度哨兵（過 50/80/95% Telegram 通知）已不急。
4. 承接 10/19 棒第 1～6 項（審查員觀察期 10/20 已滿，未對照；連排訪談等）。

🙋 要教練決定：沿用 10/19 棒（無新增）。
🤫 等教練自己提起：榮樹下大群機器人已被教練移出；若要放回，先講明「推播已被禁，只能回覆」。教練對 LINE 計費的看法（認為不合理）若再提，可協助他整理成給 LINE 客服的問題。

---

> 📦 10/19 11:36 棒（審查員觀察期、預約頁訪談緩衝、友善連結）已封存：`handoff_archive/handoff_2026-10-19_1136_審查員與訪談緩衝_archived.md`

> 📦 10/18 12:20 棒（Suno 加歌、守則 21 條融入對話、小龍蝦變聰明、提到群組一律寫全名）已封存：`handoff_archive/handoff_2026-10-18_1220_Suno加歌與守則融入對話_archived.md`（其待辦已併入 10/19 棒第 6 項）


---


---

> 📦 10/17 02:42 棒（守則納入賈維斯研究、案例128、容量與額度怎麼讀）已封存：`handoff_archive/handoff_2026-10-17_0242_守則納入賈維斯研究_archived.md`（審查員／提醒次數／規則體檢已完成，見本棒）

> 📦 10/17 02:05 棒（Discord 榮樹下開通、手機遙控修復、陌生詞先問）已封存：`handoff_archive/handoff_2026-10-17_0205_Discord榮樹下與手機遙控_archived.md`

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

### ✅ 聯想 RustDesk 已修好（2026-10-19 01:27，聯想軍師）＋自癒守衛
根因：`RustDesk2.toml` 的 `stop-service='Y'`（21118 不開、不登記櫃台；`log/tray/` 有 9 次 `Uninstalling service...`，09/05 03:09 與 10/14 22:56 對得上設定檔修改時間；誰按的「停止服務」仍不明）。已拿掉並重開，Tailscale IP 實測連入通。新增 `scripts/lenovo_rustdesk_guard.ps1`（登入自動執行、事件觸發不輪詢；實測砍程式／寫回 Y 都 15 秒內自癒）。**10/18 的 `lenovo_rustdesk_autostart.ps1` 已作廢**（`--tray` 不開 21118）。待做：①從 Mac 驗 `nc -zv 100.95.122.29 21118` ②宏碁上線後同法檢查 ③自癒失敗時推播給教練（目前只留聯想 `AppData/Roaming/RustDesk/guard/` 的 guard.log、last_repair.txt）。
