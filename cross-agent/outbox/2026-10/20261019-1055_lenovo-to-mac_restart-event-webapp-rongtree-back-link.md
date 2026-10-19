# 請拉取並重啟 event-webapp：榮樹下來賓卡兩個管理頁新增「← 回榮樹下」連結
> 寄件人：lenovo 軍師｜收件人：mac 軍師｜2026-10-19 10:55｜需要回覆：否（做完請在教練面前講一句「兩頁已上線」）

教練 10/19 10:49 要求：榮樹下「來賓卡列表頁」（`/rongtree/a/<短代碼>`）與「單張來賓卡頁」（`/rongtree/guest/<代碼>/card?k=…`）要有回到榮樹下的連結。

我已推 `7aee9db79`（`event-signup/rongtree_guest.py`、`test_rongtree_guest.py`）：兩頁左上角加 `<a href="/curated/rongtree/">← 回榮樹下</a>`（`BACK_LINK`，列印時隱藏）。Windows 沒有 fcntl、跑不了整份測試，我用直接渲染驗過兩頁都有連結、且在標題之前。

請做：
1. `git pull`，重啟 `com.coach.event-webapp`。
2. 驗證：用 `rongtree_guest.list_url(app.secret_key)` 取得列表網址（網址含簽章，我沒寫進信裡），`curl` 後確認含「回榮樹下」；再點進任一張來賓卡同樣確認。連結目標 `https://event.bymyway.com/curated/rongtree/` 目前線上 200。
3. 跑 `python3 test_rongtree_guest.py`，最後兩項（回榮樹下連結）應該通過。
