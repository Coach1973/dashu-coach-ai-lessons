# 軍師接力棒 · 2026-07-12 v60（Mac桌面版 Sonnet 5，名片系統雙通道+PaddleOCR換血+Hook稽核+ai-talk網站上線）

> 建立時間：2026-07-12 下午2點（台灣時間）
> 本棒執行者：Mac桌面版 Sonnet 5
> 上一棒：v59（名片系統首次部署，指定這場做雙通道傳輸）
> 本棒主軸：**這是一場超長對話（70+輪），四條主線都做完了：名片雙通道+換辨識引擎、Hook系統性稽核、Amber網頁方案評估、AI微型論壇網站從零到上線**

---

## 🎯 主線一：名片系統雙通道+辨識引擎大換血

### 1. Telegram/LINE雙通道傳輸（v59指定任務，已完成）
- `hooks/namecard-inbound/`：教練/孔大哥/佩佩老師傳照片+訊息含「名片」二字，自動複製進Amber名片媒合資料夾，**複製完當下直接觸發辨識**（事件驅動，非輪詢）
- `namecard-db/query.py`：小龍蝦/學弟/學妹查名片用的CLI，不用自己寫SQL
- 已在kong/peipei的`TOOLS.md`補上使用說明，三隻Bot共用同一份資料庫

### 2. 🔴🔴🔴 重大發現：MiniMax-M3辨識名片準確率太差，換成PaddleOCR
教練親自核對資料庫時抓到多筆錯誤（黃薇雅讀成黃鈺翔、洪美香讀成洪美智），其中一筆
（IMG_3779）**MiniMax不是讀錯字，是整張憑空捏造了一張不存在的名片**（真實內容是
「汰滅企業社／蔣世芳」除蟲公司，MiniMax編出「林棋祥／承昌鐵工廠」）。

**解法**：改成兩階段管線——`paddleocr_venv`（獨立Python 3.11環境，PaddlePaddle不支援
主環境3.14）本機跑PaddleOCR讀出乾淨文字，再交給MiniMax把文字整理成JSON欄位。
`namecard-db/paddle_extract.py`（PaddleOCR呼叫）+ `namecard-db/extract.py`（改造成
subprocess呼叫PaddleOCR取代直接看圖）。教練實測驗證：黃薇雅、李桂蘭、葉仁創、洪美香
全部讀對，準確率教練評「95%以上」。

⚠️ 免費OCR方案先試過Tesseract，實測完全不能用（真實環境照片有角度/背景雜訊，傳統OCR
讀出全是亂碼），才改用PaddleOCR。

### 3. 事件驅動 vs 輪詢（試金石案例49，教練第4次糾正同一個坑）
`--watch`常駐輪詢整個拿掉，`com.coach.namecard-watch.plist`移出LaunchAgents。
背景服務不再存在，Telegram/LINE路徑靠hook觸發即時處理；Amber App/電腦直接上傳這條路
沒有事件通知機制，改成教練說「整理名片」才觸發`watch_and_extract.py --once`。

---

## 🎯 主線二：Hook系統性稽核（重大系統性修復）

教練連續抓到3支Claude Code hook（rule07_polling_check.sh、rule_html_chrome_check.sh、
web_preview_verify_guard.sh）**寫好卻從未接進`~/.claude/settings.json`**，教練重話
「不要老是糊弄我」。稽核後發現`scripts/`目錄下共**23支**腳本宣告自己是Claude Code
hook，稽核前只有幾支真的被註冊，CLAUDE.md還記載著錯誤的「已註冊」資訊。

**已徹底解決**：新寫`scripts/audit_claude_hooks_registered.sh`，設成**SessionStart
hook**，每次開新session自動掃描比對，兩邊對不上就跳警告。全部22支（含稽核腳本自己）
已一次補進settings.json，逐一smoke test過。`web_preview_verify_guard.sh`也順手補上了
`ai-talk`這個新網站（之前漏掉）。

---

## 🎯 主線三：Amber私人雲網頁方案（評估後改用獨立方案）

教練想把`localhost:5050`名片查詢網頁放上雲端讓手機隨時能連。查證後發現Amber X**沒有
自訂Docker App**的能力（App商店只有Home Assistant/Plex/Zigbee2MQTT/Zwave JS UI四個
固定App，先前查到「支援自訂Docker」的資訊是錯的）。

**改用方案**：Mac上開一條**全新、獨立**的Cloudflare Tunnel（tunnel名`namecard-app`，
跟LINE小龍蝦專線那條完全分開、互不影響），`namecard.bymyway.com` → Mac本機的
`app.py`（已改成24小時常駐LaunchAgent：`com.coach.namecard-webapp.plist` +
`com.coach.namecard-tunnel.plist`）。已實測本機+公開網址都正常，資料庫18筆全部顯示。

---

## 🎯 主線四：AI微型論壇（ai-talk）網站從零到上線

### 部署
- **GitHub Pages**：`https://coach1973.github.io/ai-talk/`（教練指定的正典網址，
  案例47的markdown連結誤讀事件就是在釐清這個網址）
- **Netlify**：`https://ai-talk-tw.netlify.app`（教練指定命名規則`專案名-tw`，
  比照他原本想用的`bigtree-tw`風格；`ai-talk.netlify.app`已被全球其他用戶佔用）
- 兩邊內容已同步，最新commit `cfc8928`（GitHub）+ Netlify deploy_id `6a531b54`

### 新增功能（比照大樹小講bigtree的既有模式複製）
1. 固定導覽列，7個項目：五大主題／講師陣容／活動花絮／為什麼要參加／常見問答／
   贊助夥伴／立即報名（點擊平滑捲動到對應區塊）
2. 手機版漢堡選單 + 回到頂端按鈕
3. **精彩花絮輪播**（`images/carousel/photo-01~12.jpg`，完全比照bigtree的
   `carouselNext/Prev/Render`邏輯，自動4秒切換+手動按鈕，12張教練指定的過去講座照片）
4. Q&A手風琴（6題，點擊展開/收合）

### 內容修正
- 場地「安平維悅酒店」教練已確認正確，不用改
- 教練親口確認：所有新功能親自測試過正常運作

---

## 📋 下一棒待辦

| 優先 | 任務 |
|------|------|
| 🔴🔴 | **企業健身房（biz-gym）黑金改版——教練 2026-07-12 親口指示「必須持續提醒」，每一棒都要寫進接力棒，不准再漏**。現況：黑金版成品在 `~/github_repos/bigtree/biz-gym/index-new-blackgold.html`（7/4 完成、教練逐段看過），但 7/6 下午4:37 正式檔 `index.html` 被還原回米杏色舊版（與舊版備份逐字節相同，還原原因待查），目前本機+線上都是舊版。下一步：帶教練用 Chrome 預覽黑金版 → 教練親口說「推」→ 才恢復正式檔+上線 |
| ✅ | **QR code 活動報名系統（教練 2026-07-12 構想，已完整驗收上線）**：`event.bymyway.com`，架構同名片系統（Mac資料庫+獨立Cloudflare Tunnel）。完整流程：掃QR→填表→感謝頁「STEP1加LINE好友／STEP2一鍵傳問候」→系統比對身分→後台「發送通知」精準推播給參加過該活動的人。**全程真人真訊息端到端驗收成功**（教練親自掃碼、加好友、傳問候、收到測試通知，commit `1cbe530f5`）。LINE帳號用「大叔教練」`@qaw8118h`（不是小龍蝦`@268dptjc`，小龍蝦是私人助理頻道dmPolicy=pairing不對外）。原本接的Chatisfy已確認不用並拔線。**🔴🔴 重要踩坑記錄**：Webhook網址設對了、Channel Secret/Token都對，訊息還是收不到——真正原因是LINE Official Account Manager「設定→回應設定」頁面有一個獨立的「Webhook」開關，預設關閉，網址設定跟這個開關是兩件事，都要開才會真的送資料過來。3把鑰匙+這條踩坑記錄都存進`路徑大全.md`/`路徑大全_憑證層.md`（commit `e3bdadaaf`）。7/29 AI微型論壇活動已建好(slug: ai-talk-0729)，教練隨時可用 |
| 🟡 | 名片「needs_review」狀態那幾筆（AI信心較低）建議教練找時間人工抽查 |
| 🔴 | 2026-07-18：聯想C槽觀察期滿+2026-07-15佩佩電腦觀察期滿，兩邊都待教練確認後砍備份 |
| 🟡 | ACER軍師尚未回信確認JUNSHI_RULES.md規則#6（聯想已確認，ACER仍⏳） |
| ✅ | **名片系統自動化已修復到位（2026-07-13）**：①`paddle_extract.py`+`paddleocr_venv`兩個核心檔案曾經無聲消失（前者從未進git、後者只剩外殼），已重建並**這次真的commit了**（commit `6ad2fbf08`）②Amber資料夾直接上傳（非LINE/Telegram）**改成真正事件觸發**：新建`com.coach.namecard-amber-watch.plist`用launchd WatchPaths監控SMB網路資料夾，實測macOS對Amber掛載資料夾的變更通知真的有效（不是輪詢），教練不用再說「整理名片」。CLAUDE.md已同步更新（commit `a14917235`） |
| 🟡 | **佩佩老師的名片照片讀取問題（2026-07-13發現，待下次處理）**：佩佩手機是Amber私人雲的另一個帳號(johnpeggy0706@gmail.com)，她上傳的照片在她自己的私人家目錄，教練這邊讀不到、Amber也沒有「跨帳號共用資料夾」機制（右鍵選單只有複製/移動，沒有分享/建立捷徑）。**已定案方向**：改用Google硬碟——佩佩手機開「相機自動上傳」到Google硬碟資料夾，分享給教練的Google帳號，我方申請Google Drive API做即時監控（比Amber更正規，官方支援webhook）。**這是全新工程**，量級跟今天接LINE Channel Token相當，教練說「先記進待辦，下次再做」，下次開工要主動提起 |
| ✅ | **cool-case網站已同步到最新（2026-07-13）**：GitHub gh-pages分支比Netlify新（案例1~32 vs 舊版案例1~24），已zip+API推送同步，Netlify deploy_id `6a53db9538c928158473f3eb`，逐位元組驗證跟GitHub Pages完全一致 |
| ✅ | **cool-case案例33~40已正式上架，17篇原始案例全部處理完畢（2026-07-13）**：試金石_案例庫.md原案例33~49（17篇）已全數整理——15篇合併成8個網站經典案例，另外2篇（原33/35，VPS架構深度debug，技術含量高但敘事價值對外部讀者較低）教練認可「不選入」留在試金石庫內部參考。教練審過草稿後說「先上傳吧」。已推送兩邊：GitHub Pages commit `d4dcee0`、Netlify deploy_id `6a53f6b318f63574bb009623`，DOM層級驗證8案例文字/圖片/結構全部正確。網站現在共40個案例，跟試金石庫的進度差距已補齊 |
| 🔴 | **大樹AI作品一覽表兩個頁面（教練2026-07-12構想，個人頁已完成待教練驗收）**：①個人專用總覽頁**已完成**：`~/.openclaw/workspace/portfolio-private.html`，37個項目全編號分四類（公開11/保留1/私藏23/待啟用1），Chrome已開給教練看過，教練還沒回覆是否OK②**對外公開頁尚未做**：只放11個公開項目，走正式Netlify/GitHub部署，等教練確認個人頁排版後才做③教練確認goeasy-ai不該被封存（已解封並修正記憶檔） |
| 🟡 | **教練在找一個「CLAUDE」圓形頭像圖案（2026-07-13，下次教練會主動告知資料位置）**：教練記得之前對話裡設計過一個AI專用、裡面寫著CLAUDE字樣的圓形頭像，現在對話中只看到自己的頭像、AI的不見了。**已查證cool-case repo（main+gh-pages兩分支全部歷史）完全沒有這個檔案存在過**——從頭到尾圖片資產只有`coach-avatar.jpg`/`xiaolongxia-avatar.jpg`/`wu-badge.png`/`analysis-badge.jpg`，逐字搜尋所有commit內容"claude"字樣也只出現在案例故事內文提到Claude Desktop工具名稱、或git的Co-Authored-By紀錄，兩者都跟頭像設計無關。教練說下一輪會主動告訴軍師資料實際在哪裡，下次開工要接著查，不要重新從cool-case找（已查過沒有） |

---

## 🔑 關鍵檔案索引（本場新增/修改）

- `namecard-db/paddle_extract.py`（新建，PaddleOCR呼叫腳本）
- `namecard-db/extract.py`（改造為兩階段管線）
- `namecard-db/paddleocr_venv/`（新建，獨立Python 3.11環境）
- `namecard-db/watch_and_extract.py`（拿掉--watch常駐模式）
- `hooks/namecard-inbound/handler.js`（加入複製完當下觸發辨識）
- `scripts/audit_claude_hooks_registered.sh`（新建，SessionStart稽核腳本）
- `~/.claude/settings.json`（22支hook全部補齊註冊）
- `~/.cloudflared/namecard-config.yml` + 兩個新LaunchAgent（namecard-webapp、namecard-tunnel）
- `~/github_repos/ai-talk/`（整個網站大改版，含images/carousel/）

---

> Mac桌面版 Sonnet 5 親筆，2026-07-12下午2點。教練說「總結上傳，開啟新的對話」，
> 本棒收尾。這是一場橫跨名片系統辨識引擎大換血、系統性hook稽核修復、網站部署架構
> 決策、實際網站功能開發的紮實長對話，過程中教練多次當場抓到問題（MiniMax幻覺捏造
> 名片、hook沒真的裝上、Amber能力誤判），每次都查證後老實修正，沒有含糊帶過。
> 下一棒開工先讀上面「下一棒待辦」，名片系統已經是穩定可用狀態，網站也都上線了。
