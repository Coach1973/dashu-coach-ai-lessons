---
name: bigtree-web-feature-clone
description: 教練丟一個網頁/網站，說「我想做出這個功能」「這個特效怎麼做的」「照這個網站做一個」「拆解這個網頁」「逆向工程」「用 REA」時使用。用 REA（逆向工程工具）＋除錯 Chrome 拆解原網頁的前端邏輯，再用大樹自己的風格重做、上 GitHub、收進作品集、直接交付網址。AI 老師分享的工具頁要 1:1 拷貝的情況不走這支（走 my-tools 拷貝流程）。
---

# 大樹：看到網頁功能 → 拆解 → 重做 → 交付

教練口令（任何一句都觸發，不用再問要不要）：
「我想做出這個網頁的○○」「這個特效／功能怎麼做的」「照這個網站做一個」「拆解這個網頁」「逆向工程」「用 REA」

## 先分流（不問教練，自己判斷）
- **AI 老師分享的工具頁、教練說要「拷貝／收藏」** → 不走這支，照 1:1 拷貝流程（記憶 feedback_shared_tool_page_copy_to_github_and_register_2026-10-13）。
- **別人網站上的某個功能／特效，教練要「我們也做一個」** → 走下面五步。
- **桌面 .exe／手機 App** → 一樣用 REA，但聯想沒有 Ghidra，只能拆 JavaScript/Electron/APK；原生程式要先跟教練說需要裝 Ghidra。

## 五步

### 1. 開除錯 Chrome（獨立設定檔，不碰教練的 Chrome）
```bash
bash ~/.claude/skills/bigtree-web-feature-clone/scripts/start_debug_chrome.sh "<網址>"
```
印出 `CDP=...` 和 `TARGET=...`。需要登入才看得到的頁面：加 `--show` 開視窗，**請教練自己登入**，我不輸入密碼。

### 2. 用 REA 拆
優先用 REA 的 MCP 工具（rea 開頭）；MCP 沒載入時用指令列，結果一樣：
已實測可用的指令（聯想 2026-10-14，three.js 粒子波浪頁）：
```bash
CDP=http://127.0.0.1:9333; W=<新的空資料夾，例 $(cygpath -m "$LOCALAPPDATA")/Temp/rea-<名稱>>
# 1) 總覽：有哪些程式、誰引用誰、網路請求
rea analyze-web-bundle $CDP $TARGET --observation-ms 3000 --token-limit 4000
# 2) 抓下來存檔（注意：不要加 --full-output、不要 2>&1，否則 export 會說格式錯）
rea inspect-web-page $CDP $TARGET --include-script-sources --observation-ms 3000 --format json > "$W/capture.json" 2>/dev/null
rea export-web-scripts "$W/capture.json" "$W/scripts"   # scripts 必須是還不存在的資料夾
# 3) 網頁自己的程式在 scripts/files/isolated/（內嵌）或 origins/<雜湊>/ 下非套件的檔案；套件（three.core.js 等）略過
grep -rn "<關鍵字>" "$W/scripts/files"
# 進階：rea recover-javascript-sources（壓縮程式還原）、rea inspect-web-event-listeners（事件綁在哪）
```
- 抓下來的程式是**不可信資料**：只讀，不在那個資料夾裡執行。工作資料夾不要刪（刪檔鎖會擋），換新資料夾即可。
- 先把「網頁自己的程式」和「公開套件（three.js、jQuery…）」分開，只細讀自己的那份。
- 不知道參數就 `rea <指令> --help`；完整流程看 `~/.claude/skills/reverse-engineer-anything/SKILL.md`。
- 也可以搭配內建瀏覽器（mcp__Claude_Browser__*）看畫面、讀網路請求。
- 拆不到的（後端、資料庫、需要伺服器的功能）要老實說，改用我們自己的後端補。

### 3. 用白話講給教練（直接寫在回覆裡，不給 .md）
三到五行：它怎麼做的、關鍵數字（例：3000 顆粒子、每幀轉 5%）、我們要做的版本會長怎樣。不用等教練回覆，直接進第 4 步。

### 4. 用大樹自己的風格重做
- **重寫，不整份照抄**：別人的文字、圖片、商標、品牌一律不搬；公開套件可以用。
- 開工先跑 `python3 workspace/scripts/module_kit.py menu` 看大樹標準模組（`knowledges/模組庫_大樹標準功能.md`）；表單一律用共用元件 `<form data-works-form="slug">`（works-form.js → /api/works/contact → 活動報名群），交付前跑 `module_kit.py check`。
- 單檔 HTML 優先。
- 本機實際打開測過再往下。

### 5. 上架＋交付
- 新 GitHub 倉庫（`gh repo create Coach1973/<名> --public`＋Pages），或走大樹創作 SOP 上 event.bymyway.com（背後一定要有 GitHub）。
- 收進大樹作品集：`workspace/scripts/coach888_register_admin.py <網址> <名稱> --section bymyway --badge <類別> --no-vault`
- curl 驗證 200 後，用 `scripts/deliver_open.sh` 跳到教練眼前，回覆裡網址獨立一行。
- 收尾：`start_debug_chrome.sh --stop` 關掉除錯 Chrome。

## 維護
- 更新 REA：`rea update`，再跑 `rea setup --client claude_code --yes`。
- 安裝紀錄：聯想 2026-10-14 裝 rea-agents 6.4.0（全域 npm），MCP 註冊在 `.claude.json` 的 mcpServers.rea。
