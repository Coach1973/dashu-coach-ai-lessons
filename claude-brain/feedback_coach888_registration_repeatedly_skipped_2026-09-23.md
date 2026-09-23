---
name: feedback-coach888-registration-repeatedly-skipped
description: 教練自己的公開作品上架時，忘記同步登記進coach888「AI作品一覽」，教練說這是重複發生的問題，規則早就存在但只靠記憶檔沒有落實
metadata:
  type: feedback
---

# 🔴🔴 coach888登記規則早就寫了，卻一犯再犯——這條需要hook，不能只靠記憶檔

**Why**：2026-09-23，ai-story漫畫上架event.bymyway.com後，教練問「有收錄進AI作品一覽嗎」，查證發現沒有——事後才想起`reference_curation_sop_2026-09-06.md`第56~57行早就白紙黑字寫「教練自己的作品→收coach888」（2026-09-05教練親定），這條規則不是不存在，是**執行時沒有真的照著走**。教練當場質問「之前不是說過了...為什麼這件事情老是忘記呢」——這句話的語氣顯示這不是第一次，是重複型缺失。

跟[[feedback_taiwan_time_always]]、[[feedback_no_background_polling_lies]]同一個模式：**光寫進記憶檔/SOP文件沒用，AI不會每次主動翻出來對照**，尤其當這條規則寫在「另一份」SOP文件裡（策展SOP），而我當下在跑的是「新建立的」個人創作SOP文件時，就更容易漏掉——因為我只顧著寫新文件本身的邏輯，沒有回頭確認舊文件裡有沒有這類「收尾動作」需要一併繼承。

**How to apply**：
- 已把「登記coach888」這一步直接寫進[[SOP_教練個人創作上架event.bymyway.com不進商圈]]文件本身的第6步，跟「上架」動作綁在同一份checklist，不是另外一份文件裡的規則。
- 任何時候要幫教練建立/複製一份新的「上架SOP」文件，動手前先檢查舊有相關SOP文件裡有沒有「收尾/登記」類的隱藏步驟一併繼承過來，不能只看新任務本身的邏輯。
- 這個模式已經出現到需要**hook層級的deterministic check**，不能再靠「寫進memory」這種軟性提醒——下一步：檢查`curated_sites_registry.json`新增`category`含「教練個人創作」或「策展」且非店家名冊(`no_shop_card:true`)的項目時，同一個session/同一天內`coach888`repo有沒有對應commit，沒有就在Stop hook攔下來提醒。這件事本身工程量不小(跨兩個獨立git repo比對)，已用spawn_task分派成獨立任務，不要在一般對話session裡臨時湊合寫。

## 相關連結
[[reference_curation_sop_2026-09-06]]（第56~57行原始規則出處）、[[feedback_new_public_site_must_register_coach888_2026-09-04]]（原始規則的記憶檔）、[[feedback_coach888_new_items_go_first]]（新項目排序規則）、[[feedback_taiwan_time_always]]（同類「軟性提醒失敗→需要hook」案例）、守則#01、守則#07
