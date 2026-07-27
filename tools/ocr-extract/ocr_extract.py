"""
通用圖片文字辨識→結構化欄位擷取工具。

從 namecard-db/extract.py 抽出來的通用版：兩階段管線不變（PaddleOCR 本機辨識
文字，免費零Token → MiniMax 把文字整理成呼叫端指定的 JSON 欄位），差別是
這裡的欄位/情境是參數，不綁死名片格式，讓「讀圖片建檔」這類任務都能重複使用。

PaddleOCR 需要 Python 3.11 環境，沿用 namecard-db 已裝好的 paddleocr_venv
（同一台機器上只裝一份，不重複安裝這個好幾GB的依賴）。

用法（CLI）：
    python3 ocr_extract.py <圖片路徑> --fields '{"標題":"活動標題","日期":"活動日期"}' --task "活動海報"
    python3 ocr_extract.py <圖片路徑> --fields-file fields.json

用法（當作模組匯入）：
    from ocr_extract import extract_structured_fields
    result = extract_structured_fields(
        "photo.jpg",
        field_schema={"name": "姓名", "amount": "金額，含幣別"},
        task_description="這是一張收據",
    )
"""
import argparse
import json
import os
import re
import subprocess
import sys

import anthropic

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_NAMECARD_DB_DIR = os.path.normpath(os.path.join(_THIS_DIR, "..", "..", "namecard-db"))
_PADDLE_PYTHON = os.path.join(_NAMECARD_DB_DIR, "paddleocr_venv", "bin", "python3")
_PADDLE_SCRIPT = os.path.join(_NAMECARD_DB_DIR, "paddle_extract.py")

MODEL = os.environ.get("OCR_EXTRACT_MODEL", "MiniMax-M3")


def _load_env_file(path: str) -> None:
    """讀 .env 檔案，把 export KEY="VALUE" 這種格式的變數塞進 os.environ。
    強制覆蓋（不是setdefault）：呼叫這支工具的shell本身可能已經有Claude Code
    自己的 ANTHROPIC_API_KEY/ANTHROPIC_BASE_URL（指向不同的端點），這支工具
    要用的是自己 .env 裡設定的MiniMax端點，不能被外層shell的既有值蓋過。"""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = line.removeprefix("export ").strip()
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ[key] = value


_load_env_file(os.path.join(_THIS_DIR, ".env"))


def _repair_stray_backslashes(text: str) -> str:
    """圖片裡常見手寫/裝飾用的反斜線不是合法JSON跳脫字元，會讓json.loads()炸掉，
    把非法的反斜線都跳脫成 \\\\。"""
    return re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", text)


def _ensure_paddle_readable_path(image_path: str) -> str:
    """PaddleOCR不吃HEIC，先轉成暫存JPEG給它讀；其他格式直接用原檔路徑。"""
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in (".heic", ".heif"):
        return image_path

    import pillow_heif
    from PIL import Image

    pillow_heif.register_heif_opener()
    img = Image.open(image_path).convert("RGB")
    tmp_path = image_path + ".paddletmp.jpg"
    img.save(tmp_path, format="JPEG", quality=90)
    return tmp_path


def _run_paddleocr(image_path: str) -> list[str]:
    """呼叫獨立的Python 3.11環境跑PaddleOCR，回傳偵測到的文字行列表。"""
    readable_path = _ensure_paddle_readable_path(image_path)
    try:
        result = subprocess.run(
            [_PADDLE_PYTHON, _PADDLE_SCRIPT, readable_path],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise RuntimeError(f"paddleocr子行程失敗: {result.stderr[-500:]}")
        return [l for l in result.stdout.splitlines() if l.strip()]
    finally:
        if readable_path != image_path and os.path.exists(readable_path):
            os.remove(readable_path)


def _build_system_prompt(field_schema: dict[str, str], task_description: str) -> str:
    context_line = f"這張圖片是「{task_description}」。" if task_description else ""
    fields_json = json.dumps(
        {k: f"{v}，沒有就填 null" for k, v in field_schema.items()},
        ensure_ascii=False,
        indent=2,
    )
    return f"""你是圖片資料判讀助手。使用者會給你一段用OCR從照片辨識出來的文字，
這段文字是逐行的偵測結果，順序可能跟圖片上的排版不完全一致，也可能有少數辨識雜訊。
{context_line}請根據這些文字整理成結構化資料。文字可能是繁體中文、簡體中文、英文，或中英夾雜。

只輸出一個 JSON 物件，不要有任何其他文字、不要用 markdown code block 包起來。欄位如下：

{fields_json}

規則：
- 完全看不出來的欄位一律填 null，不要瞎猜
- 這是OCR文字不是圖片，逐行文字本身就是最準確的依據，不要自己腦補修改文字內容
- 圖片常有裝飾圖案、浮水印、印章等非關鍵資訊文字，OCR可能把這類裝飾文字的殘影字元跟
  正確欄位排在相鄰行，不要把不相關、語意不通的零星字元硬湊進欄位內容
"""


def extract_structured_fields(
    image_path: str,
    field_schema: dict[str, str],
    task_description: str = "",
    client: anthropic.Anthropic | None = None,
) -> dict:
    """讀一張圖片，依 field_schema 指定的欄位回傳結構化擷取結果 dict。
    失敗時回傳 {"_error": "...", "_raw": "..."}

    field_schema: {"欄位名": "欄位說明"}，例如 {"name": "姓名", "date": "活動日期"}
    task_description: 這次要辨識的情境說明，例如「這是一張名片」「這是一張活動海報」
    """
    client = client or anthropic.Anthropic()

    ocr_lines = _run_paddleocr(image_path)
    if not ocr_lines:
        return {"_error": "PaddleOCR沒有讀到任何文字", "_raw": ""}
    ocr_text = "\n".join(ocr_lines)

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=_build_system_prompt(field_schema, task_description),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"以下是OCR辨識出的文字，請整理成JSON：\n\n{ocr_text}",
                    },
                ],
            }
        ],
    )

    raw_text = "".join(
        block.text for block in message.content if getattr(block, "type", None) == "text"
    )

    candidates = [raw_text]
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1:
        candidates.append(raw_text[start : end + 1])

    for candidate in list(candidates):
        candidates.append(_repair_stray_backslashes(candidate))

    for candidate in candidates:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    return {"_error": "JSON解析失敗", "_raw": raw_text}


def main() -> None:
    parser = argparse.ArgumentParser(description="通用圖片文字辨識→結構化欄位擷取")
    parser.add_argument("image_path", help="圖片路徑")
    parser.add_argument("--fields", help='欄位schema，JSON字串，例如 \'{"name":"姓名"}\'')
    parser.add_argument("--fields-file", help="欄位schema的JSON檔案路徑（跟 --fields 二擇一）")
    parser.add_argument("--task", default="", help="這張圖片的情境說明，例如「活動海報」「收據」")
    args = parser.parse_args()

    if args.fields_file:
        with open(args.fields_file, "r", encoding="utf-8") as f:
            field_schema = json.load(f)
    elif args.fields:
        field_schema = json.loads(args.fields)
    else:
        parser.error("必須指定 --fields 或 --fields-file")
        return

    result = extract_structured_fields(args.image_path, field_schema, args.task)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
