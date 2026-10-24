#!/usr/bin/env python3
"""
海報「只改文字」：拿一張已完成的海報當唯一參考圖，lk888 /v1/images/edits 重畫，只改 prompt 指定的文字。
（generate_poster_swap.py 是換人用、要兩張圖；這支是改字用、只要一張圖。）

用法：
  python3 poster_edit_text.py --image <現成海報.png> --prompt-file <prompt.txt> \
      --size 1536x1024 --out <輸出.png>        # 直版用 1024x1536
一次只跑一張，不重跑（每次都扣 LK888 額度）。
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_poster_swap as g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--size", default="1536x1024")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    prompt = Path(a.prompt_file).read_text(encoding="utf-8")
    img = g.generate_with_references(prompt, [Path(a.image)], a.size)
    Path(a.out).write_bytes(img)
    print("OK", a.out, len(img))


if __name__ == "__main__":
    main()
