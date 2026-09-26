#!/usr/bin/env python3
"""
漫畫版 v2 — 人物更成熟 + 角色更多元 + 鎖臉
教練 2026-09-26 08:25 親定改動：
  1. 人物再成熟一點（教練 late 40s~mid-50s、成熟權威、配角加歲月痕跡）
  2. 角色再多樣（多世代/多職業/多性別/多族群）
  3. 風格 OK 才跑剩 27 張
"""
import argparse
import base64
import json
import re
import sys
import time
import urllib.request
import lk888_guard
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DATA_DIR = WORKSPACE / "claude-brain" / "data" / "comic_source_20260926_teamwork_manga"
PROMPTS_JSON = DATA_DIR / "prompts.json"
REFERENCE = WORKSPACE / "claude-brain" / "data" / "comic_reference" / "coach_face_reference.jpg"
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
LK888_API_URL = "https://api.lk888.ai/v1/images/edits"
SIZE = "1536x1024"


def get_api_key():
    text = CRED_FILE.read_text(encoding="utf-8")
    m = re.search(r"^API Key：(sk-\S+)", text, re.MULTILINE)
    if not m:
        raise RuntimeError("路徑大全_憑證層.md 裡找不到 lk888 API Key")
    return m.group(1)


def get_telegram_bot_token():
    cfg = json.loads((Path.home() / ".openclaw" / "openclaw.json").read_text())
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


# ==================== 成熟導向 IDENTITY BIBLE ====================
IDENTITY_BIBLE = """IDENTITY LOCK - NON-NEGOTIABLE:

[Coach - Mature Protagonist]
- East Asian Taiwanese male, late forties to mid-fifties
- Mature authoritative presence, dignified executive gravitas
- Subtle age lines around eyes and forehead showing decades of wisdom
- Short neat black hair with natural salt-and-pepper graying at temples
- Strong defined jawline with slight weathering from years of leadership
- Calm commanding eyes radiating experience and steady confidence
- Slight knowing smile that conveys patience earned through decades
- Well-tailored navy-blue two-piece suit (NO vest), crisp white shirt, blue striped tie
- NO glasses, NO facial hair, NO beard, NO mustache, NO stubble
- NO lapel pin, NO name badge, NO pocket square, NO accessories

[Maturity Directive - All Characters]
- Characters should look mid-career to mature (late 20s through 60s), NOT fresh graduates
- Older mentors (60s): distinguished silver hair, reading glasses, dignified bearing
- Senior professionals (40s-50s): subtle graying, reading glasses, executive presence
- Mid-career professionals (30s-40s): confident, settled, mature energy
- Younger professionals (late 20s-early 30s): ambition and energy, but NOT teenagery
- Every character should look like a real professional with years of experience

[Style Anchor]
- Clean modern Japanese anime key-visual illustration (no photo, no watercolor, no western cartoon)
- Crisp confident line art, flat vibrant cel shading, soft cinematic lighting
- Warm golden highlights + deep navy blue palette
- Contemporary Taiwan setting
- Richly detailed background with cultural specificity

[Safety Rail]
- Absolutely NO text, letters, numbers, logos, watermarks, subtitles anywhere
- NO extra fingers, NO distorted hands
- NO Western/Caucasian faces as main characters
- Recurring protagonist 'the Coach' must keep identical face and suit in every panel
"""


def build_p01_v2_prompt():
    """p01 v2: 8人多元成熟團隊封面"""
    return (
        "A rooftop terrace at dawn overlooking a Taipei cityscape with Taipei 101 in the distance and mountains behind. "
        "In the foreground, a DIVERSE MULTI-GENERATIONAL team of EIGHT Taiwanese professionals stand shoulder to shoulder facing the sunrise, seen from a low heroic angle. "
        "From left to right: "
        "(1) A distinguished silver-haired female tech pioneer in her early 60s, elegant gray blazer over black turtleneck, kind grandmother eyes behind designer glasses, confident warm presence. "
        "(2) A lean older male craftsman in his late 50s, denim work apron over white shirt with rolled sleeves, calloused hands, distinguished silver-gray beard, master artisan look with calm dignity. "
        "(3) A mature female executive in her early 50s, charcoal power suit with silver-streaked bob haircut, veteran boardroom commander, subtle pearl earrings, refined strength. "
        "(4) THE COACH at center - late forties to mid-fifties Taiwanese businessman, short neat black hair with subtle natural graying at temples, well-tailored navy-blue suit with white shirt and blue striped tie, mature authoritative presence with slight knowing smile, calm commanding eyes radiating decades of leadership wisdom (see IDENTITY LOCK below). "
        "(5) A confident female designer in her late 30s, sleek modern blazer over silk blouse, holding a tablet, creative professional energy but with settled career confidence. "
        "(6) A mixed-heritage male strategist in his late 30s, sharp tailored suit, half-Taiwanese half-Western features, modern rectangular glasses, analytical expression. "
        "(7) A warm female mentor in her early 50s, soft cardigan over blouse, kindergarten/education background, motherly warmth and approachable wisdom. "
        "(8) A young male engineer in his late 20s, smart casual shirt with rolled sleeves, holding laptop, fresh tech talent energy but with a focused mature-for-his-age look. "
        "All eight look toward the sunrise together, a powerful visual metaphor for Taiwan's multi-generational, multi-professional, multi-gender collaborative future. "
        "Above and behind them a faint glowing constellation network of light lines and nodes spreads across the sky like a global web, connecting them. "
        "A large leafy tree frames the left edge with sunlight filtering through the leaves. "
        f"\n\n{IDENTITY_BIBLE}\n\n"
        "Style: clean modern Japanese anime key-visual illustration, crisp confident line art, flat vibrant cel shading, soft cinematic lighting with warm golden highlights, richly detailed background, contemporary Taiwan setting, warm gold and deep navy blue palette, hopeful cinematic mood, 3:2 landscape aspect ratio (1536x1024), high detail. Absolutely no text, no letters, no numbers, no logos, no watermark, no subtitles."
    )


def call_lk88_edit(prompt: str, reference_path: Path, size: str = SIZE, quality: str = "auto") -> bytes:
    api_key = get_api_key()
    boundary = "----MangaBoundary" + datetime.now().strftime("%H%M%S%f")
    body = []
    # image field
    body.append(f"--{boundary}\r\n".encode())
    body.append(
        f'Content-Disposition: form-data; name="image"; filename="{reference_path.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
    )
    body.append(reference_path.read_bytes())
    body.append(b"\r\n")
    # prompt
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
    body.append(prompt.encode("utf-8"))
    body.append(b"\r\n")
    # model
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="model"\r\n\r\n')
    body.append(b"gpt-image-2")
    body.append(b"\r\n")
    # size
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="size"\r\n\r\n')
    body.append(size.encode("utf-8"))
    body.append(b"\r\n")
    # quality
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="quality"\r\n\r\n')
    body.append(quality.encode("utf-8"))
    body.append(b"\r\n")
    # n
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="n"\r\n\r\n')
    body.append(b"1")
    body.append(b"\r\n")
    body.append(f"--{boundary}--\r\n".encode())
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
    with lk888_guard.urlopen(req, timeout=300) as resp:
        result = json.loads(resp.read())
    if "data" in result and result["data"]:
        item = result["data"][0]
        if "b64_json" in item:
            return base64.b64decode(item["b64_json"])
        elif "url" in item:
            with urllib.request.urlopen(item["url"], timeout=120) as img_resp:
                return img_resp.read()
    raise ValueError(f"Unexpected response: {result}")


def png_to_jpeg(png_bytes: bytes, out_path: Path, quality: int = 85) -> int:
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    img.save(out_path, "JPEG", quality=quality, optimize=True)
    return out_path.stat().st_size


def push_telegram(image_path: Path, caption: str) -> bool:
    try:
        bot_token = get_telegram_bot_token()
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        boundary = "----TgBoundary" + datetime.now().strftime("%H%M%S%f")
        body = []
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n6124913915\r\n".encode())
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode())
        body.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{image_path.name}\"\r\nContent-Type: image/jpeg\r\n\r\n".encode()
        )
        body.append(image_path.read_bytes())
        body.append(f"\r\n--{boundary}--\r\n".encode())
        data = b"".join(body)
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        print(f"⚠️ Telegram push failed: {e}", flush=True)
        return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--p01-only", action="store_true", help="only generate p01 v2 test")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=28)
    args = p.parse_args()

    if args.p01_only:
        out_jpg = DATA_DIR / "p01_v2_test.jpg"
        print(f"=== 漫畫版 v2 — p01 測試版（8 人多元成熟團隊）===", flush=True)
        print(f"=== Reference：{REFERENCE.name}（{REFERENCE.stat().st_size} bytes）===", flush=True)
        print(f"=== Size：{SIZE} | Model：gpt-image-2 ===\n", flush=True)

        prompt = build_p01_v2_prompt()
        print(f"=== Prompt 長度：{len(prompt)} chars ===", flush=True)
        t0 = time.time()
        try:
            png_bytes = call_lk88_edit(prompt, REFERENCE, SIZE, "auto")
            elapsed = time.time() - t0
            size = png_to_jpeg(png_bytes, out_jpg, 85)
            print(f"   ✅ 存 {out_jpg.name} ({size} bytes, 生成 {elapsed:.1f}s)", flush=True)
            caption = f"🔒 漫畫版 v2 測試｜8 人多元成熟團隊封面｜{elapsed:.1f}s"
            push_telegram(out_jpg, caption)
            print(f"   📲 已 push Telegram", flush=True)
        except Exception as e:
            print(f"   ❌ 失敗: {e}", flush=True)
        return


if __name__ == "__main__":
    main()
