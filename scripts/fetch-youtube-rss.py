#!/usr/bin/env python3
"""
fetch-youtube-rss.py — 抓 31 個 YouTube 頻道最新影片
不需要 API Key，用公開 RSS，零 AI Token
"""
import urllib.request, re, sys
from datetime import datetime, timezone, timedelta

CHANNELS = [
    ("孔老師AI研習社",    "UCpnBpREMjMNFvLTLnc2iLPQ"),
    ("inspiredcanvas",    "UC17zrOCuDUXmtREyx9G2tCQ"),
    ("LuluTechnology",    "UCPwCUeMO9EB-kFno2zKsm9w"),
    ("綠色火車",          "UCJhUtNsR5pvU_gWWkxxUXUQ"),
    ("applefans520",      "UCCC_m0Lw7Z4IT6IjoPb0ZLg"),
    ("KOCPC",             "UCcQA-MzQxCvET1S-BekQdAA"),
    ("PanSci科學新聞",    "UCATnB3v_NkTTd9iD_4W2A-g"),
    ("apple-dad",         "UCIpZAGl9xHcuzmHW0AAJs7g"),
    ("rickhau99",         "UCKMtbQbyhpBgyKaNX5vJUsw"),
    ("MeticsMedia中文",   "UC7Qp52WIwke2P3l1Xh6k74Q"),
    ("AlanChen",          "UCfB2JYduVCYdHcoxlEWGw4w"),
    ("PH-WorkFlow",       "UCpXOvRzWW0lJhYrUeWBlNmA"),
    ("TuTu",              "UCuhAUKCdKrjYoMiJQc74ZkQ"),
    ("lichangzhanglaile", "UC0v9b0Z00wWED_vGy-Q6ibg"),
    ("Macro_Alpha_cn",    "UC9oosAco7nIVZwuGhnC0FKg"),
    ("AIPractitioners",   "UCfMXQ45Ch5EnT2jokiHuysw"),
    ("SFReality",         "UCCzf5FvUaAurIuY-YGmWJyQ"),
    ("mage291",           "UCG_qhxmgI1E0wO4x11TiI5w"),
    ("ami.moment",        "UCGs_cktFPCgN8ggJJVon84g"),
    ("TackyTechy",        "UC3YHFDbkHcqVxg4w20YYC7A"),
    ("martinz2025",       "UC1HhvtQd_yTBJAGYNYffmSQ"),
    ("BizofFame",         "UCQT2N6N_Jay8nWS_0h7muyw"),
    ("Petersunreview",    "UCl9BPXjyEmA0q6IrQvsEazA"),
    ("techbang3c",        "UC9IyDJ6vlG50iYjXGQpwwOQ"),
    ("aaron-1215",        "UCKHHtxWYOg15Gsrsa9ZDfrA"),
    ("talkspg",           "UCUa8Meh6_eFq7v1h_CCa9fQ"),
    ("AI-Short-Taipei",   "UC1Ld3B4Y1NBam9BTk9tMThR"),
    ("digitalxu",         "UCGQPLvp98hRrzTG14AiTfUQ"),
    ("austinchou888",     "UC3hsgc8SHJs1RDMEZBCAccA"),
    ("HarryLee",          "UCEA4ZfPzWDHp72mlq7IvUcw"),
    ("sensebar",          "UCI2YklLazU9tB_Kh_9nMpKA"),
]

days = 2
if "--days" in sys.argv:
    try: days = int(sys.argv[sys.argv.index("--days")+1])
    except: pass

CUTOFF = datetime.now(timezone.utc) - timedelta(days=days)
TZ8 = timezone(timedelta(hours=8))
results, errors = [], []

for name, cid in CHANNELS:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml = resp.read().decode("utf-8")

        # 頻道名稱（第一個 <title> 標籤）
        titles_in_xml = re.findall(r"<title[^>]*>(.*?)</title>", xml, re.DOTALL)
        channel_name = titles_in_xml[0].strip() if titles_in_xml else name

        # 解析每個 entry
        entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
        for entry in entries[:3]:
            t = re.search(r"<title[^>]*>(.*?)</title>", entry, re.DOTALL)
            l = re.search(r'<link[^>]*href="([^"]+)"', entry)
            p = re.search(r"<published>(.*?)</published>", entry)
            if not (t and l and p): continue
            try:
                pub = datetime.fromisoformat(p.group(1).replace("Z","+00:00"))
            except: continue
            if pub >= CUTOFF:
                results.append({
                    "ch": channel_name,
                    "title": t.group(1).strip(),
                    "url": l.group(1),
                    "pub": pub.astimezone(TZ8).strftime("%m/%d %H:%M"),
                })
    except Exception as e:
        errors.append(f"❌ {name}: {e}")

print(f"=== 過去 {days} 天新影片（共 {len(results)} 部）===\n")
for i, r in enumerate(results, 1):
    print(f"{i}. 【{r['ch']}】{r['title']}")
    print(f"   🔗 {r['url']}  ({r['pub']} 台北)")
    print()

if errors:
    print(f"\n=== 無法讀取（{len(errors)} 個）===")
    for e in errors: print(f"  {e}")
