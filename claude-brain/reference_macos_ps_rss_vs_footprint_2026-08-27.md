---
name: reference-macos-ps-rss-vs-footprint-2026-08-27
description: macOS上用ps -o rss量測程式記憶體會嚴重低估，跟Activity Monitor/教練實際看到的「真實記憶體」可以差10倍以上，要用top -pid X -l 1 -stats mem才對得上
metadata: 
  node_type: memory
  type: reference
  originSessionId: 65db632c-0f23-4fd8-aaf3-3f247ae2fd81
  modified: 2026-08-26T17:48:41.002Z
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
