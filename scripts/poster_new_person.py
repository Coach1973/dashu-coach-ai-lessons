#!/usr/bin/env python3
"""
海報換人：一行指令出「橫版＋直版」兩張（中華新媒體影音發展協會版型）。

2026-10-24 教練：「他丟一張圖片、寫上職稱，就這麼簡單的事」——巴哈每次自己寫提示詞、挑模板、
查資料，10 分鐘還沒出圖。改成固定一行，不用想：

  python3 ~/.openclaw/workspace/scripts/poster_new_person.py \
    --photo <佩佩老師傳來的照片路徑> --name 林家羽 --role 秘書長 \
    --titles "時尚爵士新媒體製作公司執行長/南山人壽業務襄理 MDRT 百萬圓桌會員/亞伯安磁力健康按摩鞋 營銷總監"

版型＝王志玄已完成的中華新媒體版（頂部協會名、人物左側大字姓名＋職稱＋小字頭銜）。
兩張同時跑（各約 1～2 分鐘），存 PNG＋JPEG（JPEG 傳群組用），最後印出兩個 .jpg 路徑。
"""
import argparse
import re
import sys
import threading
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_poster_swap import generate_with_references  # noqa: E402
from PIL import Image  # noqa: E402

DATA = Path.home() / ".openclaw" / "workspace" / "claude-brain" / "data"
TEMPLATES = {
    "橫版": (DATA / "poster_wangzhixuan_horizontal_title_nmda_20261024.png", "1536x1024"),
    "直版": (DATA / "poster_wangzhixuan_portrait_title_nmda_20261024.png", "1024x1536"),
}

PROMPT = """第一張圖是一張已完成的{kind}宣傳海報（版面模板）。第二張圖是一位真人照片（臉部來源）。

其餘元素一律完全不變（依第一張圖）：版面與構圖、背景、頂部大標題「中華新媒體影音發展協會」與其下英文行、左上角圓形標誌、右側金色獎杯（不改造型、不加字）、中央「星耀亞洲 SHINING ACROSS ASIA」、器材、社群圖示、底部五個圖示與文字。

只改兩處：

一、人物：換成第二張照片裡的那位人物——臉部五官、髮型、膚色、性別必須就是本人（照片裡有戴眼鏡才戴）；保留原海報人物的位置與半身比例，姿勢可改為自然的雙手交叉或自然垂放；服裝改成得體的正式商務穿著；表情親切自信、直視前方。照片四周若有白邊、相框、扇子等裝飾，一律不要帶進海報。

二、人物左側文字（繁體中文，字形端正、清晰可讀、不得有錯字亂碼；位置與字體風格照第一張圖）：
- 大字姓名（原「王志玄」）改成：「{name}」
- 其下職稱（原「副理事長」）改成：「{role}」
- 其下原本兩行小字（「南投縣飛雁創業協會」「第六屆理事長」）全部拿掉，改成以下 {n} 行小字（每行一個，照順序，白色、字級略小、不要壓到人物身體）：
{lines}
"""


def make(kind, photo, name, role, titles, stamp):
    template, size = TEMPLATES[kind]
    prompt = PROMPT.format(kind=kind, name=name, role=role, n=len(titles),
                           lines="\n".join(f"「{t}」" for t in titles))
    img = generate_with_references(prompt, [template, photo], size)
    tag = "horizontal" if kind == "橫版" else "portrait"
    png = DATA / f"poster_{stamp}_{tag}.png"
    png.write_bytes(img)
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
