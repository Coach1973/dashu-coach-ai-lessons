---
name: reference-macos-ps-rss-vs-footprint-2026-08-27
description: macOS上用ps -o rss量測程式記憶體會嚴重低估，跟Activity Monitor/教練實際看到的「真實記憶體」可以差10倍以上，要用top -pid X -l 1 -stats mem才對得上；2026-08-29補充「釋放」指令對系統性記憶體壓力幫助有限
metadata: 
  node_type: memory
  type: reference
  originSessionId: 65db632c-0f23-4fd8-aaf3-3f247ae2fd81
  modified: 2026-08-29T17:32:04.954Z
---

2026-08-27發現：`scripts/rustdesk_memory_guard.sh`（2026-07-09建立，每天固定
時間跑）用`ps -o rss= -p $PID`量測RustDesk `--server`process記憶體，門檻
設800MB(800000KB)。教練在Activity Monitor親眼看到這個process用了5.48GB，
但當下`ps -o rss`量出來只有488MB——**差了11.5倍**，導致這支腳本從
2026-07-11調高門檻後，過去約6週每天固定執行、log看起來一切正常（「未超過
門檻，略過」），實際上門檻永遠不可能被真實觸發，等於形同虛設。

**根因**：macOS的「真實記憶體」（Activity Monitor顯示的數字，也是`top`指令
`-stats mem`欄位顯示的"footprint"）包含壓縮記憶體(compressor)、記憶體對應
區段(mapped regions)等`ps`的RSS欄位不會完整計入的部分。對一般小程式差異
不大，但對會大量用記憶體對應/GPU緩衝/影音編碼的程式（RustDesk這類遠端桌面
軟體常見），兩者可以差到10倍以上。

**修法**：改用
```bash
top -pid "$PID" -l 1 -stats mem 2>/dev/null | tail -1
```
輸出格式是純數字+單位（如`5621M`、`118M`、`2G`），跟Activity Monitor同一個
數字來源，用regex解析M/G/K單位換算成統一單位即可。

**Why**：這是「監控機制存在、有跑、log正常，但量錯單位所以永遠不會真的
觸發」的一種新形狀——跟[[feedback_ai_claimed_mechanism_verify_before_trust]]
（機制根本不存在，AI自己編數字）不同，這次機制是真的、有真的hook/cron在
跑，但底層量測方式從一開始就有系統性偏差，讓門檻形同虛設。兩種形狀都需要
「不能只看log有沒有正常輸出，要去驗證量出來的數字是不是真的對得上使用者
親眼看到的數字」。

**How to apply**：
1. 任何在macOS上寫「監控/限制某個process記憶體用量」的腳本，一律用
   `top -pid X -l 1 -stats mem`，不要用`ps -o rss`，除非明確只是要比較
   同一支程式自己隨時間的相對變化（不需要對得上使用者看到的絕對值）。
2. 建立這類監控腳本後，除了看log格式正常，還要**至少驗證一次跟Activity
   Monitor（或使用者口頭回報的數字）對得上**，不能只信自己寫的量測邏輯
   語法沒錯就當作數字正確。
3. 若使用者回報「這個東西佔用量比你監控系統顯示的高很多」，第一個懷疑
   對象是量測單位/口徑不一致，不是先假設使用者記錯或誇大。

Related: [[feedback_ai_claimed_mechanism_verify_before_trust]]（同類「機制
看似正常實則失效」形狀，但根因不同）、[[feedback_lock_must_be_hook_not_optin]]
（防呆機制要能真的擋下來才算數，不能只是存在）

## 🔴 2026-08-29補充：「釋放」指令(重啟RustDesk)對系統性記憶體壓力幫助有限，不能預設觸發了就代表問題解決

教練回報Mac反應變慢，說「釋放」觸發`scripts/rustdesk_free_memory.sh`（`kill -TERM`重啟RustDesk `--server`
process）後，教練回報「好像沒啥用」。重新查證發現：**RustDesk重啟後短暫同時出現新舊兩個process
（合計比重啟前的單一process記憶體用量還高）**，而且RustDesk本身在教練這台Mac整體15GB used的量級裡
只佔一小部分（約200~350M），重啟它對緩解系統性記憶體壓力幾乎沒有實質幫助。教練最後**靠重開機**才讓
記憶體真正從15GB used恢復到8.34GB，關閉一堆前景App也沒有達到重開機的效果。

**Why**：這支「釋放」指令原本的設計目的很單純（RustDesk本身有記憶體洩漏，重啟它是對症下藥），但當
教練用「反應變慢」這個更廣泛的症狀觸發它時，隱含的期待被放大成「這個指令能解決反應慢的問題」，兩者
其實是不同量級的問題——單一App的洩漏 vs. 系統層級的記憶體碎片化。macOS的記憶體碎片化/compressor
累積只有重啟核心（reboot）才能徹底清空，關App或重啟單一process都清不掉。

**How to apply**：
1. 教練說「反應變慢」時，不要直接假設「釋放」指令就是對症解法——先用`top -l 1 -n 0`查
   `PhysMem`/`Load Avg`確認真正瓶頸在哪（記憶體/CPU/網路），再決定要不要觸發「釋放」
2. 「釋放」指令本身仍然有效（RustDesk記憶體洩漏是真的），但只在教練明確要重啟RustDesk本身時才有意義，
   不要把它當成通用的「電腦變慢急救按鈕」
3. 如果診斷後發現是系統層級記憶體壓力（可用記憶體剩不到500M、Load Average持續偏高），誠實告訴教練
   重開機是更徹底的解法，不要靠關App硬撐

Related: [[project_coach_rustdesk_remote_env]]（RustDesk跨平台環境背景）
