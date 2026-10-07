# 專案卡：活動報名/簽到/抽獎後台（event-signup）

- **位置**：`/Users/bymyway/.openclaw/workspace/event-signup`（在 workspace repo 內，**不是** github_repos）
- **正式站**：https://event.bymyway.com （本機 Flask port 5060，launchd `com.coach.event-webapp` + tunnel）
- **⚠️ port 5060 是瀏覽器不安全埠**：本機驗證用 curl，開網頁走 event.bymyway.com（有 hook 攔 Chrome 開 5060）
- **資料庫**：`event.db`——events（場次，含 slug/start_time）、attendees（手機號=同一人身分證，含 company_title/email）、signups（報名/簽到）、advance_registrations（🔴 49筆歷史名單，教練要印簽到表用，**絕不能刪**）
- **核心路由**：`/e/<slug>` 報名表單｜`/checkin` 手機比對簽到｜`/wheel` 抽獎轉盤｜`/admin` 後台｜`/api/register` 大樹小講網站雙寫 JSON 端點（CORS，permissive 永遠回 200）
- **通知**：`_notify_coach_line()` 用龍蝦小助教 LINE token 推播教練｜`_notify_xiaolongxia()` 走 Telegram
- **🔴 測試鐵律**：打 /api/register 成功=真的推播教練 LINE，測試前先講清楚；測完立刻清 attendees+signups 測試資料
- **部署**：改完 `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp` 重啟即生效
- **連動**：大樹小講新增場次必須同輪補 events 表（slug 格式 bigtree-MMDD，同日多場加 start_time）
