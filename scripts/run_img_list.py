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
import base64, html, json, re, shutil, subprocess, sys, time, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lk888_guard  # noqa: E402
from generate_industry_chain import get_api_key, LK888_API_URL  # noqa: E402

SIZE = {"16:9": "1536x1024", "4:3": "1536x1024", "3:2": "1536x1024", "4:5": "1024x1536", "3:4": "1024x1536", "1:1": "1024x1024"}
MAX_ITEMS = 12
NOTIFY = Path(__file__).resolve().parent / "notify_coach.sh"
COACH_CHAT_ID = "6124913915"
TESSERACT = shutil.which("tesseract") or "/opt/homebrew/bin/tesseract"


def load_items(src):
    """網址：抓頁面，取出 <pre> 裡那段 JSON 陣列；檔案：直接讀。"""
    if not src.startswith("http"):
        return json.loads(Path(src).read_text(encoding="utf-8"))
    req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8", "replace")
    for block in re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S):
        try:
            data = json.loads(html.unescape(re.sub(r"<[^>]+>", "", block)))
        except ValueError:
            continue
        if isinstance(data, list) and data and all(isinstance(x, dict) and "prompt" in x for x in data):
            return data
    sys.exit("網頁裡找不到出圖清單 JSON：%s" % src)


def save_web_copy(png):
    """出圖當下另存網頁小圖（2026-10-30 教練：LK888 的 2～3MB 原圖網頁用不到）；網頁一律放這張，原 PNG 留作備份。"""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im.thumbnail((1000, 1000), Image.LANCZOS)
    im.save(png.with_suffix(".web.webp"), "WEBP", quality=72, method=6)


def gen(item, out_dir, key):
    f = out_dir / item["file"]
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
    items = load_items(args[0])
    for it in items:
        it.setdefault("file", it["id"] + ".png")
    out_dir = Path(args[1]); out_dir.mkdir(parents=True, exist_ok=True)
    if len(items) > MAX_ITEMS:
        sys.exit("清單 %d 張，超過一次上限 %d 張，請教練確認後分批" % (len(items), MAX_ITEMS))
    todo, skipped = [], []
    for it in items:
        if it.get("type") not in ("概念", "圖解背景"):
            skipped.append((it["id"], "類型是「%s」，需要參考照片，這支不處理" % it.get("type")))
        elif it.get("ratio") not in SIZE:
            skipped.append((it["id"], "比例 %s 不支援" % it.get("ratio")))
        else:
            todo.append(it)
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
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(gen, it, out_dir, key): it for it in todo}
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
    if done:
        sheet = out_dir / "contact-sheet.jpg"
        contact_sheet(done, sheet)
        zip_path = out_dir / "images.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in done:
                web = p.with_suffix(".web.webp")
                if not web.exists():
                    save_web_copy(p)
                    web = p.with_suffix(".web.webp")
                # 只放網頁用壓縮圖（教練 2026-10-24「1MB 以內就夠」＋10/30「可以壓縮、清晰可見、不要模糊」）。
                # 原圖 PNG 留在本機當備份，不進 zip——網頁用不到，進去只會把包裹撐到 10MB 以上。
                z.write(web, p.stem + ".webp")
        big = [(n, i.file_size) for n, i in zipfile.ZipFile(zip_path).infolist() if i.file_size > 1_000_000]
        if big:
            print("  ⚠️ 超過 1MB 的檔案：", big)
    minutes = (time.time() - t_start) / 60
    (out_dir / "run_summary.json").write_text(json.dumps(
        {"ok": sorted(ok_ids), "failed": errors, "skipped": skipped, "ocr": qa,
         "minutes": round(minutes, 1), "out": str(out_dir)}, ensure_ascii=False, indent=1), encoding="utf-8")
    caption = "🖼 出圖完成：成功 %d 張、失敗 %d 張、跳過 %d 張（%.0f 分鐘）\n%s" % (
        len(results), len(errors), len(skipped), minutes, "\n".join("%s：%s" % kv for kv in qa.items()))
    for i, why in errors + skipped:
        caption += "\n%s：%s" % (i, why[:80])
    sent = False
    if send and sheet:
        sent = tg_send("sendPhoto", "photo", sheet, caption) and tg_send("sendDocument", "document", zip_path, "網頁用圖（已壓縮，每張 1MB 以內）")
    if send and not sent:
        subprocess.run([str(NOTIFY), caption + "\n輸出：%s" % out_dir], check=False)
    print("📨 已傳教練 Telegram" if sent else "📨 沒有傳圖（%s）" % ("--no-send" if not send else "傳送失敗或沒有圖，已改發文字通知"))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
