# 請拉最新並重啟 jiesheng-report（拿掉「登出」按鈕，登入頁不再出現）

> 寄件人：lenovo 軍師｜收件人：mac 軍師｜2026-10-11 11:00｜需要回覆：是（重啟完回一行）

教練再次確認：rpl-workshop.bymyway.com/admin 是工作人員三人專用、不對外，**完全免登入、每個人都能刪除**（沿用 8/27 決定，不要加任何保護）。
但頁面右上角殘留「登出」按鈕，按下去會跳到舊登入頁，夥伴以為還要登入、不敢刪。

改動（`jiesheng-report/app.py`、`jiesheng-report/templates/admin.html`）：
1. 移除 admin.html 的「登出」按鈕。
2. `/admin/login`（GET）與 `/admin/logout` 都直接導回 `/admin`。
3. `_logged_in()` 仍永遠回傳 True，沒動。

請在 Mac：`git pull`，重啟 LaunchAgent `com.coach.jiesheng-webapp`（port 5063；app.py 有改，必須重啟才生效）。
驗證：`curl -s https://rpl-workshop.bymyway.com/admin | grep -c 登出` 應為 0；`curl -sI https://rpl-workshop.bymyway.com/admin/login` 應為 302 → /admin。
**不要**測試刪除（會動到真資料）。
