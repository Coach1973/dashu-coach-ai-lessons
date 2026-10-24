#!/usr/bin/env python3
"""人才軍火庫（顧問師天團）自動連結：新上架的顧問／專家個人網頁，自動寫進該專家在名錄裡的「url」欄位。
規則（教練 2026-10-24 定）：凡做出顧問或專家的網頁，就自動放進他在天團名錄的連結。
- 只改「沒有連結」或「連結是別頁的 #錨點」的專家；已有獨立個人頁的不動。
- 網站標題的第一段必須含專家姓名（避免多人合輯頁誤配）。
- 事件觸發：curation_process 上架處理完跑一次；沒有任何要改的就什麼都不做。
用法：skyteam_link_expert.py [--dry-run]
"""
import json, re, subprocess, sys
from pathlib import Path

REG = Path.home() / ".openclaw/workspace/event-signup/curated_sites_registry.json"
REPO = Path.home() / "github_repos/skyteam"
IDX = REPO / "index.html"
PAT = re.compile(r'(<script id="experts-data" type="application/json">)(.*?)(</script>)', re.S)
SKIP_SLUGS = {"skyteam"}


def main(dry: bool) -> int:
    sites = [s for s in json.loads(REG.read_text(encoding="utf-8"))["sites"]
             if s.get("status") == "live" and s["slug"] not in SKIP_SLUGS]
    h = IDX.read_text(encoding="utf-8")
    m = PAT.search(h)
    experts = json.loads(m.group(2))
    changed = []
    for e in experts:
        url = e.get("url") or ""
        if url and "#" not in url:
            continue
        hits = [s for s in sites if e["name"] in re.split(r"[｜|・—\-]", s["title"])[0]]
        if len(hits) != 1:
            continue
        new = hits[0]["event_url"]
        if new != url:
            changed.append((e["name"], url, new))
            e["url"] = new
    for c in changed:
        print("連結:", c)
    if not changed or dry:
        return 0
    IDX.write_text(h[:m.start(2)] + json.dumps(experts, ensure_ascii=False) + h[m.end(2):], encoding="utf-8")
    names = "、".join(c[0] for c in changed)
    subprocess.run(["git", "-C", str(REPO), "add", "index.html"], check=True)
    subprocess.run(["git", "-C", str(REPO), "commit", "-q", "-m", f"[Mac] 人才軍火庫自動連結專家個人頁：{names}"], check=True)
    subprocess.run(["git", "-C", str(REPO), "push", "-q", "origin", "main"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main("--dry-run" in sys.argv))
