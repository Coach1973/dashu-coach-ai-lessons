#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大樹標準功能模組：開工清單＋上架自動接線＋交付前檢查（2026-10-14 教練交辦）

教練原話：「之後任何新建類似底層邏輯的網站，是不是我都不用再提醒，它自動就會套用？…當我建立專案時，
你直接提供清單詢問：『請問大樹教練，這幾樣功能是否要套版加入？』預設全部勾選，如果我不需要再手動取消。」
「只要我們有任何上架的 SOP 作品，裡面有所謂的『送出資料』，是不是也能自動串接？」

模組目錄與每個模組的範本程式在 knowledges/模組庫_大樹標準功能.md（唯一真相源，改模組先改那份）。

用法：
  python3 scripts/module_kit.py menu "專案名稱"          # 開工清單（預設全勾），原樣貼給教練
  python3 scripts/module_kit.py check <slug>              # 交付前檢查某個作品：表單接線／GitHub／大樹作品集
  python3 scripts/module_kit.py audit                     # 掃全部策展站，列出「有表單卻沒接收件」的頁
  python3 scripts/module_kit.py wire <slug> [--dry-run]   # 幫某站的表單自動接上通用表單模組
上架流程（curation_process.py）兩條路都會自動呼叫 auto_wire_dir()，不用人記得。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
REPOS = Path.home() / "github_repos"
REGISTRY = WS / "event-signup" / "curated_sites_registry.json"
SCRIPT_TAG = '<script src="/static/works-form.js" defer></script>'

# ── 開工清單：key, 白話名稱, 一句話說明, 預設勾選 ─────────────────────────────
MODULES = [
    ("notify", "送出資料就通知您", "網頁上任何「送出／報名／留資料」，一送出就進「活動報名即時通知」群，您一定收得到", True),
    ("signup", "活動報名（場次＋同行人數）", "有場次的活動頁：報名寫進報名資料庫、通知群收到，問「報名幾人」一行指令就有含同行的總數", True),
    ("self_edit", "本人專屬修改連結", "每個人填完拿到自己的修改網址，之後自己補照片、改資料、刪除，不用登入（百人導師／BNI／南應大同一套）", True),
    ("admin", "教練後台＋一鍵複製專屬連結", "後台看得到每一筆、可隱藏／刪除／新增空座位，每人旁邊有「複製專屬連結」，可直接傳給本人", True),
    ("coach888", "收進大樹作品集", "公開網址放「最新作品」、後台網址放「活動後台」，您不用記任何網址", True),
    ("github", "背後接 GitHub", "聯想、宏碁、小龍蝦都能改，推上去自動換新", True),
    ("booking", "預約／取消時段", "對方自己挑時段預約、可取消，您收到通知（教練行程預約頁、榮樹下同一套）", True),
    ("seats", "空座位（名單先放好）", "已知名單先放好空位，本人點自己的名字認領補資料（誠信原則，不設密碼）", True),
    ("engage", "按讚／票選／留言牆", "訪客可以按讚、投票、留一句話，不用登入", True),
    ("share", "分享卡與短網址", "傳到 LINE／FB 有漂亮預覽圖；長網址自動做成短網址", True),
    ("burger", "手機漢堡選單", "手機上頂部出現「☰ 選單」，點開是大字段落清單＋主要按鈕，頂部選單改了自動跟著變", True),
]


def menu(name: str) -> str:
    lines = [f"請問大樹教練，「{name}」這幾樣功能是否要套版加入？（預設全部勾選，不需要的請說「拿掉第幾項」）", ""]
    for i, (_k, title, desc, on) in enumerate(MODULES, 1):
        lines.append(f"{'☑' if on else '☐'} {i}. {title}——{desc}")
    lines += ["", "沒說拿掉的，我就全部做上去；做完我會逐項實測，再跟您回報。"]
    return "\n".join(lines)


# ── 表單偵測與自動接線 ─────────────────────────────────────────────────────
KNOWN_ENDPOINT = re.compile(
    r"/api/[A-Za-z0-9_\-]+|sme-register-fn|formspree\.io|docs\.google\.com/forms|forms\.gle|script\.google\.com/macros"
    r"|data-works-form|works-form\.js")
FORM_RE = re.compile(r"(<form\b[^>]*>)(.*?)(</form>)", re.S | re.I)
FIELD_RE = re.compile(r"<(input|textarea|select)\b[^>]*>", re.I)
SKIP_TYPES = {"submit", "button", "hidden", "range", "checkbox", "radio", "file", "image", "reset", "search", "color"}


def _attr(tag: str, name: str):
    m = re.search(r"\b" + name + r"""\s*=\s*(["'])(.*?)\1""", tag, re.I | re.S)
    return m.group(2) if m else None


def _label_before(body: str, pos: int, tag: str) -> str:
    fid = _attr(tag, "id")
    if fid:
        m = re.search(r"<label\b[^>]*for=[\"']" + re.escape(fid) + r"[\"'][^>]*>(.*?)</label>", body, re.S | re.I)
        if m:
            return re.sub(r"<[^>]+>", "", m.group(1))
    labels = list(re.finditer(r"<label\b[^>]*>(.*?)</label>", body[max(0, pos - 400):pos], re.S | re.I))
    return re.sub(r"<[^>]+>", "", labels[-1].group(1)) if labels else ""


def _guess_name(kind: str, tag: str, label: str, taken: set) -> str:
    t = (_attr(tag, "type") or "").lower()
    hint = " ".join(filter(None, [label, _attr(tag, "placeholder"), _attr(tag, "id"), _attr(tag, "aria-label"),
                                  _attr(tag, "autocomplete"), _attr(tag, "inputmode"), t]))
    rules = [("email", r"e-?mail|信箱|電子郵件"), ("phone", r"tel|phone|電話|手機|聯絡方式|mobile"),
             ("name", r"姓名|名字|稱呼|\bname\b|您的大名")]
    if kind == "textarea" and "message" not in taken:
        return "message"
    for key, pat in rules:
        if key not in taken and re.search(pat, hint, re.I):
            return key
    if kind == "select" and "item" not in taken:
        return "item"
    i = 1
    while f"extra{i}" in taken:
        i += 1
    return f"extra{i}"


def form_status(html_text: str) -> list:
    """回傳每個表單的狀態：wired（已接收件）／unwired（有可填欄位卻沒接）／no_fields（只是計算機之類，不用接）。"""
    out = []
    for m in FORM_RE.finditer(html_text):
        open_tag, body = m.group(1), m.group(2)
        fields = [f for f in FIELD_RE.finditer(body)
                  if (_attr(f.group(0), "type") or "").lower() not in SKIP_TYPES]
        action = _attr(open_tag, "action") or ""
        if not fields:
            out.append("no_fields")
        elif KNOWN_ENDPOINT.search(open_tag) or (action and not action.startswith("#") and "mailto:" not in action):
            out.append("wired")
        else:
            out.append("unwired")
    return out


def page_wired(html_text: str) -> bool:
    """整頁有自己的送出程式（fetch 到 /api/…）就算已接，不動它。"""
    if "works-form: skip" in html_text:          # 刻意不接（例如匿名提問牆），頁內要寫原因
        return True
    return bool(re.search(r"fetch\(\s*[`'\"][^`'\"]*(/api/|sme-register-fn)", html_text)) or "works-form.js" in html_text \
        or bool(re.search(r"(API|ENDPOINT)\s*=\s*['\"]https?://event\.bymyway\.com/api/", html_text))


def auto_wire_html(html_text: str, slug: str):
    """把沒接收件的表單接上 /static/works-form.js。回傳 (新內容, 報告list)。已接好的頁原封不動。"""
    report = []
    if page_wired(html_text):
        return html_text, report

    def fix(m):
        open_tag, body, close = m.group(1), m.group(2), m.group(3)
        fields = [f for f in FIELD_RE.finditer(body) if (_attr(f.group(0), "type") or "").lower() not in SKIP_TYPES]
        if not fields or KNOWN_ENDPOINT.search(open_tag):
            return m.group(0)
        taken = {(_attr(f.group(0), "name") or "").lower() for f in fields} - {""}
        renames = {"contact": "phone", "tel": "phone", "mobile": "phone", "msg": "message", "content": "message",
                   "type": "item", "topic": "item", "fullname": "name", "username": "name", "mail": "email"}
        new_body, last = [], 0
        for f in fields:
            tag, kind = f.group(0), f.group(1).lower()
            cur = (_attr(tag, "name") or "").lower()
            new_tag = tag
            if cur and cur in renames and renames[cur] not in taken:
                new_tag = re.sub(r"""\bname\s*=\s*(["'])[^"']*\1""", f'name="{renames[cur]}"', tag, count=1)
                taken.discard(cur); taken.add(renames[cur])
            elif not cur:
                nm = _guess_name(kind, tag, _label_before(body, f.start(), tag), taken)
                taken.add(nm)
                new_tag = re.sub(r"^<(input|textarea|select)\b", lambda x: f'<{x.group(1)} name="{nm}"', tag, count=1, flags=re.I)
            new_body.append(body[last:f.start()]); new_body.append(new_tag); last = f.end()
        new_body.append(body[last:])
        body2 = "".join(new_body)
        # 「展示版／不會寄出」的字樣拿掉，避免訪客以為沒送出
        body2 = re.sub(r"<p[^>]*>[^<]*(展示版|不會寄出|尚未串接)[^<]*</p>", "", body2)
        tag2 = re.sub(r"""\sonsubmit\s*=\s*(["']).*?\1""", "", open_tag, flags=re.S | re.I)
        tag2 = tag2[:-1].rstrip() + f' data-works-form="{slug}">'
        missing = [k for k in ("name",) if k not in taken] + ([] if {"phone", "email"} & taken else ["phone或email"])
        report.append(("⚠️ 缺 " + "、".join(missing) + " 欄，訪客送不出去，請軍師補欄位") if missing
                      else "✅ 已接上（" + "、".join(sorted(k for k in taken if not k.startswith("extra"))) + "）")
        return tag2 + body2 + close

    new = FORM_RE.sub(fix, html_text)
    if report and SCRIPT_TAG not in new:
        new = re.sub(r"</body>", SCRIPT_TAG + "\n</body>", new, count=1, flags=re.I) if re.search(r"</body>", new, re.I) \
            else new + "\n" + SCRIPT_TAG + "\n"
    return new, report


def auto_wire_dir(site_dir: Path, slug: str, dry_run: bool = False) -> str:
    """上架流程用：整個網站資料夾的 html 都檢查一遍。回傳一行給通知用的說明（沒有表單就回空字串）。"""
    notes = []
    for p in sorted(Path(site_dir).rglob("*.html")):
        if any(part.startswith(".") for part in p.parts):
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        new, rep = auto_wire_html(txt, slug)
        if rep:
            if not dry_run and new != txt:
                p.write_text(new, encoding="utf-8")
            notes += [f"{p.relative_to(site_dir)}：{r}" for r in rep]
    if not notes:
        return ""
    return "\n📮 送出資料自動接線（進活動報名即時通知群）：\n" + "\n".join("   " + n for n in notes)


# ── 檢查 ──────────────────────────────────────────────────────────────────
def _registry():
    d = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return d.get("sites", d) if isinstance(d, dict) else d


def audit() -> list:
    rows = []
    for s in _registry():
        slug = s["slug"]
        d = REPOS / slug
        for p in sorted(d.glob("*.html")) if d.is_dir() else []:
            txt = p.read_text(encoding="utf-8", errors="ignore")
            st = form_status(txt)
            if "unwired" in st and not page_wired(txt):
                rows.append((slug, p.name, s.get("status", ""), s.get("title", "")[:30]))
    return rows


# 字最小 20px（教練 2026-10-14：「我們做的任何網頁，字體大小最少都要 20px」）
_FONT_DECL = re.compile(r"font(?:-size)?\s*:[^;}\"]*")
_SMALL_PX = re.compile(r"(?<![\d.])(1[0-9]|[0-9])(?:\.\d+)?px")


def small_fonts(html_text: str) -> list:
    """CSS 裡 font／font-size 寫了小於 20px 的地方（含 clamp 的最小值）。"""
    return sorted({m.group(0).strip()[:50] for m in _FONT_DECL.finditer(html_text) if _SMALL_PX.search(m.group(0))})


def check(slug: str) -> list:
    out = []
    d = REPOS / slug
    if not d.is_dir():
        return [f"❌ 找不到 {d}"]
    unwired = [p.name for p in d.glob("*.html")
               if "unwired" in form_status(p.read_text(encoding="utf-8", errors="ignore"))
               and not page_wired(p.read_text(encoding="utf-8", errors="ignore"))]
    out.append("❌ 表單沒接收件：" + "、".join(unwired) + f"（跑 module_kit.py wire {slug}）" if unwired else "✅ 送出資料：已接（或本站沒有表單）")
    small = {p.name: small_fonts(p.read_text(encoding="utf-8", errors="ignore")) for p in d.glob("*.html")}
    small = {k: v for k, v in small.items() if v}
    out.append("❌ 字小於 20px：" + "；".join(f"{k}（{len(v)} 處，例：{v[0]}）" for k, v in small.items())
               if small else "✅ 字體：全部 20px 以上")
    try:
        remote = subprocess.run(["git", "-C", str(d), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    except Exception:  # noqa: BLE001
        remote = ""
    out.append(f"✅ GitHub：{re.sub(r'https://[^@]*@', 'https://', remote)}" if remote else f"❌ 沒有 GitHub（跑 scripts/curated_git.py ensure {slug}）")
    try:
        r = subprocess.run([sys.executable, str(WS / "scripts" / "coach888_register_admin.py"), "--list"],
                           capture_output=True, text=True, timeout=30)
        listed = f"/curated/{slug}/" in r.stdout or f"/{slug}" in r.stdout
        out.append("✅ 大樹作品集：已收錄" if listed else "⚠️ 大樹作品集：--list 沒看到（公開網址收在「最新作品」時這裡看不到，請以 coach888 頁面為準）")
    except Exception as e:  # noqa: BLE001
        out.append(f"⚠️ 大樹作品集：查不到（{e}）")
    return out


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd = a[0]
    if cmd == "menu":
        print(menu(a[1] if len(a) > 1 else "這個專案")); return 0
    if cmd == "audit":
        rows = audit()
        print(f"有表單卻沒接收件的頁：{len(rows)} 個")
        for r in rows:
            print("  ❌ {:<26} {:<14} {:<6} {}".format(*r))
        return 1 if rows else 0
    if cmd == "check" and len(a) > 1:
        for line in check(a[1]):
            print(line)
        return 0
    if cmd == "wire" and len(a) > 1:
        note = auto_wire_dir(REPOS / a[1], a[1], dry_run="--dry-run" in a)
        print(note or "這個站沒有需要接線的表單")
        return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main())
