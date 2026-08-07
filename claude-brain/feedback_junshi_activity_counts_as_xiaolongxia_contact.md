---
name: feedback-junshi-activity-counts-as-xiaolongxia-contact
description: 教練跟軍師（終端機/桌面版）互動也算「有理小龍蝦」，不限內容範圍，已用hook自動記錄
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0042945d-d90c-456c-8ebb-8c6d854b1f9d
  modified: 2026-08-07T13:45:22.115Z
---

教練跟軍師（Mac 終端機/桌面版）互動，不管聊什麼內容，一律視為「教練有在跟小龍蝦系統互動」，小龍蝦的「教練沉默 N 小時」計算要把這個算進去，不能只認 Telegram/LINE 訊息。

**Why**：2026-08-06 教練回報「小龍蝦說我 67 小時沒說話，但我明明有在跟你聊」。查證發現真根因是 2026-08-03 15:58 有一則 Telegram 訊息真的被收到卻沒回覆、內容也沒存底（見 gateway log 證據），修好那個之後，教練接著問「怎麼讓小龍蝦知道我不是沒理他」——因為教練當天確實一直在跟軍師密集處理好幾個網站任務，但那些互動完全不會被小龍蝦的沉默計時器看見。教練 2026-08-07 選了最寬的範圍：「不限，只要是跟軍師互動就算」（曾提議只算「跟小龍蝦本身有關的問題」較窄範圍，教練否決，明確要最寬版）。

**How to apply**：技術上已用 `scripts/log_junshi_activity_to_echo.sh`（UserPromptSubmit hook，已註冊進 `~/.claude/settings.json`）自動落實，不靠模型記得——教練每發一句話給軍師，都會同步寫一筆進 `~/.openclaw/workspace/state/inbound_echo/YYYY-MM-DD.jsonl`（chatId 標教練的 Telegram ID `6124913915`，跟真正的 Telegram/LINE 訊息共用同一份 echo log），`scripts/sync_coach_last_message.sh` 已經會讀這份檔案，不用再改。如果未來要收緊範圍（比如教練覺得沉默警示變得沒意義），回頭改這支 hook 加內容篩選即可，不用整個砍掉重做。

Related: [[reference_new_session_context]]（三機身份分流原意）
