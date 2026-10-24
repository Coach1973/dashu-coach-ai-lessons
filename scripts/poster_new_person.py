#!/usr/bin/env python3
"""
海報換人：一行指令出「橫版＋直版」兩張（中華新媒體影音發展協會版型）。

2026-10-24 教練：「他丟一張圖片、寫上職稱，就這麼簡單的事」——巴哈每次自己寫提示詞、挑模板、
查資料，10 分鐘還沒出圖。改成固定一行，不用想：

  python3 ~/.openclaw/workspace/scripts/poster_new_person.py \
    --photo <佩佩老師傳來的照片路徑> --name 林家羽 --role 秘書長 \
    --titles "時尚爵士新媒體製作公司執行長/南山人壽業務襄理 MDRT 百萬圓桌會員/亞伯安磁力健康按摩鞋 營銷總監"

版型＝王志玄已完成的中華新媒體版（頂部協會名、人物左側大字姓名＋職稱＋小字頭銜）。
兩張同時跑（約 1～2 分鐘），頭銜由程式用電腦字體排大字（跟底部「影音製作」一樣大、太長自動分行），
存 PNG＋JPEG（JPEG 傳群組用），最後印出兩個 .jpg 路徑。
"""
import argparse
import re
import sys
import threading
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_poster_swap import generate_with_references  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402

DATA = Path.home() / ".openclaw" / "workspace" / "claude-brain" / "data"
TEMPLATES = {
    "橫版": (DATA / "poster_wangzhixuan_horizontal_title_nmda_20261024.png", "1536x1024",
             "人物左邊緣大約在畫面寬度 38% 的位置，文字放在畫面左側 5%～35% 之間"),
    "直版": (DATA / "poster_wangzhixuan_portrait_title_nmda_20261024.png", "1024x1536",
             "人物放右半邊、左邊緣大約在畫面寬度 45% 的位置，文字放在畫面左側 5%～42% 之間"),
}

PROMPT = """第一張圖是一張已完成的{kind}宣傳海報（版面模板）。第二張圖是一位真人照片（臉部來源）。

其餘元素一律完全不變（依第一張圖）：版面與構圖、背景、頂部大標題「中華新媒體影音發展協會」與其下英文行、左上角圓形標誌、右側金色獎杯（不改造型、不加字）、中央「星耀亞洲 SHINING ACROSS ASIA」、器材、社群圖示、底部五個圖示與文字。

只改以下幾處：

一、人物：換成第二張照片裡的那位人物。最重要：一看就要認得出是本人——臉型、五官比例、眼型、鼻子、嘴型與笑容、髮型、膚色、年齡感都照第二張照片，不要美化、不要瘦臉、不要變年輕、不要變成網紅臉或模特兒臉（照片裡有戴眼鏡才戴）。姿勢、頭的角度、表情與笑容也照第二張照片（例如照片是單手托腮、頭微側，就照做）；服裝改成得體的正式商務穿著；半身。照片四周若有白邊、相框、扇子等裝飾，一律不要帶進海報。

二、版面：人物整體放在畫面中間偏右（{person_pos}），人物左邊留出一整塊乾淨空白給文字。所有文字（姓名、職稱、頭銜）都只能放在這塊空白裡，一個字都不可以壓到人物的頭髮、臉、衣服或手臂。

三、人物左側只寫兩行字（繁體中文，字形端正、清晰可讀、不得有錯字亂碼；字體風格照第一張圖）：
- 大字姓名（原「王志玄」）改成：「{name}」
- 其下職稱（原「副理事長」）改成：「{role}」
- 其下原本兩行小字（「南投縣飛雁創業協會」「第六屆理事長」）全部拿掉，那一塊留白、乾淨無字（頭銜之後另外排）。
"""


# 頭銜用電腦字體排大字（教練 10/24：字跟底部「影音製作」一樣大，不寫小字；AI 寫小字常錯）
FONT = "/System/Library/Fonts/Supplemental/Songti.ttc"  # index 2 = 宋體-繁 粗體
COLUMN = {"橫版": (0.04, 0.29, 0.25, 0.55), "直版": (0.04, 0.42, 0.25, 0.50)}  # 左欄 x 起訖、找職稱的 y 範圍（比例）
POSITION_WORDS = ["總經理", "董事長", "理事長", "執行長", "總監", "襄理", "經理", "會長", "創辦人", "負責人", "院長", "主任", "顧問", "講師"]


def wrap(text, font, maxw, d):
    if d.textlength(text, font=font) <= maxw:
        return [text]
    if " " in text:
        head, tail = text.split(" ", 1)
        return wrap(head, font, maxw, d) + wrap(tail, font, maxw, d)
    for w in POSITION_WORDS:
        i = text.rfind(w)
        if i > 0:
            return wrap(text[:i], font, maxw, d) + wrap(text[i:], font, maxw, d)
    cut = len(text)
    while cut > 1 and d.textlength(text[:cut], font=font) > maxw:
        cut -= 1
    return [text[:cut]] + wrap(text[cut:], font, maxw, d)


def fix_name(png, kind, name):
    """2026-10-25 教練：AI 畫姓名遇少見字會畫錯（瀞→灝、枘→棶）。姓名也改用電腦字體重排：
    先把 AI 畫的姓名抹成乾淨底色，再用宋體粗體寫上正確的字，位置、大小照原來那一塊。"""
    im = Image.open(png).convert("RGB")
    W, H = im.size
    x0r, x1r, y0r, y1r = COLUMN[kind]
    gx0, gx1 = int(W * x0r), int(W * (x1r - 0.04))
    gy0, gy1 = int(H * y0r), int(H * y1r)
    a = np.array(im).astype(float)
    dark = np.array(im.convert("L"))[gy0:gy1, gx0:gx1] < 60
    rows = np.where(dark.sum(1) > 25)[0]
    if not len(rows):
        return
    r0 = r1 = rows[0]
    for r in rows:                      # 第一組連續的深色列＝姓名（姓名與職稱之間有空隙）
        if r - r1 > 8:
            break
        r1 = r
    cols = np.where(dark[r0:r1 + 1].sum(0) > 1)[0]
    c0, c1 = gx0 + cols.min(), gx0 + cols.max()
    y0, y1 = gy0 + r0, gy0 + r1
    pad = 14
    ys, ye, xs, xe = max(0, y0 - pad), min(H, y1 + pad), max(0, c0 - pad), min(W, c1 + pad)
    mask = np.zeros((H, W), bool)
    sub = np.array(im.convert("L"))[ys:ye, xs:xe] < 150
    mask[ys:ye, xs:xe] = np.array(Image.fromarray((sub * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))) > 0
    def blur(x, r=12):                  # 方框模糊（numpy 累加），浮點圖 PIL 不支援
        for ax in (0, 1):
            c = np.cumsum(np.pad(x, [(r + 1, r) if i == ax else (0, 0) for i in range(x.ndim)], mode="edge"), axis=ax)
            x = (np.take(c, range(2 * r + 1, c.shape[ax]), axis=ax) - np.take(c, range(0, c.shape[ax] - 2 * r - 1), axis=ax)) / (2 * r + 1)
        return x
    for _ in range(6):                  # 用周圍的底色往裡填（柔和的漸層底色）
        w = (~mask).astype(float)
        den = blur(w)[..., None]
        fill = blur(a * w[..., None]) / np.maximum(den, 1e-3)
        a = np.where(mask[..., None] & (den > 1e-3), fill, a)
        mask = mask & (den[..., 0] <= 1e-3)
    im = Image.fromarray(a.clip(0, 255).astype("uint8"))
    size = int((y1 - y0 + 1) / 0.9)
    font = ImageFont.truetype(FONT, size, index=2)
    maxw = int(W * x1r) - int(c0)
    while font.getlength(name) > max(maxw, c1 - c0 + 40) and size > 20:
        size -= 2
        font = ImageFont.truetype(FONT, size, index=2)
    d = ImageDraw.Draw(im)
    bbox = d.textbbox((0, 0), name, font=font)
    d.text((c0 - bbox[0], y0 - bbox[1]), name, font=font, fill=(12, 12, 12))
    im.save(png)


def draw_titles(png, kind, titles):
    im = Image.open(png).convert("RGB")
    W, H = im.size
    x0r, x1r, y0r, y1r = COLUMN[kind]
    g = np.array(im.convert("L"))
    gx0, gx1 = int(W * x0r), int(W * (x1r - 0.04))
    box = g[int(H * y0r):int(H * y1r), gx0:gx1] < 60   # 姓名、職稱是黑色大字
    hit = np.where(box.sum(1) > 25)[0]
    # 只取最上面那一塊（姓名＋職稱，中間空隙 ≤ 40px），下方城市背景的暗處不算
    end = hit[0] if len(hit) else 0
    for r in hit:
        if r - end > 40:
            break
        end = r
    block = box[hit[0]:end + 1] if len(hit) else box[:0]
    cols = np.where(block.sum(0) > 2)[0]
    left = gx0 + (cols.min() if len(cols) else 40)
    top = int(H * y0r) + (end if len(hit) else int(H * 0.2)) + 22
    fs = 26
    font = ImageFont.truetype(FONT, fs, index=2)
    d = ImageDraw.Draw(im)
    maxw = int(W * x1r) - left
    lines = [ln for t in titles for ln in wrap(t, font, maxw, d)]
    glow = Image.new("L", im.size, 0)
    gd = ImageDraw.Draw(glow)
    for i, ln in enumerate(lines):
        gd.text((left, top + i * 36), ln, font=font, fill=255, stroke_width=4, stroke_fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(3)).point(lambda v: min(255, int(v * 1.4)))
    im = Image.composite(Image.new("RGB", im.size, (255, 250, 242)), im, glow)
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text((left, top + i * 36), ln, font=font, fill=(12, 12, 12))
    im.save(png)


def make(kind, photo, name, role, titles, stamp):
    template, size, person_pos = TEMPLATES[kind]
    prompt = PROMPT.format(kind=kind, person_pos=person_pos, name=name, role=role)
    img = generate_with_references(prompt, [template, photo], size)
    tag = "horizontal" if kind == "橫版" else "portrait"
    png = DATA / f"poster_{stamp}_{tag}.png"
    png.write_bytes(img)
    png.with_name(png.stem + "_raw.png").write_bytes(img)  # 沒排頭銜的原圖，重排字用
    fix_name(png, kind, name)   # 姓名由電腦字體重排，避免少見字被 AI 畫錯
    if titles:
        draw_titles(png, kind, titles)
    jpg = png.with_suffix(".jpg")
    Image.open(png).convert("RGB").save(jpg, "JPEG", quality=90)
    return jpg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photo", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--role", default="", help="姓名下面那一行，例如 秘書長、副理事長")
    ap.add_argument("--titles", default="", help="頭銜，用 / 或 、 或換行分隔")
    ap.add_argument("--only", choices=["橫版", "直版"], help="只出一張（重做時用）")
    a = ap.parse_args()

    photo = Path(a.photo).expanduser()
    if not photo.exists():
        sys.exit(f"錯誤：照片不存在 {photo}")
    titles = [t.strip() for t in re.split(r"[/／、\n]", a.titles) if t.strip()]
    stamp = f"{a.name}_{datetime.now():%Y%m%d_%H%M}"
    kinds = [a.only] if a.only else ["橫版", "直版"]
    results, errors = {}, {}

    def run(k):
        try:
            results[k] = make(k, photo, a.name, a.role, titles, stamp)
        except Exception as e:  # noqa: BLE001
            errors[k] = e

    threads = [threading.Thread(target=run, args=(k,)) for k in kinds]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for k in kinds:
        if k in results:
            print(f"{k}：{results[k]}")
        else:
            print(f"{k} 失敗：{errors[k]}", file=sys.stderr)
    sys.exit(0 if results else 1)


if __name__ == "__main__":
    main()
