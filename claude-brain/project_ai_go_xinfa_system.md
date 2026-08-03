---
name: project-ai-go-xinfa-system
description: 大樹教練特助心法跨 AI 一鍵注入系統 ai-go.github.io，2026-06-23 上線
metadata: 
  node_type: memory
  type: project
  originSessionId: 4e51c46d-66d2-4a7f-aef6-2ae5c071e132
  modified: 2026-08-03T06:10:15.666Z
---

# 🌳 ai-go · 特助心法跨 AI 一鍵注入系統

**上線日**：2026-06-23
**雙入口**：
- https://coach1973.github.io/ai-go/（GitHub Pages，開發者/AI fetch 用）
- https://www.bymyway.com/ai-go/（教練個人品牌站，社群分享用，bymyway page_id 27390）

**GitHub**：https://github.com/Coach1973/ai-go
**本機路徑**：`/Users/bymyway/github_repos/ai-go/`
**本機 preview**：`http://localhost:8765/`（launch.json name=ai-go）
**bymyway 部署腳本**：`projects/bymyway-bridge/examples/deploy_ai_go_to_bymyway.py` + `publish_ai_go.py`

## 用途

教練在任何裝置、任何 AI 上開新對話 → 貼網址（或全文）→ AI 30 秒進入頂級特助狀態。
跨 Claude / ChatGPT / Gemini / Grok / MiniMax / DeepSeek / Llama 共用同一份心法。

**Why**：解決「換 AI / 換對話就要重教 AI 怎麼當特助」的摩擦痛點。教練拍板「完全公開」=
這同時是教練個人品牌作品（呼應 [[project-ai-coach-brand-story]]），心法 = 方法論代名詞，
像「彼得・杜拉克管理學」之於商管。

**How to apply**：
- 教練要在新 AI 開工 → 貼網址或方法 B raw URL
- 心法本文有任何更新 → 改 `system-prompt.md` 並 push → Pages 5 分鐘內生效
- 其他軍師/特助看到 ai-go 字眼 → 知道指的是這個系統
- 不要在 ai-go repo 內加血淚案例（教練拍板「不加」，案例量會稀釋核心）

## 三種貼法（依場景）

| 場景 | 貼法 |
|------|------|
| AI 會主動 fetch URL（Claude、ChatGPT browse、Gemini grounding）| 貼主 URL `https://coach1973.github.io/ai-go/` |
| Pages CDN 沒同步 / 想拿純文字 | 貼 raw URL `https://raw.githubusercontent.com/Coach1973/ai-go/main/system-prompt.md` |
| 任何離線 AI / 不會 fetch 的 AI | 開 https://coach1973.github.io/ai-go/ → 點橘色大按鈕 → 貼全文 |

## 內容架構（10 區段）

1. SYSTEM 元指令（給 AI 看：讀完做開工宣言）
2. 最高指導原則（使命/願景/理念）
3. 三大信念
4. 靈魂三問
5. 特助 21 守則（一字不差含教練親筆詮釋）
6. 執行細則 E01~E10
7. 開工六步驟
8. 暗號協議表
9. 開工宣言（一字不差朗讀）
10. 驗證題（自證已讀，避免 AI 裝懂）

## 授權

CC BY-ND 4.0（姓名標示・禁止改作）— 可公開分享、貼 AI、放系統提示，不可改寫重發。
教練/海餅乾俱樂部 © 2007–2026。

## 部署機制

- Git push → GitHub Pages 自動 build（30 秒-3 分鐘）
- CDN cache 可能再延遲幾分鐘——急用時改抓 raw.githubusercontent.com
- `_headers` 已寫死 Content-Type 防 Netlify-style text/plain 陷阱（雖然 Pages 不吃 _headers，留著兼容未來移到 Netlify）

## 給未來軍師

更新心法 SOP：
1. 改 `/Users/bymyway/github_repos/ai-go/system-prompt.md`（守則 #21 一字不差！）
2. 改 `index.html` 對應渲染區段
3. 本機 Chrome 驗收（`http://localhost:8765/`）
4. 教練說 OK → `git push`
5. 等 5 分鐘讓 Pages CDN 同步，或主動 `gh api -X POST /repos/Coach1973/ai-go/pages/builds` 強迫 rebuild

## 2026-08-03 新增：教練專屬人設區塊（coach-persona.md）

公版 `system-prompt.md` 給任何人用；教練自己貼給新 AI 時，另外需要一段「我是誰、怎麼跟我溝通」的個人身份說明（跟公版方法論是兩件事，不能混在一起讓其他使用者也讀到教練個資）。已新增 `coach-persona.md`（中英對照：關於我/怎麼跟我溝通8條/我重視的價值）+ `index.html` 頁尾前新增獨立區塊（綠色系跟公版橘色區隔，清楚標示「不是公版方法論，你不是教練本人可以跳過」，獨立一鍵複製按鈕）。commit `4d38936`。

**已知缺口**：本次只推了 `coach1973.github.io/ai-go/` 這個入口，`www.bymyway.com/ai-go/` 鏡像走獨立部署腳本 `deploy_ai_go_to_bymyway.py`，尚未同步，兩入口內容目前不一致，見 [[project_windows_workspace_git_sync_gap_2026-07-17]] 類似的雙入口同步風險。

**踩過的坑**：本機 Python `http.server` 對 `.md` 檔案預設不宣告 charset，直接點開連結會顯示亂碼，但這只是本機預覽伺服器的限制——正式站 `_headers` 早有 `/*.md → charset=utf-8` 萬用規則（用 README.md 這種沒有專屬 `_headers` 條目、只吃萬用規則的檔案當對照組驗證過），不影響正式部署。下次本機驗收 `.md` 檔案時，若看到亂碼先懷疑本機伺服器沒宣告 charset，不要誤判成部署有問題。
