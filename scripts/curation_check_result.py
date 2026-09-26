#!/usr/bin/env python3
"""策展/大樹作品上傳後的「真實結果」查詢工具（2026-09-26教練交辦：一次性解決反覆猜網址的問題）。

背景：curation_process.py是非同步背景處理，curl上傳回200只代表「檔案收到、排進佇列」，
不代表處理完成，也不保證最終網址等於custom_slug（店家若命中既有暫代頁，會被改成
shops.bymyway.com/<其他slug>/，custom_slug被略過——這是2026-09-06教練拍板的既有設計，
不是bug）。過去Hermes兩次都用「等N秒＋猜/curated/<custom_slug>/」的方式自我驗證，
兩次都猜錯（一次是index.html判斷式太嚴格真的失敗、一次是網址本來就不是猜的那個），
最後都得寫信給軍師人工查log才知道真相。

這支工具把「查log→判斷結果→算出真實網址→curl驗證上線」這一串軍師每次手動做的
動作包成一行指令，任何AI（Hermes/小龍蝦/ACER/聯想）上傳後都能自己立刻查真相，
不用再猜、不用再寫信求救。

用法：
    python3 scripts/curation_check_result.py <zip檔名關鍵字或custom_slug>

輸出：JSON，欄位：found / status(success|overwritten_existing|failed|pending|not_found)
     / actual_url / live_check(HTTP狀態碼) / note
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

WORKSPACE = Path("/Users/bymyway/.openclaw/workspace")
LOG_PATH = WORKSPACE / "distill" / "curation_process.log"
EVENT_SIGNUP = WORKSPACE / "event-signup"
INCOMING_DIR = EVENT_SIGNUP / "curation_uploads" / "incoming"
PROCESSING_DIR = EVENT_SIGNUP / "curation_uploads" / "processing"
FAILED_DIR = EVENT_SIGNUP / "curation_uploads" / "failed"

LINE_PATTERNS = [
    # (regex, status)
    (re.compile(r"✅ 完成\(覆蓋既有暫代頁\)：(?P<pkg>.+?) → (?P<slug>[\w-]+)$"), "overwritten_existing"),
    (re.compile(r"✅ 大樹作品完成：(?P<pkg>.+?) → (?P<slug>[\w-]+)$"), "success_creation"),
    (re.compile(r"✅ 完成：(?P<pkg>.+?) → (?P<slug>[\w-]+)$"), "success_shop_new"),
    (re.compile(r"❌ 處理失敗：(?P<pkg>.+?): (?P<err>.+)$"), "failed"),
]


def url_for(status: str, slug: str) -> str:
    # 2026-09-27教練拍板全站統一：不管新店家或覆蓋既有暫代頁，網址一律 event.bymyway.com/curated/<slug>/
    return f"https://event.bymyway.com/curated/{slug}/"


def live_check(url: str) -> int | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (curation-check)"})
        return urllib.request.urlopen(req, timeout=15).status
    except urllib.error.HTTPError as e:  # noqa: F821
        return e.code
    except Exception:  # noqa: BLE001
        return None


def check_pending_dirs(keyword: str) -> str | None:
    for d, label in ((INCOMING_DIR, "還沒開始處理(incoming/)"), (PROCESSING_DIR, "處理中(processing/)"), (FAILED_DIR, "已失敗(failed/)")):
        if not d.is_dir():
            continue
        for p in d.iterdir():
            if keyword in p.name:
                return label
    return None


def main() -> None:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "用法：python3 curation_check_result.py <zip檔名關鍵字或custom_slug>"}, ensure_ascii=False))
        sys.exit(1)
    keyword = sys.argv[1]

    if not LOG_PATH.is_file():
        print(json.dumps({"found": False, "status": "not_found", "note": "log檔不存在"}, ensure_ascii=False))
        return

    lines = LOG_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    match = None
    for line in reversed(lines):  # 從最新往回找，同一個關鍵字取最後一次結果
        if keyword not in line:
            continue
        for pat, status in LINE_PATTERNS:
            m = pat.search(line)
            if m:
                match = (status, m.groupdict())
                break
        if match:
            break

    if not match:
        pending_note = check_pending_dirs(keyword)
        if pending_note:
            print(json.dumps({"found": True, "status": "pending", "note": pending_note}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({
                "found": False, "status": "not_found",
                "note": "log裡查無這個關鍵字，也不在incoming/processing/failed/。確認關鍵字是否正確、或launchd WatchPaths是否真的觸發過(查com.coach.curation-watch.plist是否還活著)",
            }, ensure_ascii=False, indent=2))
        return

    status, groups = match
    if status == "failed":
        print(json.dumps({
            "found": True, "status": "failed",
            "package": groups.get("pkg"), "error": groups.get("err"),
            "note": "檔案已搬到curation_uploads/failed/，需人工檢查後重新上傳",
        }, ensure_ascii=False, indent=2))
        return

    slug = groups["slug"]
    url = url_for(status, slug)
    http_status = live_check(url)
    note = ""
    if status == "overwritten_existing":
        note = "這家店原本有自助登錄的暫代頁，已覆蓋成完整網站；網址以上面actual_url為準"
    print(json.dumps({
        "found": True, "status": status, "package": groups.get("pkg"),
        "actual_slug": slug, "actual_url": url, "live_check_http_status": http_status,
        "note": note,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
