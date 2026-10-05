---
name: reference-industry-service-chain-term
description: 「產業服務鏈」是 BNI 專用術語（大家共同來服務一個特定族群）；語音常被辨識成「產業服務列」「產業伏變」，聽到都是它，對應 knowledges/SOP_產業鏈.md，從 905 項專業清單生成
metadata:
  node_type: memory
  type: reference
---

教練 2026-10-06 00:29 糾正：10/04 AI 企業團隊戰略對話裡的「產業服務列」「產業伏變」是語音辨識錯字，正確是「**產業服務鏈**」。這是 **BNI 專用術語：大家共同來服務一個特定族群**。

**怎麼對應**
- 做法就是 `knowledges/SOP_產業鏈.md`（教練簡稱「產業鏈SOP」、也叫「[類別]夥伴圖」）；節點從 `namecard-db/taxonomy.json` 的 905 項專業清單生成，教練確認「沒有問題」。
- 小龍蝦實際執行的 `agents/main/agent/workshop-skills/industry-chain-prompt/SKILL.md` 早就認得「產業服務鏈」；SOP 檔頭 10/06 補上口語叫法與這兩個錯字。

**Why：** 我 10/06 00:14 把它猜成「產業鏈服務圖」並寫進 `docs/source/README.md`，詞對了一半（意思對、字不對）；教練當場糾正。

**How to apply：** 教練或文件裡出現「產業服務列」「產業伏變」「產業服務鏈」→ 一律當作產業服務鏈，直接走產業鏈SOP，不用再問（守則#18 已由此條確認過）。

Related: [[feedback_search_namecard_db_before_claiming_taxonomy_missing_2026-09-23]]、[[project_100_cases_youtube_unlisted_text_first_2026-10-06]]
