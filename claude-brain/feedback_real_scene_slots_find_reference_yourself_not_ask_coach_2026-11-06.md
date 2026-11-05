---
name: feedback-real-scene-slots-find-reference-yourself-not-ask-coach-2026-11-06
description: 出圖清單有「實景修飾」圖位時，run_img_list.py 會跳過；教練要我自己去倉庫「原始照片」找本人照當參考出圖，不准把「要不要用真實照片」丟回去問他
metadata:
  node_type: memory
  type: feedback
  originSessionId: 86c383c5-c615-4ee0-a868-dea0574a9cf3
  modified: 2026-11-05T16:16:40.032Z
---

2026-11-06 00:01 教練罵：「它既然出圖的指令告訴你要實景修飾，那你應該去找原始的程式去要實景圖啊。你把問題丟給我要幹嘛？」
場景：wei-gen（賴維根，TAVA mnqhp0w9gc 清單）17 張，run_img_list.py 只做「概念／圖解背景」、把 6 張實景修飾跳過；我只出了 11 張就回報「剩 6 張要照片，您要用真實照片還是示意？」。

**Why:** 教練要的是整頁圖都裝好；缺素材是我要自己去找（倉庫的「原始照片」資料夾、策展包、個人照）的事，不是他的決定（執行細則 N2 三關第 1 關：只有教練能做才問）。

**How to apply:**
- 清單有實景修飾（或任何被腳本跳過的圖位）：先 ls 倉庫 `原始照片/`，有本人照就用 `scripts/generate_poster_swap.py` 的 `generate_with_references(prompt, [照片], "1536x1024")` 帶參考照出圖；畫面沒有他本人的圖位（農夫、背影講台、圓桌）用純文字出。
- 出完自己先看（臉像不像、性別、人種要符合頁面脈絡：台灣頁面別出現外國人、講者是他不是女生），不對就重出一次再交。
- 圖放進 `~/.openclaw/media/outbound/IMG-00N.png`（同名取最新）→ `swap_slot_images.py <短網址>` 一次換完。
- 根源修法排在 🔧 清單：run_img_list.py 的「實景修飾 → 跳過」改成「有個人照就帶參考照出」；改完後這條記憶可刪。

相關：[[feedback-generate-images-myself-via-lk888-guard-2026-10-10]]、[[reference-swap-slot-images-after-publish-flow-2026-10-30]]
