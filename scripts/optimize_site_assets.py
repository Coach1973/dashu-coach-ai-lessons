#!/usr/bin/env python3
"""個人作品上架前自動壓縮圖片／影片（2026-10-02 教練裁示：無論檔案大小，只要網頁上能清楚呈現，一律壓成較小格式）

用法：
  python3 scripts/optimize_site_assets.py <網站資料夾> [--dry-run]
上傳流程（curation_process.py 的 kind=creation）會自動呼叫，失敗時照原檔上架，不擋上架。

做法（只動檔案，不動網頁排版）：
- 圖片（png/jpg/jpeg）大於 100KB 才處理；最長邊超過 2000px 縮到 2000px（手機＋視網膜螢幕夠清楚）；
  存成 webp（色彩多的照片用 q82；色彩很少的圖表／文字圖用無損 webp，字不會糊）；
  省不到 25% 就保留原檔。
- 只在「網頁文字檔（html/css/js/json）裡真的找得到這個檔名」時才換成 webp 並改引用；
  找不到引用（可能是程式動態組檔名）就不動，避免弄壞圖。
- 同檔名出現在不同資料夾時，全部轉或全部不轉，避免引用對不上。
- 外部網址（http://、https://、//）裡的同名檔案不會被改。
- 影片 mp4 大於 10MB 才重新編碼（H.264，最長邊 1280、CRF 28、faststart），省不到 20% 就保留原檔，檔名不變。
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

IMG_MIN_BYTES = 100 * 1024
IMG_MAX_EDGE = 2000
IMG_MIN_SAVING = 0.25
GRAPHIC_MAX_COLORS = 4096
VIDEO_MIN_BYTES = 10 * 1024 * 1024
VIDEO_MIN_SAVING = 0.20
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".svg", ".txt", ".xml"}
IMG_SUFFIXES = {".png", ".jpg", ".jpeg"}


def _fmt(n: int) -> str:
    return f"{n / 1024 / 1024:.1f}MB" if n >= 1024 * 1024 else f"{n / 1024:.0f}KB"


def _text_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES]


def _encode_webp(src: Path, dest: Path) -> bool:
    """回傳 True 表示已寫出 dest。"""
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        w, h = im.size
        if max(w, h) > IMG_MAX_EDGE:
            scale = IMG_MAX_EDGE / max(w, h)
            im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        im = im.convert("RGBA" if has_alpha else "RGB")
        probe = im.copy()
        probe.thumbnail((400, 400))
        few_colors = probe.convert("RGB").getcolors(maxcolors=GRAPHIC_MAX_COLORS) is not None
        if few_colors:
            im.save(dest, "WEBP", lossless=True, quality=100, method=6)
        else:
            im.save(dest, "WEBP", quality=82, method=6)
    return dest.exists()


_REF_DELIMS = frozenset(" \t\r\n\f\v\"'()<>,=")      # token 往左延伸的邊界
_REF_AFTER = frozenset(" \t\r\n\f\v\"'()<>,?#;")     # 檔名後面允許接的字元


def _rewrite_refs(text: str, old_name: str, new_name: str) -> tuple[str, int]:
    """把『不是外部網址』的 token 裡的 old_name 換成 new_name。
    2026-10-15 重寫：原本用 `[^\\s"'()<>,=]*` + 檔名的 regex，遇到 10MB 內嵌圖片資料（一整段沒有空白的 base64）
    會對每個起點都掃到底再倒退，變成平方級，陳淑玲品牌網頁包 15 分鐘還沒跑完（10/13 真公益包同病，當時靠瘦身繞過）。
    改成先用字串找檔名出現的位置，再只往左延伸一次，語意不變、時間線性。"""
    if old_name not in text:
        return text, 0
    out: list[str] = []
    last = 0
    count = 0
    n = len(text)
    L = len(old_name)
    pos = text.find(old_name)
    while pos != -1:
        end = pos + L
        if pos >= last and (end >= n or text[end] in _REF_AFTER):
            b = pos
            while b > last and text[b - 1] not in _REF_DELIMS:
                b -= 1
            token = text[b:end]
            if not token.startswith(("http://", "https://", "//")):
                out.append(text[last:b])
                out.append(token[:-L] + new_name)
                last = end
                count += 1
        pos = text.find(old_name, pos + 1)
    out.append(text[last:])
    return "".join(out), count


def optimize_images(root: Path, dry_run: bool, report: dict) -> None:
    candidates: dict[str, list[Path]] = {}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in IMG_SUFFIXES and p.stat().st_size > IMG_MIN_BYTES:
            candidates.setdefault(p.name, []).append(p)
    if not candidates:
        return
    texts = {p: p.read_text(encoding="utf-8", errors="ignore") for p in _text_files(root)}

    for name, paths in candidates.items():
        # 找得到引用才處理
        refs = sum(_rewrite_refs(t, name, "x")[1] for t in texts.values())
        if refs == 0:
            report["skipped"].append(f"{name}（網頁文字裡找不到引用，不動）")
            continue
        new_name = Path(name).stem + ".webp"
        if any((p.parent / new_name).exists() for p in paths):
            report["skipped"].append(f"{name}（同資料夾已有 {new_name}，不動）")
            continue
        tmp_out: list[tuple[Path, Path]] = []
        ok = True
        for p in paths:
            out = p.parent / new_name
            try:
                _encode_webp(p, out)
            except Exception as e:  # noqa: BLE001
                report["skipped"].append(f"{name}（轉檔失敗：{e}）")
                ok = False
                break
            if out.stat().st_size > p.stat().st_size * (1 - IMG_MIN_SAVING):
                out.unlink(missing_ok=True)
                report["skipped"].append(f"{name}（省不到 {int(IMG_MIN_SAVING * 100)}%，保留原檔）")
                ok = False
                break
            tmp_out.append((p, out))
        if not ok:
            for _, out in tmp_out:
                out.unlink(missing_ok=True)
            continue
        if dry_run:
            for p, out in tmp_out:
                report["items"].append((str(p.relative_to(root)), p.stat().st_size, out.stat().st_size))
                out.unlink(missing_ok=True)
            continue
        # 正式改：改引用、刪原檔
        for tp, t in list(texts.items()):
            new_t, n = _rewrite_refs(t, name, new_name)
            if n:
                tp.write_text(new_t, encoding="utf-8")
                texts[tp] = new_t
        for p, out in tmp_out:
            report["items"].append((str(p.relative_to(root)), p.stat().st_size, out.stat().st_size))
            p.unlink()


def optimize_videos(root: Path, dry_run: bool, report: dict) -> None:
    if not shutil.which("ffmpeg"):
        return
    for p in root.rglob("*.mp4"):
        if not p.is_file() or p.stat().st_size <= VIDEO_MIN_BYTES:
            continue
        out = p.with_name(p.stem + ".__opt__.mp4")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(p),
               "-vf", "scale='min(1280,iw)':-2", "-c:v", "libx264", "-crf", "28", "-preset", "veryfast",
               "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)]
        try:
            subprocess.run(cmd, check=True, timeout=900)
        except Exception as e:  # noqa: BLE001
            out.unlink(missing_ok=True)
            report["skipped"].append(f"{p.name}（影片壓縮失敗：{e}）")
            continue
        before, after = p.stat().st_size, out.stat().st_size
        if dry_run or after > before * (1 - VIDEO_MIN_SAVING):
            if not dry_run:
                report["skipped"].append(f"{p.name}（省不到 {int(VIDEO_MIN_SAVING * 100)}%，保留原檔）")
            else:
                report["items"].append((str(p.relative_to(root)), before, after))
            out.unlink(missing_ok=True)
            continue
        out.replace(p)
        report["items"].append((str(p.relative_to(root)), before, after))


def optimize_dir(root: Path, dry_run: bool = False) -> dict:
    root = Path(root)
    report: dict = {"items": [], "skipped": [], "before": 0, "after": 0}
    report["before"] = sum(f.stat().st_size for f in root.rglob("*") if f.is_file())
    optimize_images(root, dry_run, report)
    optimize_videos(root, dry_run, report)
    report["after"] = sum(f.stat().st_size for f in root.rglob("*") if f.is_file()) if not dry_run else \
        report["before"] - sum(b - a for _, b, a in report["items"])
    return report


def summarize(report: dict) -> str:
    n = len(report["items"])
    line = f"🗜 壓縮 {n} 個檔案：整包 {_fmt(report['before'])} → {_fmt(report['after'])}" if n else \
        f"🗜 沒有需要壓縮的檔案（整包 {_fmt(report['before'])}）"
    if report["skipped"]:
        line += f"；未動 {len(report['skipped'])} 個（{'；'.join(report['skipped'][:3])}）"
    return line


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    rep = optimize_dir(Path(args[0]), dry_run="--dry-run" in sys.argv)
    for rel, b, a in rep["items"]:
        print(f"  {rel}: {_fmt(b)} → {_fmt(a)}")
    print(summarize(rep))
