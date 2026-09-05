---
name: feedback_shared_file_dual_serve_no_redirect_2026-09-05
description: event.bymyway.com和GitHub Pages共用同一份index.html時絕對不能加轉址頁，會造成無限迴圈——小龍蝦真實踩過的production bug
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bdb4d3d8-b2a2-477a-bea7-9c4e596abd45
  modified: 2026-09-05T14:00:30.914Z
---

在這套系統裡，凡是掛在`event.bymyway.com/<repo>/`底下的網站（`event-signup/app.py`用`_serve_repo_file()`實作），讀取的是`~/github_repos/<repo>/index.html`這份**本機檔案**，跟同一個repo的GitHub Pages（`coach1973.github.io/<repo>/`）用的是同一份檔案——不是兩份獨立內容，是一份檔案被兩個入口各自讀取。

2026-09-05小龍蝦（Telegram/LINE主帳號）想把GitHub Pages導向新家event.bymyway.com，把`lin-beiyi`、`66-harbour`、`tainan-pickleball-art-rotary`三個repo的`index.html`整份改成「本站已搬家，跳轉到event.bymyway.com/xxx」的轉址頁。結果event.bymyway.com讀到的也是這份轉址頁，變成**自己serve一個叫訪客跳回自己的頁面，無限迴圈**——訪客打開event.bymyway.com/lin-beiyi/實際看到的內容就是`<meta http-equiv="refresh" content="0; url=https://event.bymyway.com/lin-beiyi/">`，永遠跳轉下去。此bug存活數小時，直到教練回報「陷入迴圈」才被查出並修復（三個repo還原真實內容，commit`f0fb3cd`/`d212d20`/`de3b46d`）。

**Why（為什麼會犯這個錯）**：直覺上「GitHub Pages導向新家」聽起來合理，但沒意識到`_serve_repo_file()`架構下兩個入口共用同一份原始檔，改一邊等於兩邊都改。

**How to apply（怎麼應用）**：
1. 任何要新增/修改「同時掛GitHub Pages又掛event.bymyway.com」的網站，**不需要、也絕對不能**讓GitHub Pages版做轉址——兩邊各自獨立顯示同一份真實內容本來就沒問題（cica/KR/tainan-shangquan都是這樣運作，沒人覺得需要導向哪一邊）。
2. 如果真的有需求要讓GitHub Pages版轉址（例如要徹底棄用GitHub Pages），必須用**不同的檔案或不同分支**，不能跟event.bymyway.com讀取的`index.html`共用同一份。
3. 改完任何repo-served網站，驗證標準是「打開event.bymyway.com/xxx/親眼看到內容正確」，不能只驗證GitHub Pages那端的HTTP狀態碼——這正是本次JUNSHI_HANDOFF記錄「兩站皆已curl確認200」卻沒抓到迴圈bug的原因，200只代表有回應，不代表內容對。

關聯：[[reference_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]（`_serve_repo_file`架構原始設計）
