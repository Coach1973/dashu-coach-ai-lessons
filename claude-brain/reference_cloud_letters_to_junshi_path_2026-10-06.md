---
name: reference-cloud-letters-to-junshi-path-2026-10-06
description: 雲端對話(bni-chapters)寫給軍師的信固定放分支 docs/to_junshi/，Mac 開工與讀信用 scripts/cloud_letters.sh 自動掃；雲端碰不到 cross-agent/inbox/mac
metadata:
  type: reference
---

雲端對話（Claude Code 雲端，只接了 bni-chapters 倉庫）碰不到 workspace 的 `cross-agent/inbox/mac/`，而 bni-chapters/CLAUDE.md 原本沒寫信放哪，所以 10/06 雲端的交接信放在 `docs/letter_to_junshi_2026-10-06.md`（自己分支），Mac 的「讀信」和開工只看 inbox/mac，沒掃到，教練被迫叫人開頁面複製貼上（守則 #12）。

**Why:** 教練 10/06 14:28 追問「雲端寫信為什麼軍師收不到、要給他正確路徑」。根因是雲端那邊沒有路徑規定、Mac 這邊也沒掃雲端分支，兩頭都漏。

**How to apply:**
- 雲端寫信固定放自己分支 `docs/to_junshi/YYYYMMDD-HHMM_cloud-to-mac_主題.md` 並推上雲端（已寫進 bni-chapters/CLAUDE.md，master `afa34c4`；新雲端對話才會讀到，已開著的舊對話要提醒一次）。
- Mac 端：`bash scripts/cloud_letters.sh list|cat|mark`，掃 bni-chapters 所有遠端分支，以檔案內容雜湊記已讀（state/cloud_letters_read.txt）；開工 hook（feed_junshi_handoff.sh）有未讀就列在最前面，「讀信」反射 R-CROSS-LETTER 也會叫跑它。
- 新增別的雲端倉庫：改 cloud_letters.sh 的 REPOS（或環境變數 CLOUD_LETTERS_REPOS），並在該倉庫 CLAUDE.md 補同一段。
- 雲端若接的是 workspace 倉庫，直接寫 cross-agent/inbox/mac/ 即可，不用走這條。
