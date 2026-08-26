---
name: reference-stop-hook-tool-result-boundary-bug-2026-08-27
description: "stop_rules_master.py（守則#07輪詢偵測）35天沒抓到真實違規的根因與修復——transcript裡工具回音也是type==\"user\"，被誤判成回合邊界"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 71be3dde-cb15-4712-b695-16c9c4ad7235
  modified: 2026-08-26T18:13:03.638Z
---

`scripts/stop_rules_master.py`（Stop hook總管，2026-08-12由10支獨立腳本合併而成）的規則D（守則#07輪詢設計偵測），從2026-07-23起實際上已經失效超過一個月——真實對話裡幾乎不曾真正擋下任何違規，即使違規語句100%命中regex。

**根因**：收集「這一整回合AI輸出」的TURN_TEXT邏輯，用「往回掃描transcript，遇到第一個`type=='user'`事件就停」當回合邊界。但Claude Code transcript裡，每一次工具呼叫（Bash/Read/Edit/Write）執行完的結果也記錄成`type=='user'`（`content`是`[{"type":"tool_result",...}]`，沒有`text`區塊）——不是教練真人講話，是工具回音。真實對話一個回合幾乎必然有多次工具呼叫，往回掃描幾乎每次都被最近一次工具回音提早打斷，抓不到更早（同一回合稍早）講的違規內容，包括寫進檔案裡的設計（Write/Edit的`content`/`new_string`）。

這個bug不是2026-08-12合併造成的新問題——查git log確認`if t == 'user': break`這行邏輯早在2026-07-23的commit `00821d280`就已存在（當時是為了修「設計寫進檔案沒出現在最後一句話會漏抓」的問題，結果新寫的邏輯反而讓這個情境更難被抓到），08-12合併只是逐字搬過去。程式碼裡其實已經有正確的判斷邏輯可用——用在C規則（台灣時間鐵律）的`_last_user_idx`：判斷`user`事件的`content`是字串、或list裡有`type=='text'`區塊，才算真人講話——但這段邏輯沒被套用到D規則，兩處各自獨立、悄悄分岔。

同時發現`test_stop_rules_master.sh`（08-12建立的迴歸測試）「輪詢設計」測試案例只有一句話零工具呼叫，測不出這個bug；且它拿來當基準的「原版10支腳本」全部依賴`lib/stop_ctx.sh`，這支共用快取層在**同一天**被合併作業當多餘檔案刪除，導致原版腳本呼叫必失敗、永遠回報「沒擋下」——測試從建立當天起，比對基準就是空的。

**修復**：新增`_is_real_user_prompt(evt)`輔助函式（判斷邏輯與C規則的`_last_user_idx`一致），TURN_TEXT掃描與`_last_user_idx`都改用它，工具回音不再被誤判成回合邊界。用教練查證時抓到的真實transcript（`65db632c-...jsonl`）截到那個回合結束處重播驗證：exit code從沒抓到→正確變2，且抓到兩處違規（口頭講的+寫進`rustdesk_memory_guard.sh`檔案裡的）。同步重寫`test_stop_rules_master.sh`，加`run_case_direct()`直接斷言exit code（不再依賴已死的舊版基準），新增「回合前段違規+5次工具呼叫後才結束」的迴歸測試。

**Why**：這是同一場對話裡發現的第7個「監控/防呆機關看似正常實則悄悄失效」案例（同型態見 [[reference_macos_ps_rss_vs_footprint_2026-08-27]]），教練親口要求查清楚並徹底修好，寫進試金石案例66。

**How to apply**：之後任何要修改「往回掃描transcript找回合邊界」的程式碼，先讀這條記憶+試金石案例66，並用真實（非零工具呼叫）的transcript重播驗證，不能只靠合成單輪測試通過就信任。看到程式碼裡有多處各自實作「這個user事件是不是真人講話」的判斷，優先抽成共用函式，不要各自複製一份（容易分岔）。改動任何依賴外部檔案的東西前，先確認有沒有測試套件也依賴同一份外部檔案，避免像`lib/stop_ctx.sh`那樣，刪除時漏想到測試也在用它。

Related: [[feedback_event_driven_not_polling_pattern]]（守則#07輪詢設計本身的教訓）、[[feedback_ai_claimed_mechanism_verify_before_trust]]（同型態：機關存在不代表真的在運作）、[[reference_openclaw_hook_requires_hookmd_metadata]]（同型態：hook註冊但沒真的生效）
