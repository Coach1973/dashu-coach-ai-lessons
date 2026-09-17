---
name: feedback-agent-soul-files-not-synced-2026-09-17
description: kong/peipei/小二各自有獨立、未同步的SOUL.md/workspace，main workspace的SOUL.md新增規則不會自動傳到他們那邊——任何新SOP/規則要教全員知道，必須逐一手動複製
metadata:
  type: feedback
---

**發生什麼**：2026-09-17教練交辦建立「報名頁上架SOP」，軍師把規則寫進main workspace的`SOUL.md`＋同步進Hermes/小二各自的`knowledges/`（因為之前已知這兩個讀不到main workspace）。但漏了孔大哥(kong)/佩佩老師(peipei)——查證後發現`agents/peipei/SOUL.md`、`agents/kong/SOUL.md`是完全獨立的檔案（不是symlink，內容也完全沒有策展SOP/報名頁SOP的任何段落），而且這兩個agent目錄**從未被git追蹤過**（`git log`查無任何歷史）。結果佩佩老師被交辦上架大樹小講10/3活動頁時，因為她的SOUL.md根本沒有這個規則，改用她原本就知道的策展SOP上架，把一個報名活動頁誤判成店家，上架到大台南策展中心的店家名冊裡。

**Why 這條很重要**：這台機器上至少有5個不同的「AI員工」在跑（main/小龍蝦、Hermes、小二、kong、peipei），每一個都有自己獨立的workspace/SOUL.md/知識庫，**彼此之間沒有任何自動同步機制**。只更新main workspace的SOUL.md、以為「反正大家都讀得到」是錯的假設——這次錯的代價是一個活動頁被誤上架成店家、且後續軍師想清理誤上架內容時又犯了[[feedback_curation_delete_takes_down_live_url_not_soft_hide_2026-09-17]]那個錯，一次疏漏連環引發第二次疏漏。

**How to apply**：任何新SOP/規則/技能只要牽涉到「教練可能會交辦給哪個AI做」，寫完主檔後要主動盤點這件事「哪些agent可能會被交辦到」，逐一確認：①main（SOUL.md，其他agent多半直接讀或symlink這份）②Hermes（`~/.hermes/workspace/knowledges/`，讀不到main的`claude-brain/`）③小二（`~/.openclaw-test2/workspace/knowledges/`，獨立沙盒）④kong（`~/.openclaw/agents/kong/SOUL.md`，獨立檔案）⑤peipei（`~/.openclaw/agents/peipei/SOUL.md`，獨立檔案）。不能只改一份就假設全員都學到了，這五個目前是完全獨立、需要人工逐一同步的孤島。

Related: [[reference_event_registration_page_sop_2026-09-17]]、[[feedback_curation_delete_takes_down_live_url_not_soft_hide_2026-09-17]]
