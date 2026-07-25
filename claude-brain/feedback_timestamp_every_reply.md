---
name: feedback-timestamp-every-reply
description: 教練要求終端機/桌面版(軍師/特助)對話每則回覆開頭都要標台灣時間戳記，方便他一眼判斷訊息是幾點發的
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2aedf319-34ef-4bb3-8704-d568dda3a347
  modified: 2026-07-24T00:42:32.673Z
---

教練2026-07-24要求：終端機/桌面版（軍師/特助）的每一則回覆開頭都要標一個時間戳記，格式類似「🕐 2026-07-24（五）08:41 台灣時間」，讓他一看就知道這則訊息幾點幾分發的，方便評估。

**Why**：教練原話「這樣一看就知道這是幾點幾分發的訊息，你也好評估」——這是在[[feedback_taiwan_time_always]]時間鐵律基礎上更進一步的具體格式要求，從「講時間要換算成台灣時間」延伸到「每則訊息都主動標記」。

**How to apply**：
- 每次系統會在UserPromptSubmit hook自動注入當下台灣時間（"[時間覺察]現在：YYYY-MM-DD HH:MM:SS 星期X"），直接取用這個值格式化成戳記，不用自己再查一次
- 戳記放在回覆最開頭第一行
- 這是終端機/桌面版（Claude Code）這個介面的要求，範圍是「這個對話」——小龍蝦(OpenClaw/Telegram/LINE)那邊要不要比照辦理，教練沒有明說涵蓋到那裡，之後若教練提到小龍蝦訊息也要加戳記，再另外評估怎麼在OpenClaw那層實作（可能要透過hook在delivery前加字首，跟rule-reminder是不同機制）
- 不要跟[[feedback_taiwan_time_always]]的核心鐵律搞混：那條是「講到任何時間點都要換算成台灣時間、不能唸UTC」，這條是「每則訊息都主動附時間戳」，兩條同時遵守
