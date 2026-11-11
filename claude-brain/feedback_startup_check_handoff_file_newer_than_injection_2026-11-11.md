---
name: feedback-startup-check-handoff-file-newer-than-injection
description: 開工注入的接力棒可能比檔案舊（別的對話框剛收工）；回報前看 JUNSHI_HANDOFF_LATEST.md 第一行時間，比注入新就以檔案為準
metadata:
  type: feedback
---
2026-11-11 08:44 教練說「開工」，hook 注入的是 08:01 那棒；另一個對話框 08:45 才收工寫進 bni-story 第 2 棒交辦。我照注入回「沒有交辦，今天從哪件事開始？」，教練：「你再重新讀一下。開工，當然有很重要的事情讓你做啊，怎麼還問？」

**Why:** 教練常在一個對話框說「總」後立刻開新對話框說「開工」，兩邊相差一兩分鐘，注入會抓到舊棒。
**How to apply:** 開工回報前 `head -1 workspace/JUNSHI_HANDOFF_LATEST.md` 和 `git log -3`，若最新一棒時間比注入的新，以檔案為準並直接開始那棒的「下一步」。永遠不要在教練說「開工」後回「沒有交辦」而不先查檔案本身。
