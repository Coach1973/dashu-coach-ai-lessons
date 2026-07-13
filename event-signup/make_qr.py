"""
產生活動QR code。跑法：
  venv/bin/python3 make_qr.py <slug>     單一活動的QR（掃了直接進那場報名頁，網址含slug）
  venv/bin/python3 make_qr.py --checkin  固定簽到QR（掃了永遠導向後台設定的「目前活動」，
                                          網址不含slug，一勞永逸不用重印，後台切換場次見/admin）
輸出：qr/<slug 或 checkin>.png（高解析，印刷可用）+ 對應 -print.html（A4立牌頁）
"""
import os
import sys

import qrcode
from qrcode.image.pil import PilImage

import db

BASE_URL = "https://event.bymyway.com/e/"
CHECKIN_URL = "https://event.bymyway.com/checkin"
CHECKIN_TITLE = "大樹小講系列講座 數位簽到系統"
CHECKIN_GIFT_NOTE = "🎁 集滿 5 次活動場次，還會送神秘禮物！"
QR_DIR = os.path.join(os.path.dirname(__file__), "qr")

PRINT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{title}｜報到QR立牌</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@700;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  @page {{ size:A4 portrait; margin:0; }}
  body {{
    font-family:'Noto Sans TC', sans-serif; background:#0a0a0a; color:#fff;
    width:210mm; height:297mm; margin:0 auto; padding:0 15mm; display:flex; flex-direction:column;
    align-items:center; justify-content:center; text-align:center; gap:10mm;
  }}
  .eyebrow {{ color:#c8a96e; font-size:24px; font-weight:700; letter-spacing:8px; }}
  h1 {{ font-size:44px; font-weight:900; line-height:1.35; }}
  .date {{ color:#c8a96e; font-size:30px; font-weight:900; }}
  .qrbox {{ background:#fff; padding:10mm; border-radius:8mm; }}
  .qrbox img {{ width:100mm; height:100mm; display:block; }}
  .cta {{ font-size:34px; font-weight:900; line-height:1.6; }}
  .cta span {{ color:#c8a96e; }}
  .sub {{ font-size:22px; color:rgba(255,255,255,.75); font-weight:700; }}
  .gift {{ font-size:24px; font-weight:900; color:#c8a96e; background:rgba(200,169,110,.12);
    border:1px solid rgba(200,169,110,.4); border-radius:10px; padding:12px 20px; }}
</style>
</head>
<body>
  <div class="eyebrow">歡迎蒞臨</div>
  <h1>{name_html}</h1>
  {date_html}
  {gift_html}
  <div class="qrbox"><img src="{slug}.png" alt="報到QR"></div>
  <div class="cta">手機掃描 <span>30 秒完成報到</span></div>
  <div class="sub">留下資料，下次活動第一時間通知您</div>
</body>
</html>
"""


def _write(slug: str, url: str, title: str, name_html: str, date_html: str, gift_html: str = "") -> None:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")

    os.makedirs(QR_DIR, exist_ok=True)
    png_path = os.path.join(QR_DIR, f"{slug}.png")
    img.save(png_path)

    html_path = os.path.join(QR_DIR, f"{slug}-print.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(PRINT_TEMPLATE.format(
            title=title, name_html=name_html, date_html=date_html, slug=slug, gift_html=gift_html,
        ))

    print(f"QR內容: {url}")
    print(f"PNG: {png_path}")
    print(f"立牌頁: {html_path}")


def make_checkin() -> None:
    """固定簽到QR：標題永遠寫死，網址永遠是/checkin，印一次永久用，
    後台/admin切換「目前活動」即可換到不同場次，不用重印。
    教練指定三行依序顯示（標題兩行+集點文案一行），QR圖在後面。"""
    name_html = "大樹小講系列講座<br>數位簽到系統"
    gift_html = f'<div class="gift">{CHECKIN_GIFT_NOTE}</div>'
    _write("checkin", CHECKIN_URL, CHECKIN_TITLE, name_html, "", gift_html)


def make_event(slug: str) -> None:
    conn = db.get_conn()
    event = db.get_event(conn, slug)
    conn.close()
    if not event:
        print(f"找不到活動：{slug}（先在資料庫建立這場活動）")
        sys.exit(1)

    date_html = f'<div class="date">{event["event_date"]}</div>' if event["event_date"] else ""
    _write(slug, BASE_URL + slug, event["name"], event["name"], date_html)


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--checkin":
        make_checkin()
    elif arg:
        make_event(arg)
    else:
        print("用法：make_qr.py <slug> 或 make_qr.py --checkin")
        sys.exit(1)


if __name__ == "__main__":
    main()
