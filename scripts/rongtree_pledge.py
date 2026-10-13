#!/usr/bin/env python3
"""榮樹下「樹蔭席」承諾牆（2026-10-14 教練構想）：每集 3～5 位樹蔭席嘉賓聽完故事，承諾自己能出的一份力，
掛成一片葉子；做到了變金色，並記入真公益足跡。

資料＝~/github_repos/rongtree/pledges.json（網頁 /curated/rongtree/#seats 直接讀），改完自動 commit＋push。

  rongtree_pledge.py add --name 王小明 --org "某某宮 主委" --what "在 30 間廟宇張貼路跑報名資訊" [--episode "EP.06 張麗蝶"]
  rongtree_pledge.py done --id p3          # 標記已做到（金色葉子）
  rongtree_pledge.py undo --id p3          # 改回承諾中
  rongtree_pledge.py remove --id p3        # 刪除（登錯時用）
  rongtree_pledge.py list
加 --no-push 只改檔不上傳（測試用）。
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("RONGTREE_REPO") or Path.home() / "github_repos" / "rongtree")
FILE = REPO / "pledges.json"


def load():
    try:
        return json.loads(FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"pledges": []}


def save(d, msg, push=True):
    FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not push:
        return
    subprocess.run(["git", "-C", str(REPO), "add", "pledges.json"], check=True)
    subprocess.run(["git", "-C", str(REPO), "commit", "-q", "-m", f"[Mac] 樹蔭席承諾牆：{msg}"], check=True)
    r = subprocess.run(["git", "-C", str(REPO), "push", "-q"], capture_output=True, text=True)
    print("✅ 已上傳 GitHub" if r.returncode == 0 else f"⚠️ 網頁已更新，但上傳 GitHub 失敗：{r.stderr.strip()[:200]}")


def find(d, pid):
    hit = [p for p in d["pledges"] if p["id"] == pid]
    if not hit:
        sys.exit(f"找不到承諾 {pid}（用 list 看編號）")
    return hit[0]


def main():
    ap = argparse.ArgumentParser(description="榮樹下樹蔭席承諾牆")
    ap.add_argument("--no-push", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--name", required=True)
    a.add_argument("--org", default="")
    a.add_argument("--what", required=True)
    a.add_argument("--episode", default="")
    for c in ("done", "undo", "remove"):
        sub.add_parser(c).add_argument("--id", required=True)
    sub.add_parser("list")
    args = ap.parse_args()
    d = load()
    push = not args.no_push

    if args.cmd == "add":
        n = max([int(p["id"][1:]) for p in d["pledges"]] + [0]) + 1
        p = {"id": f"p{n}", "name": args.name.strip()[:30], "org": args.org.strip()[:40], "what": args.what.strip()[:120],
             "episode": args.episode.strip()[:40], "status": "promised", "date": dt.date.today().isoformat()}
        d["pledges"].append(p)
        save(d, f"新增 {p['name']} 的承諾", push)
        print(f"🍃 已掛上葉子 {p['id']}：{p['name']}——{p['what']}")
    elif args.cmd in ("done", "undo"):
        p = find(d, args.id)
        p["status"] = "done" if args.cmd == "done" else "promised"
        if args.cmd == "done":
            p["done_date"] = dt.date.today().isoformat()
        else:
            p.pop("done_date", None)
        save(d, f"{p['name']} {'已做到' if args.cmd == 'done' else '改回承諾中'}", push)
        print(f"{'✨ 金色葉子' if args.cmd == 'done' else '🍃 改回承諾中'}：{p['id']} {p['name']}")
    elif args.cmd == "remove":
        p = find(d, args.id)
        d["pledges"].remove(p)
        save(d, f"移除 {p['name']} 的承諾", push)
        print(f"已移除 {p['id']} {p['name']}")
    else:
        for p in d["pledges"]:
            print(f"{p['id']}｜{'✓ 已做到' if p['status'] == 'done' else '承諾中'}｜{p['name']}（{p['org']}）｜{p['what']}｜{p['episode']}")
        if not d["pledges"]:
            print("承諾牆目前還沒有葉子")


if __name__ == "__main__":
    main()
