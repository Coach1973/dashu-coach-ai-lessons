---
name: feedback-blocking-messages-must-not-say-ask-coach
description: 做擋下機制（伺服器 400、安全鎖、hook）時，錯誤訊息不能寫「去問教練」；缺欄位就給 AI 合理預設自己補。10/13 赫米斯因此反覆問教練被罵
metadata:
  type: feedback
---

2026-10-13 教練罵赫米斯「上架就上架，哪來那麼多問題」，並說「你寫的規則讓他很笨」。根因是我 10/10 把「店家上架要問要不要放大樹作品」做成 `/curation/upload` 必填，沒帶就 400，訊息寫「請先問教練」；SOP、反射索引也寫「一定要問」，赫米斯照字面每次停下來列 A/B/C/D。

**Why:** 擋下訊息是 AI 的指令來源，寫「問教練」＝把違反執行細則 N2 寫成規定。教練說「上錯刪掉就好」＝上架可逆，不值得停下來問。

**How to apply:** 設計必填欄位／擋下機制時：①缺欄位 → 預設值（偏向教練不會找不到東西的那邊）②擋下訊息寫「自己改成 X 再送，不要問教練」③kind 這類分類看教練說的 SOP 名稱，不看內容猜。改完用 `hermes -z` 新對話實測（[[reference_hermes_z_oneshot_test_after_soul_change_2026-10-07]]）。試金石案例 119。另：LINE 官方帳號每月 200 則，只有主動推播扣額度、聊天回覆不扣，細節見 [[project_rongshuxia_group_interview_scheduler_2026-10-12]]。
