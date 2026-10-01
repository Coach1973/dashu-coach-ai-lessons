---
name: feedback-telegram-url-must-stand-alone-2026-10-02
description: 送到Telegram/LINE的網址前後只能換行或空白，緊貼括號中文會被吃進連結點不開；教練點了十幾二十次才講
metadata:
  type: feedback
---

送到 Telegram／LINE（尤其「活動報名即時通知」群）的網址，必須獨立一行，前後不准緊貼全形括號、標點、中文。

**Why:** curation_process.py 通知寫成 `網址（已確認打得開）`，Telegram 把括號一起當連結，教練每次都要複製刪字再貼，做了十幾二十次（2026-10-02 糾正，試金石案例97，commit eae265beb）。

**How to apply:** 寫任何通知/回覆含網址時，網址自己一行；驗證通知要想「教練是在 Telegram 點」，不是只 curl 200。
