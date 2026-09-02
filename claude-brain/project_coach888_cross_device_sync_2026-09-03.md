---
name: project-coach888-cross-device-sync-2026-09-03
description: coach888作品一覽排版狀態改伺服器集中同步(event.bymyway.com/api/coach888/state)，取代單一瀏覽器localStorage各自為政，解決Mac改完ACER看不到的問題
metadata:
  node_type: memory
  type: project
  originSessionId: fa97ce20-02cc-40c2-aaad-1ba7f3961669
  modified: 2026-09-03T06:06:00.000Z
---

教練直接點出我先前的「救回排版」只是治標：「有解決我提出的嗎？例如，我在MAC電腦改完排版，在ACER電腦上卻看到舊的，能即時更新排版嗎？」——這才是根本問題，不是「救回一次意外清空」。

**Why：** coach888（GitHub Pages純靜態站）原本5組編輯狀態（layout排序/titles標題/badges標籤/names顯示名稱/collapse收合）全部只存在單一瀏覽器的localStorage，跨裝置完全不同步，要同步只能靠手動「複製目前排序」按鈕貼給AI固化進正式檔案——這條路徑教練不會主動想到要做，也容易忘記。

**做法：** 在`event-signup`（已有CORS開放API先例，如`/api/register`、`/api/tut/join`）新增`coach888_state`資料表+`/api/coach888/state`端點（GET回傳5組狀態、POST依key更新）。coach888既有的`saveLayout()`/`saveTitles()`/`saveBadges()`/`saveNames()`/`saveCollapse()`五支函式寫完localStorage後，debounce 400ms推一次到伺服器；頁面載入先用localStorage/預設HTML快速畫面，背景同時拉伺服器最新值，拉到後重新套用並`renumber()`校正編號。伺服器連不上時整套退回原本純localStorage行為，不影響離線可用性。

**已用真實跨瀏覽器測試驗證**（非僅程式碼審查）：在教練實際Chrome收合「最近刪除」分類→伺服器`coach888_state`表確認`recentlydeleted:true`→用完全獨立、從未載入過此頁的瀏覽器context清空localStorage後載入→1.5秒內正確顯示收合狀態。證實跨裝置即時同步真的成立。

commit：coach888 repo `9a23f8f`；workspace `event-signup/app.py`+`schema.sql`（新增`coach888_state`表+路由）。

**這個模式可複用**：任何「純靜態GitHub Pages + localStorage編輯」的教練專案，若之後也出現跨裝置不同步的抱怨，可直接套用同一套做法——掛在已有CORS-open API的既有Flask app（event-signup或namecard-db）底下，不用新增獨立後端。

Related: [[feedback_never_clear_user_storage_without_backup_2026-09-03]]（同一起事件的另一面：清空前要先備份）
