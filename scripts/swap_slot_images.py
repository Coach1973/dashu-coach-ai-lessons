#!/usr/bin/env python3
"""把小龍蝦用 LK888 出好的圖（IMG-001…）換進已上架的策展網頁（教練 2026-10-30 定的流程，省去搬圖）。

用法（教練只要說「○○ 已上架，換 IMG-001～004」，我就跑這一行）：
  python3 scripts/swap_slot_images.py <短網址>                 # 直接換、commit、push
  python3 scripts/swap_slot_images.py <短網址> --dry-run       # 只列出會換哪幾個位置，不動檔案
  python3 scripts/swap_slot_images.py <短網址> --map IMG-003=alt:關鍵字 --map IMG-004=alt:關鍵字
      ↑ 網頁沒有標記的位置（例如要換掉的是真實照片），用該 <img> 的 alt 文字裡的關鍵字指定（必須剛好對到 1 個）

怎麼找位置（依序）：
  1. <img data-slot="IMG-001" ...>      ← 開工指令請 TAVA 這樣標；只換 src
  2. <div class="ill"><svg>…</svg><span class="tag">…待換圖 IMG-001</span></div>   ← 舊版示意插畫位，整塊換成圖，圖說改「AI 繪製示意插畫」
  3. --map 指定的 alt 關鍵字
來源圖：~/.openclaw/media/outbound/IMG-00N*.png（取最新一張）。網頁在 ~/github_repos/<短網址>/index.html（改那裡＝線上版）。
圖片處理：長邊縮到 1000、轉 webp（品質 72，單張約 50～120KB，手機與電腦看都清楚）、以 base64 內嵌（跟 TAVA 網頁「圖片放進網頁裡」的規則一致）；原始 PNG 另存 ~/Pictures/<短網址>_AI原圖_<日期>/。（2026-10-30 教練定：LK888 的圖一律壓小再放進網頁，原 1600／q82 約 230～270KB。）
任何一個位置找不到或對到不只 1 個＝該張不換、最後列出，不會亂換。
輸出只印摘要，絕對不印網頁內容（網頁常有數 MB 的 base64）。
"""
import argparse, base64, datetime, glob, io, os, re, shutil, subprocess, sys
from PIL import Image

OUT = os.path.expanduser("~/.openclaw/media/outbound")


LONG_SIDE = 1000
WEBP_QUALITY = 72


def webp_data_uri(png):
    im = Image.open(png).convert("RGB")
    im.thumbnail((LONG_SIDE, LONG_SIDE), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=WEBP_QUALITY, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), len(buf.getvalue()), im.size


def set_src(tag, uri):
    return re.sub(r'src="[^"]*"', lambda m: 'src="%s"' % uri, tag, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--map", action="append", default=[], help="IMG-003=alt:關鍵字")
    ap.add_argument("--src", default=OUT)
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()

    repo = os.path.expanduser("~/github_repos/%s" % a.slug)
    page = os.path.join(repo, "index.html")
    if not os.path.isfile(page):
        sys.exit("找不到 %s" % page)
    html = open(page, encoding="utf-8").read()
    size0 = len(html)
    maps = dict(m.split("=", 1) for m in a.map)

    srcs = {}
    for p in sorted(glob.glob(os.path.join(a.src, "IMG-*.png")), key=os.path.getmtime):
        srcs[re.match(r"(IMG-\d+)", os.path.basename(p)).group(1)] = p
    if not srcs:
        sys.exit("在 %s 找不到 IMG-xxx 的 PNG" % a.src)

    done, skipped = [], []
    for iid in sorted(srcs):
        uri, nbytes, wh = webp_data_uri(srcs[iid])
        kind = None
        # 1. data-slot
        pat = re.compile(r'<img\b[^>]*data-slot="%s"[^>]*>' % iid)
        found = pat.findall(html)
        if len(found) == 1:
            html = html.replace(found[0], set_src(found[0], uri), 1)
            kind = "data-slot"
        elif len(found) > 1:
            skipped.append((iid, "data-slot 對到 %d 個" % len(found))); continue
        # 2. 舊版示意插畫位
        if kind is None:
            pat = re.compile(r'<div class="ill">(<svg(?:(?!</svg>).)*</svg>)<span class="tag">[^<]*%s[^<]*</span></div>' % iid, re.S)
            found = list(pat.finditer(html))
            if len(found) == 1:
                m = found[0]
                al = re.search(r'aria-label="([^"]*)"', m.group(1))
                alt = "AI 繪製" + (al.group(1) if al else "示意插畫")
                new = ('<div class="ill"><img src="%s" alt="%s" style="width:100%%;height:100%%;display:block;object-fit:cover">'
                       '<span class="tag">AI 繪製示意插畫</span></div>') % (uri, alt)
                html = html[:m.start()] + new + html[m.end():]
                kind = "示意插畫位"
            elif len(found) > 1:
                skipped.append((iid, "示意插畫位對到 %d 個" % len(found))); continue
        # 3. --map alt
        if kind is None and iid in maps and maps[iid].startswith("alt:"):
            kw = maps[iid][4:]
            pat = re.compile(r'<img\b[^>]*alt="[^"]*%s[^"]*"[^>]*>' % re.escape(kw))
            found = pat.findall(html)
            if len(found) == 1:
                html = html.replace(found[0], set_src(found[0], uri), 1)
                kind = "alt:" + kw
            else:
                skipped.append((iid, "alt「%s」對到 %d 個" % (kw, len(found)))); continue
        if kind is None:
            skipped.append((iid, "找不到位置（網頁沒標記，也沒有 --map）")); continue
        done.append((iid, kind, nbytes // 1024, wh))

    for iid, kind, kb, wh in done:
        print("換 %s ← %s｜%dKB webp %dx%d" % (iid, kind, kb, wh[0], wh[1]))
    for iid, why in skipped:
        print("沒換 %s：%s" % (iid, why))
    print("網頁大小 %.2fMB → %.2fMB" % (size0 / 1e6, len(html) / 1e6))
    if a.dry_run or not done:
        print("（dry-run，未動檔案）" if a.dry_run else "沒有可換的")
        return

    bak = os.path.expanduser("~/Pictures/%s_AI原圖_%s" % (a.slug, datetime.date.today().strftime("%Y%m%d")))
    os.makedirs(bak, exist_ok=True)
    for iid, _, _, _ in done:
        shutil.copy2(srcs[iid], bak)
    open(page, "w", encoding="utf-8").write(html)
    print("已寫入 %s；原始 PNG 備份在 %s" % (page, bak))

    ids = "、".join(i for i, _, _, _ in done)
    msg = "[Mac] 換入 LK888 出的圖 %s（小龍蝦 media/outbound → 網頁）\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" % ids
    run = lambda *c: subprocess.run(c, cwd=repo, capture_output=True, text=True)
    run("git", "add", "index.html")
    r = run("git", "commit", "-q", "-m", msg, "--", "index.html")
    h = run("git", "rev-parse", "--short", "HEAD").stdout.strip()
    print("commit", h, "" if r.returncode == 0 else r.stderr.strip()[:200])
    if not a.no_push:
        r = run("git", "push", "-q")
        print("push", "ok" if r.returncode == 0 else "失敗：" + r.stderr.strip()[:200])


if __name__ == "__main__":
    main()
