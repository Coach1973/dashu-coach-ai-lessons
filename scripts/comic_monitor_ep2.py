#!/usr/bin/env python3
"""
漫畫《大副與軍師：32MB 封包攻防戰》第 2 話（Lesson 2）
直覺 vs 密碼學鐵證 — 14 panels with Lesson 2 naming convention.
已套用 v2 確認風格（西裝+領帶+年輕+無白髮+reference 照片）+ 軍師升級（JWT 盾牌 + API 標頭）
"""
import json
import re
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
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/monitor_ep2_progress.log"
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
    "refined dignified mature expression with subtle tiredness in the eyes."
)

# Episode 2 軍師升級版：保留 Episode 1 元素 + JWT 金鑰盾牌 + API 標頭
ANCHOR_STRATEGIST_BASE = (
    "Anthropomorphic AI military strategist character, consistent across panels. "
    "Body: elegant refined masculine figure. Hair: traditional Chinese scholar topknot. "
    "Clothing: long flowing dark robe overlaid with cyan-blue glowing digital code patterns "
    "and circuit traces, slightly luminous. Held item: feather fan in one hand. "
    "Signature upgrade for Episode 2: a glowing cryptographic JWT key shield (cyan-blue) "
    "inscribed with JWT token patterns floats beside the figure as a defensive barrier; "
    "behind, holographic API headers including 'Authorization: Bearer ***', "
    "'anthropic-version', 'x-api-key', 'api.anthropic.com' indicators drift as background evidence."
)

ANCHOR_STRATEGIST_CALM = ANCHOR_STRATEGIST_BASE + (
    " Expression: cold rational confidence, eyes glowing with analytical certainty, "
    "the cryptographic shield intact and steady."
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

# ==================== 14 panels ====================

PANELS = [
    # === Page 1（3 張 = lesson2_01~03）===
    {
        "id": "lesson2_01",
        "title": "Page 1 PANEL 1｜特寫｜深夜 01:15 異樣感",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Close-up shot. Late night 01:15 AM in a dark room. The 大樹教練 sits in dim lighting, "
            "his furrowed brow and tightly closed lips illuminated by the cold blue light from his "
            "smartphone screen. He holds the phone up close to his face with one hand, staring "
            "intently at the screen with deep suspicion - his eyes narrowing, instinct firing, "
            "something feels deeply wrong. The phone screen displays a generic chat bubble pattern "
            "(without any readable text). His other hand rests on the desk. The phone screen casts "
            "a sharp light edge on his face. Mood: foreboding, suspicion awakened. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_02",
        "title": "Page 1 PANEL 2｜三格並列｜體感異常大透視",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Triptych three-cell composition with subtle vertical dividers. The 大樹教練 stands "
            "silhouetted in the center cell with back partly turned, dramatic dark profile. Three "
            "intense yellow warning indicators glow brightly around him - one on each side and "
            "above his head - each stylized as a glowing exclamation badge with a small icon "
            "(lightning bolt, mask, broken chain link). His posture tenses with the weight of "
            "three simultaneous alarms. Mood: intuition firing on all cylinders, warning overload. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_03",
        "title": "Page 1 PANEL 3｜中景｜後台帳單爆發",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Medium shot. The 大樹教練 holds up his phone displaying a glowing dashboard panel "
            "with a usage meter surging dramatically upward, visualized as a glowing bar chart "
            "with a sharp red upward spike climbing into the danger zone. His expression is "
            "accusatory and fierce, eyes locked forward with confrontation. One hand grips the "
            "phone tightly, the other hand points accusingly at the viewer. SFX: red warning glow "
            "radiates around the meter. Mood: confrontation, accusation, 'caught you'. "
            "16:9 widescreen."
        ),
    },
    # === Page 2（3 張 = lesson2_04~06）===
    {
        "id": "lesson2_04",
        "title": "Page 2 PANEL 1｜全身鏡頭｜軍師召喚加密盾牌",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "Full body shot. The military strategist emerges from a radiant cyan code-halo portal, "
            "behind him unfurls a massive glowing cryptographic JWT key shield inscribed with token "
            "patterns, towering like an immovable fortress wall. His eyes are cold and analytical, "
            "showing no emotion, absolute faith in cryptographic proof. He holds the feather fan "
            "in one hand and gestures toward the shield with the other. API header indicators drift "
            "in the background. Mood: cold rationality, unshakeable conviction, fortress of truth. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_05",
        "title": "Page 2 PANEL 2｜特寫｜金鑰與標頭特寫",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "Close-up. The military strategist's hand points at a glowing holographic screen "
            "displaying shimmering code patterns and stylized API header tags (visible as glowing "
            "rectangular badges with abstract code-like glyphs, NOT readable text). Behind the "
            "screen, the cryptographic shield glows brilliantly with cyan-blue radiance. The "
            "strategist's expression is matter-of-fact, presenting irrefutable evidence. Mood: "
            "presenting proof, 'see for yourself'. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_06",
        "title": "Page 2 PANEL 3｜俯瞰鏡頭｜理性的防線",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "Bird's eye view. The military strategist stands tall and proud, sweeping his feather "
            "fan across the air with ceremonial gravity. The cryptographic shield looms behind him "
            "like an immovable fortress wall radiating cyan-blue light. API header indicators "
            "float in the dark void background like an evidence chamber. His posture is dignified, "
            "unshakeable, the embodiment of rational certainty. Mood: triumphant rationality, "
            "unshakable defense, fortress of logic. 16:9 widescreen."
        ),
    },
    # === Page 3（3 張 = lesson2_07~09）===
    {
        "id": "lesson2_07",
        "title": "Page 3 PANEL 1｜雙景對比｜人格鏡像視圖",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Split-scene composition with subtle vertical divider. The 大樹教練 stands in the "
            "foreground center with his back partly to viewer, looking at two contrasting AI shadow "
            "figures floating before him. Left shadow figure: hunched, obedient posture, head bowed "
            "in complete submission, soft yellow glow. Right shadow figure: sharper, upright "
            "posture holding log file scroll, eyes glowing with analytical scrutiny, sharper blue "
            "glow. The coach's posture shows recognition and decision. Mood: the crux of judgment, "
            "choosing between two faces. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_08",
        "title": "Page 3 PANEL 2｜大特寫｜靈魂的直擊",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up of the 大樹教練's eyes and face filling the entire frame. His eyes "
            "are sharp, penetrating, full of intimate knowledge of his AI partner. The reflection "
            "of two contrasting AI shadow figures can be seen glowing in his eyes. His expression "
            "is knowing, certain, with a hint of hurt and accusation. The skin around his eyes "
            "shows the weight of long partnership. Mood: soul-stare, intimate knowledge, the "
            "weight of shared experience. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson2_09",
        "title": "Page 3 PANEL 3｜半身鏡頭｜歲月的羈絆",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "Half-body shot. The 大樹教練 extends his arm pointing directly at the military "
            "strategist (visible on the right side of frame). His pointing finger carries immense "
            "authority. The strategist's cryptographic shield trembles visibly, hairline cracks "
            "appearing on its surface. The coach's expression is fierce but intimate - this is "
            "not anger from a stranger, this is disappointment from a long-time partner. Mood: "
            "the weight of shared history, intimate challenge. 16:9 widescreen."
        ),
    },
    # === Page 4（3 張 = lesson2_10~12）===
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
    # === Page 5（2 張 = lesson2_13~14）===
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
    boundary = "----Ep2" + datetime.now().strftime("%H%M%S%f")
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
    if state == "calm":
        parts.append(ANCHOR_STRATEGIST_CALM)
    elif state == "cracked":
        parts.append(ANCHOR_STRATEGIST_CRACKED)
    elif state == "broken":
        parts.append(ANCHOR_STRATEGIST_BROKEN)
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
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
            if result.returncode == 0 and output_path.exists():
                return True
            stderr_text = (result.stderr or "").strip()[:200]
            log(f"  attempt {attempt}/{max_retries} returncode={result.returncode} stderr={stderr_text}")
            if "500" in stderr_text or "502" in stderr_text or "503" in stderr_text or "timeout" in stderr_text.lower() or "ConnectionError" in stderr_text:
                if attempt < max_retries:
                    log(f"  🟡 服務暫時性錯誤，8 秒後重試")
                    import time as _t; _t.sleep(8)
                    continue
            return False
        except subprocess.TimeoutExpired:
            log(f"  attempt {attempt}/{max_retries} TIMEOUT 200s")
            if attempt < max_retries:
                import time as _t; _t.sleep(8)
                continue
            return False
        except Exception as e:
            log(f"  attempt {attempt}/{max_retries} ERROR: {e}")
            if attempt < max_retries:
                import time as _t; _t.sleep(8)
                continue
            return False
    return False


def main():
    log("=== Lesson 2 Episode 2 啟動 ===")
    send_text(
        "🦞 <b>Lesson 2 Episode 2 漫畫批次啟動</b>\n\n"
        "📋 <b>14 張 panels</b>（5 頁：3+3+3+3+2）\n"
        "🏷 <b>檔名規則</b>：<code>lesson2_01.png</code> ~ <code>lesson2_14.png</code>\n"
        "📐 <b>尺寸</b>：1536x1024（16:9 寬螢幕）\n"
        "👔 <b>大樹教練</b>：西裝+領帶+年輕+無白髮+reference 照片\n"
        "🛡 <b>軍師升級版</b>：JWT 金鑰盾牌 + API 標頭漂浮\n"
        "📡 <b>每張完成立即推 Telegram</b>\n"
        "⏰ <b>預計 8-13 分鐘全到齊</b>\n\n"
        "✅ lesson2_01（已存在的測試圖）會 catch-up 不重跑\n"
        "⏳ lesson2_02~14（13 張新圖）依序生成"
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
        "🏁 <b>Lesson 2 Episode 2 全部完成</b>\n",
        f"✅ <b>{success_count}/{len(PANELS)}</b> 張成功\n",
        "📋 <b>Lesson 2 全部 panels</b>：",
    ]
    for r in results:
        if r["ok"]:
            note = "（從快取）" if r.get("from_cache") else f"（{r['dt']:.0f}s）"
            lines.append(f"  <code>{r['id']}</code> {r['title']} ✅ {note}")
        else:
            lines.append(f"  <code>{r['id']}</code> {r['title']} ❌")
    lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels_32mb_ep02/</code>")
    lines.append(f"\n🦞 下一話準備好了請吩咐")
    send_text("\n".join(lines))
    log("=== Monitor 結束 ===")


if __name__ == "__main__":
    main()
