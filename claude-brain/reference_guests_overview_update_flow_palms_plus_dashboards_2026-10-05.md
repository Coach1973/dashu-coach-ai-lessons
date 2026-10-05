---
name: reference_guests_overview_update_flow_palms_plus_dashboards_2026-10-05
description: 來賓總覽(chapters.bymyway.com/guests)怎麼更新：PALMS報表到某日＋之後由各分會戰情表來賓名單補上；BNI Connect 地區PALMS報表一份含全部分會；要的月數節點與日期範圍
metadata:
  type: reference
---
**來賓總覽 = 官方 PALMS 報表（到 8/31）＋ 9/1 起三個戰情表每週來賓名單的邀請人**（教練 2026-10-05 定：「從戰情表最新資訊更新回來賓總表，這樣你就不用進 Connect 查」）。
- 戰情表資料庫（唯讀）：`~/github_repos/zhenzuan-guests/zhenzuan_guests.db`（真鑽）、`zhenxin-guests/zhenxin_guests.db`、`zhencheng-guests/zhencheng_guests.db`，表 `guest_list(week_date, name, inviter)`。
- 重做：`cd ~/github_repos/BNI-Training && python3 guests_build_data.py && python3 guests_build_html.py`，再 commit/push；chapters.bymyway.com/guests 讀這個檔，立刻生效。探測器同步：`cd ~/github_repos/bni-chapters && venv/bin/python import_detector_stats_2026-10-05.py real-diamonds sincere`。
- 「只用『至』＝最新匯出日的報表」：建置程式會跳過其他區間（例如只含 4 月、或 2023-09～2024-05 的檔）。月數照天數換算（8/31 起算 12、18、24、36）。
- 要新增月數節點（只在要更精確或新增按鈕時）：BNI Connect 報告→分會→「分會 - PALMS摘要報告」，或**「地區 PALMS 報告摘要」一份就含所有分會**（教練 10/05 用這個最省事）。日期要用日曆點選，打字無效；結束日跟現有報表一致（目前 2026-08-31），開始日用月初：18 個月＝2025-03-01、36 個月＝2023-09-01。
- 戰情表以外的週報：真鑽「本週會議出席報告」教練貼文字，我用 `zhenzuan-guests/import_weekly_reports_2026-10-05.py` 的格式轉進戰情表（每週逐項核對週報人數）。
- BNI Connect 技術備忘：分會切換是頁首 `a#bniChapter` 下拉（真富42515、真愛44080、真誠31215、真鑫44081、真鑽23528、真心31243、真拾31242、真美32932）；選單是 JS 點擊式、`find` 看不到；背景 fetch POST 報表會被導回、不能用，得讓教練本人在畫面上按「開始」匯出。

**Why:** 2026-10-05 我因為不知道戰情表已有每週來賓資料，打算進 Connect 抓 40 份報表，被教練問「花多少 tokens」。
**How to apply:** 更新來賓數字先看戰情表有沒有資料，再決定要不要請教練匯 PALMS。相關：[[reference_bni_guest_count_use_palms_not_guest_visits_2026-10-05]]

**每月燈號（探測器）**：教練每月下載地區 PALMS（近 6 個月）算燈號，也會存 BNI Connect 官方「會員紅綠燈 - 分會 (年-月).xlsx」到下載資料夾。我用 `cd ~/github_repos/bni-chapters && python3 import_light_scores_2026-10-05.py`（系統 python3，要 openpyxl）一次匯入：官方 xlsx 優先，PALMS 報表照 `event.bymyway.com/bni-traffic/` 算法換算（程式 `github_repos/bni-traffic/index.html`，2026-10-05 用真鑽 2026-09 官方 47 人逐一比對，一致）。探測器的最近燈號與連續綠燈／連續完美月數由此自動算。
