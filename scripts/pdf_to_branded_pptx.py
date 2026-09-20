#!/usr/bin/env python3
"""
PDF轉品牌底圖PPT：把每頁PDF插圖套上指定底圖(如BNI ACCELERATE)，
自動避開底圖角落的LOGO/裝飾區，插圖其餘部分維持滿版。

用法：
  python3 pdf_to_branded_pptx.py --pdf 簡報.pdf --bg 底圖.jpg --out 輸出.pptx

同一份底圖重複使用時，遮罩比例(--mask-*)不用重新量測，直接沿用預設值即可
（預設值就是2026-09-21幫BNI ACCELERATE底圖量出來的座標）。
換一張新底圖、LOGO位置不同時，才需要依「重新量測遮罩」章節的做法重新測一次，
再用 --mask-* 參數覆蓋。
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Emu

EMU_PER_INCH = 914400


def extract_pdf_pages(pdf_path: Path, out_dir: Path, dpi: int = 150) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = out_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf_path), str(prefix)],
        check=True,
    )
    return sorted(out_dir.glob("page-*.png"))


def build_mask(w: int, h: int, logo_box: tuple, swoosh_tri: tuple, feather: int) -> Image.Image:
    """logo_box: (x0_ratio,y0_ratio,x1_ratio,y1_ratio) 矩形保護區(左下角LOGO)
       swoosh_tri: (x0_ratio, apex_y_ratio) 右下角三角形保護區，從(x0,h)到(w,h)到(w,apex_y)"""
    mask = Image.new("L", (w, h), 255)
    draw = ImageDraw.Draw(mask)

    lx0, ly0, lx1, ly1 = logo_box
    draw.rectangle([lx0 * w, ly0 * h, lx1 * w, ly1 * h], fill=0)

    sx0, sy0 = swoosh_tri
    draw.polygon([(sx0 * w, h), (w, h), (w, sy0 * h)], fill=0)

    return mask.filter(ImageFilter.GaussianBlur(feather))


def compose(bg_path: Path, page_paths: list[Path], out_dir: Path, mask: Image.Image) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    bg = Image.open(bg_path).convert("RGB")
    W, H = bg.size
    results = []
    for i, page_path in enumerate(page_paths, 1):
        illus = Image.open(page_path).convert("RGB")
        src_ratio = illus.width / illus.height
        dst_ratio = W / H
        if src_ratio > dst_ratio:
            new_h = H
            new_w = int(H * src_ratio)
        else:
            new_w = W
            new_h = int(W / src_ratio)
        illus_resized = illus.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - W) // 2
        top = (new_h - H) // 2
        illus_cropped = illus_resized.crop((left, top, left + W, top + H))

        composed = Image.composite(illus_cropped, bg, mask)
        out_path = out_dir / f"slide-{i:02d}.png"
        composed.save(out_path, quality=95)
        results.append(out_path)
    return results


def build_pptx(slide_images: list[Path], out_pptx: Path):
    slide_w = int(13.333 * EMU_PER_INCH)
    slide_h = int(7.5 * EMU_PER_INCH)
    prs = Presentation()
    prs.slide_width = Emu(slide_w)
    prs.slide_height = Emu(slide_h)
    blank_layout = prs.slide_layouts[6]
    for img_path in slide_images:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(str(img_path), 0, 0, width=Emu(slide_w), height=Emu(slide_h))
    prs.save(str(out_pptx))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="來源PDF路徑")
    ap.add_argument("--bg", required=True, help="品牌底圖路徑(jpg/png)")
    ap.add_argument("--out", required=True, help="輸出.pptx路徑")
    ap.add_argument("--work-dir", default=None, help="暫存頁面/合成圖目錄，預設用輸出檔旁邊的_work資料夾")
    ap.add_argument("--dpi", type=int, default=150, help="PDF轉圖DPI，數字越大越清晰但越慢")
    ap.add_argument("--feather", type=int, default=28, help="遮罩羽化程度(像素)，數字越大過渡越柔和")
    # 預設值＝2026-09-21幫BNI ACCELERATE底圖量出來的座標，換底圖才需要調整
    ap.add_argument("--mask-logo-box", default="0,0.854,0.296,1.0",
                     help="左下角LOGO保護區 x0,y0,x1,y1(比例0~1)")
    ap.add_argument("--mask-swoosh", default="0.804,0.799",
                     help="右下角三角形保護區 x0,apex_y(比例0~1)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    bg_path = Path(args.bg)
    out_pptx = Path(args.out)
    work_dir = Path(args.work_dir) if args.work_dir else out_pptx.parent / f"{out_pptx.stem}_work"

    logo_box = tuple(float(v) for v in args.mask_logo_box.split(","))
    swoosh_tri = tuple(float(v) for v in args.mask_swoosh.split(","))

    print(f"[1/4] 抽取PDF頁面（{args.dpi} DPI）...")
    pages_dir = work_dir / "pages"
    page_paths = extract_pdf_pages(pdf_path, pages_dir, args.dpi)
    print(f"      共 {len(page_paths)} 頁")

    print("[2/4] 建立遮罩...")
    bg = Image.open(bg_path)
    mask = build_mask(bg.width, bg.height, logo_box, swoosh_tri, args.feather)

    print("[3/4] 合成每張投影片...")
    slides_dir = work_dir / "slides"
    slide_images = compose(bg_path, page_paths, slides_dir, mask)

    print("[4/4] 組裝PPTX...")
    build_pptx(slide_images, out_pptx)

    print(f"完成：{out_pptx}（共 {len(slide_images)} 張投影片）")
    print(f"合成過程檔案保留在：{work_dir}（確認OK後可自行刪除）")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        print("錯誤：pdftoppm執行失敗，請確認已安裝poppler（brew install poppler）", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"錯誤：{e}", file=sys.stderr)
        sys.exit(1)
