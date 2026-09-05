---
name: reference-windows-claude-session-storage-layout-2026-09-05
description: 聯想Windows這台機器Claude對話記錄實際儲存位置盤點——真正逐字稿在E槽(經junction連到C槽)，桌面版App自己另有一份C槽本機快取，兩者若混淆會誤判「對話記錄不見了」
metadata: 
  node_type: memory
  type: reference
  originSessionId: 40c7e7f7-5d29-449f-934e-e850c46e3837
  modified: 2026-09-05T13:20:03.764Z
---

教練半夜一鍵還原到8/10備份後，懷疑「對話記錄都不見了」，實際查證這台機器(聯想Windows)的儲存結構如下：

**真正的對話逐字稿（安全，在E槽）**：
- `E:\Claude-Data\.claude\projects\E--Claude-Data\*.jsonl` ——每場對話一個檔案，完整逐字稿
- `C:\Users\bymyw\.claude` 是一條指向 `E:\Claude-Data\.claude` 的**symlink**（2026-04-06建立），所以C槽這條路徑其實也是在讀E槽的真實資料
- 8/10還原只會動C槽「檔案本身的內容」，這條symlink本身在8/10之前就存在，還原不會破壞它——查證當下45個jsonl檔案，41個mtime在8/11之後，完全連續無斷層

**桌面版App自己的本機快取（會被C槽還原動到，但只是快取不是原始資料）**：
- `C:\Users\bymyw\AppData\Roaming\Claude\` ——這是一個**真實存在於C槽、沒有連到E槽**的資料夾，裡面有`claude-code-sessions`（session meta索引）、`IndexedDB`、`Local Storage`等App自己的UI渲染快取
- 如果C槽被還原到某個較早時間點，這份本機快取/索引會跟著倒退，可能讓App介面（如「歷史對話」清單）短暫顯示異常或不完整，但**不代表底層E槽的真實逐字稿被刪除**

**Why**：教練這台機器有C槽（系統碟，會被「易數一鍵還原」整碟還原）跟E槽（資料碟，獨立於還原範圍外）兩層架構，Claude Code的核心資料刻意搬到E槽+junction連回C槽，就是為了在C槽被還原/重灌時資料不會跟著消失。但桌面版App本身的一些本機索引/快取仍然單獨存在C槽，沒有被納入這套junction保護。

**How to apply**：教練往後若又提到「復原/重灌後對話記錄不見了」，第一步先直接查`E:\Claude-Data\.claude\projects\E--Claude-Data\`底下jsonl檔案的數量跟mtime時間軸有沒有斷層（通常沒有），可以用Grep工具搜特定關鍵字驗證某場對話內容確實還在。如果E槽資料完好，就是App介面本機快取的問題，不代表真的遺失，跟教練說明時要把「E槽真實資料」跟「App介面本機快取」這兩件事分開講清楚，不要籠統說「對話記錄都在」或「都不見了」。

Related: [[feedback_desktop_session_storage_and_blackbox_wording]]（Mac版同類查證方法）
