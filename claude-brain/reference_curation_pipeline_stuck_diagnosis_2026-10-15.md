---
name: reference-curation-pipeline-stuck-diagnosis-2026-10-15
description: 教練上傳作品後「收到新檔案」通知有、「上架完成」通知沒來＝處理程序卡住；怎麼查（ps/sample/processing 資料夾）、怎麼救、10/15 根因（圖片瘦身 regex 平方級）
metadata:
  type: reference
---

**症狀**：Telegram 只有「📦 收到新檔案…背景處理中」，沒有「完成」通知（10/15 chen-shuling 包等了 15 分鐘；10/13 真公益包同病）。

**查法（唯讀）**：`python3 scripts/curation_check_result.py <關鍵字>` 回 pending／processing/；`ps aux | grep curation_process`（正常幾十秒就結束，CPU 100% 超過幾分鐘＝卡死）；`sample <pid> 2` 看 Python 堆疊；`event-signup/curation_uploads/watch.log` 最後一行；包還在 `processing/` 不會自動重跑。

**救法**：kill 卡住的 python → 把 `processing/` 裡該包連 `.slug/.kind/.works` 搬回 `incoming/`（launchd WatchPaths 會自動重跑，incoming 裡排隊的包也一起處理）→ 用 curation_check_result 與線上網址驗證。

**10/15 根因**：`scripts/optimize_site_assets.py::_rewrite_refs` 用 `[^\s"'()<>,=]*檔名` 的 regex，遇到 10MB 內嵌 base64 圖片（整段沒空白）變平方級。已改線性寫法＋`scripts/test_optimize_rewrite_refs.py` 15 項（commit `2b3ae30b5`）。

**Why**：教練以為通知沒來是 Telegram 壞了。**How to apply**：通知缺「完成」先查程序是否卡住，不要先猜通知管道；上傳 HTML 單檔 >5MB（內嵌圖片）時留意處理時間。
