---
name: project-context-glossary
description: Use when starting substantial work in a "real software" project (has its own database/schema/backend logic, not a static marketing page) that doesn't yet have a CONTEXT.md. Create one to capture domain vocabulary so future sessions don't re-explain the same terms.
---

# 專案共享語言（CONTEXT.md）

來源：研究 mattpocock/skills 的核心洞察——每個專案先建一份術語表，AI跟教練才不用每次重新解釋一次業務語言，且變數/函式命名能更一致、AI花更少token在「猜這個詞是什麼意思」上。

## 何時該建

專案有自己的資料庫schema、後端邏輯、或多重身份/流程（例如mentor100的「導師 vs 種子導師」「edit_token vs 帳密」、namecard-db的「卡片 vs 配對」）就值得建。

**純靜態行銷頁（HTML+CSS+少量JS的活動頁/銷售頁）通常不需要**——教練大多數專案是這一類，術語量少、AI一眼就懂，硬建CONTEXT.md反而是額外維護負擔。判斷標準：如果解釋這個專案需要超過3個「這個詞在這裡的意思是……」，就該建。

## 怎麼建

1. 讀 `schema.sql`（如果有）——資料表名稱、欄位就是最直接的領域詞彙
2. 讀路由/入口（`app.py`的`@app.route`、或主要頁面結構）——搞懂有哪些「身份」「流程」
3. 寫進專案根目錄 `CONTEXT.md`，格式參考 `mentor100/CONTEXT.md`、`namecard-db/CONTEXT.md`：
   - 這是什麼（一段話）
   - 核心名詞（每個容易混淆的詞，講清楚「這在這裡指什麼，不是什麼」）
   - 架構決策為什麼這樣（尤其是踩過坑之後刻意這樣設計的地方）
   - 已知教訓/狀態（寫給下一場軍師）

## 使用時機

診斷bug、規劃新功能前，先讀專案的`CONTEXT.md`（如果存在）建立心智模型，再讀程式碼細節——這是`engineering-verification-discipline` skill的前置步驟。
