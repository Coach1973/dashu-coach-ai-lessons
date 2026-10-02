---
name: reference_tut_memory_wall_moderation_2026-10-02
description: 南應校友回憶牆(tut-memory)投稿＋照片存伺服器、群組審核才公開的做法與坑；之後做別的互動牆可照用
metadata:
  type: reference
---
event.bymyway.com/curated/tut-memory/ 原本照片只存訪客瀏覽器(localStorage)、別人看不到。2026-10-02 教練要「所有照片可勾起大家回憶＋人工審核」，改成：

- 後端在 `event-signup/app.py` 的 `/api/memwall/<slug>/notes`(GET只回approved、POST存pending)，表 `memwall_notes`，照片 `event-signup/memwall_uploads/`(已 .gitignore)。新牆只要把 slug 加進 `MEMWALL_SLUGS`。
- 審核：投稿→Telegram 群「活動報名即時通知」(-5349981085，教練+佩佩老師+bot)收到照片＋簽章連結 `/memwall/review/<id>?t=<HMAC>`，點開按通過／不通過，不用登入；簽章用 `EVENT_SECRET_KEY`。
- 自己送出的待審留言只在自己瀏覽器顯示「⏳審核中」，通過後以伺服器版本為準(用 serverId 去重)。

**坑**：Cloudflare 會把 `.jpg` 的 404 快取 4 小時 → 審核前被請求過的照片，通過後仍破圖。已讓 404 回 `Cache-Control: no-store`。
**坑**：投稿通知曾想測試真送群組，怕吵到佩佩老師；只驗了 bot 是群管理員＋sendPhoto 本機成功。第一則真實投稿要確認群組有收到。
同一輪還發現講座報名、「加入校友會」也只存瀏覽器(假的)；加入改開召集令 `/tut/` 真表單，講座等教練通知主題後再接。相關：[[reference_curation_sop_2026-09-06]]
