## 🔴 給跨對話框軍師讀的總結摘要（2026-09-27 19:37，雲端 Sonnet 5，新的一棒 v253）

**本場主軸：雲端session一開場Stop hook就被「coach888結構性稽核鎖」擋收工，查出是稽核腳本本身在雲端環境會崩潰的bug（假警報），不是真的漏收錄。已完整診斷+驗證修法，但教練裁示「commit診斷、不代表要套用」，留給軍師審批值不值得修，本場故意不改動正式腳本。**

### 1. 🔴 coach888結構性稽核腳本雲端會假崩潰擋Stop（只留診斷+建議修法，未套用，待軍師審批）
**現象**：雲端session連query/git status都還沒做完，Stop hook就跳出「🔴🔒 coach888結構性稽核鎖」擋收工，訊息措辭是「有新頁面沒收錄」。

**查證過程（非猜測，逐步用指令推翻）**：
- 直接手動跑`python3 scripts/audit_coach888_coverage.py --strict`→`FileNotFoundError`，exit code 1
- 原因①：`audit_coach888_coverage.py`第23行寫死Mac專屬路徑`Path("/Users/bymyway/.openclaw/workspace")`，雲端主機沒有這個路徑
- 原因②：就算改成`Path.home()`，雲端工作頁本來就只`sparse-checkout` main分支的`scripts/knowledges/cloud_sync`等目錄（見`.claude/cloud_bootstrap.sh`），不含`event-signup/`，也沒有`~/github_repos/coach888/`——這兩個來源檔在雲端環境本來就不存在，不是「沒下載到」而是設計上就不打算下載
- 呼叫端`stop_rules_master.py`把「腳本崩潰」跟「腳本正常跑完、真的找到新缺漏」都當成returncode 1一視同仁去擋Stop，等於**雲端每次收工都會被這個假警報擋下，跟這場對話有沒有交付新頁面完全無關**（本場只跑了`git log/status/diff`唯讀指令，沒碰event-signup、沒`gh repo create`）

**已驗證的建議修法（未commit進正式腳本，只是診斷紀錄）**：
```diff
--- a/scripts/audit_coach888_coverage.py
+++ b/scripts/audit_coach888_coverage.py
@@ -20,7 +20,7 @@ import re
 import sys
 from pathlib import Path

-WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
+WORKSPACE = Path.home() / ".openclaw" / "workspace"
 APP_PY = WORKSPACE / "event-signup" / "app.py"
 COACH888_HTML = Path.home() / "github_repos" / "coach888" / "index.html"
 BASELINE_PATH = WORKSPACE / "scripts" / "coach888_audit_baseline.txt"
@@ -65,6 +65,15 @@ def extract_visible_section_html(full_html: str) -> str:


 def main():
+    if not APP_PY.is_file() or not COACH888_HTML.is_file():
+        # 雲端工作頁只sparse-checkout main分支的scripts/knowledges/cloud_sync等目錄，
+        # 不含event-signup、也沒有~/github_repos/coach888(見.claude/cloud_bootstrap.sh)，
+        # 這裡讀不到來源檔是環境限制，不代表教練真的漏收錄了什麼——照
+        # stop_rules_master.py呼叫端的既有原則「稽核腳本本身故障不該擋住教練收工」，
+        # 安靜跳過，不當成新缺漏擋Stop。
+        missing = APP_PY if not APP_PY.is_file() else COACH888_HTML
+        print(f"⚠️ 找不到 {missing}（本環境無此checkout，跳過此稽核，不代表有漏收錄）")
+        return
     app_text = APP_PY.read_text(encoding="utf-8")
     coach888_text = COACH888_HTML.read_text(encoding="utf-8")
     visible = extract_visible_section_html(coach888_text)
```
本地驗證：套用後`python3 audit_coach888_coverage.py --strict`從崩潰(exit 1)變成正常印警告+`exit 0`；`bash stop_rules_master.sh`整支也回`exit 0`。Mac本機因為`event-signup/app.py`跟`~/github_repos/coach888/index.html`真的存在，這個if判斷不會觸發，稽核邏輯完全不變——**這個修法只影響雲端假警報，不影響Mac正式稽核**。

**教練裁示（09-27 19:36親口）**：commit診斷結果，不代表要執行修復；留給桌面版軍師有額度時審批這個判斷值不值得做，不要在雲端這場對話直接跑指令試修（避免白耗額度）。

### 📋 下一場開工先做
軍師看到這則，決定：①同意→把上面的diff實際套進`scripts/audit_coach888_coverage.py`並commit＋push main②不同意/有更好想法→直接在這裡回覆理由即可，不用回頭問教練（這是純技術判斷，教練已授權軍師審批）。套用後記得跑一次`bash scripts/stop_rules_master.sh`確認雲端不再假擋，也在Mac本機跑一次確認`event-signup/app.py`存在時邏輯沒變。

（09-30 14:40教練總結收工：這棒到此結束，教練接下來改用本地端（Mac桌面版）繼續跑後面的流程，這則交接棒是唯一要接手的東西，沒有其他懸而未決的事。這場「查到bug但不確定該不該修」的處理方式已寫成通用原則，見試金石案例91（merge時發現案例90號碼被聯想機的RustDesk案例先用掉，已改編號91，內容不變），日後雲端session遇到同類情況可直接照案例91的四步驟做，不用重新請示。）

### 🔑 本場commit
workspace（main分支）：`b85d746`、`3809457`、`4d4fd15`（總結收工，補案例91）、`64486f0`（merge聯想機09-28案例90，解決案例編號衝突）

---
## 🔴 給跨對話框軍師讀的總結摘要（2026-09-27 00:25，Mac桌面版 Opus 5.5／Sonnet 5 交替，新的一棒 v252）

**本場主軸：審議Sonnet寫給Opus的VPS遷移信，抓出安全漏洞；修好「開工沒讀到信」的根因；LK888接上第二個帳戶自動備援；大台南商圈名冊換照片＋全站網址統一event開頭。**

### 1. 🔴 審議VPS遷移信→抓到github_repos外洩漏洞（試金石案例86）
shops.bymyway.com新路由只查「資料夾存在」，整個`~/github_repos`（含來賓名單.db、log）外人可下載。修法：白名單＋`_serve_repo_file()`擋.db/.env/.log/.sql/.py/.sh/.bak。log查無外人下載紀錄（但log不記Host，無法100%排除）。信件補第八節審議結果。commit `56da56292` `8535c8be0` `34b90d80e`。

### 2. 🔴 開工沒讀到信的兩個根因（教練連問兩次）
①開工注入超過10KB被收成檔案只露出2KB預覽，第2~6步沒讀→信件改置頂；②赫米斯寫給Mac的一般信放`cross-agent/inbox/mac/`，派工程式看不懂就發Telegram叫教練「找人看」（搬運工）→開工注入直接列出信箱未歸檔信件，派工程式不再通知教練。實跑驗證。commit `5ff0b8b5a`。

### 3. LK888第二帳戶＋自動備援
收費閘門`lk888_guard.py`加多組金鑰：額度不足(401/402/403/429＋訊息含額度字樣)同一張自動換下一條線，不重跑。憑證層順序：1號線＝09-26新帳戶(主要)、2號線＝原帳戶(備援)，教練選自動切換不用暗號。封網模擬＋兩線只讀登入驗證OK；LK888沒有查餘額API。commit `d5ed28f4b`。教練貼的新金鑰曾進對話蒸餾檔，金鑰掃描攔下已遮蔽，從未進版控。

### 4. 大台南商圈名冊＋全站網址統一
①鑫瀚昌旅行社還是Google地圖：09-26早上25張卡片是人工換照片，兩支插卡程式沒一起改→`curation_process.py`新增`update_directory_card_photo()`、`insert_tainan_shangquan_card()`照片優先②牛市町換教練截圖插畫③傅恩平換他網站裡的空白筆記本照④**教練拍板全站店家網址統一`event.bymyway.com/curated/`**：迴頭快剪/ema/鑫瀚昌搬過去，shops.bymyway.com只剩301轉址（kr→/KR/），自助登錄暫代頁直接建在/curated/並登記名單，赫米斯AGENTS.md/SOUL.md說明同步。全部真實網址驗證。commit workspace `96a513627` `2cb4a498d`(被自動同步一起收進)、tainan-shangquan `b386886` `9d40e7c`、赫米斯 `333c4aa`。

### 5. 教練問Claude Pro要不要升Max
查實際用量：本週已用93%、還有3天半才重置（台灣時間9/30 13:00）→建議升級；Max額度不能給小龍蝦用（訂閱不產API key，官方也禁止訂閱登入給第三方用）。教練尚未決定，不用追問。

### 📋 下一場開工先做
（09-27 01:35 已評估完成，不用再當交辦重報）大台南商圈shops.bymyway.com改event.bymyway.com後，查證FB是否要清舊網址：curl驗證shops.bymyway.com/、/kr/、/huitou/、/hsinhan/全部301/302正確轉址到新網址；查「大台南策展中心」FB粉專從最新到9/6最早一篇貼文全文，沒有任何一篇貼文內文含shops.bymyway.com連結（含API自動貼文批次跟09-18真人瀏覽器重貼批次，全部本來就是event.bymyway.com/curated/）。結論：FB不用改，舊網址有轉址接住。

（09-27 00:40 已處理，不用再當交辦重報）FB申訴查到：支援案件ID 1104855015568562「Hacked asset」，9/12起狀態「已收到」、從未更新；吳大樹個人帳號2021-06-28起「帳號受到限制」(廣告刊登準則，AI偵測)，個人廣告帳號/3個粉專/兩個商家資產管理組合連帶受限；頁面上沒有「要求審查」按鈕，只剩案件的「前往聊天室」可催件。09-27 01:14 AI擬英文催件信（案件編號/受限資產清單/請求指派專員+補件需求+時程）貼進聊天室，教練親自送出（只送出1則，完整1258字）。之前教練9/12已催10次、9/13被回「此案無法透過聊天處理」。之後等Meta回信到bymyway7@gmail.com或聊天室，教練提起再查，不主動追。

### 🔑 本場commit
workspace：`56da56292` `8535c8be0` `34b90d80e` `5ff0b8b5a` `d5ed28f4b` `96a513627` `2cb4a498d`；tainan-shangquan：`b386886` `9d40e7c`；赫米斯：`333c4aa`。本次總結commit另計。

---
## 🔴 給跨對話框軍師讀的總結摘要（2026-09-26 22:47，聯想Windows Sonnet 5，新的一棒 v251）

**本場主軸：跨天長session，主要處理教練交辦的兩個Netlify網站文案修改+部署，另外兩度撞見並修復這台機器git session-end自動同步卡住的問題（一次是6天沒人發現的中斷rebase，一次是這次收工時撞到的HEARTBEAT.md合併衝突）。**

### 1. workshop-invite.netlify.app：結繩領導學工作坊邀請頁改期為11/25-26台北劍潭青年活動中心
這是手動zip部署型網站（非GitHub自動部署），本機找不到原始檔案，改用curl直接抓正式站HTML當來源編輯。日期/地點/邀請函文字全部照教練逐字指示修改。**過程中一度誤判**：把原本頁面上已存在的「我要出席台北場」按鈕連結當成未知資訊去問教練，教練指正「這個台北場連結本來就是11/25-26的報名連結」——查證用的是既有資料裡本來就寫明的答案，不該當成缺失資訊反問。改完後本機Chrome預覽給教練看過確認才用`.NET ZipArchive`打包+Netlify Deploy API上線，curl驗證正式站內容正確。

### 2. jiesheng-leadership.netlify.app：主站拿掉台南場，只留台北場
這是GitHub自動部署型（git push即觸發Netlify），改法跟上面不同。教練說「現在唯一的一廠就是台北廠」，把hero區與訂價區的台南場文案跟按鈕全部移除，只留台北場（11/25-26）跟單顆報名按鈕，本機預覽確認後git push，curl驗證正式站無殘留「台南」字樣。

### 3. 🔴 兩度修復這台機器session-end自動同步卡住的git異常
①**09-21**：發現repo從09-15起卡在一個沒人注意到的interactive rebase整整6天，疊加多個異常commit；查證後確認是09-19教練裁示的`git-filter-repo`金鑰清除事件後續（本機clone跟改寫後的origin/main完全無共同祖先），依既有SOP建立安全網(tag+branch)後`git reset --hard origin/main`對齊解決。②**09-26收工時**：`git status`顯示HEARTBEAT.md又進入合併衝突（UU），這次是本機與Mac同時間點各自的session-end同步互撞。解決衝突時發現一個新技術坑：**`git rebase --continue`在這個git版本(2.53.0)即使index裡沒有任何unmerged條目，只要還有「已修改但未staged」的其他追蹤檔案（如`state/sync_health/tree.json`），仍會報「You must edit all merge conflicts」拒絕繼續**——必須把所有modified檔案（不只衝突檔）一起`git add`才會放行，這點跟一般認知的「只需resolve衝突檔」不同，已記進記憶備查。修復後`pull --rebase`把Mac累積的13個新commit拉下來，push成功。

### 📋 下一場開工先做
兩個Netlify網站修改已交付教練確認完成，沒有懸而未決的事。git同步異常這類問題如果第三次出現，優先懷疑是不是又有未清乾淨的舊金鑰歷史殘留或多機同時寫入HEARTBEAT.md衝突，不用重新從頭排查。

### 🔑 本場commit
`daf2f1984`(HEARTBEAT.md合併衝突修復)、聯想此前已推送的handoff更正commit（09-21 session）。workshop-invite/jiesheng-leadership為Netlify/GitHub上的獨立repo部署，非本repo commit。

---

---

> 📦 v248~v250完整內容已封存：`handoff_archive/handoff_v248_to_v250_archived_2026-09-27.md`（v248公開交接棒上線／v249開工hook與赫米斯上架bug／v250 VPS遷移與鑫瀚昌）

> 📦 v247完整內容已封存：`handoff_archive/handoff_v247_archived_2026-09-26.md`（v247：赫米斯登入自動跳出根因修復+副螢幕防呆+模型分工v2上線+雲端方案分岔陷阱查證）

> 📦 v246完整內容已封存：`handoff_archive/handoff_v246_archived_2026-09-25.md`（v246：執行細則16條E併9條N規則上線+VPS/LINE/大台南小幫手每位朋友單獨記憶查證+龍蝦小助教記憶檔被巡檢指令灌爆bug修復）

---

> 📦 v245完整內容已封存：`handoff_archive/handoff_v245_archived_2026-09-25.md`（v245：VPS/LINE健檢推播404修復+五項修法落地+小龍蝦2.0評估+版本變動通知）

> 📦 v244完整內容已封存：`handoff_archive/handoff_v244_archived_2026-09-25.md`（v244：大樹創作SOP口語別名缺失修復+coach888插入bug修復+coach888分類重組+MEMORY.md清理）


> 📦 v242~v243完整內容已封存：`handoff_archive/handoff_v242_to_v243_archived_2026-09-24.md`（v242產業鏈SOP誤報700+分類資料庫查證+名片系統去識別化技術文件雙版本交付／v243 MEMORY.md索引159筆清零+namecard-db前會員/來賓資訊改造+cloudflared版本過舊發現解決，E16瘦身2026-09-24執行）
> 📦 v238~v241完整內容已封存：`handoff_archive/handoff_v238_to_v241_archived_2026-09-24.md`（含全面體檢/agents人設檔救回/llama-cpp修復/聚寶盆發票/ezPay作廢SOP等v238~v241全紀錄）

---

## 📋 現在真正待辦（狀態追蹤總表，2026-07-24建立；2026-09-24教練要求根源改版）

> 🔴 **2026-09-24根源改版（教練：「同一類事情不要再重複來煩我了」）**：這張表是**AI自己的工作筆記，不是要唸給教練聽的清單**。任何事要拿去問教練，必須同時過三關，少一關就不准問：
> ① **只有教練能做**：花錢、代表教練對外發言、不可逆操作、教練自己的內容與喜好、需要教練本人親自登入（例如要手機簡訊驗證碼、教練個人銀行等系統從未存過帳密的帳號）。路徑大全／既有腳本裡已存好帳密的主機與服務（VPS、GitHub、Netlify、ezPay等），AI 自己用，不算這一關。AI自己查得到、做得到、判斷得了的，一律自己處理。
> ② **教練沒答過**：先查本表、封存檔、記憶檔。教練裁示過的（含「不用管」「略過」「到此為止」「保留就好」），換任何說法都不准再問。
> ③ **現在不問會卡住**：教練正在等結果，或幾天內有期限。不急的放「等教練自己提起」，不主動提。
> **每件事最多問一次**：問過沒回應＝教練現在不想處理，移到「等教練自己提起」，不准追問、不准開工重唸。
> **開工回報不唸待辦**：只講「🙋要教練決定」裡還沒問過的（通常是零件），然後問「今天從哪件事開始？」
> 教練裁示「不用管／不做／略過」的列，當場搬去封存檔，不准留在這裡。

### 🙋 要教練決定（三關全過才能放；格式：標題｜只有教練能做的原因｜卡住什麼｜問過：日期或「未問」）
（目前沒有）


### 🤫 等教練自己提起（AI不主動問、開工不唸；教練提到時才去封存檔查詳情）
> 詳情全文：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`
- 大台南商圈示範版位林百貨/神農街換成建築/街景照（要從網路下載照片，09-26已問過一次，教練沒回）
- VPS升級LTS 2026.7.35（教練09-24：10/1左右月報會自動提醒，時間到再說）
- 367位前會員推薦人補查（BNI Connect帳密沒存在路徑大全，要教練本人登入一次；09-24已問過一次）
- 柯朝陽發票（教練09-24：延後約一年，不用管）
- 試金石商業化計畫書（教練09-24：還沒想到怎麼商品化，暫時不用管）
- 小二(test2)/OpenClaw 2.0評估（暫停，等官方修復）
- 小二Telegram輪詢異常（教練09-21：等小二成熟再處理）
- 聯想C碟WinSxS再瘦身4~5GB（要不要做，教練沒回）
- bni-chapters真誠分會網頁架構問題（教練還沒說明是哪個問題）
- 「教練都在想什麼」補更多素材（等教練提供）
- 其他LINE帳號比照搬遷（等教練指定帳號，SOP已備妥）
- 小龍蝦後台看不到中文名（教練裁示：看到陌生ID問了再回）
- coach888拖拉排序好不好用（等教練回饋）
- 「全世界最優秀的團隊計畫」報名連結（等教練給網址）
- 企業健身房正式建站（等教練交辦）
- 企業健身房4項文案修改（等教練交辦下一步）
- BNI小幫手實戰體驗（等教練親測）
- Coze舊機器人何時停用（等教練裁示）
- ACER 36.3GB備份刪除（需教練在ACER親自開對話）
- 赫米斯Telegram線登出登入時斷約2分鐘（綁使用者登入，要改成開機常駐系統服務才能根治；09-25已告知一次，教練沒要求處理）

### 🔧 AI自己的工作清單（AI自行處理，做完不用跟教練報告細節）

> 📦 **更早162筆已完成列**：`handoff_archive/handoff_status_table_completed_archive_2026-09-18.md`；**09-24搬出的21筆結案列**：`handoff_archive/handoff_status_table_parked_and_closed_2026-09-24.md`

| 優先 | 任務 | 狀態 | 說明 |
|---|---|---|---|
| 🟡 | **團隊協作全面體檢（2026-09-24 Opus 5.5）：五項修法教練13:37說「執行」，已落地** | ⚠️持續追蹤-首次真實使用待觀察 | 完整報告`knowledges/2026-09-24_團隊協作全面體檢報告.md`。①每日08:10全隊點名`scripts/daily_team_rollcall.py`+launchd`ai.openclaw.daily-rollcall`(13:41實跑送達)；VPS/LINE健檢改為只在異常時通知②VPS看守Mac：VPS`/root/watch_mac.sh`每30分，Mac連續兩次連不上才通知(測試訊息message_id 3860送達)③上傳頁`kind`必填，`creation`全自動進coach888最新作品——**09-25首次真實作品實測，發現index.html判斷bug已修復**（個人創作常沒有index.html慣例檔名，改成剩一個html檔就自動採用，見v249），真實上架成功④產業鏈同主題同對話10分鐘防重複⑤VPS健檢拿掉1小時無活動誤報；赫米斯記憶檔金鑰是教練指示保留的寫法，不搬。commit`b076a80fc`+`777c9c7c4`。**VPS升級另見下一列**。VPS健檢缺天原因仍未查明，改由每日點名檢查「今天有沒有跑」。 |
| 🟡 | **雲端工作頁規則同步（2026-09-25 Opus 5.5，教練原則：同一套規則本機雲端一體適用，只有動到Mac本機的事例外）** | ✅已上線，兩條路實測通過 | 機制與SOP見記憶`reference_move_to_cloud_this_repo_2026-09-25.md`：`cloud_sync/`(全域規則+11技能副本，每則回覆結束自動更新)+`workspace/.claude/settings.json`(main)+外層`.claude/settings.json`+`cloud_bootstrap.sh`(master)。commit`1e0bea3ab`+`2db3d1330`(workspace)、`a0975a949`(外層)。**待修小bug**：`model_tier_advisor.sh`剛用/model切換後的第一則仍顯示舊模型(09-25切Opus後仍報sonnet-5)，雲端第一則顯示「未知模型」。外層master分岔已查證安全並合併推送`f517ec524`，v247「791d775d2未push」一句已過時。 |
| 🟡 | **公開交接棒「隨身軍師・一鍵接手」上線（2026-09-25，教練說「推」，後續修好AI相容性問題）** | ✅已上線，每次「總結」自動更新 | **主要網址（貼給任何AI）：`https://coach1973.github.io/ai-go/status.html`**；純文字備用：`status.md`。目的：教練Claude每週額度不夠，思考型問題分流到其他網頁版Opus，貼一個網址對方就知道規則＋目前工作狀態。🔴**真因查證（curl實測，不是猜的）**：一開始只做.md版，教練回報「其他AI說讀不到、被屏蔽」——查證GitHub Pages對.md副檔名回傳`content-type: text/markdown`，index.html回傳`text/html`；人爬蟲UA(GPTBot等)全部200無阻擋，不是robots/WAF——是多數AI內建讀網頁工具只認text/html。已建`scripts/render_public_status_html.py`(python-markdown轉換+bare URL自動連結)，`status.md`仍是唯一手改來源，`scripts/publish_public_status.sh`每次發布自動轉出`status.html`不會分岔。更新流程：`summary_upload_trigger.sh`第5步改寫`~/github_repos/ai-go/status.md`→跑`publish_public_status.sh`(機密掃描→轉HTML→再掃描→commit兩檔→push→確認網站換新版，等5分鐘)。只寫教練自己的事，不寫帳密/主機位址/路徑/他人個資。已收進coach888「工具類」第一項並改指向.html（伺服器狀態+靜態HTML都改，舊狀態備份`state/coach888_state_backup_20260925_110956.json`）。同場順便修正教練品牌數據「1.5萬位老闆」→「6,000+場演講、10萬人受眾」（教練親口訂正，5個檔案）。🔴**教練追問揪出遺漏**：status.html內文引用的另外兩份`coach-persona.md`/`system-prompt.md`本身也是同一個content-type問題，沒有一起修——已比照建`coach-persona.html`/`system-prompt.html`，三份都納入`publish_public_status.sh`自動轉出，`index.html`的「查看全文」連結也改指向.html（JS一鍵複製到剪貼簿的fetch()維持指向.md不變，複製出來才是純文字不是HTML標籤）。順便修好`publish_public_status.sh`驗證上線的迴圈：GitHub Pages CDN偶爾超過5分鐘才生效，push本身成功卻被誤判成失敗跳exit 1（已實際發生2次），改成push成功就算數，CDN慢只如實回報不當失敗。commit：workspace`445210e92`+`8f953cd14`+`5ea38190d`、ai-go`39b84c7`+`22bbe94`+`5114dc3`+`3f4273e`、coach888`79a7d81`+`03021cb`。 |
| 🟢 | 外層`~/.openclaw`本機git歷史紀錄跟GitHub版本編號對不齊（純本機書面整理，教練2026-09-24裁示：不是外洩、不是公開風險，AI自行找時間處理，不用再提） | ✅無風險-低優先-AI自主處理 | **教練2026-09-24明確裁示**：這不是安全問題（金鑰外洩早在9/19處理完畢，repo本身是私有的、沒有外部協作者，也已決定金鑰不rotate），純粹是這台Mac的git紀錄本子跟GitHub對不上編號的書面瑣事，沒有任何被公開查到的風險，也沒有立即性危害。**教練要求：AI不准再主動提這件事，覺得需要處理就自己找時間安靜做完，不要拿來討論、不要問、不要當成待辦逐場複誦**。哪天AI自己收拾好了，直接做、不用報告；沒收拾好也不影響教練現在用的任何功能，不追蹤、不升級語氣。技術細節（若AI自己要動手）：新版GitHub歷史已把`agent/auth-profiles.json`等金鑰檔從全部commit移除，本機若直接`git reset --hard origin/master`會把本機正在用的同名檔案從磁碟刪掉，須先備份+確認`.gitignore`涵蓋再處理，過去做法可參考`c07544815`的worktree cherry-pick模式。 |
| 🔧 | **AI技術備忘（不准拿去跟教練講）：這個repo的git歷史已被改寫，其他機器的本機clone要先同步才能push** | ⚠️任何機器的AI下次動這個repo前自己看 | 2026-09-19 06:45教練親自裁示後，軍師用`git-filter-repo`把`路徑大全_憑證層.md`+`agent/auth-profiles.json`+`agent/models.json(.bak)`4個含明文金鑰的檔案從全部16000+ commit歷史徹底清除+強制推送到GitHub(已用全新clone獨立驗證確認乾淨)。**任何其他機器(聯想Windows/ACER/VPS)如果有這個repo的本機clone，現在都跟GitHub遠端分岔了**——下次要push前必須先`git fetch origin && git reset --hard origin/main`(或直接砍掉重新clone)，絕對不能在沒同步的狀態下直接push，否則會把舊歷史(含外洩金鑰)重新推回去，等於這次白做。教練同時裁示：外洩的金鑰(MiniMax/Gemini)**不rotate**，「已經曝光不代表會被濫用，換的話動一髮牽全身」。完整過程見[[feedback_credential_layer_file_was_git_tracked_2026-09-19]]。 |
| 🔴🔴🔴🔴 | **全機必讀：Netlify圖片部署事故檢討報告** | ⚠️永久提醒 | 2026-07-25聯想機一件本該一次做對的事做了3次部署才成功（多扣30點credit），教練親自要求全機軍師都要吸收教訓，完整報告見`knowledges/2026-07-25_ai-talk圖片部署事故檢討報告_明明有SOP卻沒執行.md`。三條鐵律：①Netlify `_headers`不用`/*`萬用規則(除非站台永遠沒圖片) ②Windows打包zip給Netlify禁用PowerShell`Compress-Archive`(反斜線路徑會404)，改用.NET ZipArchive ③部署後驗證文字跟圖片要分開各自curl確認，圖片要專查Content-Type不能只看狀態碼 |
| ⚠️ | Netlify部署額度 | ⚠️持續追蹤 | credit制，「剩幾次」=credit餘額÷15(每次部署耗15點)。`state/netlify_deploy_quota.json`最新記錄剩50次(2026-08-05，jiesheng-leadership git-auto-deploy推送後)。這只是本地推算，建議教練有空時親自到Netlify後台billing頁面核對一次真實數字最保險 |
| 🔴🔴🔴 | **Netlify站分兩型，動手前必查是哪型(2026-08-05二度誤推)** | ⚠️永久提醒 | `feedback_netlify_deploy_zip_api.md`早就記載`jiesheng-leadership`是GitHub自動部署型(2026-06-09第一次血淚)，本場(2026-08-05)Sonnet 5仍然只想著「教練說先推GitHub」沒有觸發查證動作，導致同一個錯犯第二次。已補進記憶+更新MEMORY.md索引標題直接寫「動手前必查是哪型」。**新鐵律**：聽到「推GitHub」這類指令，只要牽涉Netlify網站，一律先查是不是自動部署型，不能拆開處理成「先推一半」 |
| 🔴🔴 | 聯想C槽94GB備份（`易数一键还原Windows系统备份`）**原訂計畫改變** | ⚠️持續追蹤-暫緩刪除 | 2026-07-25發現這份7/11舊備份剛在7/24真的被拿去做過一次系統還原（LINE junction事故+WMI/CIM異常，救回一台機器），證明它有實際救援價值，**不能照原計畫刪除**。建議教練確認今天新裝的OpenCode/CC Switch搬家+Advanced SystemCare移除都正常後，做一次新的一鍵備份取代這份舊的，新備份穩定觀察期滿才能考慮刪舊的，詳見[[project_lenovo_c_drive_slimdown_2026-07-11]]更新 |
| 🟡 | **shops.bymyway.com已拆除VPS依賴（2026-09-26）；09-27教練拍板全站統一event.bymyway.com/curated/，shops只剩舊連結轉址。VPS上舊檔案+GitHub孤兒repo收尾** | ⏳待處理-低優先 | 3家店(huitou/ema/hsinhan)已遷移到Mac本機+DNS切換完成，VPS(43.245.60.200)上`/var/www/shops/`原始檔案故意沒刪，當一段時間的rollback安全網，穩定觀察期(建議至少2週無異常)過了可以安全刪除。另外測試時意外建立的GitHub孤兒repo`coach1973/hsinhan-2`因手上token沒有`delete_repo`權限刪不掉，已無任何連結指向它、無害，之後若拿到有delete權限的token可順手清掉。詳見`knowledges/LETTER_VPS策展中心遷移過程說明_給Opus_2026-09-26.md`。**09-26 Opus審議**：遷移時shops路由沒比照/curated/的白名單，整個github_repos(含來賓名單.db)可被外人下載，已修(白名單+敏感副檔名防線，實測)，詳見信第八節。 |
| 🟡 | MEMORY.md超過OpenClaw 2萬字bootstrap上限(20,717字)且有1處UTF-8亂碼，跟HEARTBEAT.md同一類問題(2026-09-25查到，只查不動，優先度低於HEARTBEAT.md因為不影響小龍蝦即時反應) | ⏳待處理 | 用跟HEARTBEAT.md同樣手法瘦身：找出佔比最大的段落搬去handoff_archive或distill、備份原檔、確認新檔UTF-8正常。不用問教練，AI自己找時間做完即可 |
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

> 📦 v218完整內容已封存：`handoff_archive/handoff_v218_archived_2026-09-19.md`（Mac桌面版，全部釋放+MiniMax團隊品質稽核機制+開工hook身份誤判修復+幕僚長晨報重建+Netlify中文檔名部署bug發現）

---

> 📦 v219完整內容已封存：`handoff_archive/handoff_v219_archived_2026-09-19.md`（Mac桌面版，手機/軍師討論邊界+Netlify中文檔名修復部署+後台帳密清單結案+workspace git大掃除含金鑰外洩發現+coach888熱門排行新功能）

> 📦 v220完整內容已封存：`handoff_archive/handoff_v220_archived_2026-09-19.md`（Mac桌面版，接力棒狀態表失真教訓+機械防呆`handoff_sync_guard.sh`上線+CLAUDE.md 236KB→78KB瘦身+M系列MiniMax 1M機制查證+手機Remote Control重啟卡死未解留待下一棒）

> 📦 v221+v222完整內容已封存：`handoff_archive/handoff_v221_v222_archived_2026-09-19.md`（v221 Mac桌面版，手機Remote Control真正根因查明修復+舊SOP早有答案的教訓／v222 Mac桌面版，中正大學互動牆從零建置上線+赫米斯Telegram斷線16小時根因修復，E16瘦身本場執行）

> 📦 v223~v227完整內容已封存：`handoff_archive/handoff_v223_to_v227_archived_2026-09-20.md`（v223 B路徑1M通驗證／v224跨對話框交接SOP／v225 MiniMax懸案初步調查+coach888同步修復(平行session)／v226產業鏈SOP雙執行root cause／v227 MiniMax懸案徹底解謎+手機1M實測成功，E16瘦身2026-09-20執行）

---


> 📦 v228~v230完整內容已封存：`handoff_archive/handoff_v228_to_v230_archived_2026-09-21.md`（v228憑證層git追蹤問題發現／v229 git-filter-repo歷史清除執行完畢／v230 CCU留言關閉+coach888收錄查證，E16瘦身2026-09-21執行）

---

> 📦 v231~v237完整內容已封存：`handoff_archive/handoff_v231_to_v237_archived_2026-09-24.md`（v231 TokenTable接OpenCode+Episode11漫畫+agent捏造完工案例／v232 CCU媒體格式連環修復／v233海餅乾網站+BNI PPT SOP建立／v234聯想bni-dna/bigtree維護+記憶體洩漏追蹤／v235手機流量查證鏈+EM模式定義／v237膠囊咖啡機產業鏈+語音轉簡體字記錄，E16瘦身2026-09-24執行）
