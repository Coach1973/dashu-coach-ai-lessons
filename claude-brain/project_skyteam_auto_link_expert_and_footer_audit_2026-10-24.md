---
name: project-skyteam-auto-link-expert-and-footer-audit-2026-10-24
description: 顧問師天團=人才軍火庫(skyteam)；專家個人頁上架後自動填名錄連結(skyteam_link_expert.py)；網頁頁尾「TAVA AI 製作／出品人 大樹教練／友善連結 榮樹下」75站只有15站齊全
metadata:
  type: project
---

教練 10/24 說「顧問師天團」＝人才軍火庫 https://event.bymyway.com/curated/skyteam/（登記表標題寫「顧問師天團」）。他要求：凡做出顧問或專家的網頁，自動放進該專家在天團名錄的連結。

做法：`scripts/skyteam_link_expert.py`（名錄 JSON 在 skyteam/index.html 的 experts-data；標題第一段含姓名、名錄 url 空或是 # 錨點才補；已接進 curation_process.py 上架完成後背景跑；workspace `e0db37531`）。未等到真上架驗證；不會替名錄外的新專家建卡片。

頁尾標準三句（TAVA AI 製作／出品人 大樹教練／友善連結 榮樹下，範本在 runforfuture、rongtree 的 footer）：10/24 稽核 75 站僅 15 站齊全，NMDA 兩頁已補（nmda `1d55a2b`），其餘約 60 站待教練決定要不要全補；沒有自動機制。

**Why:** 教練要品牌尾巴一致，且不想每次提醒。**How to apply:** 新上架網頁要補三句；教練說「全部補」才批次改，店家頁掛名先問一次。相關 [[project_skyteam_identity_labels_chapters_six_columns_2026-10-24]]。
