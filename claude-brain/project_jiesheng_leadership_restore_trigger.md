---
name: project-jiesheng-leadership-restore-trigger
description: 教練說「恢復早鳥名額」或「恢復搶早鳥名額」時，還原 jiesheng-leadership 的早鳥按鈕版本
metadata: 
  node_type: memory
  type: project
  originSessionId: 5ad547ac-8632-4ab2-81a1-56aa2819cd2e
---

## 觸發暗號

教練說「恢復早鳥名額」或「恢復搶早鳥名額」時，立刻執行以下動作：

## 執行步驟

1. 把備份檔蓋回主檔：
```bash
cp /Users/bymyway/github_repos/jiesheng-leadership/_backup/index_含早鳥名額版.html \
   /Users/bymyway/github_repos/jiesheng-leadership/index.html
```

2. 本機預覽讓教練確認（#workshop 區塊應出現三個按鈕：報名線上座談會、報名工作坊、搶限量早鳥名額）

3. 教練說「推」→ commit + push

## 背景

- **Why**：金流系統就緒前先隱藏早鳥按鈕；就緒後一鍵復原
- **備份來源 commit**：`eb74bf5`（2026-06-11）
- **備份檔路徑**：`_backup/index_含早鳥名額版.html`（存在 jiesheng-leadership repo 裡）
- **移除早鳥版 commit**：`e7833b7`（2026-06-11）

**How to apply**：暗號觸發→不問→直接準備好→讓教練確認→才推
