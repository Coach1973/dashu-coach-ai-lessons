# ocr-extract：通用圖片文字辨識→結構化欄位擷取工具

從 `namecard-db/extract.py` 抽出來的通用版。任何「讀一張圖片、把上面的文字整理成
JSON 欄位」的任務都能用，不用 AI 自己盯著圖片瞇眼看，也不用每次都重新設計一套
辨識管線。

## 為什麼不用 AI 直接看圖辨識

`namecard-db` 實測過：MiniMax-M3 直接看名片圖片辨識，準確率明顯不如「PaddleOCR
先把文字讀出來→MiniMax 只做文字整理」這種兩階段做法（曾把「黃薇雅」讀成「黃鈺翔」、
「洪美香」讀成「洪美智」這類真人姓名確認過的錯誤）。兩階段管線本機 OCR 免費、
MiniMax 不限流量，等於零 Token 成本，還比較準。

## 用法

### 當命令列工具

```bash
cd ~/.openclaw/workspace/tools/ocr-extract
./venv/bin/python3 ocr_extract.py <圖片路徑> --task "情境說明" --fields '{"欄位名":"欄位說明"}'
```

範例（收據）：
```bash
./venv/bin/python3 ocr_extract.py receipt.jpg --task "這是一張收據" \
  --fields '{"store_name":"店名","amount":"金額（含幣別）","date":"日期"}'
```

也可以把欄位schema寫成獨立json檔，用 `--fields-file schema.json` 代替 `--fields`。

### 當 Python 模組匯入

```python
from ocr_extract import extract_structured_fields

result = extract_structured_fields(
    "photo.jpg",
    field_schema={"name": "姓名", "amount": "金額，含幣別"},
    task_description="這是一張收據",
)
```

回傳一個 dict；失敗時是 `{"_error": "...", "_raw": "..."}`。

## 環境需求

- PaddleOCR 沿用 `namecard-db/paddleocr_venv`（同一台機器，不重複安裝這個
  好幾 GB 的依賴）——如果之後 `namecard-db` 整個搬走或砍掉，這支工具的 OCR
  階段會跟著失效，要記得一起搬。
- 本工具自己的 `venv/` 只裝了 `anthropic` 這個輕量套件（不需要 Python 3.11
  限制，那個限制只有 PaddlePaddle 本體才需要）。
- `.env`（git-ignored）放 MiniMax 的 `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL`，
  跟 `namecard-db/.env` 是同一組帳號的憑證副本。

## 已知雷點

**外層 shell 的 `ANTHROPIC_API_KEY`/`ANTHROPIC_BASE_URL` 會蓋過 `.env`**：
如果從已經跑著 Claude Code 的終端機呼叫這支工具，那個終端機本身可能已經
export 了指向別的端點的 `ANTHROPIC_*` 變數。`_load_env_file()` 刻意用直接賦值
（不是 `setdefault`）覆蓋掉，確保這支工具永遠用自己 `.env` 裡的 MiniMax 端點，
不會被外層環境污染——2026-07-27 建置時實測踩到這個坑（用 setdefault 版本第一次
測試就打到 `api.anthropic.com` 而非 MiniMax，回傳 401），已修正並重測通過。

## 驗證紀錄（2026-07-27 建置時實測）

用兩張真實名片照片、兩組完全不同命名風格的自訂欄位schema測試過：
- `{"name","company","phone"}` → 正確辨識姓名/公司/電話
- `{"contact_person","organization","email_address"}` → 正確辨識公司，
  查無email正確回傳null（沒有瞎猜）

證明欄位參數化管線本身可行，不綁死任何特定格式。
