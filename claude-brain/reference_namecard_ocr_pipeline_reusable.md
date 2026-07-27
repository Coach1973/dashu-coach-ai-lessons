---
name: reference-namecard-ocr-pipeline-reusable
description: namecard-db的PaddleOCR+MiniMax兩階段圖片文字辨識管線，已驗證高準確度，可複用於任何「讀圖片文字」場景，不用AI自己盯圖片看
metadata: 
  node_type: memory
  type: reference
  originSessionId: fd094a96-8867-4bdc-a472-49dd84f00d25
  modified: 2026-07-26T10:05:27.999Z
---

`/Users/bymyway/.openclaw/workspace/namecard-db/extract.py` + `paddle_extract.py` 是一套已經上線運作（`namecard.bymyway.com`，23筆真實名片資料，辨識品質高）的圖片文字辨識管線，遇到任何「教練丟圖片要AI讀出文字/建檔」的需求，優先考慮直接複用或抽出這套邏輯，不要讓AI（我）自己盯著圖片瞇眼辨識。

**Why**：extract.py 檔頭註解明白寫著教練實測結論——「MiniMax-M3直接看圖辨識率太差，『黃薇雅』讀成『黃鈺翔』、『洪美香』讀成『洪美智』等真人姓名確認過的錯誤」。改成兩階段管線後準確度大幅提升，且**兩階段都不耗費Claude Code這邊的Token**：PaddleOCR本機跑（免費，零API成本）、MiniMax不限流量（見[[reference_windows_bash_network_sandbox_isolation]]同類基礎設施筆記）。2026-07-26 我（軍師）自己讀教練提供的4張報名截圖時用PIL裁切放大硬看，準確度不如這套管線，且真的看錯過一次姓名（陳慧雯讀成陳薏雯）。

**架構（兩階段）**：
1. `paddle_extract.py`：獨立跑在 `namecard-db/paddleocr_venv`（Python 3.11環境，因為PaddlePaddle不支援主環境3.14），用法 `python3 paddle_extract.py <圖片路徑>`，輸出偵測到的文字，一行一個。HEIC/HEIF格式要先轉JPEG（PaddleOCR不吃）。
2. `extract.py` 的 `extract_card_fields(image_path)`：呼叫上面的OCR拿到純文字後，把文字（不是圖片）交給MiniMax-M3（`anthropic.Anthropic()`，`.env`裡設`ANTHROPIC_BASE_URL`指向MiniMax端點）整理成結構化JSON。SYSTEM_PROMPT可依場景替換（名片欄位/報名資料欄位/任何結構化擷取需求皆可套用同一套「OCR文字→LLM整理JSON」的骨架）。

**How to apply**：下次遇到「讀圖片建檔」類任務（報名表、收據、清單截圖等），先評估能不能直接呼叫這套管線（或複製改寫SYSTEM_PROMPT），而不是用Read工具讀圖片自己判讀。若圖片本身解析度/字體太小連PaddleOCR都讀不清楚，才是唯一該讓教練重新提供清晰截圖的情境（見[[feedback_screenshot_rules_consolidated]]第四次補充）。

**待辦（2026-07-26 交辦，尚未動手）**：教練要求把這套管線抽成通用小工具（不綁死名片欄位），下一場對話直接繼續。
