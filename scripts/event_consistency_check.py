#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""活動場次一致性巡檢（教練 2026-08-24 交辦：官網↔個別活動頁要雙向連動）

教練要的是：「改個別網頁要對照官網同步更新，官網更新個別網站也要跟著動。」
真正做得到「連動」的前提是有人會發現不同步——所以這支每天自動比對三件事：

  ① event.db（唯一真相源） vs bigtree-tw 正式站：場次有沒有一邊多一邊少
  ② 每個未來場次有沒有 slug：沒有 slug＝那場報名寫不進資料庫，也不會發通知（靜默漏接）
  ③ 每個個別活動頁有沒有真的接上通知管線：
     接法有兩種都算合格——(a) 自己打 /api/register (b) 深連結回官網報名
     兩種都沒有＝那個頁面的報名是「黑洞」，教練跟佩佩老師永遠不會知道有人報名

第③項就是 2026-08-24 這次巡檢抓到 ai-forum-taichung（台中場 9/23-24）的方式：
它的報名鈕直接跳藍新金流付款，完全不經過任何通知，報名了也沒人會收到訊息。

用法：
  python3 scripts/event_consistency_check.py            # 印報告
  python3 scripts/event_consistency_check.py --notify   # 有問題才發 Telegram
"""

import json
import os
import re
import sqlite3
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
EVENT_DB = os.path.join(WORKSPACE, "event-signup", "event.db")
REPOS = os.path.expanduser("~/github_repos")
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
COACH_CHAT_ID = "6124913915"
LIVE_SITE = "https://bigtree-tw.netlify.app/"
STATE_FILE = os.path.join(WORKSPACE, "state", "event_consistency_state.json")
TPE = timezone(timedelta(hours=8))

# 個別活動頁 → 它負責哪些場次 slug。新增微站時在這裡加一行，巡檢就會自動涵蓋。
SATELLITE_SITES = {
    "ai-talk": {"desc": "AI微論壇 嘉義場", "slugs": ["bigtree-0828"]},
    "ai-fit": {"desc": "從從容容用AI聊健康 台南場", "slugs": ["bigtree-0922-day", "bigtree-0922-night"]},
    "ai-forum-taichung": {"desc": "AI微論壇 台中場", "slugs": ["bigtree-0923", "bigtree-0924"]},
}

API_ENDPOINT_RE = re.compile(r"event\.bymyway\.com/api/register")
DEEPLINK_RE = re.compile(r"bigtree-tw\.netlify\.app/\?session=")


def db_sessions():
    """讀 event.db 的場次（唯一真相源）。回傳 {slug: row}，只看還沒過期的。"""
    conn = sqlite3.connect(EVENT_DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT slug, name, event_date, start_time, site, location, venue, status FROM events"
    ).fetchall()
    conn.close()
    today = datetime.now(TPE).strftime("%Y-%m-%d")
    out = {}
    for r in rows:
        d = dict(r)
        d["is_future"] = bool(d.get("event_date")) and d["event_date"] >= today
        out[d["slug"]] = d
    return out


def live_site_slugs():
    """抓 bigtree-tw 正式站上實際列出的 slug。抓不到回 None（網路問題不算不一致）。"""
    try:
        with urllib.request.urlopen(LIVE_SITE, timeout=15) as r:
            html = r.read().decode("utf-8", errors="replace")
        return set(re.findall(r"slug:'([^']+)'", html))
    except Exception as e:
        print(f"⚠️ 抓不到正式站（{e}），本輪跳過官網比對", file=sys.stderr)
        return None


def satellite_status():
    """檢查每個個別活動頁怎麼收報名。"""
    result = {}
    for repo, meta in SATELLITE_SITES.items():
        path = os.path.join(REPOS, repo, "index.html")
        if not os.path.exists(path):
            result[repo] = {**meta, "exists": False}
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        has_api = bool(API_ENDPOINT_RE.search(html))
        has_deeplink = bool(DEEPLINK_RE.search(html))
        result[repo] = {
            **meta, "exists": True,
            "has_api": has_api, "has_deeplink": has_deeplink,
            "notified": has_api or has_deeplink,
            "how": "自己打 /api/register" if has_api else ("深連結回官網報名" if has_deeplink else "❌ 沒有任何通知管線"),
        }
    return result


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


def main() -> int:
    do_notify = "--notify" in sys.argv
    problems = []

    sessions = db_sessions()
    future = {s: v for s, v in sessions.items() if v["is_future"] and v.get("status") != "cancelled"}
    # 其他獨立站（例如 ai-art）的場次本來就不會列在大樹官網，不拿來比
    future_bigtree = {s: v for s, v in future.items() if (v.get("site") or "bigtree") == "bigtree"}
    live = live_site_slugs()
    sats = satellite_status()

    print("═══ 活動場次一致性巡檢 ═══")
    print(f"時間：{datetime.now(TPE).strftime('%Y-%m-%d %H:%M:%S')}（台灣時間）")
    print(f"資料庫場次：共 {len(sessions)} 場，其中未來場次 {len(future)} 場\n")

    # ① 官網 vs 資料庫
    print("① 官網 vs 資料庫")
    if live is None:
        print("   ⏭️  正式站抓不到，跳過")
    else:
        only_db = set(future_bigtree) - live
        only_live = live - set(sessions)
        if not only_db and not only_live:
            print(f"   ✅ 一致（正式站列出 {len(live)} 場）")
        for s in sorted(only_db):
            msg = f"資料庫有「{future_bigtree[s]['name']}（{s}／{future_bigtree[s]['event_date']}）」但官網沒列出——是不是忘了按一鍵發佈？"
            print(f"   🔴 {msg}")
            problems.append(msg)
        for s in sorted(only_live):
            msg = f"官網列出的場次「{s}」在資料庫查無——報名會寫不進去"
            print(f"   🔴 {msg}")
            problems.append(msg)

    # ② 未來場次有沒有 slug
    print("\n② 未來場次的報名識別碼")
    no_slug = [v for v in future.values() if not v.get("slug")]
    if not no_slug:
        print(f"   ✅ {len(future)} 場都有 slug，報名都寫得進資料庫")
    for v in no_slug:
        msg = f"場次「{v['name']}（{v['event_date']}）」沒有 slug，那場報名寫不進資料庫也不會通知"
        print(f"   🔴 {msg}")
        problems.append(msg)

    # ③ 個別活動頁的通知管線
    print("\n③ 個別活動頁的報名通知管線")
    for repo, st in sats.items():
        if not st["exists"]:
            msg = f"個別活動頁 {repo} 找不到 index.html"
            print(f"   ⚠️  {msg}")
            problems.append(msg)
            continue
        # 活動已辦完或取消，頁面會改成回顧／取消公告、拿掉報名鈕，沒有通知管線是正常的
        if not any(slug in future for slug in st["slugs"]):
            print(f"   ⏭️  {repo}（{st['desc']}）→ 場次已結束或取消，不再收報名，不檢查")
            continue
        icon = "✅" if st["notified"] else "🔴"
        print(f"   {icon} {repo}（{st['desc']}）→ {st['how']}")
        if not st["notified"]:
            problems.append(
                f"個別活動頁「{st['desc']}」({repo}) 的報名不會發任何通知——"
                f"有人報名教練跟佩佩老師都不會知道"
            )
        # 順便確認它負責的場次在資料庫裡真的存在
        for slug in st["slugs"]:
            if slug not in sessions:
                msg = f"{repo} 對應的場次代碼 {slug} 在資料庫查無"
                print(f"      🔴 {msg}")
                problems.append(msg)

    print("\n═══ 結論 ═══")
    if not problems:
        print("✅ 全部一致，沒有需要教練處理的事")
    else:
        print(f"🔴 共 {len(problems)} 項需要處理：")
        for i, p in enumerate(problems, 1):
            print(f"  {i}. {p}")

    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "checked_at": datetime.now(TPE).isoformat(),
            "future_sessions": len(future),
            "problems": problems,
            "satellites": sats,
        }, f, ensure_ascii=False, indent=2)

    if do_notify and problems:
        notify("🔎 活動場次巡檢發現 " + str(len(problems)) + " 項問題：\n"
               + "\n".join(f"· {p}" for p in problems[:8])
               + "\n\n完整報告：state/event_consistency_state.json")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
