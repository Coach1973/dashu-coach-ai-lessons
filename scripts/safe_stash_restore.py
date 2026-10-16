#!/usr/bin/env python3
"""自動同步「stash 放不回去」時的安全放回（2026-10-16 盤查：52 筆暫存沒人取回，索引、SOP、整份檔案默默不見）。

用法：safe_stash_restore.py <repo路徑> <stash的sha>
在 `git stash pop` 失敗之後呼叫。逐檔處理，保證暫存裡的東西一定落地，不會再留在暫存清單裡沒人管：
  - 現在的檔＝暫存的版本 → 不用動
  - 現在的檔＝暫存當時的原樣（沒人改過）→ 直接放回暫存版本
  - 兩邊都改過、文字檔（.md .txt .csv .log .jsonl）→ 兩邊的行都保留（git merge-file --union）
  - 兩邊都改過、其他檔（json、程式…）→ 保留現在的，暫存版本另存到 handoff_archive/stash_rescue_auto/<時間>/
  - 暫存裡記的「刪除」一律不執行（寧可多留一個檔，也不刪）
全部處理完才把這筆暫存從清單移除。本程式出任何錯都不刪暫存、回 0，不擋呼叫它的程式。
"""
import os
import subprocess
import sys
import tempfile
from datetime import datetime

TEXT_EXT = (".md", ".txt", ".csv", ".log", ".jsonl")


def git(repo, *args, check_rc=False, binary=True):
    r = subprocess.run(["git", "-c", "core.quotepath=off", "-C", repo, *args], capture_output=True)
    return r.returncode, (r.stdout if binary else r.stdout.decode("utf-8", "ignore"))


def show(repo, rev, path):
    rc, out = git(repo, "show", f"{rev}:{path}")
    return out if rc == 0 else None


def main(repo, sha):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    rescue_root = os.path.join(repo, "handoff_archive", "stash_rescue_auto", stamp)
    counts = {"same": 0, "restored": 0, "union": 0, "rescued": 0, "skipped_delete": 0}

    # 1) 先清掉 pop 留下的「未合併」狀態：衝突檔先回到現在的版本（HEAD），再逐檔判斷
    _, unmerged = git(repo, "diff", "--name-only", "--diff-filter=U", binary=False)
    for f in filter(None, unmerged.splitlines()):
        git(repo, "checkout", "--ours", "--", f)
    git(repo, "reset", "-q")

    # 2) 暫存裡的檔案：有追蹤的改動（sha^1→sha）＋未追蹤的新檔（sha^3）
    items = []
    _, changed = git(repo, "diff", "--name-status", f"{sha}^1", sha, binary=False)
    for line in filter(None, changed.splitlines()):
        st, f = line.split("\t", 1)
        items.append((st[0], f, f"{sha}^1", sha))
    if git(repo, "rev-parse", "-q", "--verify", f"{sha}^3")[0] == 0:
        _, ut = git(repo, "ls-tree", "-r", "--name-only", f"{sha}^3", binary=False)
        for f in filter(None, ut.splitlines()):
            items.append(("A", f, None, f"{sha}^3"))

    for st, f, base_rev, rev in items:
        p = os.path.join(repo, f)
        if st == "D":
            counts["skipped_delete"] += 1
            continue
        want = show(repo, rev, f)
        if want is None:
            continue
        cur = open(p, "rb").read() if os.path.isfile(p) else None
        base = show(repo, base_rev, f) if base_rev else None
        if cur == want:
            counts["same"] += 1
        elif cur is None or cur == base:
            os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
            open(p, "wb").write(want)
            counts["restored"] += 1
        elif f.lower().endswith(TEXT_EXT):
            with tempfile.TemporaryDirectory() as td:
                paths = []
                for name, data in (("cur", cur), ("base", base or b""), ("want", want)):
                    q = os.path.join(td, name)
                    open(q, "wb").write(data)
                    paths.append(q)
                r = subprocess.run(["git", "merge-file", "-p", "--union", *paths], capture_output=True)
            open(p, "wb").write(r.stdout)
            counts["union"] += 1
        else:
            q = os.path.join(rescue_root, f)
            os.makedirs(os.path.dirname(q), exist_ok=True)
            open(q, "wb").write(want)
            counts["rescued"] += 1

    # 3) 全部落地了，才把這筆暫存移出清單
    _, lst = git(repo, "stash", "list", "--format=%H %gd", binary=False)
    for line in lst.splitlines():
        h, ref = line.split(" ", 1)
        if h == sha:
            git(repo, "stash", "drop", "-q", ref)
            break
    summary = (f"相同{counts['same']} 放回{counts['restored']} 兩邊合併{counts['union']} "
               f"另存{counts['rescued']} 不執行刪除{counts['skipped_delete']}")
    if counts["rescued"]:
        summary += f"（另存在 {os.path.relpath(rescue_root, repo)}）"
    print(summary)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3 and sys.argv[2]:
            main(os.path.abspath(sys.argv[1]), sys.argv[2])
    except Exception as e:  # 壞了也不刪暫存、不擋人
        print(f"safe_stash_restore 出錯（暫存保留在清單）：{e!r}")
    sys.exit(0)
