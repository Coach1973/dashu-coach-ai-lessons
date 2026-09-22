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
