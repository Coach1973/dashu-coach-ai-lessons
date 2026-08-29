"""
產生活動QR code。跑法：
  venv/bin/python3 make_qr.py <slug>     單一活動的QR（掃了直接進那場報名頁，網址含slug）
  venv/bin/python3 make_qr.py --checkin  固定簽到QR（掃了永遠導向後台設定的「目前活動」，
                                          網址不含slug，一勞永逸不用重印，後台切換場次見/admin）
  venv/bin/python3 make_qr.py --wheel    掃碼玩抽獎立牌（2026-08-09教練指示，跟--checkin同一個
                                          後端網址，只是不押日期、文案改「掃QRCODE玩抽獎」，
                                          往後每場活動都用這張取代--checkin立牌）
  venv/bin/python3 make_qr.py --slides   簡報QR（掃了進/slides頁：加LINE好友+下載今日簡報，
                                          網址固定不用重印，後台上傳/切換今日簡報見/admin）
  venv/bin/python3 make_qr.py --ganjing  乾淨世界頻道關注QR（2026-08-29教練指示，導去外部
                                          頻道連結，跟event.db活動場次無關，純推廣用）
輸出：qr/<slug 或 checkin 或 wheel 或 slides-drop 或 ganjing>.png（高解析，印刷可用）+ 對應 -print.html（A4立牌頁）
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
SLIDES_URL = "https://event.bymyway.com/slides"
SLIDES_TITLE = "簡報下載＋加好友"
GANJING_URL = "https://www.ganjingworld.com/s/3EBAgQObRg"
GANJING_TITLE = "大樹教練．乾淨世界頻道"
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
  <div class="eyebrow">{eyebrow}</div>
  <h1>{name_html}</h1>
  {date_html}
  {gift_html}
  <div class="qrbox"><img src="{slug}.png" alt="{alt_text}"></div>
  <div class="cta">{cta_html}</div>
  <div class="sub">{sub_text}</div>
</body>
</html>
"""


def _write(
    slug: str, url: str, title: str, name_html: str, date_html: str, gift_html: str = "",
    eyebrow: str = "歡迎蒞臨", cta_html: str = '手機掃描 <span>30 秒完成報到</span>',
    sub_text: str = "留下資料，下次活動第一時間通知您", alt_text: str = "報到QR",
) -> None:
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
            eyebrow=eyebrow, cta_html=cta_html, sub_text=sub_text, alt_text=alt_text,
        ))

    print(f"QR內容: {url}")
    print(f"PNG: {png_path}")
    print(f"立牌頁: {html_path}")


def make_checkin(event_label: str = "") -> None:
    """固定簽到QR：印一次永久用。2026-07-28教練指出來賓報名網站時已留過姓名/電話，
    現場只需要再輸入手機號碼比對身份即可，不用整份表單重填一次——網址維持CHECKIN_URL，
    /checkin這個route本身已改成「只問手機號碼」的簡化簽到頁（比對成功記進signups表供集點）。
    event_label：選填，這次現場活動的名稱（例如「AI微型論壇」），印在「歡迎蒞臨」標題正下方、
    醒目金色大字，讓來賓一眼看出這是哪一場，不用每次重新設計版型。"""
    name_html = "大樹小講系列講座<br>數位簽到系統"
    label_html = f'<div class="date">{event_label}</div>' if event_label else ""
    _write(
        "checkin", CHECKIN_URL, CHECKIN_TITLE, name_html, label_html,
        gift_html=f'<div class="gift">{CHECKIN_GIFT_NOTE}</div>',
    )


def make_wheel() -> None:
    """通用「掃碼玩抽獎」立牌：2026-08-09教練指示，不押特定場次日期，往後每場活動
    都用這張立牌取代原本的checkin立牌。網址、後端流程跟--checkin完全相同（掃了進
    /checkin輸入手機號碼比對報名資料，比對成功即完成報到並自動列入現場抽獎轉盤名單），
    只是把文案從「數位簽到」改包裝成「掃碼玩抽獎」，讓來賓更有參與抽獎的動機去掃碼。
    後台看得到每筆簽到記錄對應到哪一場（依日期自動判斷目前活動），不受這張立牌影響。"""
    name_html = "掃 QRCODE<br>玩抽獎"
    _write(
        "wheel", CHECKIN_URL, "掃碼玩抽獎", name_html, "",
        gift_html=f'<div class="gift">{CHECKIN_GIFT_NOTE}</div>',
        cta_html='手機掃描 <span>立即報到＋抽獎資格</span>',
        sub_text="掃碼完成報到，直接列入現場抽獎名單", alt_text="掃碼玩抽獎QR",
    )


def make_slides() -> None:
    """簡報QR：固定網址/slides，印一次永久用。每次上台前只要去/admin上傳今天的簡報檔
    （檔名開頭寫今天日期，例如2026-07-16-AI微型論壇.pdf），系統自動比對，不用重印QR。"""
    name_html = "掃碼加入好友<br>領取今日簡報"
    _write(
        "slides-drop", SLIDES_URL, SLIDES_TITLE, name_html, "",
        eyebrow="感謝聆聽", cta_html='手機掃描 <span>加好友領簡報</span>',
        sub_text="今日簡報檔即刻下載，未來活動也會通知您", alt_text="簡報下載QR",
    )


def make_ganjing() -> None:
    """乾淨世界頻道關注QR：固定網址，印一次永久用。跟活動簽到/抽獎無關，純粹導流
    到大樹教練的乾淨世界頻道，主打「300集免費影片」的內容量，不提集點送禮（教練
    2026-08-29指示不寫任何集點文字）。"""
    name_html = "大樹教練<br>乾淨世界頻道"
    _write(
        "ganjing", GANJING_URL, GANJING_TITLE, name_html, "",
        eyebrow="立即關注", cta_html='高品質自我成長影片<br><span>300 集</span>免費觀看',
        sub_text="手機掃描 QRCode 馬上開始收看", alt_text="關注乾淨世界頻道QR",
    )


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
    elif arg == "--wheel":
        make_wheel()
    elif arg == "--slides":
        make_slides()
    elif arg == "--ganjing":
        make_ganjing()
    elif arg:
        make_event(arg)
    else:
        print("用法：make_qr.py <slug> 或 make_qr.py --checkin 或 make_qr.py --wheel 或 make_qr.py --slides 或 make_qr.py --ganjing")
        sys.exit(1)


if __name__ == "__main__":
    main()
