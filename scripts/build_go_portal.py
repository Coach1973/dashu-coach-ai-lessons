#!/usr/bin/env python3
"""大樹入口（event.bymyway.com/curated/go/）資料產生器。2026-11-11 教練交辦。

用法：python3 build_go_portal.py ~/github_repos/go    → 寫出 data.js（網站倉庫＝線上，寫完在倉庫 commit＋push 就上線）
     python3 build_go_portal.py <網站資料夾> --check → 只印統計與找不到的項目，不寫檔

資料來源（全部只讀）：
  1. coach888（大樹作品集）：~/github_repos/coach888/index.html ＋ 雲端排版 /api/coach888/state
  2. my-tools：~/github_repos/my-tools/tools.json
  3. works-map（大樹作品分類表）：works_map_classify.load()（all-works/data.json）
  4. Claude 報告清單快照：scripts/go_portal_artifacts.json（[名稱, 網址, 最後更新日]）
  5. 使用頻率：Chrome 近 75 天開過幾天（只算教練自家網域）＋ /api/coach888/click-counts 點擊次數

分類＝下方 SERIES（明確名單，教練 11/11 指定的六大系列）＋ AUTO（關鍵字把其餘作品自動歸進系列的「其他相關」）。
網頁執行時還會即時抓雲端排版與點擊次數：新上架的作品不用重跑這支也會出現在搜尋與「最新加入」。
"""
import collections, json, re, shutil, sqlite3, sys, tempfile, time, urllib.request
from pathlib import Path

H = Path.home()
sys.path.insert(0, str(Path(__file__).parent))
import works_map_classify as wc  # noqa: E402

API = "https://event.bymyway.com/api/coach888/"
CHROME_HISTORY = H / "Library/Application Support/Google/Chrome/Default/History"
OWN = ("bymyway.com", "coach1973.github.io", "claude.ai/artifact", "netlify.app", "tava-ai.com/chat")
HUBS = ("coach1973.github.io/coach888", "coach1973.github.io/my-tools", "event.bymyway.com/curated/works-map",
        "coach1973.github.io/all-works", "event.bymyway.com/curated/go")


def norm(u):
    u = re.sub(r"^https?://", "", u.strip()).split("#")[0]
    host, _, rest = u.partition("/")
    return (host + "/" + rest.partition("?")[0]).rstrip("/").lower()


def get_json(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "Mozilla/5.0 (go-portal-builder)"})  # 預設 UA 會被 Cloudflare 擋 403
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


# ───────────────────────── 1. 收集全部作品 ─────────────────────────
def collect():
    src = (H / "github_repos/coach888/index.html").read_text(encoding="utf-8")
    static = {}
    for m in re.finditer(r'<div class="item" data-url="([^"]+)">.*?<a class="name"[^>]*>(.*?)</a>.*?'
                         r'<div class="badge [a-z]+"[^>]*>(.*?)</div>', src, re.S):
        static.setdefault(m.group(1), (re.sub("<[^>]+>", "", m.group(2)), m.group(3)))
    st = get_json("state")
    J = lambda k: json.loads(st[k]) if isinstance(st.get(k), str) else (st.get(k) or {})
    layout, names, items, titles = J("coach888_layout"), J("coach888_names"), J("coach888_items"), J("coach888_titles")
    out = []
    for sec, urls in layout.items():
        if sec == "recentlydeleted":
            continue
        for u in urls:
            it = items.get(u) or {}
            n = names.get(u) or it.get("name") or static.get(u, ("", ""))[0] or u
            b = it.get("badge") or static.get(u, ("", ""))[1]
            out.append({"n": n, "u": u, "d": "", "b": b, "from": "大樹作品集・" + titles.get(sec, sec)})
    newest = [u for u in layout.get("zuixinzuopin", [])][:14]
    for sec in json.load(open(H / "github_repos/my-tools/tools.json", encoding="utf-8")):
        for t in sec.get("tools", sec.get("items", [])):
            out.append({"n": t["name"], "u": t["url"], "d": t.get("desc", ""), "b": t.get("tag", ""),
                        "from": "my-tools・" + sec["title"]})
    wm, _ = wc.load()
    cats = {k: t for k, _, t, _ in wc.CATS}
    for x in wm:
        if x["cat"] == "internal":
            continue
        out.append({"n": x["name"], "u": x["url"], "d": "", "b": "", "from": "作品分類表・" + cats[x["cat"]],
                    "t": x.get("updated", "")})
    arts = json.load(open(Path(__file__).parent / "go_portal_artifacts.json", encoding="utf-8"))
    for n, u, d in arts:
        out.append({"n": n, "u": u, "d": "", "b": "報告", "from": "Claude 報告", "t": d})
    # 去重：同一網址留第一個（作品集名稱優先），日期取有的
    seen, uniq = {}, []
    for x in out:
        k = norm(x["u"])
        if k in seen:
            y = seen[k]
            y["t"] = y.get("t") or x.get("t", "")
            y["d"] = y["d"] or x["d"]
            continue
        seen[k] = x
        uniq.append(x)
    return uniq, newest, {norm(u): d for _, u, d in arts}


# ───────────────────────── 2. 使用頻率 ─────────────────────────
def usage():
    days = collections.defaultdict(set)
    try:
        tmp = Path(tempfile.mkdtemp()) / "History"
        shutil.copy(CHROME_HISTORY, tmp)
        db = sqlite3.connect(tmp)
        cond = " or ".join(f"u.url like '%{d}%'" for d in OWN)
        for url, d in db.execute(
                f"select u.url, date(v.visit_time/1000000-11644473600,'unixepoch','+8 hours') from visits v "
                f"join urls u on u.id=v.url where ({cond}) and "
                f"v.visit_time/1000000-11644473600 > cast(strftime('%s','now','-75 days') as integer)"):
            days[norm(url)].add(d)
        db.close()
    except Exception as e:  # Chrome 紀錄讀不到就只用點擊次數，不擋產生
        print("⚠️ Chrome 紀錄讀不到：", e)
    clicks = collections.Counter()
    try:
        for u, n in get_json("click-counts").items():
            clicks[norm(u)] += n if isinstance(n, int) else 0
    except Exception as e:
        print("⚠️ 點擊次數讀不到：", e)
    return {k: len(v) for k, v in days.items()}, clicks


# ───────────────────────── 3. 六大系列（教練 11/11 指定） ─────────────────────────
# 每一項：(顯示名稱, 網址或「找:名稱片段」, 一句說明)。網址含金鑰的一律用「找:」從作品集取，不在這裡寫死。
SERIES = [
    {"id": "team", "name": "全世界最優秀的團隊計劃", "short": "團隊計劃", "color": "#e8c170", "img": "images/g-team.webp",
     "tag": "客戶、人才、伯樂——全部構想的核心", "groups": [
        ("網頁製作三神器", "tools", [
            ("網頁一鍵導入", "找:網頁一鍵導入", "做個人品牌／活動網頁，一鍵帶入開工指令"),
            ("生圖一鍵注入", "找:生圖一鍵注入", "LK888 出圖，一鍵帶入圖片指令"),
            ("反向技能書 14 招示範", "找:反向技能書 14 招示範", "看得到、點得到的 14 個網頁特效"),
        ]),
        ("計劃核心頁", "core", [
            ("全世界最優秀的團隊計畫", "https://event.bymyway.com/curated/bestteam/", "計劃總頁"),
            ("三缺：客戶、人才、伯樂", "https://event.bymyway.com/curated/three-lacks/", "商務市場最缺的三件事"),
            ("人才軍火庫・顧問師天團", "https://event.bymyway.com/curated/skyteam/", "上百位專家與顧問師"),
            ("為你轉身・商業導師席", "https://event.bymyway.com/curated/turnforyou/", "八位商業顧問師"),
            ("AI 百人導師團隊", "https://mentor100.bymyway.com/", "mentor100 導師計畫"),
            ("信任遊戲", "找:信任遊戲（測試版）", "信任一圈一圈長出來"),
            ("團隊分會總表（非 BNI）", "https://team.bymyway.com/", "招募創始會員"),
            ("BNI 組隊計畫×免費建站漏斗", "找:BNI組隊計畫×免費建站漏斗策略筆記", "策略筆記"),
            ("經典對話：商務市場最缺三件事", "找:經典對話：商務市場最缺三件事", "大樹教練與雲端克勞德軍師"),
            ("原話報告書：AI 企業團隊戰略", "找:教練原話報告書｜AI 企業團隊戰略", "BNI × AI × 教育訓練"),
            ("原話逐字報告書：商務遊戲", "找:教練原話逐字報告書｜商務遊戲", "AI 百人導師"),
            ("百人軍火庫企劃書", "找:百人軍火庫企劃書", "Claude 報告"),
            ("大樹軍火庫", "https://claude.ai/artifact/SZ1VcgyKtufGpUXxH2c6AP", "Claude 報告"),
        ]),
        ("後台與管理", "admin", [
            ("未上架的人才軍火庫", "找:未上架的人才軍火庫", "勾選上架／下架"),
            ("AI 百人導師後台", "找:AI百人導師後台系統", "導師資料管理"),
            ("團隊分會後台", "https://team.bymyway.com/admin", "編輯・第一分會"),
            ("AI 資源媒合・帳號審核", "找:AI資源媒合系統・帳號審核", "審核加入的帳號"),
            ("信任遊戲現場後台", "找:信任遊戲", "活動現場用"),
        ]),
        ("一鍵系列・製作工具", "kit", [
            ("出圖一鍵注入", "找:出圖一鍵注入", ""),
            ("策展一鍵注入", "找:策展一鍵注入", ""),
            ("簡報套底圖一鍵注入", "找:簡報套底圖一鍵注入", ""),
            ("特助一鍵注入", "找:特助一鍵注入", ""),
            ("隨身軍師・一鍵接手", "找:隨身軍師・一鍵接手", "工作交接棒，貼給任何 AI"),
            ("反向操作技能書", "找:反向操作技能書｜看到喜歡的網頁", "拆解別人的網頁，換成自己的重做"),
            ("網頁開頭動畫技能", "找:做整個網頁開頭動畫的技能", "一頁式開工指令"),
            ("課程報名網頁開工指令", "https://coach1973.github.io/course-signup-playbook/", ""),
            ("大樹常用技能表（公開版）", "找:大樹常用技能表（公開版）", ""),
            ("字級大小對照表", "找:字級大小對照表", ""),
        ]),
    ]},
    {"id": "rongtree", "name": "榮樹下", "short": "榮樹下", "color": "#86d19a", "img": "images/g-rongtree.webp",
     "tag": "大樹下泡茶，聊出一集又一集的故事", "groups": [
        ("每次都用", "daily", [
            ("來賓卡（全部來賓總覽）", "找:榮樹下｜來賓卡", "來賓資料、AI 來賓卡、預約狀態"),
            ("時間預約表", "https://event.bymyway.com/curated/rongtree/#prep", "接下來的訪談＋還有空檔的時間"),
            ("來賓進度追蹤表", "https://event.bymyway.com/curated/rongtree-sop/#tracker", "網頁直接勾選"),
            ("大樹教練可約時間", "找:大樹教練｜可約時間", "別人預約我的時間表"),
        ]),
        ("對外頁面", "public", [
            ("榮樹下官網", "https://event.bymyway.com/curated/rongtree/", "邱裕榮與吳大樹談古論今聊家常"),
            ("預約專訪表單", "https://event.bymyway.com/curated/rongtree/#join", "來賓自己選時間"),
            ("來賓邀約 SOP 流程", "找:榮樹下｜來賓邀約 SOP 流程", ""),
            ("邀請函", "https://event.bymyway.com/curated/rongtree/invite.html", ""),
            ("SoundOn Podcast 節目頁", "找:SoundOn Podcast 播放器", "每一集都在這裡"),
        ]),
    ]},
    {"id": "bni", "name": "BNI 商務團隊", "short": "BNI", "color": "#ff8a80", "img": "images/g-bni.webp",
     "tag": "總表、後台、各分會戰情，一次到位", "groups": [
        ("最常看", "daily", [
            ("BNI 大台南南區分會總表", "https://chapters.bymyway.com/", "最常點的一頁"),
            ("戰情儀表板（全區）", "https://chapters.bymyway.com/dashboards", "大台南南區"),
            ("DNA 出席", "https://coach1973.github.io/bni-dna/", ""),
            ("培訓總覽", "https://chapters.bymyway.com/training", ""),
            ("來賓總覽", "https://chapters.bymyway.com/guests", ""),
            ("來賓邀約排行榜", "https://coach1973.github.io/BNI-Training/guests.html", ""),
            ("BNI 培訓行事曆", "https://event.bymyway.com/tainan-calender/", ""),
            ("燈號表", "https://event.bymyway.com/bni-traffic/", ""),
        ]),
        ("後台", "admin", [
            ("分會後台管理系統", "https://chapters.bymyway.com/admin", ""),
            ("信用証追蹤系統", "https://namecard.bymyway.com/bni-credit", ""),
            ("BNI 培訓紀錄總資料庫", "找:BNI培訓紀錄總資料庫", ""),
            ("開發票專用後台", "https://namecard.bymyway.com/invoice-admin", "培訓費、入會續約發票"),
            ("名片資料庫搜尋", "https://namecard.bymyway.com/", ""),
            ("找人才・找專業", "https://namecard.bymyway.com/find", ""),
            ("產業鏈媒合總覽", "https://namecard.bymyway.com/chains", ""),
            ("大台南小幫手・對話監控", "https://bni.bymyway.com/chat", "LINE 小幫手的對話"),
        ]),
        ("各分會戰情儀表板", "chapters", [
            ("真鑽分會", "https://real-diamonds.bymyway.com/", "邀約來賓戰情"),
            ("真誠分會", "https://sincere.bymyway.com/", "邀約來賓戰情"),
            ("真鑫分會", "https://zhenxin.bymyway.com/", "邀約來賓戰情"),
            ("真貴籌備會", "https://real-wealth.bymyway.com/", "邀約來賓戰情"),
            ("Team 01", "https://team01.bymyway.com/", "邀約來賓戰情"),
            ("真誠分會頁", "https://chapters.bymyway.com/sincere", ""),
            ("真鑽・重返榮耀三年數據", "https://real-diamonds.bymyway.com/report", ""),
        ]),
        ("教材與培訓", "teach", [
            ("說故事完成入會訪談", "https://event.bymyway.com/curated/bni-story/", "15 張卡牌，今天剛換好圖"),
            ("從 A 到 B：過橋任務", "https://event.bymyway.com/curated/a-to-b/", ""),
            ("你的假設對了嗎？來賓接待", "找:你的假設對了嗎？｜BNI 來賓接待培訓工作坊", "45 分鐘工作坊互動教材"),
            ("冷卻期標準話術 SOP", "找:BNI 冷卻期標準話術 SOP", "邀約・回訪・假設"),
            ("系統實戰與心態修練教材", "找:BNI 系統實戰與心態修練教材", "信任資產活教材"),
            ("學會邀約・五倍成長工作坊", "找:學會邀約，你永遠不缺客戶", ""),
        ]),
    ]},
    {"id": "comic", "name": "漫畫系列", "short": "漫畫", "color": "#ffb3c7", "img": "images/g-comic.webp", "family": "team",
     "tag": "團隊計劃的漫畫版——同一個脈絡", "groups": [
        ("漫畫", "comic", [
            ("大樹的答案・漫畫版", "https://event.bymyway.com/curated/answer/", "日系漫畫版思想漫畫"),
            ("大樹的答案・真人版", "https://event.bymyway.com/curated/answer-tree/", ""),
            ("企業成長條漫 EP01–05", "https://event.bymyway.com/curated/answer2/", "全五話"),
            ("造林・十二章漫畫", "https://event.bymyway.com/curated/zaolin/", "一個人、四段車程，與一片森林"),
            ("32MB 封包攻防戰・全集", "https://event.bymyway.com/curated/ai-story/", "教練與軍師的 AI 漫畫"),
            ("32MB 封包攻防戰・第 1 話", "找:深夜的 32MB 封包攻防戰 第1話", "TAVA 做的漫畫"),
        ]),
        ("AI 漫劇・長談", "drama", [
            ("你非常確定嗎？AI 漫劇", "https://event.bymyway.com/curated/yousure/", "第一版"),
            ("證明給機器看・四夜長談", "https://event.bymyway.com/curated/c-challenge/", "大樹教練與軍師"),
        ]),
    ]},
    {"id": "jarvis", "name": "與賈維斯的對話檢討", "short": "賈維斯", "color": "#8fd3ff", "img": "images/g-jarvis.webp",
     "tag": "每一次檢討，都讓特助更懂您", "groups": [
        ("對話主控台", "console", [
            ("VPS 小龍蝦主控台", "https://coach.bymyway.com/chat", "對外體驗版"),
            ("大台南小幫手・對話監控", "https://bni.bymyway.com/chat", "LINE 小幫手"),
            ("教練都在想什麼・對話監控", "https://seabiscuit.bymyway.com/chat", "LINE 小幫手"),
        ]),
        ("體檢與檢討報告", "review", "ARTS:賈維斯|檢討|體檢|盤查|靈魂拷問|系統優化|改了 11 次|額度查因"),
        ("設備與分工檢討", "infra", "ARTS:SSD|空間|容量|外接 Claude|換 Claude|雲端與本機"),
        ("特助養成", "grow", [
            ("特助 21 心法完整版", "找:特助21心法完整版", ""),
            ("特助心法實踐故事・第一部", "https://coach1973.github.io/coach-case/", ""),
            ("特助心法實踐故事・第二部", "https://coach1973.github.io/coach-case2/", ""),
            ("特助心法實踐故事・第三部", "https://coach1973.github.io/coach-case3/", ""),
            ("特助心法實踐故事・第四部", "https://coach1973.github.io/coach-case4/", ""),
            ("頂級特助俱樂部（純淨版）", "找:頂級特助俱樂部（純淨版）", ""),
            ("試金石檔案", "找:試金石檔案", ""),
        ]),
    ]},
    {"id": "milestone", "name": "大樹常用・里程碑", "short": "常用・里程碑", "color": "#f2b866", "img": "images/g-milestone.webp",
     "tag": "每天要用的入口，加上一路走來的里程碑", "groups": [
        ("每天要用", "daily", [
            ("大臺南商圈・店家登錄", "找:大臺南商圈整合計劃・店家登錄", "點擊次數第一名"),
            ("商圈後台（上／下架店家）", "找:大台南商圈整合計劃後台", ""),
            ("教練專屬後台密碼總覽", "找:教練專屬後台密碼總覽", ""),
            ("大樹教練待辦事項", "找:大樹教練待辦事項（特助主動提醒版）", "特助主動提醒版"),
            ("大樹小講", "https://event.bymyway.com/bigtree/", "2013 年起的公益巡講"),
            ("大樹小講・場次管理", "https://event.bymyway.com/admin/sessions", ""),
            ("大樹小講・活動後台", "找:大樹小講活動後台系統", ""),
            ("海餅乾俱樂部 20 週年", "https://event.bymyway.com/seabiscuit20/", ""),
            ("大樹教育顧問官網", "https://www.bymyway.com/", ""),
            ("策展上傳（手動上架作品）", "找:策展上傳網址（教練自己手動上傳用）", ""),
            ("掃描檔案下載", "找:掃描檔案下載", ""),
            ("留資料後台（作品頁表單收件）", "找:留資料後台", ""),
            ("課程教材線上觀看後台", "找:教練課程教材線上觀看後台", ""),
            ("NMDA 會員資料後台", "找:NMDA 會員資料後台", ""),
        ]),
        ("活動現場工具", "event", [
            ("數位簽到系統", "找:數位簽到系統", ""),
            ("抽獎轉盤系統", "找:抽獎轉盤系統", ""),
            ("掃 QR Code 玩抽獎", "找:掃 QR Code 玩抽獎", ""),
            ("結繩領導學戰報系統", "找:結繩領導學戰報系統", ""),
            ("佩佩老師活動後台", "找:佩佩老師活動後台系統", ""),
            ("佩佩老師報名系統", "找:佩佩老師活動報名系統", ""),
            ("佩佩老師報到系統", "找:佩佩老師報到系統", ""),
        ]),
        ("里程碑紀錄", "timeline", "TIMELINE"),
    ]},
]
# 關鍵字自動歸類（把沒列在上面的作品放進各系列的「其他相關」）。順序有意義：先比對到的先拿。
AUTO = [
    ("comic", r"漫畫|條漫|漫劇|/answer|zaolin|ai-story|yousure"),
    ("rongtree", r"榮樹下|rongtree"),
    ("jarvis", r"賈維斯|體檢|自我檢測|特助|試金石|小龍蝦"),
    ("bni", r"BNI|分會|chapters\.bymyway|真鑽|真誠|真鑫|真貴|team01|namecard"),
    ("team", r"團隊計畫|最優秀|軍火庫|天團|百人導師|mentor100|為你轉身|三缺|信任遊戲|trust\.bymyway|一鍵|反向|開工指令"),
]
MILESTONE_SKIP = r"賈維斯|檢討|體檢|盤查|靈魂拷問|系統優化|改了 11 次|額度查因|SSD|空間|容量|外接 Claude|換 Claude|雲端與本機"


def build(out_dir, check=False):
    allx, newest, art_dates = collect()
    hdays, clicks = usage()
    by = {norm(x["u"]): x for x in allx}

    def find(q):
        q = q[2:]
        exact = next((x for x in allx if x["n"] == q), None)  # 名稱完全相同優先（「信任遊戲」≠「信任遊戲（測試版）」）
        return exact or next((x for x in allx if q in x["n"]), None)

    items, idx, missing = [], {}, []

    def add(x, s, g, name=None, desc=None, extra=None):
        k = norm(x["u"])
        key = (x["u"], s, g)
        if key in idx:
            return idx[key]
        it = {"n": name or x["n"], "u": x["u"], "d": desc if desc is not None else x.get("d", ""), "s": s, "g": g,
              "h": hdays.get(k, 0), "c": clicks.get(k, 0), "f": x.get("from", "")}
        if x.get("t"):
            it["t"] = x["t"]
        if extra:
            it.update(extra)
        items.append(it)
        idx[key] = len(items) - 1
        return idx[key]

    placed = set()
    series_out = []
    arts = json.load(open(Path(__file__).parent / "go_portal_artifacts.json", encoding="utf-8"))
    for S in SERIES:
        groups = []
        for title, gk, spec in S["groups"]:
            ids = []
            if spec == "TIMELINE":
                tl = [a for a in arts if not re.search(MILESTONE_SKIP, a[0])]
                tl.append(["大樹作品分類表（256 件作品分 9 類）", "https://event.bymyway.com/curated/works-map/", "2026-11-09"])
                tl.append(["大樹入口上線（就是這一頁）", "https://event.bymyway.com/curated/go/", "2026-11-11"])
                tl.sort(key=lambda a: a[2], reverse=True)
                for n, u, d in tl:
                    x = by.get(norm(u)) or {"n": n, "u": u, "d": ""}
                    ids.append(add(x, S["id"], gk, name=n, desc="", extra={"t": d}))
                    placed.add(norm(u))
            elif isinstance(spec, str) and spec.startswith("ARTS:"):
                for n, u, d in sorted(arts, key=lambda a: a[2], reverse=True):
                    if re.search(spec[5:], n):
                        ids.append(add(by.get(norm(u)) or {"n": n, "u": u, "d": ""}, S["id"], gk, name=n, desc="",
                                       extra={"t": d}))
                        placed.add(norm(u))
            else:
                for name, ref, desc in spec:
                    x = find(ref) if ref.startswith("找:") else (by.get(norm(ref)) or {"n": name, "u": ref, "d": ""})
                    if x is None:
                        missing.append(f"{S['short']}／{title}／{name}（{ref}）")
                        continue
                    if not ref.startswith("找:") and "#" in ref:
                        x = dict(x, u=ref)  # 錨點（#prep 等）保留
                    ids.append(add(x, S["id"], gk, name=name, desc=desc))
                    placed.add(norm(x["u"]))
            groups.append({"t": title, "k": gk, "i": ids})
        series_out.append({k: S[k] for k in ("id", "name", "short", "color", "img", "tag")} |
                          ({"family": S["family"]} if S.get("family") else {}) | {"groups": groups, "more": []})
    # 其他相關（自動歸類）＋搜尋用的其餘作品
    sid = {s["id"]: s for s in series_out}
    rest = 0
    for x in allx:
        k = norm(x["u"])
        if k in placed or any(h in k for h in HUBS):
            continue
        hay = x["n"] + " " + x["u"]
        hit = next((s for s, rx in AUTO if re.search(rx, hay)), None)
        i = add(x, hit or "", "more")
        if hit:
            sid[hit]["more"].append(i)
        else:
            rest += 1
    # 最新加入（作品集「最新作品」前 14 筆）
    new_ids = []
    for u in newest:
        x = by.get(norm(u))
        if x:
            j = next((i for i, it in enumerate(items) if norm(it["u"]) == norm(u)), None)
            new_ids.append(j if j is not None else add(x, "", "more"))
    data = {
        "built": time.strftime("%Y-%m-%d %H:%M"),
        "series": series_out,
        "items": items,
        "newest": new_ids,
        "hubs": [
            {"n": "大樹作品集（排版後台）", "u": "https://coach1973.github.io/coach888/", "d": "拖曳排序、改名、新增項目都在這裡"},
            {"n": "大樹作品分類表", "u": "https://event.bymyway.com/curated/works-map/", "d": "256 件作品依 9 類排好"},
            {"n": "my-tools 常用工具箱", "u": "https://coach1973.github.io/my-tools/", "d": "AI 老師推薦的工具、日常查詢"},
            {"n": "作品一覽（全部作品）", "u": "https://coach1973.github.io/all-works/", "d": "三個來源去重，可搜人名"},
        ],
        "stats": {"all": len({norm(i["u"]) for i in items}), "placed": len(placed), "history_days": 75,
                  "sources": {"coach888": 274, "mytools": 45, "worksmap": 260}},
        "auto": [[s, rx] for s, rx in AUTO],
    }
    print(f"作品 {data['stats']['all']} 件（系列內 {len(placed)}，自動歸類 "
          f"{sum(len(s['more']) for s in series_out)}，只在搜尋 {rest}）；最新加入 {len(new_ids)}")
    for s in series_out:
        print(f"  {s['short']}: " + "、".join(f"{g['t']}{len(g['i'])}" for g in s["groups"]) + f"、其他{len(s['more'])}")
    if missing:
        print("❌ 找不到：\n  " + "\n  ".join(missing))
    if not check:
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        js = "window.GO=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
        (Path(out_dir) / "data.js").write_text(js, encoding="utf-8")
        print("寫出", Path(out_dir) / "data.js", f"{len(js.encode()) // 1024} KB")
    return not missing


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(0 if build(sys.argv[1], "--check" in sys.argv) else 1)
