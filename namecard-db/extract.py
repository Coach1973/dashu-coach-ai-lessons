"""
名片欄位擷取：讀一張名片照片，回傳結構化欄位(dict)。

2026-07-12 改成兩階段管線（教練實測抓到MiniMax-M3直接看圖辨識準確率太差，
「黃薇雅」讀成「黃鈺翔」、「洪美香」讀成「洪美智」等真人名確認過的錯誤）：
    第一階段：PaddleOCR 本機辨識出照片上的文字（免費、不經過任何外部API）
    第二階段：把辨識出的文字（不是圖片）交給MiniMax整理成結構化欄位
PaddleOCR需要Python 3.11環境（PaddlePaddle不支援主環境的3.14），跑在
獨立的 paddleocr_venv，用subprocess呼叫 paddle_extract.py。
"""
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from minimax_batch_guard import guard_call  # noqa: E402

MODEL = os.environ.get("NAMECARD_MODEL", "MiniMax-M3")

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PADDLE_PYTHON = os.path.join(_THIS_DIR, "paddleocr_venv", "bin", "python3")
_PADDLE_SCRIPT = os.path.join(_THIS_DIR, "paddle_extract.py")
_TAXONOMY_PATH = os.path.join(_THIS_DIR, "taxonomy.json")


def _build_taxonomy_block() -> str:
    """把標準分類詞庫(taxonomy.json)整理成給AI參考的分組文字塊，
    供AI從中挑選最貼近的standard_category，不再自由發揮文字。"""
    if not os.path.exists(_TAXONOMY_PATH):
        return "（尚未建立標準分類詞庫，此欄位可留空）"
    with open(_TAXONOMY_PATH, encoding="utf-8") as f:
        taxonomy = json.load(f)
    grouped: dict[str, list[str]] = defaultdict(list)
    for item in taxonomy["items"]:
        grouped[item["category"]].append(item["name"])
    lines = []
    for category, names in grouped.items():
        unique_names = sorted(set(names))
        lines.append(f"[{category}] " + "、".join(unique_names))
    return "\n".join(lines)


_TAXONOMY_BLOCK = _build_taxonomy_block()

SYSTEM_PROMPT = f"""你是名片資料判讀助手。使用者會給你一段用OCR從名片照片辨識出來的文字，
這段文字是逐行的偵測結果，順序可能跟名片上的排版不完全一致，也可能有少數辨識雜訊。
請根據這些文字整理成結構化資料。名片可能是繁體中文、簡體中文、英文，或中英夾雜。

只輸出一個 JSON 物件，不要有任何其他文字、不要用 markdown code block 包起來。欄位如下：

{{
  "name": "姓名，沒有就填 null",
  "title": "職稱，沒有就填 null",
  "company": "公司名稱，沒有就填 null",
  "mobile": "手機號碼，沒有就填 null",
  "landline": "市話/公司電話，沒有就填 null",
  "email": "Email，沒有就填 null",
  "line_id": "LINE ID（可能標示為 LINE、Line ID、或直接是一串英數字加 ID 圖示），沒有就填 null",
  "website": "網址，沒有就填 null",
  "address": "地址，沒有就填 null",
  "tagline": "名片上印的產品/服務標語、口號、業務項目條列文字，逐字照抄，沒有就填 null",
  "category": "根據公司名稱、職稱、標語，用 4 個字以內判斷這家是做什麼產業/行業別，例如：保險、室內設計、食品批發、法律服務、餐飲設備。無法判斷就填 null",
  "standard_category": "從下方【標準分類詞庫】裡選一個語意最貼近的專業項目名稱，必須逐字照抄詞庫裡的寫法，不可自己改寫或縮寫；詞庫裡真的找不到任何貼近的項目才填 null",
  "keywords": ["3 到 8 個跟這家公司業務相關的關鍵字，中文為主，供之後搜尋與產業媒合使用"],
  "confidence_notes": "如果有欄位讀得不確定或看不清楚，簡短說明是哪個欄位，全部有把握就填 null"
}}

規則：
- 電話號碼統一整理成台灣常見格式（例如 0912-345-678 或 02-1234-5678），但不要臆測缺漏的數字
- 如果同一張名片有多組電話，mobile 放手機、landline 放市話，兩者都有就都填
- 完全看不出來的欄位一律填 null，不要瞎猜
- 這是OCR文字不是圖片，逐行文字本身就是最準確的依據，不要自己腦補修改文字內容
- 名片常有裝飾圖案、浮水印、印章、標語（如「深耕台灣 走向世界」）等非聯絡資訊文字，
  OCR可能把這類裝飾文字的殘影字元跟姓名/職稱等欄位排在相鄰行，不要把不相關的零星字元
  拼進姓名欄位——姓名通常是2到4個連續、語意通順的中文字，不要把明顯不相關或語意不通的
  字元硬湊進去

【標準分類詞庫】（standard_category必須從這裡面逐字選一項，這是BNI官方533項專業分類
+ 大台南南區682+產業全生態戰略總庫整合而成的權威詞庫，用於後續產業鏈精準媒合）：
{_TAXONOMY_BLOCK}
"""


def _repair_stray_backslashes(text: str) -> str:
    """名片標語常出現業主手寫的反斜線（如「農舍\\鐵皮屋」），不是合法JSON跳脫字元，
    會讓json.loads()直接炸掉。把非法的反斜線（後面不是合法跳脫字元）都跳脫成 \\\\。"""
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
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        return lines
    finally:
        if readable_path != image_path and os.path.exists(readable_path):
            os.remove(readable_path)


def extract_card_fields(image_path: str, client: anthropic.Anthropic | None = None) -> dict:
    """回傳擷取結果 dict。失敗時回傳 {"_error": "...", "_raw": "..."}"""
    client = client or anthropic.Anthropic()

    ocr_lines = _run_paddleocr(image_path)
    if not ocr_lines:
        return {"_error": "PaddleOCR沒有讀到任何文字", "_raw": ""}
    ocr_text = "\n".join(ocr_lines)

    guard_call("extract_card_fields")
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"以下是OCR辨識出的名片文字，請整理成JSON：\n\n{ocr_text}",
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
