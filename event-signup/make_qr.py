"""
產生活動QR code。跑法：venv/bin/python3 make_qr.py <slug>
輸出：qr/<slug>.png（高解析，印刷可用）+ qr/<slug>-print.html（A4立牌頁）
"""
import os
import sys

import qrcode
from qrcode.image.pil import PilImage

import db

BASE_URL = "https://event.bymyway.com/e/"
QR_DIR = os.path.join(os.path.dirname(__file__), "qr")

PRINT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{name}｜報到QR立牌</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@700;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  @page {{ size:A4 portrait; margin:0; }}
  body {{
    font-family:'Noto Sans TC', sans-serif; background:#0a0a0a; color:#fff;
    width:210mm; height:297mm; margin:0 auto; display:flex; flex-direction:column;
    align-items:center; justify-content:center; text-align:center; gap:10mm;
  }}
  .eyebrow {{ color:#c8a96e; font-size:24px; font-weight:700; letter-spacing:8px; }}
  h1 {{ font-size:52px; font-weight:900; line-height:1.3; }}
  .date {{ color:#c8a96e; font-size:30px; font-weight:900; }}
  .qrbox {{ background:#fff; padding:10mm; border-radius:8mm; }}
  .qrbox img {{ width:100mm; height:100mm; display:block; }}
  .cta {{ font-size:34px; font-weight:900; line-height:1.6; }}
  .cta span {{ color:#c8a96e; }}
  .sub {{ font-size:22px; color:rgba(255,255,255,.75); font-weight:700; }}
</style>
</head>
<body>
  <div class="eyebrow">歡迎蒞臨</div>
  <h1>{name}</h1>
  <div class="date">{date}</div>
  <div class="qrbox"><img src="{slug}.png" alt="報到QR"></div>
  <div class="cta">手機掃描 <span>30 秒完成報到</span></div>
  <div class="sub">留下資料，下次活動第一時間通知您</div>
</body>
</html>
"""


def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else ""
    conn = db.get_conn()
    event = db.get_event(conn, slug)
    conn.close()
    if not event:
        print(f"找不到活動：{slug}（先在資料庫建立這場活動）")
        sys.exit(1)

    url = BASE_URL + slug
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img: PilImage = qr.make_image(fill_color="black", back_color="white")

    os.makedirs(QR_DIR, exist_ok=True)
    png_path = os.path.join(QR_DIR, f"{slug}.png")
    img.save(png_path)

    html_path = os.path.join(QR_DIR, f"{slug}-print.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(PRINT_TEMPLATE.format(name=event["name"], date=event["event_date"] or "", slug=slug))

    print(f"QR內容: {url}")
    print(f"PNG: {png_path}")
    print(f"立牌頁: {html_path}")


if __name__ == "__main__":
    main()
