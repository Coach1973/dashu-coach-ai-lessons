"""
一張照片拍多張名片(教練要求提升效率：一次拍6~8張，不用一張一張拍)，
用AI視覺偵測每張名片的邊界框，自動裁切成多張獨立圖片，各自走原本的
辨識管線(PaddleOCR+MiniMax整理欄位)。

技術驗證(2026-08-25實測)：MiniMax-M3支援圖片輸入(vision)，且對名片
邊界框定位準確——4張名片合照測試，AI回傳的邊界框比手動估算的更貼合
實際名片範圍，不會切到名片內容或留太多背景。
"""
import base64
import json
import os

import anthropic

_MEDIA_TYPES = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".webp": "image/webp",
}

DETECT_PROMPT = """這張照片裡可能有一張或多張名片並排放置。請找出每一張名片在圖片中的邊界框位置。

只輸出一個JSON陣列，不要有其他文字、不要用markdown code block包起來：
[
  {"index": 1, "x_min": 0.0到1.0之間的比例, "y_min": 同上, "x_max": 同上, "y_max": 同上},
  ...
]

座標是相對於整張圖片寬高的比例(0=最左/最上，1=最右/最下)，不是絕對像素。
依照名片在畫面中由上到下、由左到右的順序編號。
如果整張照片其實只有一張名片(填滿或接近填滿畫面)，就只回傳一個元素。
如果完全看不出來是名片(例如空白照片、風景照、純文字文件)，回傳空陣列[]。
"""


def _to_jpeg_bytes(image_path: str) -> bytes:
    """統一轉成JPEG bytes餵給AI視覺模型；HEIC需要先解碼(Anthropic API不吃HEIC)"""
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in (".heic", ".heif"):
        with open(image_path, "rb") as f:
            return f.read()

    import io

    import pillow_heif
    from PIL import Image

    pillow_heif.register_heif_opener()
    img = Image.open(image_path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return buf.getvalue()


def _extract_json_array(raw_text: str) -> list:
    start = raw_text.find("[")
    end = raw_text.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        return json.loads(raw_text[start : end + 1])
    except json.JSONDecodeError:
        return []


def detect_card_regions(image_path: str, client: anthropic.Anthropic, model: str) -> list[dict]:
    """回傳這張照片裡偵測到的名片邊界框清單(比例座標，已驗證合法性)"""
    img_bytes = _to_jpeg_bytes(image_path)
    img_b64 = base64.b64encode(img_bytes).decode()

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                    {"type": "text", "text": DETECT_PROMPT},
                ],
            }
        ],
    )
    raw_text = "".join(b.text for b in message.content if getattr(b, "type", None) == "text")
    regions = _extract_json_array(raw_text)

    valid = []
    for r in regions:
        try:
            x_min, y_min = float(r["x_min"]), float(r["y_min"])
            x_max, y_max = float(r["x_max"]), float(r["y_max"])
            if 0 <= x_min < x_max <= 1 and 0 <= y_min < y_max <= 1:
                valid.append({"x_min": x_min, "y_min": y_min, "x_max": x_max, "y_max": y_max})
        except (KeyError, ValueError, TypeError):
            continue
    return valid


def split_image(image_path: str, regions: list[dict], output_folder: str, base_name: str) -> list[str]:
    """依邊界框裁切成多張獨立圖片，存進output_folder，回傳新檔名清單"""
    import pillow_heif
    from PIL import Image

    pillow_heif.register_heif_opener()
    img = Image.open(image_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size

    saved_files = []
    for i, r in enumerate(regions, 1):
        pad_x = (r["x_max"] - r["x_min"]) * 0.03
        pad_y = (r["y_max"] - r["y_min"]) * 0.03
        left = max(0, int((r["x_min"] - pad_x) * w))
        top = max(0, int((r["y_min"] - pad_y) * h))
        right = min(w, int((r["x_max"] + pad_x) * w))
        bottom = min(h, int((r["y_max"] + pad_y) * h))

        crop = img.crop((left, top, right, bottom))
        filename = f"{base_name}_split{i}.jpg"
        crop.save(os.path.join(output_folder, filename), format="JPEG", quality=90)
        saved_files.append(filename)
    return saved_files
