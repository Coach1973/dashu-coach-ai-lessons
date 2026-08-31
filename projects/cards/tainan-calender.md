# 專案卡：BNI大台南培訓行事曆（tainan-calender）

- **🎯 owner：Hermes**（2026-08-31教練拍板，網站內容維運類任務預設交Hermes，見`cross-agent/README.md`任務分工鐵律）
- **repo**：`/Users/bymyway/github_repos/tainan-calender`
- **正式站**：https://tainan-calender.netlify.app
- **部署型態**：Netlify 手動 zip 推型——**教練說「推」才部署**；zip 必含 `_headers`（曾因缺它整頁顯示原始碼）
- **資料來源**：bni_tainan agent 的行事曆同步 cron（`7048432e`，每4小時）抓官方行事曆 → `agents/bni_tainan/knowledge/tainan_calendar.md`
- **血淚**：`parseDateScore()` 要能解析無斜線 MMDD 格式（0905-0906），否則全站排序錯亂（已修）
- **近期**：新領導團隊培訓已改期 9/21（一）ZOOM 線上
