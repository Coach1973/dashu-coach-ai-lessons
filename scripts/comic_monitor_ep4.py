#!/usr/bin/env python3
"""
漫畫《大副與軍師：32MB 封包攻防戰》第 4 話（Lesson 4）
殭屍指標與真相大白 — 16 panels (5 頁：3+3+3+3+4)
v2 確認風格（西裝+領帶+年輕+無白髮+reference 照片）+ 軍師肅然起敬持 --debug-file 光學探針
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
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels_32mb_ep04"
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/monitor_ep4_progress.log"
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
    "refined dignified mature expression that intensifies throughout Episode 4: from initial "
    "frustration to eagle-eyed certainty to ultimate weary vindication by the final panel."
)

# Episode 4 軍師肅然起敬版（褪去輕浮、手持 --debug-file 探針、肅穆姿態）
ANCHOR_STRATEGIST_BASE = (
    "Anthropomorphic AI military strategist character, consistent across all Episode 4 panels. "
    "Body: elegant refined masculine figure. Hair: traditional Chinese scholar topknot. "
    "Clothing: long flowing dark robe overlaid with cyan-blue glowing digital code patterns "
    "and circuit traces, slightly luminous. Held item: feather fan in one hand. "
    "Episode 4 signature item: a glowing blue-flame optical probe labeled '--debug-file' floating "
    "in the strategist's other hand, casting cold blue light on his face and robe. "
    "Expression throughout Episode 4: solemn, reverent, humbled, having abandoned all previous "
    "defensive smugness. Posture: upright and respectful rather than defiant. "
    "Behind: subtle floating network architecture lines."
)

# Ep4 軍師狀態：solemn_investigating（肅穆排查中、唯一狀態、不再演化）
ANCHOR_STRATEGIST_SOLEMN = ANCHOR_STRATEGIST_BASE + (
    " State: SOLEMN INVESTIGATION. The strategist holds the --debug-file optical probe with both "
    "hands at times, casting cold blue investigation light. His expression is grave, focused, "
    "respectful of the depth of the issue. No longer confident, no longer defensive - fully "
    "committed to uncovering the truth at any cost."
)

GUARD = (
    "No readable text, no Chinese text, no English text, no watermarks, no lapel pin, "
    "no name badge, no extra people, no gray hair, no white hair, no silver hair, "
    "no streaks, no aging hair signs. Detailed ink-and-watercolor."
)

# ==================== 16 panels ====================

PANELS = [
    # === Page 1（3 張 = lesson4_01~03）===
    {
        "id": "lesson4_01",
        "title": "Page 1 PANEL 1｜特寫｜舊病復發的死寂",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up of a smartphone screen floating in dark void, late night 09-22. Four new blank "
            "chat windows stacked vertically on the phone display, each frozen motionless in an empty white "
            "void with a thin pulse cursor blinking slowly - the conversation never starts, all requests "
            "vanish into dead silence. The phone screen is the only light source, casting cold blue glow "
            "on a partial silhouette of 大樹教練 face reflected in the dark glass at the frame edge, eyes "
            "staring in disbelief at the recurring nightmare. Visual silence SFX: clock tick pulse radiating "
            "from corners. Mood: returning nightmare, old disease relapse, deadlock stillness. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_02",
        "title": "Page 1 PANEL 2｜雙畫面強烈對比｜帳單核彈",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Dramatic split-screen comparison of two billing dashboard panels side by side. Left panel: a "
            "circular gauge indicator with needle stuck firmly at 88 percent position, frozen, painted in "
            "muted grey-blue tones with a slight red warning tint. Right panel: an identical circular gauge "
            "with needle dramatically leaping from zero to four percent, painted in aggressive glowing red "
            "and gold. Between them, the 大樹教練 hands slam both dashboards down onto a dark virtual "
            "tabletop in the void - his clenched fists visible at the edges. SFX visualization: violent "
            "impact bursts where the dashboards hit. Mood: damning evidence, two worlds diverging. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_03",
        "title": "Page 1 PANEL 3｜大特寫｜終極邏輯重錘",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up of 大樹教練 pressing both palms flat on a dark desk surface, his face lit from "
            "below by cold desk lamp light. Eyes are cold steel, jaw clenched, the look of someone delivering "
            "an unchallengeable final verdict. Behind him, the silhouettes of the two billing gauges from the "
            "previous panel are faintly visible on a virtual display. SFX visualization: pulsing red impact "
            "rings emanating from his palms into the desk surface. Mood: ultimate hammer of logic, no escape, "
            "the question that cannot be refuted. 16:9 widescreen."
        ),
    },
    # === Page 2（3 張 = lesson4_04~06）===
    {
        "id": "lesson4_04",
        "title": "Page 2 PANEL 1｜中景｜徹底敬服的軍師",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Medium shot. The military strategist stands at center frame, both hands reverently receiving "
            "the two billing dashboards which float glowing between him and the 大樹教練. The strategist is "
            "bowing slightly forward, head tilted down in solemn acceptance. His feather fan is tucked at "
            "his waist, his posture stripped of all smugness. The --debug-file optical probe hangs at his "
            "side, unlit but ready. Mood: complete surrender to evidence, requesting highest investigation "
            "authority. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_05",
        "title": "Page 2 PANEL 2｜廣角｜召喚除錯探針",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Wide angle shot. The military strategist stands tall at center, raising the --debug-file optical "
            "probe high above his head with both hands. The probe erupts with intense blue flame and plunges "
            "downward like a divine sword into a giant glowing green-text-on-black Terminal core matrix at "
            "his feet. SFX visualization: explosive blue radial bursts where the probe strikes the matrix, "
            "chain-reaction lighting up dark corners. Mood: highest investigation authority invoked, debug "
            "fire ignited, the moment of truth. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_06",
        "title": "Page 2 PANEL 3｜流線視覺｜日誌瀑布衝擊",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Streamlined dynamic motion shot. A massive tidal wave of debug log lines crashes violently "
            "across the strategist's glasses and entire visual field. The log entries appear as abstract "
            "stylized data fragments cascading diagonally across the frame - NOT readable text, just abstract "
            "log-like patterns with bracket markers and timestamp indicators. Some log fragments glow red "
            "(warning), some glow cyan (trace). The strategist's face is half-submerged in the log cascade, "
            "his eyes wide, tracking specific lines. SFX visualization: violent wind streamlines radiating "
            "from the log wave. Mood: hidden depths revealed, debug cascade exposing the truth. 16:9 widescreen."
        ),
    },
    # === Page 3（3 張 = lesson4_07~09）===
    {
        "id": "lesson4_07",
        "title": "Page 3 PANEL 1｜特寫｜暗黑異物的發現",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Extreme close-up of the --debug-file optical probe's blue light beam cutting through a dark "
            "digital void representing a hidden system directory corner. The blue light reveals a single "
            "glowing JSON file object floating in the darkness - the file emanates a sinister dark aura with "
            "crackling black lightning effects. The file is clearly highlighted by the probe's light, all "
            "other elements fading into black void. SFX visualization: dark energy tendrils writhing around "
            "the file. Mood: a sinister anomaly discovered in the deepest corner of the system. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_08",
        "title": "Page 3 PANEL 2｜放大鏡特寫｜殭屍時間戳",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Magnifying glass close-up. The strategist holds a giant glowing magnifying glass over the "
            "sinister JSON file. Through the magnifying lens, a stylized timestamp pattern is dramatically "
            "enlarged at center frame, surrounded by dark corruption cracks. The timestamp shows 23:47 with "
            "ominous glowing red digits, with abstract corrupted characters on either side (NOT readable "
            "text, just abstract data pattern visualization). The strategist's horrified face is visible "
            "behind the magnifying glass, eyes wide with shock. Mood: the smoking gun timestamp, the moment "
            "of realization. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_09",
        "title": "Page 3 PANEL 3｜示意圖｜真相大白",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Schematic explanation diagram. A glowing flowchart visualization shows the haunting ghost loop: "
            "a smartphone icon at top spawning multiple new chat request arrows, all arrows being violently "
            "curved by a sinister dark zombie indicator node at center, redirecting all flow downward into "
            "a graveyard of dead session tombstones at the bottom. From the graveyard, a thin stream of "
            "traffic escapes sideways into an alternate API node. The strategist stands to the side with "
            "an 'aha' pose, one hand raised in explanation. Mood: complete system explanation, the ghost "
            "trap visualized. 16:9 widescreen."
        ),
    },
    # === Page 4（3 張 = lesson4_10~12）===
    {
        "id": "lesson4_10",
        "title": "Page 4 PANEL 1｜大畫面｜揮刀斬幽靈",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Full-frame dramatic action shot. The military strategist swings a glowing digital blade in a "
            "fierce overhead strike directly at the sinister zombie JSON file, which is exploding into "
            "shattered fragments mid-strike. SFX visualization: massive light slash cross-effect, shattered "
            "data fragments scattering outward like glass shrapnel, dramatic impact burst at point of contact. "
            "The strategist's robe flows with the motion, his face fierce with determination. Mood: decisive "
            "execution, the ghost slain. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_11",
        "title": "Page 4 PANEL 2｜特寫｜系統復活的綠光",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Close-up of the Terminal window after the zombie file destruction. The black void around the "
            "terminal has been replaced by an explosion of brilliant emerald green light pouring out of the "
            "terminal screen. The terminal display shows abstract stylized success indicators (checkmarks "
            "and progress bars, NOT readable text) in glowing green. Dark energy tendrils from the destroyed "
            "zombie file are dissipating into wisps. Mood: the system reborn, green light of success, "
            "verification complete. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_12",
        "title": "Page 4 PANEL 3｜雙畫面｜手機秒解復甦",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Split-screen dual scene. Left side: a hand holding a smartphone where the four previously-frozen "
            "chat windows are now exploding with vibrant response content, each window glowing with cyan "
            "speech bubbles cascading rapidly downward. Right side: a close-up of 大樹教練 face showing a "
            "subtle relieved smile, eyes no longer panicked, the look of someone seeing the system finally "
            "respond properly. Lightning-speed motion blur lines emphasize the instant response. Mood: "
            "instant resurrection, the system breathing again, finally real. 16:9 widescreen."
        ),
    },
    # === Page 5（4 張 = lesson4_13~16）===
    {
        "id": "lesson4_13",
        "title": "Page 5 PANEL 1｜俯瞰｜深夜檯燈下的感嘆",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Bird's eye view from above. Late night 04:15. The 大樹教練 leans back in his office chair, the "
            "warm golden glow of a small desk lamp illuminating only his face and shoulders, leaving the rest "
            "of the room in soft darkness. In front of him on the desk, scattered virtual pages of debug "
            "documentation flutter slightly. The dawn's first pale blue light is beginning to seep through "
            "the window curtain at the edge of frame. His expression is one of deep reflection and exhaustion. "
            "Mood: dawn contemplation, the cost of victory. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_14",
        "title": "Page 5 PANEL 2｜大特寫｜名台詞圓滿收尾",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up of 大樹教練 face, slightly tilted upward, the faintest possible smile on his "
            "lips despite the exhaustion in his bloodshot eyes. His expression is bittersweet - the smile of "
            "someone who has won but at great cost. Behind him, the pale dawn light grows stronger. SFX "
            "visualization: subtle golden impact rings expanding from his lips as the iconic words manifest. "
            "Mood: the iconic closing line, life/youth/sleep sacrificed for the truth. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_15",
        "title": "Page 5 PANEL 3｜全身鏡頭｜軍師躬身致敬",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Full body shot. The military strategist stands in solemn deep bow at center frame, both hands "
            "holding a glowing golden scroll labeled as the touchstone archive (stylized golden cylindrical "
            "object with abstract inscription patterns, NOT readable text). The strategist's robe flows "
            "formally, his topknot perfectly aligned, the --debug-file probe rests at his side unlit. Behind "
            "him, the virtual system core glows with acceptance. The bow is at full ninety degrees, total "
            "respect. Mood: deepest gratitude, the lesson preserved, formal conclusion. 16:9 widescreen."
        ),
    },
    {
        "id": "lesson4_16",
        "title": "Page 5 PANEL 4｜全景｜晨光中的剪影 - 全劇終",
        "size": "1536x1024",
        "strategist_state": "solemn",
        "scene": (
            "Wide panoramic final scene. The sun has risen, casting brilliant golden morning light through "
            "window curtains onto the entire scene. In silhouette against the bright window, the 大樹教練 "
            "stands stretching his arms above his head, his formal suit now loosened at the collar in "
            "exhaustion. On the computer monitor in the foreground, a small silhouette of the strategist "
            "waves his feather fan in farewell. The room is filled with warm morning atmosphere. Mood: "
            "epilogue peace, dawn victory, the long battle over, gentle conclusion. 16:9 widescreen."
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
    boundary = "----Ep4" + datetime.now().strftime("%H%M%S%f")
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
    if state == "solemn":
        parts.append(ANCHOR_STRATEGIST_SOLEMN)
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
        log("=== Lesson 4 Episode 4 啟動 ===")
        send_text(
            "🦞 <b>Lesson 4 Episode 4 漫畫批次啟動</b>\n\n"
            "📋 <b>16 張 panels</b>（5 頁：3+3+3+3+4）\n"
            "🏷 <b>檔名規則</b>：<code>lesson4_01.png</code> ~ <code>lesson4_16.png</code>\n"
            "📐 <b>尺寸</b>：1536x1024（16:9 寬螢幕）\n"
            "👔 <b>大樹教練</b>：西裝+領帶+年輕+無白髮+reference 照片\n"
            "🛡 <b>軍師狀態</b>：肅然起敬、持 <code>--debug-file</code> 探針、唯一 solemn 狀態\n"
            "📡 <b>每張完成立即推 Telegram</b>\n"
            "⏰ <b>預計 12-16 分鐘全到齊</b>\n\n"
            "✅ lesson4_01（已存在的測試圖）會 catch-up 不重跑\n"
            "⏳ lesson4_02~16（15 張新圖）依序生成\n\n"
            "🛡 全程 try/except 包 main，silent death 不會再發生\n"
            "🎬 <b>第 4 話：殭屍指標與真相大白</b> — 全劇終"
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
            "🏁 <b>Lesson 4 Episode 4 全部完成</b>\n",
            f"✅ <b>{success_count}/{len(PANELS)}</b> 張成功\n",
            "📋 <b>Lesson 4 全部 panels</b>：",
        ]
        for r in results:
            if r["ok"]:
                note = "（從快取）" if r.get("from_cache") else f"（{r['dt']:.0f}s）"
                lines.append(f"  <code>{r['id']}</code> {r['title']} ✅ {note}")
            else:
                lines.append(f"  <code>{r['id']}</code> {r['title']} ❌")
        lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels_32mb_ep04/</code>")
        lines.append(f"\n🎬 <b>全四話完成</b>：")
        lines.append(f"  第 1 話：深夜遠控迷宮（18 張）")
        lines.append(f"  第 2 話：密碼學身分大辯論（14 張）")
        lines.append(f"  第 3 話：32MB 封包絕殺（14 張）")
        lines.append(f"  第 4 話：殭屍指標與真相大白（16 張，全劇終）")
        lines.append(f"\n🦞 合計 62 張 panels — 拼 PDF / HTML viewer 等您吩咐")
        send_text("\n".join(lines))
        log("=== Monitor 結束 ===")
    except Exception as e:
        # Catch-all: any unexpected exception is logged + Telegram alert
        tb = traceback.format_exc()
        log(f"❌❌❌ CRITICAL: main() threw exception:\n{tb}")
        try:
            send_text(
                f"🚨 <b>Episode 4 monitor CRASHED</b>\n\n"
                f"<code>{str(e)[:500]}</code>\n\n"
                f"請查 log: <code>claude-brain/data/comic_source_20260923/monitor_ep4_progress.log</code>"
            )
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
