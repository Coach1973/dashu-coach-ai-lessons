#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""結繩領導學・每日 LINE 行銷名單（v2）

名單來源（全部本機既有資料庫）：
  A. event-signup/event.db      attendees(369,105 有 LINE ID)、advance_registrations(50)、
                                tut_alumni_signups、leader_workshop_signups、event_1010_signups、works_contact_leads
  B. jiesheng-report/jiesheng_report.db   registrants(29，結繩工作坊報名，含台北場 20)
  C. namecard-db/namecards.db   cards(466 張名片，451 手機／7 LINE ID)、guests(3222)
  D. scripts/peers_footprints/fp_data.json  43 位人脈夥伴（無電話）

篩選（教練 2026-11-01 指示「過濾一下手機裡面的人脈」）：
  排除：教練本人／自家團隊／台北場已報名／電話重複／無任何聯絡方式／測試資料
  保留：企業主、高階主管、曾報名活動者、結繩工作坊報名者
  分流：line_id 有 → 機器人可推（LINE 官方帳號）；只有手機 → 教練手機手動發

輸出：state/jiesheng_marketing.json
"""
import argparse, json, re, sqlite3
from datetime import date, datetime
from pathlib import Path

WS = Path("/Users/bymyway/.openclaw/workspace")
ES_DB = WS / "event-signup/event.db"
JS_DB = WS / "jiesheng-report/jiesheng_report.db"
NC_DB = WS / "namecard-db/namecards.db"
FP = WS / "scripts/peers_footprints/fp_data.json"
STATE = WS / "state/jiesheng_marketing.json"
SENT_LOG = WS / "state/jiesheng_sent_log.jsonl"

DAILY_BATCH = 15          # 每日機器人推播上限（LINE 月配額 200，留 30 則安全線）
QUOTA_RESERVE = 30       # LINE 月配額保留線（沿用 event-signup 的 LINE_FORWARD_MIN_QUOTA）
PHONE_ROTATE_SIZE = 40   # 每日給教練手機手動發送的人數（10 分鐘約可發 40 則）
PHONE_START = "2026-11-01"
WORKSHOP = "台北"

SELF_NAMES = {"吳大樹", "大樹教練", "大樹", "吳大樹教練", "coach wu", "王大樹"}

# 高階決策者關鍵字（教練「人脈」篩選核心：企業主／主管才可能帶團隊來上課）
BOSS_KW = ("老闆", "董事長", "總裁", "創辦人", "總經理", "執行長", "經營者", "合夥人",
           "主理人", "總監", "副總", "總監", "經理", "組長", "隊長", "leader", "ceo",
           "owner", "founder", "president", "director", "manager", "總部", "廠長", "店長")
TEST_KW = ("測試", "test", "TEST", "示範", "範例", "假", "dummy", "asdf", "123")


def ro(p):
    try:
        return sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    except Exception:
        return None


def norm_phone(p):
    if not p:
        return ""
    d = re.sub(r"\D", "", str(p))
    if len(d) == 9 and d.startswith("9"):
        d = "0" + d
    if len(d) == 8 and d.startswith("7"):
        d = "0" + d
    return d if len(d) >= 9 else ""


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def collect():
    cand, excl = {}, []
    sent = load_state().get("sent", {}) or {}

    def put(name, phone, line_id, source, email="", title="", company="", note=""):
        name = (name or "").strip()
        phone = norm_phone(phone)
        if not name and not phone:
            return
        key = phone or ("fp:" + name)
        rec = cand.get(key)
        if rec is None:
            rec = {"name": name, "phone": phone, "line_id": (line_id or "").strip(),
                   "email": (email or "").strip(), "title": (title or "").strip(),
                   "company": (company or "").strip(), "note": note or "", "sources": []}
            cand[key] = rec
        else:
            if not rec["line_id"] and line_id:
                rec["line_id"] = line_id.strip()
            if not rec["email"] and email:
                rec["email"] = email.strip()
            if not rec["title"] and title:
                rec["title"] = title.strip()
            if not rec["company"] and company:
                rec["company"] = company.strip()
        if source not in rec["sources"]:
            rec["sources"].append(source)

    # ── A. event-signup ──
    c = ro(ES_DB)
    if c:
        for n, p, l, t in c.execute(
                "SELECT name, phone, line_user_id, company_title FROM attendees"):
            put(n, p, l, "活動報名", title=t or "")
        for n, p, e, comp in c.execute(
                "SELECT name, phone, email, company FROM advance_registrations"):
            put(n, p, None, "預約報名", email=e or "", company=comp or "")
        for tbl in ("tut_alumni_signups", "leader_workshop_signups", "event_1010_signups"):
            try:
                for n, p in c.execute(f"SELECT name, phone FROM {tbl}"):
                    put(n, p, None, "學員名單")
            except Exception:
                pass
        # 台南商圈：欄位是 shop/contact（店家負責人），不是 name/phone
        try:
            for shop, contact, cat in c.execute(
                    "SELECT shop, contact, category FROM tainan_shangquan_signups"):
                put(contact, None, None, "台南商圈", title=cat or "", company=shop or "")
        except Exception:
            pass
        try:
            for n, p, e in c.execute("SELECT name, phone, email FROM works_contact_leads"):
                put(n, p, None, "企業合作名單", email=e or "")
        except Exception:
            pass
        c.close()

    # ── B. 結繩工作坊報名 ──
    c = ro(JS_DB)
    if c:
        for w, n, p, paid, ref in c.execute(
                "SELECT workshop, name, phone, paid, referrer FROM registrants"):
            put(n, p, None, f"結繩工作坊報名({w})",
                note=f"邀請人:{ref or '-'}／繳費:{'已繳' if paid else '未繳'}")
            if w == WORKSHOP:
                excl.append({"name": n, "phone": norm_phone(p),
                             "reason": f"結繩台北場已報名（{'已繳' if paid else '未繳'}）→ 走成交付不重複行銷"})
        c.close()

    # ── C. 名片資料庫 ──
    c = ro(NC_DB)
    if c:
        for n, m, l, t, comp, cat in c.execute(
                "SELECT name, mobile, line_id, title, company, category FROM cards"):
            put(n, m, l, "名片", title=t or "", company=comp or "", note=cat or "")
        for n, m, e, comp, prof in c.execute(
                "SELECT name, mobile, email, company, profession FROM guests"):
            put(n, m, None, "來賓名單", email=e or "", title=prof or "", company=comp or "")
        c.close()

    # ── D. 人脈足跡夥伴 ──
    if FP.exists():
        try:
            for r in json.loads(FP.read_text(encoding="utf-8")):
                put(r.get("name"), None, None, "人脈足跡夥伴", title=r.get("role") or "")
        except Exception:
            pass

    return list(cand.values()), excl, sent


def team_names():
    out = set()
    c = ro(ES_DB)
    if c:
        for tbl in ("tut_team_members", "nmda_team_members", "team_members"):
            try:
                for (n,) in c.execute(f"SELECT name FROM {tbl}"):
                    if n:
                        out.add(n.strip())
            except Exception:
                pass
        c.close()
    return out


def build():
    state = load_state()
    sent = state.get("sent", {}) or {}
    cand, excl, _ = collect()
    team = team_names()

    final, ex, seen = [], list(excl), {}
    for r in cand:
        name, phone = r["name"], r["phone"]
        blob = f"{name}{r['title']}{r['company']}{r['note']}{r['email']}"
        if not name or any(k in blob for k in TEST_KW):
            ex.append({"name": name, "phone": phone, "reason": "測試／無效資料"}); continue
        if name in SELF_NAMES or "大樹教練" in name:
            ex.append({"name": name, "phone": phone, "reason": "教練本人"}); continue
        if name in team:
            ex.append({"name": name, "phone": phone, "reason": "自家團隊成員"}); continue
        if phone and phone in seen:
            ex.append({"name": name, "phone": phone, "reason": f"電話重複（與 {seen[phone]} 同人）"}); continue
        if phone:
            seen[phone] = name
        if not phone and not r["line_id"] and not r["email"]:
            ex.append({"name": name, "phone": "", "reason": "無任何聯絡方式"}); continue
        if phone in sent or ("fp:" + name) in sent:
            r["sent_on"] = sent.get(phone) or sent.get("fp:" + name)
        final.append(r)

    def score(r):
        s = 0
        if r["line_id"]:
            s += 45
        if any("工作坊報名" in x for x in r["sources"]):
            s += 38
        if any("預約報名" in x or "學員名單" in x for x in r["sources"]):
            s += 22
        if any(k in (r["title"] or "") for k in BOSS_KW):
            s += 20
        if r["company"]:
            s += 8
        if any("名片" in x for x in r["sources"]):
            s += 10
        if any("企業合作名單" in x for x in r["sources"]):
            s += 6
        if any("人脈足跡" in x for x in r["sources"]):
            s += 12
        if r["email"]:
            s += 3
        return s

    final.sort(key=lambda r: (-score(r), r["name"]))
    for r in final:
        r["score"] = score(r)
        r["channel"] = "bot" if r["line_id"] else ("phone" if r["phone"] else "email")

    todo = [r for r in final if not r.get("sent_on")]
    bot_all = [r for r in todo if r["channel"] == "bot"]
    phone_all = [r for r in todo if r["channel"] == "phone"]

    # ── 教練手動發送名單：每日輪轉，保證「全部的人都要發完」且不重複轟炸 ──
    # 以起始日為基準算第幾天，每天往後推進 PHONE_ROTATE_SIZE 位。
    start = date(2026, 11, 1)
    day_idx = max(0, (date.today() - start).days)
    rot = (day_idx * PHONE_ROTATE_SIZE) % len(phone_all) if phone_all else 0
    phone_batch = (phone_all[rot:] + phone_all[:rot])[:PHONE_ROTATE_SIZE] if phone_all else []

    data = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "workshop": "結繩領導學・台北場 11/25-26",
        "signup_url": "https://rplconstw.pse.is/Taipei1125",
        "daily_batch_size": DAILY_BATCH,
        "quota_reserve": QUOTA_RESERVE,
        "today_bot_batch": bot_all[:DAILY_BATCH],
        "today_phone_batch": phone_batch,
        "phone_rotation": {"day_index": day_idx, "offset": rot,
                           "rotate_size": PHONE_ROTATE_SIZE, "pool": len(phone_all)},
        "candidates": final,
        "excluded": ex,
        "sent": sent,
        "stats": {
            "總候選": len(final),
            "機器人可推(有LINE ID)": len([r for r in final if r["channel"] == "bot"]),
            "教練手機手動發(只有手機)": len([r for r in final if r["channel"] == "phone"]),
            "只有Email": len([r for r in final if r["channel"] == "email"]),
            "已發過": len([r for r in final if r.get("sent_on")]),
            "待發": len(todo),
            "排除": len(ex),
        },
    }
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


def mark_sent(phones=(), names=()):
    if not STATE.exists():
        print("尚無名單檔，先跑 --build"); return
    d = json.loads(STATE.read_text(encoding="utf-8"))
    sent = d.setdefault("sent", {})
    today = date.today().isoformat()
    hit = 0
    for r in d["candidates"]:
        if (phones and r["phone"] in phones) or (names and r["name"] in names):
            k = r["phone"] or ("fp:" + r["name"])
            sent[k] = today
            hit += 1
    d["sent"] = sent
    STATE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    with SENT_LOG.open("a", encoding="utf-8") as f:
        for r in d["candidates"]:
            k = r["phone"] or ("fp:" + r["name"])
            if sent.get(k) == today and (phones and r["phone"] in phones or names and r["name"] in names):
                f.write(json.dumps({"date": today, "name": r["name"], "phone": r["phone"],
                                    "channel": r["channel"]}, ensure_ascii=False) + "\n")
    print(f"已標記 {hit} 位為已發（{today}）")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--today", action="store_true")
    ap.add_argument("--mark-sent", nargs="*", default=None)
    ap.add_argument("--name", action="append", default=None)
    ap.add_argument("--phone-sheet", action="store_true")
    a = ap.parse_args()
    if a.phone_sheet:
        if not STATE.exists():
            build()
        d = json.loads(STATE.read_text(encoding="utf-8"))
        batch = d["today_phone_batch"]
        stamp = date.today().strftime("%Y%m%d")
        txt = WS / f"state/jiesheng_phone_sheet_{stamp}.txt"
        csv = WS / f"state/jiesheng_phone_sheet_{stamp}.csv"
        lines = [f"結繩領導學・台北場 11/25-26　報名：{d['signup_url']}",
                 f"憑書報名 NT$10,000（原價 16,800）｜劍潭青年活動中心",
                 f"教練手機手動發送名單｜{date.today()}　共 {len(batch)} 位",
                 "（每日 12:15 提醒，發完這份名單就好；下一批自動輪轉）", "=" * 60]
        for i, r in enumerate(batch, 1):
            tag = r["title"][:12] if r["title"] else ""
            co = r["company"][:14] if r["company"] else ""
            lines.append(f"{i:2}. {r['name']:14} {r['phone']:12} {tag:12} {co}")
        txt.write_text("\n".join(lines), encoding="utf-8")
        with csv.open("w", encoding="utf-8-sig") as f:
            f.write("序號,姓名,手機,職稱,公司\n")
            for i, r in enumerate(batch, 1):
                f.write(f"{i},{r['name']},{r['phone']},{r['title']},{r['company']}\n")
        rot = d.get("phone_rotation", {})
        print(f"=== 教練手機手動發送名單（{len(batch)} 位）===")
        for i, r in enumerate(batch, 1):
            print(f"{i:2}. {r['name']:16} {r['phone']:12} {r['title'][:10]:10} {r['company'][:12]}")
        print(f"  檔案：{txt}")
        print(f"  檔案：{csv}")
        print(f"  輪轉：第 {rot.get('day_index',0)+1} 天／名單池 {rot.get('pool',0)} 位／每日 {rot.get('rotate_size',0)} 位")
    elif a.mark_sent is not None:
        mark_sent(set(a.mark_sent or []), set(a.name or []))
    elif a.today:
        if not STATE.exists():
            build()
        d = json.loads(STATE.read_text(encoding="utf-8"))
        print(f"=== 機器人批次（{len(d['today_bot_batch'])} 位）===")
        for i, r in enumerate(d["today_bot_batch"], 1):
            print(f"{i:2}. {r['name']:16} {r['phone']:12} {r['title'][:10]:10} | {'、'.join(r['sources'])}")
        print(f"\n=== 教練手機手動發（今日建議 {len(d['today_phone_batch'])} 位／待發 "
              f"{d['stats']['教練手機手動發(只有手機)']} 位）===")
        for i, r in enumerate(d["today_phone_batch"][:20], 1):
            print(f"{i:2}. {r['name']:16} {r['phone']:12} {r['title'][:10]:10} {r['company'][:12]}")
    else:
        d = build()
        print("=== 名單統計 ===")
        for k, v in d["stats"].items():
            print(f"  {k}: {v}")
        print(f"  輸出：{STATE}")
