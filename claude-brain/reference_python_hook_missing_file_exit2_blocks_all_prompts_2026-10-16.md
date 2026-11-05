---
name: reference-python-hook-missing-file-exit2-blocks-all-prompts-2026-10-16
description: Hook 腳本檔不見時 Python 結束代碼是 2，Claude Code 把 UserPromptSubmit 的 exit 2 當成擋下訊息，導致手機／Mac 所有 Claude 對話叫不動；雲端可用 list_events 讀手機橋接對話查錯
metadata:
  node_type: memory
  type: reference
  originSessionId: session_01A4aKmGDLzxQGhUuLSk6yqz
  modified: 2026-10-16T10:30:00.000Z
---

# Hook 腳本不見 → 每句話都被擋（2026-10-16 15:12～18:2x 台灣時間）

**現象**：教練從手機或 Mac 本機對 Claude 說任何話都沒反應，畫面只出現
`UserPromptSubmit operation blocked by hook: [/usr/bin/env python3 .../scripts/reflex_router.py prompt]: ... can't open file ... [Errno 2] No such file or directory`。

**機制（雲端實測）**：`python3 不存在的檔案.py` 結束代碼是 **2**。Claude Code 規定 UserPromptSubmit hook 回傳 2＝擋下這句話。所以「腳本檔不見」不是警告，而是讓整個 Claude 癱瘓。

**怎麼查（雲端也查得到）**：Mac 癱瘓時，雲端對話可用 `list_sessions(mine=true)` 找 `environment_kind: bridge` 的手機對話，再用 `list_events(kinds=["user","result"])` 讀到每則訊息被擋的原文與耗時（54～78 毫秒＝沒呼叫模型）。

**怎麼解**：在 Mac「終端機」（不是 Claude 對話框，不會被擋）從 origin/main 只補回不存在的檔案：
`cd ~/.openclaw/workspace && git fetch -q origin main && git ls-tree -r -z --name-only origin/main -- scripts | while IFS= read -r -d '' f; do [ -e "$f" ] || printf '%s\0' "$f"; done > /tmp/m.nul; git --literal-pathspecs restore --source=origin/main --worktree --pathspec-from-file=/tmp/m.nul --pathspec-file-nul`

**根治（待 Mac 做）**：settings.json 的 hook 指令改成「檔案在才跑，不在就 exit 0 並印提醒給 AI」，見接力棒 2026-10-16 18:29 棒第 4 點。這是同類第二次（9/18 hooks 目錄也從工作區消失過），要改機制，不要再加記憶。

**雲端限制**：雲端連不到 event.bymyway.com（網路規則 403），WebFetch 連 example.com 都解析不到，無法從雲端驗網站，要回 Mac 驗。

**教練原話線索**：「它阻止我，那我接下來要幹嘛呢？什麼也沒講，就貼一個這個東西阻止我」→ 任何擋下教練的訊息都要附白話的下一步。
