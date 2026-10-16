## 🔴 給跨對話框軍師讀的總結摘要（2026-10-17 00:50 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree），Sonnet 5.5→Opus 5.5；教練說「總結」收工；本段 10/16 23:51～10/17 00:50，對話容量約 42%）

**主軸：Discord 機器人「龍蝦特助」兩種腦都通，平常用 MiniMax 省用量；教練要的「先查再答」標準已接進系統（每次提醒＋回話擋下）。收工前健康檢查 🟢 全部正常。**
- **Discord**：先接小龍蝦（金鑰不進 git，SecretRef 指到 `~/.claude/channels/discord/openclaw-secrets.json`；`plugins.allow` 要補 discord 否則一直 stopped；`d9d8e2c92`）→ 教練追問「為什麼朋友可以我不可以」→ 查本機 `cachedGrowthBookFeatures.tengu_harbor=true`、帳號個人 Pro、乾淨環境實測 Listening → 切真的 Claude（tmux `discord-claude`、資料夾 `~/claude-discord`），00:10 教練實測「確實是 Claude」→ 00:30 教練要省流量，切回 MiniMax（`c482276a2`）。換腦一行：`bash scripts/discord_brain_switch.sh minimax|claude|status`（Telegram／LINE 會斷約 20 秒）。機器人已改名「龍蝦特助」（開發者後台的應用程式名仍叫「Claude特助」）。細節在記憶 project_discord_bot_claude_tezhu_pending_openclaw_2026-10-16。
- **先查再答**（`80b8a1a80`）：反射 R-VERIFY-BEFORE-ANSWER（教練問原因／能不能／是不是／對嗎，每次都提醒；路由新增 `repeat`；歷史回測 4,092 句中 1,073 句觸發）；`stop_rules_master.py` E2（判斷題這輪 0 次查證就下結論→擋下要求補查，記錄在 `distill/rule03_verify_violations.log`）；24 項迴歸全過。極限：有用工具卻仍把推論講成結論，程式抓不到，靠「查到的／推論／沒查的」三分法。試金石125。
- **其他**：「BB＝MiniMax」反射＋語音對照（Claude 與小龍蝦都吃）；Hook 稽核紅字＝舊 `scripts/context_percent_hook.sh`，已拿掉宣告；Discord Claude 視窗容量算法與桌面版相同（開機即 8%，沒有新對話鈕，要重啟 tmux）。
- **教練原話線索**：「為什麼你都不能說「我先去了解一下真實情況」，不要著急回答我吧？」「這種反反覆覆，你不覺得很煩嗎？」「不是今天晚上而已，之前也多次發生過這種情況」→ 判斷題先查第一手證據，話分「查到的／推論／沒查的」，不夠就說「我先去了解」（三大信念一「真誠：說真話，辦真事，一切歸於真實。」）。「我現在還不確定我 Discord 要怎麼用，所以也不想浪費我的流量」→ 平常 MiniMax，要用才切 Claude。

### 📋 下一場開工先做（以本棒為準）
1. 🔧 看「先查再答」E2 有沒有誤擋：`grep -A2 "E2 判斷題零查證" distill/rule03_verify_violations.log`；誤擋就改反射索引 R-VERIFY-BEFORE-ANSWER 的 match（E2 讀同一條）。
2. 🔧 修憑證層「Claude（主力 UNLIMITED）」過時（aiprimetech 金鑰 401）：先查有沒有換過金鑰；查不到就放 🤫（只有教練能給新金鑰）。
3. 承接下方 19:45 棒：軍火庫設計稿教練回應後照做、志工頁 `JOINED`、下次登入看 `launchagents_guard.log`、gateway `providers.nvidia.models[17].input` 驗證錯誤等。

🙋 要教練決定：軍火庫企劃書 4 件（標題、目標數字、提名信方式、名冊引擎開工）｜問過：2026-10-15 企劃書內
🤫 等教練自己提起：「在群裡幫我接回去」是不是也要開「榮樹下」伺服器頻道（10/17 凌晨問過、未回；要開就在 `channels.discord.guilds` 加 `1560663537527820298`、groupPolicy 改 allowlist，先 dry-run）；Discord Claude「說新對話就自動重開」、開機自動啟動；後台應用程式名稱改成龍蝦特助；Claude 線（aiprimetech）新金鑰；及下方 19:45 棒的 🤫 清單。

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
