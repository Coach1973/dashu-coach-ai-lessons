---
name: html-preview-chrome-only
description: 本機 HTML 預覽指定瀏覽器——Mac=Chrome；聯想(Windows)2026-07-13起改用Comet，因為聯想這台Chrome跳出來會空白、Comet正常
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3089ccd5-21cb-458c-92e4-eaecbd96dee9
---

# 🔴🔴🔴 2026-07-13更新：聯想（Windows）改用 Comet，不再用 Chrome

教練當場指示：「你下次跳出來的時候，不要跳 Chrome，因為它那邊感覺有問題，網頁出不來。
可是我把同樣的網址貼到 Comet，它就正常可以出來。所以你這邊可以預設跳出來的是 Comet
的瀏覽器嗎？然後記住設定，不要跳空白頁出來給我看，跳出來必須是要有東西。」

**Why:** 聯想這台機器用 `start chrome "<url>"` 跳出來的視窗教練看到的是空白頁（不論是
`file://` 本機路徑，還是 `http://localhost:8901/` 本機 server，都空白），改貼同一個
網址到 Comet 瀏覽器（`comet.exe`）畫面正常。根因未查（可能是這台 Chrome 本身設定/擴充
功能有問題），但教練要的不是查根因，是「跳出來的東西教練看得到」，Comet 目前驗證過
可以正常顯示。

**How to apply（僅限聯想/Windows這台機器，Mac 端仍維持 Chrome，見下方原始鐵律）：**
```bash
"C:/Users/bymyw/AppData/Local/Perplexity/Comet/Application/comet.exe" "http://localhost:<port>/"
# 或推上線後
"C:/Users/bymyw/AppData/Local/Perplexity/Comet/Application/comet.exe" "https://xxx.netlify.app/"
```
- 聯想這台以後任何 HTML 驗證要跳瀏覽器給教練看，**第一動作改成上面這行，不要再用
  `start chrome`**
- 若之後教練回報 Comet 也空白，代表要進一步查根因（可能是本機server起太慢、Comet
  也需要等一下再截圖），不能直接又退回 Chrome
- 2026-07-13 本次教練親眼在 Comet 看過 bigtree 7/22 高雄場地址資訊、確認畫面正常，
  才說「可以往上推了」——這次沒有再重演案例46（有真的跳出瀏覽器給教練看，且教練
  確認過才推 Netlify）

# 🔴 本機 HTML 預覽鐵律（教練 2026-06-17 下午 3:09 親口定稿）

**唯一指定開啟的 HTML 瀏覽器 = Google Chrome**。

## 強制指令格式

```bash
open -a "Google Chrome" /absolute/path/to/index.html
# 或啟動本機 server 再開
open -a "Google Chrome" "http://localhost:8000/"
```

## 禁止做的事

| ❌ 禁止 | 為什麼 |
|--------|--------|
| `open` 不指定 -a（會走系統預設） | 預設可能是 Safari，跟教練平常檢視環境不一致 |
| `open -a Safari ...` | 教練不用 Safari，且渲染細節跟 Chrome 不同 |
| **觸發 Claude Code Launch preview panel**（2026-06-17 教練第三次強調）| 面板展不開、看不到整體、教練每次都要手動關閉、AI 每次開啟浪費資源 |
| 只依賴預覽面板渲染 | 跟真實瀏覽器有差異，網站上線後可能不一樣 |
| 開 `file://` 給教練看（仍可能在 Safari）| 同上，且 file:// 沒有 server，相對路徑可能壞 |
| **只用 `mcp__Claude_Browser__preview_*` 系列工具（無頭瀏覽器）自己截圖確認就回報完成**（2026-07-10 案例46 第四次犯）| 這是 AI 自我除錯用的，不是教練驗收用的——AI 看過≠教練看過，兩者是不同目的的動作，缺一不可 |

## 🔴 AI 端如何避免觸發 Launch 預覽面板

Claude Code 內建 PostToolUse hook：用 `Edit` / `Write` 工具改 HTML 會**自動**把檔案推進 Launch 預覽面板（settings.json 無開關可關）。AI 端要主動避開：

| 改 HTML 方式 | 觸發預覽？ | 採用 |
|------------|---------|------|
| `Edit` 工具 | ✅ 會 | ❌ |
| `Write` 工具 | ✅ 會 | ❌ |
| `Bash` + `python3` heredoc 改 HTML | ❌ 不會 | ✅ |
| `Bash` + `sed -i ''` 改 HTML | ❌ 不會 | ✅ |

**標準作法**：HTML 改動寫成 Python 腳本透過 Bash 跑，改完直接 `open -a "Google Chrome"`，省去教練每次手動關預覽的時間。

## Why
教練 2026-06-17 下午 3:09 親口提醒：「之前打開都是用 chrome 為何這次是使用 safari，唯一指定開啟的 html 就是 chrome」。
這是教練的「真實工作環境一致性」鐵律——本機預覽必須跟 Netlify 上線後一致，Chrome 是教練檢視所有作品的瀏覽器。
若軍師用 Safari 預覽，渲染 OK 不代表 Chrome OK，可能踩字型/CSS 差異坑。

## How to apply
1. **任何時候要給教練看 HTML，第一動作**：`open -a "Google Chrome" <path>`
2. **絕不依賴 Claude Code 預覽面板**當作唯一證據——它只是輔助
3. 如果是要本機 server，先 `python3 -m http.server` 起好，再 `open -a "Google Chrome" "http://localhost:<port>/"`
4. 若教練要求改用其他瀏覽器，當場確認；否則 Chrome 是唯一答案
5. 教練主要工作環境是 Windows + Chrome；Mac 端 Chrome 也已安裝

## 🔴 第四次犯（2026-07-10，試金石案例46）

用 `mcp__Claude_Browser__preview_screenshot` 等無頭瀏覽器 MCP 工具自己截圖確認 HTML 畫面正確後，直接跟教練回報「已經看過、確認正確」，**沒有額外執行 `open -a "Google Chrome"` 讓教練本人親眼看到**。教練當場重話：「講多少次你沒跳HTML給我看。」

**新增 How to apply**：AI 用無頭瀏覽器工具做內部除錯驗證，跟「跳 Chrome 給教練看」是兩個不同目的、缺一不可的動作。**任何 HTML 改動要回報「完成」之前，最後一步永遠是 `open -a "Google Chrome" <path或URL>`**，不能因為自己已經用內部工具驗證過畫面正確，就省略這一步。

## 🔴 第五次犯＋Windows端解法（2026-07-13，聯想桌面版）

改完 ai-talk 講師簡介後，先試 `mcp__claude-in-chrome__*`（Claude in Chrome 擴充功能）
想跳出教練本人的真實 Chrome，但擴充功能沒連上（"Claude in Chrome is not connected"），
retry 兩次都失敗。**這時候退回去只用 `mcp__Claude_Browser__*`（App內建無頭瀏覽器）自己
截圖驗證，就跟教練回報完成**——又是同一個坑，教練當場點破：「你這邊沒有執行跳 HTML
出來給我看。」

**真正解法**：這台是教練本人的實體 Windows 電腦（不是遠端連線），不需要靠 MCP 瀏覽器
自動化工具才能碰到教練的螢幕——**直接用 Bash 工具跑 Windows 原生指令 `start chrome
"<url>"`**（或 `start "" "<url>"`），就會在教練自己的螢幕上真的彈出 Chrome 視窗。
這一試就成功，比檢查 Claude in Chrome 擴充功能連線狀態更直接。

**Windows 版 How to apply（跟 Mac 版 `open -a "Google Chrome"` 對應）**：
```bash
start chrome "http://localhost:<port>/"
# 或推上線後
start chrome "https://xxx.netlify.app/"
```
Claude in Chrome MCP 擴充功能不是這台機器的必要依賴——它沒連上時不代表沒辦法跳出瀏覽器
給教練看，`start chrome` 永遠是本機最後保底手段，優先層級應該跟 Mac 的 `open -a` 同等，
不是等 MCP 失敗才想到的備案。

## 🔒 確定性 Hook 已上鎖（2026-07-11，教練口頭指示「做」）

不再只靠「記得要開 Chrome」——已比照簡體字 Stop Hook 架構，建立 `scripts/rule_html_chrome_check.sh`：這一輪若 Edit/Write 改過 `.html`，且改動之後找不到 `open -a "Google Chrome"` 的紀錄，強制 exit 2 攔截，不讓「已看過」的回報送到教練眼前。已註冊進 `~/.claude/settings.json` Stop hooks，並用假 transcript 實測四種情境全部正確（詳見試金石案例46後續段落）。

同場也補了另一個真漏洞：既有的 `web_preview_verify_guard.sh`（git push 前查證用）原本把無頭瀏覽器工具的截圖也算成有效證據，這正是案例46能矇混過關的破口，已拿掉，只認 `open -a "Google Chrome"` 為唯一證據。
