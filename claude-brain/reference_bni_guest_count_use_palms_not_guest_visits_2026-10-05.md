---
name: reference_bni_guest_count_use_palms_not_guest_visits_2026-10-05
description: BNI 會員帶來賓人數一律用 PALMS（BNI-Training/guests_data.json，同 /guests），名片庫 guest_visits.invited_by 手打漏很多；培訓用 /training 的 data.json＋data_msp.json
metadata:
  type: reference
---
- **帶來賓人數**：BNI 官方「PALMS 摘要報告」來賓欄，檔案 `~/github_repos/BNI-Training/guests_data.json`（巢狀快照：近 1、2、3…97 個月，截至 2026-09-01；真鑽／真誠／真鑫才有），公開頁 https://chapters.bymyway.com/guests 。教練 2026-09-01 定為唯一依據。
- **不要用** `workspace/namecard-db/namecards.db` 的 `guest_visits.invited_by` 算人數：邀請人是手打的，漏很多（郭政輝 97 vs 官方 303、康文彬 158 vs 254）。它只適合查「某位來賓是誰帶的」。
- **培訓場數**：`BNI-Training/data.json`（同 /training，官方報表＋教練自己開的 MSP 課，截至 8/17）＋ `data_msp.json` 之後的場次（9/7、9/10…）。`claude-brain/data/bni_region_training_raw.json` 少了 MSP 課。
- 信任裝備探測器的匯入程式 `~/github_repos/bni-chapters/import_detector_stats_2026-10-05.py` 已照這套來源寫好。

**Why:** 2026-10-05 探測器第一版用錯來源上線，教練拿 /guests 一對就抓到（試金石案例105）。
**How to apply:** 只要畫面要顯示會員帶來賓或培訓數字，先對 /guests、/training 同一份；兩邊不一致以 PALMS 為準。相關：[[reference_bni_induction_dates_in_training_raw_2026-10-04]]、[[project_business_club_game_design_principles_2026-10-03]]
