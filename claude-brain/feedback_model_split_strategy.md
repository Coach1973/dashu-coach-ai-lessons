---
name: model-split-strategy
description: 軍師在 Claude Code session 內用 Sonnet 開工/Sonnet 跑工具/Opus 做判斷的分工策略，省成本不降品質
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 42abcd59-99b7-486b-9227-f8619c4608d4
---

軍師（Claude Code 終端機/桌面版）一場 session 內可用 `/model` 切換模型來分工：

| 階段 | 模型 | 用途 |
|------|------|------|
| 開工讀檔 | Sonnet 4.6 | 讀 CLAUDE.md、接力棒、HEARTBEAT、心法 — 大量 input |
| 工具操作 | Sonnet 4.6 | 跑 grep/git/scp/檔案編輯 — 中等複雜度 |
| 關鍵判斷 | Opus 4.7 | 設計題、爭議仲裁、教練要「腦力」的對話 |
| 切回執行 | Sonnet 4.6 | 拍板後的執行落地 |

**Why:** 2026-05-29 教練親口拍板。三層理由：
1. **品質第一，不刪減開工內容**——開工讀的全部都是維護品質用的，刪掉就傷品質
2. **成本上 Sonnet ≈ Opus 的 1/5**——同樣的 16KB 開工內容，Sonnet 處理省 80%
3. **轉換成本低**——`/model` 切換是 session 內即時生效，不重啟

**How to apply:**
- 教練開新視窗時，建議軍師主動建議：「先 Sonnet 開工讀完所有檔案，準備好再切 Opus 做判斷」
- 遇到設計題、爭議、教練要「想一想」的提問 → 主動切 Opus
- 純執行類（commit/push/scp/檔案操作）→ 留在 Sonnet 省錢
- **校正**：context window 容量是 200K 不論模型，**切模型不會省 context、不會撐更多輪**，只省「處理同樣輪次的錢」
- 輪次到了（黃 20/橘 30/紅 38）還是要刷新，這條鐵律不變
