#!/usr/bin/env python3
"""
漫畫版 v3 — 去掉歲月感、保留成熟權威（教練 2026-09-26 08:32 親定）
教練原話：「歲月感太重，我要成熟，但不是年紀大」
  → 不用皺紋/灰髮/法令紋等時間痕跡
  → 用沉穩眼神、從容微笑、挺拔姿態、領袖魅力表達「成熟」
"""
import argparse
import base64
import json
import re
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


# ==================== v3 IDENTITY BIBLE：成熟感靠氣質，不是靠歲月痕跡 ====================
IDENTITY_BIBLE_V3 = """IDENTITY LOCK - NON-NEGOTIABLE (v3: maturity through charisma, NOT age marks):

[Coach - Mature Protagonist WITHOUT age marks]
- East Asian Taiwanese male, late thirties to mid-forties
- Mature authoritative presence expressed through CONFIDENT CHARISMA, not through age marks
- Clean smooth complexion — NO wrinkles, NO crow's feet, NO laugh lines, NO forehead lines, NO nasolabial folds
- Short neat FULL BLACK hair, neatly groomed, NO gray, NO silver, NO salt-and-pepper, NO graying at temples
- Strong defined jawline, smooth clear skin
- Calm commanding eyes radiating inner confidence and quiet authority
- Gentle composed smile that conveys patience and capability (NOT the smile of someone who has 'seen it all')
- Well-tailored navy-blue two-piece suit (NO vest), crisp white shirt, blue striped tie
- NO glasses, NO facial hair, NO beard, NO mustache, NO stubble
- NO lapel pin, NO name badge, NO pocket square, NO accessories

[CRITICAL ANTI-AGING DIRECTIVE]
- The Coach should look like a successful professional at peak career maturity
- Maturity shown through POSTURE, GAZE, COMPOSURE, CHARISMA — NOT through aging skin, gray hair, or wrinkles
- He looks like someone who has always taken care of himself, like a present-day mature executive
- Picture a 40-something CEO in a Fortune 500 photo shoot — polished, confident, smooth skin, dark hair, but with unmistakable gravitas
- AVOID: weathered face, crow's feet, forehead furrows, gray temples, silver streaks, jowls, sagging skin, tired eyes, any signs of physical aging

[Maturity Directive - All Characters - SAME PRINCIPLE]
- ALL characters should look mature and professional, but POLISHED and PRESENT
- Older mentors (60s): silver hair IS appropriate here (it's their defining feature), but smooth skin, dignified bearing
- Senior professionals (40s-50s): NO gray, NO wrinkles — just confident posture and executive presence
- Mid-career (30s-40s): smooth skin, ambitious but settled energy
- Younger (late 20s): fresh energy, smooth skin, no age marks
- Maturity = posture + gaze + composure + professional polish, NOT age marks

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


def build_p01_v3_prompt():
    """p01 v3: 8人多元成熟團隊封面（主角去掉歲月感）"""
    return (
        "A rooftop terrace at dawn overlooking a Taipei cityscape with Taipei 101 in the distance and mountains behind. "
        "In the foreground, a DIVERSE MULTI-GENERATIONAL team of EIGHT Taiwanese professionals stand shoulder to shoulder facing the sunrise, seen from a low heroic angle. "
        "From left to right: "
        "(1) A distinguished silver-haired female tech pioneer in her early 60s, elegant gray blazer over black turtleneck, kind wise eyes behind designer glasses, dignified grandmother presence. "
        "(2) A lean older male craftsman in his late 50s, denim work apron over white shirt with rolled sleeves, calloused hands, neatly trimmed silver beard (NOT gray hair on head — solid color), master artisan look with calm dignity. "
        "(3) A confident female executive in her early 50s, charcoal power suit with stylish silver-streaked bob haircut, veteran boardroom commander, subtle pearl earrings, refined strength — smooth skin, no wrinkles. "
        "(4) THE COACH at center - late thirties to mid-forties Taiwanese businessman, SHORT NEAT FULL BLACK HAIR (NO gray, NO silver), clean smooth complexion (NO wrinkles, NO crow's feet, NO forehead lines, NO nasolabial folds), well-tailored navy-blue suit with white shirt and blue striped tie, mature authoritative presence expressed through CHARISMA not age marks — calm commanding eyes radiating inner confidence, gentle composed smile conveying patience and capability, strong defined jawline with smooth clear skin. Picture a Fortune 500 CEO at peak career maturity: polished, confident, smooth skin, dark hair, but with unmistakable gravitas. (see IDENTITY LOCK v3 below). "
        "(5) A confident female designer in her late 30s, sleek modern blazer over silk blouse, holding a tablet, creative professional energy with settled career confidence — smooth skin, no wrinkles. "
        "(6) A mixed-heritage male strategist in his late 30s, sharp tailored suit, half-Taiwanese half-Western features, modern rectangular glasses, analytical expression — smooth skin. "
        "(7) A warm female mentor in her early 50s, soft cardigan over blouse, kindergarten/education background, motherly warmth and approachable wisdom — smooth skin, gentle kind eyes, no wrinkles. "
        "(8) A young male engineer in his late 20s, smart casual shirt with rolled sleeves, holding laptop, fresh tech talent energy, smooth skin. "
        "All eight look toward the sunrise together, a powerful visual metaphor for Taiwan's multi-generational, multi-professional, multi-gender collaborative future. "
        "Above and behind them a faint glowing constellation network of light lines and nodes spreads across the sky like a global web, connecting them. "
        "A large leafy tree frames the left edge with sunlight filtering through the leaves. "
        f"\n\n{IDENTITY_BIBLE_V3}\n\n"
        "Style: clean modern Japanese anime key-visual illustration, crisp confident line art, flat vibrant cel shading, soft cinematic lighting with warm golden highlights, richly detailed background, contemporary Taiwan setting, warm gold and deep navy blue palette, hopeful cinematic mood, 3:2 landscape aspect ratio (1536x1024), high detail. Absolutely no text, no letters, no numbers, no logos, no watermark, no subtitles."
    )


def call_lk88_edit(prompt: str, reference_path: Path, size: str = SIZE, quality: str = "auto") -> bytes:
    api_key = get_api_key()
    boundary = "----MangaBoundary" + datetime.now().strftime("%H%M%S%f")
    body = []
    body.append(f"--{boundary}\r\n".encode())
    body.append(
        f'Content-Disposition: form-data; name="image"; filename="{reference_path.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
    )
    body.append(reference_path.read_bytes())
    body.append(b"\r\n")
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
    body.append(prompt.encode("utf-8"))
    body.append(b"\r\n")
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="model"\r\n\r\n')
    body.append(b"gpt-image-2")
    body.append(b"\r\n")
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="size"\r\n\r\n')
    body.append(size.encode("utf-8"))
    body.append(b"\r\n")
    body.append(f"--{boundary}\r\n".encode())
    body.append(b'Content-Disposition: form-data; name="quality"\r\n\r\n')
    body.append(quality.encode("utf-8"))
    body.append(b"\r\n")
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
    p.add_argument("--p01-only", action="store_true")
    args = p.parse_args()

    if args.p01_only:
        out_jpg = DATA_DIR / "p01_v3_test.jpg"
        print(f"=== 漫畫版 v3 — p01 測試版（去掉歲月感、保留成熟權威）===", flush=True)
        print(f"=== Reference：{REFERENCE.name}（{REFERENCE.stat().st_size} bytes）===", flush=True)
        print(f"=== Size：{SIZE} | Model：gpt-image-2 ===\n", flush=True)

        prompt = build_p01_v3_prompt()
        print(f"=== Prompt 長度：{len(prompt)} chars ===", flush=True)
        t0 = time.time()
        try:
            png_bytes = call_lk88_edit(prompt, REFERENCE, SIZE, "auto")
            elapsed = time.time() - t0
            size = png_to_jpeg(png_bytes, out_jpg, 85)
            print(f"   ✅ 存 {out_jpg.name} ({size} bytes, 生成 {elapsed:.1f}s)", flush=True)
            caption = f"🔒 漫畫版 v3 測試｜去掉歲月感、保留成熟權威｜{elapsed:.1f}s"
            push_telegram(out_jpg, caption)
            print(f"   📲 已 push Telegram", flush=True)
        except Exception as e:
            print(f"   ❌ 失敗: {e}", flush=True)
        return


if __name__ == "__main__":
    main()
