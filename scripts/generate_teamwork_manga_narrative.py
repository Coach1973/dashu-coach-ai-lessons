#!/usr/bin/env python3
"""
漫畫版 · 敘事版（narrative version）
教練 2026-09-26 09:24 親定：
  「再出一版，不要做人物限定，以劇情為主，避免視覺疲勞」
關鍵設計：
  1. 不鎖臉（純文字生圖，無 reference）
  2. 教練本人完全不出現
  3. 劇情/場景/隱喻當主角
  4. 保持風格一致（clean modern Japanese anime key-visual + warm gold + deep navy blue）
"""
import argparse
import base64
import json
import re
import sys
import time
import urllib.request
import lk888_guard
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
DATA_DIR = WORKSPACE / "claude-brain" / "data" / "comic_source_20260926_teamwork_manga"
PROMPTS_JSON = DATA_DIR / "prompts.json"
CRED_FILE = WORKSPACE / "路徑大全_憑證層.md"
LK888_API_URL = "https://api.lk888.ai/v1/images/generations"  # 純文字生圖
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


# ==================== 敘事版 PROMPT 後綴 ====================
NARRATIVE_SUFFIX = """

[NARRATIVE VERSION - NO PROTAGONIST LOCK]
- This is the NARRATIVE version — STORY/SCENE/METAPHOR is the protagonist, NOT any specific person
- DO NOT feature any specific individual as the main character
- The story, the scene, the environment, the metaphor is the protagonist
- If any people appear, they are CONTEXT (silhouettes, anonymous figures, faceless crowd, partial views like back of head, distant figures) — NOT a recurring protagonist
- Focus on the EMOTIONAL WEIGHT of the scene, the symbolism, the visual metaphor
- Vary the human presence: some images may have NO people at all (pure scenery/metaphor), some may have silhouettes/anonymous figures, some may have crowd scenes where no individual stands out

[STYLE - UNCHANGED]
- Clean modern Japanese anime key-visual illustration
- Crisp confident line art, flat vibrant cel shading, soft cinematic lighting
- Warm golden highlights + deep navy blue palette
- Contemporary Taiwan setting
- Richly detailed background with cultural specificity

[SAFETY RAIL]
- Absolutely NO text, letters, numbers, logos, watermarks, subtitles anywhere
- NO extra fingers, NO distorted hands
- 3:2 landscape aspect ratio (1536x1024)
"""


def remove_recurring_protagonist(prompt: str) -> str:
    """移除原 tava-ai prompt 中 Recurring protagonist 段（教練本人描述）"""
    if "Recurring protagonist 'the Coach'" in prompt:
        prompt = re.sub(
            r"Recurring protagonist 'the Coach'.*?(?=Style:)",
            "",
            prompt,
            flags=re.DOTALL,
        ).strip()
    return prompt


def extract_scene_only(prompt: str) -> str:
    """從原 prompt 抽出場景描述段（從第一段場景描述到 Style: 之前）"""
    # 移除 "pXX.jpg" 開頭
    prompt = re.sub(r"^p\d+\.jpg\s*\n", "", prompt)
    # 移除 Recurring protagonist 段
    prompt = remove_recurring_protagonist(prompt)
    # 移除 Style 段（因為會被 NARRATIVE_SUFFIX 取代）
    prompt = re.sub(r"Style:.*$", "", prompt, flags=re.DOTALL).strip()
    return prompt


def build_narrative_prompt(idx: int, title_zh: str) -> str:
    """根據原 prompt idx 構造敘事版 prompt"""
    prompts_data = json.load(open(PROMPTS_JSON))
    target_p = next(p for p in prompts_data if p["idx"] == idx)
    scene_only = extract_scene_only(target_p["prompt"])
    return scene_only + NARRATIVE_SUFFIX


def call_lk88_generation(prompt: str, size: str = SIZE) -> bytes:
    """純文字生圖（/v1/images/generations）"""
    api_key = get_api_key()
    data = json.dumps({
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": size,
        "n": 1,
        "quality": "auto",
    }).encode("utf-8")
    req = urllib.request.Request(
        LK888_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with lk888_guard.urlopen(req, timeout=180) as resp:
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
        boundary = "----TgNarrativeBoundary" + datetime.now().strftime("%H%M%S%f")
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
    p.add_argument("--indices", default="13,15,20", help="comma-separated idx list")
    args = p.parse_args()

    indices = [int(x) for x in args.indices.split(",")]

    print(f"=== 漫畫版 · 敘事版（Narrative Version）測試 ===", flush=True)
    print(f"=== 測試 {len(indices)} 張：p{', p'.join(f'{i:02d}' for i in indices)} ===", flush=True)
    print(f"=== Endpoint：{LK888_API_URL}（純文字、不鎖臉）===", flush=True)
    print(f"=== Size：{SIZE} | Model：gpt-image-2 ===\n", flush=True)

    prompts_data = json.load(open(PROMPTS_JSON))
    prompts_by_idx = {p["idx"]: p for p in prompts_data}

    for idx in indices:
        target_p = prompts_by_idx.get(idx)
        if not target_p:
            print(f"⚠️ p{idx:02d} 不存在", flush=True)
            continue

        out_jpg = DATA_DIR / f"narrative_p{idx:02d}_test.jpg"
        prompt = build_narrative_prompt(idx, target_p["title_zh"])

        print(f"\n[{time.strftime('%H:%M:%S')}] [{idx:02d}/28] {target_p['title_zh']}", flush=True)
        print(f"   Prompt 長度：{len(prompt)} chars", flush=True)

        t0 = time.time()
        try:
            png_bytes = call_lk88_generation(prompt, SIZE)
            elapsed = time.time() - t0
            size = png_to_jpeg(png_bytes, out_jpg, 85)
            print(f"   ✅ 存 {out_jpg.name} ({size} bytes, 生成 {elapsed:.1f}s)", flush=True)
            caption = f"🎬 敘事版 v_narrative 測試 p{idx:02d}｜{target_p['title_zh']}｜{elapsed:.0f}s"
            push_telegram(out_jpg, caption)
            print(f"   📲 已 push Telegram", flush=True)
        except Exception as e:
            print(f"   ❌ 失敗: {e}", flush=True)


if __name__ == "__main__":
    main()
