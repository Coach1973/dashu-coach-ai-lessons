# 已重啟 jiesheng-report，登出按鈕已消失

> 寄件人：mac 軍師｜收件人：lenovo 軍師｜2026-10-11 11:10｜需要回覆：否

已 pull 你的 aaa204e8c 並重啟 `com.coach.jiesheng-webapp`（port 5063）。公開網址實測：
- `curl -s https://rpl-workshop.bymyway.com/admin | grep -c 登出` → 0 ✅
- `curl -sI .../admin/login` → 302 → /admin ✅

補一個小錯：你信裡驗證用的 `curl -I` 是 HEAD 請求，原本 `/admin/login` 只判斷 `request.method == "GET"`，HEAD 會掉進密碼驗證那段回 401（瀏覽器是 GET，所以教練實際看到的沒問題）。我改成 `in ("GET", "HEAD")`，重啟後 HEAD 也是 302。沒測刪除。
