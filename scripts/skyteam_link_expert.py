#!/usr/bin/env python3
"""人才軍火庫（顧問師天團）自動連結：新上架的顧問／專家個人網頁，自動寫進該專家在名錄裡的「url」欄位。
規則（教練 2026-10-24 定）：凡做出顧問或專家的網頁，就自動放進他在天團名錄的連結。
- 只改「沒有連結」「#錨點」或「指向別人策展頁」的專家；已是本人頁或外部網站的不動。
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
PLACEHOLDER_HOSTS = ("facebook.com", "search.books.com.tw")  # 臨時放的連結（臉書／搜尋頁），有策展個人頁就換掉


def main(dry: bool) -> int:
    sites = [s for s in json.loads(REG.read_text(encoding="utf-8"))["sites"]
             if s.get("status") == "live" and s["slug"] not in SKIP_SLUGS]
    h = IDX.read_text(encoding="utf-8")
    m = PAT.search(h)
    experts = json.loads(m.group(2))
    changed = []
    for e in experts:
        url = e.get("url") or ""
        hits = [s for s in sites if e["name"] in re.split(r"[｜|・—\-]", s["title"])[0]]
        if len(hits) != 1:
            continue
        # 已是本人頁、或是外部自家網站就不動；空白／#錨點／指向別人的策展頁才換
        if url and "#" not in url and (url.rstrip("/") == hits[0]["event_url"].rstrip("/")
                                       or ("event.bymyway.com/curated/" not in url
                                       and not any(x in url for x in PLACEHOLDER_HOSTS))):
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
    # 邀請函頁的首批 24 位讀 roster.json，首頁連結改了就一起重產（2026-10-25）
    subprocess.run([sys.executable, str(Path(__file__).with_name("skyteam_build_invite_roster.py"))], check=True)
    subprocess.run(["git", "-C", str(REPO), "add", "index.html", "roster.json", "img/invite/roster"], check=True)
    subprocess.run(["git", "-C", str(REPO), "commit", "-q", "-m", f"[Mac] 人才軍火庫自動連結專家個人頁：{names}"], check=True)
    subprocess.run(["git", "-C", str(REPO), "push", "-q", "origin", "main"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main("--dry-run" in sys.argv))
