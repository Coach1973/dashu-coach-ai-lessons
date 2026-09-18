# 軍師接力棒 · 2026-09-18 v219（Mac桌面版 Sonnet 5，手機/軍師討論邊界+Netlify中文檔名修復部署+後台帳密清單結案+workspace git大掃除(含金鑰外洩發現)+coach888「熱門排行」新功能）

> 建立時間：2026-09-18 19:25 ~ 22:48（台灣時間，約3.4小時）
> 上一棒：v218
> 本棒主軸：**教練發現手機(MiniMax)跟桌面版同時開新對話框讀到同一份接力棒，會把留給軍師的討論題目搶答掉，要求做出區隔；同時針對v218留下的3項待辦明確裁示「不要再問，直接做」。逐項執行完畢後，教練委託新任務：coach888作品一覽依點擊次數做即時熱門排行。**

## 🎯 本場戰果

### 1. 手機(MiniMax)不再搶答軍師專屬討論題目
接力棒待辦表新增「💬」狀態代碼；`feed_junshi_handoff.sh`偵測到`IS_MOBILE=1`時，額外注入明確指令：看到💬項目完全略過，不搶答不主動提，只做🔒/⏳/✅/⚠️這幾類任務。已模擬手機/桌面兩種身份(靠`ANTHROPIC_BASE_URL`/`ANTHROPIC_API_KEY`是否清空判斷)測試通過，確認新指令只出現在手機分支。

### 2. 大樹小講10/3場Netlify部署（v218遺留待辦，教練裁示「去改不要問」）
根因：`archive/大樹小講_歷史講座紀錄.html`+一個孤兒資料夾`archive/2026-07-01_創業x政府xAI講座/`共5個中文檔名，Netlify zip deploy API不接受非ASCII檔名。已`git mv`改成`archive/lecture-history.html`等英文命名，3個html檔案的連結同步修正，本機http.server+真實Chrome驗證後推GitHub、部署Netlify。正式站已curl驗證10/3內容、EDM圖片、`/archive/lecture-history`clean URL全部200。

### 3. 後台系統帳密集中清單（v218遺留待辦，教練裁示「彙整就是了」）
查證發現其實09/05~06就已彙整進`路徑大全_憑證層.md`(13組系統)，是一筆沒被關掉的過期待辦。補上真缺口(`event.bymyway.com/vault`漏收錄)、確認教練本人問小龍蝦時`toolsBySender`無限制、`SOUL.md`補上明確讀取路由指引(原本完全沒告訴小龍蝦要去哪查)。

### 4. workspace repo git狀態大掃除（v218遺留待辦，教練裁示「清理就是了」）
救回被doctor --fix/schema遷移又清空一次的`TOOLS.md`+兩個`workspace-state.json`(內容與HEAD一致)；`.gitignore`補齊`*.migrated.*`/全域`__pycache__`/產業鍊SOP生圖產物/FB調查暫存log+截圖/`event-signup/static_tmp/`/`project_card_injected`dedup標記/危險指令通行證`state/DELETE_APPROVED`共7類規則；補commit過去10天累積但從未落地的50+個檔案(記憶檔/跨機收信/對話蒸餾檔)。**意外發現**：3個檔案(`state/inbound_echo/2026-09-12.jsonl`+2份對話蒸餾檔)原封不動含一組Telegram bot token跟**當晚才剛用來部署bigtree的Netlify token**，已故意不commit這3個檔案+寫入記憶`feedback_distilled_and_echo_logs_can_leak_live_secrets_2026-09-18`回報教練，**教練裁示「不用管」，接受風險維持現狀**（比照小二token外洩舊判例）。

### 5. coach888新增「🔥熱門排行」：依點擊次數即時排名
教練需求：作品一覽項目愈來愈多，想依實際點擊次數自動排出常用項目，不用每次在分類裡找來找去。實作：`event-signup`新增`coach888_clicks`表+兩支端點(`POST /api/coach888/click`累加、`GET /api/coach888/click-counts`回傳全部計數)，coach888前端用`navigator.sendBeacon`在每次點項目連結時記一次，頁面最上方新增獨立區塊即時渲染前10名。**架構刻意跟既有15個分類的排版/拖曳/存檔機制完全隔離**——新區塊用`.hot-item`/`.hot-grid`全新class名稱，不進`saveLayout()`的`.grid`/`.item`掃描範圍，不會污染`coach888_layout`狀態、不會被拖曳/刪除功能誤綁定，原本手動整理的分類完全不受影響。**過程修一個真bug**：`navigator.sendBeacon`的請求帶`credentials:'include'`，CORS規範禁止搭配萬用字元`Access-Control-Allow-Origin: *`、且必須明確回`Allow-Credentials: true`，兩個條件都補上後才真正送得出去(本機用真實Chrome點擊+production API驗證兩輪才抓全，過程詳見新增記憶`reference_sendbeacon_cors_credentials_gotcha_2026-09-18`)。已端到端測試：點擊→POST寫入→重新整理→熱門排行正確顯示排名+次數，測試資料已清除，正式站GitHub Pages已curl驗證部署生效。

## ⚠️ 本場教訓/發現（已寫入記憶）
1. `feedback_distilled_and_echo_logs_can_leak_live_secrets_2026-09-18`：`terminal-notes/distilled/`跟`state/inbound_echo/`這類「已加工過」的衍生檔案，仍可能原封不動含真實API Key/Token，commit前要單獨掃描，不能假設蒸餾過程會自動遮蔽。
2. `reference_sendbeacon_cors_credentials_gotcha_2026-09-18`：`navigator.sendBeacon`跨網域請求會帶`credentials:'include'`，伺服器CORS設定若用萬用字元`*`或漏掉`Allow-Credentials:true`，請求會被瀏覽器整個擋下且不易察覺(beacon是fire-and-forget，不會有明顯的失敗提示，只能查console或直接驗證後端有沒有收到)。

## 📋 下一場開工先做
1. **💬軍師專屬討論題目仍未處理**：試金石案例庫商業化/資產化路徑，本場教練把時間都用在裁示執行任務+coach888新功能，這個話題還沒真的展開討論，下一場看到接力棒待辦表的💬項目應主動提起。
2. 沿用v218既有待辦：孔大哥/佩佩老師industry-chain-sop hook真人實測(教練不催)、peipei-ai-backup舊commit金鑰歷史(教練已表態不處理)、`stop_rules_master.py`規則#07誤判regex(教練示意MiniMax有空自行補丁)。
3. E16接力棒瘦身：本場已完成，v216已搬進`handoff_archive/handoff_v216_archived_2026-09-18.md`，主檔現維持v217~v219共3棒。

## 🔑 本場commit
`workspace`：`22252989c`(手機軍師討論過濾+帳密清單補完)、`3df65360b`(.gitignore補齊+例行狀態同步)、`577281fbc`(補commit50個記憶/收信/蒸餾檔)、`4d37bc428`(補commit中文檔名收信紀錄)、`5bf14310f`(coach888點擊計數後端API)。`github_repos/bigtree`：`549fa9c`(中文檔名改ASCII)，Netlify deploy`6aad2282`。`github_repos/coach888`：`22fc17b`(熱門排行前端)。

---

