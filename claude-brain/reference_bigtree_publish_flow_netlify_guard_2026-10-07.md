---
name: reference-bigtree-publish-flow-netlify-guard
description: 大樹小講新增／改場次後要上 Netlify 的正確做法：event.db 為唯一真相源，用 bigtree_publish 的 diff_summary 預覽再 publish；hook 要求指令最開頭帶 NETLIFY_DEPLOY_CONFIRMED=1，要用 event-signup 的 venv python
metadata:
  type: reference
---

**三個大樹小講網址**：`event.bymyway.com/bigtree/`（主力，動態讀 event.db，改資料庫立刻生效）；`bigtree-tw.netlify.app`（靜態，要發佈）；GitHub Pages（備援）。**官網**＝www.bymyway.com，不是這些。

**新增／改場次流程（10/07 加 ema1017 用過）**：①`event.db` 的 events 表（`site='bigtree'`、`status='active'`）是唯一真相源 ②先預覽：`NETLIFY_DEPLOY_CONFIRMED=1 /Users/bymyway/.openclaw/workspace/event-signup/venv/bin/python3 - <<EOF …bigtree_publish.diff_summary(db.get_conn())…` 看「新增／下架／修改」，確認沒有意外變動（過期場次會自動下架；Netlify 那份常比動態頁舊） ③確認後 `publish(conn, message=…)`：寫檔→只 `git add index.html`→commit/push→用 `git archive HEAD` 打包（不夾帶未提交檔）→部署→扣額度。

**坑**：`netlify_deploy_guard.sh` 偵測到指令含 `bigtree_publish` 就擋，且 `NETLIFY_DEPLOY_CONFIRMED=1` 必須是**整條指令的最開頭**（前面不能有 `cd … &&`，要在 Python 裡 `os.chdir`）；連 `sed` 讀那個檔名都會被擋，改用 Read 工具。系統 `/usr/bin/python3` 是 3.9，`X | None` 型別標註會報錯，要用 webapp 的 venv python。教練 09-23 已鬆綁「Netlify 不用每次先問」，但新場次公開上線仍先取得他的同意（10/07 是他說「可以列」）。
