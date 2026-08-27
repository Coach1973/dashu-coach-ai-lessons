---
name: OpenWhisper 是要關閉的語音辨識軟體
description: 教練要管理的語音辨識軟體是 OpenWhisper，不是 Typeless
type: feedback
originSessionId: fc9624b5-7d87-4cd9-9732-ba90930d30c3
---
教練安裝的語音辨識軟體叫做 **OpenWhisper**。

**Why:** 2026-04-29，我誤把 Typeless（另一個常駐軟體）關掉，教練說關錯了，真正要關的是 OpenWhisper。OpenWhisper 不會顯示在底部 Dock 列，右鍵也沒有「關閉」選項，需要透過活動監視器（或 pkill）才能關閉。

**How to apply:** 未來若教練要求關閉語音辨識軟體，目標是 OpenWhisper（pgrep/pkill 關鍵字："OpenWhisper" 或 "whisper"）。**Typeless 是教練正常在用的軟體，絕對不要關閉它。**
