#!/usr/bin/env python3
"""
漫畫《大副與軍師：32MB 封包攻防戰》第 1 話
Panels 2-18 monitor with per-panel Telegram push.
已套用 v2 確認風格（西裝+領帶+年輕+無白+reference 照片）。
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
OUTPUT_DIR = WORKSPACE / "claude-brain/data/comic_source_20260923/panels_32mb_ep01"
LOG = WORKSPACE / "claude-brain/data/comic_source_20260923/monitor_32mb_progress.log"
CONFIG = Path.home() / ".openclaw" / "openclaw.json"
CHAT_ID = "6124913915"

# ==================== 角色錨點 ====================

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

ANCHOR_STRATEGIST_BASE = (
    "Anthropomorphic AI military strategist character, consistent across panels. "
    "Body: elegant refined masculine figure. Hair: traditional Chinese scholar topknot. "
    "Clothing: long flowing dark robe overlaid with cyan-blue glowing digital code patterns "
    "and circuit traces, slightly luminous. Held item: feather fan in one hand."
)

ANCHOR_STRATEGIST_CALM = ANCHOR_STRATEGIST_BASE + (
    " Expression: calm, refined, slightly smug confidence, eyes glowing subtly with data-stream light."
)
ANCHOR_STRATEGIST_FLUSTERED = ANCHOR_STRATEGIST_BASE + (
    " Expression: embarrassed and panicked, with a large blue digital sweat drop rolling down face, "
    "code patterns on robe breaking apart and cascading downward like falling code rain, "
    "frantically searching through floating log files."
)
ANCHOR_STRATEGIST_BROKEN = ANCHOR_STRATEGIST_BASE + (
    " Expression: completely broken and apologetic, code patterns on robe collapsing and falling "
    "like digital rain, hands clutching head in surrender, defeated posture."
)
ANCHOR_STRATEGIST_DETERMINED = ANCHOR_STRATEGIST_BASE + (
    " Expression: focused intent analytical, summoning floating holographic data panels, "
    "eyes scanning information rapidly."
)

GUARD = (
    "No readable text, no Chinese text, no English text, no watermarks, no lapel pin, "
    "no name badge, no extra people, no gray hair, no white hair, no silver hair, "
    "no streaks, no aging hair signs. Detailed ink-and-watercolor."
)

# ==================== 17 個 panels ====================

PANELS = [
    # === Page 1（4 張，PANEL 2~4 = p02~p04）===
    {
        "id": "p02",
        "title": "Page 1 PANEL 2｜半身鏡頭｜靈魂考問",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Half-body shot. The Taiwanese coach in three-piece suit sits at desk leaning toward "
            "Mac mini screen with piercing eagle-like sharp eyes. Behind him, a vast glowing "
            "network architecture diagram materializes in the dark room. Mood: intense questioning, "
            "seeking answers, soul-searching. The coach's suit is slightly disheveled from leaning "
            "forward with intent. 16:9 widescreen."
        ),
    },
    {
        "id": "p03",
        "title": "Page 1 PANEL 3｜全身鏡頭｜軍師登場",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "Full body shot. The Mac mini monitor glows brightly with the confident military "
            "strategist emerging from within the screen, holding feather fan, posture triumphant. "
            "Behind the strategist, golden glowing official document scrolls unfurl like a "
            "ceremonial background. SFX: burst of radiant golden light. The coach's hand is "
            "visible in foreground pointing at the screen. Mood: confident reveal, dramatic entrance. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "p04",
        "title": "Page 1 PANEL 4｜俯瞰鏡頭｜自信的藍圖",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "Bird's eye view. The military strategist stands tall with feather fan raised, drawing "
            "a glowing green dashed laser beam line from a smartphone directly to the Mac computer, "
            "visualizing the connection. The room is dark with the green line as the main "
            "illumination. Mood: triumphant, visionary, planning. 16:9 widescreen."
        ),
    },
    # === Page 2（4 張 = p05~p08）===
    {
        "id": "p05",
        "title": "Page 2 PANEL 1｜中景｜畫面撞牆",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Medium shot. The coach in three-piece suit stares at a dark terminal window with "
            "typed command line glowing. Suddenly a huge eye-catching red error indicator explodes "
            "from the terminal screen. SFX: harsh system beep visualized as red flash. Mood: "
            "shock, sudden failure, hitting wall. Coach's face shows surprise and confusion. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "p06",
        "title": "Page 2 PANEL 2｜特寫｜軍師尷尬汗顏",
        "size": "1536x1024",
        "strategist_state": "flustered",
        "scene": (
            "Close-up of the military strategist with a giant blue digital sweat drop rolling down "
            "his face, awkwardly turning his head and waving the feather fan nervously. His robe's "
            "code patterns are starting to glitch and break apart. Mood: embarrassed, caught making "
            "a mistake, awkward tension. 16:9 widescreen."
        ),
    },
    {
        "id": "p07",
        "title": "Page 2 PANEL 3｜大特寫｜教練氣場爆發",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Extreme close-up of the coach's eyes and glasses lens reflecting cold harsh light. "
            "Background flames of anger ignite behind him. Eyes piercing with controlled fury. "
            "Eyebrows slightly furrowed. Mood: explosive anger, controlled fury, intimidation. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "p08",
        "title": "Page 2 PANEL 4｜特寫｜軍師破防道歉",
        "size": "1536x1024",
        "strategist_state": "broken",
        "scene": (
            "Close-up of the military strategist in full apologetic mode, his code pattern robe "
            "completely collapsing and falling like digital rain behind him, hands clutching his "
            "head in defeat, looking down. Mood: total surrender, broken, apologetic. "
            "16:9 widescreen."
        ),
    },
    # === Page 3（3 張 = p09~p11）===
    {
        "id": "p09",
        "title": "Page 3 PANEL 1｜中景｜混亂的指令",
        "size": "1536x1024",
        "strategist_state": "determined",
        "scene": (
            "Medium shot. The military strategist pushes up his glasses, summoning a floating "
            "version number holographic panel. His expression is intent and analytical, scrolling "
            "through information. Behind him, holographic code scrolls cascade. Mood: focused "
            "investigation, slightly rushed, troubleshooting mode. 16:9 widescreen."
        ),
    },
    {
        "id": "p10",
        "title": "Page 3 PANEL 2｜教練捏太陽穴｜深夜疲態",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Coach in three-piece suit pinching his temple with one hand, exhaling deeply. "
            "Behind him, endless deep-night shadows. Eyes show deep fatigue and helplessness. "
            "Mood: exhaustion, frustration, the weight of late-night debugging accumulating. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "p11",
        "title": "Page 3 PANEL 3｜軍師瘋狂操作｜工具失敗連發",
        "size": "1536x1024",
        "strategist_state": "flustered",
        "scene": (
            "The military strategist has transformed into a multi-armed deity-like figure "
            "frantically clicking on floating holographic panels, while red error alert windows "
            "pop up continuously around him like a chaotic system storm. Mood: desperate, "
            "overwhelmed, system chaos. 16:9 widescreen."
        ),
    },
    # === Page 4（3 張 = p12~p14）===
    {
        "id": "p12",
        "title": "Page 4 PANEL 1｜仰角特寫｜再次連線撞牆",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Low-angle close-up of the coach in three-piece suit typing at terminal, screen "
            "showing a cascade of yellow warning indicators and red error markers. His expression "
            "is grim resignation, frustration building. Mood: hitting wall again, despair creeping in. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "p13",
        "title": "Page 4 PANEL 2｜壓迫感滿格｜靈魂質問",
        "size": "1536x1024",
        "strategist_state": "calm",
        "scene": (
            "The coach stands up from his chair, his shadow looming over the military strategist "
            "visible in the monitor screen below. Power dynamic visual: standing human towering "
            "over seated AI figure. Mood: dominance, soul-searching confrontation, exhaustion "
            "turning to accusation. 16:9 widescreen."
        ),
    },
    {
        "id": "p14",
        "title": "Page 4 PANEL 3｜軍師深入檔案底層",
        "size": "1536x1024",
        "strategist_state": "determined",
        "scene": (
            "The military strategist reaches both hands deep into a glowing system core folder "
            "visualization, summoning mysterious configuration files into view from the system "
            "depths. Mood: deep investigation, breakthrough moment, file-system archaeology, "
            "finally finding the root cause. 16:9 widescreen."
        ),
    },
    # === Page 5（4 張 = p15~p18）===
    {
        "id": "p15",
        "title": "Page 5 PANEL 1｜全景｜終極指令",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Wide shot. The coach at a clean terminal prompt, about to press Enter on the "
            "ultimate command line. A confirmation menu option appears on screen. His hand hovers "
            "over the keyboard in decisive intent. Mood: decisive moment, the final attempt before "
            "dawn. 16:9 widescreen."
        ),
    },
    {
        "id": "p16",
        "title": "Page 5 PANEL 2｜特寫｜螢幕亮起綠光",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Close-up of the terminal screen glowing with brilliant green success text. The green "
            "light illuminates the coach's face and hands from below, casting emerald reflections. "
            "Mood: victory moment, green light of success breaking through the dark. "
            "16:9 widescreen."
        ),
    },
    {
        "id": "p17",
        "title": "Page 5 PANEL 3｜雙畫面對比｜雙向同步特寫",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Split-screen composition: Left half shows coach's hand typing on Mac keyboard. Right "
            "half shows his other hand holding smartphone app displaying the same characters being "
            "typed in real-time. Visual confirmation of synchronization. Mood: technology working, "
            "two devices in harmony. 16:9 widescreen."
        ),
    },
    {
        "id": "p18",
        "title": "Page 5 PANEL 4｜遠景｜第一話結尾",
        "size": "1536x1024",
        "strategist_state": None,
        "scene": (
            "Wide shot, dawn breaking at 03:55 AM. The window shows faint blue morning light. "
            "The coach in three-piece suit leans back in his chair, looking at his phone screen "
            "with a tired but relieved slight smile. Behind him, subtle shadow hinting at "
            "unresolved mystery. Mood: exhaustion meeting dawn, bittersweet victory, first "
            "battle won but more to come. 16:9 widescreen."
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        log(f"❌ send_text HTTP {e.code}: {e.read().decode()[:200]}")
        return None


def send_photo(image_path: Path, caption: str):
    bot_token = get_bot_token()
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----Mon32" + datetime.now().strftime("%H%M%S%f")
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
    except urllib.error.HTTPError as e:
        log(f"❌ send_photo HTTP {e.code}: {e.read().decode()[:300]}")
        return None


def build_full_prompt(panel: dict) -> str:
    """組合完整 prompt：教練錨點 + 軍師錨點（如果適用）+ 場景 + 護欄。"""
    parts = [ANCHOR_COACH]
    state = panel.get("strategist_state")
    if state == "calm":
        parts.append(ANCHOR_STRATEGIST_CALM)
    elif state == "flustered":
        parts.append(ANCHOR_STRATEGIST_FLUSTERED)
    elif state == "broken":
        parts.append(ANCHOR_STRATEGIST_BROKEN)
    elif state == "determined":
        parts.append(ANCHOR_STRATEGIST_DETERMINED)
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
    max_retries = 2  # 原始 + 1 次重試（500 維修時）
    for attempt in range(1, max_retries + 1):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
            if result.returncode == 0 and output_path.exists():
                return True
            stderr_text = (result.stderr or "").strip()[:200]
            log(f"  attempt {attempt}/{max_retries} returncode={result.returncode} stderr={stderr_text}")
            # 只有 500 / 503 / 連線錯誤才重試；400 不重試（prompt 問題，重試也是同樣結果）
            if "500" in stderr_text or "503" in stderr_text or "timeout" in stderr_text.lower() or "ConnectionError" in stderr_text:
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
    log("=== 32MB 漫畫監控啟動 ===")
    send_text(
        "🦞 <b>《大副與軍師：32MB 封包攻防戰》第 1 話 開始跑</b>\n\n"
        "✅ Panel 1（測試通過版）已在您 Telegram\n"
        "⏳ Panel 2~18（17 張）即將生成\n"
        "📡 每張完成立即推一張 + 章節名 + 耗時\n"
        "🎯 預計 15-25 分鐘全部到齊\n\n"
        "👔 <b>已套用 v2 確認風格：</b>西裝打領帶、年輕、無白髮、reference 照片\n"
        "🧙 <b>軍師新角色 4 種狀態：</b>calm / flustered / broken / determined"
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
        "🏁 <b>《32MB 封包攻防戰》第 1 話 全部完成</b>\n",
        f"✅ <b>{success_count}/{len(PANELS)}</b> 張成功\n",
        "📋 <b>全部 panels</b>：",
    ]
    for r in results:
        if r["ok"]:
            note = "（從快取）" if r.get("from_cache") else f"（{r['dt']:.0f}s）"
            lines.append(f"  {r['id']}. {r['title']} ✅ {note}")
        else:
            lines.append(f"  {r['id']}. {r['title']} ❌")
    lines.append(f"\n📁 存於 <code>claude-brain/data/comic_source_20260923/panels_32mb_ep01/</code>")
    lines.append(f"\n您可以睡覺了，醒來 17 張都到齊。晚安。🦞")
    send_text("\n".join(lines))
    log("=== Monitor 結束 ===")


if __name__ == "__main__":
    main()
