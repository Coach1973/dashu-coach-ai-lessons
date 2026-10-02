---
name: project_curated_sites_github_cross_machine_edit_2026-09-30
description: 教練要每個event.bymyway.com策展網站（大樹作品＋店家）都有GitHub，聯想/宏碁Claude桌面版貼網址就能改、先看效果、推上去網站自動換新；兩個關鍵動作被Claude Code安全檢查擋下待授權
metadata:
  node_type: memory
  type: project
  originSessionId: 460979e3-7b38-4c37-8a42-e8e91101983f
  modified: 2026-09-30T13:07:43.329Z
---

2026-09-30 教練交辦：上架大樹作品SOP／大台南策展SOP時，同時建一份GitHub；聯想或宏碁的Claude桌面版只要貼 event.bymyway.com 網址，就對應找到GitHub、改版面時能即時看到效果、改完網站跟著更新。只限靜態網站（有資料庫的照舊在Mac改）。

**Why:** 小龍蝦和赫米斯改版面沒辦法即時呈現畫面給教練看；教練想在任何一台電腦無縫接著做，不想被綁在Mac。

**How to apply:**
- 對應規則：`event.bymyway.com/curated/<slug>/` ↔ `github.com/Coach1973/<slug>`，Mac本機 `~/github_repos/<slug>/`。工具 `workspace/scripts/curated_git.py`（ensure/ensure-all/sync）。
- 09-30現況：35站中24站已有GitHub（早期策展流程建的22站＋jacky-brand、submission）；其餘11站補建、接進上架流程、GitHub通知Mac自動更新的入口，被Claude Code自動安全檢查擋下（「Remote Repoint」與新增外部可觸發執行的入口），已記在接力棒🙋區等教練回「上」。
- 沒有自動更新入口之前：聯想/宏碁push後，要有Mac的軍師跑 `curated_git.py sync <slug>` 網站才換新。

相關：[[feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30]]、[[reference_curation_sop_2026-09-06]]
