---
name: reference-bni-induction-dates-in-training-raw-2026-10-04
description: BNI 會員年資唯一依據＝BNI Connect「會員資格會期報告」的「最近會齡」(教練10-04下載，存 claude-brain/data/bni_membership_tenure_report_2026-10-04.csv)；累計會齡只當歷史
metadata:
  type: reference
---

- **年資一律看「最近會齡」**（教練 2026-10-04 21:03 定）：BNI Connect「會員資格會期報告」，存 `workspace/claude-brain/data/bni_membership_tenure_report_2026-10-04.csv`（原始 `_原始.xls`，大台南南區 84 位：真鑽47／真誠17／真鑫17／真富2／真愛1）。
  - **累計會齡**＝所有 BNI 時間加總（含離會前、在別的分會）；**最近會齡**＝這次入會、在這個分會連續到現在。離會再回來，最近會齡重算（例：李紫妤累計 7 年 2 個月、最近 6 年 3 個月，2020-07 起；真誠李美花累計 8 年 1 個月、最近 6 年 2 個月）。
  - 籌備會期間不算，會期從正式例會開始（康文彬 2019-01 起＝7 年 9 個月；本人說「8 年」是把籌備期算進去，一律以報告為準）。
  - 報告日期是月份精度（YYYY-MM-01）。
- 舊來源 `claude-brain/data/bni_region_training_raw.json` 的 `induction_date`（2026-08-18 培訓報表）跟會期報告差幾天到一個月，**不要再拿來算年資**。
- 教練語音常見同音：康文斌＝康文彬、陳文成＝陳坤成、蘇志陽＝蘇志揚。
- **帶來賓**：`namecard-db/namecards.db` guest_visits（invited_by 格式「康 文彬」有空格要先去掉），真鑽 2018-08-14 起 2,910 筆。
- 分會現任人數以最新**菁英表**為準（真鑽 47＝會期報告 47，已離會的柯朝陽、蘇志揚不算）。
- 用途：信任遊戲探測器「系統已確認」裝備，見 `knowledges/2026-10-04_信任遊戲_信任裝備探測器_可行方案v1.md` 第六節。
- 相關：[[feedback-elite-list-is-master-no-reentry-2026-10-04]]、[[feedback-bni-member-db-authoritative-source]]
- ⚠️ **會期報告會留已離會的人**：10/04 匯出的報告真誠有 17 位，其中郭素玲、盧尚政教練 10/05 確認已離會。分會現任名單一律以教練給的菁英表／夥伴 PPT PDF 為準，會期報告只拿來查會齡，不拿來加人。
