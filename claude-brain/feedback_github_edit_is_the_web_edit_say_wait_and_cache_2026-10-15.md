---
name: feedback_github_edit_is_the_web_edit_say_wait_and_cache_2026-10-15
description: 教練說「你改了 GitHub 為什麼網頁沒改，那我叫你改網頁就好」：GitHub Pages 網頁就是倉庫本身、部署要 1～2 分鐘、瀏覽器快取 10 分鐘；改完要自己確認線上版並把「可能要等／強制重新整理」講在第一次回報
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4aac7f25-d657-43c8-a422-e28fd94a634d
  modified: 2026-10-15T17:52:40.742Z
---

2026-10-15 20:44 教練在我改完張麗蝶 lidie 學歷後糾正：「你改了 GitHub，為什麼網頁上沒有跟著改？那我剛才就叫你改網頁就好了。」

**Why:** 教練不分「GitHub」與「網頁」，認為改 GitHub＝改網頁，推完卻看不到新字就是我沒做完。當時第一次線上檢查還是舊的，我隔一會兒才看到更新，卻沒把「部署要等 1～2 分鐘＋瀏覽器快取 10 分鐘」講在第一次回報。另外 10/15 21:05 Mac 軍師查出：event.bymyway.com/curated 的網站讀 Mac 本機 clone，靠 GitHub webhook 同步，lidie 漏掛 webhook，所以 GitHub 改了正式站 10 分鐘沒換新（已補掛並修上架流程）。

**How to apply:** ①改教練給的網址，改完一律用 curl（加隨機參數）驗證線上版有新字才說「已更新」，沒更新先重試／查 `gh api .../pages/builds/latest`。②第一次回報就講：「已推上、線上已確認；若您看到舊的，按 Ctrl+F5」。③不要讓教練在「GitHub／網頁」兩個詞之間做選擇，一律說「網頁已改好」。④Pages 狀態 errored 時可 `gh api -X POST repos/<repo>/pages/builds` 手動重跑。相關：[[reference_lenovo_memory_ntfs_nonpaged_pool_leak_2026-10-15]]（同日其他事）。
