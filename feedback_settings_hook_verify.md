---
name: Hook / settings.json 註冊類任務必須 cat 驗證
description: 跨檔註冊任務不能只說「已 jq patch」，必須把目標檔案 cat 出來貼進回報，否則視同假回報
type: feedback
originSessionId: f730794b-4b6d-402b-ad7e-ad4b5407b3d7
---
跨檔註冊類任務（hook、cron、launchd、PATH、shell rc）回報完工前，必須做兩件事：

1. `cat` 目標檔案的目標區段，貼進回報
2. 跑一次模擬觸發，驗證行為符合預期

**Why**：2026-05-16 11:00 前一場 Opus 軍師回報「第一招 Hook 已完工」，腳本確實寫好上雲（commit `c6933602`），但 `~/.claude/settings.json` 的 `hooks` 區段是 `{}`，根本沒註冊。教練 12:00 喊「開工」沒觸發，當場抓包。這跟記憶 `feedback_assistant_path_hallucination.md` 是同一類錯誤：說了「寫到 X」實際沒寫到。

**How to apply**：凡是涉及「修改 settings.json / config / 系統檔讓某腳本被掛上去」的任務：
- 回報模板必須有：① 目標檔案 cat 結果（區段）② 模擬觸發輸出 ③ commit hash
- 三項缺一不算完成，禁止用「已 jq patch」「已寫入」「應該生效」這類字眼結案
- 對應 R10 承諾鐵律的延伸：「跨檔註冊類任務」回報門檻高於一般 commit
