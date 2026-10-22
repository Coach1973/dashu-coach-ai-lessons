"""官網預約自動占位的測試。不碰真資料（行程總表換成暫存複本）、不發任何通知、不寫資料庫、不動 Google 日曆。
執行：cd event-signup && set -a; source .env; set +a; venv/bin/python test_rongtree_hold.py"""
import datetime as dt
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "scripts"))

import coach_schedule_view as v  # noqa: E402

tmp = Path(tempfile.mkdtemp())
data_copy = tmp / "教練行程總表.json"
shutil.copy(v.DATA, data_copy)
v.DATA = data_copy                 # 全部改打暫存複本
v._refresh_google = lambda: None   # book() 開頭會去讀 Google 日曆並寫回正式總表，測試不要

import app as A  # noqa: E402
import coach_schedule as cs  # noqa: E402

cs.DATA = str(data_copy)

events = []
A._rongtree_hold_notify = lambda t: events.append(("notify", t))
A._rongtree_hold_record_lead = lambda *a, **k: events.append(("lead", a))
A._rongtree_hold_push_google = lambda: events.append(("google",))
A.app.config["TESTING"] = True
client = A.app.test_client()

fails = []


def check(label, cond, detail=""):
    print(("✅ " if cond else "❌ ") + label, "" if cond else f"→ {detail}")
    if not cond:
        fails.append(label)


def load():
    return json.loads(data_copy.read_text(encoding="utf-8"))


def post(payload, ip="1.2.3.4"):
    r = client.post("/api/rongtree/hold", json=payload, headers={"CF-Connecting-IP": ip})
    return r.status_code, (r.get_json() or {})


def first_free_evening(skip=0):
    data = load()
    n = 0
    for i in range(1, 25):
        d = dt.datetime.now(v.TZ).date() + dt.timedelta(days=i)
        busy = v._busy(d, data)
        if any((s, e) == (0, 1440) for s, e, _ in busy):
            continue
        for a, b in v._day_windows(busy, data)[1]:
            if b - a >= v.SESSION:
                if n == skip:
                    return d, a
                n += 1
    raise SystemExit("找不到可測試的空檔")


d, a = first_free_evening()
hm = v._fmt(a)
base = {"date": d.isoformat(), "start": hm, "name": "測試先生", "org": "測試公司", "contact": "0912345678", "msg": "測試留言"}

# 1. 成功占位
A._RONGTREE_HOLD_HITS.clear()
st, j = post(base)
time.sleep(0.4)
check("1. 送出一個空檔 → 200、held=true", st == 200 and j.get("ok") and j.get("held"), (st, j))
ev = next((e for e in load()["events"] if e.get("booked_by") == "官網預約"), None)
check("1b. 總表多一筆「待確認」榮樹下訪談（booked_by=官網預約、tentative）", bool(ev) and ev.get("tentative") and ev.get("booking_type") == "榮樹下訪談", ev)
check("1c. 姓名單位聯絡方式只在私人備註；沒有 guest 欄位（公開清單不會出現姓名）",
      bool(ev) and "測試先生" in ev.get("note", "") and "guest" not in ev and "測試先生" not in ev.get("booked_by", ""), ev)
kinds = [k[0] for k in events]
check("1d. 有通知、留資料紀錄、寫 Google 各一次", kinds.count("notify") == 1 and kinds.count("lead") == 1 and kinds.count("google") == 1, kinds)
note_text = next((e[1] for e in events if e[0] == "notify"), "")
check("1e. 通知含時間、姓名、確認預約／取消預約指令", "測試先生" in note_text and "確認預約" in note_text and "取消預約" in note_text and hm in note_text, note_text)

# 2. 占位後空檔消失（含前後 30 分緩衝）
data = load()
win = v._day_windows(v._busy(d, data), data)[1]
check("2. 被占的那一小時不再是空檔", not v._fits(a, win), win)
check("2b. 緊接著的下一小時（離訪談不到 30 分）也不行", not v._fits(a + 60, win), win)

# 3. 同一小時再送 → 搶不到
events.clear()
st, j = post(base, ip="5.6.7.8")
check("3. 同一小時再送 → 409 code=taken、不通知", st == 409 and j.get("code") == "taken" and not events, (st, j, events))

# 4. 必填、格式、機器人
st, j = post({**base, "name": ""}, ip="9.9.9.1")
check("4. 沒填姓名 → 400", st == 400, (st, j))
st, j = post({**base, "contact": "abc"}, ip="9.9.9.2")
check("4b. 聯絡方式不正確 → 400", st == 400, (st, j))
n_before = len(load()["events"])
st, j = post({**base, "website": "http://spam"}, ip="9.9.9.3")
check("4c. 機器人隱藏欄位有字 → 假裝成功但不占位、不通知", st == 200 and j.get("held") is False and len(load()["events"]) == n_before and not events, (st, j))

# 5. 取消後空檔恢復（用既有的取消機制）
data = load()
label_err = cs.cancel_item(data, ev["id"], None)
cs.save(data)
data = load()
win = v._day_windows(v._busy(d, data), data)[1]
check("5. 取消這筆預約後，那一小時恢復成空檔", label_err[1] is None and v._fits(a, win), (label_err, win))

# 6. 同時待確認上限（6 筆）→ 409 code=full，不占位
data = load()
for i in range(6):
    dd = dt.datetime.now(v.TZ).date() + dt.timedelta(days=2 + i)
    data["events"].append({"id": f"cap{i}", "date": dd.isoformat(), "start": "10:00", "end": "11:00", "title": "榮樹下訪談（待確認）",
                           "source": "預約頁", "kind": "interview", "tentative": True, "booking_type": "榮樹下訪談", "booked_by": "官網預約"})
data_copy.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
events.clear()
n_before = len(load()["events"])
st, j = post(base, ip="8.8.8.8")
check("6. 官網待確認已滿 6 筆 → 409 code=full、不占位", st == 409 and j.get("code") == "full" and len(load()["events"]) == n_before and not events, (st, j))

# 7. 同一個 IP 每小時最多 4 次
A._RONGTREE_HOLD_HITS.clear()
# 欄位正確才會計次（無效請求沒有副作用）；用不存在的時段 03:00，每次都會是 409，但都算一次
data_copy.write_text(json.dumps({**load(), "events": [e for e in load()["events"] if not str(e.get("id", "")).startswith("cap")]}, ensure_ascii=False), encoding="utf-8")
codes = [post({**base, "start": "03:00"}, ip="7.7.7.7")[0] for _ in range(5)]
check("7. 同一個 IP 每小時最多 4 次：第 5 次起 → 429", codes[:4] == [409] * 4 and codes[4] == 429, codes)

# 8. 預約頁原本的 book() 不受影響（不帶 who/note）
ok, res = v.book(d.isoformat(), hm, "咖啡會議")
check("8. 預約頁原本的預約（咖啡會議）照舊：預約人＝陳佩君老師", ok and res["booked_by"] == "陳佩君老師" and res["note"].startswith("預約人：陳佩君老師"), (ok, res))

print("\n全部通過" if not fails else f"\n有 {len(fails)} 項失敗：{fails}")
raise SystemExit(1 if fails else 0)
