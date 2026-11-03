"""南應大校友會台南分會：理監事團隊與顧問團隊（2026-10-14 教練交辦）

比照 BNI 分會頁（github_repos/bni-chapters 的 /<slug>/join）同一套機制：
按「我要建立檔案」→ 填姓名、公司等資料 → 送出立刻上架（不經審核）→ 拿到一條專屬修改連結，
之後自己改、自己刪。顧問名單（記憶牆「專屬商務團隊資源」那 17 位）先放好空座位，
本人點自己的名字就能補上照片與簡介（誠信原則，比照 BNI 認座位）。

網址：
  /tut/team                      公開頁（理監事團隊＋顧問團隊）
  /tut/team/join                 我要建立檔案（名單上有名字的先點名字）
  /tut/team/claim/<id>    POST   認領顧問空座位 → 轉到自己的修改頁
  /tut/team/edit/<token>         本人專屬修改連結（含刪除）
  /tut/team/photo/<檔名>          照片
  /tut/team/a/<code>             管理後台（簽章短址，已收進大樹作品集）：隱藏／刪除／新增空座位
色系：南應大官網主色紫 #854D92（2026-10-14 從 tut.edu.tw 網站樣式表與校徽實際取色）。
"""
import hashlib
import hmac
import html
import os
import re
import secrets
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

import db

UPLOAD_DIR = Path(__file__).resolve().parent / "tut_team_uploads"
MAX_UPLOAD = 12_000_000
MAX_EDGE = 900
PHOTO_RE = re.compile(r"^[0-9a-f]{16}\.jpg$")
TEAMS = {"board": "理監事團隊", "advisor": "顧問團隊"}
# 職務排序：先比對到的排前面；沒列到的職務排在同團隊最後
ROLE_ORDER = ["榮譽理事長", "理事長", "副理事長", "常務理事", "理事", "常務監事", "監事召集人", "監事",
              "秘書長", "總幹事", "執行長", "總顧問", "首席顧問", "榮譽顧問", "顧問"]
LINKS = [("link_web", "網站"), ("link_fb", "Facebook"), ("link_ig", "Instagram"), ("link_line", "LINE")]
FIELDS = ["team", "role", "name", "company_title", "dept_year", "bio"] + [k for k, _ in LINKS]
LIMITS = {"role": 20, "name": 30, "company_title": 60, "dept_year": 40, "bio": 800,
          "link_web": 300, "link_fb": 300, "link_ig": 300, "link_line": 300}

# 記憶牆「專屬商務團隊資源」名單（github_repos/tut-memory/index.html 的 BIZ_TEAM，2026-10-14 抄錄）
ADVISOR_SEATS = [
    ("林士民", "台南文創協會", ""), ("林家旭", "台灣形象設計發展協會", ""),
    ("李中閔", "網紅部落客聯盟協會理事", ""),
    ("鄭儷絲", "中華網紅協會理事長", "https://event.bymyway.com/cica/"),
    ("劉雅萍", "台南市台灣世界旗袍文化推展聯合會理事長", ""),
    ("陳彥玲", "全球健康發展協會", "https://northern-tw.netlify.app/"),
    ("施正益", "彰化縣網路購物服務人員職業工會理事長", ""),
    ("謝志賓", "新媒體影音發展協會", "https://event.bymyway.com/curated/nmda/"),
    ("陳美芬", "職能發展協會理事長", ""),
    ("林丁禾", "藝術商務顧問", "https://event.bymyway.com/curated/art-lab/"),
    ("吳日勤", "東倫敦大學藝術博士", ""),
    ("李瑞惠", "有限責任台灣區綠能作物運銷合作社", ""),
    ("楊仟慧", "國際同濟會台灣總會金駝分會藝術總監", ""),
    ("阿樂老師", "可成音樂文化有限公司", ""),
    ("江睿翔", "山田聯誼會51屆秘書長", ""),
    ("林志和", "智匯保經一處副總", ""),
]

# 理監事校友名單（2026-10-23 教練 02:00 貼的 23 位，順序照貼）。第一次用到時放成空座位，
# 照片、職稱、簡介、連結之後補在資料庫；記憶牆（tut-memory）的「理監事校友名單」讀 /api/tut/team/board，兩邊同一份。
BOARD_SEATS = ["王佩茹", "楊孟薰", "陳佩君", "謝念均", "許山本美道子", "王佑文", "劉上維", "邱鈺涵",
               "林泓丞", "曾智美", "陳沛岺", "潘皓瑋", "何冠忻", "林惠雯", "彭韻錚", "邱錦秀",
               "顏妙青", "金巧玲", "陳孟珩", "楊志芳", "吳泰良", "郭怡淳", "孫熙閑"]

# 有網頁連結的顧問：本人補資料前，先放從網頁整理的介紹（2026-10-14 教練：至少先看得到對方的網頁簡介）。
# 只寫網頁上看得到的內容；網頁沒提到本人的（謝志賓），只介紹協會、不替本人寫頭銜。
SEAT_SOURCE_NOTE = "\n\n（以上整理自公開網頁，待本人補充）"
SEAT_INTROS = {
    "鄭儷絲": "中華網紅協會（CICA）創會理事長暨永續長。協會於 2020 年 11 月 1 日立案，是全國性非營利人民團體，"
             "主張「網紅是一個產業」，攜手臺北網紅節與 TY Star 臺北網紅獎，也推動培養身障網紅與銀髮網紅、扶助弱勢直播主。"
             "本人擁有十餘年主持、採訪、活動企劃與製作經驗，曾任東森 ET FM 節目製作人暨主持人、"
             "正聲廣播與中國廣播公司節目主持人，也是直播培訓講師與公益主持人。",
    "陳彥玲": "陳彥玲博士，紐約北方醫學中心國際合作處處長。全球健康發展協會與紐約北方醫學教育基金會合作推廣四維醫學，"
             "2026 年 6 月 26 日在國立中正大學舉辦「智匯健康｜腦力長青」失智防治與逆齡醫學跨界論壇"
             "（嘉義縣衛生局指導，國立中正大學中小企業育成中心、全球健康發展協會、紐約北方醫學中心共同推動），"
             "陳彥玲博士為論壇致詞貴賓。",
    "謝志賓": "協會介紹：中華新媒體影音發展協會於 2026 年 6 月 29 日立案，推動新媒體人才培育、產業孵化與跨界共創，"
             "串聯影音製作、AI 短影音、直播與商業資源，協助中小企業建立新媒體能力；"
             "2026 年 10 月 31 日在台中舉辦協會啟動大會。",
    # 林丁禾、江睿翔：用本人在 AI 百人導師（mentor100.bymyway.com）自己填的簡介（2026-10-14 教練：照片也從百人導師移植）
    "林丁禾": "林丁禾藝術孵化實驗室 創辦人（藝術孵化＆課程）。1978 年出生於高雄，政治大學商學院科技與創新管理研究所、"
             "台灣藝術大學美術學院雕塑學系畢業。2018 年起為正觀藝術畫廊藝術顧問，同時是高雄市女青年會對外招生藝術課程老師，"
             "以及六城市 EMBA 心靈領袖讀書會企業講師與聯席主持人。2020 年創立藝術孵化實驗室，持續以「藝術入世」的角度，"
             "積極成為「商業藝術」與「社會雕塑」的實踐者，經常在跨界的不同領域舉行藝術講座與創作實踐，"
             "推動以人為本的自我實現，同時創造社會價值。",
    "江睿翔": "睿翔AI應用工作室，AI 應用教學講師。專長 AI 應用教學，並協助企業 ESG 永續經營、輔導政府部門補助案。",
    # 以下兩位整理自「為你轉身」導師席（event.bymyway.com/curated/turnforyou/，2026-10-14 教練：有資料就先移植）
    "李中閔": "宸霖智權科技集團業務經理、中華媒體交流協會總幹事。專長社區型政府補助申請，對協會的成立與運作經驗豐富；"
             "也擔任社團法人高雄市職能發展協會常務理事、國際獅子會 300E3 區雄大獅子會資訊長、高雄市見真際同濟會創會秘書長、"
             "高雄市幸運草歌藝共好協進會總幹事，並任台灣小姐選拔大會南區執行長、2026 世界美顏小姐籌委會執行總監、"
             "總成國際整合行銷公司副總。",
    # 正確名字是「施正益」（教練 2026-10-14 確認；記憶牆原本寫錯一個字，已一起更正）
    "施正益": "彰化縣網路購物服務人員職業工會理事長、時間旅人文創創辦人。從事網路行銷與顧問二十六年，擔任 TTQS 網路行銷課程講師；"
             "是 Google 地圖第 10 級在地嚮導（Google 地圖社群貢獻的最高等級），發展「地圖關鍵字行銷」與在地嚮導團隊，"
             "協助店家做地圖優化、360 度環景照片與影片拍攝。",
}
NAME_FIXES = {"施" + "正義": "施正益"}   # 2026-10-14 教練確認的正確寫法（舊座位自動改名）
TURNFORYOU = "https://event.bymyway.com/curated/turnforyou/"
SEAT_LINKS = {
    "李中閔": {"link_web": TURNFORYOU}, "施正益": {"link_web": TURNFORYOU},
    "林丁禾": {"link_fb": "https://www.facebook.com/dinghe.lin", "link_ig": "https://www.instagram.com/star119832003/"},
    "江睿翔": {"link_fb": "https://www.facebook.com/mickjay1201"},
}
_TFY_IMG = Path.home() / "github_repos" / "turnforyou" / "img" / "mentors"
_M100_IMG = Path.home() / "github_repos" / "mentor100" / "static" / "uploads"
SEAT_PHOTOS = {"李中閔": _TFY_IMG / "li-zhongmin.jpg", "施正益": _TFY_IMG / "shi-zhengyi.jpg",
               "林丁禾": _M100_IMG / "unnamed-939916e2.jpg",
               "江睿翔": _M100_IMG / "85806E99-0013-4845-9FFB-770A52874B71-ca08edce.jpg",
               "林士民": _M100_IMG / "專業灰背景企業肖像-a012e03a.jpg"}

E = html.escape


# ---------- 資料 ----------
def _conn():
    conn = db.get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS tut_team_members ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT, team TEXT NOT NULL, role TEXT NOT NULL DEFAULT '',"
        " name TEXT NOT NULL, company_title TEXT NOT NULL DEFAULT '', dept_year TEXT NOT NULL DEFAULT '',"
        " bio TEXT NOT NULL DEFAULT '', photo_file TEXT, link_web TEXT NOT NULL DEFAULT '',"
        " link_fb TEXT NOT NULL DEFAULT '', link_ig TEXT NOT NULL DEFAULT '', link_line TEXT NOT NULL DEFAULT '',"
        " edit_token TEXT NOT NULL UNIQUE, filled INTEGER NOT NULL DEFAULT 1, hidden INTEGER NOT NULL DEFAULT 0,"
        " sort INTEGER NOT NULL DEFAULT 999, ip TEXT,"
        " created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),"
        " updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime')))"
    )
    return conn


def seed_advisor_seats():
    """第一次用到時放好顧問與理監事空座位；各團隊已經有任何資料就不再動（不會重複、不會蓋掉本人填的）。"""
    conn = _conn()
    if not conn.execute("SELECT 1 FROM tut_team_members WHERE team='board' LIMIT 1").fetchone():
        for i, name in enumerate(BOARD_SEATS):
            conn.execute("INSERT INTO tut_team_members (team, role, name, edit_token, filled, sort)"
                         " VALUES ('board', '', ?, ?, 0, ?)", (name, secrets.token_urlsafe(16), i))
        conn.commit()
    if not conn.execute("SELECT 1 FROM tut_team_members WHERE team='advisor' LIMIT 1").fetchone():
        for i, (name, title, url) in enumerate(ADVISOR_SEATS):
            conn.execute("INSERT INTO tut_team_members (team, role, name, company_title, link_web, edit_token, filled, sort)"
                         " VALUES ('advisor', '顧問', ?, ?, ?, ?, 0, ?)", (name, title, url, secrets.token_urlsafe(16), i))
        conn.commit()
    for wrong, right in NAME_FIXES.items():
        conn.execute("UPDATE tut_team_members SET name=? WHERE team='advisor' AND name=?", (right, wrong))
    # 還沒補資料、簡介還空著的顧問座位，補上網頁整理的介紹（本人填過的不動）
    for name, intro in SEAT_INTROS.items():
        conn.execute("UPDATE tut_team_members SET bio=? WHERE team='advisor' AND name=? AND filled=0"
                     " AND (bio='' OR bio LIKE ?)", (intro + SEAT_SOURCE_NOTE, name, "%" + SEAT_SOURCE_NOTE.strip()))
    for name, links in SEAT_LINKS.items():
        for col, url in links.items():
            conn.execute(f"UPDATE tut_team_members SET {col}=? WHERE team='advisor' AND name=? AND filled=0 AND {col}=''",
                         (url, name))
    for name, src in SEAT_PHOTOS.items():
        row = conn.execute("SELECT id FROM tut_team_members WHERE team='advisor' AND name=? AND filled=0 AND photo_file IS NULL",
                           (name,)).fetchone()
        if row and src.is_file():
            fname = _save_image_bytes(src.read_bytes())
            if fname:
                conn.execute("UPDATE tut_team_members SET photo_file=? WHERE id=?", (fname, row["id"]))
    conn.commit()
    conn.close()


def _rank(r):
    role = r["role"] or ""
    idx = next((i for i, k in enumerate(ROLE_ORDER) if k in role), len(ROLE_ORDER))
    return (idx, r["sort"], r["id"])


def list_members(include_hidden=False):
    seed_advisor_seats()
    conn = _conn()
    rows = conn.execute("SELECT * FROM tut_team_members" + ("" if include_hidden else " WHERE hidden=0")).fetchall()
    conn.close()
    return sorted(rows, key=_rank)


def board_public(build=""):
    """記憶牆「理監事校友名單」用的資料：跟 /tut/team 同一份。一般訪客只有公開欄位（不含修改連結、IP）；
    build＝教練的建置模式簽章短碼，對了才多給每人的編輯網址。"""
    out = []
    for r in list_members():
        if r["team"] != "board":
            continue
        title = " ｜ ".join(x for x in (r["role"], r["company_title"]) if x)
        bio = "\n\n".join(x for x in ((f"🎓 {r['dept_year']}" if r["dept_year"] else ""), r["bio"]) if x)
        item = {"id": r["id"], "filled": bool(r["filled"]), "name": r["name"], "title": title, "bio": bio,
                "photo": f"https://event.bymyway.com/tut/team/photo/{r['photo_file']}" if r["photo_file"] else "",
                "links": [{"label": lab, "url": r[k]} for k, lab in LINKS if r[k]]}
        if build:
            item["edit"] = f"https://event.bymyway.com/tut/team/edit/{r['edit_token']}?build={build}"
        out.append(item)
    return out


def get_by_token(token):
    if not token or len(token) > 64:
        return None
    conn = _conn()
    r = conn.execute("SELECT * FROM tut_team_members WHERE edit_token=?", (token,)).fetchone()
    conn.close()
    return r


def get_by_id(mid):
    conn = _conn()
    r = conn.execute("SELECT * FROM tut_team_members WHERE id=?", (mid,)).fetchone()
    conn.close()
    return r


def open_seats():
    return [r for r in list_members() if not r["filled"]]


def _norm_link(key, v):
    v = v.strip()
    if not v:
        return ""
    if key == "link_line" and not re.match(r"^https?://", v, re.I):
        return "https://line.me/ti/p/~" + re.sub(r"[^\w.@-]", "", v.lstrip("@"))
    if not re.match(r"^https?://", v, re.I):
        v = "https://" + v
    return v if re.match(r"^https?://[^\s<>\"']+$", v) else ""


def clean_form(form, need_photo, partial=False):
    """回傳 (資料 dict, 錯誤訊息)。partial＝教練的建置模式，只要有團隊跟姓名就收，其他之後補。"""
    d = {}
    for k in FIELDS:
        v = (form.get(k) or "").strip()
        v = v[:LIMITS.get(k, 20)] if k == "bio" else re.sub(r"\s+", " ", v)[:LIMITS.get(k, 20)]
        d[k] = _norm_link(k, v) if k.startswith("link_") else v
    d["bio"] = d["bio"].replace(SEAT_SOURCE_NOTE.strip(), "").strip()   # 本人存檔＝已補充，拿掉「待本人補充」
    if d["team"] not in TEAMS:
        return d, "請選擇您是「理監事團隊」還是「顧問團隊」"
    if partial:
        return d, ("" if d["name"] else "請填寫「姓名」")
    for k, label in (("name", "姓名"), ("company_title", "公司／職稱"), ("bio", "個人簡介")):
        if not d[k]:
            return d, f"請填寫「{label}」"
    if need_photo:
        return d, "請上傳一張照片"
    return d, ""


def save_photo(file_storage):
    """驗證是真的圖片、轉正、縮圖存 jpg；回傳檔名，失敗回 None。"""
    return _save_image_bytes(file_storage.read(MAX_UPLOAD + 1))


def _save_image_bytes(data):
    if not data or len(data) > MAX_UPLOAD:
        return None
    try:
        img = Image.open(BytesIO(data))
        img.load()
    except (UnidentifiedImageError, OSError):
        return None
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    img.thumbnail((MAX_EDGE, MAX_EDGE))
    UPLOAD_DIR.mkdir(exist_ok=True)
    name = f"{os.urandom(8).hex()}.jpg"
    img.save(UPLOAD_DIR / name, "JPEG", quality=85)
    return name


def insert(d, photo_file, ip):
    token = secrets.token_urlsafe(16)
    conn = _conn()
    conn.execute(
        f"INSERT INTO tut_team_members ({', '.join(FIELDS)}, photo_file, edit_token, filled, ip)"
        f" VALUES ({', '.join('?' * len(FIELDS))}, ?, ?, 1, ?)",
        [d[k] for k in FIELDS] + [photo_file, token, ip])
    conn.commit()
    conn.close()
    return token


def update(mid, d, photo_file):
    conn = _conn()
    sets = ", ".join(f"{k}=?" for k in FIELDS)
    conn.execute(f"UPDATE tut_team_members SET {sets}, photo_file=COALESCE(?, photo_file), filled=1,"
                 " updated_at=datetime('now','localtime') WHERE id=?", [d[k] for k in FIELDS] + [photo_file, mid])
    conn.commit()
    conn.close()


def delete(mid):
    r = get_by_id(mid)
    conn = _conn()
    conn.execute("DELETE FROM tut_team_members WHERE id=?", (mid,))
    conn.commit()
    conn.close()
    if r and r["photo_file"] and PHOTO_RE.match(r["photo_file"]):
        (UPLOAD_DIR / r["photo_file"]).unlink(missing_ok=True)


def set_hidden(mid, hidden):
    conn = _conn()
    conn.execute("UPDATE tut_team_members SET hidden=? WHERE id=?", (1 if hidden else 0, mid))
    conn.commit()
    conn.close()


def add_seat(team, role, name, title):
    conn = _conn()
    conn.execute("INSERT INTO tut_team_members (team, role, name, company_title, edit_token, filled) VALUES (?,?,?,?,?,0)",
                 (team, role[:20], name[:30], title[:60], secrets.token_urlsafe(16)))
    conn.commit()
    conn.close()


# ---------- 簽章 ----------
def admin_code(secret):
    return hmac.new(secret.encode(), b"tut-team-admin", hashlib.sha256).hexdigest()[:12]


def admin_url(secret):
    return f"https://event.bymyway.com/tut/team/a/{admin_code(secret)}"


# ---------- 頁面 ----------
CSS = """
:root{--purple:#854D92;--purple-deep:#3D2B47;--purple-mid:#5B3A6B;--purple-soft:#EDE4F3;--bg:#F6F2F8;--card:#FFFFFF;
--line:#D4B8E0;--text:#2E2433;--muted:#6B6170;--gold:#B8862B;--danger:#A33A3A}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 20px/1.75 "Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif}
a{color:var(--purple)}h1,h2,h3{line-height:1.35;margin:0}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
.top{background:var(--purple-deep);color:#fff;font-size:20px}.top .wrap{display:flex;gap:16px;align-items:center;min-height:48px;flex-wrap:wrap}
.top a{color:#E9DDF0;text-decoration:none}.top b{color:#fff;margin-right:auto;letter-spacing:.06em}
.hero{background:linear-gradient(160deg,var(--purple-deep),var(--purple) 70%);color:#fff;padding:56px 0 64px}
.eyebrow{letter-spacing:.24em;font-size:20px;color:#E9DDF0;margin:0 0 10px}
.hero h1{font-size:clamp(30px,6vw,48px);font-weight:700}.hero p.lead{max-width:640px;color:#EFE7F4;margin:16px 0 28px}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 28px;border-radius:999px;border:0;
background:#fff;color:var(--purple-deep);font-family:inherit;font-weight:700;font-size:20px;line-height:1;text-decoration:none;cursor:pointer}
.btn.purple{background:var(--purple);color:#fff}.btn.ghost{background:none;border:1.5px solid var(--purple);color:var(--purple)}
.btn.danger{background:none;border:1.5px solid var(--danger);color:var(--danger);font-size:20px;min-height:44px}
.hero .count{margin-left:16px;color:#E9DDF0;font-size:20px}
section.team{padding:48px 0 8px}.team h2{font-size:clamp(24px,4vw,32px);color:var(--purple-deep);display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.team h2 small{font-size:20px;color:var(--muted);font-weight:400}.team .intro{color:var(--muted);margin:6px 0 22px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;display:flex;flex-direction:column}
.card .head{display:flex;gap:16px;align-items:center;margin-bottom:12px}
.ph{width:84px;height:84px;border-radius:50%;object-fit:cover;flex:none;border:3px solid var(--purple-soft);background:var(--purple-soft);
display:flex;align-items:center;justify-content:center;font:700 32px/1 "Noto Serif TC",serif;color:var(--purple);object-position:50% 18%}
.role{display:inline-block;font-size:20px;padding:1px 12px;border-radius:999px;background:var(--purple-soft);color:var(--purple-deep);margin-bottom:4px}
.card h3{font-size:22px}.ct{color:var(--muted);font-size:20px;margin:2px 0 0}
.bio{white-space:pre-line;margin:0;font-size:20px}
.bio-wrap summary{cursor:pointer;list-style:none}.bio-wrap summary::-webkit-details-marker{display:none}
.bio-wrap .short{display:block;color:var(--text)}.bio-wrap .more{display:block;color:var(--purple);font-size:20px;margin-top:4px}
.bio-wrap[open] .short{display:none}.bio-wrap[open] .more{font-size:0}.bio-wrap[open] .more::after{content:"收合";font-size:20px}
.links{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto;padding-top:14px}
.links a{font-size:20px;padding:4px 14px;border-radius:999px;border:1px solid var(--line);text-decoration:none}
.card.seat{border-style:dashed;background:transparent}.card.seat .ph{background:#fff}
.card.seat form{padding-top:12px}.card.seat .links{margin-top:auto}
.seat-btn{font-family:inherit;font-weight:500;font-size:20px;line-height:1;min-height:44px;padding:0 18px;border-radius:999px;border:1.5px solid var(--purple);background:none;color:var(--purple);cursor:pointer;width:100%}
.empty{border:1px dashed var(--line);border-radius:14px;padding:22px;color:var(--muted)}
.cta{margin:56px 0;padding:36px 24px;border-radius:18px;background:var(--purple-soft);text-align:center}
.cta h2{color:var(--purple-deep);font-size:clamp(22px,4vw,30px);margin-bottom:8px}.cta p{color:var(--muted);margin:0 0 20px}
footer{background:var(--purple-deep);color:#D9CCE0;font-size:20px;padding:28px 0}footer a{color:#fff}
/* 表單 */
.paper{background:#fff;border:1px solid var(--line);border-radius:16px;padding:clamp(20px,4vw,36px);margin:28px 0 56px}
.field{display:flex;flex-direction:column;margin-bottom:18px}label{font-weight:500;margin-bottom:6px}
.req{color:var(--purple)}.opt{color:var(--muted);font-weight:400;font-size:20px;margin-left:6px}
input[type=text],input[type=url],textarea{font:inherit;color:var(--text);border:1.5px solid var(--line);border-radius:10px;padding:10px 14px;min-height:50px;width:100%;background:#fff}
textarea{min-height:150px;resize:vertical}input:focus,textarea:focus{outline:none;border-color:var(--purple)}
.hint{color:var(--muted);font-size:20px;margin-top:4px}
.choices{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.choice{position:relative}.choice input{position:absolute;opacity:0}
.choice span{display:flex;align-items:center;justify-content:center;min-height:56px;border:1.5px solid var(--line);border-radius:12px;font-weight:500;cursor:pointer;text-align:center;padding:6px}
.choice input:checked+span{border-color:var(--purple);background:var(--purple-soft);color:var(--purple-deep)}
.choice input:focus-visible+span{outline:3px solid var(--purple);outline-offset:2px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:0 16px}
.err{background:#FBEDED;color:var(--danger);border-radius:10px;padding:12px 16px;margin-bottom:18px}
.ok{background:#EEF6EE;color:#2F6B34;border-radius:10px;padding:12px 16px;margin-bottom:18px}
.claim{background:var(--purple-soft);border-radius:14px;padding:18px 20px;margin:24px 0}
.claim p{margin:0 0 10px}.chips{display:flex;flex-wrap:wrap;gap:8px}.chips form{margin:0}
.chips button{font:inherit;font-size:20px;min-height:42px;padding:0 16px;border-radius:999px;border:1px solid var(--purple);background:#fff;color:var(--purple-deep);cursor:pointer}
.cur{display:flex;gap:12px;align-items:center;margin-bottom:8px}.cur img{width:64px;height:64px;border-radius:50%;object-fit:cover}
.copy{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 20px}.copy input{flex:1;min-width:220px;font:inherit;font-size:20px;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px}
table{width:100%;border-collapse:collapse;font-size:20px}td,th{text-align:left;padding:10px 6px;border-bottom:1px solid var(--line);vertical-align:top}
td form{display:inline}td button{font:inherit;font-size:20px;padding:4px 10px;border-radius:8px;border:1px solid var(--line);background:#fff;cursor:pointer}
@media(max-width:640px){.two{grid-template-columns:1fr}.hero{padding:40px 0 48px}.hero .count{display:block;margin:12px 0 0}}
.editbtn{background:var(--purple);color:#fff !important;font-weight:700}
"""

TITLE = "南應大校友會台南分會"


def _page(title, body, robots=True):
    return f"""<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{'' if robots else '<meta name="robots" content="noindex,nofollow">'}
<title>{E(title)}</title><meta name="theme-color" content="#3D2B47"><style>{CSS}</style></head><body>
<div class="top"><div class="wrap"><b>{TITLE}</b><a href="/tut/team">理監事與顧問</a><a href="/tut/">校友會召集令</a><a href="/curated/tut-memory/">回憶牆</a></div></div>
{body}
<footer><div class="wrap">台南應用科技大學校友會台南分會｜資料由本人自行填寫與維護｜<a href="/tut/">加入校友會</a></div></footer>
</body></html>"""


def _photo(r, cls="ph"):
    if r["photo_file"]:
        return f'<img class="{cls}" src="/tut/team/photo/{E(r["photo_file"])}" alt="{E(r["name"])}" loading="lazy">'
    return f'<span class="{cls}" aria-hidden="true">{E((r["name"] or "?")[:1])}</span>'


def _bio_html(bio):
    """長簡介先露前 150 字，其餘收進「看完整介紹」。"""
    if len(bio) <= 160:
        return f'<p class="bio">{E(bio)}</p>'
    return (f'<details class="bio-wrap"><summary><span class="short bio">{E(bio[:150])}…</span>'
            f'<span class="more">看完整介紹</span></summary><p class="bio">{E(bio)}</p></details>')


def _card(r, build=""):
    edit = (f'<div class="links"><a class="editbtn" href="/tut/team/edit/{E(r["edit_token"])}?build={E(build)}">'
            f'✏️ 編輯（上傳照片／簡介）</a></div>' if build else "")
    links = "".join(f'<a href="{E(r[k])}" target="_blank" rel="noopener nofollow">{lab}</a>' for k, lab in LINKS if r[k])
    role = f'<span class="role">{E(r["role"])}</span>' if r["role"] else ""
    dept = f'<p class="ct">🎓 {E(r["dept_year"])}</p>' if r["dept_year"] else ""
    bio = r["bio"] or ""
    if not r["filled"]:
        intro = _bio_html(bio) if bio else '<p class="ct">簡介準備中</p>'
        seat_links = "".join(f'<a href="{E(r[k])}" target="_blank" rel="noopener nofollow">看{lab if k != "link_web" else "網頁介紹"} ›</a>'
                             for k, lab in LINKS if r[k])
        return (f'<div class="card seat"><div class="head">{_photo(r)}<div>{role}<h3>{E(r["name"])}</h3>'
                f'<p class="ct">{E(r["company_title"])}</p></div></div>{intro}'
                f'{f"<div class=links>{seat_links}</div>" if seat_links else ""}'
                f'{edit or f"""<form method="post" action="/tut/team/claim/{r["id"]}"><button class="seat-btn">我是{E(r["name"])}，補上我的簡介</button></form>"""}</div>')
    bio_html = _bio_html(bio)
    return (f'<article class="card"><div class="head">{_photo(r)}<div>{role}<h3>{E(r["name"])}</h3>'
            f'<p class="ct">{E(r["company_title"])}</p>{dept}</div></div>{bio_html}'
            f'{f"<div class=links>{links}</div>" if links else ""}{edit}</article>')


def render_index(build=""):
    rows = list_members()
    board = [r for r in rows if r["team"] == "board"]
    adv = [r for r in rows if r["team"] == "advisor"]
    filled = sum(1 for r in rows if r["filled"])

    def sec(key, items, intro, empty):
        n = sum(1 for r in items if r["filled"])
        grid = f'<div class="grid">{"".join(_card(r, build) for r in items)}</div>' if items else f'<p class="empty">{empty}</p>'
        return (f'<section class="team" id="{key}"><div class="wrap"><h2>{TEAMS[key]}<small>已上架 {n} 位</small></h2>'
                f'<p class="intro">{intro}</p>{grid}</div></section>')

    build_note = ('<p class="lead" style="background:#fff3cd;color:#3D2B47;padding:10px 14px;border-radius:8px">'
                  '🛠 建置模式（只有您看得到）：每張卡片都有「✏️ 編輯」，可以上傳照片、補職稱和簡介，也可以只補其中一項。</p>'
                  if build else "")
    body = f"""<header class="hero"><div class="wrap">
<p class="eyebrow">TAINAN UNIVERSITY OF TECHNOLOGY ALUMNI</p>
<h1>{TITLE}<br>理監事團隊與顧問團隊</h1>
<p class="lead">把校友的經驗與資源串在一起。點開每一位，認識為南應人服務的理監事與顧問；您也在團隊裡嗎？按下面的按鈕，自己建立檔案，送出就上架。</p>
{build_note}<a class="btn" href="/tut/team/join">我要建立檔案</a><span class="count">目前 {filled} 位已上架</span>
</div></header>
{sec("board", board, "校友會的理事、監事與幹部。名單上已有您的名字？點您那一張的按鈕，補上照片與簡介就上架。", "理監事名單確定後，請理監事本人按「我要建立檔案」，選「理監事團隊」填寫，送出就會出現在這裡。")}
{sec("advisor", adv, "為校友提供產業、商務與專業資源的顧問夥伴。名單上已有您的名字？點您那一張的按鈕，補上照片與簡介就上架。", "顧問名單整理中。")}
<div class="wrap"><div class="cta"><h2>您也是理監事或顧問？</h2><p>填姓名、公司、簡介，附一張照片，3 分鐘完成，送出立刻上架。</p>
<a class="btn purple" href="/tut/team/join">我要建立檔案</a></div></div>"""
    return _page(f"{TITLE}｜理監事團隊與顧問團隊", body)


def _form_html(action, d, error, existing=None, seats=(), build=""):
    d = d or {}
    rq = "" if build else "required"   # 建置模式：職稱、簡介、照片都不必填
    v = lambda k: E(d.get(k, "") or "")  # noqa: E731
    team = d.get("team", "")
    choices = "".join(
        f'<label class="choice"><input type="radio" name="team" value="{k}" {"checked" if team == k else ""} required><span>{lab}</span></label>'
        for k, lab in TEAMS.items())
    photo_req = not (existing and existing["photo_file"]) and not build
    cur = (f'<div class="cur">{_photo(existing)}<span class="hint">目前的照片；不換就不用再上傳</span></div>'
           if existing and existing["photo_file"] else "")
    claim = ""
    if seats:
        groups = ""
        for key, lab in TEAMS.items():
            part = "".join(f'<form method="post" action="/tut/team/claim/{s["id"]}"><button>{E(s["name"])}</button></form>'
                           for s in seats if s["team"] == key)
            if part:
                groups += f'<p class="hint" style="margin:10px 0 4px">{lab}</p><div class="chips">{part}</div>'
        claim = (f'<div class="claim"><p><b>名單上已經有您的名字？</b>直接點您的名字，補上照片與簡介即可，不用重新填。</p>'
                 f'{groups}</div>')
    links = "".join(
        f'<div class="field"><label for="{k}">{lab}<span class="opt">選填</span></label>'
        f'<input type="text" id="{k}" name="{k}" value="{v(k)}" placeholder="{"LINE ID 或加好友網址" if k == "link_line" else "https://"}"></div>'
        for k, lab in LINKS)
    return f"""{claim}<form class="paper" method="post" action="{action}" enctype="multipart/form-data">
{f'<p class="err" role="alert">{E(error)}</p>' if error else ''}
<div class="field"><label>您是哪一個團隊<span class="req"> *</span></label><div class="choices">{choices}</div></div>
<div class="two">
<div class="field"><label for="name">姓名<span class="req"> *</span></label><input type="text" id="name" name="name" value="{v('name')}" required maxlength="30" autocomplete="name"></div>
<div class="field"><label for="role">校友會職務<span class="opt">選填</span></label><input type="text" id="role" name="role" value="{v('role')}" maxlength="20" placeholder="例：理事長、常務理事、監事、顧問"></div>
</div>
<div class="field"><label for="company_title">公司／職稱<span class="req"> *</span></label><input type="text" id="company_title" name="company_title" value="{v('company_title')}" {rq} maxlength="60" placeholder="例：大樹教育 創辦人"></div>
<div class="field"><label for="dept_year">南應大科系與畢業年<span class="opt">選填</span></label><input type="text" id="dept_year" name="dept_year" value="{v('dept_year')}" maxlength="40" placeholder="例：企管系 1998 年畢業"></div>
<div class="field"><label for="bio">個人簡介<span class="req"> *</span></label><textarea id="bio" name="bio" {rq} maxlength="800" placeholder="您的專長、經歷，以及能為校友提供的資源（800 字內）">{v('bio')}</textarea></div>
<div class="field"><label for="photo">個人照片{'<span class="req"> *</span>' if photo_req else '<span class="opt">選填</span>'}</label>{cur}
<input type="file" id="photo" name="photo" accept="image/*" {"required" if photo_req else ""}><p class="hint">清楚的半身照最好，手機照片直接傳即可</p></div>
<div class="two">{links}</div>
<input type="text" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<button class="btn purple" type="submit">{'儲存修改' if existing else '送出並上架'}</button>
</form>"""


def render_join(d=None, error=""):
    body = f"""<div class="wrap" style="max-width:760px;padding-top:36px">
<p class="eyebrow" style="color:var(--purple)">我要建立檔案</p><h1 style="color:var(--purple-deep)">建立您的校友會團隊檔案</h1>
<p style="color:var(--muted)">送出後立刻出現在「理監事團隊與顧問團隊」頁面，並給您一條專屬修改連結，之後隨時可以自己修改。</p>
{_form_html("/tut/team/join", d, error, seats=open_seats())}</div>"""
    return _page("我要建立檔案｜" + TITLE, body, robots=False)


def render_edit(r, d=None, error="", saved=False, first=False, build=""):
    d = d or dict(r)
    url = f"https://event.bymyway.com/tut/team/edit/{r['edit_token']}"
    back = f"/tut/team?build={E(build)}#{r['team']}" if build else f"/tut/team#{r['team']}"
    bnote = ('<p class="ok" role="status">🛠 建置模式：照片、職稱、簡介可以只補其中一項，按「儲存修改」就更新。</p>' if build else "")
    note = ""
    if first:
        note = ('<p class="ok" role="status"><b>已上架！</b>這是您的專屬修改連結，請存起來（加入書籤或傳給自己 LINE），之後修改資料都用它：</p>'
                f'<div class="copy"><input id="me" value="{E(url)}" readonly><button class="btn purple" type="button" '
                f'onclick="navigator.clipboard.writeText(document.getElementById(\'me\').value).then(()=>this.textContent=\'已複製\')">複製連結</button>'
                f'<a class="btn ghost" href="{back}">看我的檔案</a></div>')
    elif saved:
        note = f'<p class="ok" role="status">已儲存，頁面已更新。<a href="{back}">回團隊頁看看</a></p>'
    elif not r["filled"]:
        note = '<p class="ok" role="status">您的名字已經在名單上了，補上照片與簡介，按「儲存修改」就會上架。</p>'
    body = f"""<div class="wrap" style="max-width:760px;padding-top:36px">
<p class="eyebrow" style="color:var(--purple)">專屬修改頁</p><h1 style="color:var(--purple-deep)">{E(r['name'])} 的檔案</h1>
{bnote}{note}
{_form_html(f"/tut/team/edit/{r['edit_token']}" + (f"?build={E(build)}" if build else ""), d, error, existing=r, build=build)}
<form method="post" action="/tut/team/edit/{r['edit_token']}/delete" onsubmit="return confirm('確定要刪除您的檔案嗎？刪除後就不會出現在團隊頁。')" style="margin:-32px 0 56px">
<button class="btn danger">刪除我的檔案</button></form></div>"""
    return _page("修改我的檔案｜" + TITLE, body, robots=False)


def render_admin(secret, msg=""):
    code = admin_code(secret)
    rows = list_members(include_hidden=True)
    tr = "".join(
        f"<tr><td>{TEAMS.get(r['team'], r['team'])}<br>{E(r['role'])}</td><td><b>{E(r['name'])}</b><br>{E(r['company_title'])}</td>"
        f"<td>{'✅ 已上架' if r['filled'] else '🪑 空座位'}{'<br>🙈 已隱藏' if r['hidden'] else ''}</td>"
        f"<td><a href='/tut/team/edit/{E(r['edit_token'])}' target='_blank' rel='noopener'>修改</a> "
        f"<button type='button' data-url='https://event.bymyway.com/tut/team/edit/{E(r['edit_token'])}' onclick='copyLink(this)'>複製專屬連結</button> "
        f"<form method='post' action='/tut/team/a/{code}/hide/{r['id']}'><input type='hidden' name='hidden' value='{0 if r['hidden'] else 1}'>"
        f"<button>{'恢復顯示' if r['hidden'] else '隱藏'}</button></form> "
        f"<form method='post' action='/tut/team/a/{code}/delete/{r['id']}' onsubmit=\"return confirm('確定刪除？')\"><button>刪除</button></form></td></tr>"
        for r in rows)
    team_opts = "".join(f'<label class="choice"><input type="radio" name="team" value="{k}" {"checked" if k == "board" else ""}><span>{lab}</span></label>' for k, lab in TEAMS.items())
    body = f"""<div class="wrap" style="padding-top:32px;padding-bottom:56px">
<h1 style="color:var(--purple-deep)">理監事與顧問團隊・管理後台</h1>
<p style="color:var(--muted)">「修改」可直接幫本人改資料；「隱藏」先不公開、資料保留；有人亂填可以刪除。<a href="/tut/team" target="_blank">看公開頁</a></p>
{f'<p class="ok">{E(msg)}</p>' if msg else ''}
<p class="hint">「複製專屬連結」＝傳給本人讓他自己補資料或修改的連結（不用登入）；上方網址列的後台網址只有你知道，不要傳給別人。</p>
<table><thead><tr><th>團隊／職務</th><th>姓名／公司</th><th>狀態</th><th></th></tr></thead><tbody>{tr}</tbody></table>
<form class="paper" method="post" action="/tut/team/a/{code}/seat"><h2 style="font-size:22px;margin-bottom:12px">新增空座位</h2>
<p class="hint" style="margin-top:0">理監事名單確定後，可先把名字放上去，本人點自己的名字補資料。</p>
<div class="field"><div class="choices">{team_opts}</div></div>
<div class="two"><div class="field"><label for="s_name">姓名</label><input type="text" id="s_name" name="name" required maxlength="30"></div>
<div class="field"><label for="s_role">職務</label><input type="text" id="s_role" name="role" maxlength="20" placeholder="例：常務理事"></div></div>
<div class="field"><label for="s_title">公司／職稱</label><input type="text" id="s_title" name="company_title" maxlength="60"></div>
<button class="btn purple">新增座位</button></form></div>
<script>
function copyLink(btn) {{
  var url = btn.getAttribute('data-url');
  var done = function () {{ var t = btn.textContent; btn.textContent = '已複製！'; setTimeout(function () {{ btn.textContent = t; }}, 1800); }};
  if (navigator.clipboard) {{ navigator.clipboard.writeText(url).then(done, function () {{ prompt('請複製這條連結：', url); }}); }}
  else {{ prompt('請複製這條連結：', url); }}
}}
</script>"""
    return _page("管理後台｜" + TITLE, body, robots=False)
