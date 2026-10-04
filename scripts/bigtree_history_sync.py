#!/usr/bin/env python3
"""大樹小講「過往講座歷史紀錄」自動補登（2026-10-04 教練裁示：上架在大樹小講的活動，結束後一定要自動納入歷史頁）

做什麼：
  掃 event-signup/event.db 裡 site='bigtree'、status='active'、日期已過的場次；
  歷史頁（github_repos/bigtree/archive/lecture-history.html 的 EVENTS 清單）還沒有那一天的 → 自動補一張卡片
  （海報優先抓該場活動網頁的 og:image / edm，抓不到就產生一張文字卡），再 commit + push 到 GitHub。
  event.bymyway.com/bigtree/archive/lecture-history.html 直接讀本機檔案，補完立刻看得到。
  不碰 Netlify（Netlify 部署要教練說「推」）。

跑法：
  bigtree_history_sync.py            補登並 commit/push
  bigtree_history_sync.py --dry-run  只列出會補哪些，不改檔
排程：launchd ai.openclaw.bigtree-history-sync，每天 00:20（日期一過就是「結束之後」）。
"""
from __future__ import annotations

import re
import sqlite3
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urljoin

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DB_PATH = WORKSPACE / "event-signup" / "event.db"
REPO = Path("/Users/bymyway/github_repos/bigtree")
HISTORY = REPO / "archive" / "lecture-history.html"
EDM_DIR = REPO / "archive" / "edm"
LOG = WORKSPACE / "distill" / "bigtree_history_sync.log"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
WEEKDAY = ["一", "二", "三", "四", "五", "六", "日"]
# 跟 event-signup/bigtree_publish.py 的 SLOT_TIMES 同一份對照（只用來把時段名稱換成時間文字）
SLOT_TIMES = {
    "早": "09:00–12:00", "早半": "10:00–12:30", "午": "14:00–17:00", "午半": "14:00–16:30",
    "晚": "18:00–21:00", "晚半": "18:00–20:30", "夜": "19:30–21:30", "線上": "10:00–12:00",
    "上午": "10:00–12:00", "下午": "13:30–16:30", "AM": "09:00–12:00", "PM": "13:00–16:00",
    "全日": "09:00–17:00", "午後": "15:00–17:30",
}
GIT = ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com"]
TAIPEI = timezone(timedelta(hours=8))


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now(TAIPEI):%Y-%m-%d %H:%M:%S}] {msg}"
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def js_str(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")


def past_events(today: str) -> list[dict]:
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    rows = db.execute(
        "SELECT slug,name,event_date,start_time,slot_key,location,venue,address,event_url FROM events "
        "WHERE site='bigtree' AND status='active' AND event_date < ? ORDER BY event_date, start_time",
        (today,),
    ).fetchall()
    db.close()
    out = []
    for r in rows:
        if "待定" in (r["name"] or ""):  # 「主題待定」的佔位場次不算真的辦過
            continue
        out.append(dict(r))
    return out


def covered_dates(html: str) -> set[tuple[int, int]]:
    i = html.index("const EVENTS")
    j = html.index("];", i)
    return {(int(m), int(d)) for m, d in re.findall(r"grid:'(\d+)/(\d+)'", html[i:j])}


def fetch(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 bigtree-history-sync"})
        return urllib.request.urlopen(req, timeout=20).read()
    except Exception as exc:  # noqa: BLE001
        log(f"  抓取失敗 {url}：{exc}")
        return None


def poster_from_page(event_url: str) -> bytes | None:
    """活動網頁的 og:image（沒有就找 edm.jpg）當歷史頁海報。"""
    if not event_url:
        return None
    page = fetch(event_url)
    if not page:
        return None
    text = page.decode("utf-8", "ignore")
    m = re.search(r'property="og:image"\s+content="([^"]+)"', text) or re.search(
        r'content="([^"]+)"\s+property="og:image"', text
    )
    cands = [urljoin(event_url, m.group(1))] if m else []
    cands.append(urljoin(event_url, "edm.jpg"))
    for u in cands:
        data = fetch(u)
        if data and data[:3] in (b"\xff\xd8\xff", b"\x89PN", b"RIF"):
            return data
    return None


def save_poster(raw: bytes, dest: Path) -> None:
    from io import BytesIO

    from PIL import Image

    im = Image.open(BytesIO(raw)).convert("RGB")
    im.thumbnail((1200, 1200))
    im.save(dest, "JPEG", quality=85, optimize=True)


def text_card(ev: dict, dest: Path) -> None:
    """沒有海報時的備用卡：深綠底 + 日期 + 活動名稱 + 地點。"""
    from PIL import Image, ImageDraw, ImageFont

    W = 1080
    im = Image.new("RGB", (W, W), (28, 42, 40))
    d = ImageDraw.Draw(im)
    big, mid, small = (ImageFont.truetype(FONT, s) for s in (120, 64, 46))
    y, m, day = ev["event_date"].split("-")
    d.text((80, 150), f"{int(m)}/{int(day)}", font=big, fill=(246, 185, 138))
    name, lines = ev["name"], []
    while name:
        lines.append(name[:11])
        name = name[11:]
    for i, ln in enumerate(lines[:4]):
        d.text((80, 330 + i * 90), ln, font=mid, fill=(255, 255, 255))
    where = " ".join(x for x in (ev.get("location"), ev.get("venue")) if x)
    d.text((80, 900), where, font=small, fill=(215, 205, 185))
    d.text((80, 970), "大樹小講 · 無話不談", font=small, fill=(246, 185, 138))
    im.save(dest, "JPEG", quality=88)


def build_entry(ev: dict, img_rel: str) -> str:
    y, m, d = (int(x) for x in ev["event_date"].split("-"))
    wd = WEEKDAY[datetime(y, m, d).weekday()]
    t = SLOT_TIMES.get(ev.get("slot_key") or "") or (ev.get("start_time") or "")
    date_txt = f"{y} 年 {m} 月 {d} 日（{wd}）{t}".strip()
    name = ev["name"]
    where = ev.get("venue") or ev.get("location") or ""
    core = where.replace("國立", "")
    short = name if (not where or core in name or (ev.get("location") or "") in name) else f"{name}（{where}）"
    parts = [p for p in ((ev.get("venue") or "") + (f"（{ev['address']}）" if ev.get("address") else ""),) if p]
    desc = "｜".join(parts + [ev.get("location") or ""]) if (parts or ev.get("location")) else name
    return (
        f"  {{ grid:'{m}/{d}', date:'{js_str(date_txt)}',\n"
        f"    short:'{js_str(short)}', title:'{js_str(name)}',\n"
        f"    desc:'{js_str(desc.strip('｜'))}',\n"
        f"    img:'{img_rel}', link:'{js_str(ev.get('event_url') or '')}' }},\n\n"
    )


def insert_entry(html: str, ev: dict, entry: str) -> str:
    y, m, d = (int(x) for x in ev["event_date"].split("-"))
    i = html.index("const EVENTS")
    j = html.index("];", i)
    for mm in re.finditer(r"^  \{ grid:'(\d+)/(\d+)'", html[i:j], flags=re.M):
        if (int(mm.group(1)), int(mm.group(2))) > (m, d):
            pos = i + mm.start()
            return html[:pos] + entry + html[pos:]
    return html[:j] + entry.rstrip("\n") + "\n" + html[j:]


def main() -> int:
    dry = "--dry-run" in sys.argv
    today = datetime.now(TAIPEI).strftime("%Y-%m-%d")
    html = HISTORY.read_text(encoding="utf-8")
    have = covered_dates(html)
    missing, seen = [], set()
    for ev in past_events(today):
        y, m, d = (int(x) for x in ev["event_date"].split("-"))
        key = (ev["event_date"], ev.get("venue") or ev.get("location"))
        if (m, d) in have or key in seen:
            continue
        seen.add(key)
        missing.append(ev)
    if not missing:
        log("歷史頁已涵蓋所有已結束的大樹小講場次，無需補登")
        return 0
    log(f"需補登 {len(missing)} 場：" + "、".join(f"{e['event_date']} {e['name']}" for e in missing))
    if dry:
        return 0
    EDM_DIR.mkdir(parents=True, exist_ok=True)
    added = []
    for ev in missing:
        ymd = ev["event_date"].replace("-", "")[4:]
        fname = f"edm_{ymd}_{ev['slug'].replace('bigtree-', '')}.jpg"
        dest = EDM_DIR / fname
        raw = poster_from_page(ev.get("event_url") or "")
        try:
            if raw:
                save_poster(raw, dest)
                log(f"  {ev['slug']}：海報取自活動網頁 → {fname}")
            else:
                text_card(ev, dest)
                log(f"  {ev['slug']}：無海報，產生文字卡 → {fname}")
        except Exception as exc:  # noqa: BLE001
            log(f"  {ev['slug']}：圖片處理失敗 {exc}，這場先跳過")
            continue
        html = insert_entry(html, ev, build_entry(ev, f"edm/{fname}"))
        added.append((ev, fname))
    if not added:
        return 1
    HISTORY.write_text(html, encoding="utf-8")
    run = lambda *a: subprocess.run(a, cwd=REPO, capture_output=True, text=True)  # noqa: E731
    files = ["archive/lecture-history.html"] + [f"archive/edm/{f}" for _, f in added]
    run(*GIT, "add", *files)
    msg = "[Mac] 歷史紀錄自動補登：" + "、".join(f"{e['event_date'][5:]} {e['name']}" for e, _ in added)
    r = run(*GIT, "commit", "-m", msg + "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
    if r.returncode != 0:
        log(f"commit 失敗：{r.stderr.strip() or r.stdout.strip()}")
        return 1
    p = run(*GIT, "push", "origin", "HEAD")
    h = run("git", "rev-parse", "--short", "HEAD").stdout.strip()
    log(f"已補登 {len(added)} 場，commit {h}，push {'成功' if p.returncode == 0 else '失敗：' + p.stderr.strip()}")
    return 0 if p.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
