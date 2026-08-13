---
name: project-advance-registrations-backfill-purpose-2026-08-14
description: event.db的advance_registrations表裡49筆backfill資料教練要用來印簽到表，不是測試資料不能誤刪
metadata: 
  node_type: memory
  type: project
  originSessionId: 7c3bfad2-6f16-4c09-ab1c-23bcf3e61ae2
  modified: 2026-08-13T19:50:32.017Z
---

`event-signup/event.db`裡新建的`advance_registrations`表，目前有49位不重複報名者（2026-08-14從教練貼出的51筆歷史LINE報名通知文字backfill、去重複後的結果，詳見[[project_dual_registration_data_sources_2026-08-14]]）。

**教練原話**：「總結，要記得這份名單，我到時要印簽到表」。

**Why**：這不是測試資料、不是可清除的暫存內容——是教練要拿來印製活動現場簽到表的正式名單（主要是AI微論壇嘉義場8/28共31人+大樹小講多場次），跟`signups`表（現場數位簽到記錄）是兩回事，不要混淆或誤刪。

**How to apply**：往後任何要清理`event.db`測試資料、或整理/重構這個資料庫結構的動作，絕對不能動到`advance_registrations`表既有的49筆記錄。教練問「幫我印簽到表」或「這場人夠不夠」這類問題時，直接查：
```sql
SELECT session_label, name, phone, company FROM advance_registrations
WHERE session_label LIKE '%關鍵字%' AND session_label NOT LIKE '%系統測試%';
```
若教練之後持續手動貼新的報名通知文字要求backfill，比照同樣的解析方式（見USER.md「教練問報名統計時怎麼查」段落）新增進同一張表，不要另開新表。
