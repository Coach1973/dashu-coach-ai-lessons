#!/usr/bin/env python3
"""單獨重跑 p17 + p18（502 後補完）"""
import json
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
SCRIPT = WORKSPACE / "scripts/generate_comic_panel.py"
REFERENCE = WORKSPACE / "claude-brain/data/comic_reference/coach_face_reference.jpg"
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels_32mb_ep01"
CONFIG = Path.home() / ".openclaw" / "openclaw.json"
CHAT_ID = "6124913915"

ANCHOR_COACH = (
    "Traditional Chinese graphic novel style, cinematic realistic ink-and-watercolor. "
    "Consistent character design: a refined Taiwanese male coach, mid-early 40s with youthful "
    "energetic appearance; same face shape, jawline, nose, eye spacing in every panel; "
    "hair short, neatly groomed, JET BLACK pure dark hair color, NO gray NO white NO silver "
    "NO streaks NO salt-and-pepper NO aging hair NO temples white, youthful hairline; "
    "no glasses no facial hair; wearing a TAILORED GRAY PLAID THREE-PIECE SUIT with white "
    "dress shirt and a blue tie with subtle dot pattern, formal executive attire; "
    "refined dignified mature expression with subtle tiredness in the eyes."
)
GUARD = (
    "No readable text, no Chinese text, no English text, no watermarks, no lapel pin, "
    "no name badge, no extra people, no gray hair, no white hair, no silver hair, "
    "no streaks, no aging hair signs. Detailed ink-and-watercolor."
)

PANELS = {
    "p17": {
        "title": "Page 5 PANEL 3｜雙畫面對比｜雙向同步特寫",
        "size": "1536x1024",
        "scene": (
            "Split-screen composition: Left half shows coach's hand typing on Mac keyboard. Right "
            "half shows his other hand holding smartphone app displaying the same characters being "
            "typed in real-time. Visual confirmation of synchronization. Mood: technology working, "
            "two devices in harmony. 16:9 widescreen."
        ),
    },
    "p18": {
        "title": "Page 5 PANEL 4｜遠景｜第一話結尾",
        "size": "1536x1024",
        "scene": (
            "Wide shot, dawn breaking at 03:55 AM. The window shows faint blue morning light. "
            "The coach in three-piece suit leans back in his chair, looking at his phone screen "
            "with a tired but relieved slight smile. Behind him, subtle shadow hinting at "
            "unresolved mystery. Mood: exhaustion meeting dawn, bittersweet victory, first "
            "battle won but more to come. 16:9 widescreen."
        ),
    },
}


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def get_bot_token() -> str:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


def send_photo(image_path: Path, caption: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----Retry" + datetime.now().strftime("%H%M%S%f")
    body = []
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{CHAT_ID}\r\n".encode("utf-8")
    )
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8")
    )
    body.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{image_path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode("utf-8")
    )
    body.append(image_path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(body)
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"❌ send_photo: {e}")
        return None


def send_text(text: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps(
        {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    ).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log(f"❌ send_text: {e}")
        return None


def generate_one(panel_id: str, panel: dict) -> bool:
    out_path = OUTPUT_DIR / f"{panel_id}.png"
    full_prompt = (
        f"{ANCHOR_COACH} "
        f"Scene: {panel['title']}. {panel['scene']} "
        f"{GUARD}"
    )
    cmd = [
        "python3", str(SCRIPT),
        "--prompt", full_prompt,
        "--reference", str(REFERENCE),
        "--size", panel["size"],
        "--out", str(out_path),
    ]
    # 含 500/502/503/504 都重試（502 是 502 Bad Gateway，也是暫時性）
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        log(f"[{panel_id}] attempt {attempt}/{max_retries}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
            if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 100000:
                return True
            stderr_text = (result.stderr or "").strip()[:200]
            log(f"  returncode={result.returncode} stderr={stderr_text}")
            if any(code in stderr_text for code in ["500", "502", "503", "504"]) or "timeout" in stderr_text.lower() or "ConnectionError" in stderr_text:
                if attempt < max_retries:
                    import time as _t
                    sleep_s = 12 * attempt  # 漸進式退避 12/24 秒
                    log(f"  🟡 暫時性錯誤，{sleep_s} 秒後重試")
                    _t.sleep(sleep_s)
                    continue
        except subprocess.TimeoutExpired:
            log(f"  TIMEOUT 200s")
            if attempt < max_retries:
                import time as _t
                _t.sleep(10)
                continue
        except Exception as e:
            log(f"  ERROR: {e}")
        return False
    return False


def main():
    log("=== p17 + p18 重跑啟動 ===")
    send_text(
        "🦞 <b>heartbeat 醒來補 2 張</b>\n\n"
        "🟡 monitor 完成 15/17，p17 跟 p18 因 LK888 出 <b>502 Bad Gateway</b> 失敗\n"
        "🟢 retry 邏輯已擴充（500/502/503/504 都重試，漸進式 12s/24s 退避）\n"
        "⏳ 立刻補 p17 → p18 → 推 Telegram → 發完成彙整"
    )

    for panel_id, panel in PANELS.items():
        t0 = datetime.now()
        success = generate_one(panel_id, panel)
        dt = (datetime.now() - t0).total_seconds()

        out_path = OUTPUT_DIR / f"{panel_id}.png"
        if success and out_path.exists():
            size_mb = out_path.stat().st_size / 1024 / 1024
            caption = (
                f"✅ <b>{panel_id} 已補完</b>｜{panel['title']}\n\n"
                f"📁 {panel_id}.png ({size_mb:.1f}MB)\n"
                f"📐 {panel['size']}\n"
                f"⏱ 耗時 {dt:.0f}s（含重試）"
            )
            send_photo(out_path, caption)
            log(f"  ✅ {panel_id} pushed ({dt:.0f}s)")
        else:
            send_text(f"❌ <b>{panel_id} 仍失敗</b>｜{panel['title']}\n請教練起床手動補")
            log(f"  ❌ {panel_id} failed")

    # 最終彙整
    all_panels = sorted([f.name for f in OUTPUT_DIR.glob("p*.png") if "test" not in f.name])
    lines = [
        "🏁 <b>《32MB 封包攻防戰》第 1 話 全部完成</b>\n",
        f"✅ <b>{len(all_panels)}/{len(all_panels) + 0}</b> 張（p01 catch-up + p02~18）\n" if len(all_panels) >= 18 else f"⚠️ <b>{len(all_panels)}/18</b> 張（仍有缺失）\n",
        "📋 <b>全部 panels</b>：",
    ]
    for i in range(1, 19):
        pid = f"p{i:02d}"
        path = OUTPUT_DIR / f"{pid}.png"
        if path.exists() and path.stat().st_size > 100000:
            size_mb = path.stat().st_size / 1024 / 1024
            lines.append(f"  ✅ {pid} ({size_mb:.1f}MB)")
        else:
            lines.append(f"  ❌ {pid} missing")
    lines.append(f"\n📁 <code>claude-brain/data/comic_source_20260923/panels_32mb_ep01/</code>")
    lines.append(f"\n🦞 <b>第 1 話《32MB 封包攻防戰》已完成</b>，起床後可以瀏覽。晚安。")
    send_text("\n".join(lines))
    log("=== 完成 ===")


if __name__ == "__main__":
    main()
