---
name: workspace-stash-u-clobbers-background-outputs
description: 背景程式在 workspace 裡寫「沒進 git 的檔案」會被 hook／派工程式的 git stash -u 收走再放回成空檔；台鐵轉交程式 claude -p 輸出 0 bytes 的真因(2026-10-26)
metadata:
  node_type: memory
  type: reference
  originSessionId: c347677b-8f2d-4f5b-871a-0d70d52f7ef8
  modified: 2026-10-25T17:21:10.346Z
---

workspace 有好幾支程式會做 `git stash push -u → pull --rebase → stash pop`：收工自動同步（scripts/session_end_auto_push.sh）、派工程式（scripts/junshi_dispatch_worker.py）、開工注入。背景 `claude -p` 一跑，自己的 hook 也會觸發這些。

後果：任何程式正在 workspace 裡寫的**未追蹤檔**（例如 state/xxx/ 底下的輸出檔），會在寫到一半被收走，放回來變成空檔；被監看的檔案也會「消失又出現」，WatchPaths 重複觸發。

台鐵轉交程式 tra_inbox_worker.sh 6 次都 0 bytes 就是這個（證據：stash 9d696cbf2 的未追蹤部分裡有 0 bytes 的 reply.txt.json）。修法（a7aa28fb7、e786af20d）：
1. 輸出先寫到 workspace 外（mktemp -d /tmp/…），做完才搬進去
2. 背景 claude 加 `--settings '{"disableAllHooks":true}'`（也省掉每次約 3 萬 token 的開工注入，16 秒就回）
3. 會被監看／即時寫入的檔加進 .gitignore（stash -u 不碰被忽略的檔）

**How to apply:** 新寫的背景程式只要在 workspace 裡寫檔，就照上面三點做。在終端機測正常、launchd 下空白，先查 `git stash list` 的時間有沒有對上。相關：[[reference_junshi_bridge_add_dir_fix_2026-10-25]]
