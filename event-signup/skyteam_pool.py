#!/usr/bin/env python3
"""未上架的人才軍火庫（教練 2026-11-02 交辦）：做好的人一律先進「未上架」，教練在後台勾選才上架；已上架的也能勾選下架。
比照大台南策展中心的上架／下架後台（/curation/admin）。

- 未上架名單：~/.openclaw/data/skyteam_pool.json（不在網站資料夾，不會被公開讀到；寫入前備份）
- 已上架名單：~/github_repos/skyteam/index.html 的 experts-data＋FRONT（顧問師前段人數）
- 上架／下架後：重產邀請函名單（skyteam_build_invite_roster.py）→ commit＋push skyteam

上架去處：
  front        顧問師前段（插在前段最後一位，FRONT+1；分類用主題分類）
  商務團隊      放名單後段（江宜倫維持最後）
  人脈資源團隊  同上

用法：
  skyteam_pool.py list
  skyteam_pool.py add <slug> [--name N --role R --background B --summary S --tags a,b,c --category C --image 照片檔]
  skyteam_pool.py set-image <slug> [照片檔]   不給照片檔＝自動用個人網頁首頁第一張（教練 11/05 定）
  skyteam_pool.py publish <slug>... --to front|商務團隊|人脈資源團隊 [--topic 主題分類]
  skyteam_pool.py unpublish <姓名>...
  skyteam_pool.py dismiss <slug>...       不是人才（例如活動頁）→ 移出清單，之後不再自動加入
  skyteam_pool.py auto                    策展上架後自動跑：新上架、標題像個人頁的，加進未上架（第一次只記基準）
"""
from __future__ import annotations

import base64
import fcntl
import html as htmllib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

DATA = Path.home() / ".openclaw/data"
POOL = DATA / "skyteam_pool.json"
LOCK = DATA / "skyteam_pool.lock"
BACKUP_DIR = DATA / "skyteam_pool_backups"
REPO = Path.home() / "github_repos/skyteam"
IDX = REPO / "index.html"
REPOS = Path.home() / "github_repos"
REG = Path.home() / ".openclaw/workspace/event-signup/curated_sites_registry.json"
INVITE_BUILDER = Path.home() / ".openclaw/workspace/scripts/skyteam_build_invite_roster.py"
PAT = re.compile(r'(<script id="experts-data" type="application/json">)(.*?)(</script>)', re.S)
FRONT_PAT = re.compile(r"const FRONT=(\d+);")
TOPICS = ["品牌與商業策略", "永續與產業創新", "音樂與藝術創意", "AI 與數位轉型", "教育與人才培育", "財金與風險管理"]
TEAMS = ["商務團隊", "人脈資源團隊"]
KEEP_LAST = "江宜倫"  # 教練 10/28：放整份名單最後
SKIP_SLUGS = {"skyteam"}
_ENV = {**os.environ, "PATH": f"/opt/homebrew/bin:/usr/bin:/bin:{os.environ.get('PATH', '')}"}
GIT = ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com"]


# ---------- 資料讀寫 ----------
def load_pool() -> dict:
    if POOL.exists():
        return json.loads(POOL.read_text(encoding="utf-8"))
    return {"pool": [], "dismissed": [], "seen": None}


def save_pool(p: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    if POOL.exists():
        BACKUP_DIR.mkdir(exist_ok=True)
        shutil.copy2(POOL, BACKUP_DIR / f"skyteam_pool.{datetime.now():%Y%m%d-%H%M%S-%f}.json")
        for old in sorted(BACKUP_DIR.glob("skyteam_pool.*.json"))[:-30]:  # 留最近 30 份
            old.unlink()
    tmp = POOL.with_suffix(".tmp")
    tmp.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(POOL)


def read_roster() -> tuple[str, list, int]:
    h = IDX.read_text(encoding="utf-8")
    experts = json.loads(PAT.search(h).group(2))
    return h, experts, int(FRONT_PAT.search(h).group(1))


def write_roster(h: str, experts: list, front: int) -> None:
    m = PAT.search(h)
    h = h[:m.start(2)] + json.dumps(experts, ensure_ascii=False) + h[m.end(2):]
    h = FRONT_PAT.sub(f"const FRONT={front};", h, count=1)
    IDX.write_text(h, encoding="utf-8")


def slug_of(url: str) -> str:
    m = re.search(r"/curated/([^/?#]+)", url or "")
    return m.group(1) if m else ""


class _Lock:
    def __enter__(self):
        DATA.mkdir(parents=True, exist_ok=True)
        self.f = open(LOCK, "w")
        fcntl.flock(self.f, fcntl.LOCK_EX)
        return self

    def __exit__(self, *a):
        fcntl.flock(self.f, fcntl.LOCK_UN)
        self.f.close()


def _publish_repo(message: str) -> str:
    """重產邀請函名單 → commit＋push skyteam。回傳 commit 短碼。"""
    subprocess.run([sys.executable, str(INVITE_BUILDER)], check=True, timeout=120, env=_ENV,
                   stdout=subprocess.DEVNULL)
    subprocess.run(["git", "add", "-A"], cwd=REPO, check=True, timeout=15, env=_ENV)
    subprocess.run(GIT + ["commit", "-q", "-m", message], cwd=REPO, check=True, timeout=15, env=_ENV)
    subprocess.run(["git", "push", "-q"], cwd=REPO, check=True, timeout=60, env=_ENV)
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True,
                          env=_ENV).stdout.strip()


def _rollback() -> None:
    """推不上去就把 skyteam 退回上一版（含已 commit 但沒推上去的），名單不動。"""
    st = subprocess.run(["git", "status", "-sb"], cwd=REPO, capture_output=True, text=True, env=_ENV).stdout
    if "ahead" in st.splitlines()[0]:
        subprocess.run(["git", "reset", "-q", "--soft", "@{u}"], cwd=REPO, env=_ENV)
    subprocess.run(["git", "reset", "-q"], cwd=REPO, env=_ENV)
    subprocess.run(["git", "checkout", "--", "."], cwd=REPO, env=_ENV)
    subprocess.run(["git", "clean", "-fdq", "img/invite/roster"], cwd=REPO, env=_ENV)


# ---------- 照片 ----------
def image_data_uri(path: str) -> str:
    """照片裁成 4:5、520×650 webp，回傳 data URI（跟名單裡其他人同規格）。"""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    w, h = im.size
    tw = int(h * 0.8)
    if tw <= w:
        x = (w - tw) // 2
        im = im.crop((x, 0, x + tw, h))
    else:
        th = int(w / 0.8)
        y = (h - th) // 3  # 臉通常在上半部，往上偏
        im = im.crop((0, y, w, y + th))
    im = im.resize((520, 650), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=80)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def page_first_image(slug: str) -> str | None:
    """個人網頁（完成版）首頁第一張內嵌照片＝教練認定的本人照。回傳 data URI（4:5、520×650 webp），沒有就回 None。
    2026-11-05 教練指正：做好的網頁第一張就是照片，不准再翻原始照片資料夾瞎找。"""
    page = REPOS / slug / "index.html"
    if not page.exists():
        return None
    h = page.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<img[^>]*src="data:image/[a-z+]+;base64,([A-Za-z0-9+/=]{200,})"', h)
    if not m:
        return None
    from PIL import Image
    tmp = DATA / f"_first_{slug}.img"
    tmp.write_bytes(base64.b64decode(m.group(1)))
    try:
        return image_data_uri(str(tmp))
    finally:
        tmp.unlink(missing_ok=True)


# ---------- 從網頁抓基本資料 ----------
def _registry_sites() -> list:
    return [s for s in json.loads(REG.read_text(encoding="utf-8"))["sites"] if s["slug"] not in SKIP_SLUGS]


def card_from_page(slug: str) -> dict:
    site = next((s for s in _registry_sites() if s["slug"] == slug), {})
    page = REPOS / slug / "index.html"
    h = page.read_text(encoding="utf-8", errors="ignore")[:400000] if page.exists() else ""
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    d = re.search(r'name="description" content="(.*?)"', h, re.S)
    title = site.get("title") or (htmllib.unescape(t.group(1)) if t else slug)
    desc = site.get("description") or (htmllib.unescape(d.group(1)) if d else "")
    parts = [x.strip() for x in re.split(r"[｜|]", title) if x.strip()]
    name = parts[0] if parts else slug
    role = parts[1] if len(parts) > 1 else ""
    summary = re.split(r"(?<=[。！？])", desc)[0][:60] if desc else ""
    return {"name": name, "category": "品牌與商業策略", "role": role, "background": desc[:90],
            "summary": summary, "tags": [], "url": f"https://event.bymyway.com/curated/{slug}/", "image": ""}


# ---------- 動作 ----------
def add(slug: str, fields: dict | None = None, image: str | None = None, force: bool = False) -> str:
    with _Lock():
        p = load_pool()
        _, experts, _ = read_roster()
        if not force:
            if any(slug_of(e.get("url")) == slug for e in experts):
                return f"{slug} 已經在人才軍火庫，略過"
            if slug in p["dismissed"]:
                return f"{slug} 之前被移出清單（不是人才），略過；要加回來用 --force"
        card = card_from_page(slug)
        card.update({k: v for k, v in (fields or {}).items() if v})
        if image:
            card["image"] = image_data_uri(image)
        elif not card.get("image"):
            card["image"] = page_first_image(slug) or ""
        card["slug"] = slug
        card["added_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        p["pool"] = [c for c in p["pool"] if c["slug"] != slug] + [card]
        p["dismissed"] = [s for s in p["dismissed"] if s != slug]
        save_pool(p)
        return f"已加進未上架的人才軍火庫：{card['name']}（{slug}）"


def set_image(slug: str, image: str | None = None) -> str:
    with _Lock():
        p = load_pool()
        c = next((c for c in p["pool"] if c["slug"] == slug), None)
        if not c:
            return f"未上架名單裡沒有 {slug}"
        uri = image_data_uri(image) if image else page_first_image(slug)
        if not uri:
            return f"{slug} 的網頁上找不到照片，請給照片檔"
        c["image"] = uri
        save_pool(p)
        return f"已換 {c['name']} 的照片"


def publish(slugs: list, to: str, topic: str | None = None) -> tuple[bool, str]:
    if not slugs:
        return False, "沒有勾選任何人"
    if to != "front" and to not in TEAMS:
        return False, f"不認得的上架去處：{to}"
    with _Lock():
        p = load_pool()
        picked = [c for c in p["pool"] if c["slug"] in slugs]
        if not picked:
            return False, "沒有勾選任何人"
        h, experts, front = read_roster()
        taken = {e["name"] for e in experts}
        dup = [c["name"] for c in picked if c["name"] in taken]
        if dup:
            return False, f"人才軍火庫已經有同名的人：{'、'.join(dup)}，沒有上架"
        last = experts.pop() if experts and experts[-1]["name"] == KEEP_LAST else None
        names = []
        for c in picked:
            card = {k: c.get(k, "") for k in ("name", "category", "role", "background", "summary", "tags", "url", "image")}
            if c.get("chapter"):
                card["chapter"] = c["chapter"]
            if to == "front":
                if topic in TOPICS:
                    card["category"] = topic
                elif card["category"] not in TOPICS:
                    card["category"] = TOPICS[0]
                experts.insert(front, card)
                front += 1
            else:
                card["category"] = to
                experts.append(card)
            names.append(c["name"])
        if last:
            experts.append(last)
        write_roster(h, experts, front)
        where = "顧問師前段" if to == "front" else to
        try:
            sha = _publish_repo(f"[Mac] 人才軍火庫後台上架（{where}）：{'、'.join(names)}")
        except Exception as e:  # noqa: BLE001
            _rollback()
            return False, f"上架失敗，名單沒有改動（{e}）"
        p["pool"] = [c for c in p["pool"] if c["slug"] not in slugs]
        save_pool(p)
        return True, f"已上架到{where}：{'、'.join(names)}（約 1～2 分鐘後網頁更新，commit {sha}）"


def unpublish(names: list) -> tuple[bool, str]:
    with _Lock():
        p = load_pool()
        h, experts, front = read_roster()
        keep, moved = [], []
        for i, e in enumerate(experts):
            if e["name"] in names:
                if i < front:
                    front -= 1
                moved.append(e)
            else:
                keep.append(e)
        if not moved:
            return False, "沒有勾選任何人"
        write_roster(h, keep, front)
        try:
            sha = _publish_repo(f"[Mac] 人才軍火庫後台下架（移回未上架）：{'、'.join(e['name'] for e in moved)}")
        except Exception as e:  # noqa: BLE001
            _rollback()
            return False, f"下架失敗，名單沒有改動（{e}）"
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        for e in moved:
            c = dict(e)
            c["slug"] = slug_of(e.get("url")) or "name-" + e["name"]
            c["added_at"] = now
            c["note"] = "從人才軍火庫下架"
            p["pool"] = [x for x in p["pool"] if x["slug"] != c["slug"]] + [c]
        save_pool(p)
        return True, f"已下架、移回未上架：{'、'.join(e['name'] for e in moved)}（約 1～2 分鐘後網頁更新，commit {sha}）"


def dismiss(slugs: list) -> tuple[bool, str]:
    with _Lock():
        p = load_pool()
        gone = [c["name"] for c in p["pool"] if c["slug"] in slugs]
        if not gone:
            return False, "沒有勾選任何人"
        p["pool"] = [c for c in p["pool"] if c["slug"] not in slugs]
        p["dismissed"] = sorted(set(p["dismissed"]) | set(slugs))
        save_pool(p)
        return True, f"已移出清單（之後不會再自動加入）：{'、'.join(gone)}"


_NOT_PERSON = re.compile(r"活動|課|工作坊|計劃|計畫|SOP|報告|送件|協會|分會|俱樂部|中心|農莊|食堂|餐|咖啡|旅行社|"
                         r"商圈|漫畫|漫劇|大會|邀請|票選|一覽|名單|天團|軍火庫|教材|技能書|研究|手作|DIY|快剪|官邸|"
                         r"補助|收集|榮樹下|真公益|約瑟布|答案|團隊|系統")


# 標題開頭要是常見姓氏：11/02 實測現有 130 站誤抓 0、軍火庫 61 人抓到 46（漏的由軍師做頁時手動 add）
_SURNAMES = set("王李張劉陳楊黃趙吳周徐孫馬朱胡郭何高林羅鄭梁謝宋唐許韓馮鄧曹彭曾蕭田董袁潘于蔣蔡余杜葉程蘇魏呂丁任沈姚盧姜"
                "崔鍾譚陸汪范金石廖賈夏韋傅方白鄒孟熊秦邱江尹薛閻段雷侯龍史陶黎賀顧毛郝龔邵萬錢嚴覃武戴莫孔向湯游柯簡賴翁詹莊涂紀洪施溫顏歐")


def looks_like_person(site: dict) -> bool:
    title = site.get("title", "")
    if "｜" not in title and "|" not in title:
        return False
    lead = re.split(r"[｜|]", title)[0].strip()
    if site.get("category") == "大樹小講活動" or _NOT_PERSON.search(lead):
        return False
    return lead[:1] in _SURNAMES and bool(re.match(r"^[一-鿿]{2,4}", lead)) and len(lead) <= 24


def auto() -> list:
    """新上架、標題像個人頁、不在軍火庫也不在未上架的 → 自動加進未上架（沒有照片，等軍師補）。"""
    p = load_pool()
    sites = [s for s in _registry_sites() if s.get("status", "live") == "live"]
    if p.get("seen") is None:  # 第一次：現有網站全部當基準，不回頭加
        with _Lock():
            p = load_pool()
            p["seen"] = sorted(s["slug"] for s in sites)
            save_pool(p)
        return []
    _, experts, _ = read_roster()
    in_roster = {slug_of(e.get("url")) for e in experts}
    added = []
    for s in sites:
        if s["slug"] in p["seen"]:
            continue
        if looks_like_person(s) and s["slug"] not in in_roster and s["slug"] not in {c["slug"] for c in p["pool"]}:
            add(s["slug"])
            added.append(s["slug"])
    with _Lock():
        p = load_pool()
        p["seen"] = sorted(set(p["seen"]) | {s["slug"] for s in sites})
        save_pool(p)
    return added


def main(argv: list) -> int:
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    a = sub.add_parser("add")
    a.add_argument("slug")
    for f in ("name", "role", "background", "summary", "tags", "category", "image", "chapter"):
        a.add_argument(f"--{f}")
    a.add_argument("--force", action="store_true")
    si = sub.add_parser("set-image")
    si.add_argument("slug")
    si.add_argument("image", nargs="?", default=None)  # 不給＝用個人網頁第一張照片
    pb = sub.add_parser("publish")
    pb.add_argument("slugs", nargs="+")
    pb.add_argument("--to", required=True)
    pb.add_argument("--topic")
    up = sub.add_parser("unpublish")
    up.add_argument("names", nargs="+")
    ds = sub.add_parser("dismiss")
    ds.add_argument("slugs", nargs="+")
    sub.add_parser("auto")
    o = ap.parse_args(argv)
    if o.cmd == "list":
        p = load_pool()
        for c in p["pool"]:
            print(f"{c['slug']}\t{c['name']}\t{c['category']}\t{'有照片' if c.get('image') else '照片待補'}")
        print(f"共 {len(p['pool'])} 位；移出清單 {len(p['dismissed'])} 個")
    elif o.cmd == "add":
        fields = {"name": o.name, "role": o.role, "background": o.background, "summary": o.summary,
                  "category": o.category, "chapter": o.chapter,
                  "tags": [t.strip() for t in o.tags.split(",")] if o.tags else None}
        print(add(o.slug, fields, o.image, o.force))
    elif o.cmd == "set-image":
        print(set_image(o.slug, o.image))
    elif o.cmd == "publish":
        print(publish(o.slugs, o.to, o.topic)[1])
    elif o.cmd == "unpublish":
        print(unpublish(o.names)[1])
    elif o.cmd == "dismiss":
        print(dismiss(o.slugs)[1])
    elif o.cmd == "auto":
        print(json.dumps({"added": auto()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
