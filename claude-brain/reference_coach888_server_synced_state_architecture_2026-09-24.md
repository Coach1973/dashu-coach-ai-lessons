---
name: reference-coach888-server-synced-state-architecture
description: coach888(大樹AI作品總覽)的實際顯示內容以/api/coach888/state伺服器狀態為準，不是git的index.html靜態內容——分類標題/順序/項目位置都可能被教練在線上即時改過，只查git會查到過時資訊；另外這個repo的gongkai分類混雜新舊兩種item HTML模板，插入新項目時用字串比對容易切壞既有項目結構；呼叫其API要帶瀏覽器User-Agent否則被Cloudflare擋
metadata:
  node_type: memory
  type: reference
  originSessionId: e4206935-cdda-4d24-bc42-eb03d1c6cfe3
  modified: 2026-09-23T17:22:58.157Z
---

# coach888 技術架構：伺服器同步狀態 > 靜態 HTML，動手前一定要先查即時狀態

## 核心事實（2026-09-24 查證確認）

`coach888`（`github_repos/coach888`，部署在 `coach1973.github.io/coach888/`）**不是純靜態頁面**。它有一套跨裝置同步機制（2026-09-03交辦），把教練在瀏覽器上即時編輯的排版（分類標題改名、項目順序、新增/刪除分類）存到後端：

```
GET/POST https://event.bymyway.com/api/coach888/state
```

儲存的 7 個 key：`coach888_layout`（各分類項目URL順序）、`coach888_titles`（分類標題override）、`coach888_badges`、`coach888_names`、`coach888_collapse`、`coach888_sections`（自訂分類清單）、`coach888_section_order`（分類顯示順序）。每個 key 的 value 本身又是一層 JSON 字串（要 `json.loads` 兩次）。

**這代表**：git 裡 `index.html` 寫的分類標題（例如 `data-section="gongkai"` 底下 `<span class="title-text">對外公開</span>`）只是**首次載入前的靜態基準**，教練若已經在瀏覽器把它改名成別的（實測案例：`gongkai` 被教練改名成「netlify代表作」），**JS 載入時會用伺服器狀態覆蓋掉靜態文字**。只看 git 原始碼會查到教練已經不在用的舊名稱，回報教練時就會像[[feedback_sop_must_alias_spoken_trigger_phrase_2026-09-24]]提到的案例一樣講錯話讓教練聽不懂。

## How to apply：動手改 coach888 前

1. **先查即時狀態，不要只看 git**：
   ```bash
   curl -s "https://event.bymyway.com/api/coach888/state" -H "User-Agent: Mozilla/5.0" | python3 -m json.tool
   ```
   分類的真實標題看 `coach888_titles`，真實項目順序看 `coach888_layout`，`data-section` 的 key（如`gongkai`）才是永久識別碼，標題文字可能早就被教練改掉。
2. **要新增/搬動項目，同時改兩邊**：git 的 `index.html`（給第一次載入的訪客/爬蟲看，也是沒有JS時的降級內容）+ 用 POST 更新伺服器狀態（給教練/任何裝置實際看到的內容）。只改一邊會造成「我改了但教練看不到」或「教練看到的跟git記錄的不一樣」。
3. **POST 呼叫必須帶瀏覽器 User-Agent**：Cloudflare 會擋掉 Python `urllib` 預設 UA 的請求（回 403 Forbidden），要用 `curl -H "User-Agent: Mozilla/5.0" -H "Origin: https://coach1973.github.io"` 或帶等效 header 才能通過。這個端點本身（Flask層）沒有任何驗證機制，403 完全是 Cloudflare WAF 層擋的，不是程式碼權限問題。

## 陷阱：這個 repo 混雜新舊兩種 item HTML 模板

`gongkai`（現稱「netlify代表作」）分類混了：
- **舊模板**（較早期項目，如「AI人才檢索提案」）：`<div class="item" data-cat="gongkai"><a href="..."><div class="thumb">...</div><div class="meta">...</div></a></div>`
- **新模板**（2026-09後新增項目）：單行 `<div class="item" data-url="..."><span class="drag-handle">...</span>...<span class="item-del">✕</span></div>`

2026-09-24 案例：Hermes 新增《造林》項目時，用「找第一個 `<div class="item"` 字串出現的位置」插入，結果真的插進舊模板項目自己的 `<a>` 標籤內部（切在 `<div class="thumb">` 跟 `<div class="meta">` 中間），把那個項目的 HTML 結構切斷，教練回報「看不到最新作品」正是這個原因。已修復見 [[feedback_sop_must_alias_spoken_trigger_phrase_2026-09-24]]。

**往後插入新項目前**：先確認要插入的分類裡有沒有混用舊模板（`data-cat=` 屬性），插入位置要對準 `<div class="grid" data-section="...">` 這個開頭標籤本身，不要用「第一個 item」這種容易誤判的相對定位。插入後務必核對 `<div>`/`</div>`、`<a>`/`</a>` 標籤數量平衡，不平衡代表切壞了東西。

## 另一個獨立機制：熱門排行榜

`熱門排行`（🔥 Hot Ranking）**完全獨立於 layout/section 系統之外**，純靠點擊次數（`/api/coach888/click`累加、`/api/coach888/click-counts`讀取）自動排序前10名，不進 `saveLayout()` 的 `.grid`/`.item` 掃描範圍。2026-09-24前完全沒有刪除機制（活動結束也退不了榜），已新增 `DELETE /api/coach888/click-counts`（帶 `{"url":...}` body）+ 前端每筆的✕鈕解決。

## 相關
- [[feedback_sop_must_alias_spoken_trigger_phrase_2026-09-24]]（這次架構誤解導致的實際事故案例）

**2026-10-05 16:45 教練要「同一個作品重複放在最新作品」**：coach888 頁面同一個網址只會顯示在一個分類——伺服器 layout 寫兩個分類都有，畫面只留最後讀到的那個（團隊系列從 11 項掉成 10 項），頁面一存檔還會把另一邊洗掉。**要重複放，第二個必須是不同的網址字串**：信任遊戲＝團隊系列放 `https://trust.bymyway.com/game/`、最新作品放 `https://trust.bymyway.com/`（首頁 302 轉到 /game/，打開是同一頁）；items 兩個網址各一筆。寫入只 POST `coach888_layout`＋`coach888_items` 兩個 key，其餘不動；寫完用真瀏覽器開 coach1973.github.io/coach888/ 數兩區項數核對。`curation_process.register_coach888` 是「搬」（會先從其他分類移除），不能拿來做重複放。
