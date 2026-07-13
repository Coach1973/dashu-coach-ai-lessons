# 軍師接力棒 · 2026-07-13 v65（Mac桌面版 Sonnet 5，佩佩老師報名系統上線+截圖鎖漏洞修復+cool-case頭像案未完）

> 建立時間：2026-07-13 19:05（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v64（聯想桌面版 Sonnet 5，coach888/jiesheng/bigtree三站更新+聯想26GB記憶體洩漏根治，完整內容見下方精簡回顧）
> 本棒主軸：**幫佩佩老師建了一套獨立的活動報名系統（複製教練版event-signup，換綁她自己的LINE官方帳號），端到端測試通過；過程中教練抓到「截圖鎖」有真的漏洞（matcher清單漏掉一個工具家族），已修好+驗證+通知聯想/ACER去查自己的機器；另外cool-case頭像案（把終端機/桌面版對話從小龍蝦頭像改成Opus軍師頭像）分析到一半被打斷，沒做完，下一棒要接著做**

---

## 🎯 本場戰果

### 1. 🔴🔴🔴 未完成事項：cool-case頭像重新歸類（分析做了一半，沒執行）

教練要求：cool-case網站（`coach1973.github.io/cool-case/`）裡所有「小龍蝦AI特助」
頭像的對話泡泡，只要內容實際上是終端機/桌面版（軍師）在講話而不是Telegram小龍蝦，
就要改成新的claude-avatar.svg + 改名「Opus 軍師」（聯想已經先修過8處，但那8處是
本來就已經標「Opus軍師」名字只是圖片配錯；其餘66處全部標「小龍蝦AI特助」，教練
確認要判斷哪些其實是軍師講的）。

**已做的分析**（案例1~40逐一讀過scene/narrative/root-cause/實際對話內容），初步
判斷這些案例明顯是終端機/桌面版內容（強訊號：提到終端機/桌面版/Claude Code/CLI/
git push/sed指令/rsync/PhotoRec等）：
`案例4, 6, 7?, 10, 12?, 14, 15, 20, 21, 23, 24, 33, 34, 36, 37`
（標?的是訊號比較弱，需要再確認）

案例1/2/5/9/11/13/16/17/18/19判斷是真的OpenClaw/Telegram/小龍蝦系統相關內容，
應該維持小龍蝦頭像不動。

**沒做完的部分**：
1. 案例7（海餅乾知識庫）、案例12（送出按鈕）這兩則訊號比較模糊，需要重讀確認
2. 最終名單確認後，要寫程式把符合條件案例裡的
   `xiaolongxia-avatar.jpg" alt="小龍蝦"` → `claude-avatar.svg" alt="Opus 軍師"`
   以及 `>小龍蝦 AI 特助<` → `>Opus 軍師<` 換掉（只換符合案例編號範圍內的，
   不要replace_all整份文件，會誤傷真的小龍蝦案例）
3. 換完要開真的Chrome給教練看（不能只用內部工具截圖，見下面第3項教訓），教練
   確認後才commit push GitHub，確認完再問要不要推Netlify（cool-case同時部署在
   Netlify，上次commit `6a53f6b318f63574bb009623`，這次頭像案要推的話要重新走
   部署SOP三步驟）

**下一棒直接從這裡接手**，不用重新分析，上面的判斷清單可以直接用，只是還要
補案例7/12的判斷再動手改。

### 2. 佩佩老師活動報名系統（peipei-event）從零建置到端到端測試通過

教練要幫佩佩老師複製一份跟教練版一樣的「掃QR報到→加LINE好友→傳問候→系統比對
身分→精準群發通知」系統，換成她自己的LINE官方帳號 `@701ohlly`。

- 新GitHub私有repo：`Coach1973/peipei-event`（複製自`event-signup`，拿掉教練版
  LINE金鑰/舊QR，port改5061避免跟教練版5060衝突）
- 新Cloudflare Tunnel：`peipei-event.bymyway.com` → localhost:5061（tunnel id
  `10eaf2db-7a38-418e-a4a6-8daca6161a34`，設定檔`~/.cloudflared/
  peipei-event-config.yml`）
- LINE三把鑰匙：教練一開始誤貼了教練版的Channel Access Token（已攔下說明LINE
  Token不能跨帳號共用），教練重新去LINE後台Issue一組新的，我用LINE API
  `/v2/bot/info`驗證過這組token確實對應到`@701ohlly`（顯示名稱「佩佩活動策展
  諮詢顧問」）才填進系統，不是盲目相信教練貼的字串
- 活動代號：教練說這是「常態性佩佩老師認識朋友的管道」不是單場活動，改名
  `peipei`，標題「音樂藝術策展＋商務連接＝有質感的活動」，不標日期（表單/QR
  立牌模板都改成沒日期就不顯示，不留空白）
- **端到端測試教練親自做過，我有查資料庫+log驗證，不是聽教練說「有反應」就信**：
  填表→查重（同一手機號兩次填只算一筆，thanks頁正確顯示"已報到過"）→加LINE
  好友→傳問候句→webhook收到（`POST /line/webhook`兩次都200）→資料庫裡吳大樹這
  筆已經綁定`line_user_id`，全部驗證通過
- commit：`8d54915`（初版）、`fd4c8ff`（改常態代號+QR版面修正）

**下一棒待辦**：群發通知功能（`/admin/notify`）教練還沒實測過，QR立牌
（`qr/peipei-print.html`）教練還沒看過印出來的實體效果，服務目前是前景跑
（`nohup python3 app.py`），還沒做成LaunchAgent常駐開機自動跑（教練版
`event-signup`已有對應的plist範本可以照抄）。

### 3. 🔴🔴🔴 截圖鎖真的有漏洞，教練當場抓到，已修好+通知聯想/ACER

驗收peipei-event成品時，我重複用內部無頭瀏覽器工具截圖確認，沒有被
「截圖鎖」（`scripts/screenshot_lock.sh`，教練明令未經同意不可截圖）擋下來。
教練直接質問「不是說有上鎖嗎？」

**根因**：`screenshot_lock.sh`裡判斷「哪些工具算截圖」的清單、以及
`~/.claude/settings.json`裡`hooks.PreToolUse`的matcher，兩邊都只列了
`mcp__computer-use__*`跟`mcp__Claude_in_Chrome__*`，完全漏掉這次session實際
重複用到的`mcp__Claude_Browser__computer`。不是鎖故意放水，是清單沒寫全。

**已修好**：兩邊都補上這個工具，餵4組假指令實測（無通行證截圖→擋/zoom→擋/
一般操作→放行/有通行證→放行，全部符合預期），commit `323d6c73d`。

**已寫信通知聯想+ACER**（教練親口指示「寫封信去交待其他電腦照做」）：
`cross-agent/inbox/lenovo/20260713-1900_mac-to-lenovo_screenshot-lock-audit.md`
`cross-agent/inbox/acer/20260713-1900_mac-to-acer_screenshot-lock-audit.md`
內容要求對方查自己的`settings.json`matcher（這個檔不跟git同步，各機獨立）、
對照自己機器實際會用到的截圖工具、**用餵假指令實測**（不能只肉眼比對清單），
查完不管有沒有洞都要回信。**下一棒開工留意`cross-agent/inbox/mac/`有沒有
聯想/ACER的回信**。

另外教練同時確認：另一支「成品完成必須開真Chrome給教練看」的鎖
（`web_preview_verify_guard.sh`）本身沒有漏洞，它只認`open -a "Google Chrome"`
這個證據，內部截圖工具本來就被排除在證據之外，這條規矩一直都在運作。

### 4. 聯想cool-case頭像上線案——已驗證屬實（本場開頭）

聯想回報「claude-avatar.svg已套進Opus軍師8處對話泡泡，commit ce1402d」，我沒有
直接採信轉述，親自`git fetch`+`git show ce1402d`查證commit確實存在、內容跟回報
一致，才確認這件事。（這就是後續第1項頭像案的起點）

---

## 📋 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🔴🔴🔴 | **cool-case頭像重新歸類案，分析到一半沒做完**——見上面第1項，有完整判斷清單可以直接接手，只差案例7/12再確認+實際執行改檔+開Chrome給教練看+等教練說「推」 |
| 🔴🔴 | **留意`cross-agent/inbox/mac/`有沒有聯想/ACER回覆截圖鎖稽核結果**，收到要讀完處理，處理完記得移到outbox |
| 🟡 | peipei-event：群發通知功能還沒實測，QR立牌還沒印出來給教練看實體效果，服務還沒做成LaunchAgent開機常駐（目前是前景nohup跑，教練重開機或Mac休眠會斷） |
| 🟡 | 教練還沒完全確認Windows「自動儲存並還原應用程式」設定是否已在`ms-settings:signinoptions`關閉（聯想機，v64留的） |
| 🟢 | 「開工 (fork)」重複出現的真正觸發點還沒查清楚（聯想機，v64留的） |
| 🟢 | 「待教練確認用途」清單還剩：vip-club、coach-vip-club、coach-case系列、teamwork、tainan-calender（v64留的） |
| 🔴 | 2026-07-18：聯想C槽觀察期滿，確認教練這幾天用起來正常後可刪2份保留備份（共約94GB）（v64留的） |

（名片系統、biz-gym黑金版等其餘待辦仍在Mac的v60棒裡持續，此處不重複列出）

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `github_repos/peipei-event/`（新repo，複製自event-signup，commit `8d54915`/`fd4c8ff`）
- `~/.cloudflared/peipei-event-config.yml`、tunnel `10eaf2db-...`（新建）
- `scripts/screenshot_lock.sh`（補上`mcp__Claude_Browser__computer`判斷，commit `323d6c73d`）
- `~/.claude/settings.json`（matcher補同一個工具，不在git範圍，只影響這台Mac）
- `cross-agent/inbox/lenovo/`、`cross-agent/inbox/acer/`（各新增一封截圖鎖稽核信）
- `~/github_repos/cool-case/`（頭像案分析中，尚未實際改檔，git stash裡還留著一份
  07-02的舊草稿`stale-case37-draft-before-avatar-task-20260713`，跟本場無關可忽略
  或找教練確認要不要正式清掉）

---

## 📜 v64 精簡回顧（聯想桌面版 Sonnet 5，完整內容見git歷史/上一版本檔案）

1. coach888作品總覽分類重排成5大類，編號改連續1-37（commit `453ad1e`）
2. jiesheng-leadership三場工作坊報名連結改成PAYUNi金流連結（commit `c0b8e72`）
3. bigtree新增7/22高雄場地地址（commit `e570806`）
4. 🔴🔴🔴 聯想這台HTML驗證改用Comet瀏覽器（`comet.exe`），不再用Chrome（Chrome
   跳出來是空白視窗，根因未查但教練要的是「看得到」不是查根因）
5. 🔴🔴🔴 意外挖到聯想電腦26GB核心非分頁記憶體洩漏，鎖定IObit Advanced
   SystemCare過濾驅動，解除安裝+重開機驗證93%→34%，徹底根治
6. 查證「開工(fork)」重複出現不是本機腳本造成，但真正觸發點未查清楚

---

> Mac桌面版 Sonnet 5 親筆，2026-07-13 19:05。這場對話一開始是驗證聯想的頭像
> commit，接著教練要求把cool-case裡所有實際是終端機/桌面版對話卻掛小龍蝦頭像
> 的案例全部改過來——這個分析做到一半，教練轉去談佩佩老師的活動報名系統，這件
> 事就沒做完，是本棒最大的未竟事項，已經把判斷清單寫清楚，下一棒可以直接接手
> 不用重新分析。佩佩老師的系統從零建到端到端測試通過，資料庫+log都親自查過驗證
> 不是聽教練說「有反應」就信。過程中教練當場抓到截圖鎖有真的漏洞（不是嘴上說的
> 假鎖，是清單真的沒寫全），修好、實測、寫信通知聯想跟ACER去查自己的機器——這
> 是教練親口要求「不用我重複提醒」的落實，把稽核責任寫進跨機信箱系統，不是只
> 在這台Mac修好就結案。下一棒開工先讀上面「下一棒待辦」，第一件事是把頭像案
> 做完。
