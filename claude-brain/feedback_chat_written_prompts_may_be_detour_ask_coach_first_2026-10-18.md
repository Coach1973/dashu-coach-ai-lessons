---
name: feedback-chat-written-prompts-may-be-detour-ask-coach-first
description: 教練貼來的長指令常是 Chat（網頁版 AI）寫的、不懂教練 code 環境；看到繞遠的步驟先找教練問清楚真正要的結果，不要照單全收
metadata:
  node_type: memory
  type: feedback
  originSessionId: 17388054-19c8-51da-a5ba-30a2d6f8f537
  modified: 2026-10-18T03:39:31.130Z
---

教練貼給我的長指令，常常是 Chat（Claude 網頁版／別的 AI）幫他寫的。Chat 不知道教練電腦與 code 的實際工作狀況，所以指令裡常有繞遠的步驟。

**Why:** 2026-10-18「加 Suno 歌曲進 taipeiema1017」：Chat 寫的指令要求「下載 mp3 與封面放進 assets、不要用 Suno 外站網址當播放來源、照昨天打包上傳」。我照字面做，卡在 Suno 音檔加密、重新上傳會變 `taipeiema1017-2`、來回問教練要 mp3，浪費約 15 分鐘，教練不高興。教練真正要的只有一句：「給 Suno 網址，誰點了都能聽，把這首歌放進昨天的網頁」。最簡單做法是 Suno 官方內嵌播放器（`https://suno.com/embed/<歌曲編號>`），直接改原網頁資料夾、commit＋push，網址不變。

**How to apply:**
- 看到指令步驟很多、很繞（要下載檔案、要重新打包上傳、要避開某個簡單做法），動手前先找教練問一句「您真正要的結果是什麼？」，或先回報「有更簡單的做法：…，用這個可以嗎？」。
- 教練要的結果通常比指令簡單很多；先用最簡單做法能不能達成來判斷。
- 卡關時不要叫教練去下載檔案；先回頭問「這條路是不是繞遠了」。
- 與 [[reference-move-to-cloud-this-repo-2026-09-25]] 無關；與 N2「方向模糊只問一句：您想要什麼結果？」同一精神。
- 站台更新方式：event.bymyway.com 的 `/curated/<slug>/` 直接讀 `~/github_repos/<slug>`，改檔 commit＋push 即上線，網址不變；用上傳表單重傳同 slug 會被改名成 `-2`。
- 已落成機制（教練 10/18 說「守則16很好用，要融入對話工作」）：條件反射 `R-RULE16-LONG-INSTRUCTION-ASK-RESULT`（knowledges/反射索引.json，prompt 時刻）；教練貼多步驟長指令（「要做的事」「執行步驟」或 1.2.3.編號清單）就自動跳出守則#16 提醒。回測 4,499 句只跳 12 次。
