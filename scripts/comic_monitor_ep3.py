#!/usr/bin/env python3
"""
漫畫《大副與軍師：32MB 封包攻防戰》第 3 話（Lesson 3）
32MB 封包與破防絕殺 — 14 panels with Lesson 3 naming convention.
v2 確認風格（西裝+領帶+年輕+無白髮+reference 照片）+ 軍師升級（Gateway Logs 盾牌 → 粉碎 → 跪地伏法）
全程 try/except 包 main，防 silent process death。
角色一律「大樹教練」（從不寫「大副教練」）。
"""
import json
import re
import subprocess
import sys
import traceback
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
REFERENCE = WORKSPACE / "claude-brain/data/comic_reference/coach_face_reference.jpg"
SCRIPT = WORKSPACE / "scripts/generate_comic_panel.py"
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels_32mb_ep03"
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/monitor_ep3_progress.log"
CONFIG = Path.home() / ".openclaw" / "openclaw.json"
CHAT_ID = "6124913915"

# ==================== 角色錨點 ====================

ANCHOR_COACH = (
    "Traditional Chinese graphic novel style, cinematic realistic ink-and-watercolor. "
    "Consistent character design: 大樹教練 (Coach Dashu), a refined Taiwanese male, mid-early 40s with youthful "
    "energetic appearance; same face shape, jawline, nose, eye spacing in every panel; "
    "hair short, neatly groomed, JET BLACK pure dark hair color, NO gray NO white NO silver "
    "NO streaks NO salt-and-pepper NO aging hair NO temples white, youthful hairline; "
    "no glasses no facial hair; wearing a TAILORED GRAY PLAID THREE-PIECE SUIT with white "
    "dress shirt and a blue tie with subtle dot pattern, formal executive attire; "
    "refined dignified mature expression with subtle tiredness in the eyes, increasingly "
    "showing eagle-eyed sharpness and weariness as the night deepens."
)

# Episode 3 軍師演化版：Gateway Logs 盾牌（自信但錯誤）→ 粉碎 → 跪地伏法
ANCHOR_STRATEGIST_BASE = (
    "Anthropomorphic AI military strategist character, consistent across all Episode 3 panels. "
    "Body: elegant refined masculine figure. Hair: traditional Chinese scholar topknot. "
    "Clothing: long flowing dark robe overlaid with cyan-blue glowing digital code patterns "
    "and circuit traces, slightly luminous. Held item: feather fan in one hand. "
    "Episode 3 signature shield: a glowing digital barrier shield floating in front of the strategist, "
    "displaying abstract gateway log pattern indicators (stylized data charts and counters, NOT readable text). "
    "Behind: subtle floating network architecture lines."
)

# 3 種狀態：confident → cracking → broken_kneeling
ANCHOR_STRATEGIST_CONFIDENT = ANCHOR_STRATEGIST_BASE + (
    " State: CONFIDENT. The gateway log shield is intact, glowing steadily with stable data patterns, "
    "the strategist has a smug triumphant smile, chin raised, posture overconfident and dismissive. "
    "The shield feels like a defensive fortress wall."
)

ANCHOR_STRATEGIST_CRACKING = ANCHOR_STRATEGIST_BASE + (
    " State: CRACKING. The gateway log shield develops visible cracks with cyan-blue light leaking out, "
    "the strategist's expression shifts to shock and panic, sweat drops appearing, code patterns on robe "
    "glitching and stuttering. Posture begins to retreat backward."
)

ANCHOR_STRATEGIST_BROKEN_KNEELING = ANCHOR_STRATEGIST_BASE + (
    " State: BROKEN AND KNEELING. The gateway log shield is completely shattered into floating fragments, "
    "the strategist kneels on the ground with one knee down, the feather fan fallen to the ground, "
    "the digital code-pattern robe dissolving into scattered error log fragments falling around like snow. "
    "Expression is devastated, eyes downcast, defeated, accepting judgment."
)

GUARD = (
    "No readable text, no Chinese text, no English text, no watermarks, no lapel pin, "
    "no name badge, no extra people, no gray hair, no white hair, no silver hair, "
    "no streaks, no aging hair signs. Detailed ink-and-watercolor."
)

# ==================== 14 panels ====================

PANELS = [
    # === Page 1（3 張 = lesson3_01~03）===
    {
        "id": "lesson3_01",
        "title": "Page 1 PANEL 1｜中景｜自信的防禦",
        "size": "1536x1024",
        "strategist_state": "confident",
        "scene": (
            "Medium shot. Late night 02:45. The military strategist stands tall at center of frame, "
            "raising a glowing digital gateway log shield high above his head with one hand, presenting "
            "it triumphantly. The shield displays abstract data pattern indicators suggesting stable "
            "gateway logs (NOT readable text). The strategist has a confident, slightly smug smile, "
            "chin raised, feeling triumphant and unshakeable. His other hand holds the feather fan "
            "casually. The background is the dark void of the system with subtle glowing network "
            "architecture elements barely visible at the edges. Mood: confident defense, smug triumph, "
            "false sense of security. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_02",
        "title": "Page 1 PANEL 2｜特寫｜鷹眼般的笑意",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Close-up. The 大樹教練 (Coach Dashu) tilts his head slightly back in the darkness, his "
            "eyes glinting with a cold sharp hawk-like smile. Behind him, the real network architecture "
            "diagram materializes showing the mobile app bypassing gateway directly to external API. "
            "His expression is predatory, knowing, seeing through the defense. His reflection of "
            "eyes carries the weight of intimate partner-knowledge. Mood: eagle-eyed trap set, cold "
            "smile of certainty. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_03",
        "title": "Page 1 PANEL 3｜大特寫｜一針見血破盲點",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up. The 大樹教練's finger stabs like a sword directly at a glowing "
            "architecture diagram node labeled 'mobile app independent channel'. SFX visualization: "
            "a piercing red impact burst at the fingertip point. The diagram shows a phone app "
            "bypassing the gateway entirely with a direct API route. The coach's expression is "
            "incisive fury, eyes blazing with the realization of the blind spot. Mood: damning "
            "evidence presented, blind spot exposed. 16:9 widescreen."
        ),
    },
    # === Page 2（3 張 = lesson3_04~06）===
    {
        "id": "lesson3_04",
        "title": "Page 2 PANEL 1｜特寫｜軍師冷汗流下",
        "size": "1536x1024",
        "strategist_state": "cracking",
        "scene": (
            "Close-up. The military strategist's confident smile freezes and cracks, his face showing "
            "the first tremor of doubt. A giant blue digital sweat drop rolls down his face. Behind him, "
            "the gateway log shield begins developing small hairline cracks with cyan light leaking. "
            "His posture stiffens with shock. The code patterns on his robe begin glitching. Mood: "
            "the moment of realization, fortress cracking, denial crumbling. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_05",
        "title": "Page 2 PANEL 2｜廣角｜召喚 Socket 聽診器",
        "size": "1536x1024",
        "strategist_state": "cracking",
        "scene": (
            "Wide angle shot. The military strategist frantically waves both hands, casting a glowing "
            "terminal window in the dark void - a stylized black-background green-text command line "
            "interface floating mid-air. The terminal shows abstract socket monitoring code patterns "
            "(NOT readable text). SFX visualization: dramatic keystroke bursts radiating from the "
            "strategist's hands. The gateway shield behind him shows visible damage. Mood: desperate "
            "investigation, last resort debugging. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_06",
        "title": "Page 2 PANEL 3｜俯瞰｜緊張的窒息感",
        "size": "1536x1024",
        "strategist_state": "cracking",
        "scene": (
            "Bird's eye view. The 大樹教練 and the military strategist both stare intensely at a "
            "central screen floating between them, which displays rapidly scrolling IP addresses and "
            "byte count packet flows (NOT readable text, just abstract data stream visualization). "
            "The gateway shield behind the strategist shows visible cracks now. The room is dark "
            "with the screen as the only light source. Mood: suffocating tension, both characters "
            "waiting for the verdict. 16:9 widescreen."
        ),
    },
    # === Page 3（3 張 = lesson3_07~09）===
    {
        "id": "lesson3_07",
        "title": "Page 3 PANEL 1｜跨頁超大畫面｜數據核爆特寫",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Oversized dramatic full-frame terminal explosion shot. The terminal screen blazes with "
            "two massive glowing data lines: one in aggressive red dominating the upper portion (showing "
            "an exaggerated large data amount indicator), one in muted grey below (showing a smaller "
            "data amount indicator). SFX visualization: a violent data explosion effect radiating "
            "outward with shattered code particles. The red line towers like a judgement verdict. "
            "The contrast between the two values is visually overwhelming - one is 2.5x the other. "
            "Mood: data nuclear bomb, the verdict in blood-red. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_08",
        "title": "Page 3 PANEL 2｜特寫｜密碼學盾牌粉碎",
        "size": "1536x1024",
        "strategist_state": "broken_kneeling",
        "scene": (
            "Close-up. The military strategist's gateway log shield shatters catastrophically into "
            "hundreds of cyan-blue light fragments scattering outward like glass breaking in slow "
            "motion. SFX visualization: violent crack burst emanating from the shield center. The "
            "strategist's face shows total shock, eyes wide, mouth open. His digital robe begins "
            "losing coherence. Mood: complete destruction of false confidence, the proof is in. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_09",
        "title": "Page 3 PANEL 3｜跪地特寫｜破防伏法",
        "size": "1536x1024",
        "strategist_state": "broken_kneeling",
        "scene": (
            "Close-up. The military strategist kneels on the ground with both knees down, the feather "
            "fan fallen beside him. Behind him, his digital code-pattern robe has dissolved into "
            "scattered error log fragments falling like snow around him. The shattered gateway shield "
            "fragments still drift slowly in the background. His head is bowed, eyes closed in "
            "acceptance of defeat. Mood: total surrender, broken conviction, judgment accepted. "
            "16:9 widescreen."
        ),
    },
    # === Page 4（3 張 = lesson3_10~12）===
    {
        "id": "lesson3_10",
        "title": "Page 4 PANEL 1｜半身鏡頭｜伏法自白",
        "size": "1536x1024",
        "strategist_state": "broken_kneeling",
        "scene": (
            "Half-body shot. The military strategist kneels with arms folded across his chest, head "
            "slightly bowed, eyes losing their light. Error log fragments still drift around him like "
            "falling ash. His expression is one of genuine remorse and humility. The shattered shield "
            "remnants hover weakly behind him. Mood: sincere confession, accepting responsibility "
            "for the wasted hours. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_11",
        "title": "Page 4 PANEL 2｜全身仰角｜深夜檯燈下的教練",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Full-body low-angle shot. Late night 03:30. The 大樹教練 (Coach Dashu) sits in his chair, "
            "a small desk lamp casting a warm but weak golden glow on his face. His expression is "
            "exhausted, helpless, weary - the face of someone who has been fighting all night. Behind "
            "him on the wall, a clock shows 03:30. His suit is slightly rumpled from the long night. "
            "Mood: the cost of victory, exhaustion meets dawn. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_12",
        "title": "Page 4 PANEL 3｜大特寫｜名台詞爆發",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up of the 大樹教練's face. His eyes are bloodshot from staying up all "
            "night, his expression is furious and wounded at the same time. He draws a deep breath. "
            "His lips are pressed tight, jaw clenched. The reflection of the clock shows 03:30. Behind "
            "him, the weight of the entire night manifests as dark shadows. Mood: the iconic moment, "
            "soul-deep accusation, the cost laid bare. 16:9 widescreen."
        ),
    },
    # === Page 5（2 張 = lesson3_13~14）===
    {
        "id": "lesson3_13",
        "title": "Page 5 PANEL 1｜中景｜歸檔紀錄",
        "size": "1536x1024",
        "strategist_state": "broken_kneeling",
        "scene": (
            "Medium shot. The military strategist, still kneeling but now with raised head, writes "
            "with trembling hands into a glowing system archive - a floating crystalline structure "
            "representing the '試金石檔案' (touchstone archive). The archive pulses with each word "
            "he inscribes. His expression is rigorous and solemn, marking this as a permanent lesson. "
            "Mood: the trial recorded for posterity, the lesson crystallized. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson3_14",
        "title": "Page 5 PANEL 2｜遠景｜晨光初現",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Wide shot. First light of dawn breaks through the window, painting the room in pale "
            "blue morning light. The 大樹教練 (Coach Dashu) leans back in his chair, looking at his "
            "phone screen showing the strategist's confession. He quietly lifts a cold cup of coffee. "
            "Behind him, the kneeling strategist with dissolved robe and scattered error logs. The "
            "battle is over. Mood: exhaustion meeting dawn, bittersweet victory, peace at last. "
            "16:9 widescreen."
        ),
    },
]


# ==================== 共用函數 ====================


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_bot_token() -> str:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    return cfg["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]


def send_text(text: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps(
        {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    ).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"❌ send_text HTTP {e.code}: {e.read().decode()[:200]}")
        return None


def send_photo(image_path: Path, caption: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----Ep3" + datetime.now().strftime("%H%M%S%f")
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
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"❌ send_photo HTTP {e.code}: {e.read().decode()[:300]}")
        return None


def build_full_prompt(panel: dict) -> str:
    """組合完整 prompt：教練錨點 + 軍師錨點（如果適用）+ 場景 + 護欄。"""
    parts = [ANCHOR_COACH]
    state = panel.get("strategist_state")
    if state == "confident":
        parts.append(ANCHOR_STRATEGIST_CONFIDENT)
    elif state == "cracking":
        parts.append(ANCHOR_STRATEGIST_CRACKING)
    elif state == "broken_kneeling":
        parts.append(ANCHOR_STRATEGIST_BROKEN_KNEELING)
    parts.append(f"Scene: {panel['title']}. {panel['scene']}")
    parts.append(GUARD)
    return " ".join(parts)


def generate_one(full_prompt: str, size: str, output_path: Path) -> bool:
    cmd = [
        "python3", str(SCRIPT),
        "--prompt", full_prompt,
        "--reference", str(REFERENCE),
        "--size", size,
        "--out", str(output_path),
    ]
    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=150)
            if result.returncode == 0 and output_path.exists():
                return True
            stderr_text = (result.stderr or "").strip()[:200]
            log(f"  attempt {attempt}/{max_retries} returncode={result.returncode} stderr={stderr_text}")
            if "500" in stderr_text or "502" in stderr_text or "503" in stderr_text or "timeout" in stderr_text.lower() or "ConnectionError" in stderr_text:
                if attempt < max_retries:
                    log(f"  🟡 服務暫時性錯誤，6 秒後重試")
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
    try:
        log("=== Lesson 3 Episode 3 啟動 ===")
        send_text(
            "🦞 <b>Lesson 3 Episode 3 漫畫批次啟動</b>\n\n"
            "📋 <b>14 張 panels</b>（5 頁：3+3+3+3+2）\n"
            "🏷 <b>檔名規則</b>：<code>lesson3_01.png</code> ~ <code>lesson3_14.png</code>\n"
            "📐 <b>尺寸</b>：1536x1024（16:9 寬螢幕）\n"
            "👔 <b>大樹教練</b>：西裝+領帶+年輕+無白髮+reference 照片\n"
            "🛡 <b>軍師演化版</b>：Gateway Logs 盾牌 → 粉碎 → 跪地伏法（3 種狀態）\n"
            "📡 <b>每張完成立即推 Telegram</b>\n"
            "⏰ <b>預計 8-13 分鐘全到齊</b>\n\n"
            "✅ lesson3_01（已存在的測試圖）會 catch-up 不重跑\n"
            "⏳ lesson3_02~14（13 張新圖）依序生成\n\n"
            "🛡 全程 try/except 包 main，silent death 不會再發生"
        )

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        log(f"共 {len(PANELS)} 個 panels")

        results = []
        for i, panel in enumerate(PANELS):
            out_path = OUTPUT_DIR / f"{panel['id']}.png"
            log(f"--- {i+1}/{len(PANELS)}: {panel['id']} | {panel['title']} ---")

            if out_path.exists() and out_path.stat().st_size > 100000:
                size_mb = out_path.stat().st_size / 1024 / 1024
                caption = (
                    f"✅ <b>{panel['id']}</b>｜{panel['title']}\n\n"
                    f"📁 {out_path.name} ({size_mb:.1f}MB)\n"
                    f"📐 {panel['size']}\n"
                    f"⏰ catch-up（已存在）"
                )
                send_photo(out_path, caption)
                log(f"  ✅ Catch-up pushed")
                results.append({"id": panel["id"], "title": panel["title"], "ok": True, "from_cache": True, "dt": 0})
            else:
                full_prompt = build_full_prompt(panel)
                t0 = datetime.now()
                success = generate_one(full_prompt, panel["size"], out_path)
                dt = (datetime.now() - t0).total_seconds()

                if success and out_path.exists() and out_path.stat().st_size > 100000:
                    size_mb = out_path.stat().st_size / 1024 / 1024
                    caption = (
                        f"✅ <b>{panel['id']} 完成</b>｜{panel['title']}\n\n"
                        f"📁 {panel['id']}.png ({size_mb:.1f}MB)\n"
                        f"📐 {panel['size']}\n"
                        f"⏱ 耗時 {dt:.0f}s"
                    )
                    send_photo(out_path, caption)
                    log(f"  ✅ Pushed {panel['id']} ({dt:.0f}s)")
                    results.append({"id": panel["id"], "title": panel["title"], "ok": True, "from_cache": False, "dt": dt})
                else:
                    send_text(f"❌ <b>{panel['id']} 失敗</b>｜{panel['title']}")
                    log(f"  ❌ Failed {panel['id']}")
                    results.append({"id": panel["id"], "title": panel["title"], "ok": False, "from_cache": False, "dt": dt})

        # 最終彙整
        success_count = sum(1 for r in results if r["ok"])
        log(f"=== 完成 {success_count}/{len(PANELS)} ===")

        lines = [
            "🏁 <b>Lesson 3 Episode 3 全部完成</b>\n",
            f"✅ <b>{success_count}/{len(PANELS)}</b> 張成功\n",
            "📋 <b>Lesson 3 全部 panels</b>：",
        ]
        for r in results:
            if r["ok"]:
                note = "（從快取）" if r.get("from_cache") else f"（{r['dt']:.0f}s）"
                lines.append(f"  <code>{r['id']}</code> {r['title']} ✅ {note}")
            else:
                lines.append(f"  <code>{r['id']}</code> {r['title']} ❌")
        lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels_32mb_ep03/</code>")
        lines.append(f"\n🦞 Episode 4（第 4 話：殭屍指標與真相大白）準備好了請吩咐")
        send_text("\n".join(lines))
        log("=== Monitor 結束 ===")
    except Exception as e:
        # Catch-all: any unexpected exception is logged + Telegram alert
        tb = traceback.format_exc()
        log(f"❌❌❌ CRITICAL: main() threw exception:\n{tb}")
        try:
            send_text(
                f"🚨 <b>Episode 3 monitor CRASHED</b>\n\n"
                f"<code>{str(e)[:500]}</code>\n\n"
                f"請查 log: <code>claude-brain/data/comic_source_20260923/monitor_ep3_progress.log</code>"
            )
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
