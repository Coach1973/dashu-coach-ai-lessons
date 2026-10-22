#!/usr/bin/env python3
"""海報換人換字（3 參考圖版）：模板海報 + 已完成直版成品（獎杯參考） + 真人照片。
用法：python3 generate_poster_swap_3ref.py --template A.jpg --ref2 直版成品.png --photo face.jpg \
      --prompt-file p.txt --size 1536x1024 --out out.png
"""
import argparse, base64, json, sys, urllib.request, lk888_guard
from datetime import datetime
from pathlib import Path
from generate_comic_panel import get_api_key, LK888_API_URL, WORKSPACE


def generate(prompt, image_paths, size, model="gpt-image-2"):
    boundary = "----PosterSwap3" + datetime.now().strftime("%H%M%S")
    body = []
    for p in image_paths:
        ctype = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        body.append(f"--{boundary}\r\n".encode())
        body.append(f'Content-Disposition: form-data; name="image[]"; filename="{p.name}"\r\nContent-Type: {ctype}\r\n\r\n'.encode("utf-8"))
        body.append(p.read_bytes()); body.append(b"\r\n")
    for name, val in (("prompt", prompt), ("model", model), ("size", size)):
        body.append(f"--{boundary}\r\n".encode())
        body.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.append(val.encode("utf-8")); body.append(b"\r\n")
    body.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(LK888_API_URL, data=b"".join(body),
        headers={"Authorization": f"Bearer {get_api_key()}",
                 "Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    with lk888_guard.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return base64.b64decode(result["data"][0]["b64_json"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", required=True)
    ap.add_argument("--ref2", required=True, help="已完成直版成品，只取獎杯造型參考")
    ap.add_argument("--photo", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--size", default="1536x1024")
    ap.add_argument("--model", default="gpt-image-2")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    paths = [Path(a.template), Path(a.ref2), Path(a.photo)]
    for p in paths:
        if not p.exists():
            raise FileNotFoundError(f"圖不存在: {p}")
    img = generate(Path(a.prompt_file).read_text(encoding="utf-8"), paths, a.size, a.model)
    out = Path(a.out) if a.out else WORKSPACE / "claude-brain" / "data" / f"poster_swap3_{datetime.now():%Y%m%d-%H%M%S}.png"
    out.parent.mkdir(parents=True, exist_ok=True); out.write_bytes(img)
    print(f"圖片已存檔：{out}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr); sys.exit(1)
