---
name: reference-github-pages-md-content-type-ai-compat-2026-09-25
description: GitHub Pages對.md副檔名回傳content-type:text/markdown(非text/html)，多數AI內建讀網頁工具只認text/html會回報「讀不到/被屏蔽」——任何要給外部AI讀的公開頁一律要有.html版本
metadata:
  node_type: memory
  type: reference
  originSessionId: 88a8b6c3-e631-4390-8d89-3c37d65f917b
  modified: 2026-09-25T05:15:00.178Z
---

教練把公開網址（`ai-go/status.md`，用意是貼給任何網頁版AI讀取工作狀態）拿去實測，
ChatGPT/Gemini/Grok 都回報「讀不到、被屏蔽」，只有 Claude 讀得到。

**查證過程（curl 實測，不是猜的）**：
- `curl -sI` 兩個檔案的 header：`status.md` → `content-type: text/markdown`；同目錄 `index.html` → `content-type: text/html`。這是 GitHub Pages 對副檔名的預設行為，不是 Jekyll 處理過的頁面。
- robots.txt：該站沒有自訂 robots.txt（回 404）。
- 用常見 AI 爬蟲 UA（GPTBot、ChatGPT-User、PerplexityBot、Google-Extended、ClaudeBot）逐一 curl，全部 HTTP 200，沒有被 WAF/robots 擋。

**結論**：不是網站被封鎖，是多數 AI 內建的「讀網頁」工具只認得 `text/html`（可能是白名單機制或渲染器只處理 HTML DOM），看到 `text/markdown` 這種較冷門的 MIME type 就直接判定「無法存取」回報給使用者，使用者聽起來就像是「被屏蔽了」。

**Why**：任何要設計「貼一個網址給任意 AI 讀」的公開頁面，光有 .md 版本不夠，一定要有 .html 版本才能保證跨平台相容。

**How to apply**：
- 往後任何公開頁若同時要給人看、也要給任意 AI 抓取，一律準備 `.html` 版本當主要對外網址；`.md`/純文字版只當備用（給真的不能讀 HTML 的工具）。
- 不用兩邊手動維護：寫一支轉換腳本（本例 `~/.openclaw/workspace/scripts/render_public_status_html.py`，用 python-markdown），markdown 當唯一手改來源，每次發布自動轉出 HTML，避免分岔。
- HTML 內容要直接印進原始碼（不能靠 JS 才顯示），沒有瀏覽器 JS 引擎的爬蟲/AI 一樣讀得到——這點原本的 `ai-go/index.html` 就做對了，只是 status.md 沒有對應的 HTML 版本。
- 判斷「讀不到」是不是內容類型問題，先 `curl -sI` 比對 content-type，再用常見爬蟲 UA 逐一測試排除 robots/WAF 可能性，不要看到「AI說讀不到」就直接假設是網站被封鎖或需要授權。

## 相關
[[reference_move_to_cloud_this_repo_2026-09-25]]（同一天建立的公開交接棒機制）
