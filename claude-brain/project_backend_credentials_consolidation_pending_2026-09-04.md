---
name: project-backend-credentials-consolidation-pending
description: 教練2026-09-04交辦下一場要做的事：把所有後台系統集中到coach888作品一覽的一個分類並註明帳密，語音辨識有一個詞待確認
metadata: 
  node_type: memory
  type: project
  originSessionId: e04e921e-76e5-4743-82a4-59fbb8062c1d
  modified: 2026-09-03T21:38:17.414Z
---

教練 2026-09-04 05:36 交辦：「等我開啟新對話的時候，去我的『大品一覽』裡面，幫我把所有的後台系統通通集中起來在一個分類，並註明帳密。」

**Why:** 這場對話聊到`/materials/admin`後台的帳密設計，教練順勢想到他的其他系統(bni-chapters、namecard-db發票後台等)帳密散落各處不好找，想要一個統一入口清楚列出「哪個系統/哪個網址/帳號密碼是什麼」。

**待確認一件事**：教練說的「大品一覽」很可能是語音辨識把「作品一覽」聽成「大品一覽」——教練現有系統裡確實有一個「coach888作品一覽」(`https://coach1973.github.io/coach888/`)，是他長期在用、教練唯一稱之為「作品」清單的網頁，已有多個分類區塊(常用/後臺/BNI專用等)。**下一場開工先跟教練確認**「您說的大品一覽是不是coach888作品一覽？」，不要直接假設就動手，符合守則#18語音糾偏原則。

**How to apply:** 確認後，任務是在coach888新增一個「後台系統帳密」分類，內容需要盤點教練名下所有帶登入/管理功能的後台（namecard-db/invoice-admin、bni-chapters的9個分會admin、materials/admin等），逐一列出網址+帳號+密碼。**帳密是敏感資料**，要先確認coach888這個repo是公開還是私有(記憶`project_bni_chapters_public_launch_2026-08-03`裡提過coach888是公開GitHub Pages repo)——如果是公開的，帳密絕對不能直接寫進coach888頁面本身，要嘛整個repo改私有、要嘛帳密清單改放進權限受限的路徑大全_憑證層.md，這件事優先於直接動手，先跟教練確認清楚存放位置再做。

Related: [[project_materials_viewer_system_2026-09-04]]
