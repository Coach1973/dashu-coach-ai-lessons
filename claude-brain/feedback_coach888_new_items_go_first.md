---
name: feedback-coach888-new-items-go-first
description: coach888作品一覽新增項目一律放該分類第一項(num=1)，不要放最後一項——教練找新項目找半天找不到
metadata:
  node_type: memory
  type: feedback
  originSessionId: fa97ce20-02cc-40c2-aaad-1ba7f3961669
  modified: 2026-09-03T02:40:00.000Z
---

教練原話（2026-09-03）：「以後新增的一律放在第一項，不然我找半天也找不到。」

**背景**：這次幫「台南應用科技大學校友會」在coach888「bymyway自架版」分類新增項目時，順手放在該分類最後一項(第7項)，教練找不到（背後還疊加了localStorage舊快照蓋掉新項目的問題，兩個問題一起發生讓教練完全看不到新東西）。

**Why：** 教練不會逐項往下滑找新東西，新增的項目要在第一眼就看到。

**How to apply：** 之後每次在coach888任何分類新增項目，插入位置固定放該`grid`區塊的**第一個**`.item`（`num`從1開始，其餘項目num依序往後推一位），不要放在陣列尾端。這條規則跟原有的「推正式站要同步更新作品總覽」([[project_portfolio_netlify_github_logic]])是同一個流程的下一步微調，不衝突。

Related: [[feedback_column_layout_screenshot_misread_2026-09-02]]（同一個coach888本場另一個易混淆的UI細節）
