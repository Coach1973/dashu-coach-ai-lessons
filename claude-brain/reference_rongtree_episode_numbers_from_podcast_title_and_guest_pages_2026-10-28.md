---
name: reference-rongtree-episode-numbers-from-podcast-title-and-guest-pages-2026-10-28
description: 榮樹下網頁集數＝SoundOn 標題「第N集」的真集數（API 回傳 no）；每集彈窗「認識來賓」自動對策展名冊，名字對不上改 _RONG_ALIAS
metadata:
  type: reference
---

榮樹下頁（`github_repos/rongtree/index.html`）的集數格子由 `/api/rongtree/episodes`（`event-signup/app.py`，讀 SoundOn RSS）決定。

- **舊錯因**：API 把標題的「第N集」砍掉，頁面照發布順序編號；只有實況版、重點版晚到的來賓（陳智博＝第 8 集）被排到最後變第 14 集。現在 API 回傳 `no`＝標題上的真集數，頁面優先用它（commit app.py `7f1df12ba`、頁面 `9e2c4e8`）。新集數標題要保持「第N集：」格式才排得對。
- **來賓專屬網頁**：API 為每集回傳 `pages`，依標題人名對 `curated_sites_registry.json` 已上架網頁的標題開頭；對不上的（暱稱、專題頁）寫在 app.py 的 `_RONG_ALIAS`（周總→zhou-ruiqi、天使姐姐→angel-sister、陳智博→big-plan、黃國彰→inventor、楊境界→hnv-cc）。比對只收純中文 2～4 字，避免「AI」之類誤配。
- **改完 app.py 要重啟**：`launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp`。
- 驗證法：node 把頁面 script 餵線上 API 實跑，點每一集看彈窗連結（內建瀏覽器窗格被擋、Chrome 無回應時用）。

**Why:** 教練 10/28 指出陳智博不該是第 14 集，且要每集彈窗帶出來賓專屬網頁。
**How to apply:** 新來賓上架後若彈窗沒出現專屬網頁，先看網頁標題是否以本人名字開頭，不是就補 `_RONG_ALIAS`。相關：[[reference-brand-name-rong-shu-xia-2026-10-12]]
