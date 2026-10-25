#!/usr/bin/env python3
"""人才軍火庫首頁前 FRONT 位 → 邀請函頁用的 roster.json＋縮圖（2026-10-25 教練：邀請函首批 24 位要跟首頁排名連動）。

首頁（skyteam/index.html）的 experts-data 前 FRONT 位就是「排名池」；首頁載入時再依點擊數重排。
邀請函頁讀 roster.json＋/api/skyteam/ranking，用同一條排序規則取前 24 位。
所以首頁換人、調 FRONT、改照片後，跑一次本程式即可（可重複執行）：
    python3 scripts/skyteam_build_invite_roster.py
"""
import base64, hashlib, io, json, re, sys
from pathlib import Path
from PIL import Image

REPO = Path.home() / "github_repos/skyteam"
OUT_DIR = REPO / "img/invite/roster"
s = (REPO / "index.html").read_text(encoding="utf-8")
front = int(re.search(r"const FRONT=(\d+)", s).group(1))
experts = json.loads(re.search(r'<script[^>]*id="experts-data"[^>]*>(.*?)</script>', s, re.S).group(1))[:front]
OUT_DIR.mkdir(parents=True, exist_ok=True)
keep, roster = set(), []
for e in experts:
    img = e.get("image") or ""
    thumb = None
    raw = None
    if img.startswith("data:image"):
        raw = base64.b64decode(img.split(",", 1)[1])
    elif img and (REPO / img).is_file():
        raw = (REPO / img).read_bytes()
    if raw:
        key = hashlib.md5(raw).hexdigest()[:10]
        f = OUT_DIR / f"{key}.webp"
        if not f.exists():
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            w, h = im.size
            tw = min(w, int(h * 0.8))  # 4:5，取上方（人像臉在上）
            im = im.crop(((w - tw) // 2, 0, (w - tw) // 2 + tw, min(h, int(tw * 1.25)))).resize((320, 400), Image.LANCZOS)
            im.save(f, "WEBP", quality=82)
        thumb = f"img/invite/roster/{key}.webp"
        keep.add(f.name)
    roster.append({"n": e["name"], "r": e.get("role", ""), "u": e.get("url") or "", "i": thumb})
for f in OUT_DIR.glob("*.webp"):
    if f.name not in keep:
        f.unlink()
(REPO / "roster.json").write_text(json.dumps(roster, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"roster.json：{len(roster)} 位（FRONT={front}），縮圖 {len(keep)} 張")
