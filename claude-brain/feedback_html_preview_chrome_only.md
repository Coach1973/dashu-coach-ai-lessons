---
name: html-preview-chrome-only
description: 本機 HTML 預覽唯一指定瀏覽器 = Chrome；禁止 Safari / 預覽面板 / file:// 取代
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3089ccd5-21cb-458c-92e4-eaecbd96dee9
---

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
