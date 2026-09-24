#!/usr/bin/env python3
"""策展SOP自動上架處理器（2026-09-06教練交辦）。

觸發方式：launchd WatchPaths 監控 event-signup/curation_uploads/incoming/
（事件觸發，不是輪詢——比照namecard-inbound同一種機制），資料夾內容一有變化
就跑這支腳本。腳本本身是「掃一遍incoming/，處理找到的每個檔案，處理完就搬走」
的冪等設計，重複觸發也不會重工，因為處理中的檔案一開始就被搬出incoming/。

完整流程：解壓縮 → 判斷ASCII slug(拼音轉換) → 建GitHub repo+push+開Pages →
登記進curated_sites_registry.json(讓event.bymyway.com/curated/<slug>/立刻可讀取，
不需要重啟Flask服務) → 插入tainan-shangquan店家名冊卡片 → 自動發一則大台南策展中心
FB貼文宣布 → Telegram通知教練（2026-09-06教練追加：全自動，不用等軍師人工發文）。

刻意不做的事（留給軍師下次確認時人工潤飾，見reference_curation_sop_2026-09-06.md）：
- 店家分類/描述的最終潤飾（這裡用關鍵字猜測，只是暫時的合理預設值，FB文案也是自動套模板）
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.error
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
EVENT_SIGNUP = WORKSPACE / "event-signup"
INCOMING_DIR = EVENT_SIGNUP / "curation_uploads" / "incoming"
PROCESSING_DIR = EVENT_SIGNUP / "curation_uploads" / "processing"
PROCESSED_DIR = EVENT_SIGNUP / "curation_uploads" / "processed"
FAILED_DIR = EVENT_SIGNUP / "curation_uploads" / "failed"
REGISTRY_PATH = EVENT_SIGNUP / "curated_sites_registry.json"
GITHUB_REPOS_DIR = Path("/Users/bymyway/github_repos")
TAINAN_SHANGQUAN_REPO = GITHUB_REPOS_DIR / "tainan-shangquan"
LOG_PATH = WORKSPACE / "distill" / "curation_process.log"
FB_PAGE_TOKENS_PATH = WORKSPACE / "fb_automation" / "page_tokens_2026-09-01.json"
FB_PAGE_NAME = "大台南策展中心"

COACH888_REPO = GITHUB_REPOS_DIR / "coach888"
COACH888_STATE_API = "https://event.bymyway.com/api/coach888/state"
COACH888_SECTION = "zuixinzuopin"  # 「最新作品」分類，2026-09-24教練新建，專放教練個人創作
# Cloudflare會擋Python預設UA(回403)；Origin比照coach888頁面本身
COACH888_HEADERS = {"User-Agent": "Mozilla/5.0 (curation-bot)", "Origin": "https://coach1973.github.io",
                    "Content-Type": "application/json"}

OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
TELEGRAM_NOTIFY_CHAT_ID = "-5349981085"  # 「活動報名即時通知」群組(教練+佩佩老師共見)，2026-09-06教練交辦：策展上傳完成也要跟活動報名一樣即時通知這裡，不只發教練個人對話

# 2026-09-12暫停：這個App(1050871501278089)還沒通過FB App Review，實測用完全登出的
# 瀏覽器驗證，用這組token發的貼文一般訪客完全看不到(只有App角色成員/管理員看得到)。
# 2026-09-06~09-10已累積21則這樣的隱形貼文。App Review通過前繼續呼叫這支只會不斷
# 產生更多看不見的貼文(白工)，先暫停自動發文，改由Telegram通知教練「有新店家上架」，
# 教練/軍師視需要手動用Meta Business Suite補發。詳見
# claude-brain/reference_fb_graph_api_app_review_required_for_public_visibility_2026-09-11.md
FB_AUTO_POST_PAUSED = True
_ENV = {**os.environ, "PATH": f"/opt/homebrew/bin:/Users/bymyway/.local/bin:{os.environ.get('PATH', '')}"}

CATEGORY_KEYWORDS = {
    "食": ["咖啡", "餐", "茶", "美食", "甜點", "廚房", "飲", "料理", "小吃", "烘焙"],
    "衣": ["服飾", "品牌", "生技", "彩妝", "穿搭", "織品", "時尚"],
    "住": ["民宿", "旅宿", "家居", "室內設計", "裝潢"],
    "行": ["交通", "旅遊", "運輸", "租車", "導覽"],
    "育": ["協會", "教育", "課程", "導師", "培訓", "學會", "團體", "講座", "工作坊"],
    "樂": ["運動", "藝術", "俱樂部", "扶輪社", "音樂", "健身", "球", "遊戲"],
}


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
    print(line, end="")


def notify(text: str) -> None:
    """2026-09-06補：回傳的message_id一併記進log——教練事後要求「網址改短
    之後把發錯的舊通知清掉」時，這台Mac完全查不到訊息ID(Bot API不能瀏覽
    群組歷史)，只能靠人工翻Telegram畫面找。往後有這行記錄，需要清舊訊息
    時可以直接呼叫deleteMessage，不用再靠人眼翻聊天記錄。"""
    try:
        with open(OPENCLAW_CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        bot_token = config["channels"]["telegram"]["accounts"]["bot_main"]["botToken"]
        body = json.dumps({"chat_id": TELEGRAM_NOTIFY_CHAT_ID, "text": text}).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data=body, method="POST", headers={"Content-Type": "application/json"},
        )
        resp = json.loads(urllib.request.urlopen(req, timeout=10).read())
        msg_id = resp.get("result", {}).get("message_id")
        log(f"📨 Telegram通知已送出，message_id={msg_id}")
    except Exception as e:  # noqa: BLE001
        log(f"⚠️ Telegram通知失敗: {e!r}")


def load_registry() -> dict:
    if not REGISTRY_PATH.is_file():
        return {"sites": []}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"sites": []}


def save_registry(data: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


_COMPANY_SUFFIXES = (
    "股份有限公司", "有限公司", "企業社", "工作室", "事務所", "商行",
    "有限合夥事業", "設計工程", "廣告設計",
)


def primary_title_segment(title: str) -> str:
    """<title>常是「品牌名｜行銷標語」的完整句子，只取分隔符號前的品牌名稱本身
    用來產生網址slug，避免像「牛市町｜只漲不跌的美味—品牌理念」整句轉拼音變成
    超長網址(教練2026-09-06實際踩到，已手動改名修正)。完整title仍保留給
    registry的title欄位(卡片顯示用)，不受影響。

    2026-09-06二次修復：教練當晚接連手動改短4個網址(百聖廣告設計工程有限公司/
    楊尚儒商聚樣dma/張騰文-騰文昌/幸福導師Esther楊在真)，發現這批標題大多是
    「沒有清楚分隔符號的完整公司全名」或用純「-」(無空格)當分隔，原本的
    分隔符號清單漏接。已補上：①純「-」也算分隔符號 ②結果仍含常見公司/工作室
    尾綴時，順手砍掉尾綴進一步縮短。仍會有猜不準的情況(教練需要的是「品牌核心
    2-4字」，不是規則能完全取代人判斷)，這種情況要靠下面新增的redirect機制
    收尾——不管日後被人工改短幾次，舊網址都會自動轉址不會死掉。"""
    segment = title
    for sep in ("｜", "|", "—", "－", "–", " - ", "-", "："):
        if sep in segment:
            segment = segment.split(sep, 1)[0].strip()
            break
    for suffix in _COMPANY_SUFFIXES:
        if segment.endswith(suffix):
            segment = segment[: -len(suffix)].strip()
            break
    return segment or title


def slugify_title(title: str) -> str:
    from pypinyin import lazy_pinyin
    raw = "-".join(lazy_pinyin(primary_title_segment(title)))
    slug = re.sub(r"[^a-z0-9-]", "", raw.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "site"


def _sidecar_slug_path(pkg_path: Path) -> Path:
    """教練2026-09-06拍板：自動猜的短網址常常猜不準，源頭解決方式是讓上傳的人
    (教練或夥伴)在送出檔案前就自己指定短網址，寫進上傳網頁的自訂欄位。
    這個欄位跟zip檔一起存成同名+.slug的旁路檔案，process_one()優先採用，
    完全不需要再靠pinyin猜測。"""
    return pkg_path.parent / f"{pkg_path.name}.slug"


def read_custom_slug(pkg_path: Path) -> str:
    sidecar = _sidecar_slug_path(pkg_path)
    if sidecar.is_file():
        val = sidecar.read_text(encoding="utf-8").strip()
        if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,60}", val):
            return val
    return ""


def read_kind(pkg_path: Path) -> str:
    """shop=店家策展、creation=大樹作品。2026-09-24起上傳頁強制選類型，沒有.kind就不猜。"""
    sidecar = pkg_path.parent / f"{pkg_path.name}.kind"
    return sidecar.read_text(encoding="utf-8").strip() if sidecar.is_file() else ""


def cleanup_sidecar_slug(pkg_path: Path) -> None:
    for sidecar in (_sidecar_slug_path(pkg_path), pkg_path.parent / f"{pkg_path.name}.kind"):
        if sidecar.is_file():
            sidecar.unlink()


def unique_slug(base: str, existing: set) -> str:
    slug = base
    n = 2
    while slug in existing or (GITHUB_REPOS_DIR / slug).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


def extract_package(pkg_path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    if pkg_path.suffix == ".zip":
        with zipfile.ZipFile(pkg_path) as z:
            z.extractall(dest)
    else:
        with tarfile.open(pkg_path) as t:
            t.extractall(dest)
    # 常見情況：zip裡包了一層跟zip同名的資料夾，把內容拉到dest頂層方便後續處理
    entries = [p for p in dest.iterdir() if not p.name.startswith(".")]
    if len(entries) == 1 and entries[0].is_dir():
        inner = entries[0]
        for item in inner.iterdir():
            shutil.move(str(item), str(dest / item.name))
        inner.rmdir()


def find_index_html(root: Path) -> Path | None:
    direct = root / "index.html"
    if direct.is_file():
        return direct
    matches = list(root.rglob("index.html"))
    return matches[0] if matches else None


def extract_meta(html_text: str) -> tuple[str, str]:
    title_m = re.search(r"<title>([^<]{1,120})</title>", html_text, re.IGNORECASE)
    title = title_m.group(1).strip() if title_m else ""
    desc_m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']{1,200})["\']',
        html_text, re.IGNORECASE,
    )
    desc = desc_m.group(1).strip() if desc_m else ""
    return title, desc


_TW_CITY = (
    "(?:台北|新北|桃園|台中|臺中|台南|臺南|高雄|基隆|新竹|苗栗|彰化|"
    "南投|雲林|嘉義|屏東|宜蘭|花蓮|台東|臺東|澎湖|金門|連江)"
)
ADDRESS_PATTERN = re.compile(
    _TW_CITY + r"[市縣][一-鿿0-9]{2,20}(?:路|街|大道|巷)"
    r"[一-鿿0-9]{0,10}號(?:[一-鿿0-9]{0,6}樓)?"
)


def extract_address(html_text: str) -> str:
    """2026-09-08教練交辦：策展SOP自動上架的店家卡片沒有地址就沒有地圖，
    教練每次都要自己開Google地圖手動找、複製連結貼上。改成從網站原始碼裡
    直接掃台灣地址格式(市/縣+路/街+號)，抓到就用同一套app.py既有的
    query-based地圖embed(不需要API Key，教練自助登錄流程已用同款做法穩定
    運作)，抓不到就照舊不顯示地圖(非致命，退回原本樣式)。"""
    m = ADDRESS_PATTERN.search(html_text)
    return m.group(0) if m else ""


def guess_category(text: str) -> str:
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in kws):
            return cat
    return "樂"


def get_github_token() -> str:
    result = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, timeout=15, env=_ENV,
    )
    for line in result.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1].strip()
    raise RuntimeError("無法從git credential fill取得GitHub token")


def create_github_repo(token: str, slug: str) -> None:
    payload = json.dumps({"name": slug, "private": False, "auto_init": False}).encode("utf-8")
    req = urllib.request.Request(
        "https://api.github.com/user/repos", data=payload, method="POST",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        urllib.request.urlopen(req, timeout=20)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        if e.code == 422 and "already exists" in body:
            return
        raise RuntimeError(f"建repo失敗 HTTP {e.code}: {body}") from e


def enable_github_pages(token: str, slug: str) -> None:
    payload = json.dumps({"source": {"branch": "main", "path": "/"}}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/Coach1973/{slug}/pages", data=payload, method="POST",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        urllib.request.urlopen(req, timeout=20)
    except urllib.error.HTTPError:
        pass  # 非致命：GitHub Pages有沒有開不影響event.bymyway.com/curated/<slug>/正常運作


def push_repo(repo_dir: Path, token: str, slug: str) -> None:
    subprocess.run(["git", "init", "-q"], cwd=repo_dir, check=True, env=_ENV)
    subprocess.run(
        ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com", "add", "-A"],
        cwd=repo_dir, check=True, env=_ENV,
    )
    subprocess.run(
        ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com",
         "commit", "-q", "-m", "策展SOP自動上架"],
        cwd=repo_dir, check=True, env=_ENV,
    )
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True, env=_ENV)
    remote_with_token = f"https://Coach1973:{token}@github.com/Coach1973/{slug}.git"
    subprocess.run(["git", "remote", "add", "origin", remote_with_token], cwd=repo_dir, check=True, env=_ENV)
    subprocess.run(["git", "push", "-u", "origin", "main", "-q"], cwd=repo_dir, check=True, env=_ENV)
    subprocess.run(
        ["git", "remote", "set-url", "origin", f"https://github.com/Coach1973/{slug}.git"],
        cwd=repo_dir, check=True, env=_ENV,
    )


def get_shop_vps_creds() -> tuple[str | None, str | None]:
    """讀event-signup/.env取得VPS SSH連線資訊，跟app.py的_provision_shop_placeholder()共用同一組憑證。"""
    env_path = EVENT_SIGNUP / ".env"
    host = password = None
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("SHOPS_VPS_HOST="):
                host = line.split("=", 1)[1].strip()
            elif line.startswith("SHOPS_VPS_SSH_PASSWORD="):
                password = line.split("=", 1)[1].strip()
    return host, password


def find_existing_shop_slug(brand_name: str) -> str | None:
    """檢查這家店是不是已經在shops.bymyway.com有暫代頁（自助登錄表單`_provision_shop_placeholder()`
    那條路產生的），有的話回傳既有slug。2026-09-06教練拍板：策展上傳網址對這種店家要改成
    覆蓋暫代頁內容而非另建一個新GitHub網站，避免同一家店出現兩個不同網址的重複站台。"""
    from pypinyin import lazy_pinyin
    registry_path = TAINAN_SHANGQUAN_REPO / "_shops_slugs.json"
    if not registry_path.is_file():
        return None
    try:
        used = set(json.loads(registry_path.read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001
        return None
    raw = "-".join(lazy_pinyin(brand_name))
    candidate = re.sub(r"-+", "-", re.sub(r"[^a-z0-9-]", "", raw.lower())).strip("-") or "shop"
    return candidate if candidate in used else None


def overwrite_shop_placeholder(site_dir: Path, slug: str) -> None:
    """把完整網站(index.html+assets等)整個覆蓋掉shops.bymyway.com/<slug>/既有暫代頁內容，
    網址保持不變。用tar打包後scp+遠端解壓（不用scp -r萬用字元，避免中文檔名或特殊字元出錯）。"""
    host, password = get_shop_vps_creds()
    if not host or not password:
        raise RuntimeError("找不到SHOPS_VPS_HOST/SHOPS_VPS_SSH_PASSWORD設定，無法覆蓋暫代頁")
    tar_path = f"/tmp/shop_overwrite_{slug}.tar.gz"
    subprocess.run(["tar", "-czf", tar_path, "-C", str(site_dir), "."], check=True, env=_ENV)
    remote_tmp = f"/tmp/shop_overwrite_{slug}.tar.gz"
    ssh_base = ["sshpass", "-p", password, "ssh", "-o", "StrictHostKeyChecking=no", f"root@{host}"]
    subprocess.run(ssh_base + [f"rm -rf /var/www/shops/{slug} && mkdir -p /var/www/shops/{slug}"],
                   check=True, timeout=30, capture_output=True, env=_ENV)
    subprocess.run(["sshpass", "-p", password, "scp", "-o", "StrictHostKeyChecking=no",
                    tar_path, f"root@{host}:{remote_tmp}"],
                   check=True, timeout=60, capture_output=True, env=_ENV)
    subprocess.run(ssh_base + [f"tar -xzf {remote_tmp} -C /var/www/shops/{slug}/ && rm {remote_tmp}"],
                   check=True, timeout=30, capture_output=True, env=_ENV)
    os.remove(tar_path)


def ensure_og_tags_absolute(repo_dir: Path, slug: str) -> None:
    """2026-09-18軍師交辦：策展SOP上架後自動確保og:標籤使用絕對路徑，
    否則FB preview card抓不到縮圖（og:image規範要求絕對URL）。
    - 既有og:image若為相對路徑→改寫成絕對URL
    - 缺og:title/og:description/og:image→用<title>/<meta name=description>/第一張<img>補
    - 確保og:description不跟og:title完全一樣（教練2026-09-18抱怨重複）
    """
    base_url = "https://event.bymyway.com/curated"
    index_file = find_index_html(repo_dir)
    if not index_file:
        return
    content = index_file.read_text(encoding="utf-8", errors="ignore")
    original = content

    # 1. 既有 og:image 相對路徑 → 絕對
    og_img_pat = re.compile(
        r'(<meta\s+property="og:image"\s+content=")([^"]+)(")',
        re.IGNORECASE,
    )
    m = og_img_pat.search(content)
    if m and not m.group(2).startswith(("http://", "https://")):
        rel = m.group(2).lstrip("./")
        new_url = f"{base_url}/{slug}/{rel}"
        content = og_img_pat.sub(lambda mm: f"{mm.group(1)}{new_url}{mm.group(3)}", content, count=1)

    # 2. 缺 og:title → 補一組完整 og: 標籤
    if 'property="og:title"' not in content:
        title, desc = extract_meta(content)

        def _normalize(s: str) -> str:
            return re.sub(r"[\s\-|\/・—_,，。;;:\"'《》「」()（）]+", "", s).lower()
        if title and desc and _normalize(title) == _normalize(desc):
            desc = f"{desc} 完整內容請看官網介紹"

        img_url = ""
        for pat in (
            r'<meta\s+property="og:image"\s+content="([^"]+)"',
            r'<img[^>]+src="([^"]+)"',
        ):
            im = re.search(pat, content, re.IGNORECASE)
            if im:
                src = im.group(1)
                if not src.startswith(("http://", "https://")):
                    src = f"{base_url}/{slug}/{src.lstrip('./')}"
                img_url = src
                break

        og_lines = [
            f'    <meta property="og:type" content="website">',
            f'    <meta property="og:title" content="{title}">',
        ]
        if desc:
            og_lines.append(f'    <meta property="og:description" content="{desc}">')
        if img_url:
            og_lines.append(f'    <meta property="og:image" content="{img_url}">')
        og_block = "\n".join(og_lines)

        new_content, n = re.subn(
            r"(<title>[^<]+</title>)",
            r"\1\n" + og_block,
            content,
            count=1,
        )
        if n:
            content = new_content
        else:
            content = re.sub(
                r"(<head[^>]*>)",
                r"\1\n" + og_block,
                content,
                count=1,
            )

    if content != original:
        index_file.write_text(content, encoding="utf-8")


def find_post_image(repo_dir: Path, html_text: str) -> Path | None:
    """挑一張代表圖：優先og:image，找不到就用頁面第一張<img>，都找不到回傳None
    （None時貼文改用純文字動態，不勉強硬塞圖）。"""
    for pattern in (
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<img[^>]+src=["\']([^"\']+)["\']',
    ):
        m = re.search(pattern, html_text, re.IGNORECASE)
        if m:
            candidate = (repo_dir / m.group(1).lstrip("/")).resolve()
            try:
                candidate.relative_to(repo_dir.resolve())
            except ValueError:
                continue
            if candidate.is_file():
                return candidate
    return None


def post_to_facebook(title: str, desc: str, event_url: str, image_path: Path | None) -> bool:
    """自動發一則大台南策展中心FB貼文宣布新店家上架（2026-09-06教練交辦：全自動不用等軍師人工發文）。
    文案套固定模板（emoji開頭+店名+簡介+連結+hashtag），非致命——失敗只記log，不擋整體上架流程。"""
    if FB_AUTO_POST_PAUSED:
        log(f"⏸️ FB自動貼文已暫停(App Review未通過，訪客看不到)，跳過「{title}」，請人工評估是否手動補發")
        return False
    try:
        tokens = json.loads(FB_PAGE_TOKENS_PATH.read_text(encoding="utf-8"))
        page = next((p for p in tokens.get("pages", []) if p.get("name") == FB_PAGE_NAME), None)
        if not page:
            log(f"⚠️ FB貼文跳過：找不到粉專「{FB_PAGE_NAME}」的token")
            return False
        page_id, access_token = page["id"], page["access_token"]

        caption = (
            f"🎯【大台南商圈上新網站】{title}正式上線！\n\n"
            + (f"{desc}\n\n" if desc else "")
            + f"看看這個新加入的好店家 👉 {event_url}\n\n"
            + "更多加入大台南商圈整合計劃的好店家，都在 👉 https://event.bymyway.com/tainan-shangquan/\n\n"
            + f"#大台南策展中心 #{re.sub(r'[^0-9A-Za-z一-鿿]', '', title)}"
        )

        if image_path:
            cmd = [
                "curl", "-s", f"https://graph.facebook.com/v20.0/{page_id}/photos",
                "-F", f"source=@{image_path}",
                "-F", f"caption={caption}",
                "-F", f"access_token={access_token}",
            ]
        else:
            cmd = [
                "curl", "-s", f"https://graph.facebook.com/v20.0/{page_id}/feed",
                "-F", f"message={caption}",
                "-F", f"link={event_url}",
                "-F", f"access_token={access_token}",
            ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        resp = json.loads(result.stdout or "{}")
        if "error" in resp:
            log(f"⚠️ FB貼文失敗：{resp['error']}")
            return False
        log(f"✅ FB貼文成功：{resp}")
        return True
    except Exception as e:  # noqa: BLE001
        log(f"⚠️ FB貼文例外：{e!r}")
        return False


def insert_tainan_shangquan_card(title: str, desc: str, category: str, event_url: str, address: str = "") -> None:
    index_path = TAINAN_SHANGQUAN_REPO / "index.html"
    content = index_path.read_text(encoding="utf-8")
    marker = "<!-- SHOP_CARDS_INSERT_POINT：新店家自動插入這行下面，勿刪除此標記 -->"
    if marker not in content:
        raise RuntimeError("SHOP_CARDS_INSERT_POINT標記不存在")
    import html as html_mod
    e = html_mod.escape

    address_row = f'<li><span class="k">地址</span><span>{e(address)}</span></li>' if address else ""

    # 2026-09-08：地址抓得到才加地圖欄位(shop-media)，跟app.py的
    # _shop_directory_card_html()同款query-based embed，不需要API Key。
    # 抓不到地址就退回單欄舊樣式，不強塞空地圖。
    if address:
        brand = primary_title_segment(title)
        map_q = quote(f"{address} {brand}")
        review_q = quote(f"{brand} 台南")
        media_block = f"""
            <div class="shop-media">
              <div class="map-frame">
                <iframe
                  src="https://www.google.com/maps?q={map_q}&amp;output=embed"
                  loading="lazy"
                  referrerpolicy="no-referrer-when-downgrade"
                  title="Google 地圖：{e(title)}（{e(address)}）"></iframe>
              </div>
            </div>"""
        review_link = f'<p class="slot-note"><a href="https://www.google.com/maps/search/?api=1&amp;query={review_q}" target="_blank" rel="noopener">在 Google 地圖上查看評論 →</a></p>'
    else:
        media_block = ""
        review_link = ""

    card = f"""
          <!-- 計劃夥伴店家：{e(title)}（策展SOP自動上架，待軍師補完整介紹） -->
          <article class="shop-row reveal">
            <div>
              <div class="shop-head">
                <span class="pill">計劃夥伴店家</span>
                <span class="tag">{e(category)}</span>
              </div>
              <h3>{e(title)}</h3>
              <p class="shop-desc">{e(desc) if desc else '網站已自動上架，介紹文案待軍師補充。'}</p>
              <ul class="shop-facts">
                <li><span class="k">分類</span><span>{e(category)}</span></li>
                {address_row}
              </ul>
              <p class="slot-note"><a href="{e(event_url)}" target="_blank" rel="noopener">查看店家專屬網站 →</a></p>
              {review_link}
            </div>{media_block}
          </article>
"""
    content = content.replace(marker, marker + "\n" + card, 1)
    index_path.write_text(content, encoding="utf-8")
    subprocess.run(["git", "add", "index.html"], cwd=TAINAN_SHANGQUAN_REPO, check=True, env=_ENV)
    subprocess.run(
        ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com",
         "commit", "-q", "-m", f"策展SOP自動上架：新店家「{title}」"],
        cwd=TAINAN_SHANGQUAN_REPO, check=True, env=_ENV,
    )
    subprocess.run(["git", "push", "-q"], cwd=TAINAN_SHANGQUAN_REPO, check=True, env=_ENV)


def insert_coach888_static_item(html_text: str, url: str, title: str) -> str:
    """把新項目插在「最新作品」grid開頭標籤正後方，並重編序號/項目數。

    錨點用 grid 開頭標籤本身，不用「第一個 item」——這個 repo 混用新舊兩種 item 模板，
    09-24赫米斯用「第一個item」定位，插進舊模板項目的<a>裡把結構切壞。"""
    if f'data-url="{url}"' in html_text:
        return html_text
    anchor = f'<div class="grid" data-section="{COACH888_SECTION}">'
    start = html_text.index(anchor)
    depth, end = 0, None
    for m in re.finditer(r"<div\b|</div>", html_text[start:]):
        depth += 1 if m.group() == "<div" else -1
        if depth == 0:
            end = start + m.end()
            break
    if end is None:
        raise RuntimeError("coach888 最新作品分類的<div>沒有正確結尾，不敢動")
    e = html.escape
    item = (f'<div class="item" data-url="{e(url)}"><span class="drag-handle">⠿</span><div class="num">0</div>'
            f'<a class="name" href="{e(url)}" target="_blank">{e(title)}</a>'
            f'<div class="url">{e(url.split("://", 1)[-1].rstrip("/"))}</div>'
            '<div class="badge public" contenteditable="true" spellcheck="false">公開</div>'
            '<span class="item-del" title="刪除這個項目">✕</span></div>')
    grid = anchor + item + html_text[start + len(anchor):end]
    counter = iter(range(1, 100000))
    grid = re.sub(r'<div class="num">\d+</div>', lambda _: f'<div class="num">{next(counter)}</div>', grid)
    for open_tag, close_tag in (("<div", "</div>"), ("<a ", "</a>")):
        if grid.count(open_tag) != grid.count(close_tag):
            raise RuntimeError(f"插入後 {open_tag}/{close_tag} 數量不平衡，已中止避免切壞coach888")
    out = html_text[:start] + grid + html_text[end:]
    n_items = grid.count('<div class="item"')
    return re.sub(
        rf'(<div class="section-title" data-section="{COACH888_SECTION}">[^\n]*?<span class="count">)\d+(項</span>)',
        rf"\g<1>{n_items}\g<2>", out, count=1,
    )


def register_coach888(url: str, title: str) -> str:
    """登記進coach888「最新作品」第一筆。伺服器同步狀態是教練實際看到的內容(必成功)，
    git靜態HTML只是沒JS時的備援(失敗不影響，回報註記即可)。"""
    def get_state() -> dict:
        req = urllib.request.Request(COACH888_STATE_API, headers=COACH888_HEADERS)
        return json.loads(urllib.request.urlopen(req, timeout=15).read())

    state = get_state()
    layout = json.loads(state.get("coach888_layout") or "{}")
    items = json.loads(state.get("coach888_items") or "{}")
    for urls in layout.values():
        if url in urls:
            urls.remove(url)
    layout.setdefault(COACH888_SECTION, []).insert(0, url)
    items[url] = {"name": title, "badge": "公開"}
    body = json.dumps({
        "coach888_layout": json.dumps(layout, ensure_ascii=False),
        "coach888_items": json.dumps(items, ensure_ascii=False),
    }).encode("utf-8")
    urllib.request.urlopen(
        urllib.request.Request(COACH888_STATE_API, data=body, method="POST", headers=COACH888_HEADERS), timeout=15,
    )
    if json.loads(get_state()["coach888_layout"]).get(COACH888_SECTION, [None])[0] != url:
        raise RuntimeError("coach888伺服器狀態寫入後核對不符")

    try:
        token = get_github_token()
        remote = f"https://Coach1973:{token}@github.com/Coach1973/coach888.git"
        git = ["git", "-c", "user.name=CoachWU", "-c", "user.email=bymyway7@gmail.com", "-C", str(COACH888_REPO)]
        subprocess.run(git + ["pull", "-q", "--rebase", remote, "master"], check=True, env=_ENV, timeout=60)
        index = COACH888_REPO / "index.html"
        index.write_text(insert_coach888_static_item(index.read_text(encoding="utf-8"), url, title), encoding="utf-8")
        subprocess.run(git + ["add", "index.html"], check=True, env=_ENV)
        subprocess.run(git + ["commit", "-q", "-m", f"feat: 大樹作品自動上架登記《{title}》"], check=True, env=_ENV)
        subprocess.run(git + ["push", "-q", remote, "HEAD:master"], check=True, env=_ENV, timeout=60)
        return ""
    except Exception as e:  # noqa: BLE001
        log(f"coach888靜態HTML備援更新失敗(伺服器狀態已登記，教練看得到): {e!r}")
        return "（靜態備援版更新失敗，不影響教練看到的內容）"


def publish_creation(pkg_path: Path, site_dir: Path, title: str, desc: str, registry: dict, existing_slugs: set) -> None:
    """大樹作品：原封不動上架event.bymyway.com，不建GitHub repo、不插商圈卡、不發FB，
    登記進coach888「最新作品」第一筆，通知「活動報名即時通知」群組。"""
    slug = unique_slug(read_custom_slug(pkg_path) or slugify_title(title), existing_slugs)
    shutil.copytree(site_dir, GITHUB_REPOS_DIR / slug)
    event_url = f"https://event.bymyway.com/curated/{slug}/"
    registry["sites"].append({
        "slug": slug,
        "title": title,
        "description": desc,
        "category": "教練個人創作",
        "event_url": event_url,
        "github_pages_url": "",
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "live",
        "source_package": pkg_path.name,
        "no_shop_card": True,
    })
    save_registry(registry)

    try:
        req = urllib.request.Request(event_url, headers={"User-Agent": "Mozilla/5.0 (curation-bot)"})
        live_note = "已確認打得開" if urllib.request.urlopen(req, timeout=15).status == 200 else "⚠️網址回應異常"
    except Exception as e:  # noqa: BLE001
        live_note = f"⚠️網址暫時打不開：{e}"
    try:
        c888_note = "已放進大樹作品一覽「最新作品」第一筆" + register_coach888(event_url, title)
    except Exception as e:  # noqa: BLE001
        log(f"coach888登記失敗: {e!r}")
        c888_note = f"⚠️大樹作品一覽登記失敗，請軍師補登：{e}"
    notify(
        "🎨【大樹作品・已自動上架】\n"
        f"標題：{title}\n"
        f"網址：{event_url}（{live_note}）\n"
        f"{c888_note}\n"
        "📌 教練個人創作，不進大台南商圈店家名冊"
    )
    log(f"✅ 大樹作品完成：{pkg_path.name} → {slug}")


def process_one(pkg_path: Path) -> None:
    log(f"開始處理：{pkg_path.name}")
    registry = load_registry()
    existing_slugs = {s["slug"] for s in registry["sites"]}
    tmp_extract = Path("/tmp") / f"curation_{pkg_path.stem}_{os.getpid()}"
    kind = read_kind(pkg_path)
    try:
        if kind not in ("shop", "creation"):
            raise RuntimeError("沒有標明是店家網站還是大樹作品，系統不猜，請到上傳頁重新上傳並選擇類型")
        extract_package(pkg_path, tmp_extract)
        index_file = find_index_html(tmp_extract)
        if not index_file:
            raise RuntimeError("解壓縮後找不到index.html，這個檔案可能不是一個完整的靜態網站")
        # 若index.html不在頂層，把它所在的資料夾內容拉到頂層
        if index_file.parent != tmp_extract:
            for item in index_file.parent.iterdir():
                shutil.move(str(item), str(tmp_extract / item.name))

        html_text = index_file.read_text(encoding="utf-8", errors="ignore") if index_file.exists() else (tmp_extract / "index.html").read_text(encoding="utf-8", errors="ignore")
        title, desc = extract_meta(html_text)
        if not title:
            title = re.sub(r"^\d{8}-\d{6}__", "", pkg_path.stem)

        if kind == "creation":
            publish_creation(pkg_path, tmp_extract, title, desc, registry, existing_slugs)
            shutil.rmtree(tmp_extract, ignore_errors=True)
            PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pkg_path), str(PROCESSED_DIR / pkg_path.name))
            cleanup_sidecar_slug(pkg_path)
            return

        category = guess_category(f"{title} {desc}")
        address = extract_address(html_text)

        # 2026-09-06教練拍板：先查這家店是不是已經在shops.bymyway.com有暫代頁
        # （自助登錄表單那條路產生的），有的話覆蓋暫代頁內容、網址不變，不建新GitHub網站。
        existing_shop_slug = find_existing_shop_slug(primary_title_segment(title))
        if existing_shop_slug:
            overwrite_shop_placeholder(tmp_extract, existing_shop_slug)
            event_url = f"https://shops.bymyway.com/{existing_shop_slug}/"

            fb_note = ""
            image_path = find_post_image(tmp_extract, html_text)
            if post_to_facebook(title, desc, event_url, image_path):
                fb_note = "\n✅ 已自動發布大台南策展中心FB貼文宣布"
            else:
                fb_note = "\n⚠️ FB自動貼文失敗，請軍師人工補發（不影響網站本身已更新）"

            notify(
                "🎯【策展SOP・既有店家頁面已更新為完整版】\n"
                f"店名：{title}\n"
                f"網址：{event_url}（沿用既有網址，非新建站台）"
                + fb_note
            )
            log(f"✅ 完成(覆蓋既有暫代頁)：{pkg_path.name} → {existing_shop_slug}")
            shutil.rmtree(tmp_extract, ignore_errors=True)
            PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
            shutil.move(str(pkg_path), str(PROCESSED_DIR / pkg_path.name))
            cleanup_sidecar_slug(pkg_path)
            return

        base_slug = read_custom_slug(pkg_path) or slugify_title(title)
        slug = unique_slug(base_slug, existing_slugs)
        repo_dir = GITHUB_REPOS_DIR / slug
        shutil.copytree(tmp_extract, repo_dir)
        ensure_og_tags_absolute(repo_dir, slug)

        token = get_github_token()
        create_github_repo(token, slug)
        push_repo(repo_dir, token, slug)
        enable_github_pages(token, slug)

        event_url = f"https://event.bymyway.com/curated/{slug}/"
        github_pages_url = f"https://coach1973.github.io/{slug}/"

        registry["sites"].append({
            "slug": slug,
            "title": title,
            "description": desc,
            "category": category,
            "event_url": event_url,
            "github_pages_url": github_pages_url,
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "status": "live",
            "source_package": pkg_path.name,
        })
        save_registry(registry)

        card_note = ""
        try:
            insert_tainan_shangquan_card(title, desc, category, event_url, address)
        except Exception as e:  # noqa: BLE001
            card_note = f"\n⚠️ 加入大台南策展中心店家名冊失敗（網站本身已上線，不影響）：{e}"
            log(f"插卡失敗: {e!r}")

        fb_note = ""
        image_path = find_post_image(repo_dir, html_text)
        if post_to_facebook(title, desc, event_url, image_path):
            fb_note = "\n✅ 已自動發布大台南策展中心FB貼文宣布"
        else:
            fb_note = "\n⚠️ FB自動貼文失敗，請軍師人工補發（不影響網站本身已上線）"

        map_note = f"\n📍 已自動偵測地址並加地圖：{address}" if address else "\n⚠️ 網站內容抓不到地址，店家名冊卡片暫無地圖（可請生成網站的AI工具把地址寫清楚後重新上傳）"
        notify(
            "🎯【策展SOP・新店家已自動上架】\n"
            f"店名：{title}\n"
            f"分類：{category}（自動猜測，可能需要軍師調整）\n"
            f"網址：{event_url}\n"
            f"GitHub Pages：{github_pages_url}"
            + map_note
            + card_note
            + fb_note
            + "\n📌 待軍師下次確認：潤飾店家介紹文案。"
        )
        log(f"✅ 完成：{pkg_path.name} → {slug}")
    except Exception as e:  # noqa: BLE001
        log(f"❌ 處理失敗：{pkg_path.name}: {e!r}")
        FAILED_DIR.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pkg_path), str(FAILED_DIR / pkg_path.name))
        cleanup_sidecar_slug(pkg_path)
        notify(
            "⚠️【策展SOP・自動上架失敗】\n"
            f"檔案：{pkg_path.name}\n錯誤：{e}\n"
            f"檔案已保留在 curation_uploads/failed/，請軍師人工檢查。"
        )
        shutil.rmtree(tmp_extract, ignore_errors=True)
        return
    shutil.rmtree(tmp_extract, ignore_errors=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(pkg_path), str(PROCESSED_DIR / pkg_path.name))
    cleanup_sidecar_slug(pkg_path)


def main() -> None:
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSING_DIR.mkdir(parents=True, exist_ok=True)
    pending = [
        p for p in INCOMING_DIR.iterdir()
        if p.is_file() and not p.name.startswith(".") and not p.name.endswith((".slug", ".kind"))
    ]
    if not pending:
        return
    for pkg in pending:
        # 立刻搬出incoming/，避免同一份檔案被重複觸發的WatchPaths事件重工
        staged = PROCESSING_DIR / pkg.name
        try:
            shutil.move(str(pkg), str(staged))
        except Exception as e:  # noqa: BLE001
            log(f"搬移到processing/失敗，跳過本輪: {pkg.name}: {e!r}")
            continue
        # 自訂短網址旁路檔案(上傳頁面填了才會有)跟著一起搬，process_one()才找得到
        for ext in (".slug", ".kind"):
            sidecar_src = INCOMING_DIR / f"{pkg.name}{ext}"
            if sidecar_src.is_file():
                shutil.move(str(sidecar_src), str(PROCESSING_DIR / sidecar_src.name))
        process_one(staged)


if __name__ == "__main__":
    main()
