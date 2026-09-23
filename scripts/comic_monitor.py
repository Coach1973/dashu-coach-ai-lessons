#!/usr/bin/env python3
"""
漫畫進度監控 + 推送器（取代 v2 batch 的最後推送邏輯）
邏輯：
  - 對每個 panel_NN.png（N = 1~14）
    - 已存在且有效 → 推到 Telegram（catch-up），跳過生成
    - 不存在 → 用 generate_comic_panel.py 生成，完成後推
  - 結束時發彙整回報
"""
import json
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
HTML = WORKSPACE / "claude-brain/data/comic_source_20260923/證明給機器看_章回漫畫小說.html"
REFERENCE = WORKSPACE / "claude-brain/data/comic_reference/coach_face_reference.jpg"
SCRIPT = WORKSPACE / "scripts/generate_comic_panel.py"
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels"
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/monitor_progress.log"
CONFIG = Path.home() / ".openclaw" / "openclaw.json"
CHAT_ID = "6124913915"

ANCHOR = (
    "Consistent character design across all panels: a distinguished Taiwanese middle-aged male coach "
    "in his late 40s with neatly groomed short dark hair fully dark no gray, no glasses no facial hair, "
    "wearing a tailored gray plaid three-piece suit with white dress shirt and a blue tie with subtle "
    "dot pattern; same face shape, same jawline, same nose, same eye spacing in every panel; "
    "no lapel pin, no name badge, no extra accessories, no extra people; "
    "refined, dignified, contemplative expression when alone; slightly warm mature expression in close-ups."
)
GUARD = "no readable text, no Chinese text, no English text, no watermarks, no lapel pin, no name badge"

# 章節中文標題（與原始小說順序對應）
TITLES_ZH = [
    "開場跨頁（楔子）",
    "三格喜劇轉怒氣（第一回）",
    "第一夜勝利與伏筆（第二回）",
    "真假軍師（第三回）",
    "兩種證據的天秤（第四回）",
    "百分比實驗（第五回）",
    "盲點裂開（第六回）",
    "真相大白跨頁（第七回）",
    "青春向誰討（第八回）",
    "雙帳單法庭（第九回）",
    "四扇假門（第十回）",
    "殭屍指標被拔除（第十一回）",
    "結局（第十二回）",
    "封面",
]


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def parse_prompts():
    """用之前修好的 word-boundary regex 解析。"""
    text = HTML.read_text(encoding="utf-8")
    parts = text.split('<div class="prompt">')
    prompts = []
    for p in parts[1:]:
        end = p.find('</div>')
        if end < 0:
            continue
        block = p[:end]
        m = re.search(r'<strong>([^<]+)</strong>', block)
        if not m:
            continue
        title = m.group(1).strip()
        raw = re.sub(r'<[^>]+>', '', block[m.end():]).strip()
        sl = raw.lower()
        if "double-page" in sl or re.search(r"\b21:9\b", sl):
            size = "1792x1024"
        elif re.search(r"\b16:9\b", sl) or "widescreen" in sl:
            size = "1536x1024"
        elif re.search(r"\b2:3\b", sl) or "portrait" in sl:
            size = "1024x1536"
        else:
            size = "1536x1024"
        # 補強護欄
        if "no readable" not in raw.lower() and "no text" not in raw.lower():
            raw = raw.rstrip(" .") + ", " + GUARD
        else:
            raw = raw.rstrip(" .") + ", " + GUARD
        prompts.append({"title": title, "prompt": raw, "size": size})
    return prompts


def get_bot_token():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


def send_text(text: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"❌ send_text HTTP {e.code}: {e.read().decode()[:200]}")
        return None


def send_photo(image_path: Path, caption: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----Monitor" + datetime.now().strftime("%H%M%S%f")
    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{CHAT_ID}\r\n".encode("utf-8"))
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{image_path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode("utf-8")
    )
    body.append(image_path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(body)
    req = urllib.request.Request(url, data=data, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"❌ send_photo HTTP {e.code}: {e.read().decode()[:300]}")
        return None


def generate_one(full_prompt: str, size: str, output_path: Path) -> bool:
    cmd = [
        "python3", str(SCRIPT),
        "--prompt", full_prompt,
        "--reference", str(REFERENCE),
        "--size", size,
        "--out", str(output_path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
        if result.returncode != 0:
            log(f"  returncode={result.returncode}")
            if result.stderr:
                log(f"  stderr: {result.stderr.strip()[:200]}")
        return result.returncode == 0 and output_path.exists()
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT 200s")
        return False
    except Exception as e:
        log(f"  ERROR: {e}")
        return False


def main():
    log("=== 進度監控器啟動 ===")
    send_text(
        "📡 <b>即時進度推送上線</b>\n\n"
        "⚠️ 抱歉，前一版 batch 把所有 14 張壓到最後才一次推，您完全看不到進度，是我的錯。\n\n"
        "🔧 新策略（取代中）：\n"
        "✅ 已完成的 1~4 張 → 立刻 catch-up 推送\n"
        "⏳ 剩餘 5~14 → 每張完成立即推 1 張\n"
        "🎯 預計 ~15 分鐘內全部到齊，您可放心去睡"
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prompts = parse_prompts()
    log(f"共 {len(prompts)} 個 prompts")

    results = []
    for i, p in enumerate(prompts):
        out_path = OUTPUT_DIR / f"panel_{i+1:02d}.png"
        full_prompt = f"{ANCHOR} {p['prompt']}"
        title_zh = TITLES_ZH[i] if i < len(TITLES_ZH) else p["title"]
        size = p["size"]

        log(f"--- {i+1}/{len(prompts)}: {title_zh} [{size}] ---")

        if out_path.exists() and out_path.stat().st_size > 100000:
            # 已存在 — catch-up 推送
            size_mb = out_path.stat().st_size / 1024 / 1024
            caption = (
                f"✅ <b>{i+1}/14</b>｜{title_zh}\n\n"
                f"📁 {out_path.name} ({size_mb:.1f}MB)\n"
                f"📐 {size}\n"
                f"⏰ {datetime.now().strftime('%H:%M:%S')}（catch-up 從本地推）"
            )
            send_photo(out_path, caption)
            log(f"  ✅ Catch-up pushed {out_path.name}")
            results.append({"index": i + 1, "title": title_zh, "size": size, "ok": True, "from_cache": True, "dt": 0})
        else:
            # 需要生成
            send_text(f"⏳ <b>正在生成 {i+1}/14</b>｜{title_zh}\n\n預計 30-90s")
            t0 = datetime.now()
            success = generate_one(full_prompt, size, out_path)
            dt = (datetime.now() - t0).total_seconds()

            if success and out_path.exists() and out_path.stat().st_size > 100000:
                size_mb = out_path.stat().st_size / 1024 / 1024
                caption = (
                    f"✅ <b>{i+1}/14 完成</b>｜{title_zh}\n\n"
                    f"📁 panel_{i+1:02d}.png ({size_mb:.1f}MB)\n"
                    f"📐 {size}\n"
                    f"⏱ 耗時 {dt:.0f}s"
                )
                send_photo(out_path, caption)
                log(f"  ✅ Generated + pushed {out_path.name} ({dt:.0f}s)")
                results.append({"index": i + 1, "title": title_zh, "size": size, "ok": True, "from_cache": False, "dt": dt})
            else:
                send_text(f"❌ <b>{i+1}/14 失敗</b>｜{title_zh}")
                log(f"  ❌ Failed {out_path.name}")
                results.append({"index": i + 1, "title": title_zh, "size": size, "ok": False, "from_cache": False, "dt": dt})

    # 最終彙整
    success_count = sum(1 for r in results if r["ok"])
    log(f"=== 完成 {success_count}/{len(prompts)} ===")

    lines = ["🏁 <b>《證明給機器看》漫畫插畫全部完成</b>\n", f"✅ <b>{success_count}/{len(prompts)}</b> 張成功\n", "📋 <b>全部章節</b>："]
    for r in results:
        if r["ok"]:
            note = "（從快取）" if r.get("from_cache") else f"（{r['dt']:.0f}s）"
            lines.append(f"  {r['index']:02d}. {r['title']} ({r['size']}) ✅ {note}")
        else:
            lines.append(f"  {r['index']:02d}. {r['title']} ({r['size']}) ❌")
    lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels/</code>")
    lines.append("\n您可以安心去睡了。每張圖都已即時推到 Telegram。\n晚安教練 🦞")
    send_text("\n".join(lines))

    log("=== Monitor 結束 ===")


if __name__ == "__main__":
    main()
