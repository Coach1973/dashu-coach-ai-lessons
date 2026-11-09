---
name: feedback-img-list-lk888-no-ask-routine-authorized
description: 教練給出圖清單網址（TAVA prompts.html）＝直接用 LK888 出圖，不問「要不要花點數」；教練 11/09 嫌問了很不專業
metadata:
  node_type: memory
  type: feedback
  originSessionId: eed47877-ddcf-4da0-b025-dd86ea543d12
  modified: 2026-11-09T03:36:31.445Z
---

11/09 11:36 教練給 bni-story 的 TAVA 出圖清單，我先說「要花點數、先確認」，教練回：「前幾天製作那麼多網頁，哪一次有在問是否同意調用 LK888？你現在問我，我覺得很不專業。」

**Why:** 出圖清單的 LK888 費用是教練每次製作網頁的例行授權，花錢防線已在 `run_img_list.py` 裡（同 prompt 24 小時只付一次、一次最多 12 張、不自動重試）。stop hook 的「花錢要問」是指超出例行範圍的新花費。

**How to apply:** 收到出圖清單網址或「把照片接入某網頁」→ 直接 `run_img_list.py` 出圖→看圖→換進網頁→推上線→線上驗證，一次做完，不問。實景修飾自己找參考照。

**補（同日 11:46）：** 同一場教練連問兩次「為什麼十分鐘都沒回應、不用先跟我說現在什麼情況嗎」——出圖 7 張＋逾時重跑，我悶頭跑沒中途講話。**How to apply:** 任何預計超過 2 分鐘的工作，先一句話講「現在在做什麼、約多久」，之後每 3～5 分鐘補進度；背景跑的任務出第一批成果就先交，不等全部完成。
