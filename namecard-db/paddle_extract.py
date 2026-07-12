"""
獨立跑在 paddleocr_venv（Python 3.11）的 OCR 子行程。
用法：python3 paddle_extract.py <圖片路徑>
輸出：辨識出的文字，一行一個印到 stdout（給 extract.py 的 subprocess 讀）。
"""
import sys

from paddleocr import PaddleOCR

_OCR = None


def get_ocr() -> PaddleOCR:
    global _OCR
    if _OCR is None:
        _OCR = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=True)
    return _OCR


def main() -> None:
    image_path = sys.argv[1]
    ocr = get_ocr()
    results = ocr.predict(image_path)
    for res in results:
        texts = res.get("rec_texts") or []
        for text in texts:
            if text and text.strip():
                print(text.strip())


if __name__ == "__main__":
    main()
