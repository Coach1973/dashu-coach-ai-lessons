---
name: reference-jinja2-dict-values-key-collision-2026-08-30
description: Jinja2樣板用點記法存取dict時，鍵名叫values/keys/items等Python字典內建方法名會撞名，資料靜默消失不報錯
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0f9618ae-e25f-4bf7-a476-73d71acabdd7
  modified: 2026-08-30T03:56:51.847Z
---

在真誠分會邀約來賓系統（sincere.bymyway.com，[[project_sincere_bymyway_guest_tracker_2026-08-30]]）開發過程中發現：把每週三項指標（來賓/121/咖啡會議）包進一個鍵名叫 `"values"` 的Python dict，傳給Jinja2樣板後用點記法 `entry.values.guests` 存取。

**現象**：整張表所有人、所有週次的來賓人數格子全部靜默顯示「0人」——連陳佩君實際26人的紀錄都被蓋成0。右側「總邀約」欄位因為走的是另一段不經過這個dict的計算邏輯，顯示仍然正確，導致bug被局部正確的數字掩蓋，起初不容易發現。

**根因**：Jinja2的屬性存取（`obj.attr`）對dict會先嘗試`getattr`（找同名方法/屬性），找不到才退回`obj['attr']`。Python字典本身有內建方法`.values()`/`.keys()`/`.items()`，所以`entry.values`會拿到「dict.values這個內建方法的bound method物件」，不是塞進去的資料；後面接的`.guests`在這個方法物件上找不到屬性，Jinja2的Undefined機制不報例外、直接回傳空值。

**修復**：把dict鍵名從`"values"`改成`"metrics"`（或任何不撞Python dict內建方法名的名稱），重新驗證五週資料正確顯示8/1/5/6/6人。

**通用教訓**：任何要在Jinja2樣板裡用點記法存取的dict，都不能用`values`/`keys`/`items`當鍵名。這個bug不會報錯、不會拋例外，只會讓資料在Python端明明正確、樣板卻靜默顯示空白/預設值，很難靠肉眼複查程式碼發現，只有實際跑起來、拿真實資料核對輸出才抓得到——這也印證了守則#03「自我驗證」跟功能驗收要用真實輸出核對，不能只看程式碼邏輯「應該」是對的。

Related: [[project_sincere_bymyway_guest_tracker_2026-08-30]]
