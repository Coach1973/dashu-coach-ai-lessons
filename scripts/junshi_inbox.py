#!/usr/bin/env python3
"""軍師待處理匣：系統自己的健康／維運通知先進這裡，由軍師（我）開工時看、自己處理，不打擾教練。
2026-11-01 教練：「小龍蝦沒事不要講一大堆我看不懂的東西……你自己內部不就處理了嗎？」

用法：
  junshi_inbox.py add <來源> <訊息>   加一筆（同來源同內容 6 小時內不重複記）
  junshi_inbox.py list                印出還沒處理的（開工 hook 用）
  junshi_inbox.py done                全部標為已處理（處理完才跑）
  junshi_inbox.py stale <小時>        有超過 N 小時沒處理的就印數量（沒有就不印）
"""
import hashlib, json, re, sys, time
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
BOX = WS / "state" / "junshi_inbox.jsonl"
DONE = WS / "state" / "junshi_inbox_done.jsonl"


def _load():
    out = []
    if BOX.exists():
        for line in BOX.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd = a[0]
    BOX.parent.mkdir(parents=True, exist_ok=True)
    if cmd == "add" and len(a) >= 3:
        src, msg = a[1], a[2]
        h = hashlib.sha1((src + msg).encode()).hexdigest()[:12]
        now = time.time()
        if any(e.get("h") == h and now - e.get("ts", 0) < 6 * 3600 for e in _load()):
            return
        # 2026-11-10 賈維斯體檢：匣子 6 天堆到 31 件，多半是「全員正常」「已自動重啟／補好」這種
        # 不用任何人處理的報平安，害開工時沒人清、還推「小事放了兩天」給教練。
        # 沒有紅黃燈的報平安直接記進已處理，不進匣子。
        if not re.search(r"🔴|🟡|⚠️|失敗|沒有|沒備份|卡住|鬼打牆", msg) and re.search(r"全員正常|已自動重啟|已自動補好", msg):
            with DONE.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": now, "t": time.strftime("%m-%d %H:%M"), "src": src, "h": h, "msg": msg, "auto": "info_only"}, ensure_ascii=False) + "\n")
            return
        with BOX.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": now, "t": time.strftime("%m-%d %H:%M"), "src": src, "h": h, "msg": msg}, ensure_ascii=False) + "\n")
    elif cmd == "list":
        es = _load()
        if not es:
            return
        print("## 🔧 小龍蝦／系統自己的通知（不要唸給教練；開工後你自己查、自己修，修完跑 `python3 scripts/junshi_inbox.py done`）")
        for e in es:
            print("- [%s｜%s] %s" % (e["t"], e["src"], e["msg"].replace("\n", " ")[:600]))
        print("教練已明講：這些他看不懂、不想被打擾。能自己修就修；只有「花錢／對外發言／不可逆」或真的需要他做決定的，才用白話一句話跟他說。")
    elif cmd == "done":
        es = _load()
        if es:
            with DONE.open("a", encoding="utf-8") as f:
                for e in es:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
        BOX.write_text("", encoding="utf-8")
    elif cmd == "stale" and len(a) >= 2:
        hrs = float(a[1])
        old = [e for e in _load() if time.time() - e.get("ts", 0) > hrs * 3600]
        if old:
            print(len(old))


main()
