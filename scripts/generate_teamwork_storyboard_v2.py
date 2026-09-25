#!/usr/bin/env python3
"""
全世界最優秀的團隊計畫｜20 張分鏡批次生成 v2（鎖臉版 + JPEG 存檔）
教練 2026-09-25 22:00 下單：
- 全部 20 張都用鎖臉（含 #17 重跑，當時沒鎖臉政策）
- 改存 JPEG q=85（節省儲存 + 傳輸時間）
- A 節奏：每張完成立即 push Telegram
"""
import argparse
import base64
import io
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("錯誤：找不到 PIL（Pillow）。請先 pip3 install Pillow", file=sys.stderr)
    sys.exit(1)

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DATA_DIR = WORKSPACE / "claude-brain/data/comic_source_20260925_teamwork"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = DATA_DIR / "generation.log"

LK888_API_URL = "https://api.lk888.ai/v1/images/edits"
LK888_SIZE = "1536x1024"
REFERENCE_PATH = WORKSPACE / "claude-brain/data/comic_reference/coach_face_reference.jpg"
COACH_CHAT_ID = "6124913915"
JPEG_QUALITY = 85
JPEG_MIN_SIZE = 50_000  # catch-up threshold
MODEL = "gpt-image-2"


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


def generate_image_with_reference(prompt: str, reference_path: Path, api_key: str) -> bytes:
    """呼叫 LK888 /v1/images/edits，multipart 帶 reference 圖 + prompt"""
    boundary = "----TeamworkV2Boundary" + time.strftime("%H%M%S%f")[:18]
    body = []

    # image 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(
        f'Content-Disposition: form-data; name="image"; filename="{reference_path.name}"\r\n'
        f'Content-Type: image/jpeg\r\n\r\n'.encode("utf-8")
    )
    body.append(reference_path.read_bytes())
    body.append(b"\r\n")

    # prompt 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
    body.append(prompt.encode("utf-8"))
    body.append(b"\r\n")

    # model 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(b'Content-Disposition: form-data; name="model"\r\n\r\n')
    body.append(MODEL.encode("utf-8"))
    body.append(b"\r\n")

    # size 欄位
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(b'Content-Disposition: form-data; name="size"\r\n\r\n')
    body.append(LK888_SIZE.encode("utf-8"))
    body.append(b"\r\n")

    body.append(f"--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(body)

    req = urllib.request.Request(
        LK888_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    b64 = result["data"][0]["b64_json"]
    return base64.b64decode(b64)


def save_as_jpeg(png_bytes: bytes, out_path: Path) -> int:
    """把 PNG bytes 轉 JPEG q=85 存檔"""
    img = Image.open(io.BytesIO(png_bytes))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return out_path.stat().st_size


def send_telegram_photo(photo_path: Path, caption: str, bot_token: str):
    boundary = "----TeamworkV2TGBoundary" + time.strftime("%H%M%S%f")[:18]
    photo_bytes = photo_path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{COACH_CHAT_ID}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="photo"; filename="{photo_path.name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
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

    prompts_path = DATA_DIR / "prompts_v2.json"
    if not prompts_path.exists():
        log(f"❌ 找不到 {prompts_path}")
        sys.exit(1)
    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
    prompts.sort(key=lambda p: p["idx"])

    total = len(prompts)
    log(f"=== 開始批次生成 v2（鎖臉 + JPEG）：{total} 張 ===")
    log(f"=== Reference：{REFERENCE_PATH.name} ({REFERENCE_PATH.stat().st_size} bytes) ===")
    log(f"=== Size：{LK888_SIZE} | Model：{MODEL} | JPEG q={JPEG_QUALITY} ===")

    done_count = 0
    for p in prompts:
        idx = p["idx"]
        scene_zh = p["scene_zh"]
        out_path = DATA_DIR / f"teamwork_{idx:02d}.jpg"

        # Catch-up 邏輯：已存在 .jpg 且 > 50KB → 跳過生成，只推 Telegram
        if out_path.exists() and out_path.stat().st_size > JPEG_MIN_SIZE:
            done_count += 1
            log(f"[{idx:02d}/{total}] ✅ Catch-up（{out_path.stat().st_size} bytes, {done_count}/{total}）")
            try:
                caption = (
                    f"📖 [{idx}/{total}] {scene_zh}\n"
                    f"全世界最優秀的團隊計畫｜第 {done_count}/{total} 張（Catch-up）\n"
                    f"🔒 鎖臉版 v2｜{LK888_SIZE}｜JPEG q={JPEG_QUALITY}"
                )
                send_telegram_photo(out_path, caption, bot_token)
                log(f"  📲 已 push Telegram（Catch-up）")
            except Exception as e:
                log(f"  ⚠️ Telegram 推送失敗：{e}")
            continue

        done_count += 1
        log(f"[{idx:02d}/{total}] ({done_count}/{total}) 🎨 {scene_zh} 生圖中...")
        t0 = time.time()
        try:
            png_bytes = generate_image_with_reference(p["prompt"], REFERENCE_PATH, api_key)
            elapsed_gen = time.time() - t0

            t1 = time.time()
            jpeg_size = save_as_jpeg(png_bytes, out_path)
            elapsed_save = time.time() - t1

            log(f"  ✅ 存 {out_path.name} ({jpeg_size} bytes, 生成 {elapsed_gen:.1f}s + JPEG {elapsed_save:.1f}s)")

            caption = (
                f"📖 [{idx}/{total}] {scene_zh}\n"
                f"全世界最優秀的團隊計畫｜第 {done_count}/{total} 張\n"
                f"🔒 鎖臉版 v2｜{LK888_SIZE}｜JPEG q={JPEG_QUALITY}\n"
                f"⏱ 生成 {elapsed_gen:.0f} 秒"
            )
            send_telegram_photo(out_path, caption, bot_token)
            log(f"  📲 已 push Telegram")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")[:200]
            log(f"  ❌ HTTPError {e.code}: {err_body}")
            time.sleep(5)  # 避免連續失敗時被 API rate-limit
        except Exception as e:
            log(f"  ❌ Error: {e}")
            time.sleep(3)
        time.sleep(2)

    total_elapsed = time.time() - start_time
    log(f"=== 完成 {total} 張，總耗 {total_elapsed:.0f} 秒 ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL: {e}", file=sys.stderr)
        sys.exit(1)
