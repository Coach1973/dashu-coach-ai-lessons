#!/usr/bin/env python3
"""聯想電腦用：把 Comet 瀏覽器「近 75 天開過教練自家網站哪幾天」抽出來，給大樹入口（/curated/go/）排「最常用」。
2026-11-11 教練交辦：「我最常使用的是聯想電腦，用 Comet 瀏覽器重複點擊」，只看 Mac 的 Chrome 不準。

用法（在聯想的 mac-openclaw-workflows 資料夾裡）：
  py scripts\\export_comet_history.py            → 寫出 state\\browser_usage\\lenovo_comet.json
  py scripts\\export_comet_history.py --push     → 寫出後只提交這一個檔並推上雲端
  py scripts\\export_comet_history.py --history <History 檔路徑> --out <輸出路徑>   → 測試用

隱私：只留教練自家網域（OWN，跟 build_go_portal.py 同一份）的網址與日期，其他瀏覽紀錄一筆都不帶出去。
Comet 是 Chromium 核心，History 跟 Chrome 同格式；Comet 開著時檔案被鎖，所以先複製一份再讀。
"""
import argparse, collections, datetime, glob, json, os, re, shutil, sqlite3, subprocess, sys, tempfile
from pathlib import Path

OWN = ("bymyway.com", "coach1973.github.io", "claude.ai/artifact", "netlify.app", "tava-ai.com/chat")  # 跟 build_go_portal.py 一致
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "state" / "browser_usage" / "lenovo_comet.json"


def norm(u):  # 跟 build_go_portal.norm 一致
    u = re.sub(r"^https?://", "", u.strip()).split("#")[0]
    host, _, rest = u.partition("/")
    return (host + "/" + rest.partition("?")[0]).rstrip("/").lower()


def find_histories():
    base = os.environ.get("LOCALAPPDATA", "")
    pats = [os.path.join(base, "Perplexity", "Comet", "User Data", "*", "History"),
            os.path.join(base, "*", "Comet", "User Data", "*", "History"),
            os.path.join(base, "Comet", "User Data", "*", "History")]
    found = []
    for p in pats:
        for f in glob.glob(p):
            if f not in found and os.path.isfile(f):
                found.append(f)
    return found


def read(history, days, visits):
    tmp = Path(tempfile.mkdtemp()) / "History"
    shutil.copy(history, tmp)
    db = sqlite3.connect(tmp)
    cond = " or ".join("u.url like ?" for _ in OWN)
    n = 0
    for url, d in db.execute(
            "select u.url, date(v.visit_time/1000000-11644473600,'unixepoch','+8 hours') from visits v "
            f"join urls u on u.id=v.url where ({cond}) and "
            "v.visit_time/1000000-11644473600 > cast(strftime('%s','now',?) as integer)",
            [f"%{d}%" for d in OWN] + [f"-{days} days"]):
        visits[norm(url)].add(d)
        n += 1
    db.close()
    shutil.rmtree(tmp.parent, ignore_errors=True)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", action="append", help="指定 History 檔（可多個）；不給就自動找 Comet")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--days", type=int, default=75)
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()

    hs = a.history or find_histories()
    if not hs:
        sys.exit("❌ 找不到 Comet 的 History 檔（找過 %LOCALAPPDATA%\\Perplexity\\Comet\\User Data\\*\\History）。"
                 "請在 Comet 網址列打 comet://version 看「個人資料路徑」，再用 --history <該路徑>\\History 重跑。")
    visits = collections.defaultdict(set)
    for h in hs:
        print(f"讀取 {h}：{read(h, a.days, visits)} 筆自家網站開啟紀錄")
    data = {"machine": "lenovo", "browser": "Comet", "days": a.days,
            "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "visits": {k: sorted(v) for k, v in sorted(visits.items())}}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    top = sorted(visits.items(), key=lambda kv: -len(kv[1]))[:8]
    print(f"寫出 {out}：{len(visits)} 個網址")
    for k, v in top:
        print(f"  {len(v):>3} 天  {k}")

    if a.push:
        rel = str(out.resolve().relative_to(REPO))
        g = lambda *x: subprocess.run(["git", "-C", str(REPO), *x], check=True)
        g("add", rel)
        if subprocess.run(["git", "-C", str(REPO), "diff", "--cached", "--quiet", "--", rel]).returncode:
            g("commit", "-m", f"[聯想] Comet 自家網站開啟紀錄（近 {a.days} 天，{len(visits)} 個網址）", "--", rel)
            g("pull", "--rebase", "--autostash")
            g("push")
            print("✅ 已推上雲端")
        else:
            print("沒有變動，不用推")


if __name__ == "__main__":
    main()
