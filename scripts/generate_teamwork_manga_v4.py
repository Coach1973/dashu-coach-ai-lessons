#!/usr/bin/env python3
"""
漫畫版 v4 — 加強鎖臉（多張 reference + 具體臉部錨點 + 構圖凸顯教練）
教練 2026-09-26 08:36 親定：
  「其他人都對了，就是教練的不對味，你沒有鎖臉，不像我，再試一張」
"""
import argparse
import base64
import json
import re
import time
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DATA_DIR = WORKSPACE / "claude-brain" / "data" / "comic_source_20260926_teamwork_manga"
PROMPTS_JSON = DATA_DIR / "prompts.json"
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
LK888_API_URL = "https://api.lk888.ai/v1/images/edits"
SIZE = "1536x1024"

# 4 張教練照片（多張 reference 加強鎖臉）
REFS = [
    WORKSPACE / "claude-brain" / "data" / "comic_reference" / "coach_seated_three_quarter_window.jpg",       # _7 主參考 900KB
    WORKSPACE / "claude-brain" / "data" / "comic_reference" / "coach_face_front_three_quarter.jpg",           # _5 三分之二 541KB
    WORKSPACE / "claude-brain" / "data" / "comic_reference" / "coach_face_anchor_debacked.jpg",              # _9 去背 254KB
    WORKSPACE / "claude-brain" / "data" / "comic_reference" / "coach_standing_full_low_angle.jpg",           # _13 立姿 502KB
]


def get_api_key():
    text = CRED_FILE.read_text(encoding="utf-8")
    m = re.search(r"^API Key：(sk-\S+)", text, re.MULTILINE)
    if not m:
        raise RuntimeError("路徑大全_憑證層.md 裡找不到 lk888 API Key")
    return m.group(1)


def get_telegram_bot_token():
    cfg = json.loads((Path.home() / ".openclaw" / "openclaw.json").read_text())
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


# ==================== v4 IDENTITY BIBLE：具體臉部錨點（從 4 張照片實際觀察）====================
IDENTITY_BIBLE_V4 = """IDENTITY LOCK - NON-NEGOTIABLE (v4: SPECIFIC FACE ANCHOR FROM 4 REFERENCE PHOTOS):

[Coach - FACE LOCK - CRITICAL - MUST MATCH REFERENCE PHOTOS EXACTLY]
- East Asian Taiwanese male, late thirties to mid-forties (mature but well-preserved)
- Face shape: oval-square (橢圓偏方), clean defined jawline but not too sharp, slightly rounded chin
- Skin: warm yellow Asian tone, smooth clear complexion, NO wrinkles anywhere (no crow's feet, no forehead lines, no nasolabial folds, no laugh lines)
- Forehead: medium-wide, smooth and full, no wrinkles, natural rounded hairline
- Eyebrows: straight with subtle natural arch (劍眉), medium-thick density, PURE BLACK, neat groomed, slightly tapered at ends, dignified masculine
- Eyes: SINGLE EYELID (單眼皮) or very subtle inner-fold, SHARP ALMOND-SHAPE, slightly upward corners at outer edge, MEDIUM SIZE, deep focused calm confident gaze with quiet inner strength, clear bright whites with dark brown irises
- Nose: HIGH STRAIGHT nose bridge with medium height, smooth straight profile, ROUNDED FULL nose tip, MEDIUM nose wings (not narrow, not wide), the most prominent feature on the face
- Lips: MEDIUM thickness, upper slightly thinner than lower, well-defined lip line, corners naturally SLIGHTLY UPWARD conveying confidence and patience
- Expression: gentle composed smile (不露齒 or very subtle teeth show), calm commanding gaze that conveys quiet authority and life experience WITHOUT age marks
- Facial hair: CLEAN-SHAVEN with extremely subtle light stubble shadow on chin area (NOT visible beard, just very faint shadow texture)

[Hair - SPECIFIC LOCK]
- SHORT hair, 2-3cm length
- STYLE: classic SIDE-PARTED with volume on top, sides trimmed short, top combed to the side, neat and polished
- COLOR: PURE BLACK (烏黑亮麗), NO gray, NO silver, NO salt-and-pepper, NO white strands
- TEXTURE: soft with subtle sheen, well-groomed and professional

[Body & Outfit - SPECIFIC LOCK]
- Build: slim-fit athletic, height around 172-178cm, no visible belly, well-proportioned
- NAVY-BLUE two-piece suit (深藍西裝), well-tailored modern cut, NO vest, NO waistcoat
- CRISP WHITE dress shirt
- BLUE STRIPED TIE (細條紋)
- NO glasses, NO beard, NO mustache, NO stubble, NO earrings
- NO lapel pin, NO name badge, NO pocket square, NO accessories of any kind (these were visible in reference photos but ABSOLUTELY DO NOT include them in this illustration — the manga Coach has none)

[CRITICAL ANTI-DRIFT DIRECTIVES]
- The Coach's face MUST closely resemble the person in the reference photos provided
- Preserve: oval-square face shape, single eyelid almond eyes, high straight nose with rounded tip, medium lips with slight upward corners, short side-parted pure black hair
- AVOID ANY AGE MARKS: no wrinkles, no gray hair, no weathered skin, no jowls, no sagging
- Maturity expressed through CHARISMA, GAZE, COMPOSURE, POSTURE — NOT through physical aging
- Picture a 40-year-old CEO: polished, confident, smooth skin, dark hair, but with unmistakable gravitas
- The Coach should be IMMEDIATELY RECOGNIZABLE as the person in the reference photos

[Composition Direction - HEROIC FOREGROUND]
- The Coach stands slightly FORWARD of the other seven team members (half-step ahead, foreground position)
- The Coach's face must be CLEARLY VISIBLE with sharp detail (not lost in crowd)
- Low heroic camera angle (looking up slightly) emphasizes the Coach's commanding presence
- Coach is THE PROTAGONIST — the rest of the team frames him but does not dominate him

[Other 7 Team Members - UNCHANGED FROM v3 (coach approved these as correct)]
(1) Silver-haired female tech pioneer, early 60s, gray blazer over black turtleneck, designer glasses
(2) Older male craftsman, late 50s, denim work apron over white shirt, silver beard, calloused hands
(3) Female executive, early 50s, charcoal power suit, silver-streaked bob haircut, pearl earrings
(5) Female designer, late 30s, modern blazer over silk blouse, holding tablet
(6) Mixed-heritage male strategist, late 30s, sharp tailored suit, rectangular glasses
(7) Female mentor, early 50s, cardigan over blouse, education background, motherly warmth
(8) Young male engineer, late 20s, smart casual shirt, holding laptop

[Style Anchor - UNCHANGED]
- Clean modern Japanese anime key-visual illustration
- Crisp confident line art, flat vibrant cel shading, soft cinematic lighting
- Warm golden highlights + deep navy blue palette
- Contemporary Taiwan setting

[Safety Rail - UNCHANGED]
- Absolutely NO text, letters, numbers, logos, watermarks, subtitles anywhere
- NO extra fingers, NO distorted hands
- NO Western/Caucasian faces as main characters
"""


def build_p01_v4_prompt():
    """p01 v4: 8人團隊封面（教練臉部具體錨點 + heroic foreground）"""
    return (
        "A rooftop terrace at dawn overlooking a Taipei cityscape with Taipei 101 in the distance and mountains behind. "
        "In the foreground, a DIVERSE MULTI-GENERATIONAL team of EIGHT Taiwanese professionals stand together facing the sunrise. "
        "THE COACH stands slightly FORWARD of the other seven members (half-step ahead, foreground position), seen from a low heroic angle. "
        "From left to right: "
        "(1) A distinguished silver-haired female tech pioneer in her early 60s, elegant gray blazer over black turtleneck, kind wise eyes behind designer glasses, dignified grandmother presence. "
        "(2) A lean older male craftsman in his late 50s, denim work apron over white shirt with rolled sleeves, calloused hands, neatly trimmed silver beard, master artisan look with calm dignity. "
        "(3) A confident female executive in her early 50s, charcoal power suit with stylish silver-streaked bob haircut, veteran boardroom commander, subtle pearl earrings, refined strength. "
        "(4) THE COACH - standing slightly forward in HEROIC FOREGROUND, late thirties to mid-forties Taiwanese businessman. FACE MUST MATCH REFERENCE PHOTOS EXACTLY: oval-square face shape with clean defined jawline, warm yellow skin tone with smooth clear complexion (NO wrinkles), single eyelid almond-shaped eyes with slight upward corners, deep focused calm confident gaze, high straight nose with rounded tip, medium lips with slight upward corners, short side-parted pure black hair (2-3cm length, no gray), clean-shaven with subtle light stubble shadow, mature professional charisma through posture and gaze. Well-tailored navy-blue suit with white shirt and blue striped tie. "
        "(5) A confident female designer in her late 30s, sleek modern blazer over silk blouse, holding a tablet. "
        "(6) A mixed-heritage male strategist in his late 30s, sharp tailored suit, rectangular glasses. "
        "(7) A warm female mentor in her early 50s, soft cardigan over blouse, motherly warmth. "
        "(8) A young male engineer in his late 20s, smart casual shirt with rolled sleeves, holding laptop. "
        "All eight look toward the sunrise together. Above and behind them a faint glowing constellation network of light lines and nodes spreads across the sky like a global web. "
        "A large leafy tree frames the left edge with sunlight filtering through the leaves. "
        f"\n\n{IDENTITY_BIBLE_V4}\n\n"
        "Style: clean modern Japanese anime key-visual illustration, crisp confident line art, flat vibrant cel shading, soft cinematic lighting with warm golden highlights, richly detailed background, contemporary Taiwan setting, warm gold and deep navy blue palette, hopeful cinematic mood, 3:2 landscape aspect ratio (1536x1024), high detail. Absolutely no text, no letters, no numbers, no logos, no watermark, no subtitles."
    )


def call_lk88_edit_multi(prompt: str, reference_paths: list, size: str = SIZE, quality: str = "auto") -> bytes:
    """多張 reference 鎖臉"""
    api_key = get_api_key()
    boundary = "----MangaV4Boundary" + datetime.now().strftime("%H%M%S%f")
    body = []
    # 多張 image[] reference（LK888 /v1/images/edits 支援 image[]）
    for i, ref_path in enumerate(reference_paths):
        body.append(f"--{boundary}\r\n".encode())
        body.append(
            f'Content-Disposition: form-data; name="image[]"; filename="ref{i}_{ref_path.name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
        )
        body.append(ref_path.read_bytes())
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
    with urllib.request.urlopen(req, timeout=300) as resp:
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
        boundary = "----TgV4Boundary" + datetime.now().strftime("%H%M%S%f")
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
        out_jpg = DATA_DIR / "p01_v4_test.jpg"
        print(f"=== 漫畫版 v4 — p01 測試版（多張 reference + 具體臉部錨點）===", flush=True)
        print(f"=== References（4 張同時帶）===", flush=True)
        for i, r in enumerate(REFS):
            print(f"   {i+1}. {r.name} ({r.stat().st_size} bytes)", flush=True)
        print(f"=== Size：{SIZE} | Model：gpt-image-2 ===\n", flush=True)

        prompt = build_p01_v4_prompt()
        print(f"=== Prompt 長度：{len(prompt)} chars ===", flush=True)
        t0 = time.time()
        try:
            png_bytes = call_lk88_edit_multi(prompt, REFS, SIZE, "auto")
            elapsed = time.time() - t0
            size = png_to_jpeg(png_bytes, out_jpg, 85)
            print(f"   ✅ 存 {out_jpg.name} ({size} bytes, 生成 {elapsed:.1f}s)", flush=True)
            caption = f"🔒 漫畫版 v4 測試｜4 張 reference 鎖臉 + 具體臉部錨點｜{elapsed:.1f}s"
            push_telegram(out_jpg, caption)
            print(f"   📲 已 push Telegram", flush=True)
        except Exception as e:
            print(f"   ❌ 失敗: {e}", flush=True)
        return


if __name__ == "__main__":
    main()
