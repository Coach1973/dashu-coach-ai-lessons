#!/usr/bin/env python3
"""活動場次海報改版一行指令（佩佩老師「政府資源不求人」這一系列直式海報，906×1280）。
2026-11-03 教練：巴哈改海報拖 30 分鐘；LK888 畫小字會錯（2:30／缺字／亂碼）→ 字一律電腦字體貼、人用 Vision 去背貼，AI 不碰。

用法（兩件事可只做其中一件；約 5 秒）：
  python3 ~/.openclaw/workspace/scripts/poster_event_edit.py <底圖.jpg> \
      --city 台南場 --date "2026/12/08 (二)" --time "下午 2:00 - 4:00" \
      --venue 以登企業會議室 --addr1 臺南市安南區安西里 --addr2 安通路四段46號 \
      --photo <本人照片.jpg> [--send-to -5115910257 --caption "…"]

- 場次區塊（左：城市／日期／時間，右：場地／地址兩行）整塊擦掉重貼；字一字不差照你給的參數。
- --photo：左下角那位人物換成這張照片的本人（macOS 內建人物去背，貼回原位，伸出的前臂收掉避免蓋到緞帶字）。
- 底圖不是 906×1280 同比例會直接報錯（座標是這張版型量的），不會亂貼。
- 輸出 PNG＋JPEG，最後一行印 JPEG 路徑；--send-to 給了就用 bot_peipei 傳回該 Telegram 聊天室（佩佩老師的巴哈助理群＝-5115910257）。
- 做完請親眼看一次成品（尤其日期時間地點）再傳；有 --send-to 時等於直接傳，所以參數要自己先核對。
"""
import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

BASE_W, BASE_H = 906, 1280
HERE = Path(__file__).resolve().parent
TOOLS = Path.home() / ".openclaw" / "workspace" / "data" / "tools"
OUT_ROOT = Path.home() / ".openclaw" / "workspace" / "data" / "lk888_edit"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
RED, NAVY = (200, 30, 36), (24, 41, 92)


def fail(msg):
    sys.exit("❌ " + msg)


def vision_cutout(photo, out_png):
    exe = TOOLS / "vision_cutout"
    src = HERE / "vision_cutout.swift"
    if not exe.exists() or exe.stat().st_mtime < src.stat().st_mtime:
        TOOLS.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["swiftc", "-O", str(src), "-o", str(exe)], capture_output=True, text=True)
        if r.returncode:
            fail("人物去背工具編譯失敗：" + r.stderr[-300:])
    r = subprocess.run([str(exe), str(photo), str(out_png)], capture_output=True, text=True)
    if r.returncode:
        fail("人物去背失敗（照片裡抓不到人？）：" + (r.stdout + r.stderr)[-200:])


def main():
    ap = argparse.ArgumentParser(description="活動場次海報改版（電腦字體＋人物去背）")
    ap.add_argument("base", help="底圖（906×1280 直式）")
    ap.add_argument("--city")
    ap.add_argument("--date")
    ap.add_argument("--time")
    ap.add_argument("--venue")
    ap.add_argument("--addr1")
    ap.add_argument("--addr2", default="")
    ap.add_argument("--photo", help="左下角要換成的本人照片")
    ap.add_argument("--out", help="輸出 JPEG 路徑（預設存 data/lk888_edit/）")
    ap.add_argument("--send-to", default=None)
    ap.add_argument("--account", default="bot_peipei")
    ap.add_argument("--caption", default="")
    a = ap.parse_args()

    text_args = [a.city, a.date, a.time, a.venue, a.addr1]
    do_text = any(text_args)
    if do_text and not all(text_args):
        fail("場次區塊要一次給齊：--city --date --time --venue --addr1（--addr2 可省）")
    if not do_text and not a.photo:
        fail("什麼都沒要改：給場次文字（--city…）或 --photo")

    im = Image.open(a.base).convert("RGB")
    W, H = im.size
    if abs(W / H - BASE_W / BASE_H) > 0.01:
        fail(f"底圖尺寸 {W}×{H} 不是這張版型的比例（906×1280）。這支只認這個版型，不要硬用。")
    k = W / BASE_W

    def S(v):
        return int(round(v * k))

    px = im.load()

    def fill_rows(y0, y1, x0, x1, srcx):
        for y in range(S(y0), S(y1)):
            c = px[S(srcx), y]
            for x in range(S(x0), S(x1)):
                px[x, y] = c

    if do_text:
        X0, X1, Y0, Y1 = S(58), S(872), S(846), S(1004)
        for y in range(Y0, Y1):
            L = im.crop((S(58), y, S(58) + 6, y + 1)).resize((1, 1), Image.BOX).getpixel((0, 0))
            R = im.crop((S(866), y, S(866) + 6, y + 1)).resize((1, 1), Image.BOX).getpixel((0, 0))
            for x in range(X0, X1):
                t = (x - X0) / (X1 - X0)
                px[x, y] = tuple(int(L[i] * (1 - t) + R[i] * t) for i in range(3))
        d = ImageDraw.Draw(im)

        def font(sz):
            return ImageFont.truetype(FONT, S(sz), index=0)

        def text(xy, s, size, fill, stroke=1, anchor="ls"):
            d.text((S(xy[0]), S(xy[1])), s, font=font(size), fill=fill, stroke_width=stroke, stroke_fill=fill, anchor=anchor)

        def pin(cx, cy, r):
            SS = 4
            rr = r * k * SS
            sz = int(r * k * 2.6) * SS
            tmp = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
            td = ImageDraw.Draw(tmp)
            cx2, cy2 = sz // 2, int(r * k * SS * 1.15)
            col = RED + (255,)
            td.polygon([(cx2 - rr * 0.85, cy2 + rr * 0.55), (cx2 + rr * 0.85, cy2 + rr * 0.55), (cx2, cy2 + rr * 2.0)], fill=col)
            td.ellipse([cx2 - rr, cy2 - rr, cx2 + rr, cy2 + rr], fill=col)
            td.ellipse([cx2 - rr * 0.38, cy2 - rr * 0.38, cx2 + rr * 0.38, cy2 + rr * 0.38], fill=(255, 255, 255, 255))
            tmp = tmp.resize((sz // SS, sz // SS), Image.LANCZOS)
            im.paste(tmp, (int(S(cx) - tmp.width / 2), int(S(cy) - r * k * 1.15)), tmp)

        pin(104, 889, 17)
        text((137, 903), a.city, 50, RED, 1)
        text((256, 951), a.date, 41, NAVY, 1, "ms")
        text((256, 993), a.time, 33, NAVY, 0, "ms")
        d.rectangle([S(454), S(866), S(456), S(1000)], fill=(70, 60, 60))
        pin(492, 895, 17)
        text((522, 913), a.venue, 45, NAVY, 1)
        addr1, addr2 = a.addr1, a.addr2
        if not addr2 and len(addr1) > 11:
            m = len(addr1) // 2
            addr1, addr2 = addr1[:m], addr1[m:]
        text((690, 955), addr1, 27, NAVY, 0, "ms")
        if addr2:
            text((690, 990), addr2, 27, NAVY, 0, "ms")

    if a.photo:
        TMP = OUT_ROOT / "_tmp"
        TMP.mkdir(parents=True, exist_ok=True)
        cut_png = TMP / f"cut_{datetime.now():%H%M%S}.png"
        vision_cutout(a.photo, cut_png)
        fill_rows(996, 1112, 96, 134, 136)  # 舊人物露出的頭、耳殘影，用旁邊乾淨背景色補平
        fill_rows(1040, 1100, 18, 46, 14)
        cut = Image.open(cut_png).convert("RGBA")
        full_w = cut.size[0]
        bb = cut.split()[3].getbbox()
        if not bb:
            fail("去背後是空的（照片裡沒抓到人）")
        cut = cut.crop(bb)
        ox = bb[0]
        mask = Image.new("L", cut.size, 255)
        md = ImageDraw.Draw(mask)
        # 伸出的前臂收掉：手肘右側 20px（2560 寬照片＝x 905~925）羽化後全透明，位置依照片寬度等比換算
        x_keep, x_gone = int(full_w * 905 / 2560), int(full_w * 925 / 2560)
        for x in range(cut.size[0]):
            xo = x + ox
            v = 255 if xo <= x_keep else (0 if xo >= x_gone else int(255 * (x_gone - xo) / (x_gone - x_keep)))
            md.line([(x, 0), (x, cut.size[1])], fill=v)
        cut.putalpha(ImageChops.multiply(cut.split()[3], mask))
        s = 0.23 * k * 2560 / full_w  # 照片 2560 寬時縮放 0.23；其他寬度等比換算
        cut = cut.resize((max(1, int(cut.width * s)), max(1, int(cut.height * s))), Image.LANCZOS)
        layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
        layer.paste(cut, (S(-42), S(994)))
        clip = Image.new("L", im.size, 0)
        clip.paste(255, (0, 0, W, S(1232)))  # 底部紅色頁尾壓在人物前面
        layer.putalpha(ImageChops.multiply(layer.split()[3], clip))
        im.paste(layer, (0, 0), layer)

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    jpg = Path(a.out).expanduser() if a.out else OUT_ROOT / f"poster_event_{datetime.now():%Y%m%d_%H%M%S}.jpg"
    png = jpg.with_suffix(".png")
    im.save(png)
    im.save(jpg, quality=95)
    if do_text:
        print("📝 貼上的字：", " | ".join(x for x in [a.city, a.date, a.time, a.venue, a.addr1, a.addr2] if x))
    if a.send_to:
        sys.path.insert(0, str(HERE))
        from generate_comic_panel import send_telegram_photo

        r = send_telegram_photo(a.send_to, jpg, a.caption, account=a.account)
        print(f"📤 已傳到 {a.send_to}（{a.account}）message_id={r['result']['message_id']}")
    print(f"✅ 完成：{jpg}")


if __name__ == "__main__":
    main()
