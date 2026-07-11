"""
名片欄位擷取：讀一張名片照片，回傳結構化欄位(dict)。
用 Claude 的視覺理解直接讀卡片內容，不走傳統 OCR 軟體。
"""
import base64
import io
import json
import os
import re

import anthropic

MODEL = os.environ.get("NAMECARD_MODEL", "MiniMax-M3")

SYSTEM_PROMPT = """你是名片資料判讀助手。使用者會給你一張名片照片，請仔細讀出上面所有文字，
並整理成結構化資料。名片可能是繁體中文、簡體中文、英文，或中英夾雜。

只輸出一個 JSON 物件，不要有任何其他文字、不要用 markdown code block 包起來。欄位如下：

{
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
  "keywords": ["3 到 8 個跟這家公司業務相關的關鍵字，中文為主，供之後搜尋與產業媒合使用"],
  "confidence_notes": "如果有欄位讀得不確定或看不清楚，簡短說明是哪個欄位，全部有把握就填 null"
}

規則：
- 電話號碼統一整理成台灣常見格式（例如 0912-345-678 或 02-1234-5678），但不要臆測缺漏的數字
- 如果同一張名片有多組電話，mobile 放手機、landline 放市話，兩者都有就都填
- 完全看不出來的欄位一律填 null，不要瞎猜
"""


def _repair_stray_backslashes(text: str) -> str:
    """名片標語常出現業主手寫的反斜線（如「農舍\\鐵皮屋」），不是合法JSON跳脫字元，
    會讓json.loads()直接炸掉。把非法的反斜線（後面不是合法跳脫字元）都跳脫成 \\\\。"""
    return re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", text)


def _load_image_bytes(image_path: str) -> tuple[bytes, str]:
    ext = os.path.splitext(image_path)[1].lower()
    if ext in (".heic", ".heif"):
        import pillow_heif
        from PIL import Image

        pillow_heif.register_heif_opener()
        img = Image.open(image_path).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        return buf.getvalue(), "image/jpeg"

    media_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        return f.read(), media_type


def extract_card_fields(image_path: str, client: anthropic.Anthropic | None = None) -> dict:
    """回傳擷取結果 dict。失敗時回傳 {"_error": "...", "_raw": "..."}"""
    client = client or anthropic.Anthropic()
    image_bytes, media_type = _load_image_bytes(image_path)
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "請讀取這張名片照片，輸出 JSON。",
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
