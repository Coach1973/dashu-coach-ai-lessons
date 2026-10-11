---
name: feedback-check-what-url-the-overview-holds-first-2026-10-12
description: 教練說某網頁「跟作品一覽裡的不一樣」時，先查作品一覽(coach888 狀態)實際放的是哪個網址是否404，不要只比對網頁本身
metadata:
  type: feedback
---

教練 10/11 說 `curated/ema1017/` 跟作品一覽不一樣，我只比對網頁與 GitHub、猜是標題逗號；真相是作品一覽「近期活動」放的是已 404 的 `ai-class-1017`，`ema1017` 被丟進「最近刪除」。教練反問「你居然不知道裡面是錯誤的？」。
**Why:** 「作品一覽」是伺服器狀態（`/api/coach888/state` 的 layout／names／badges，值是 JSON 字串），不是網頁本身；壞連結是最常見的差異。
**How to apply:** 遇到「跟作品一覽不一樣」→ 先抓 state 解析出該項放的網址與所在分類，`curl` 狀態碼；改前備份（存到 workspace/state/）、只動該筆、讀回核對。順便掃全部網址一次（123 個約 1 分鐘）。
