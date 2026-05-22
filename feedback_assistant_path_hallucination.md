---
name: 助教假承諾路徑（系統性盲點）
description: 學長/桌面版常口頭說「已寫入 X 路徑」實際寫到別處，要核查實體檔案而非相信口頭回報
type: feedback
originSessionId: e036e714-6919-49b9-8691-6afa49800e13
---
助教（學長小龍蝦、桌面版 Claude.app）對「寫入了什麼路徑」常有系統性錯誤，要求事後驗證實體檔案是否真的存在於宣稱的位置，不能聽口頭回報就算數。

**Why:** 已知至少兩次案例——
1. 2026-05-15 18:15 學長對教練說「行事曆資料已寫入 `~/.openclaw/workspace/schedule-2026.md`」，5/16 凌晨軍師核查時 workspace 根本沒有這個檔案，學長實際寫到 `agents/kong/memory/schedule-2026.md`（學弟記憶區）。
2. 2026-04-26 桌面版報告「SOUL.md 已同步」，但實際同步到 `workspace/`（舊版參考資料夾）而非 Bot 真正讀取的 `agents/kong/SOUL.md`。

兩次的共同模式：助教看到「workspace/」或「agents/」就誤以為通用，沒驗證實際寫到哪。後果是「以為治本，其實沒治」，下次同樣問題重現。

**How to apply:**
- 助教回報「已寫入 X 檔案」時，軍師必須立刻 `ls -la X` 核查，不能信口頭
- 涉及多 session（學長/學弟/學妹/桌面版）共用檔名（SOUL.md、schedule、HEARTBEAT）時尤其要驗
- 看到「假承諾路徑」就獨立記到 LEARNINGS.md，不要混進其他根因報告
- 軍師自己寫入檔案後，回報必須附上 `ls -la` 或 commit hash 證據，不只說「已完成」
