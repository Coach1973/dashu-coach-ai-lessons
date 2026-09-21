---
name: project-backup-tool
description: 使用者用「易數一鍵還原」工具備份 Windows 系統，檔案結構為 .pmf 基底 + 時間戳記 .ptp
metadata:
  type: project
  originSessionId: 7a00178d-d0f6-42f9-a9b8-06d2af7a07e9
---
使用者用中國的「易數一鍵還原」（簡體：易数一键还原）做 Windows 系統備份。

**檔案位置：** D 槽根目錄，資料夾名為 `易数一键还原Windows系统备份（不要删除）`（簡體）或 `易數一鍵還原Windows系统備份（不要删除）`（繁體）。

**檔案命名規則（重要）：**
- `BootImage.pmf` / `SystemImage.pmf` — **基底/舊**備份（無時間戳）
- `BootImage-{YYYYMMDDhhmmss}.ptp` / `SystemImage-{YYYYMMDDhhmmss}.ptp` — **時間戳記**的較新備份

從觀察的檔案大小，.ptp 與 .pmf 量級相當（不是 5-10% 的差異檔），**研判 .ptp 是獨立完整備份**而非增量，所以可單獨刪除其中一份。

**Why:** 2026/5/13 處理使用者磁碟清理時釐清。原本使用者以為「小=舊、大=新」是反的；實際是看建立日期與檔名時間戳。

**How to apply:**
- 清理舊備份時，先列出 .pmf 與 .ptp 檔的建立日期 + 大小，比對哪個是要刪的
- 刪前一定要確保「保留的那份」仍是完整的（透過 size 量級、檔名時間戳判斷）
- 一鍵備份每執行一次，會在同一個資料夾內新增一組時間戳 .ptp 檔（不會新增資料夾）
