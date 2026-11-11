---
name: feedback-telegram-url-must-stand-alone-2026-10-02
description: 送到Telegram/LINE的網址前後只能換行或空白，緊貼括號中文會被吃進連結點不開；教練點了十幾二十次才講
metadata:
  type: feedback
---

送到 Telegram／LINE（尤其「活動報名即時通知」群）的網址，必須獨立一行，前後不准緊貼全形括號、標點、中文。

**Why:** curation_process.py 通知寫成 `網址（已確認打得開）`，Telegram 把括號一起當連結，教練每次都要複製刪字再貼，做了十幾二十次（2026-10-02 糾正，試金石案例97，commit eae265beb）。

**How to apply:** 寫任何通知/回覆含網址時，網址自己一行；驗證通知要想「教練是在 Telegram 點」，不是只 curl 200。

**第二次（2026-11-11）：** 我回教練 `**https://…/curated/go/**`，後面的 `**` 被算進連結，點開亂碼，教練每次手動刪。同一類（網址前後貼了別的符號），所以不再加新記憶，改成機制：`scripts/stop_rules_master.py` Q 鎖「網址要完整可點」擋下（commit d55e87ef6，試金石案例146）。給教練任何網址＝單獨一行、前後不加 ** 括號 標點 中文。
