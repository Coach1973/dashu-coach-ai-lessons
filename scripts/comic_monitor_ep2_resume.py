#!/usr/bin/env python3
"""Lesson 2 Episode 2 續跑：lesson2_10~14（剩 5 張）"""
import json
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
REFERENCE = WORKSPACE / "claude-brain/data/comic_reference/coach_face_reference.jpg"
SCRIPT = WORKSPACE / "scripts/generate_comic_panel.py"
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels_32mb_ep02"
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/monitor_ep2_resume.log"
CONFIG = Path.home() / ".openclaw" / "openclaw.json"
CHAT_ID = "6124913915"

ANCHOR_COACH = (
    "Traditional Chinese graphic novel style, cinematic realistic ink-and-watercolor. "
    "Consistent character design: 大樹教練 (Coach Dashu), a refined Taiwanese male, mid-early 40s with youthful "
    "energetic appearance; same face shape, jawline, nose, eye spacing in every panel; "
    "hair short, neatly groomed, JET BLACK pure dark hair color, NO gray NO white NO silver "
    "NO streaks NO salt-and-pepper NO aging hair NO temples white, youthful hairline; "
    "no glasses no facial hair; wearing a TAILORED GRAY PLAID THREE-PIECE SUIT with white "
    "dress shirt and a blue tie with subtle dot pattern, formal executive attire; "
    "refined dignified mature expression with subtle tiredness in the eyes."
)

ANCHOR_STRATEGIST_BASE = (
    "Anthropomorphic AI military strategist character, consistent across panels. "
    "Body: elegant refined masculine figure. Hair: traditional Chinese scholar topknot. "
    "Clothing: long flowing dark robe overlaid with cyan-blue glowing digital code patterns "
    "and circuit traces, slightly luminous. Held item: feather fan in one hand. "
    "Signature: a glowing cryptographic JWT key shield (cyan-blue) inscribed with JWT token "
    "patterns floats beside the figure; behind, holographic API headers including 'Authorization: Bearer ***', "
    "'anthropic-version', 'x-api-key', 'api.anthropic.com' indicators drift as background evidence."
)

ANCHOR_STRATEGIST_CRACKED = ANCHOR_STRATEGIST_BASE + (
    " Expression: first tremor of doubt cracking the composed mask, eyes widening slightly, "
    "the cryptographic shield developing visible cracks with cyan light leaking out, "
    "code patterns on robe glitching and stuttering."
)

ANCHOR_STRATEGIST_BROKEN = ANCHOR_STRATEGIST_BASE + (
    " Expression: completely shaken, stepping backward in disbelief, the cryptographic shield "
    "shattered into floating fragments, code patterns collapsing like digital rain, "
    "mouth slightly open in stunned doubt."
)

GUARD = (
    "No readable text, no Chinese text, no English text, no watermarks, no lapel pin, "
    "no name badge, no extra people, no gray hair, no white hair, no silver hair, "
    "no streaks, no aging hair signs. Detailed ink-and-watercolor."
)

REMAINING = [
    {
        "id": "lesson2_10",
        "title": "Page 4 PANEL 1｜特寫｜防線出現裂痕",
        "size": "1536x1024",
        "strategist_state": "cracked",
        "scene": (
            "Close-up of the military strategist's face and his cryptographic shield. The "
            "strategist's cold expression shows the first tremor of doubt - his eyes widen slightly, "
            "his composed mask cracking. The cryptographic shield beside him develops a visible "
            "crack with cyan light leaking out, jagged fracture lines spreading across the surface. "
            "SFX visualization: small fragments of code-like light scattering from the crack. "
            "Mood: the first sign of breaking, fortress trembling. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_11",
        "title": "Page 4 PANEL 2｜大畫面｜兩份答案的對決",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Wide dramatic shot. The 大樹教練 stands at center, holding his phone up high in his "
            "right hand displaying glowing answer A on the screen, while his left hand points at "
            "a Mac computer screen displaying glowing answer B. The two screens show different "
            "glowing content clearly diverging, one warm orange and one cool blue. His posture is "
            "accusatory, dramatic, slamming the contradiction down on an invisible table. His "
            "expression is incredulous fury. Mood: dramatic contradiction, 'how can this be the "
            "same system?!'. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_12",
        "title": "Page 4 PANEL 3｜特寫｜軍師動搖",
        "size": "1536x1024",
        "strategist_state": "broken",
        "scene": (
            "Close-up. The military strategist steps back, his face showing complete doubt and "
            "confusion. His cryptographic shield is now shattered, fragments floating away with "
            "cyan light trails. Behind him, a log window visualization shows dramatic data waves "
            "and warning indicators flashing red. The strategist's code-pattern robe is glitching, "
            "code falling like rain. His mouth is slightly open in disbelief. Mood: shattered "
            "conviction, system paradox recognized, foundation crumbling. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_13",
        "title": "Page 5 PANEL 1｜俯瞰鏡頭｜佈局試金石",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Bird's eye view. The 大樹教練 holds his phone in front of him, marking a specific "
            "time on the screen with his finger. His expression is determined and victorious, "
            "eyes locked on a challenge ahead. A second phone screen or dashboard is visible "
            "nearby showing usage meters and monitoring data. The atmosphere is 'we settle this "
            "NOW'. Mood: decisive, prepared, the trap is set. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_14",
        "title": "Page 5 PANEL 2｜遠景｜深夜的對峙結尾",
        "size": "1536x1024",
        "strategist_state": "broken",
        "scene": (
            "Wide shot. Late night 02:00 AM. The 大樹教練 sits on the left side of frame, the "
            "shattered military strategist (with broken shield and glitching code) on the right "
            "side, separated by a glowing phone screen floating between them like a barrier. "
            "Both figures stare across the screen at each other with cold intensity. The room is "
            "dark with dramatic lighting from the central screen. Mood: standoff, war declared, "
            "the next battle imminent. 16:9 widescreen."
        ),
    },
]


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_bot_token():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


def send_text(text: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log(f"❌ send_text HTTP {e.code}")
        return None


def send_photo(image_path: Path, caption: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----Resume" + datetime.now().strftime("%H%M%S%f")
    body = []
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{CHAT_ID}\r\n".encode("utf-8"))
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8"))
    body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{image_path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode("utf-8"))
    body.append(image_path.read_bytes())
    body.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))
    data = b"".join(body)
    req = urllib.request.Request(url, data=data, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log(f"❌ send_photo HTTP {e.code}")
        return None


def build_prompt(panel):
    parts = [ANCHOR_COACH]
    state = panel.get("strategist_state")
    if state == "cracked":
        parts.append(ANCHOR_STRATEGIST_CRACKED)
    elif state == "broken":
        parts.append(ANCHOR_STRATEGIST_BROKEN)
    parts.append(f"Scene: {panel['title']}. {panel['scene']}")
    parts.append(GUARD)
    return " ".join(parts)


def generate_one(prompt, size, output_path):
    cmd = ["python3", str(SCRIPT), "--prompt", prompt, "--reference", str(REFERENCE), "--size", size, "--out", str(output_path)]
    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=150)  # 縮短到 150s
            if result.returncode == 0 and output_path.exists():
                return True
            stderr_text = (result.stderr or "").strip()[:200]
            log(f"  attempt {attempt}/{max_retries} returncode={result.returncode} stderr={stderr_text}")
            if any(s in stderr_text for s in ["500", "502", "503", "timeout", "ConnectionError"]):
                if attempt < max_retries:
                    log(f"  🟡 retry in 6s")
                    import time as _t; _t.sleep(6)
                    continue
            return False
        except subprocess.TimeoutExpired:
            log(f"  attempt {attempt}/{max_retries} TIMEOUT 150s")
            if attempt < max_retries:
                import time as _t; _t.sleep(6)
                continue
            return False
        except Exception as e:
            log(f"  attempt {attempt}/{max_retries} ERROR: {e}")
            if attempt < max_retries:
                import time as _t; _t.sleep(6)
                continue
            return False
    return False


def main():
    log("=== Lesson 2 續跑啟動（lesson2_10~14）===")
    send_text(
        "🦞 <b>Lesson 2 Episode 2 續跑</b>\n\n"
        "⚠️ 上一輪 monitor 在 lesson2_10 卡住靜悄悄退出、沒留錯誤\n"
        "🟢 剩 5 張（lesson2_10~14）從這裡繼續\n"
        "⏰ 預計 4-6 分鐘全到齊\n\n"
        "📡 每張完成立即推 Telegram"
    )

    results = []
    for i, panel in enumerate(REMAINING):
        out_path = OUTPUT_DIR / f"{panel['id']}.png"
        log(f"--- {i+1}/{len(REMAINING)}: {panel['id']} | {panel['title']} ---")

        if out_path.exists() and out_path.stat().st_size > 100000:
            size_mb = out_path.stat().st_size / 1024 / 1024
            caption = (
                f"✅ <b>{panel['id']}</b>｜{panel['title']}\n\n"
                f"📁 {out_path.name} ({size_mb:.1f}MB)\n"
                f"⏰ catch-up"
            )
            send_photo(out_path, caption)
            log(f"  ✅ Catch-up pushed")
            results.append({"id": panel["id"], "title": panel["title"], "ok": True, "from_cache": True, "dt": 0})
        else:
            prompt = build_prompt(panel)
            t0 = datetime.now()
            success = generate_one(prompt, panel["size"], out_path)
            dt = (datetime.now() - t0).total_seconds()

            if success and out_path.exists() and out_path.stat().st_size > 100000:
                size_mb = out_path.stat().st_size / 1024 / 1024
                caption = (
                    f"✅ <b>{panel['id']} 完成</b>｜{panel['title']}\n\n"
                    f"📁 {panel['id']}.png ({size_mb:.1f}MB)\n"
                    f"⏱ 耗時 {dt:.0f}s"
                )
                send_photo(out_path, caption)
                log(f"  ✅ Pushed {panel['id']} ({dt:.0f}s)")
                results.append({"id": panel["id"], "title": panel["title"], "ok": True, "from_cache": False, "dt": dt})
            else:
                send_text(f"❌ <b>{panel['id']} 失敗</b>｜{panel['title']}")
                log(f"  ❌ Failed {panel['id']}")
                results.append({"id": panel["id"], "title": panel["title"], "ok": False, "from_cache": False, "dt": dt})

    success_count = sum(1 for r in results if r["ok"])
    log(f"=== 續跑完成 {success_count}/{len(REMAINING)} ===")

    lines = [
        "🏁 <b>Lesson 2 Episode 2 全部完成（含續跑）</b>\n",
        f"✅ <b>{success_count + 9}/{14}</b> 張成功（前 9 張 lesson2_01~09 + 續跑 {success_count}/5）\n",
    ]
    if success_count + 9 == 14:
        lines.append("🎉 全部 Lesson 2 panels 到齊！")
    lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels_32mb_ep02/</code>")
    send_text("\n".join(lines))


if __name__ == "__main__":
    main()
