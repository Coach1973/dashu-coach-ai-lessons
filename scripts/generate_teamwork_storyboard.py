#!/usr/bin/env python3
"""
全世界最優秀的團隊計畫｜20 張分鏡批次生成 + Telegram 推送
教練 2026-09-25 21:00 下單：
- 跳過 #17（教練說已有）
- 預設 A：每張生完立刻 push Telegram
"""
import json
import re
import sys
import time
import base64
import urllib.request
import lk888_guard
import urllib.error
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DATA_DIR = WORKSPACE / "claude-brain/data/comic_source_20260925_teamwork"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DATA_DIR / "generation.log"

API_URL = "https://api.lk888.ai/v1/images/generations"
LK888_SIZE = "1536x1024"  # 16:9 widescreen
COACH_CHAT_ID = "6124913915"
SKIP_IDX = {17}


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_api_key():
    cred = (WORKSPACE / "路徑大全_憑證層.md").read_text(encoding="utf-8")
    m = re.search(r"API Key：(sk-\S+)", cred)
    if not m:
        raise RuntimeError("找不到 LK888 API Key")
    return m.group(1)


def get_telegram_config():
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


def generate_image(prompt: str, api_key: str) -> bytes:
    payload = json.dumps({
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": LK888_SIZE,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with lk888_guard.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    b64 = data["data"][0]["b64_json"]
    return base64.b64decode(b64)


def send_telegram_photo(photo_path: Path, caption: str, bot_token: str):
    boundary = "----TeamworkFormBoundary9f8e7d6c"
    photo_bytes = photo_path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"chat_id\"\r\n\r\n{COACH_CHAT_ID}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n"
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"photo\"; filename=\"{photo_path.name}\"\r\n"
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + photo_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{bot_token}/sendPhoto",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    start_time = time.time()
    api_key = get_api_key()
    bot_token = get_telegram_config()

    prompts_path = DATA_DIR / "prompts.json"
    if not prompts_path.exists():
        log(f"❌ 找不到 {prompts_path}")
        sys.exit(1)
    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
    prompts.sort(key=lambda p: p["idx"])

    todo = [p for p in prompts if p["idx"] not in SKIP_IDX]
    total = len(todo)
    log(f"=== 開始批次生成：{total} 張（跳過 #17）===")

    done_count = 0
    for p in prompts:
        idx = p["idx"]
        scene_zh = p["scene_zh"]
        if idx in SKIP_IDX:
            log(f"[{idx:02d}/20] ⏭️  跳過 {scene_zh}（教練說已有）")
            continue
        done_count += 1
        log(f"[{idx:02d}/20] ({done_count}/{total}) 🎨 {scene_zh} 生圖中...")
        t0 = time.time()
        try:
            img_bytes = generate_image(p["prompt"], api_key)
            elapsed = time.time() - t0
            out_path = DATA_DIR / f"teamwork_{idx:02d}.png"
            out_path.write_bytes(img_bytes)
            log(f"  ✅ 存 {out_path.name} ({len(img_bytes)} bytes, {elapsed:.1f}s)")

            caption = (
                f"📖 [{idx}/20] {scene_zh}\n"
                f"全世界最優秀的團隊計畫｜第 {done_count}/{total} 張\n"
                f"⏱ {elapsed:.0f} 秒｜{LK888_SIZE}"
            )
            send_telegram_photo(out_path, caption, bot_token)
            log(f"  📲 已 push Telegram")
        except urllib.error.HTTPError as e:
            log(f"  ❌ HTTPError {e.code}: {e.read().decode('utf-8', errors='ignore')[:200]}")
        except Exception as e:
            log(f"  ❌ Error: {e}")
        time.sleep(2)

    total_elapsed = time.time() - start_time
    log(f"=== 完成 {total} 張，總耗 {total_elapsed:.0f} 秒 ===")


if __name__ == "__main__":
    main()
