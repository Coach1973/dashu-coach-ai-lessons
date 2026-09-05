# 軍師接力棒 · 2026-09-04 v181（Mac終端機 Sonnet 5，大臺南商圈整合計劃店家登錄頁上線+五項待辦決議收尾）

> 建立時間：2026-09-04 22:12 ~ 22:35（台灣時間）
> 上一棒：v180（Mac終端機，seabiscuit20媒體報導補齊20篇+全面盤點報告+新增「關於創辦人」頁面）
> 本棒主軸：**教練一口氣裁示v180留下的5項待辦；新任務：把下載資料夾裡的`tainan-shangquan.zip`（大台南策展中心店家招募落地頁）建成GitHub repo+接上event-signup後端DB+Telegram通知，比照1010/tut既有模式，已用真實POST測試驗證。**

## 🎯 本場戰果

### 1. 大臺南商圈整合計劃店家登錄頁上線（新任務）
教練提供`~/Downloads/tainan-shangquan.zip`（大台南策展中心委託，免費幫店家開通乾淨世界頻道+建置形象網站+AI行銷工具，店家填表登錄）。原始表單只是純前端假送出(隱藏表單+顯示感謝文字，零資料落地)。已建新repo`Coach1973/tainan-shangquan`(commit`c0f5180`)，`handleShopSubmit()`改`fetch()` POST `event.bymyway.com/api/tainan-shangquan/join`。後端比照1010/tut既有模式：`event-signup/schema.sql`新增`tainan_shangquan_signups`表(姓名/店名/類別/聯絡方式/地址/社群/招牌商品)，`app.py`新增路由(GET靜態頁+POST寫DB+推播「活動報名即時通知」Telegram群組)，commit`d1b02db49`。已用真實POST測試驗證DB寫入正確，測試資料已清除。

### 2. v180五項待辦教練當場裁示，四項已落實
①coach888編輯同步方案選「已同步狀態指示燈」(非手動上傳按鈕)：`syncStateToServer()`成功/失敗跳toast，commit`309f2fd`，GitHub Pages curl驗證已生效。②「後台系統帳密集中」存放位置定案：教練口頭裁示存Mac本機、教練直接問小龍蝦，已寫入記憶但**實際清單尚未彙整**，且小龍蝦工具權限受限的技術細節待下次確認，詳見待辦表。③`true-ai-team`repo補GitHub遠端：新建private repo`Coach1973/true-ai-team`並推送。④materials教材公開：教練說「等我忙完」，不動。⑤bigtree黑金改版草稿殘留：6份比稿檔+2份備份檔搬進`biz-gym/_archive_blackgold_draft_2026-09-04/`，commit`2d96eac`(本機Chrome預覽確認`index.html`未引用這些檔案後才推送)。

## ⚠️ 本場教訓/發現
1. **`web_preview_verify_guard.sh`會攔bigtree的push，即使改動只是搬移未被引用的草稿檔、零視覺影響**——仍照SOP開本機http.server+Chrome預覽一次留下證據再推送，沒有為了「反正沒差」跳過鎖。

## 🔑 本場commit
`tainan-shangquan`：`c0f5180`(初版)。`true-ai-team`：已補遠端(無新commit，純推送既有3筆歷史commit)。`bigtree`：`2d96eac`(黑金改版草稿歸檔)。`coach888`：`309f2fd`(已同步toast)。`workspace`：`d1b02db49`(tainan-shangquan後端路由)。

---

# 軍師接力棒 · 2026-09-05 v182（Mac終端機 Sonnet 5，KR養生廚房整站搬遷+bigtree活動網頁按鈕修正+seabiscuit20影片按鈕+coach888收錄鎖上線）

> 建立時間：2026-09-04 22:35 ~ 2026-09-05 03:07（台灣時間，跨日）
> 上一棒：v181（Mac終端機，大臺南商圈整合計劃店家登錄頁上線+五項待辦決議收尾）
> 本棒主軸：**教練指出「我要看活動網頁」按鈕誤放seabiscuit20，補在bigtree真正6場+發現DB即時渲染會覆寫靜態HTML的關鍵架構問題；教練用Tooo.ai demo3.tooo.ai做的KR養生廚房示範站整站搬遷上線；教練回報seabiscuit20影片「不見了」，查證其實是藏在完整守則彈窗裡沒有獨立入口，新增「看守則影片」按鈕；教練要求新公開網站一律收錄coach888不要再提醒，做成Stop hook規則L強制檢查。**

## 🎯 本場戰果

### 1. bigtree「我要看活動網頁」按鈕補正+events表新增event_url欄位
教練澄清這顆按鈕本來要放大樹小講，誤放到海餅乾20週年（教練說做得好不改動那邊）。補在bigtree真正6場：9/16高雄(ai-art)、9/22台南下午(ai-talk)、9/22台南晚上(ai-fit)、9/23-24台中x2(ai-forum)。**關鍵發現**：`event.bymyway.com/bigtree/`是DB即時渲染，`render_session_dates()`每次請求都會整段覆寫靜態HTML的SESSION_DATES陣列，只改bigtree repo原始碼沒有用（下次一鍵發佈也會被DB內容蓋掉）。已在`events`表新增`event_url`欄位當唯一真相源，`db.py`+`bigtree_publish.py`同步更新，已用真實curl驗證正式站四個網址正確渲染。同場也把`tainan-shangquan`電話改成佩佩老師0988-004-118。commit`aaedd85`(bigtree)+`cef1657`(tainan-shangquan)+`622e2ab8c`(event-signup)。

### 2. KR養生廚房官網整站搬遷上線（新任務）
教練提供`https://demo3.tooo.ai/11883/518v3/`（Tooo.ai AI建站工具做的示範站，即bigtree的9/5場地KR養生廚房）要求原封不動搬到`event.bymyway.com/KR/`。8個頁面(首頁/關於我們/餐點特色/藝文空間/聯絡我們/隱私權/服務條款/無障礙聲明)+11張圖片+main.js全部下載，路徑改寫成`/KR/`前綴，移除Tooo.ai自家追蹤腳本(demo-chk.js/report.js/cloudflare beacon)+浮水印。**聯絡表單原本打Tooo.ai自己的`api.tooo.ai/widgets/form-submit.js`**，改推我們自己的`/api/KR/contact`端點(DB+Telegram「活動報名即時通知」群組)，避免搬過來後訊息送到教練管不到的第三方帳號。`_serve_repo_file()`新增資料夾`/index.html`fallback支援多頁面靜態站(不影響既有單頁站行為)。已用真實瀏覽器UI送出表單+curl驗證8頁面200+DB寫入正確。新repo`Coach1973/KR`，commit`c0f5180`類似模式(KR repo初版)+`2cf7615f1`(event-signup後端)。

### 3. seabiscuit20「看守則影片」獨立按鈕上線
教練問「兩支影片怎麼不見了」，查證發現影片其實從未被刪除——9/4下午聯想新增「完整守則」彈窗時，就把影片放在彈窗裡面，只是沒有獨立入口，滑頁面看不到。已用JS狀態檢查(`openRulesModal()`+`performance.getEntriesByType('resource')`確認YouTube iframe真的載入)驗證後，在「✦完整守則✦」旁新增「▶看守則影片▶」獨立按鈕+獨立彈窗(videos-modal)，影片從rules-modal搬移過去(非複製)。commit`d4bffd7`。**本場一次Stop hook攔截**：改完HTML用Claude Browser工具驗證過畫面但沒有實際執行`open -a "Google Chrome"`，被規則J擋下收工，補跑Chrome開啟後才算完成，已寫入記憶`feedback_html_preview_chrome_only`（發現同名記憶檔已存在於MEMORY.md索引但實體檔案遺失，本場補回）。

### 4. coach888收錄鎖：Stop hook規則L上線
教練連續第二次發現新網站(tainan-shangquan、KR)沒放進coach888作品一覽，當場要求「請寫入SOP...不要再讓我提醒」。純文字SOP評估後判定不夠可靠，改成`stop_rules_master.py`新增規則L(deterministic check)：只要對話裡執行過`gh repo create ... --public`，Stop hook自動掃描該repo名稱是否出現在本機`coach888/index.html`，沒有就擋下收工。只認`--public`，不會誤攔`--private`備份repo(如`true-ai-team`)。已用合成transcript測試正反兩案例驗證邏輯正確，commit`c048eaf0d`。**上線當天發生一次假陽性**：heredoc造測試transcript的文字本身被記進真實對話，下一輪Stop hook誤把假repo名字當真的執行過，已修法排除heredoc定界符內容，教訓寫入記憶。KR/tainan-shangquan兩站已依此規則補進coach888，commit`cb30fe2`。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **event.bymyway.com/bigtree/是DB即時渲染，改bigtree repo原始碼裡的資料不會生效**——任何要改場次相關內容(含新按鈕需要的資料)都要往`events`表加欄位，不能只改靜態HTML。
2. **改完HTML用Claude Browser系列工具做過完整功能驗證，不能取代`open -a "Google Chrome"`**——兩者是互補不是替代，收工前這一步不能省，記憶`feedback_html_preview_chrome_only`。
3. **coach888收錄不能只靠記住，要做成deterministic hook**——同一天連續兩次疏漏後才被逼出這條鎖，早該在v179第一次疏漏後就做。
4. **合成假transcript測試hook時，heredoc本身的文字內容會被同一份真實transcript的其他規則掃到**，導致非預期誤判，測試完要檢查有沒有引發旁支問題。

## 🔑 本場commit
`bigtree`：`aaedd85`(6場活動網頁按鈕)。`tainan-shangquan`：`cef1657`(電話修改)。`event-signup`：`622e2ab8c`(bigtree event_url欄位)+`2cf7615f1`(KR路由+聯絡表單)+`c048eaf0d`(Stop hook規則L)。`KR`：初版(GitHub repo `Coach1973/KR`)。`coach888`：`cb30fe2`(KR收錄)。`seabiscuit20`：`d4bffd7`(看守則影片按鈕)。記憶庫(`.claude/projects`)：`feedback_new_public_site_must_register_coach888_2026-09-04`+`feedback_html_preview_chrome_only`(補回)+`project_backend_credentials_consolidation_pending_2026-09-04`(補回)。
