---
name: coach-verbatim-report
description: 教練要保留這場對話自己說過的每一句話時使用——「原話報告書」「逐字報告」「把我說的話一字不漏做成網頁」「下一個對話要完整保留我說過的話」「教練原話」。從原始對話紀錄逐字抽出，做成網頁、驗證零差異、交付網址。
---

# 教練原話逐字報告書（做法在記憶 reference_session_verbatim_report_from_jsonl_2026-10-04；範例程式 `scripts/build_strategy_verbatim_report_2026-10-04.py`）

## 步驟
1. **來源**：`~/.claude/projects/<資料夾>/<sessionId>.jsonl`（含壓縮前整場）。教練原話從 `type=queue-operation` 且 `operation=enqueue` 的 `content` 抽；排除開頭是 `<` 的任務通知與 `/compact`；`<!-- attach -->`（教練附檔）要保留。**不要用 `type=user` 條目**（連續兩則會被合併、還混系統文字）。
2. `/model`、`/compact` 這類指令另列「操作紀錄」，不混進話語。時間一律換台灣時間。
3. **網頁**：每則一張卡片，原話用 `white-space:pre-wrap` 原樣呈現；軍師導讀用不同底色並標「軍師註（非教練原話）」；語音諧音字原樣保留不改；字 ≥20px。
4. **驗證，缺一不可**：網頁內文 `html.unescape` 後等於原文；原文的 JSON 轉義形式出現在原始 jsonl 裡；用 Chrome 開並確認卡片數等於則數。
5. **放哪**：教練說過不擔心公開——放大樹作品（`bigtree-publish-site` 技能，kind=creation）或 Artifact 私人頁都行；接力棒寫上網址。
6. **交付**：`bash ~/.openclaw/workspace/scripts/deliver_open.sh <網址>`，網址獨立一行。最好在收工總結之前做。
