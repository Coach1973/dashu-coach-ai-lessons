# 雲端工作單：調好「網頁交付前自檢」程式（2026-11-04 Mac 軍師寫）

> 給雲端 Claude 讀。你沒有 Mac 的 hook 與守則注入，這份就是全部背景。
> 回報一律用繁體中文、白話（教練不是工程師）。

## 為什麼要做
這週教練一直在幫 AI 抓網頁錯誤（字看不清、表頭捲下去不見、圖太大）。光寫規則提醒沒用，要變成程式：交付前跑一次，有紅燈就不准交。程式已寫了一半：`workspace/scripts/page_preflight.js`（本資料夾有一份快照 `page_preflight_snapshot.js`）。

## 卡在哪
同一頁「修好前」和「修好後」，程式都報 28～50 處紅燈，分不出好壞＝誤報太多，沒法用。

## 測試資料（都在本資料夾）
- `before_fix.html`：修好前。第六章「日出」那段字壓在亮色漸層上，對比只有 1.0～1.6，**必須被抓到（🔴）**。
- `after_fix.html`：修好後（加了暗幕，對比 5 以上），這一段**必須不報**。
- `images/`：兩頁用到的圖。

## 要做到（完成標準）
1. 本資料夾開一個本機伺服器（`python3 -m http.server 8791`，**不要用 8765**），對兩頁跑：
   `node page_preflight_snapshot.js http://localhost:8791/before_fix.html`
2. 修好前：日出段標題／內文出現在紅燈清單。修好後：紅燈 0～3 處以內，且日出段不在裡面。
3. 程式裡的 Chrome 路徑是 Mac 寫死的（`/Applications/Google Chrome.app/...`），雲端要改成「有就用、沒有就用 playwright 內建 chromium」，兩邊都能跑。
4. 誤報常見來源（先查這幾個）：按鈕／標籤底色是半透明、父層才有底色；文字在 `::before` 漸層上；字被藏起來後截圖前沒等重繪；取樣點落在字外框的空白邊。
5. 調好後把改好的程式寫回 `workspace/scripts/page_preflight.js`，並把兩頁跑出來的結果貼進本資料夾 `RESULT.md`（前後各幾處紅燈、日出段有沒有抓到）。
6. commit ＋ push，commit 訊息開頭寫 `[雲端]`，結尾附上 commit 編號回報。

## 不要做
- 不要改 `特助心法.md`、`執行細則.md`、任何 CLAUDE.md 的規則文字。
- 不要碰 LINE、Telegram、任何會發訊息或扣額度的東西。
- 不要部署任何網站。

## 做完後 Mac 端會接手
把它接進「改網頁」流程（改完 HTML 沒跑自檢就擋交付）——這步要 Mac 的 hook，雲端不用做。
