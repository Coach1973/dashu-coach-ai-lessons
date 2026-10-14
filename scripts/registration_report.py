#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""報名人數統計／報名表產出（教練 2026-08-23 交辦，2026-08-24 建置）

教練原話：「之後問幾個人報名，你全部統計給我，不用手動算，要做成報名表。」
以前每次問都要有人去 join 三張表手算，現在一行指令就出來。

資料來自 event-signup/event.db 兩個來源，會分開標示不混為一談：
  · signups + attendees ── 2026-08-14 雙寫上線後，官網/微站報名即時寫進來的
  · advance_registrations ── 8/14 之前只活在 LINE 通知文字裡、事後補登的歷史名單

用法：
  python3 scripts/registration_report.py                    # 所有未來場次的人數總覽
  python3 scripts/registration_report.py --all              # 含已結束場次
  python3 scripts/registration_report.py 0828               # 某場的完整報名表（可用日期/slug/名稱關鍵字）
  python3 scripts/registration_report.py 0828 --csv         # 順便輸出 CSV 給教練列印簽到表
  python3 scripts/registration_report.py --notify           # 把總覽發到教練 Telegram
"""

import csv
import json
import os
import sqlite3
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
EVENT_DB = os.path.join(WORKSPACE, "event-signup", "event.db")
OUT_DIR = os.path.join(WORKSPACE, "state", "registration_reports")
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
COACH_CHAT_ID = "6124913915"
TPE = timezone(timedelta(hours=8))


def conn():
    c = sqlite3.connect(EVENT_DB)
    c.row_factory = sqlite3.Row
    return c


def today():
    return datetime.now(TPE).strftime("%Y-%m-%d")


def fetch_events(c, include_past: bool):
    rows = c.execute(
        "SELECT id, slug, name, event_date, start_time, location, venue, status FROM events"
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["is_past"] = bool(d["event_date"]) and d["event_date"] < today()
        if d["is_past"] and not include_past:
            continue
        out.append(d)
    out.sort(key=lambda x: (x["event_date"] or "9999", x["start_time"] or ""))
    return out


# 這些不是真的活動報名，統計時要排除，不然人數會虛胖
EXCLUDE_LABEL_MARKERS = ("系統測試", "請忽略", "百人導師申請")


def _legacy_rows(c):
    """歷史補登名單（8/14 雙寫上線前只活在 LINE 通知文字裡的那批），先濾掉非報名資料。"""
    rows = c.execute(
        """SELECT name, phone, company AS company_title, email, session_label,
                  '—' AS line_bound, registered_at AS created_at
             FROM advance_registrations ORDER BY registered_at"""
    ).fetchall()
    return [dict(r) for r in rows
            if not any(m in (r["session_label"] or "") for m in EXCLUDE_LABEL_MARKERS)]


def _match_legacy(ev, legacy_all, same_date_events):
    """把歷史補登對到場次。

    ⚠️ 這裡有兩個真實踩到的坑，改動前先看懂：
      ① 場次字串寫的是「8/26」不是「08/26」——直接拿 event_date 切出來的 MM/DD 比對會全部落空
      ② 同一天可能有兩場（8/26 早上晨光美學＋下午古典音樂、9/22 午半＋晚半），
         只比日期會讓同一批人被兩場各算一次，人數直接翻倍。
    所以：先比日期，同一天有多場時再用時間（14:00 這種）分流；
    分不出來的老實列為「無法分辨場次」，不硬塞給任何一場，也不重複計算。
    """
    if not ev["event_date"]:
        return [], []
    _, mm, dd = ev["event_date"].split("-")
    date_keys = {f"{int(mm)}/{int(dd)}", f"{mm}/{dd}"}
    on_date = [r for r in legacy_all
               if any(k in (r["session_label"] or "") for k in date_keys)]
    if len(same_date_events) <= 1:
        return on_date, []

    hhmm = (ev["start_time"] or "")[:5]
    mine = [r for r in on_date if hhmm and hhmm in (r["session_label"] or "")]
    matched_by_any = {id(r) for e in same_date_events
                      for r in on_date
                      if (e["start_time"] or "")[:5] and (e["start_time"] or "")[:5] in (r["session_label"] or "")}
    unassigned = [r for r in on_date if id(r) not in matched_by_any]
    return mine, unassigned


def count_for(c, ev, legacy_all, same_date_events):
    live = c.execute(
        "SELECT COUNT(*) FROM signups WHERE event_id = ?", (ev["id"],)
    ).fetchone()[0]
    mine, unassigned = _match_legacy(ev, legacy_all, same_date_events)
    return live, len(mine), len(unassigned)


def party_size(company_title):
    """報名表「出席人數」下拉選單（1人/2人/3人/4人以上）存在 attendees.company_title。
    回傳 (人數, 是否只是下限)。「4人以上」只能當 4 人下限算，不能當 1 人（10/13 漏算事件）。
    沒填或不是人數格式（舊版表單這欄放公司職稱）→ 當 1 人，並標為未知。"""
    import re
    m = re.fullmatch(r"\s*(\d+)\s*人(以上)?\s*", company_title or "")
    if not m:
        return 1, False, True
    return int(m.group(1)), bool(m.group(2)), False


def headcount(rows):
    """rows 需含 company_title。回傳 (總人數下限, 有幾筆是『N人以上』)。"""
    total = at_least = 0
    for r in rows:
        n, is_min, _unknown = party_size(r["company_title"])
        total += n
        at_least += 1 if is_min else 0
    return total, at_least


def live_headcount(c, ev):
    rows = c.execute(
        """SELECT a.company_title FROM signups s JOIN attendees a ON a.id = s.attendee_id
            WHERE s.event_id = ?""", (ev["id"],)).fetchall()
    return headcount(rows)


def head_note(total, at_least, n):
    """含同行人數的說明字串；跟筆數一樣就不囉嗦。"""
    if total == n and not at_least:
        return ""
    return f"（含同行{'至少 ' if at_least else '共 '}{total} 人" + (f"，其中 {at_least} 筆填『N人以上』只按下限算" if at_least else "") + "）"


def roster(c, ev, legacy_all, same_date_events):
    live = c.execute(
        """SELECT a.name, a.phone, a.company_title, a.email,
                  CASE WHEN a.line_user_id IS NULL OR a.line_user_id='' THEN '否' ELSE '是' END AS line_bound,
                  s.created_at
             FROM signups s JOIN attendees a ON a.id = s.attendee_id
            WHERE s.event_id = ? ORDER BY s.created_at""",
        (ev["id"],),
    ).fetchall()
    mine, unassigned = _match_legacy(ev, legacy_all, same_date_events)
    return [dict(r) for r in live], mine, unassigned


def notify(text: str) -> bool:
    try:
        with open(OPENCLAW_CONFIG, encoding="utf-8") as f:
            cfg = json.load(f)
        token = cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        body = json.dumps({"chat_id": COACH_CHAT_ID, "text": text}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=body, method="POST", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()).get("ok", False)
    except Exception as e:
        print(f"⚠️ Telegram 通知失敗：{e}", file=sys.stderr)
        return False


def summary(c, include_past: bool):
    events = fetch_events(c, include_past)
    all_events = fetch_events(c, include_past=True)
    legacy_all = _legacy_rows(c)
    by_date = {}
    for e in all_events:
        by_date.setdefault(e["event_date"], []).append(e)

    lines, total, pending = [], 0, 0
    for ev in events:
        live, legacy, unassigned = count_for(c, ev, legacy_all, by_date.get(ev["event_date"], []))
        n = live + legacy
        total += n
        pending = max(pending, 0)
        extra = f"（線上 {live}＋歷史 {legacy}）" if legacy else ""
        hc, hc_min = live_headcount(c, ev)
        extra += head_note(hc, hc_min, live)
        if unassigned:
            extra += f" ⚠️另有 {unassigned} 筆同日報名分不出場次"
        when = f"{ev['event_date'] or '日期未定'} {ev['start_time'] or ''}".strip()
        where = ev.get("location") or ev.get("venue") or ""
        mark = "🔚" if ev["is_past"] else ("🔥" if n else "　")
        lines.append(f"{mark} {when}｜{ev['name']}{('｜' + where) if where else ''}　→ {n} 人{extra}")
    return events, lines, total


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    include_past = "--all" in flags
    c = conn()

    if not args:
        events, lines, total = summary(c, include_past)
        header = f"📋 大樹小講報名統計（{datetime.now(TPE).strftime('%Y-%m-%d %H:%M')}）"
        print(header)
        print(f"{'所有' if include_past else '未來'}場次 {len(events)} 場，合計 {total} 人\n")
        for ln in lines:
            print(ln)
        print("\n想看某一場完整名單：python3 scripts/registration_report.py 0828")
        if "--notify" in flags:
            notify(header + f"\n{'所有' if include_past else '未來'}場次 {len(events)} 場，合計 {total} 人\n\n"
                   + "\n".join(lines))
        c.close()
        return 0

    # 指定場次：日期(0828/2026-08-28)、slug、或名稱關鍵字都能找
    kw = args[0]
    events = fetch_events(c, include_past=True)
    matched = [e for e in events if kw in (e["slug"] or "")
               or kw in (e["event_date"] or "").replace("-", "")
               or kw in (e["name"] or "")]
    if not matched:
        print(f"❌ 找不到符合「{kw}」的場次。目前有：")
        for e in events:
            print(f"   · {e['event_date']}｜{e['slug']}｜{e['name']}")
        c.close()
        return 2

    legacy_all = _legacy_rows(c)
    by_date = {}
    for e in events:
        by_date.setdefault(e["event_date"], []).append(e)

    for ev in matched:
        live, legacy, unassigned = roster(c, ev, legacy_all, by_date.get(ev["event_date"], []))
        n = len(live) + len(legacy)
        print(f"\n═══ {ev['event_date']} {ev['start_time'] or ''}｜{ev['name']} ═══")
        print(f"場地：{ev.get('venue') or ev.get('location') or '未填'}｜場次代碼：{ev['slug']}")
        print(f"報名人數：{n} 人" + (f"（線上 {len(live)}＋歷史補登 {len(legacy)}）" if legacy else ""))
        hc, hc_min = headcount(live)
        if head_note(hc, hc_min, len(live)):
            print(head_note(hc, hc_min, len(live))[1:-1])
        if unassigned:
            print(f"⚠️ 另有 {len(unassigned)} 筆同一天的歷史報名看不出是哪一場（沒寫時間），沒有算進上面的數字：")
            for r in unassigned:
                print(f"     · {r['name']}／{r['phone'] or '無電話'}　原始場次文字：{r['session_label']}")
        rows = live + legacy
        if not rows:
            print("（目前還沒有人報名）")
            continue

        # 同一支電話報兩次＝很可能是同一個人（2026-08-14 就發生過 gl t86／燒茶同號的狀況）。
        # 教練要拿這份去訂便當、排座位，人數不準會直接出事，所以主動點出來讓他判斷。
        seen = {}
        for r in rows:
            p = (r.get("phone") or "").strip()
            if p:
                seen.setdefault(p, []).append(r.get("name") or "")
        dups = {p: ns for p, ns in seen.items() if len(ns) > 1}
        if dups:
            print(f"⚠️ 有 {len(dups)} 組電話重複，可能是同一人報兩次（實際人數可能是 {n - sum(len(v) - 1 for v in dups.values())} 人）：")
            for p, ns in dups.items():
                print(f"     · {p} → {'、'.join(ns)}")
        print(f"\n{'#':>3} {'姓名':<10} {'電話':<12} {'公司／職稱':<18} {'LINE':<4} 報名時間")
        print("─" * 78)
        for i, r in enumerate(rows, 1):
            print(f"{i:>3} {(r['name'] or '')[:10]:<10} {(r['phone'] or ''):<12} "
                  f"{(r['company_title'] or '-')[:18]:<18} {r['line_bound']:<4} {(r['created_at'] or '')[:16]}")

        if "--csv" in flags:
            os.makedirs(OUT_DIR, exist_ok=True)
            path = os.path.join(OUT_DIR, f"報名表_{ev['slug']}_{datetime.now(TPE).strftime('%Y%m%d-%H%M')}.csv")
            with open(path, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(["序號", "姓名", "電話", "公司／職稱", "Email", "已綁LINE", "報名時間", "簽到"])
                for i, r in enumerate(rows, 1):
                    w.writerow([i, r["name"], r["phone"], r["company_title"] or "",
                                r["email"] or "", r["line_bound"], (r["created_at"] or "")[:16], ""])
            print(f"\n📄 已輸出可列印的簽到表：{path}")

    c.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
