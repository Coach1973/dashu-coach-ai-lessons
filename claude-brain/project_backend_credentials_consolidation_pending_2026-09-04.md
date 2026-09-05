---
name: project-backend-credentials-consolidation-pending
description: coach888「後台系統帳密集中」任務的存放位置決策——教練裁示存Mac本機、直接問小龍蝦
metadata: 
  node_type: memory
  type: project
  originSessionId: 89e4937c-c840-4c0c-bc46-68785a6d6bbf
  modified: 2026-09-04T14:30:44.898Z
---

教練確認「後台系統帳密集中」任務對應的是coach888作品一覽（非其他系統），已盤點11個帶登入的後台系統。存放位置教練2026-09-04裁示：**存放在Mac本機（不是coach888公開repo，也不是獨立網頁），教練需要密碼時直接問小龍蝦就好**。

**Why**：coach888是公開GitHub repo，帳密不能直接寫進頁面（先前AskUserQuestion提過三案：只列帳號+密碼另存私密憑證檔／整個repo改私有／帳密清單另建獨立私密頁面），教練選的其實是第一案的精神——密碼不上網頁，改成口語化查詢入口。

**How to apply**：
1. ✅ **2026-09-05已完成**：`路徑大全_憑證層.md`新增「coach888後台系統帳密」小節，9個系統逐一列出帳號/密碼。原本只存雜湊讀不出明碼的4個系統（event-signup/mentor100/peipei-event/namecard-db）已重設為統一密碼`88888`並用curl實測登入成功（302+`logged_in:true` cookie）；`materials/admin`查證後發現目前完全沒有登入保護，已如實標記；`rpl-workshop`密碼是教練刻意不讓AI持有的公司統編，維持原樣不重設。
2. 這份清單只能寫在Mac本機的`路徑大全_憑證層.md`（本來就是權限受限、不進公開repo的檔案），不可外流到coach888或任何公開頁面。
3. **小龍蝦（main agent）需要知道**：教練若在LINE/Telegram問「XX後台密碼是多少」，答案來源是Mac本機的`路徑大全_憑證層.md`，小龍蝦本身工具權限受限（no fs/exec，見`hooks/rule-reminder`的scope設計），實際上要嘛這份清單要用某種方式讓小龍蝦讀得到（例如放進小龍蝦有讀取權限的知識庫路徑），要嘛教練問的時候由軍師代答。**這個技術細節仍待落實**（本場只完成密碼盤點+重設，還沒接通小龍蝦的讀取路徑），下次可考慮讓小龍蝦收到這類問題時，寫派工單給軍師代答（比照`workspace/SOUL.md`「可以直接派工給Mac軍師」的既有機制）。

相關：[[feedback_public_admin_separation_default_2026-09-04]]
