---
name: zoom-c-drive-junction-broken-accepted-2026-08-10
description: Zoom在C碟的即時資料junction連結到E碟已失效(案例51事故後設的)，教練2026-08-10親口裁示資料量小(403MB)不用修，往後不用主動提醒
metadata: 
  node_type: memory
  type: project
  originSessionId: 4ccfac57-b4fa-4dbf-a042-6d5569266b32
  modified: 2026-08-10T11:51:06.836Z
---

2026-08-10查證發現：`C:\Users\bymyw\AppData\Local\Zoom`（Zoom實際即時寫入的資料夾，403.91MB）不是junction，是獨立真實資料夾，8/1至今有239個檔案持續被寫入；對應的`E:\Claude-Data\AppData\Zoom-Local`（[[試金石案例51]]事故後建立的備份位置）8/1至今0個檔案異動，是凍結在7月中旬的舊快照。代表案例51修復時建立的junction後來失效了（推測是Zoom更新/重裝時把資料夾整個重建成一般目錄，覆蓋掉junction），目前Zoom的即時資料沒有真的同步備份到E碟。

**教練裁示**：「既然不占什麼空間，增量也沒有太多的內容，就不管它了」——確認資料量小(403MB)+風險可接受，明確選擇不修復。

**How to apply**：往後不用主動提醒教練修復這個junction，除非教練自己提起或Zoom資料量明顯變大。若教練問起「Zoom備份有沒有問題」可直接引用這則記憶回答現況，不用重新查證一次。
