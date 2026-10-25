---
name: reference-skyteam-invite-faces-follow-home-ranking-2026-10-25
description: 人才軍火庫邀請函頁首批24位人像牆連動首頁前32位的點擊排名；首頁換人／改FRONT／換照片後要跑 skyteam_build_invite_roster.py
metadata:
  type: reference
---

教練 10/25 18:22 問「邀請函首批 24 位能不能連動首頁排名最前面的 24 位」。查到邀請函 `skyteam/invite/index.html` 原本手寫 PEOPLE 陣列（還含首頁沒有的許朝竣、傅恩平），不會跟首頁走。

**做法**：`workspace/scripts/skyteam_build_invite_roster.py` 讀首頁 `experts-data` 前 FRONT 位 → 產生 `skyteam/roster.json`＋縮圖 `img/invite/roster/<hash>.webp`（4:5，內嵌圖與 img/p/ 檔案兩種都處理）。邀請函頁載入時讀 roster.json＋新增唯讀 API `GET /api/skyteam/ranking`（不記到訪），用首頁同一條規則（點擊數高到低、同分照原順序）取前 24。抓不到排名就照原順序。

**維護**：首頁換人／改 FRONT／換照片 → 跑一次該腳本再 commit 推送 skyteam。上架自動連結（skyteam_link_expert.py）會一併重產；但手動換人/改 FRONT/換照片仍要自己跑一次。
**驗證**：headless Chrome 渲染線上兩頁，前 24 位順序一致（邀請函 skyteam d4e51dc、workspace 見 commit）。邀請函頁沒有點擊追蹤（點照片是開外站，不算首頁點擊）。
