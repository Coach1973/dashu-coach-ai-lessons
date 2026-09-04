# 軍師接力棒 · 2026-09-04 v179（Mac終端機 Sonnet 5，seabiscuit20部署四項調整+coach888作品一覽補漏+兩輪真bug修復）

> 建立時間：2026-09-04 05:41 ~ 19:14（台灣時間）
> 上一棒：v178（聯想Windows，seabiscuit20六項新功能：時光足跡/見證/語錄/完整守則/頁尾連結）
> 本棒主軸：**海餅乾20週年官網部署event.bymyway.com/seabiscuit20+教練交辦四項調整全數完成；教練問「最近做的網頁都有放作品一覽嗎」，查證發現7新站+1後台工具全漏，補齊coach888；教練回報coach888批量搬移下拉選單bug，查證根因是自訂分類從未持久化，修復並發現連帶的伺服器白名單漏洞；教練緊接著要求拿掉分類數字編號+新增大分類拖曳排序，兩輪修復都完整測試驗證；教練指出AI把本機測試分頁誤留給他操作、白忙一場，已修正流程並清空Browser pane殘留分頁；教練提議「本機編輯+上傳按鈕」，已給出不建議理由+替代方案，待教練回覆。**

## 🎯 本場戰果

### 1. seabiscuit20部署上線+教練交辦四項調整
新增`/seabiscuit20/`路由(比照DIY/Leadership等既有repo-served模式)，commit`9fe942ef9`。教練交辦四項：①footer「快速連結」加乾淨世界頻道+FB官方，「聯繫方式」精簡留LINE@官方+電子信箱(9處重複footer同步)②ai-fit(9/22台南場)拿掉午半場只留晚間場，因下午已獨立成AI微論壇③大樹小講「媒體報導」14則新聞移植，新增頁首導覽「媒體報導」④首頁新增「近期場次」按鈕區塊，4張卡片各配「我要報名這場」+「我要看活動網頁」，9/16場次到期自動隱藏。commit：seabiscuit20`b122a7b`、ai-fit`0bcba27`、workspace`9fe942ef9`。**查證確認與聯想Windows同時段平行處理同一repo無衝突**，git log乾淨、nav10頁面正確整合。

### 2. coach888作品一覽補漏：7新站+1後台工具
教練詢問近期網頁是否都有放進作品一覽，逐一查證正式站原始碼後發現海餅乾20週年/淺山綠1010/結繩DIY三版/結繩領導學/leader報名頁+教材線上觀看後台，共8項全部漏放。補進「大樹常用」1~7項+「後臺系統」1項，commit`752d71c`。

### 3. coach888真bug修復（兩輪）
**第一輪**：教練回報新增分類後批量搬移下拉選單找不到剛建的分類，查證根因遠比表面症狀嚴重——`➕新增分類`建出來的分類從未存進任何地方(不是localStorage結構/伺服器/原始HTML)，重新整理或換裝置就整個消失。新增`SECTIONS_KEY`持久化+跨裝置同步，commit`dd8e4eb`；同時發現伺服器`COACH888_STATE_KEYS`白名單漏加新key(前端存了、伺服器靜默丟棄不報錯)，補上並重啟服務，commit`963050103`。**第二輪**：教練追加拿掉分類數字編號(一、二、三...，最近刪除的🗑保留)+讓大分類本身也能拖曳排序(收合/展開皆可)，新增`section-drag-handle`+`SECTION_ORDER_KEY`，跟item拖曳同一套mousedown/mousemove/mouseup機制，commit`2cd3a31`(前端)+`f81e14678`(伺服器白名單，這次同一輪一起補，記取上次教訓)。兩輪都用真實模擬測試(新增/下拉選單/reload持久化/跨裝置同步/刪除)驗證，測試資料清乾淨未污染正式站。

### 4. 本機預覽誤導教練流程問題修正
教練回報「我剛才在你跳出來的本機頁面下改了一大堆東西...根本沒有同步到雲端正式網址上，等於白忙一場」「我已經好幾次做白工了」。已清空Browser pane所有殘留本機測試分頁(`tabs_close`關閉4個`file://`/`http://127.0.0.1`分頁)，往後只給正式網址、不留本機測試畫面在畫面上。教練接著提議「本機編輯+上傳按鈕」架構，已回覆技術建議：不建議純手動上傳(忘記按=work全丟，比現在的自動即存更危險)，改建議加「✅已同步」狀態小提示，教練尚未回覆選哪個方案。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. **Browser pane本機測試分頁絕不能留給教練看到/誤用**，收工前務必`tabs_close`清空，只給正式網址，不讓教練誤以為本機測試版就是正式站。記憶`feedback_never_expose_local_preview_to_coach_2026-09-04`。
2. **coach888新增同步key要前端陣列+後端`COACH888_STATE_KEYS`白名單同一輪一起改**，同場連踩兩次同款坑，前端完全不報錯，只有curl查伺服器實際回傳才看得出漏加。記憶`reference_coach888_sync_key_whitelist_pattern_2026-09-04`。
3. Browser pane背景/隱藏狀態下的分頁`window.innerWidth`會是0，`getBoundingClientRect`/`elementFromPoint`等像素幾何API全部失真——測試需要真實版面尺寸的互動(如拖曳排序)時，要front該分頁或改用不依賴幾何座標的替代驗證方式。
4. 教練提出的方案不一定是最佳解——他說「如果不行的話就算了」是誠心徵詢技術意見，此時該給誠實建議+替代方案，不是照單全收動手做。

## 📋 下一場開工先做
1. **coach888「已同步」狀態指示器 vs 手動上傳按鈕**，教練尚未回覆選哪個，開工先問。
2. 「後台系統帳密集中」任務：教練確認是coach888沒錯，但帳密存放位置的AskUserQuestion教練還沒回覆(中途轉向seabiscuit20)，下次開工先追問。記憶`project_backend_credentials_consolidation_pending_2026-09-04`。
3. 沿用v174/v178舊待辦：`/materials/admin`教練待自己勾選公開項目、DIY3的LINE連結已補上(本場確認)、v177記憶體洩漏是否已排除待確認。

## 🔑 本場commit
`seabiscuit20`：`b122a7b`。`ai-fit`：`0bcba27`。`diy-studio-workshop`：`daed332`(LINE連結)。`coach888`：`752d71c`(補漏8項)、`dd8e4eb`(分類持久化)、`2cd3a31`(拖曳排序+移除編號)。`workspace`：`9fe942ef9`(seabiscuit20路由)、`963050103`+`f81e14678`(伺服器白名單)、若干心跳/健康檢查常態同步commit。記憶：`feedback_never_expose_local_preview_to_coach_2026-09-04`+`reference_coach888_sync_key_whitelist_pattern_2026-09-04`。

---

