---
name: 各機 commit 邊界（教練親定 2026-05-20）
description: 我（軍師）只 commit 中央發布的變更，不碰各機自己產生的運作資料
type: feedback
originSessionId: de3cc846-e958-479d-b705-90dc4d3bc6de
---
**規則：**
- **中央發布** = 教練決策、軍師執行的變更（SOUL.md、AGENTS.md、設定檔、工具設定等）→ 由我 commit，留紀錄
- **各機運作資料** = 各小龍蝦對話產生的 sessions/、memory/ 更新、auth-state.json 等 → 各機自己的自動備份機制負責，我不插手

**Why:** 孔大哥和佩佩老師的對話框是他們自己的，他們運作產生的資料不應該由軍師這邊來 commit，邏輯不通。

**How to apply:**
- 改了 kong 或 peipei 的 SOUL.md / 其他設定檔（是我主動修改的）→ 我 commit
- kong 或 peipei 的 sessions/、memory/、auth-profiles 是他們自己跑出來的 → 不碰、不 commit
- 判斷標準：「這個變更是我做的，還是他們自己跑出來的？」
