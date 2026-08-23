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
from datetime import date, datetime
from pathlib import Path

import db

BIGTREE_REPO = Path("/Users/bymyway/github_repos/bigtree")
INDEX_HTML = BIGTREE_REPO / "index.html"
NETLIFY_SITE_ID = "40e580f0-1def-4777-adb8-587ef023ed36"
QUOTA_FILE = Path("/Users/bymyway/.openclaw/workspace/state/netlify_deploy_quota.json")
CREDENTIALS = Path("/Users/bymyway/.openclaw/workspace/credentials/netlify_token.txt")

WEEKDAY_TW = ["一", "二", "三", "四", "五", "六", "日"]

# 前端 SLOTS 表的權威來源就是 index.html，這裡只在後台顯示下拉選單時用
SLOT_CHOICES = ["早", "早半", "午", "午半", "晚", "晚半", "夜", "線上", "上午", "下午", "全日", "TBD"]


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


def diff_summary(conn) -> dict:
    """發佈前給教練看的摘要。

    「還沒發佈」要比對的是『線上官網』而不是本機檔案——本機檔案先被改好、
    但還沒部署上去的情況是存在的（例如 AI 先改好檔案），若拿本機檔案比，
    會誤判成「已經一致」，教練按了發佈也不會有動作，官網就一直停在舊版。
    改成記錄「上次真正部署成功時的內容指紋」來比對。
    """
    rows = read_sessions(conn)
    return {
        "sessions": [
            {"date": r["event_date"], "label": make_label(r["event_date"]),
             "slot": r["slot_key"], "topic": r["name"], "venue": r["venue"], "slug": r["slug"]}
            for r in rows
        ],
        "has_changes": _content_hash(rows) != _get_published_hash(conn),
    }


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

    # 只打包「已經 commit 的內容」（git archive HEAD），不是工作區現況——
    # 否則同一個 repo 裡其他還沒確認的修改（例如改到一半的別站頁面）會被一起送上線。
    zip_path = Path("/tmp/bigtree_publish.zip")
    if zip_path.exists():
        zip_path.unlink()
    with open(zip_path, "wb") as f:
        subprocess.run(["git", "archive", "--format=zip", "HEAD"], cwd=BIGTREE_REPO,
                       check=True, stdout=f, timeout=120)

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
    _set_published_hash(conn, target_hash)  # 部署成功才記錄，失敗時下次仍會顯示「待發佈」
    remaining = _bump_quota(deploy_id, commit_msg)
    return {"ok": True, "deploy_id": deploy_id, "remaining": remaining,
            "message": f"已發佈上線（{len(rows)} 場）。"}
