---
name: reference-coach888-sync-key-whitelist-pattern
description: coach888新增localStorage同步key時，前端syncStateToServer陣列跟後端COACH888_STATE_KEYS白名單要同一輪一起改，這次連續踩兩次才記住
metadata:
  type: reference
  originSessionId: e04e921e-76e5-4743-82a4-59fbb8062c1d
  modified: 2026-09-04T11:14:00.000Z
---

coach888（作品一覽表）的跨裝置同步架構：前端 `index.html` 的 `syncStateToServer()`/`pullStateFromServer()` 會把一組 localStorage key 陣列 POST/GET 到 `event.bymyway.com/api/coach888/state`，但**伺服器端（`event-signup/app.py` 的 `COACH888_STATE_KEYS`）另外維護一份獨立的白名單**，不在白名單內的 key 會被 POST 端點靜默丟棄（`if key not in COACH888_STATE_KEYS or value is None: continue`），GET 端點也只回傳白名單內的 key。

**Why:** 2026-09-04 同一場對話裡連續踩兩次同款坑——先加 `coach888_sections`（自訂分類持久化）時漏改伺服器白名單，前端存了、伺服器默默丟掉，教練那邊完全看不出異狀（沒有錯誤訊息，就是同步失敗）；修完後緊接著加 `coach888_section_order`（大分類拖曳排序）這次才記得同一輪一起補。兩個key分屬不同功能、相隔不到一小時各自新增，證明這不是單一失誤而是這個架構本身有「兩處要同步改、缺一處不會報錯」的陷阱。

**How to apply:** 往後任何要在 coach888 新增一組需要跨裝置同步的 localStorage key，動手清單：
1. 前端宣告 `var XXX_KEY = 'coach888_xxx';`
2. `syncStateToServer()`／`pullStateFromServer()` 兩處陣列都要加入 `XXX_KEY`
3. **同一輪**改 `/Users/bymyway/.openclaw/workspace/event-signup/app.py` 的 `COACH888_STATE_KEYS` 集合，加入字串 `"coach888_xxx"`
4. `launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp` 重啟服務
5. 驗證：`curl -s "https://event.bymyway.com/api/coach888/state"` 確認新key出現在回傳的keys清單裡，不能只看前端console沒報錯就當作成功——這個失敗模式的特徵就是前端完全不會報錯，只有直接查伺服器回傳內容才看得出來

Related: [[project_coach888_cross_device_sync_2026-09-03]]（原始建置那一棒，當時只有5組key，沒料到後續會陸續增加）
