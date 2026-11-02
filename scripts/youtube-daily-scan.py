#!/usr/bin/env python3
"""
youtube-daily-scan.py — 穩健版 YouTube 每日新片掃描（給 cron 用）

解決兩個會讓「每日新片」變成假空的坑：

坑 1：iCloud 把 ~/Documents 裡的腳本變成 dataless placeholder
  症狀：python3 腳本 → exit code 0、零輸出、0.02 秒跑完（因為 Python 把
        讀不到內容的檔案當成空程式執行）
  為什麼會假成功：真正的 Python 讀檔失敗會丟 OSError，但 CPython 開啟主檔
        失敗時會走空程式路徑 → 所以 exit code 0 卻什麼都沒做
  修法：執行前檢查 SF_DATALESS flag，用 brctl download 把真實內容叫回來；
        再用「檔案大小 + 可讀位元組」雙重確認真的讀到了內容。

坑 2：YouTube RSS 偶發 404 / 500
  症狀：每次跑掉幾個頻道，而且掉的不一樣（單次跑 9～13 部不穩定）
  修法：同一輪重跑多次，把結果取聯集（去重），再照時間排序輸出。

輸出格式與原版 fetch-youtube-rss.py 相同（標題＋連結＋台北時間），
讓教練收到的排版不會變。
"""
import os
import re
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

# 原始腳本：放在 iCloud Documents 裡，權威來源
SRC = "/Users/bymyway/Documents/mac-openclaw-workflows/skills/youtube-monitor/fetch-youtube-rss.py"

# 工作區副本：不在 iCloud 裡，永遠可讀，用來確認原始腳本壞掉時還有東西可跑
FALLBACK = "/Users/bymyway/.openclaw/workspace/scripts/fetch-youtube-rss.py"

# 跑幾輪取聯集（RSS 偶發錯誤越多，輪數要越多才收斂）
ROUNDS = int(os.environ.get("YT_ROUNDS", "4"))

TZ8 = timezone(timedelta(hours=8))
ENTRY_RE = re.compile(r"^\d+\. 【(.+?)】(.+)\n\s+🔗 (\S+)\s+\((.+?) 台北\)$", re.M)


def is_dataless(path):
    """回傳 True 代表這是 iCloud 只留殼、沒下載內容的檔案。"""
    try:
        st = os.lstat(path)
    except OSError:
        return False
    # SF_DATALESS = 0x40000000
    return bool(st.st_flags & 0x40000000)


def materialize(path):
    """把 iCloud 佔位檔的真實內容叫回來，並確認真的讀得到內容。"""
    if not os.path.exists(path):
        return False
    if is_dataless(path):
        print(f"[youtube-daily-scan] {path} 是 iCloud 佔位檔，正在下載真實內容…",
              file=sys.stderr)
        try:
            subprocess.run(["/usr/bin/brctl", "download", path],
                           capture_output=True, timeout=120)
        except Exception as e:
            print(f"[youtube-daily-scan] brctl download 失敗：{e}", file=sys.stderr)
    # 等檔案真的變成有內容（最多 60 秒）
    for _ in range(30):
        if not is_dataless(path):
            try:
                with open(path, "rb") as f:
                    if f.read(1):
                        return True
            except OSError:
                pass
        time.sleep(2)
    return False


def run_once(script):
    """跑一次原始腳本，回傳 (exit_code, stdout)。"""
    try:
        p = subprocess.run([sys.executable, script, "--days", "1"],
                           capture_output=True, text=True, timeout=600)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 1, ""
    except Exception as e:
        print(f"[youtube-daily-scan] 執行失敗：{e}", file=sys.stderr)
        return 1, ""


def main():
    script = SRC
    if not materialize(SRC):
        print("[youtube-daily-scan] 原始腳本取不到內容，改用工作區副本",
              file=sys.stderr)
        script = FALLBACK
        if not materialize(FALLBACK):
            print("[youtube-daily-scan] 兩份腳本都不可用", file=sys.stderr)
            print("=== 過去 1 天新影片（共 0 部）===")
            return 1

    videos = {}
    for i in range(ROUNDS):
        code, out = run_once(script)
        found = ENTRY_RE.findall(out)
        for ch, title, url, pub in found:
            vid = url.rsplit("/", 1)[-1]
            videos.setdefault(vid, (ch, title, url, pub))
        print(f"[youtube-daily-scan] 第 {i+1}/{ROUNDS} 輪：exit={code} "
              f"本輪 {len(found)} 部、累計 {len(videos)} 部", file=sys.stderr)
        if code != 0 and not found:
            continue

    if not videos:
        print("=== 過去 1 天新影片（共 0 部）===")
        return 0

    rows = sorted(videos.values(), key=lambda r: (r[3], r[0]))
    print(f"=== 過去 1 天新影片（共 {len(rows)} 部）===")
    print()
    for i, (ch, title, url, pub) in enumerate(rows, 1):
        print(f"{i}. 【{ch}】{title}")
        print(f"   🔗 {url}  ({pub} 台北)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
