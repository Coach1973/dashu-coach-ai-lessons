#!/usr/bin/env python3
"""
漫畫插畫批次生成器：
1. 解析 HTML 抓出 14 個 prompt（含封面）
2. 逐一呼叫 lk888 生成（無 Telegram 推送，避免狂炸通知）
3. 全部完成後用 Telegram sendMediaGroup 批次推送 + 彙整回報

用法：python3 batch_comic_run.py
"""
import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
HTML = WORKSPACE / "claude-brain/data/comic_source_20260923/證明給機器看_章回漫畫小說.html"
REFERENCE = WORKSPACE / "claude-brain/data/comic_reference/coach_face_reference.jpg"
SCRIPT = WORKSPACE / "scripts/generate_comic_panel.py"
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels"
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/batch_progress.log"
CHAT_ID = "6124913915"
CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"

ANCHOR = (
    "Consistent character design across all panels: a distinguished Taiwanese middle-aged male coach "
    "in his late 40s with neatly groomed short dark hair fully dark no gray, no glasses no facial hair, "
    "wearing a tailored gray plaid three-piece suit with white dress shirt and a blue tie with subtle "
    "dot pattern; same face shape, same jawline, same nose, same eye spacing in every panel; "
    "no lapel pin, no name badge, no extra accessories, no extra people; "
    "refined, dignified, contemplative expression when alone; slightly warm mature expression in close-ups."
)

GUARD = "no readable text, no Chinese text, no English text, no watermarks, no lapel pin, no name badge"


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def parse_prompts():
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
        # 決定解析度（注意：用 word boundary 避免 "2:30" 誤判成 "2:3"）
        sl = raw.lower()
        if "double-page" in sl or re.search(r"\b21:9\b", sl):
            size = "1792x1024"  # 雙頁跨頁 21:9
        elif re.search(r"\b16:9\b", sl) or "widescreen" in sl:
            size = "1536x1024"  # 16:9 橫幅
        elif re.search(r"\b2:3\b", sl) or "portrait" in sl:
            size = "1024x1536"  # 直幅
        else:
            size = "1536x1024"  # 預設橫幅
        # 補強 no text 護欄（重要：很多 prompt 漏寫）
        if "no text" not in raw.lower() and "no readable" not in raw.lower():
            raw = raw.rstrip(" .") + ", " + GUARD
        else:
            raw = raw.rstrip(" .") + ", " + GUARD
        prompts.append({"title": title, "prompt": raw, "size": size})
    return prompts


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
                log(f"  stderr: {result.stderr.strip()[:300]}")
            return False
        return output_path.exists()
    except subprocess.TimeoutExpired:
        log("  TIMEOUT 200s")
        return False
    except Exception as e:
        log(f"  ERROR: {e}")
        return False


def get_bot_token(account: str = "bot_main") -> str:
    cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"][account]["botToken"]


def send_telegram_text(text: str, chat_id: str = CHAT_ID, account: str = "bot_main") -> dict:
    bot_token = get_bot_token(account)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_media_group(image_paths, chat_id: str = CHAT_ID, account: str = "bot_main"):
    bot_token = get_bot_token(account)
    url = f"https://api.telegram.org/bot{bot_token}/sendMediaGroup"
    boundary = "----MediaGroup" + datetime.now().strftime("%H%M%S%f")
    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode("utf-8"))
    # media 欄位（JSON 陣列）
    media_items = []
    for i, _ in enumerate(image_paths):
        media_items.append({"type": "photo", "media": f"attach://photo_{i}"})
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"media\"\r\n\r\n{json.dumps(media_items)}\r\n".encode("utf-8"))
    for i, p in enumerate(image_paths):
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo_{i}\"; filename=\"{p.name}\"\r\nContent-Type: image/png\r\n\r\n".encode("utf-8"))
        body.append(p.read_bytes())
        body.append(b"\r\n")
    body.append(f"--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(body)
    req = urllib.request.Request(url, data=data, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prompts = parse_prompts()
    log(f"=== 批次開始：{len(prompts)} 個 prompts ===")

    send_telegram_text(
        f"🦞 <b>《證明給機器看》漫畫插畫批次開工</b>\n\n"
        f"📊 共 <b>{len(prompts)}</b> 張（13 章主插圖 + 1 封面）\n"
        f"🎨 角色參考：教練專業形象照（去背版）\n"
        f"⏱ 預計 14-28 分鐘\n"
        f"📁 全部跑完會彙整成 2 個 media group + 1 則彙整回報"
    )

    results = []
    for i, p in enumerate(prompts):
        out_path = OUTPUT_DIR / f"panel_{i+1:02d}.png"
        log(f"=== {i+1}/{len(prompts)}: {p['title']} [{p['size']}] ===")
        full_prompt = f"{ANCHOR} {p['prompt']}"
        t0 = datetime.now()
        success = generate_one(full_prompt, p["size"], out_path)
        dt = (datetime.now() - t0).total_seconds()
        if success:
            log(f"  ✅ {out_path}  ({dt:.1f}s)")
        else:
            log(f"  ❌ FAILED ({dt:.1f}s)")
        results.append({"index": i + 1, "title": p["title"], "path": str(out_path) if success else None, "size": p["size"], "ok": success, "dt": dt})

    # Save results JSON
    (OUTPUT_DIR.parent / "batch_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    success_count = sum(1 for r in results if r["ok"])
    log(f"=== 生成完成：{success_count}/{len(prompts)} 成功 ===")

    successful = [r for r in results if r["ok"]]

    if not successful:
        send_telegram_text("❌ 全部失敗，請查 log。")
        return

    # Send 2 media groups (10 + remaining)
    send_telegram_text(f"🦞 <b>生成完成：{success_count}/{len(prompts)} 成功</b>\n\n正在彙整圖片群組訊息...")

    if len(successful) >= 10:
        g1 = [Path(r["path"]) for r in successful[:10]]
        try:
            send_media_group(g1, CHAT_ID)
            log(f"✅ Group 1 sent ({len(g1)} images)")
        except Exception as e:
            log(f"❌ Group 1 failed: {e}")

    if len(successful) > 10:
        g2 = [Path(r["path"]) for r in successful[10:]]
        try:
            send_media_group(g2, CHAT_ID)
            log(f"✅ Group 2 sent ({len(g2)} images)")
        except Exception as e:
            log(f"❌ Group 2 failed: {e}")
    elif 0 < len(successful) < 10:
        # 全部一次送
        g = [Path(r["path"]) for r in successful]
        try:
            send_media_group(g, CHAT_ID)
            log(f"✅ Single group sent ({len(g)} images)")
        except Exception as e:
            log(f"❌ Single group failed: {e}")

    # Final summary
    lines = [f"🦞 <b>《證明給機器看》漫畫插畫完成報告</b>\n", f"✅ <b>{success_count}/{len(prompts)}</b> 張成功\n", "📋 <b>對應章節</b>："]
    for r in results:
        if r["ok"]:
            lines.append(f"  {r['index']:02d}. {r['title']} ({r['size']}) — <b>{r['dt']:.1f}s</b> ✅")
        else:
            lines.append(f"  {r['index']:02d}. {r['title']} ({r['size']}) — ❌")
    lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels/</code>")
    failed = len(prompts) - success_count
    if failed > 0:
        lines.append(f"\n⚠️ {failed} 張失敗，請查 <code>batch_progress.log</code>")
    send_telegram_text("\n".join(lines))

    log("=== 全部完成，彙整送出 ===")


if __name__ == "__main__":
    main()
