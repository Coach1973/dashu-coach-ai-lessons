#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""預約頁「兩場訪談之間留 30 分鐘緩衝」回歸測試（教練 2026-10-19）。
只用假資料呼叫 coach_schedule_view 的純計算函式，不碰真的行程總表、不開網頁、不寫任何檔。
執行：cd event-signup && ./venv/bin/python test_coach_schedule_buffer.py"""
import datetime as dt

import coach_schedule_view as v

fails = []


def check(label, cond, detail=""):
    print(("✅" if cond else "❌"), label, "" if cond else f"→ {detail}")
    if not cond:
        fails.append(label)


def hm(*xs):
    return [v._fmt(x) for x in xs]


def slots(data, d):
    busy = v._busy(d, data)
    day, eve = v._day_slots(busy, data)
    return hm(*day), hm(*eve)


EVE = {"start": "19:00", "end": "23:00"}
BASE = {"interview_window": {"start": "10:00", "end": "23:00"}, "evening_window": EVE, "events": [], "recurring": []}
SAT = dt.date(2026, 10, 24)   # 週六
THU = dt.date(2026, 10, 22)   # 週四


def data_with(events=(), recurring=()):
    return {**BASE, "events": list(events), "recurring": list(recurring)}


def iv(start, end, kind="interview", title="榮樹下訪談"):
    return {"id": "x", "date": SAT.isoformat(), "start": start, "end": end, "title": title, "kind": kind}


# 1 全空的一天：晚上 19:00／20:30／22:00（教練原話的三場），白天 90 分鐘一格
day, eve = slots(data_with(), SAT)
check("1. 全空晚上＝19:00、20:30、22:00", eve == ["19:00", "20:30", "22:00"], eve)
check("1b. 白天 10:00 起每 90 分鐘、最晚 17:30 開始（18:30 結束，距晚上 19:00 還有 30 分）",
      day == ["10:00", "11:30", "13:00", "14:30", "16:00", "17:30"], day)
allm = sorted(v._hm(t) for t in day + eve)
check("1c. 任兩個相鄰起點相隔 ≥ 90 分鐘（一場 60＋緩衝 30）", all(b - a >= 90 for a, b in zip(allm, allm[1:])), allm)

# 2 已預約中間那場 20:30–21:30：前後各留 30 分
day, eve = slots(data_with([iv("20:30", "21:30")]), SAT)
check("2. 已有 20:30–21:30 訪談 → 晚上只剩 19:00 與 22:00", eve == ["19:00", "22:00"], eve)

# 3 已預約第一場 19:00–20:00：下一個可約是 20:30
day, eve = slots(data_with([iv("19:00", "20:00")]), SAT)
check("3. 已有 19:00–20:00 訪談 → 下一個可約 20:30、22:00", eve == ["20:30", "22:00"], eve)

# 4 一般會議（不是訪談）不加緩衝
day, eve = slots(data_with([iv("21:00", "22:00", kind=None, title="團隊會議")]), SAT)
check("4. 非訪談會議 21:00–22:00 不加緩衝 → 晚上 19:00、22:00（20:30 場會撞到會議）", eve == ["19:00", "22:00"], eve)

# 5 週四：暖身（19:00–19:30）與休息（20:30–21:00）兩列固定行程 → 19:30、21:00
thu = [{"id": "w", "weekday": 3, "start": "19:00", "end": "19:30", "title": "暖身（分享會後）"},
       {"id": "r", "weekday": 3, "start": "20:30", "end": "21:00", "title": "休息（訪談間隔）"}]
day, eve = slots(data_with(recurring=thu), THU)
check("5. 週四晚上＝19:30、21:00（BNI 會議後留 30 分暖身）", eve == ["19:30", "21:00"], eve)

# 6 週四的「線上」行程保留但不擋（舊規則沒壞）
thu_online = thu + [{"id": "o", "weekday": 3, "start": "21:00", "end": "22:30", "title": "線上聚"}]
day, eve = slots(data_with(recurring=thu_online), THU)
check("6. 週四線上聚不擋預約（訪談優先）仍是 19:30、21:00", eve == ["19:30", "21:00"], eve)

# 7 訪談判斷
check("7a. kind=interview 算訪談", v._is_interview({"kind": "interview"}))
check("7b. 標題有「訪談」算訪談", v._is_interview({"title": "入會訪談（待確認）"}))
check("7c. 有 guest 算訪談", v._is_interview({"guest": "某某"}))
check("7d. 團隊會議不算", not v._is_interview({"title": "團隊會議"}))
check("7e. 每週固定行程（休息（訪談間隔））不算訪談，不能再加一圈緩衝", not v._is_interview({"weekday": 3, "title": "休息（訪談間隔）"}))

# 8 整天行程
allday = {"id": "a", "date": SAT.isoformat(), "allday": True, "title": "出差"}
busy = v._busy(SAT, data_with([allday]))
check("8. 整天行程在 _busy 裡擋掉全部（render 另外處理）", busy and busy[0][:2] == (0, 1440), busy)

# 9 兩套算法（預約頁 vs LINE／小龍蝦 coach_schedule.py）用真實行程總表、從今天到 12/31 每一天逐日比對，必須完全一樣
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import coach_schedule as cs  # noqa: E402

real = json.loads(v.DATA.read_text(encoding="utf-8"))
d0, d1 = dt.date(2026, 10, 19), dt.date(2026, 12, 31)
diff, n_days, n_slots, back2back = [], 0, 0, []
d = d0
while d <= d1:
    page = v._day_slots(v._busy(d, real), real, d)
    line = cs.day_and_eve_starts(d, real)
    if tuple(map(list, page)) != tuple(map(list, line)):
        diff.append((d.isoformat(), page, line))
    allm = sorted(page[0] + page[1])
    n_days += 1
    n_slots += len(allm)
    if any(b - a < 90 for a, b in zip(allm, allm[1:])):
        back2back.append(d.isoformat())
    d += dt.timedelta(days=1)
check(f"9. 預約頁與 LINE 算法 {n_days} 天（到 12/31）逐日完全一致（共 {n_slots} 個時段）", not diff, diff[:2])
check("9b. 到 12/31 沒有任何一天的相鄰時段相隔不到 90 分鐘（沒有一場接一場）", not back2back, back2back[:5])

# 10 頁面本身的 JavaScript 不能有語法錯誤（2026-10-19 查到：10/13 加「取消」鈕時，\n 被 Python 變成真的換行寫進 JS 字串，
#    整支腳本失效、點時段完全沒反應，一直沒人發現）。用 node --check 檢查真正輸出的頁面。
import re
import shutil
import subprocess
import tempfile

v._refresh_google = lambda: None   # 測試不要真的去問 Google 日曆
html = v.render("test-token")
scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
if shutil.which("node") and scripts:
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(scripts[-1])
    r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
    check("10. 預約頁輸出的 JavaScript 語法正確（node --check）", r.returncode == 0, (r.stderr or "")[:200])
else:
    check("10. （這台沒有 node，略過 JS 語法檢查）", True)

# 11. 2026-10-22 教練：不再切固定格子，顯示整段空檔，來賓自己挑其中任何一個小時
def wins(data, d):
    day, eve = v._day_windows(v._busy(d, data), data)
    return [f"{v._fmt(a)}-{v._fmt(b)}" for a, b in eve]


check("11. 全空晚上＝一整段 19:00-23:00", wins(data_with(), SAT) == ["19:00-23:00"], wins(data_with(), SAT))
dd = data_with([iv("21:30", "22:30")])
check("11b. 已有 21:30–22:30 → 晚上空檔 19:00-21:00（前面留 30 分）", wins(dd, SAT) == ["19:00-21:00"], wins(dd, SAT))
eve = v._day_windows(v._busy(SAT, dd), dd)[1]
check("11c. 19:30、20:00 可約；20:30 開始會碰到緩衝 → 不可",
      v._fits(v._hm("19:30"), eve) and v._fits(v._hm("20:00"), eve) and not v._fits(v._hm("20:30"), eve))

# 12. 2026-10-23 教練：週六白天可約起點 9:30（其他天仍 10:00）；預約頁與 LINE 兩邊都要認
SAT_DATA = {**BASE, "interview_window_start_by_weekday": {"5": "09:30"}}
check("12. 週六白天從 9:30 起（預約頁）", v._day_windows(v._busy(SAT, SAT_DATA), SAT_DATA, SAT)[0][0][0] == v._hm("09:30"))
check("12b. 週六白天 9:30 起（LINE 同一套）", cs.day_and_eve_starts(SAT, SAT_DATA)[0][0] == cs.hm("09:30"))
MON = dt.date(2026, 10, 26)
check("12c. 週一白天仍 10:00 起", v._day_windows(v._busy(MON, SAT_DATA), SAT_DATA, MON)[0][0][0] == v._hm("10:00"))
check("12d. 沒帶日期時照 interview_window（舊呼叫相容）", v._day_windows([], SAT_DATA)[0][0][0] == v._hm("10:00"))

print("\n全部通過" if not fails else f"\n有 {len(fails)} 項失敗：{fails}")
raise SystemExit(1 if fails else 0)
