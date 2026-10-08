---
name: bni-ppt-sop-alias
description: 教練把「PDF轉BNI品牌底圖PPT」SOP簡稱為「BNI PPT SOP」，聽到這個詞直接對應到對應檔案，不用重新解釋流程
metadata: 
  node_type: memory
  type: reference
  originSessionId: cbe89eb3-02dc-46d9-97d1-bfe0bb26221e
  modified: 2026-09-20T22:33:15.743Z
---

教練 2026-09-21 把「PDF插圖轉品牌底圖PPT」這套流程正式簡稱為 **BNI PPT SOP**。

- SOP 文件：`~/.openclaw/workspace/knowledges/SOP_PDF轉品牌底圖PPT.md`
- 執行腳本：`~/.openclaw/workspace/scripts/pdf_to_branded_pptx.py`
- 一次性環境：`~/pptx_venv`（已裝好 python-pptx + Pillow，`source ~/pptx_venv/bin/activate` 即可用）
- 用法：`python3 scripts/pdf_to_branded_pptx.py --pdf <來源.pdf> --bg <底圖> --out <輸出.pptx>`
- 底圖固定用 BNI ACCELERATE 範本時，遮罩座標（左下角LOGO、右下角紅色裝飾）已內建成預設值，不用每次重新量測，換PDF直接跑即可
- 首次建立背景：2026-09-21幫《Architecting_Business_Systems_(2).pdf》15頁做成《建構高效商務系統的建築師_BNI版.pptx》，教練驗收通過後要求把流程SOP化，因為接下來還有好幾份BNI簡報要做且不想外包給其他AI（本機圖片處理不耗對話額度）

**How to apply**：教練之後說「BNI PPT SOP」或「用那個PPT流程」時，直接照上面路徑執行，不用重新問一次要用什麼工具或怎麼做。

**🔴 2026-10-08 教練火大糾正（《96小時引爆億級商業宇宙》，案例110）**：教練要的就是「**全部覆蓋**」＝插圖整張鋪滿、LOGO與右下紅色弧形疊在最上面，跟 9/21 驗收通過的《建構高效商務系統的建築師_BNI版》一樣。我改用通用技能加手動 `--mode safe` 把圖縮進 94%×89%，被罵「偷工減料」「你到底知不知道你以前做過哪些版本」。
- **做之前先看以前做過的**：`~/Downloads.bak.20261002/*_BNI版.pptx` 或 SSD 下載夾裡的舊成品，拆圖看樣子，再動手。
- **BNI 底圖一律用本 SOP 的腳本、預設遮罩，不改參數、不縮小**；底部角落有字被蓋是既有樣子，只能交付後一句話告知，不能自行改版。
- **主檔名不加後綴**（`原檔名_BNI版.pptx`），其他嘗試版本放備份資料夾，免得教練打開最顯眼的錯檔。
- 底圖用 `workspace/assets/BNI_ACCELERATE_底圖.jpg`（1450×817），不要用對話裡貼的縮圖。
