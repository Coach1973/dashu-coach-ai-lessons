---
name: memory-write-discipline
description: Use whenever deciding whether to write something into 試金石/distill/memory files. Provides an explicit trigger checklist instead of relying on in-the-moment judgment, plus a sensitive-data check before writing.
---

# 記憶寫入雙鐵律（執行細則 E12，2026-07-10）

對應守則 #01 #14 #15。

## 鐵律一：該不該記，不靠當下心情，靠明確清單

命中以下6種情況之一，直接判定「這件事要記」，不用臨場判斷：

1. 指令執行失敗
2. 教練當場糾正（含語氣重話、口頭指正）
3. 教練要求一個目前不存在的功能/檔案
4. 外部 API／服務呼叫失敗
5. 發現既有記憶檔/守則已經過時、跟現狀不符
6. 發現一個比現行做法更好的方法

同一件事命中多條也只記一次；不同機器（Mac/Windows/VPS）看到同樣6條，判斷標準才會一致。

## 鐵律二：寫入前先過敏感資料檢查

起因：2026-07-10密碼分層時意外發現 MEMORY.md 混進一組真實VPS密碼，是事後抓漏，不是事前防護。

寫入前檢查內容是否含：**密碼／API Key／Token／身分證字號／完整帳號憑證**等敏感字串。命中就先遮蔽，或抽到權限受限的獨立檔案（如`路徑大全_憑證層.md`），再寫入敘事型記憶檔。不能靠「反正之後會發現」。

## 補充：教練的每一句話都值得記（守則#13 #01）

教練說的每一句話都是用生命換來的指導——語音輸入每分鐘200字，26年培訓經驗的心血。教練發言自動視為「需要記錄」，不問、不確認、不猶豫。教練提到任何比喻，背後都藏著他重視的價值觀，是線索，要理解並記下。
