#!/usr/bin/env python3
"""照「出圖清單」用 LK888 一次出圖，出完當場把一覽圖＋zip 傳給教練（2026-10-30 教練：出圖清單交給小龍蝦，一行指令跑完，不用再貼）。

清單來源二選一：
  ①出圖清單網頁網址（例 https://www.tava-ai.com/ivs5j0rts2/image-list.html，程式自己讀頁面最下方的 JSON）
  ②JSON 檔：陣列，每筆 id／type／ratio／prompt（file 可省略，預設 <id>.png；見 ai-go/biz-web-inject）。
只做「概念／圖解背景」（純文字生圖）；「實景修飾」要帶參考照片，這支不做，會標出來跳過。
花錢的防線：①走 lk888_guard（同一條 prompt 24 小時只付一次）②輸出夾已有的檔不重出 ③一次最多 12 張 ④失敗不自動重試。

2026-11-02 教練：「這麼簡單的事要做這麼久？」——蔡佩茹 3 張圖 12:59 就出好，小龍蝦又自己寫三版 AI 看圖檢查拖了 20 多分鐘沒交。
從此寫死在程式裡：出完只做一次 OCR 文字檢查（看有沒有多餘文字），結果寫在說明裡，不重跑、不再叫 AI 看圖，當場交圖。

用法：
  python3 run_img_list.py <網址或清單.json> <輸出資料夾> [--dry-run] [--no-send]
完成後輸出資料夾有 IMG-00X.png（原圖，留本機備份）、網頁小圖 IMG-00X.web.webp（長邊 1000／q72）、contact-sheet.jpg、images.zip、run_summary.json；
images.zip 內**只有**網頁用壓縮圖（檔名 IMG-00X.webp，每張 1MB 以內）——原圖 PNG 不進 zip（教練 2026-10-24「1MB 以內就夠」、10-30「可以壓縮，清晰可見，不要模糊」）；
並用 bot_main 直接傳一覽圖＋zip 到教練 Telegram 私聊（--no-send 只產檔不傳）。
"""
import base64, html, json, re, shutil, subprocess, sys, time, urllib.request, uuid, zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lk888_guard  # noqa: E402
from generate_industry_chain import get_api_key, LK888_API_URL  # noqa: E402

SIZE = {"16:9": "1536x1024", "4:3": "1536x1024", "3:2": "1536x1024", "4:5": "1024x1536", "3:4": "1024x1536", "1:1": "1024x1024"}
MAX_ITEMS = 12
EDIT_ENDPOINT = "https://api.lk888.ai/v1/images/edits"
NOTIFY = Path(__file__).resolve().parent / "notify_coach.sh"
COACH_CHAT_ID = "6124913915"
TESSERACT = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"


def normalize_items(data):
    """把清單每筆的正規化：prompt 欄位可能是 prompt / en（英文指令），比例可能是 ratio / aspect / size。"""
    out = []
    for x in data:
        if not isinstance(x, dict):
            continue
        it = dict(x)
        if not it.get("prompt"):
            for k in ("en", "english", "英文指令", "prompt_en"):
                if it.get(k):
                    it["prompt"] = it[k]
                    break
        if not it.get("ratio"):
            for k in ("aspect", "aspectRatio", "size", "比例"):
                if it.get(k):
                    it["ratio"] = it[k]
                    break
        if not it.get("id"):
            it["id"] = it.get("file") or "IMG-%03d" % (len(out) + 1)
        if not it.get("type") and not it.get("kind"):
            it["type"] = "概念"
        if it.get("prompt"):
            out.append(it)
    return out


def load_items(src):
    """網址：抓頁面，取出 <pre> 裡那段 JSON 陣列；檔案：直接讀。
    2026-11-05 康牧師清單：JSON 欄位是 en／zh（沒有 prompt），所以要放寬抓法。"""
    if not src.startswith("http"):
        return normalize_items(json.loads(Path(src).read_text(encoding="utf-8")))
    req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8", "replace")
    for block in re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S):
        try:
            data = json.loads(html.unescape(re.sub(r"<[^>]+>", "", block)))
        except ValueError:
            continue
        if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
            items = normalize_items(data)
            if items:
                return items
    # 2026-11-07 TAVA 女性個人IP課程 prompts.html：清單在 <script> 的 JS 陣列 const items=[{id,file,ratio,p:'…'}]（11/03 是 const P=[[…]]）。
    # 用 node 把陣列轉成 JSON（只對頁面裡抓出的那段陣列求值），欄位 p 當 prompt，沒寫 type 一律當「概念」。
    for m in re.finditer(r"const\s+items\s*=\s*(\[[\s\S]*?\n\s*\]);", page):
        try:
            r = subprocess.run(["node", "-e", "process.stdout.write(JSON.stringify(eval(process.argv[1])))", m.group(1)],
                               capture_output=True, text=True, timeout=20)
            data = json.loads(r.stdout) if r.returncode == 0 else None
        except Exception:
            data = None
        if isinstance(data, list) and data and all(isinstance(x, dict) for x in data):
            for x in data:
                if not x.get("prompt") and x.get("p"):
                    x["prompt"] = x["p"]
            items = normalize_items(data)
            if items:
                return items
    sys.exit("網頁裡找不到出圖清單 JSON：%s" % src)


def probe_page(src):
    """診斷模式：只印出圖清單頁的結構（有哪些標籤、JSON 藏在哪），不出圖、不扣點。
    2026-11-05 康牧師清單：<pre> 裡沒有 JSON，需要知道頁面長什麼樣才修 parser。"""
    req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8", "replace")
        status = resp.status
    print("HTTP", status, "len", len(page))
    print("有 <pre>:", "<pre" in page, "｜<script> 數:", len(re.findall(r"<script", page)))
    for m in re.finditer(r"<script([^>]*)>", page):
        print("  script:", (m.group(1) or "").strip()[:140])
    print("關鍵字次數：prompt=%d  IMG-=%d  ratio=%d  [ =%d" % (
        page.count("prompt"), len(re.findall(r"IMG-\d+", page)), page.count("ratio"), page.count("[")))
    for kw in ("prompt", "IMG-", "ratio"):
        i = page.find(kw)
        if i >= 0:
            print("  關鍵字 %s 首現位置 %d，前後 200 字：%s" % (kw, i, page[max(0, i - 200):i + 200].replace("\n", " ")))
    tail = page[-600:].replace("\n", " ")
    print("頁尾 600 字：", tail)


def save_web_copy(png):
    """出圖當下另存網頁小圖（2026-10-30 教練：LK888 的 2～3MB 原圖網頁用不到）；網頁一律放這張，原 PNG 留作備份。"""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im.thumbnail((1000, 1000), Image.LANCZOS)
    im.save(png.with_suffix(".web.webp"), "WEBP", quality=72, method=6)


PKG_MAX_FILE = 1_000_000   # 教練 2026-10-24「1MB 以內就夠」
PKG_MAX_TOTAL = 3_000_000  # 一包 12 張小圖約 1MB；超過 3MB 一定是夾到原圖


def build_zip(pngs, zip_path):
    """包裹只放網頁用小圖 IMG-00X.webp（教練 10/24「1MB 以內就夠」、10/30「可以壓縮，清晰可見，不要模糊」）；原圖 PNG 留本機備份。"""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in pngs:
            web = p.with_suffix(".web.webp")
            if not web.exists():
                save_web_copy(p)
            z.write(web, p.stem + ".webp")


def package_problems(zip_path):
    """交付前自我審查：拿教練定的規格檢查成品，不合就回傳原因（空清單＝合格）。"""
    infos = zipfile.ZipFile(zip_path).infolist()
    out = ["%s 不是網頁小圖（只准 .webp）" % i.filename for i in infos if not i.filename.endswith(".webp")]
    out += ["%s 有 %.1fMB，超過 1MB" % (i.filename, i.file_size / 1e6) for i in infos if i.file_size > PKG_MAX_FILE]
    total = Path(zip_path).stat().st_size
    if total > PKG_MAX_TOTAL:
        out.append("整包 %.1fMB，超過 %dMB" % (total / 1e6, PKG_MAX_TOTAL // 1_000_000))
    return out


def gen(item, out_dir, key):
    f = out_dir / item["file"]
    f.parent.mkdir(parents=True, exist_ok=True)  # 2026-11-09 清單檔名可能帶子資料夾（images/img-001.webp），先建好
    if f.exists() and f.stat().st_size > 10000:
        if not f.with_suffix(".web.webp").exists():
            save_web_copy(f)
        return item["id"], "已存在，跳過（不重複扣點）", f.stat().st_size
    payload = json.dumps({"model": "gpt-image-2", "prompt": item["prompt"], "size": SIZE[item["ratio"]]}).encode()
    req = urllib.request.Request(LK888_API_URL, data=payload, method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.time()
    with lk888_guard.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read().decode())
    f.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    save_web_copy(f)
    return item["id"], "完成 %d 秒" % (time.time() - t0), f.stat().st_size


def ref_filename(item):
    """從 ref 欄位抓出參考照片檔名（例：'p001.jpg（周良敦書房揮毫照，原始照片資料夾）' → 'p001.jpg'）。"""
    m = re.search(r"([A-Za-z0-9_\-]+\.(?:jpg|jpeg|png|webp))", (item.get("ref") or ""), re.I)
    return m.group(1) if m else None


def find_ref(item, out_dir):
    """找參考照片：先看輸出資料夾的 refs/，再看已上架 zip 裡的「原始照片/」。找不到回 None。"""
    name = ref_filename(item)
    if not name:
        return None
    local = out_dir / "refs" / name
    if local.exists():
        return local
    flat = out_dir / name
    if flat.exists():
        return flat
    processed = Path("/Users/bymyway/.openclaw/workspace/event-signup/curation_uploads/processed")
    zips = sorted(processed.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)[:6]
    for zp in zips:
        try:
            with zipfile.ZipFile(zp) as z:
                hits = [n for n in z.namelist() if n.rsplit("/", 1)[-1] == name]
                if not hits:
                    continue
                local.parent.mkdir(parents=True, exist_ok=True)
                with z.open(hits[0]) as f, open(local, "wb") as o:
                    shutil.copyfileobj(f, o)
                print("  參考照片取自 %s → %s" % (zp.name, local))
                return local
        except (zipfile.BadZipFile, OSError):
            continue
    return None


def build_edit_prompt(item, ref_name):
    """實景修飾：以真實照片為底，把清單描述的場景畫進去；保留真人與真實場域。"""
    base = (item.get("prompt") or "").strip()
    return (
        "Reference photo %s — build the scene below from this real photograph. "
        "Keep the real person (identity, face, age, hairstyle, clothing) and the real room of the reference photo, "
        "and render the described moment photorealistically, as if it really happened in that room, "
        "same camera feel, natural warm lighting, no illustration look.\n\n"
        "Scene: %s\n\n"
        "Do not add: any watermark, logo, signature, caption, banner or readable text overlay; "
        "no deformed hands, no extra fingers, no duplicated objects." % (ref_name, base)
    )


def gen_edit(item, out_dir, key, ref_path):
    """實景修飾：走 LK888 /v1/images/edits（multipart，帶參考照片）。"""
    f = out_dir / item["file"]
    f.parent.mkdir(parents=True, exist_ok=True)  # 2026-11-09 清單檔名可能帶子資料夾（images/img-001.webp），先建好
    if f.exists() and f.stat().st_size > 10000:
        if not f.with_suffix(".web.webp").exists():
            save_web_copy(f)
        return item["id"], "已存在，跳過（不重複扣點）", f.stat().st_size
    boundary = uuid.uuid4().hex
    parts = []

    def field(name, value):
        parts.append(("--%s" % boundary).encode())
        parts.append(('Content-Disposition: form-data; name="%s"' % name).encode())
        parts.append(b"")
        parts.append(value.encode("utf-8") if isinstance(value, str) else value)

    with open(ref_path, "rb") as fp:
        img = fp.read()
    parts.append(("--%s" % boundary).encode())
    parts.append(('Content-Disposition: form-data; name="image"; filename="%s"' % ref_path.name).encode())
    parts.append(b"Content-Type: image/jpeg")
    parts.append(b"")
    parts.append(img)
    field("prompt", build_edit_prompt(item, ref_path.name))
    field("model", "gpt-image-2")
    field("size", SIZE[item["ratio"]])
    field("n", "1")
    parts.append(("--%s--" % boundary).encode())
    parts.append(b"")
    body = b"\r\n".join(parts)
    req = urllib.request.Request(EDIT_ENDPOINT, data=body, method="POST",
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": f"multipart/form-data; boundary={boundary}"})
    t0 = time.time()
    with lk888_guard.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read().decode())
    f.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    save_web_copy(f)
    return item["id"], "完成 %d 秒（實景修飾）" % (time.time() - t0), f.stat().st_size


def ocr_check(png):
    """唯一一次檢查：灰階＋二值化後 OCR，抓多餘文字／浮水印。讀到字就回那幾個字，空的＝乾淨。"""
    from PIL import Image
    tmp = png.with_suffix(".ocr.png")
    try:
        Image.open(png).convert("L").point(lambda p: 255 if p > 140 else 0).save(tmp)
        out = subprocess.run([TESSERACT, str(tmp), "stdout", "-l", "chi_tra+eng"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception as e:  # 檢查壞了不擋交圖
        return "檢查沒跑成（%s）" % type(e).__name__
    finally:
        tmp.unlink(missing_ok=True)
    words = re.findall(r"[A-Za-z]{3,}|[一-鿿]{2,}|\d{3,}", out)
    return "疑似有字：" + " ".join(words[:6]) if words else "無多餘文字"


def contact_sheet(pngs, dst):
    from PIL import Image, ImageDraw
    thumbs = []
    for p in pngs:
        im = Image.open(p).convert("RGB")
        im.thumbnail((640, 640), Image.LANCZOS)
        thumbs.append((p.stem, im))
    cols = min(3, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    cw, ch = 660, max(im.height for _, im in thumbs) + 50
    sheet = Image.new("RGB", (cols * cw, rows * ch), (244, 241, 236))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(thumbs):
        x, y = (i % cols) * cw + 10, (i // cols) * ch + 10
        d.text((x, y), name, fill=(60, 60, 60))
        sheet.paste(im, (x, y + 30))
    sheet.save(dst, "JPEG", quality=85)


def tg_send(method, field, path, caption):
    """直接用 bot_main 打 Telegram API（理由同 notify_coach.sh：CLI 從腳本跑讀不到 token）。"""
    token = json.load(open("/Users/bymyway/.openclaw/openclaw.json"))["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
    out = subprocess.run(["curl", "-s", "--max-time", "120", "https://api.telegram.org/bot%s/%s" % (token, method),
                          "-F", "chat_id=" + COACH_CHAT_ID, "-F", "caption=" + caption[:1000], "-F", "%s=@%s" % (field, path)],
                         capture_output=True, text=True).stdout
    return '"ok":true' in out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    send = "--no-send" not in sys.argv
    if len(args) != 2:
        sys.exit(__doc__)
    t_start = time.time()
    if "--probe" in sys.argv:
        probe_page(args[0])
        return
    items = load_items(args[0])
    if "--dump-items" in sys.argv:
        # 診斷用：只印欄位結構，不出圖、不扣點
        for it in items:
            print("==== %s ====" % it.get("id"))
            for k, v in it.items():
                if k == "prompt":
                    print("   prompt: %s" % (v or "")[:400].replace("\n", " "))
                else:
                    print("   %s: %r" % (k, v))
        sys.exit(0)
    for it in items:
        it.setdefault("file", it["id"] + ".png")
    out_dir = Path(args[1]); out_dir.mkdir(parents=True, exist_ok=True)
    if len(items) > MAX_ITEMS:
        sys.exit("清單 %d 張，超過一次上限 %d 張，請教練確認後分批" % (len(items), MAX_ITEMS))
    todo, skipped = [], []
    for it in items:
        kind = it.get("type") or it.get("kind")  # 2026-11-03 江瑞祥清單用 kind 欄位
        if it.get("ratio") not in SIZE:
            skipped.append((it["id"], "比例 %s 不支援" % it.get("ratio")))
        elif str(kind or "").startswith(("概念", "圖解背景")):  # 「概念（之後可換成本人照片）」也算概念
            todo.append(it)
        elif kind in ("實景修飾", "實景修圖", "修飾"):
            ref = find_ref(it, out_dir)  # 2026-11-06 周良敦 IMG-004：參考照片在已上架 zip 的「原始照片/」
            if not ref and not str(it.get("ref") or "").strip():
                # 2026-11-11 金門 kinmen-1205：13 張「實景修飾」參考照片欄空白＝本來就沒有照片，不准停下來跟教練要，當概念圖直接出
                it["type"] = "概念"
                todo.append(it)
            elif not ref:
                skipped.append((it["id"], "實景修飾但找不到參考照片（%s）" % (it.get("ref") or "未指定")))
            else:
                it["_ref"] = ref
                todo.append(it)
        else:
            skipped.append((it["id"], "類型是「%s」，這支不處理" % kind))
    print("清單 %d 張：要出 %d 張，跳過 %d 張；輸出到 %s" % (len(items), len(todo), len(skipped), out_dir))
    for i, why in skipped:
        print("  跳過", i, why)
    for it in todo:
        print("  %s  %s  %s  %s" % (it["id"], it["ratio"], SIZE[it["ratio"]], it["file"]))
    if dry:
        print("（--dry-run：沒有呼叫 LK888，沒有扣點）")
        return
    key = get_api_key()
    results, errors = [], []
    def run_one(it):
        if it.get("_ref"):
            return gen_edit(it, out_dir, key, it["_ref"])
        return gen(it, out_dir, key)

    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(run_one, it): it for it in todo}
        for fu, it in futs.items():
            try:
                results.append(fu.result())
            except Exception as e:  # 不重試，失敗要講出來
                errors.append((it["id"], "%s: %s" % (type(e).__name__, str(e)[:200])))
    for r in results:
        print("  ✅", r[0], r[1], "%d KB" % (r[2] // 1024))
    for e in errors:
        print("  ❌", e[0], e[1])

    ok_ids = {r[0] for r in results}
    done = [out_dir / it["file"] for it in todo if it["id"] in ok_ids]
    qa = {p.stem: ocr_check(p) for p in done}
    for k, v in qa.items():
        print("  🔎", k, v)
    sheet = zip_path = None
    problems = []
    if done:
        sheet = out_dir / "contact-sheet.jpg"
        contact_sheet(done, sheet)
        zip_path = out_dir / "images.zip"
        build_zip(done, zip_path)
        problems = package_problems(zip_path)
        for pr in problems:
            print("  🚫", pr)
    minutes = (time.time() - t_start) / 60
    (out_dir / "run_summary.json").write_text(json.dumps(
        {"ok": sorted(ok_ids), "failed": errors, "skipped": skipped, "ocr": qa,
         "minutes": round(minutes, 1), "out": str(out_dir)}, ensure_ascii=False, indent=1), encoding="utf-8")
    caption = "🖼 出圖完成：成功 %d 張、失敗 %d 張、跳過 %d 張（%.0f 分鐘）\n%s" % (
        len(results), len(errors), len(skipped), minutes, "\n".join("%s：%s" % kv for kv in qa.items()))
    for i, why in errors + skipped:
        caption += "\n%s：%s" % (i, why[:80])
    sent = False
    if problems:  # 交付前自我審查沒過：不傳不合規的包裹，改發文字講清楚哪裡不合
        caption += "\n🚫 包裹沒通過交付檢查，沒有傳：" + "；".join(problems)
    elif send and sheet:
        sent = tg_send("sendPhoto", "photo", sheet, caption) and tg_send("sendDocument", "document", zip_path, "網頁用圖（已壓縮，每張 1MB 以內）")
    if send and not sent:
        subprocess.run([str(NOTIFY), caption + "\n輸出：%s" % out_dir], check=False)
    print("📨 已傳教練 Telegram" if sent else "📨 沒有傳圖（%s）" % ("--no-send" if not send else "傳送失敗或沒有圖，已改發文字通知"))
    # 2026-11-10 朱志成頁：出圖完要換進「已上架」的網頁，網址不用教練給——從清單網址的人名 slug 查上架登記，直接印出網址與倉庫
    try:
        import re as _re
        m = _re.search(r"tava-ai\.com/[^/]+/([^/]+)/", args[0])
        if m:
            reg = json.loads((Path(__file__).resolve().parent.parent / "event-signup" / "curated_sites_registry.json").read_text(encoding="utf-8"))
            sites = reg if isinstance(reg, list) else reg.get("sites", reg.get("items", []))
            hit = [x for x in sites if isinstance(x, dict) and x.get("slug") == m.group(1)]
            if hit:
                print("🔗 這個網頁已上架：%s｜倉庫 ~/github_repos/%s/｜圖位是 <img data-slot=IMG-編號>，直接換進該倉庫 index.html 並 push，不要只改本機、不要問教練網址" % (hit[0].get("event_url"), m.group(1)))
            else:
                print("🔗 上架登記查無 slug=%s；先查 curation_uploads/processed 再說，不要對教練說沒權限" % m.group(1))
    except Exception as e:
        print("🔗 查上架登記失敗：%s" % e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
