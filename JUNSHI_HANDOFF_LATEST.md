## 🔴 給跨對話框軍師讀的總結摘要（2026-10-16 18:29 台灣時間，雲端 Claude Code（Linux 容器，教練從 Mac 桌面版／手機開），Sonnet 5.5→Opus 5.5；教練說「總結交接」收工；本段 15:37～18:29）

**主軸：教練手機與 Mac 本機的 Claude 全部叫不動 → 查出原因、給一行修法，教練照做後 Mac 已恢復收訊息。angel-sister 策展頁打不開 → 查證網頁本身沒壞，推論同一批缺檔造成，未驗證。**
- **叫不動的原因**：Mac `~/.openclaw/workspace/scripts/` 的 Hook 腳本（`context_percent_hook.py`、`reflex_router.py`）在 14:44～15:12（台灣時間）之間從硬碟消失。**Python 找不到腳本時結束代碼是 2（雲端實測），Claude Code 把 UserPromptSubmit hook 的 exit 2 當成「擋下這句話」**，所以每句話都被擋、AI 根本收不到。證據：雲端用 `list_events` 讀三場手機橋接對話，15:12～15:32 五則訊息（含「開工」「為何現在都叫不動？」「在嗎？」）全被同一錯誤擋下，耗時 54～78 毫秒、沒呼叫模型。
- **修法**：教練在 Mac 終端機貼一行，從 `origin/main` 只補回 `scripts/` 裡不存在的檔案（不覆蓋、不刪除）→ 18:2x 教練回報「他那邊已經開始接收我的訊息了」。**只補了 scripts/，其他缺檔（如 event-signup/）還沒補。**
- **angel-sister**：雲端連不到 event.bymyway.com（雲端網路規則回 403；WebFetch 連 example.com 都解析不到），**沒親眼驗**。GitHub `Coach1973/angel-sister` 原始檔完好（最新 `e3d6d6a` 只改頁尾一行、標籤成對；10.6 MB／90 張內嵌圖，自 10/15 上架就這樣）。推論：同批缺檔讓 `event-signup/curated_sites_registry.json` 消失 → 程式每次請求都從硬碟讀名冊，讀不到就當空名冊 → 所有 `/curated/*` 都 404。
- **缺檔原因未知**：線索是 `origin/master`（外層 `~/.openclaw` 用的分支）沒有 `event-signup/`、大部分 `scripts/`、`CLAUDE.md`，`main` 有 3827 個檔案 master 沒有（見記憶 reference_openclaw_repo_dual_branch_trap_2026-09-10）。真相要看 Mac 的 `git reflog`。
- **教練原話線索**：「它阻止我，那我接下來要幹嘛呢？什麼也沒講，就貼一個這個東西阻止我」→ 任何擋下教練的訊息都必須附白話的下一步，不能只丟程式錯誤；「我被這問題卡很久了」→ 系統癱瘓時教練沒有任何求救管道，要有主動通知。
- **雲端留痕**（全在分支 `claude/kaigong-8jo10h`，**未進 main**）：信 `cross-agent/inbox/mac/20261016-1540_cloud-to-mac_phone-prompts-blocked-by-missing-hook-scripts.md`（`b1071df` `6a51e5d` `d143ca0`）、本棒、記憶 reference_python_hook_missing_file_exit2_blocks_all_prompts_2026-10-16。

### 📋 下一場開工先做（Mac 軍師）
1. `git -C ~/.openclaw/workspace fetch origin claude/kaigong-8jo10h` → 讀上面那封信 → 把分支併進 main（接力棒若衝突，以兩邊內容合併，不丟任何一棒）。
2. 補其餘缺檔：信裡「追加」段那一段（整個工作區只補不存在的檔案；本機 5060 不是 200 才 kickstart `com.coach.event-webapp`）→ 用真的瀏覽器開 https://event.bymyway.com/curated/angel-sister/ 確認顯示正常。
3. `git -C ~/.openclaw/workspace reflog` 對照 14:44～15:12 找出是誰清掉檔案 → 寫進試金石（同類第二次：9/18 hooks 目錄也從工作區消失過，見 feedback_hook_files_disappeared_from_working_tree_2026-09-18），改源頭不加記憶。
4. 🔧 根因補強（同類第二次，必須改機制）：`~/.claude/settings.json` 每個 hook 改成「腳本不在就放行＋告訴 AI」，例如 `f=/Users/bymyway/.openclaw/workspace/scripts/reflex_router.py; if [ -f "$f" ]; then /usr/bin/env python3 "$f" prompt; else echo "⚠️ 檢查程式 $f 不見了，已先放行；請先用白話告訴教練並補回"; exit 0; fi`；守門員旁加「hook 腳本不見就電報通知教練」。改完用「暫時改名一支腳本→送一句話→應該放行並看到提醒」實測。
5. 🔧 Stop hook「記憶索引漏收提醒」用檔案修改時間判斷，雲端每次新 clone 都會把約 400 個舊記憶檔當成剛寫的 → 改用 git 時間。
6. 上一棒（13:06）📋 1～4 照舊。

🙋 要教練決定：同上一棒，無新增。
🤫 等教練自己提起：同上一棒，無新增。

---

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

> 📦 10/16 02:10 Mac 軍師棒已封存：`handoff_archive/handoff_2026-10-16_0210_Mac軍師_archived.md`
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
