"""大樹小講場次：資料庫 → bigtree 官網 → Netlify 一鍵發佈。

教練 2026-08-23 交辦：場次改期／新增以前都要透過 AI 改網頁原始碼，兩份資料
（網頁裡的 SESSION_DATES 與 event.db）各自維護，一定會漏——2026-08-22 改期
就是漏在這裡。改成資料庫當唯一真相源，後台改完按一鍵發佈，網站與簽到系統同時吃到。

流程：read_sessions() → render_session_dates() → write_index() → git 推送 → Netlify 部署
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from datetime import date, datetime
from pathlib import Path

import db

BIGTREE_REPO = Path("/Users/bymyway/github_repos/bigtree")
INDEX_HTML = BIGTREE_REPO / "index.html"
NETLIFY_SITE_ID = "40e580f0-1def-4777-adb8-587ef023ed36"
QUOTA_FILE = Path("/Users/bymyway/.openclaw/workspace/state/netlify_deploy_quota.json")
CREDENTIALS = Path("/Users/bymyway/.openclaw/workspace/credentials/netlify_token.txt")

WEEKDAY_TW = ["一", "二", "三", "四", "五", "六", "日"]

# 2026-08-31教練當場點名：後台選單只列時段名稱、沒標時間，教練根本無從選起。
# 這份時間定義要跟 bigtree/index.html 的 const SLOTS 保持一致（前端渲染實際顯示的時間
# 讀的是那份，這裡只是給後台選單顯示參考用）——改了任何一邊，記得另一邊也要同步改。
SLOT_TIMES = {
    "早": "09:00–12:00", "早半": "10:00–12:30", "午": "14:00–17:00", "午半": "14:00–16:30",
    "晚": "18:00–21:00", "晚半": "18:00–20:30", "夜": "19:30–21:30", "線上": "10:00–12:00",
    "上午": "10:00–12:00", "下午": "13:30–16:30", "AM": "09:00–12:00", "PM": "13:00–16:00",
    "全日": "09:00–17:00", "午後": "15:00–17:30", "TBD": "時間未定",
}
SLOT_CHOICES = list(SLOT_TIMES.keys())


def make_label(event_date: str) -> str:
    """2026-08-21 → 8/21（五）"""
    d = datetime.strptime(event_date, "%Y-%m-%d").date()
    return f"{d.month}/{d.day}（{WEEKDAY_TW[d.weekday()]}）"


def read_sessions(conn, include_past: bool = False, only_active: bool = True):
    """讀出要發佈到官網的場次。預設只取進行中、且尚未過期的場次。"""
    sql = "SELECT * FROM events WHERE site = 'bigtree'"
    params: list = []
    if only_active:
        sql += " AND (status IS NULL OR status = 'active')"
    if not include_past:
        sql += " AND event_date >= ?"
        params.append(date.today().isoformat())
    sql += " ORDER BY event_date, COALESCE(start_time, '')"
    return conn.execute(sql, params).fetchall()


def render_session_dates(rows) -> str:
    """產生 index.html 裡那段 const SESSION_DATES = [...]; 的完整文字。"""
    lines = ["const SESSION_DATES = ["]
    for r in rows:
        parts = [
            f"date:'{r['event_date']}'",
            f"label:'{make_label(r['event_date'])}'",
            f"slots:['{r['slot_key'] or 'TBD'}']",
            f"topic:'{r['name']}'",
        ]
        for key in ("location", "venue", "address", "transport"):
            if r[key]:
                parts.append(f"{key}:'{r[key]}'")
        parts.append(f"slug:'{r['slug']}'")
        if r["event_url"]:
            parts.append(f"eventUrl:'{r['event_url']}'")
        lines.append("  {" + ", ".join(parts) + "},")
    lines.append("];")
    return "\n".join(lines)


class PublishError(Exception):
    """真的不能繼續的狀況（例如網頁結構被改壞），必須中止而不是照舊部署。"""


def write_index(conn) -> tuple[bool, str]:
    """把資料庫場次寫回 index.html。

    回傳 (檔案是否被改動, 訊息)。「沒被改動」代表檔案本來就是最新，屬正常情形；
    真正不能繼續的狀況一律丟 PublishError，避免把舊內容或壞掉的頁面推上線。
    """
    rows = read_sessions(conn)
    if not rows:
        raise PublishError("資料庫裡沒有任何『進行中且未過期』的場次，為避免把官網場次區清空，已中止。")
    html = INDEX_HTML.read_text(encoding="utf-8")
    block = render_session_dates(rows)
    new_html, n = re.subn(r"const SESSION_DATES = \[[\s\S]*?\n\];", block, html, count=1)
    if n != 1:
        raise PublishError("在 index.html 找不到場次資料區塊（網頁結構可能被改過），已中止，請找軍師看一下。")
    if new_html == html:
        return False, "本機網頁已是最新內容。"
    INDEX_HTML.write_text(new_html, encoding="utf-8")
    return True, f"已更新官網場次區（{len(rows)} 場）。"


PUBLISHED_KEY = "bigtree_published_hash"


def _content_hash(rows) -> str:
    return hashlib.sha256(render_session_dates(rows).encode("utf-8")).hexdigest()


def _get_published_hash(conn) -> str:
    row = conn.execute("SELECT value FROM app_settings WHERE key = ?", (PUBLISHED_KEY,)).fetchone()
    return row["value"] if row else ""


def _set_published_hash(conn, value: str) -> None:
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (PUBLISHED_KEY, value),
    )
    conn.commit()


def fetch_live_sessions(timeout: int = 6) -> dict | None:
    """抓目前官網上真正在跑的場次。抓不到（沒網路等）回 None，不讓後台開不起來。"""
    import urllib.request
    try:
        html = urllib.request.urlopen("https://bigtree-tw.netlify.app/", timeout=timeout).read().decode("utf-8")
    except Exception:
        return None
    m = re.search(r"const SESSION_DATES = \[([\s\S]*?)\n\];", html)
    if not m:
        return None
    live = {}
    for date_, slot, topic, rest in re.findall(
            r"\{date:'([^']*)'.*?slots:\['([^']*)'\].*?topic:'([^']*)'(.*?)\}", m.group(1)):
        slug_m = re.search(r"slug:'([^']*)'", rest)
        venue_m = re.search(r"venue:'([^']*)'", rest)
        live[(date_, slot)] = {"topic": topic,
                               "slug": slug_m.group(1) if slug_m else None,
                               "venue": venue_m.group(1) if venue_m else None}
    return live


def diff_summary(conn) -> dict:
    """發佈前給教練看的摘要：按下去到底會發生什麼事。

    「還沒發佈」要比對的是『線上官網』而不是本機檔案——本機檔案先被改好、
    但還沒部署上去的情況是存在的（例如 AI 先改好檔案），若拿本機檔案比，
    會誤判成「已經一致」，教練按了發佈也不會有動作，官網就一直停在舊版。

    另外，教練要看的是「這次會變動什麼」，不是「總共幾場」——只報總數會被
    理解成「要改這麼多場」（2026-08-23 教練當場點出這個誤解），所以這裡直接
    跟線上內容逐場比對，算出「下架／新增／內容有改／只是順序調整」。
    """
    rows = read_sessions(conn)
    result = {
        "sessions": [
            {"date": r["event_date"], "label": make_label(r["event_date"]),
             "slot": r["slot_key"], "topic": r["name"], "venue": r["venue"], "slug": r["slug"]}
            for r in rows
        ],
        "has_changes": _content_hash(rows) != _get_published_hash(conn),
        "removed": [], "added": [], "modified": [], "live_ok": False, "reordered": False,
    }

    live = fetch_live_sessions()
    if live is None:
        return result
    result["live_ok"] = True

    # 2026-08-31教練指出：一堆場次莫名其妙顯示「已下架」，查證後發現真根因——
    # 原本用(日期,時段)當比對鍵，只要動了「時段」欄位（例如把TBD改成AM/PM這種
    # 正常編輯），舊鍵就對不上新鍵，被誤判成「這場下架了+多了一場新的」，
    # 且不管真正原因是什麼，畫面一律寫死「活動已過，自動下架」，教練完全看不懂。
    # 改用slug當比對鍵——slug是活動的穩定識別碼，同一個slug永遠代表同一場活動，
    # 就算時段/場地/主題怎麼改，都該算「修改」而不是「下架一場、新增一場」的假動作。
    live_by_slug = {v["slug"]: {**v, "date": d, "slot": s}
                     for (d, s), v in live.items() if v.get("slug")}
    new_by_slug = {r["slug"]: r for r in rows}

    today_str = date.today().isoformat()
    for slug in live_by_slug.keys() - new_by_slug.keys():
        l = live_by_slug[slug]
        is_expired = l["date"] < today_str
        result["removed"].append({
            "label": make_label(l["date"]), "slot": l["slot"], "topic": l["topic"],
            "reason": "活動已過，自動下架" if is_expired else "狀態改為取消／草稿，暫不對外顯示",
        })
    for slug in new_by_slug.keys() - live_by_slug.keys():
        r = new_by_slug[slug]
        result["added"].append({"label": make_label(r["event_date"]), "slot": r["slot_key"],
                                "topic": r["name"]})
    for slug in live_by_slug.keys() & new_by_slug.keys():
        l, r = live_by_slug[slug], new_by_slug[slug]
        diffs = []
        if r["name"] != l["topic"]:
            diffs.append(f"主題：{l['topic']} → {r['name']}")
        if (r["venue"] or None) != (l.get("venue") or None):
            diffs.append(f"場地：{l.get('venue') or '未填'} → {r['venue'] or '未填'}")
        if (r["event_date"], r["slot_key"] or "TBD") != (l["date"], l["slot"] or "TBD"):
            diffs.append(f"時間：{make_label(l['date'])}｜{l['slot'] or '未定'} → "
                         f"{make_label(r['event_date'])}｜{r['slot_key'] or '未定'}")
        if diffs:
            result["modified"].append({"label": make_label(r["event_date"]), "slot": r["slot_key"], "diffs": diffs})

    # 內容都沒動，但排序不同 → 這次發佈的作用只是把順序排正確
    live_order = list(live_by_slug.keys())
    new_order = [slug for slug, _ in sorted(
        new_by_slug.items(), key=lambda kv: (kv[1]["event_date"], kv[1]["start_time"] or ""))]
    common = [s for s in live_order if s in new_by_slug]
    expected = [s for s in new_order if s in live_by_slug]
    result["reordered"] = common != expected
    return result


def _netlify_token() -> str | None:
    if CREDENTIALS.exists():
        return CREDENTIALS.read_text(encoding="utf-8").strip()
    return os.environ.get("NETLIFY_TOKEN")


def _bump_quota(deploy_id: str, note: str) -> int | None:
    """部署成功後扣一次額度並留紀錄，回傳剩餘次數。"""
    try:
        data = json.loads(QUOTA_FILE.read_text(encoding="utf-8"))
        data["quota_remaining"] -= 1
        data.setdefault("history", []).insert(0, {
            "date": date.today().isoformat(), "site": "bigtree-tw",
            "deploy_id": deploy_id, "change": note,
            "remaining_after": data["quota_remaining"],
        })
        QUOTA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return data["quota_remaining"]
    except Exception:
        return None


def quota_remaining() -> int | None:
    try:
        return json.loads(QUOTA_FILE.read_text(encoding="utf-8"))["quota_remaining"]
    except Exception:
        return None


def publish(conn, message: str = "") -> dict:
    """一鍵發佈：寫檔 → git commit/push → 打包 → 部署 Netlify。"""
    rows = read_sessions(conn)
    if not rows:
        return {"ok": False, "step": "產生網頁",
                "message": "資料庫裡沒有任何『進行中且未過期』的場次，為避免把官網場次區清空，已中止。"}
    target_hash = _content_hash(rows)
    if target_hash == _get_published_hash(conn):
        return {"ok": False, "step": "產生網頁", "message": "官網已經是最新內容，沒有需要發佈的變更。"}

    try:
        # changed=False 代表本機檔案早就是最新（例如先前已改好但沒部署成功），
        # 此時仍要繼續往下部署，不能當作「沒事做」而中止。
        write_index(conn)
    except PublishError as e:
        return {"ok": False, "step": "產生網頁", "message": str(e)}

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = message.strip() or f"大樹小講場次更新（後台一鍵發佈 {stamp}）"
    try:
        subprocess.run(["git", "add", "index.html"], cwd=BIGTREE_REPO, check=True,
                       capture_output=True, timeout=30)
        # 只有真的有異動才 commit；沒異動時 git commit 會回非 0，那不是錯誤
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=BIGTREE_REPO,
                                capture_output=True, timeout=30).returncode != 0
        if staged:
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=BIGTREE_REPO, check=True,
                           capture_output=True, timeout=30)
        subprocess.run(["git", "push", "origin", "main"], cwd=BIGTREE_REPO, check=True,
                       capture_output=True, timeout=120)
    except subprocess.CalledProcessError as e:
        detail = (e.stderr or b"").decode("utf-8", "ignore")[:300]
        return {"ok": False, "step": "存進 GitHub", "message": f"網頁已改好但推送失敗：{detail}"}

    token = _netlify_token()
    if not token:
        return {"ok": False, "step": "部署 Netlify",
                "message": "找不到 Netlify 金鑰，網頁已存進 GitHub，但沒有部署上線。"}

    # 打包方式：git archive HEAD 解到暫存目錄 → 用系統 zip 指令打包。
    # 這是 2026-08-22 實測部署成功的組合，一字都不要改，理由如下：
    #   * 用 git archive HEAD 而非工作區現況 → 不會夾帶其他還沒確認的修改上線
    #   * 不可用 `git archive --format=zip` 直接產 zip（2026-08-13、08-23 兩次
    #     都因此部署失敗，Netlify 回 "Deploy failed while extracting zip"）
    #   * 也不要改用 Python zipfile 自己走訪檔案：那樣產生的壓縮檔「沒有目錄項」
    #     （只有檔案、沒有 archive/ 這種資料夾條目），Netlify 同樣解壓失敗。
    #     2026-08-23 實測比對過成功／失敗兩包，唯一實質差異就是這 9 個目錄項。
    #     系統 zip 指令會自動寫入目錄項，中文檔名雖然沒設 UTF-8 旗標，但位元組
    #     本身就是 UTF-8，Netlify 解得正確（線上中文路徑實測 200）。
    zip_path = Path("/tmp/bigtree_publish.zip")
    if zip_path.exists():
        zip_path.unlink()
    with tempfile.TemporaryDirectory() as tmpdir:
        tar = subprocess.Popen(["git", "archive", "HEAD"], cwd=BIGTREE_REPO, stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", tmpdir], stdin=tar.stdout, check=True, timeout=180)
        tar.wait()
        subprocess.run(["zip", "-qr", str(zip_path), ".", "-x", ".git*"],
                       cwd=tmpdir, check=True, timeout=300)

    import urllib.request
    req = urllib.request.Request(
        f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys",
        data=zip_path.read_bytes(), method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/zip"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read())
    except Exception as e:
        return {"ok": False, "step": "部署 Netlify",
                "message": f"網頁已存進 GitHub，但上線失敗：{e}"}

    deploy_id = result.get("id", "")
    # Netlify 回 200 只代表「檔案收到了」，不代表已經上線——
    # 壓縮檔如果解不開，狀態會一直停在 uploaded 永遠不會 ready。
    # 2026-08-23 就是把 200 當成功，畫面報「已發佈」但官網其實還是舊版。
    # 一定要等到真的 ready 才算數。
    state = _wait_until_live(deploy_id, token)
    remaining = _bump_quota(deploy_id, commit_msg)  # 失敗的部署 Netlify 一樣計費，照扣
    if state != "ready":
        return {"ok": False, "step": "部署 Netlify", "remaining": remaining,
                "message": f"檔案已上傳但官網沒有更新成功（狀態：{state}）。"
                           f"這次額度仍會被計算，請找軍師查原因，不要重複按。"}

    _set_published_hash(conn, target_hash)  # 只有真的上線才記錄，否則下次仍顯示「待發佈」
    return {"ok": True, "deploy_id": deploy_id, "remaining": remaining,
            "message": f"已發佈上線（{len(rows)} 場）。"}


def _wait_until_live(deploy_id: str, token: str, timeout: int = 120) -> str:
    """等 Netlify 真的把這次部署發佈出去，回傳最後狀態（ready 才是成功）。"""
    import time
    import urllib.request
    url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys/{deploy_id}"
    deadline = time.time() + timeout
    state = "unknown"
    while time.time() < deadline:
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                state = json.loads(resp.read()).get("state", "unknown")
        except Exception:
            state = "查詢失敗"
        if state in ("ready", "error"):
            return state
        time.sleep(4)
    return f"{state}（等待逾時）"
