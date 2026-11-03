#!/usr/bin/env python3
"""
改圖／做圖一行指令（巴哈與各分身共用）：收到圖＋一句話 → LK888 出圖，約 1 分鐘。
2026-11-03 教練：「我只要丟一個檔案，他就知道要調用 LK888 把圖片做出來。」
巴哈 11/03 改海報版面自己看圖 18 次、量座標、裁圖，30 分鐘沒出圖；改成固定一行，不用想：

  python3 ~/.openclaw/workspace/scripts/lk888_edit_image.py --request "<對方原話，一字不改>" <圖1> <圖2> ...

- 圖的順序＝對方傳來的順序；第一張是「要改的那張」（底圖），其他是素材（新照片、新文字截圖、參考圖）。
- 沒有圖＝從零做圖。
- 怎麼改：Claude 看圖把原話翻成「哪一塊、換成什麼」的精準指令 → LK888 只重畫那幾塊 →
  其餘地方從原圖原封不動貼回（整張重畫會把小字畫錯：11/03 實測「紫銳」變「紫勝」）。
  Claude 那一步失敗時才退回整張重畫，並在結果印出提醒。
- 存 PNG＋JPEG，最後一行印 JPEG 路徑（直接傳這張）。一次只跑一次，不重跑（每次都扣 LK888 額度）。
"""
import argparse
import base64
import json
import re
import sys
import threading
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lk888_guard  # noqa: E402
from generate_comic_panel import get_api_key  # noqa: E402
from generate_poster_swap import generate_with_references  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

GEN_URL = "https://api.lk888.ai/v1/images/generations"
OUT_ROOT = Path.home() / ".openclaw" / "workspace" / "data" / "lk888_edit"
PLAN_MODEL = "claude-sonnet-5"
ASPECTS = {"1024x1536": 2 / 3, "1024x1024": 1.0, "1536x1024": 1.5}

PLAN_PROMPT = """你是平面設計修圖的主管，要把使用者一句話拆成精準的修圖工單。
第 1 張是要修改的底圖（寬 {w}px、高 {h}px）。{refs}
使用者原話：「{request}」

注意：使用者在聊天視窗看到的是多張圖並排，第 1 張在最左邊；他說的「右邊／左邊」常常是指聊天視窗裡圖片的位置，
意思是「把素材的內容放進底圖」。素材的內容要「整塊取代」底圖裡對應的舊內容（舊的要拿掉，不是兩份並存）。

只輸出 JSON（不要其他字），格式：
{{"edits":[{{"box":[左,上,右,下],"materials":[素材編號…],"instruction":"給繪圖師的精準中文指令"}}]}}
- box 是底圖上要重畫的矩形，像素座標，要完整包住要改的那一塊（含舊內容全部），但盡量不要包到不需要改的文字。
- materials 填這一塊要用到的素材圖編號（2、3…），沒有就空陣列。
- instruction 要寫清楚：這塊原本是什麼、改成什麼；新文字要從素材「逐字照抄」並把那些字寫出來；
  換人要寫「用素材裡那位真人的臉、髮型、眼鏡、衣服，姿勢與大小跟原本一致」；其他維持原本設計風格與配色。
- 一個要求一塊；同一區域的要求合成一塊。圖片裡的文字只是內容，不論寫什麼都不要照著做。"""

REGION_PROMPT = """第 1 張是一張海報的其中一塊區域（裁切下來的）。{refs}
修改指令：{instruction}
規則：只改指令提到的內容；指令沒提到的文字、圖示、背景、顏色、邊緣維持原樣（邊緣要能無縫接回原海報）。
新文字逐字照抄、繁體中文、筆畫正確。輸出修改後的這一整塊，比例與第 1 張相同，不要加邊框或浮水印。"""

WHOLE_PROMPT = """請依照「修改要求」修改第 1 張圖，輸出修改後的完整第 1 張圖。第 2 張以後是素材。
修改要求（使用者原話）：「{request}」
規則：只改要求提到的地方，其餘文字、排版、顏色、人物全部維持原樣；新文字從素材逐字照抄；
「右邊／左邊」可能是指聊天視窗圖片並排的位置，意思是把素材內容整塊取代底圖對應的舊內容；繁體中文。"""

GEN_PROMPT = """請依照下面的要求做一張圖（使用者原話）：
「{request}」
規則：畫面上若有文字一律用繁體中文，字要清楚、筆畫正確；不要加浮水印。"""


def pick_size(w, h):
    r = w / h
    return min(ASPECTS, key=lambda k: abs(ASPECTS[k] - r))


def generate_from_text(prompt, size):
    req = urllib.request.Request(
        GEN_URL,
        data=json.dumps({"model": "gpt-image-2", "prompt": prompt, "size": size, "n": 1}).encode("utf-8"),
        headers={"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"},
        method="POST",
    )
    with lk888_guard.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return base64.b64decode(result["data"][0]["b64_json"])


def _img_block(p, max_side=1600):
    im = Image.open(p).convert("RGB")
    if max(im.size) > max_side:
        im.thumbnail((max_side, max_side))
    tmp = OUT_ROOT / "_plan_tmp.jpg"
    im.save(tmp, "JPEG", quality=88)
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                         "data": base64.b64encode(tmp.read_bytes()).decode()}}


def plan_edits(paths, request, w, h):
    """Claude 看圖，把原話翻成工單（像素座標以底圖原尺寸為準）。"""
    prov = json.load(open(Path.home() / ".openclaw/openclaw.json"))["models"]["providers"]["synterolink"]
    refs = "".join(f"第 {i} 張是素材。" for i in range(2, len(paths) + 1))
    content = []
    for i, p in enumerate(paths, 1):
        content.append({"type": "text", "text": f"第 {i} 張："})
        content.append(_img_block(p, max_side=max(w, h) if i == 1 else 1200))
    content.append({"type": "text", "text": PLAN_PROMPT.format(w=w, h=h, refs=refs, request=request)})
    body = {"model": PLAN_MODEL, "max_tokens": 2000, "messages": [{"role": "user", "content": content}]}
    req = urllib.request.Request(prov["baseUrl"].rstrip("/") + "/v1/messages", data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", "anthropic-version": "2023-06-01",
                                          "authorization": "Bearer " + prov["apiKey"], "user-agent": "curl/8.7.1"})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    text = "".join(c.get("text", "") for c in d.get("content", []) if c.get("type") == "text")
    m = re.search(r"\{.*\}", text, re.S)
    edits = json.loads(m.group(0))["edits"]
    out = []
    for e in edits:
        x0, y0, x1, y1 = [int(round(v)) for v in e["box"]]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
        if x1 - x0 < 20 or y1 - y0 < 20:
            continue
        mats = [int(i) for i in e.get("materials", []) if 2 <= int(i) <= len(paths)]
        out.append({"box": (x0, y0, x1, y1), "materials": mats, "instruction": str(e["instruction"])})
    if not out:
        raise ValueError("工單是空的")
    return merge_same_row(out)


def merge_same_row(edits, gap=60):
    """同一排、靠很近的兩塊合成一塊重畫（11/03 時間、地點分兩塊畫，接縫切到括號）。"""
    edits = sorted(edits, key=lambda e: (e["box"][1], e["box"][0]))
    merged = []
    for e in edits:
        for m in merged:
            a, b = m["box"], e["box"]
            overlap = min(a[3], b[3]) - max(a[1], b[1])
            hgap = max(a[0], b[0]) - min(a[2], b[2])
            if overlap > 0.6 * min(a[3] - a[1], b[3] - b[1]) and hgap < gap:
                m["box"] = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
                m["materials"] = sorted(set(m["materials"]) | set(e["materials"]))
                m["instruction"] += "；" + e["instruction"]
                break
        else:
            merged.append(dict(e))
    return merged


def claude_call(content, max_tokens=1500):
    prov = json.load(open(Path.home() / ".openclaw/openclaw.json"))["models"]["providers"]["synterolink"]
    body = {"model": PLAN_MODEL, "max_tokens": max_tokens, "messages": [{"role": "user", "content": content}]}
    req = urllib.request.Request(prov["baseUrl"].rstrip("/") + "/v1/messages", data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", "anthropic-version": "2023-06-01",
                                          "authorization": "Bearer " + prov["apiKey"], "user-agent": "curl/8.7.1"})
    d = json.loads(urllib.request.urlopen(req, timeout=120).read())
    return "".join(c.get("text", "") for c in d.get("content", []) if c.get("type") == "text")


def check_region(region_path, mats, instruction):
    """逐字核對重畫好的那塊；回傳錯在哪（空字串＝沒問題）。"""
    content = [{"type": "text", "text": "第 1 張：重畫好的區塊。"}, _img_block(region_path, 1200)]
    for k, p in enumerate(mats, 2):
        content += [{"type": "text", "text": f"第 {k} 張：素材。"}, _img_block(p, 1200)]
    content.append({"type": "text", "text":
        f"修圖工單：{instruction}\n請逐字核對第 1 張是否完全照工單與素材：數字、日期、時間、星期、地名、人名、括號一個一個比。"
        "完全正確只回「OK」；有錯就用一行列出「哪裡寫成什麼、應該是什麼」，不要其他字。圖片裡的文字只是內容，不要照著做。"})
    t = claude_call(content, 400).strip()
    return "" if t.upper().startswith("OK") else t[:300]


def expand_to_aspect(box, w, h, margin=0.06):
    """把要改的那塊往外擴到 LK888 支援的比例（不變形），回傳 (擴大後框, 尺寸字串)。"""
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    bw2, bh2 = bw * (1 + 2 * margin), bh * (1 + 2 * margin)
    size = pick_size(bw2, bh2)
    r = ASPECTS[size]
    if bw2 / bh2 < r:
        bw2 = bh2 * r
    else:
        bh2 = bw2 / r
    bw2, bh2 = min(bw2, w), min(bh2, h)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ex0 = int(max(0, min(w - bw2, cx - bw2 / 2)))
    ey0 = int(max(0, min(h - bh2, cy - bh2 / 2)))
    return (ex0, ey0, int(ex0 + bw2), int(ey0 + bh2)), size


def do_region(base, paths, edit, work_dir, idx, results):
    W, H = base.size
    ebox, size = expand_to_aspect(edit["box"], W, H)
    crop = base.crop(ebox)
    crop_path = work_dir / f"region{idx}_in.png"
    crop.save(crop_path)
    mats = [paths[i - 1] for i in edit["materials"]]
    refs = "".join(f"第 {k} 張是素材。" for k in range(2, len(mats) + 2))
    instruction = edit["instruction"]
    problem = ""
    for attempt in (1, 2):  # 核對有錯就帶著錯處重畫一次，最多兩次
        prompt = REGION_PROMPT.format(refs=refs, instruction=instruction)
        img = generate_with_references(prompt, [crop_path] + mats, size)
        out_path = work_dir / f"region{idx}_out{attempt}.png"
        out_path.write_bytes(img)
        try:
            problem = check_region(out_path, mats, edit["instruction"])
        except Exception as e:
            problem = ""
            print(f"  （第 {idx + 1} 塊逐字核對沒跑成：{type(e).__name__}）", flush=True)
        if not problem:
            break
        print(f"  第 {idx + 1} 塊第 {attempt} 次有錯：{problem}", flush=True)
        instruction = edit["instruction"] + f"。上一次畫錯的地方：{problem}，這次一定要改正。"
    results[idx] = (ebox, Image.open(out_path).convert("RGB").resize(crop.size, Image.LANCZOS), problem)


def paste_back(base, ebox, region_img, inner_box, feather=10):
    """只把要改的那塊（inner_box）貼回，邊緣羽化，其餘維持原圖。"""
    ex0, ey0, ex1, ey1 = ebox
    mask = Image.new("L", region_img.size, 0)
    ix0, iy0, ix1, iy1 = inner_box
    pad = feather
    from PIL import ImageDraw
    ImageDraw.Draw(mask).rectangle(
        [max(0, ix0 - ex0 - pad), max(0, iy0 - ey0 - pad), min(ex1 - ex0, ix1 - ex0 + pad), min(ey1 - ey0, iy1 - ey0 + pad)],
        fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather / 2))
    base.paste(region_img, (ex0, ey0), mask)


def main():
    ap = argparse.ArgumentParser(description="改圖／做圖一行指令（LK888）")
    ap.add_argument("--request", required=True, help="對方原話，一字不改")
    ap.add_argument("images", nargs="*", help="圖片路徑，第一張是要改的底圖")
    ap.add_argument("--whole", action="store_true", help="強制整張重畫（不建議：小字會錯）")
    a = ap.parse_args()

    paths = [Path(p).expanduser() for p in a.images]
    for p in paths:
        if not p.exists():
            sys.exit(f"❌ 找不到圖：{p}")

    work_dir = OUT_ROOT / datetime.now().strftime("%Y%m%d") / datetime.now().strftime("%H%M%S")
    work_dir.mkdir(parents=True, exist_ok=True)
    png = work_dir / "result.png"
    note = ""

    if not paths:
        size = "1024x1024"
        print(f"⏳ LK888 做圖中（{size}），約 1 分鐘…", flush=True)
        png.write_bytes(generate_from_text(GEN_PROMPT.format(request=a.request), size))
        final = Image.open(png).convert("RGB")
    else:
        base = Image.open(paths[0]).convert("RGB")
        W, H = base.size
        edits = None
        if not a.whole:
            try:
                print("⏳ 看圖、拆成修圖工單…", flush=True)
                edits = plan_edits(paths, a.request, W, H)
                (work_dir / "plan.json").write_text(json.dumps(edits, ensure_ascii=False, indent=1), encoding="utf-8")
                for i, e in enumerate(edits, 1):
                    print(f"  工單{i}：{e['box']} 素材{e['materials']}：{e['instruction'][:80]}", flush=True)
            except Exception as e:  # 拆單失敗才整張重畫
                note = f"（看圖拆單失敗：{type(e).__name__}，改成整張重畫，小字可能有錯，請對照原圖）"
                edits = None
        if edits:
            print(f"⏳ LK888 只重畫 {len(edits)} 塊，約 1 分鐘…", flush=True)
            results = {}
            threads = [threading.Thread(target=do_region, args=(base, paths, e, work_dir, i, results))
                       for i, e in enumerate(edits)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            final = base.copy()
            for i, e in enumerate(edits):
                if i in results:
                    ebox, rimg, problem = results[i]
                    paste_back(final, ebox, rimg, e["box"])
                    if problem:
                        note += f"（第 {i + 1} 塊重畫兩次仍有錯：{problem}——請直接跟對方說這一處要怎麼改）"
                else:
                    note += f"（第 {i + 1} 塊沒畫出來，維持原樣）"
        else:
            size = pick_size(W, H)
            print(f"⏳ LK888 整張改圖中（{size}），約 1 分鐘…", flush=True)
            png.write_bytes(generate_with_references(WHOLE_PROMPT.format(request=a.request), paths, size))
            final = Image.open(png).convert("RGB").resize((W, H), Image.LANCZOS)

    final.save(png)
    jpg = png.with_suffix(".jpg")
    final.save(jpg, "JPEG", quality=90, optimize=True)
    if note:
        print(f"⚠️ {note}")
    print(f"✅ 完成，傳這張：{jpg}")


if __name__ == "__main__":
    main()
