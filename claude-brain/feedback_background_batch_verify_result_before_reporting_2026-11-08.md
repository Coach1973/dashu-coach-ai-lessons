---
name: feedback-background-batch-verify-result-before-reporting-2026-11-08
description: 背景批次（ffmpeg 轉 64 支 MP3）我寫錯參數全失敗，卻因為「背景程序完成」通知就回報「轉換中」；ffmpeg 的 -f mp3 要放在輸出檔名前面；背景工作回報前要讀實際結果
metadata:
  node_type: memory
  type: feedback
  originSessionId: c1744500-5b3a-42b0-886c-c829250f3b2f
  modified: 2026-11-08T12:04:47.969Z
---

11/08 轉高價銷售課程 64 支 MP3：我把 `-f mp3` 放在輸出檔名後面，ffmpeg 報「Unable to choose an output format」，64 支秒失敗、一個檔都沒產生。我先前包 `& sleep 45; cat log` 的指令讓「背景工作完成」通知提早回來，**沒讀 log 就跟教練說「已在背景轉換中」**，使用者中斷後才查出全失敗，才更正重跑（4 分鐘後 64/64、逐支比對長度零差異）。

**Why:** 守則 #03（結論前自己看過）、#05（說完成要有憑證）。背景通知只代表那條 shell 指令結束，不代表任務成功。
**How to apply:** ①ffmpeg 指令固定寫 `-i 輸入 … -f mp3 輸出.mp3`（輸出選項放輸出檔名前）；②背景批次回報前一定讀 log 看 ok／FAIL 數與實際檔案數；③批次先試跑 1 支確認有產檔再丟全部；④用「等 DONE 字樣」的背景等待，不要用 sleep 假裝進度。
