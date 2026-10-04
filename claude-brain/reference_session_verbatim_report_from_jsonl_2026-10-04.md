---
name: reference-session-verbatim-report-from-jsonl-2026-10-04
description: 教練要「整場原話一字不漏做成網頁報告書」給下一個對話框時的做法：從對話記錄 jsonl 的 queue-operation enqueue 抽，不憑記憶重寫；含逐字驗證法與成品位置
metadata: 
  node_type: memory
  type: reference
  originSessionId: 388b59cd-c89a-5682-aa66-0db09811e265
  modified: 2026-10-04T05:54:10.278Z
---

2026-10-04 教練說「這一次的對話非常精彩，把我所有完整對話一字不漏做成網頁版報告書，下一個對話框必須完整保留我說過的話」（起因：手機版 context 只有 200K，已用 167.7K，需收工換新對話框）。

**做法（已實跑，14 則／5,875 字，與原始記錄零差異）：**
- 來源：`~/.claude/projects/-Users-bymyway--openclaw/<sessionId>.jsonl`（含壓縮前整場）。
- 教練原話從 `type=queue-operation` 且 `operation=enqueue` 的 `content` 抽，排除開頭是 `<`（子代理回報／任務通知）和 `/compact`；但開頭是 `<!-- attach -->`（教練附檔）的要保留，去掉附件標記那一段（到第一個空行）只取教練打的字——否則會漏掉最重要的幾則。時間戳是 UTC，+8 才是台灣時間。
- 不要用 `type=user` 條目抽：同一時段連續送出的兩則會被系統合併成一則，還混有系統注入文字（本場 12:34 與 12:39 兩則就被合併）。
- `/model`、`/compact` 這類指令從 user 條目的 `<command-name>` 另列「操作紀錄」，不混進話語。
- 網頁：每則一張卡片，原話用 `white-space:pre-wrap` 原樣呈現；軍師導讀另用不同底色並標「軍師註（非教練原話）」；語音諧音字（如「周育凱」）原樣保留不改。
- 驗證（缺一不可）：`html.unescape(網頁內文)==原文`，且原文的 JSON 轉義形式要出現在原始 jsonl 裡；再用 Chrome 開並確認 DOM 卡片數。
- 成品：`workspace/knowledges/2026-10-03_百人同行_遊戲化設計_教練原話逐字報告書.html`（commit `2a25dcf44`），接力棒 v274 指向它；線上版 `https://event.bymyway.com/curated/game-1004/`（16 則，含 14:00 退件與 14:03 授權；14:03 之後的話看對話記錄 jsonl 重抽）。

**Why:** 教練每分鐘 200 字的語音是 26 年經驗的心血（N8），壓縮摘要會丟細節；這是他明確要的功能，之前不存在。
**How to apply:** 教練再要求「保留原話／逐字紀錄」時照這套做，不從記憶重寫；在收工前做；報告含他的私人構想；教練 10/04 親口說不擔心公開、放大樹作品或給他一個可自己讀的網頁都行，已上架 `https://event.bymyway.com/curated/game-1004/`（noindex，走大樹創作 SOP）。以後類似報告預設走這條，把網址獨立一行給他，不要只說「已在 Mac 開過」。
