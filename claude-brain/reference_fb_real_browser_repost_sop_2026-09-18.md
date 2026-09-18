---
name: reference-fb-real-browser-repost-sop
description: FB Graph API 發文訪客看不到（App Review 未通過）時，用 Playwright + Chrome DevTools Protocol 接管教練 Mac Chrome 已登入的 FB session 重貼到粉專。記錄 2026-09-18 實戰踩過的 6 個坑與一次到位腳本。
metadata:
  type: reference
---

## 適用情境

當用 Graph API 對 FB 粉專發文，但 App Review 還沒過，訪客看不到貼文（只有管理員能看到），需要用真人瀏覽器重貼。

這個 SOP 跟 `reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11.md` 是同一條路徑的兩條分支——能走 API 就走 API（見那篇），走不通就這篇。

## 前置

- 教練 Mac Chrome 已登入 FB（個人帳號有粉專管理員身份）
- Chrome profile 在 `~/Library/Application Support/Google/Chrome/Default/`
- 教練願意 8-10 分鐘不能動 Chrome（被接管期間）

## 一次到位 SOP（8 步）

### Step 1：驗證 URL 是正式站

**坑 #1**：不能用 `https://coach1973.github.io/<slug>/`（這是 GitHub Pages 開發版）。正確是 `https://event.bymyway.com/curated/<slug>/`（event-signup Flask app 正式站）。

驗證所有 slug：
```bash
for slug in everydaycaf-tai-nan-san-dian flower-site fu-en-ping historic-residence kangyenju nmda nmda-2 peipei sbip xiangjuchang xiaonan xie-wei-xiang zhang-yu-ci; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 6 "https://event.bymyway.com/curated/${slug}/")
  echo "$code $slug"
done
```
全部 200 才能繼續。

### Step 2：複製 FB cookies 到非預設 profile

**坑 #2**：不能複製整個 953MB Chrome profile（含所有網站憑證，超出授權範圍）。只複製 `Cookies` + `Cookies-journal` 兩個檔案（< 1MB，只有 FB session 資料）。

```bash
PROFILE_NEW="/tmp/chrome-repost-profile"
rm -rf "$PROFILE_NEW"
mkdir -p "$PROFILE_NEW/Default"
cp "/Users/bymyway/Library/Application Support/Google/Chrome/Default/Cookies"* "$PROFILE_NEW/Default/"
```

### Step 3：用 osascript 關教練 Chrome

```bash
osascript -e 'quit app "Google Chrome"'
# 等 process 真的結束
for i in 1 2 3 4 5; do
  pgrep -x "Google Chrome" >/dev/null 2>&1 || break
  sleep 1
done
```

### Step 4：啟動 Chrome with remote debugging port

**坑 #3**：Chrome 安全設計**拒絕用預設 profile 開啟 remote debugging port**（會跳 "DevTools remote debugging requires a non-default data directory" 錯誤）。必須用非預設 user-data-dir。

**坑 #4**：zsh 把 `--remote-allow-origins=*` 的 `*` 當 glob 展開，要 quote 起來。

```bash
nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  '--remote-allow-origins=*' \
  --user-data-dir=/tmp/chrome-repost-profile \
  >/tmp/chrome-repost.log 2>&1 &
sleep 6
curl -s http://127.0.0.1:9222/json/version | head -2  # 確認 port 起來
```

### Step 5：Playwright 透過 CDP 接管（不用本地 chromium）

**坑 #5**：Playwright npm install 時設 `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` 跳過 chromium binary 下載（200MB 省下來）。`chromium.connectOverCDP()` 不需要本地 browser，只透過 DevTools Protocol 通訊。

```bash
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install playwright --silent
```

```javascript
const browser = await chromium.connectOverCDP('http://localhost:9222');
const context = browser.contexts()[0];
const page = context.pages()[0];
```

### Step 6：FB 兩階段 modal 貼文流程（2026+ 介面）

**坑 #6**：FB 2026+ 介面是兩階段 modal，**先點「繼續」才看到「發佈」按鈕**。

**坑 #7**：發佈按鈕的 aria-label 是**繁體「發佈」**不是簡體「發布」。

**坑 #8**：Draft.js / contenteditable 編輯器對合成鍵盤事件沒反應（[reference_palms_grand_total_row_and_js_widget_typing_2026-09-15.md](reference_palms_grand_total_row_and_js_widget_typing_2026-09-15.md) 有記載），改用 `page.evaluate` + `execCommand('insertText')` 直接寫入 + 觸發 `input` event。

完整貼文流程：
```javascript
// 1. 進 FB 首頁
await page.goto('https://www.facebook.com/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);

// 2. 點「建立貼文」（首頁 feed 頂部，預設就是當前登入身份的粉專）
await page.locator('[aria-label="建立貼文"]').first().click();
await page.waitForTimeout(3000);

// 3. 寫文案到編輯器（Draft.js 對合成鍵盤沒反應）
const editor = page.locator('[role="textbox"][contenteditable="true"]').first();
await editor.click();
await editor.evaluate((el, text) => {
  el.focus();
  const sel = window.getSelection();
  sel.removeAllRanges();
  const range = document.createRange();
  range.selectNodeContents(el);
  range.collapse(false);
  sel.addRange(range);
  document.execCommand('insertText', false, text);
  el.dispatchEvent(new InputEvent('input', { bubbles: true, cancelable: true, inputType: 'insertText', data: text }));
}, body);

// 4. 點「繼續」進 stage 2
await page.locator('[aria-label="繼續"]').first().click();
await page.waitForTimeout(4000);

// 5. 點「發佈」（繁體）
await page.locator('[aria-label="發佈"]').last().click();
await page.waitForTimeout(6000);
```

### Step 7：FB 自動抓 og metadata 展開 preview card

只要文案裡有 `https://event.bymyway.com/curated/<slug>/`，FB 會自動抓 og:title / og:description / og:image 展開 preview card，不需要在文案裡手動塞圖片 URL。

### Step 8：通知教練可以再開 Chrome

12 則跑完後，告訴教練「可以再開 Chrome 了」。

## 文案格式範本

```
{店名標題}

{og:description 前 80 字}

👉 完整介紹：https://event.bymyway.com/curated/{slug}/

#大台南策展中心 #大樹教練產業鍊
```

## 驗證 SOP

每則貼完用 Mac Chrome 無痕視窗（⌘+Shift+N）開 `https://www.facebook.com/大台南策展中心/`，確認該則出現在公開時間軸。

## How to apply

下次任何時候遇到「FB API 發的文訪客看不到，要重貼到粉專」的任務：

1. **不要直接想 Playwright 接管 Chrome**——先確認教練環境是 Mac（教練 Mac = Chrome profile 在 `~/Library/...`），不是雲端
2. **不要複製整個 Chrome profile**——只複製 Cookies 檔案（Auto mode 會擋整個 profile 複製）
3. **一定要驗證 URL 用正式站**（`event.bymyway.com`）而不是 GitHub Pages
4. **一定要記得「繼續」+「發佈」繁體 + Draft.js execCommand** 這三個坑
5. 預估 token：順利 1-3 萬（含 debug），失敗 5-8 萬

完整腳本範本：`scripts/repost_curation_fb.js`（v4 起為一次到位版本）

## 關聯記憶

- [[reference-fb-graph-api-app-review-required-for-public-visibility-2026-09-11]]：為什麼要走瀏覽器（API App Review 卡住的根本原因）
- [[reference-palms-grand-total-row-and-js-widget-typing-2026-09-15]]：Draft.js 對合成鍵盤事件沒反應的詳細說明
- 腳本：`scripts/repost_curation_fb.js`
