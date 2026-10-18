---
name: reference-lenovo-rustdesk-no-autostart
description: 聯想Windows這台機器的RustDesk沒有服務/排程自動重啟機制，教練說「釋放記憶體」時不能比照Mac版直接重啟RustDesk
metadata:
  type: reference
---

聯想Windows（Lenovo）這台機器上的RustDesk（`D:\Program Files\RustDesk\rustdesk.exe`），查證確認**沒有Windows Service、沒有排程工作(Task Scheduler)、也沒有Startup項目**會在它被關掉/砍掉後自動重新拉起。

**Why:** Mac版`scripts/release_all_memory.sh`「釋放記憶體」流程裡會重啟RustDesk，是因為Mac那邊靠launchd KeepAlive自動重新拉起process，關閉後幾秒內自動復活、連線自動恢復。2026-09-03教練在聯想這台要求「釋放記憶體」時，查證發現這台機器沒有等效的自動重啟機制——若直接砍掉RustDesk process，教練若是透過RustDesk遠端連線在操作，會直接斷線且不會自動恢復，需要教練本人到機器旁手動重開，風險比Mac版高很多。

**How to apply:**
- 聯想這台機器上，教練說「釋放記憶體」時，**預設只處理LINE跟Typeless語音輸入（兩者都可安全關閉重開，不影響連線）**，RustDesk除非它本身記憶體異常飆高（教練可以看Activity Monitor/工作管理員自己判斷），否則不要主動去重啟它。
- 若情境明確需要重啟RustDesk（例如它真的記憶體異常，或教練確認自己不是靠RustDesk連線），才動手，且要先跟教練說明「這台沒有自動重啟機制，關掉後需要你自己去機器旁重開」讓他知情。
- 若之後要幫這台機器補上自動重啟機制（比照Mac的launchd KeepAlive），Windows端可用「工作排程器」設一個「程式結束時觸發」的條件式任務，或改用`nssm`把RustDesk包成Windows Service。目前未建置。

**2026-10-19 更新：** 已加 HKCU Run 登入自動啟動（仍沒有系統服務）；另查到 stop-service=Y 讓別人根本連不進來，見 [[reference-lenovo-rustdesk-stop-service-blocked-incoming-2026-10-19]]。
