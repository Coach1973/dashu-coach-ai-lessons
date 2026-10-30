#!/usr/bin/env python3
"""照「出圖清單 JSON」用 LK888 一次出圖（2026-10-30 教練：出圖清單交給小龍蝦，一行指令跑完，不用再貼）。

清單格式＝教練的「出圖指令表」：JSON 陣列，每筆 id／file／type／ratio／prompt…（見 ai-go/biz-web-inject）。
只做「概念／圖解背景」（純文字生圖）；「實景修飾」要帶參考照片，這支不做，會標出來跳過。
花錢的防線：①走 lk888_guard（同一條 prompt 24 小時只付一次）②輸出夾已有的檔不重出 ③一次最多 12 張 ④失敗不自動重試。

用法：
  python3 run_img_list.py <清單.json> <輸出資料夾> [--dry-run]
完成後在輸出資料夾留下 IMG-00X.png、網頁小圖 IMG-00X.web.webp（長邊 1000／q72，約 50～120KB）與 run_summary.json，並用 notify_coach.sh 回報教練一行結果。
"""
import base64, json, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lk888_guard  # noqa: E402
from generate_industry_chain import get_api_key, LK888_API_URL  # noqa: E402

SIZE = {"16:9": "1536x1024", "4:3": "1536x1024", "3:2": "1536x1024", "4:5": "1024x1536", "3:4": "1024x1536", "1:1": "1024x1024"}
MAX_ITEMS = 12
NOTIFY = Path(__file__).resolve().parent / "notify_coach.sh"


def save_web_copy(png):
    """出圖當下另存網頁小圖（2026-10-30 教練：LK888 的 2～3MB 原圖網頁用不到）；網頁一律放這張，原 PNG 留作備份。"""
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im.thumbnail((1000, 1000), Image.LANCZOS)
    im.save(png.with_suffix(".web.webp"), "WEBP", quality=72, method=6)


def gen(item, out_dir, key):
    f = out_dir / item["file"]
    if f.exists() and f.stat().st_size > 10000:
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


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if len(args) != 2:
        sys.exit(__doc__)
    items = json.loads(Path(args[0]).read_text(encoding="utf-8"))
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
    (out_dir / "run_summary.json").write_text(json.dumps(
        {"ok": [r[0] for r in results], "failed": errors, "skipped": skipped, "out": str(out_dir)}, ensure_ascii=False, indent=1), encoding="utf-8")
    msg = "🖼 出圖清單跑完：成功 %d 張、失敗 %d 張、跳過 %d 張。輸出：%s" % (len(results), len(errors), len(skipped), out_dir)
    subprocess.run([str(NOTIFY), msg], check=False)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
