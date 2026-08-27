---
name: 任務指令用獨立 code block，讓教練一鍵複製
description: 給不同助教的任務必須各自放在獨立的 code block 裡，不能混在一起
type: feedback
originSessionId: 8edf0dc7-0b41-4b79-bda5-7f5c4b2f40e7
---
給終端機的任務放一個 code block，給 UI 版的任務放另一個 code block。每個 block 按一下複製圖示就能完整複製，不需要教練手動選取範圍。

**Why:** 教練複製貼上任務指令時，如果兩個助教的內容放在同一塊或分散在 markdown 段落裡，就必須用滑鼠手動選取再右鍵複製，非常麻煩。code block 右上角有一鍵複製按鈕，按下後打勾確認，乾脆痛快。

**How to apply:** 每次提供任務給多個助教時：
- 終端機任務 → 單一 code block（一次複製）
- UI版任務 → 單一 code block（一次複製）
- 不要在 code block 之外穿插說明文字把指令拆散
- block 內可以用 # 分段，但整包要在同一個 block 裡
- 每個 block 開頭都必須包含15分鐘存檔鐵律：
  - 終端機：「每15分鐘 git add + commit 一次，每完成一個任務立刻 commit」
  - UI版：「每15分鐘把當前進度寫入目標檔案並存檔，不等全部完成才存」
