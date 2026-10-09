---
name: feedback_event_sites_must_have_github_wired_into_pipeline_2026-10-10
description: event.bymyway.com 每個靜態網站背後都要有 GitHub；09-30 教練下過令卻因只寫進接力棒、SOP 還寫「不做建GitHub」而被遺忘 10 天，20 站沒 repo；10-10 教練追問後改機制
metadata:
  type: feedback
---

教練 09-30 與 10-10 兩次講：所有 event.bymyway.com 的活動／作品網址，背後都必須有 GitHub。靜態內容（改文字、改照片）在小龍蝦／聯想／宏碁改 GitHub 就好，只有涉及資料庫、報名、LINE／Telegram 連動才回 Mac。

**Why:** 教練不想被綁在 Mac。10-10 發現 51 站有 20 站沒 repo（含 hnv-cc、111-wei、inventor 等 09-30 之後新站）。根因三個：①09-30 的命令只落成工具 `curated_git.py`＋接力棒 🔧 一列「下一場直接做」，沒接進上架程式；②大樹作品 SOP 與 `publish_creation()` docstring 還明寫「不建GitHub repo」，AI 照 SOP 做就違令；③開工 hook 照 N9 不唸 🔧 區，那一列 10 天沒人看。
**How to apply:** 新上架 event 網址一律由 `publish_creation()` 自動 `curated_git.py ensure <slug>`；每晚 00:40 launchd `ai.openclaw.curated-github-ensure` 補漏。教練的長期命令要改「SOP＋上架程式」，不能只放接力棒或記憶（同類錯第二次＝改源頭，N8）。GitHub 建 repo 太快會被限速，ensure-all 失敗晚點重試。相關 [[project_curated_sites_github_cross_machine_edit_2026-09-30]]。
