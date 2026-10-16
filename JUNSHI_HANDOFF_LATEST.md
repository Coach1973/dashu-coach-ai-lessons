## 🔴 給跨對話框軍師讀的總結摘要（2026-10-17 00:20 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5；教練說「開」，一路做到 Discord 切成真的 Claude；本段 23:51～00:20，對話容量約 25%）

**主軸：Discord 機器人「龍蝦特助」現在接的是真的 Claude（教練 00:10 實測「Discord 有回了，確實是 Claude」）。前一場「Anthropic 旗標對教練帳號關著」只是從程式預設值＋兩次失敗推論，沒讀本機實際旗標值；現在實測可用（試金石125）。我翻案時又把話說過頭（說「前一場說錯了」），已更正。教練 00:18 嚴正指出「先答、答錯、再推翻自己」是長期毛病，要一套回答前先查證的標準。**
- **過程**：先照上一棒接小龍蝦（OpenClaw 加 Discord，金鑰不進 git、用 SecretRef 指到 `~/.claude/channels/discord/openclaw-secrets.json`，`plugins.allow` 要補 `discord` 否則一直 stopped；`d9d8e2c92`）→教練 23:59 測有回（MiniMax）→教練追問「為什麼朋友可以我不可以」→查本機：`cachedGrowthBookFeatures.tengu_harbor=true`、核准清單含 discord、帳號個人 Pro、乾淨環境實測 `Channels: Listening` →教練 00:08 授權切換。
- **現況**：小龍蝦的 Discord 暫停（`channels.discord.enabled:false`，`c1427db72`），備援；真的 Claude 在 tmux 視窗 `discord-claude` 常駐，工作資料夾 `~/claude-discord`（`CLAUDE.md`、預先核准 5 個 Discord 工具），Claude Code 首次啟動自動升到 2.1.301，模型 Sonnet 5。權限提示會傳到教練 Discord 私訊按按鈕。啟動／檢查／退回指令全在記憶 `project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16`。
- **改名**：教練 00:02 指定機器人叫「龍蝦特助」，用機器人金鑰改好；開發者後台的應用程式名稱仍叫「Claude特助」。
- **容量（教練 00:12 問「日後叫它做事會有 context 問題吧？算法跟這邊像嗎？」）**：同一套算法（同一份 settings.json，視窗 100 萬）；Discord 視窗是一個持續的對話，剛開機就 8%（75.1k，固定開銷約 55k）；全域 hook 在 Discord 訊息也會觸發（交易紀錄確認），容量提醒理應也會到。沒有「新對話」按鈕，目前重啟 tmux 視窗。
- **其他**：Hook 稽核紅字查到是 `scripts/context_percent_hook.sh`（舊版，現行是 `.py`），已拿掉檔頭「# Hook：」宣告。每個桌面版對話都會多一個閒置的 Discord 外掛程序（外掛是 user scope），無害。
- **教練原話線索**：「我的朋友說他可以，我就納悶，為什麼他可以我不可以？你還是沒有解決我這個問題，對嗎？」→教練不接受「帳號被擋」的推論，要證據；別人能做、他不能，一定要追到底。「它也會有對話上下文視窗…我就比較想了解它那邊計算的方式」→教練在意長期用 Discord Claude 的容量管理，習慣 30% 準備、40% 開新對話。「為什麼你都不能說「我先去了解一下真實情況」，不要著急回答我吧？」「這種反反覆覆，你不覺得很煩嗎？」「我先說，不是今天晚上而已，之前也多次發生過這種情況。」→ 三大信念一「真誠：說真話，辦真事，一切歸於真實。」原因／判斷題先查第一手證據再答，話分「查到的／推論／沒查的」，不夠就說「我先去了解」。

### 📋 下一場開工先做（以本棒為準）
1. 看 tmux 視窗還活著：`tmux ls`、`tmux capture-pane -t discord-claude -p`；Discord Claude 的容量接近 30% 時提醒教練。教練若要「在 Discord 說新對話就自動重開」→ 做成重啟腳本（目前只有手動指令，見記憶）。
2. 🔧 Mac 重開機或登出後 Discord Claude 不會自動回來；教練需要時再做開機自動啟動（先把 10/16 的 launchd 事件收尾）。
3. 🔧 修憑證層「Claude（主力 UNLIMITED）」過時（aiprimetech 金鑰 401）：先查有沒有換過金鑰；查不到就放 🤫（只有教練能給新金鑰）。
4. 承接下方 19:45 棒的項目：軍火庫設計稿教練回應後照做、志工頁 `JOINED`、下次登入看 `launchagents_guard.log`、gateway `providers.nvidia.models[17].input` 驗證錯誤等。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：Discord Claude「說新對話就自動重開」、開機自動啟動；開發者後台應用程式名稱改成龍蝦特助；Claude 線（aiprimetech）新金鑰；及下方 19:45 棒的 🤫 清單。

---


## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 19:45 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5→Opus 5.5；教練說「要總結嗎」收工；本段 13:09～19:45，對話容量約 49%）

**主軸：15:00 workspace 被本機另一個 AI 對話框拉錯分支換掉，教練在外面 3.5 小時下不了任何指令、/curated/ 全部 404（重大疏失，試金石123）→ 全部救回並從源頭封住；全面盤查救回 7 月以來 52 筆自動暫存默默弄丟的東西；Claude 新增 7 個技能、小龍蝦新增 2 個技能；背景工作失敗改成當下通知。收工前健康檢查 🟢 全部正常。**
- **兇手與原因**：對話框 960f614e（做香檳下午茶網頁）在 workspace 憑印象寫 `origin master`（workspace 是 main），整個資料夾被換成 ~/.openclaw 的檔；python 檢查程式不見→回 2→教練每句話（含手機）被擋 16 次。9/10 同坑已發生過，當時只寫記憶。還原後 4,172 檔全回（`2538fe817`）。
- **源頭機制**：①8 支 python hook「檔案不在就放行」②`scripts/git_wrong_branch_guard.py`（PreToolUse）：寫錯分支名或指到毫無共同歷史的線就擋並給正確名稱，所有資料夾適用，1,525 筆真實指令回測誤擋 0（`6ef61e757` `aab134d12`）③兩個資料夾都裝 pre-rebase。
- **盤查救回**（`c1eb5ede6`）：5 個整份檔（Plaud主題整理.md 等）、13 條記憶索引、3 份 SOP 段落；遺失行封存 `handoff_archive/stash_rescue_2026-10-16/README.md`；三支自動同步改用 `scripts/safe_stash_restore.py` 逐檔放回。守門員擴大到 38 個自動服務含小龍蝦 gateway（`00886b78d`）；接力棒鏡像格式檢查改查全文（`69d1d3ad6`）；背景排程失敗當下通知 `scripts/cron_fail_notify.sh`（30 分鐘同工作 3 次→電報＋信到 inbox/mac，`de8266088`，daemon 19:22 已重啟）。
- **技能**（`9d6041215` `7502acedf`）：Claude＝健康檢查 system-health-check（`scripts/system_health_check.py`）、總結、改網頁、上架、加上報名、BNI 開票、原話報告書；小龍蝦 main＝site-down-check、bigtree-publish-site（備份 `ops/xiaolongxia_workshop_skills/`）。都實測新對話看得到／答對。報告 https://claude.ai/artifact/GF4ueUwADRQtzeaeQko2JK
- **教練原話線索**：「寫一個指令，寫到我連主人親自下命令都不行，那要你何用？」「憑什麼你們可以憑印象？」「我又不懂電腦」→ 會造成損失的動作一律「系統先查、不符就擋」，不靠 AI 自覺；做得到的事不叫教練點、不叫教練動手。

### 📋 下一場開工先做
1. 教練回應軍火庫設計稿（https://claude.ai/artifact/VvLFrV8He1qA3fnScPTSm3 ）後照做（企劃書 4 件＋雲端另 3 件；點數剩 US$36、週用量預警）；不主動追問。
2. 志工頁有人加入後教練報人數 → 改 `volunteer.html` 的 `JOINED`。
3. 🔧 下次真實登入後看 `~/Library/Logs/openclaw/launchagents_guard.log` 有沒有登入時那筆；跑一次 `system_health_check.py`。
4. 🔧 承接：gateway 啟動的 `providers.nvidia.models[17].input` 設定驗證錯誤；新 LINE 群歡迎詞沒送出原因；策展 GitHub 化收尾；聯想 `/api/mytools/state` 放行 8765 建議拿掉；worktree 分支 `claude/kaigong-424fd5` 兩個 commit 要不要搬進 master；52 筆舊 stash 留在清單（內容已封存）；`namecard-db/namecards.db.backup-…20260712` 含個資只留本機；`memory/` 有 2 個記憶檔放錯位置（應在 claude-brain/）；angel-sister 頁 10.6MB（圖片內嵌），手機慢可考慮壓。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：香檳下午茶頁 4 點確認（戰績只用原頁、理事長林家旭查無資料、照片人物依檔名推斷、類別被分成「食」）；social-club 頁尾寫「TAVA AI 設計」不是「製作」；吳錦昌沒有個人頁；預約頁「只開固定時段」；南應大 /tut/team 要不要加入口；真貴 5 位要不要從真鑽拿掉；Podcast 快取改 1 分鐘；TAVA 備份頁放哪一類；GitHub 404 三個（joseph-cloth／social-good 私有倉庫不能開 Pages、Business.gym 沒有倉庫，event 上的版本正常）。

---

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
