---
name: macos-headless-chrome-keychain
description: macOS 上用 headless Chrome 自動化抓「需要登入的網站」（cookie 登入）時，踩到 cookie 解不開、被導去登入頁的排查法與 0 按鈕修法。Use when a headless/puppeteer Chrome job on macOS suddenly hits a login page, loses cookies, or "cookies decrypt failed".
---

# macOS headless Chrome + 鑰匙圈 cookie 排查

macOS 上任何「headless Chrome 需要既有登入 cookie」的自動化作業都會踩這個坑。已驗證案例：FB 壽星抓取（2026-10-30、2026-11-01 兩次同症狀不同根因）。

## 症狀

腳本被導去登入頁（`/login`、`index.php?next=`），或 Chrome 啟動後 cookie 筆數變 0。**「session 過期」只是預設假設，多數時候不是。**

## 診斷順序（照這個順序做，不要跳）

### 第 1 步：先查「教練自己的瀏覽器」cookie 到期日

這是最快、也最不會誤導人的分法：

```bash
REAL="$HOME/Library/Application Support/Google/Chrome/Default/Cookies"
sqlite3 "$REAL" "select host_key,name,length(encrypted_value),
  datetime((expires_utc/1000000)-11644473600,'unixepoch','localtime')
  from cookies where host_key like '%facebook.com' and name in ('c_user','xs');"
```

- cookie **還在、到期日在未來** → **不是 session 過期，不要叫使用者重新登入**。繼續第 2 步。
- cookie **真的到期或整批不見** → 才是 session 過期，這時才需要使用者重新登入。

### 第 2 步：看 Chrome 自己的 stderr

用 `dumpio: true` 或直接看 Chrome 的 stderr 找這行：

- `Failed to decrypt token for service ...` → **根因 (b)：cookie 解不出來**。使用者重新登入也沒用，要改啟動方式（見下方修法 A）。
- 沒有這行但 cookie 在 → 根因 (c)：**Chrome 啟動時把 cookie 清掉了**（見修法 B）。

### 第 3 步：比對「工作 profile」的 cookie 總筆數

```bash
WORK="$HOME/.openclaw/fb_session_data_local/Default/Cookies"
sqlite3 "$WORK" "select count(*) from cookies;"   # 空殼會報 no such table: cookies
ls -la "$WORK"                                  # 空殼 ≈ 32KB；正常 ≈ 600KB
```

**只看 cookie「名稱」不看筆數會誤判**：查「有沒有 c_user/xs 這兩個名稱」在空殼 DB 裡也會回「有」。**一律看總筆數。**

### 第 4 步（最快定位法）：對照實驗

建一個乾淨 profile，只複製同樣的 cookie 檔，跑一次：

- cookie 存活 → **資料沒問題，是環境/profile 狀態問題**（修法 B）
- cookie 還是死 → **環境問題**（修法 A）

## 修法 A：沒有 responsible app（cookie 解不出來）

`puppeteer.launch()` 直接啟動的 Chrome，macOS 判定它「沒有 responsible app」→ 鑰匙圈 ACL 拒絕 → cookie 解不出來 → **Chrome 啟動時直接把 cookie 清掉**。

**改用 LaunchServices 啟動**，讓 macOS 正確歸屬 responsible app：

```bash
open -na "Google Chrome" --args \
  --user-data-dir="$WORK_PROFILE" \
  --remote-debugging-port=9225 \
  --headless=new --disable-gpu --no-first-run --no-default-browser-check \
  --disable-session-crashed-bubble about:blank
```

再接上去：

```js
const browser = await puppeteer.connect({ browserURL: 'http://localhost:9225' });
```

- `--headless=new` 保證使用者螢幕不會跳出視窗
- **profile 必須放本機碟**：放外部磁碟（USB SSD）時，背景執行沒有權限寫那個磁碟，Chrome 建不了 SingletonLock，會噴誤導性的 "The browser is already running for ..." 錯誤
- `open -na` 啟動前先清 `Singleton*`，否則 Chrome 以為已經在跑

## 修法 B：工作 profile 被 Chrome 清空（版本更新後）

**Chrome 大版本更新後，沿用舊工作 profile 會被判定版本不符 → 啟動時把 cookie 清掉。**

症狀：工作 profile 的 `Cookies` 變成 32KB 空殼（`no such table: cookies`），但教練真實 Chrome 的 cookie 完好。

**修法：每次同步前先重置 cookie 狀態，讓同步放進去的是完整快照。**

```js
function resetCookieState() {
  sh(`pkill -f "remote-debugging-port=9225" 2>/dev/null`);
  sh(`sleep 1`);
  sh(`rm -f "${PROFILE}/Default/Cookies"* "${PROFILE}/Default/Network Persistent State"* 2>/dev/null`);
  sh(`rm -f "${PROFILE}"/Singleton* "${PROFILE}/Default"/Singleton* 2>/dev/null`);
}
```

**並且一定要在 Chrome 啟動後回報 cookie 存活筆數（啟動前 vs 啟動後）**，這樣下次壞掉時一眼看得出是誰清的：

```js
console.log('Chrome 啟動後 cookie：' + (after > 0 ? '存活 ' + after + ' 筆' : '❌ 被清空'));
```

## 兩條要抄進去的一般化教訓

1. **「被導去登入頁」有兩種根因，症狀一樣**：(a) session 真過期 → 要人重登；(b)/(c) 環境壞掉 → **人重登也沒用**。**先查教練真實瀏覽器的 cookie 到期日再下判斷**，不要第一句就叫人重新登入。
2. **「壞掉時不要急著叫人來修」**——先自己找出 0 按鈕解法。叫使用者重新登入常常是白叫，因為根本不是 session 的問題。

## 驗證標準（不可省略）

修好後必須實際跑過：
- **對照實驗**：乾淨 profile + 同樣檔案 → cookie 存活（證明資料沒問題）
- **最壞狀態重跑**：把工作 profile 的 cookie DB 整個刪光再跑 → 仍正確抓到 → 真的會自癒
- **連跑兩三次結果一致**（避免抓到殘留或競態）

## 相關檔案

- 具體實作：`~/.openclaw/workspace/scripts/fb_birthday_scraper.js`（commit `d69b3b600`）
- 專屬 SOP：`~/.openclaw/workspace/knowledges/SOP_fb_birthday_scraper.md`
