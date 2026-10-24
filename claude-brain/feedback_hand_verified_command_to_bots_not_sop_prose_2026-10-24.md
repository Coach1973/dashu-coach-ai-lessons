---
name: feedback-hand-verified-command-to-bots-not-sop-prose-2026-10-24
description: 我驗證有效的做法要做成「一行指令」交給巴哈等分身，不能只寫成 SOP 文字讓它自己摸索；林家羽海報巴哈花 10 分鐘翻資料寫提示詞被教練罵
metadata:
  type: feedback
---

10/24 20:11 佩佩老師丟林家羽照片＋職稱，巴哈 10 分鐘都在讀 SOP、翻舊提示詞、查名片庫、裁照片，還選錯成舊羅爵模板。教練：「它 10 分鐘耗在自行摸索提示詞，那為什麼你沒有把已經驗證有效的東西直接寫給它呢？這不就是你的問題嗎？」

修法：`scripts/poster_new_person.py`（--photo --name --role --titles，橫直版同時出、約 1 分鐘、存 JPEG），巴哈 SOP 最上面與 SOUL.md 改成「只跑這一行」。橫版小字 AI 仍會寫錯（人壽→人蘇），要放大看、錯了用 PIL 貼字。

**Why:** 分身是 MiniMax、照文字自己推理很慢又易錯；教練邏輯「你能做它就能做，因為背後都是 LK888」。
**How to apply:** 我做成功一件分身以後會重複做的事，同一輪就包成一行指令＋寫進分身 SOP 最上面，不只寫說明文字。相關 [[reference_poster_swap_lk888_two_images_bahai_sop_2026-10-22]]。
