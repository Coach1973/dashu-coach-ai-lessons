#!/usr/bin/env python3
"""五個分會（team.bymyway.com 第一～第五分會）＋第一分會每週統計表（team01.bymyway.com）查詢／更新小工具。
2026-10-01 教練交辦給怡靜專屬特助使用（怡靜是五個分會後台的總管理）。

讀資料：唯讀開資料庫。寫資料：一律走網站自己的更新入口（跟網頁上點選是同一條路，網站會自己檢查格式）。
出缺席／來賓／121／咖啡的每週統計表目前只有第一分會有。

用法（口令都是中文）：
  team_tool.py 分會                         五個分會總覽
  team_tool.py 分會 <1~5 或 第三分會>        單一分會的介紹、成員、公告、參訪報名
  team_tool.py 名單                          第一分會每週統計表上的名單
  team_tool.py 查 <姓名>                     在五個分會和第一分會統計表裡找這個人
  team_tool.py 週 <第三週 | 2026-09-24 | 9/24 | 本週>
  team_tool.py 出席 <姓名> <週> <實體|線上|缺席|清除>
  team_tool.py 新增 <姓名>                   把名字填進第一分會統計表的第一個空位
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
import urllib.request
from datetime import date
from pathlib import Path

DB = Path.home() / "github_repos" / "team01-guests" / "team01_guests.db"
TEAM_DB = Path.home() / "github_repos" / "team-bymyway" / "team.db"
API = "http://127.0.0.1:5091"
STATUS_LABEL = {"active": "正式運作", "forming": "籌備中"}
ATT = {"實體": "onsite", "線上": "online", "缺席": "absent", "清除": None}
ATT_LABEL = {"onsite": "實體", "online": "線上", "absent": "缺席", None: "未填"}
CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def conn(path: Path = DB) -> sqlite3.Connection:
    c = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    return c


def find_chapter(t, text: str):
    s = text.strip().replace("分會", "").replace("第", "").replace("team", "").replace("Team", "").strip("-0 ")
    n = CN_NUM.get(s) or (int(s) if s.isdigit() else None)
    row = t.execute("SELECT * FROM chapters WHERE sort_order = ? OR id = ?", (n, n)).fetchone() if n else None
    if row:
        return row, None
    return None, f"找不到「{text}」，請說第一到第五分會其中一個。"


def cmd_chapters(t):
    print("【五個分會總覽】")
    for ch in t.execute("SELECT * FROM chapters ORDER BY sort_order"):
        members = t.execute("SELECT count(*) FROM chapter_members WHERE chapter_id = ?", (ch["id"],)).fetchone()[0]
        visits = t.execute("SELECT count(*) FROM visit_signups WHERE chapter_id = ?", (ch["id"],)).fetchone()[0]
        print(f"・{ch['name_zh']}（{STATUS_LABEL.get(ch['status'], ch['status'])}）成員介紹 {members} 位｜預約參訪 {visits} 筆")
    print("每週出缺席／來賓統計表：目前只有第一分會有。")


def cmd_chapter(t, text):
    ch, err = find_chapter(t, text)
    if err:
        print(err)
        return
    print(f"【{ch['name_zh']}】{STATUS_LABEL.get(ch['status'], ch['status'])}")
    if ch["hero_title"]:
        print(f"標語：{ch['hero_title']}")
    stats = [f"{r['num']} {r['label']}" for r in t.execute(
        "SELECT * FROM chapter_stats WHERE chapter_id = ? ORDER BY sort_order", (ch["id"],))]
    if stats:
        print("數字看板：" + "；".join(stats))
    members = t.execute("SELECT name, company_title FROM chapter_members WHERE chapter_id = ? ORDER BY id", (ch["id"],)).fetchall()
    print(f"成員介紹（{len(members)} 位）：" + ("、".join(f"{m['name']}（{m['company_title']}）" for m in members) or "還沒有人登錄"))
    notices = [r["title"] for r in t.execute("SELECT title FROM chapter_notices WHERE chapter_id = ? ORDER BY sort_order", (ch["id"],))]
    if notices:
        print("參訪須知：" + "、".join(notices))
    visits = t.execute("SELECT name, company, created_at FROM visit_signups WHERE chapter_id = ? ORDER BY created_at DESC", (ch["id"],)).fetchall()
    print(f"預約參訪（{len(visits)} 筆）：" + ("、".join(
        f"{v['name']}{'（' + v['company'] + '）' if v['company'] else ''} {v['created_at'][:10]}" for v in visits) or "目前沒有"))
    if visits:
        print("（電話、Email 請到後台查看，這裡不顯示）")


def search_team(t, name):
    hits = []
    for r in t.execute("SELECT m.name, m.company_title, c.name_zh FROM chapter_members m JOIN chapters c ON c.id = m.chapter_id "
                       "WHERE m.name LIKE ?", (f"%{name}%",)):
        hits.append(f"{r['name_zh']}成員：{r['name']}（{r['company_title']}）")
    for r in t.execute("SELECT v.name, v.company, v.created_at, c.name_zh FROM visit_signups v JOIN chapters c ON c.id = v.chapter_id "
                       "WHERE v.name LIKE ?", (f"%{name}%",)):
        hits.append(f"{r['name_zh']}預約參訪：{r['name']}{'（' + r['company'] + '）' if r['company'] else ''} {r['created_at'][:10]}")
    return hits


def post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except urllib.error.HTTPError as e:
        body = e.read()
        return json.loads(body) if body else {"ok": False, "error": "網站沒有回應"}
    except urllib.error.URLError:
        return {"ok": False, "error": "第一分會網站目前連不上"}


def find_member(c, name: str):
    name = name.strip()
    rows = c.execute("SELECT * FROM members WHERE left_chapter = 0 AND name != ''").fetchall()
    exact = [r for r in rows if r["name"] == name]
    if exact:
        return exact[0], None
    partial = [r for r in rows if name in r["name"] or r["name"] in name]
    if len(partial) == 1:
        return partial[0], None
    if len(partial) > 1:
        return None, f"「{name}」對到好幾位：{'、'.join(r['name'] for r in partial)}，請說完整姓名。"
    return None, f"名單裡找不到「{name}」。目前名單：{'、'.join(r['name'] for r in rows) or '（還沒有人）'}"


def find_week(c, text: str):
    weeks = c.execute("SELECT * FROM weeks WHERE is_active = 1 ORDER BY sort_order").fetchall()
    t = text.strip()
    if t in ("本週", "這週", "今天", "最新"):
        today = date.today().isoformat()
        past = [w for w in weeks if w["week_date"] <= today]
        return (past[-1] if past else weeks[0]), None
    m = re.fullmatch(r"第?([一二三四五六七八九十]|\d+)週", t)
    if m:
        n = CN_NUM.get(m.group(1)) or int(m.group(1))
        hit = [w for w in weeks if w["label"] == f"第{'一二三四五六七八九十'[n-1]}週"] if 1 <= n <= 10 else []
        if hit:
            return hit[0], None
    m = re.fullmatch(r"(?:(\d{4})[-/])?(\d{1,2})[-/](\d{1,2})", t)
    if m:
        y = m.group(1) or str(date.today().year)
        d = f"{y}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
        hit = [w for w in weeks if w["week_date"] == d]
        if hit:
            return hit[0], None
    labels = "、".join(f"{w['label']}({w['week_date'][5:].replace('-', '/')})" for w in weeks)
    return None, f"找不到「{text}」這一週。可以填的週次：{labels}"


def cmd_list(c):
    names = [r["name"] for r in c.execute(
        "SELECT name FROM members WHERE left_chapter = 0 AND name != '' ORDER BY sort_order, id")]
    blanks = c.execute("SELECT count(*) FROM members WHERE left_chapter = 0 AND name = ''").fetchone()[0]
    print(f"第一分會名單（{len(names)} 位）：{'、'.join(names) or '還沒有人'}")
    print(f"還有 {blanks} 個空位可以新增。")


def cmd_query(c, name):
    team_hits = search_team(conn(TEAM_DB), name.strip())
    for h in team_hits:
        print(h)
    m, err = find_member(c, name)
    if err:
        if team_hits:
            print(f"（第一分會每週統計表上沒有「{name}」的紀錄）")
        else:
            print(err.replace("名單裡找不到", "五個分會和第一分會統計表裡都找不到"))
        return
    today = date.today().isoformat()
    weeks = c.execute("SELECT * FROM weeks WHERE is_active = 1 AND week_date <= ? AND week_date >= ? ORDER BY sort_order",
                      (today, m["active_from"])).fetchall()
    data = {r["week_date"]: r for r in c.execute("SELECT * FROM weekly_data WHERE member_id = ?", (m["id"],))}
    totals = {"guests": 0, "ones": 0, "coffee": 0}
    att_count = {"onsite": 0, "online": 0, "absent": 0}
    print(f"【{m['name']}】第一分會紀錄")
    for w in weeks:
        r = data.get(w["week_date"])
        g, o, cf = (r["guests"], r["ones"], r["coffee"]) if r else (None, None, None)
        a = r["attendance"] if r else None
        for k, v in (("guests", g), ("ones", o), ("coffee", cf)):
            totals[k] += v or 0
        if a in att_count:
            att_count[a] += 1
        print(f"・{w['label']}（{w['week_date'][5:].replace('-', '/')}）出席：{ATT_LABEL.get(a, a)}｜來賓 {g or 0} 人｜121 {o or 0} 次｜咖啡 {cf or 0} 場")
    print(f"合計：實體 {att_count['onsite']} 次、線上 {att_count['online']} 次、缺席 {att_count['absent']} 次；"
          f"來賓 {totals['guests']} 人、121 {totals['ones']} 次、咖啡 {totals['coffee']} 場")


def cmd_week(c, wtext):
    w, err = find_week(c, wtext)
    if err:
        print(err)
        return
    rows = c.execute(
        "SELECT m.name, d.attendance FROM members m LEFT JOIN weekly_data d ON d.member_id = m.id AND d.week_date = ? "
        "WHERE m.left_chapter = 0 AND m.name != '' ORDER BY m.sort_order, m.id", (w["week_date"],)).fetchall()
    groups = {"實體": [], "線上": [], "缺席": [], "未填": []}
    for r in rows:
        groups[ATT_LABEL.get(r["attendance"], "未填")].append(r["name"])
    print(f"【{w['label']}（{w['week_date'][5:].replace('-', '/')}）出席狀況】")
    for k, v in groups.items():
        print(f"・{k} {len(v)} 位：{'、'.join(v) if v else '—'}")


def cmd_attend(c, name, wtext, status):
    if status not in ATT:
        print(f"出席狀態只能是：實體、線上、缺席、清除（收到的是「{status}」）")
        return
    m, err = find_member(c, name)
    if err:
        print(err)
        return
    w, err = find_week(c, wtext)
    if err:
        print(err)
        return
    res = post("/api/update_attendance", {"member_id": m["id"], "week_date": w["week_date"], "value": ATT[status]})
    if res.get("ok"):
        print(f"✅ 已更新：{m['name']} {w['label']}（{w['week_date'][5:].replace('-', '/')}）→ {status if status != '清除' else '未填'}")
    else:
        print(f"❌ 沒有更新成功：{res.get('error', '原因不明')}")


def cmd_add(c, name):
    name = name.strip()
    if not name:
        print("請給一個名字")
        return
    if c.execute("SELECT 1 FROM members WHERE name = ?", (name,)).fetchone():
        print(f"「{name}」已經在名單裡了")
        return
    slot = c.execute("SELECT id FROM members WHERE left_chapter = 0 AND name = '' ORDER BY sort_order, id LIMIT 1").fetchone()
    if not slot:
        print("名單已經沒有空位了，請教練處理")
        return
    res = post("/api/update_member_name", {"member_id": slot["id"], "name": name})
    print(f"✅ 已把「{name}」加進第一分會名單" if res.get("ok") else f"❌ 沒有加成功：{res.get('error', '原因不明')}")


def main():
    a = sys.argv[1:]
    c = conn()
    if a[:1] == ["分會"] and len(a) == 1:
        cmd_chapters(conn(TEAM_DB))
    elif a[:1] == ["分會"] and len(a) == 2:
        cmd_chapter(conn(TEAM_DB), a[1])
    elif a[:1] == ["名單"] and len(a) == 1:
        cmd_list(c)
    elif a[:1] == ["查"] and len(a) == 2:
        cmd_query(c, a[1])
    elif a[:1] == ["週"] and len(a) == 2:
        cmd_week(c, a[1])
    elif a[:1] == ["出席"] and len(a) == 4:
        cmd_attend(c, a[1], a[2], a[3])
    elif a[:1] == ["新增"] and len(a) == 2:
        cmd_add(c, a[1])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
