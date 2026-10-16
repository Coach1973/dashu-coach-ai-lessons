#!/usr/bin/env python3
"""擋「分支名稱打錯」的 git 指令（PreToolUse Bash）。

workspace 跟 ~/.openclaw 推到同一個 GitHub 倉庫的兩條線：
  workspace  → main
  ~/.openclaw → master
2026-10-16 15:00 有 AI 在 workspace 打成 `git pull --rebase origin master`，
整個 workspace 被換成另一套檔、教練的指令被擋 3.5 小時（試金石123）。

規則一：在這兩個資料夾裡，pull/push/rebase/merge/reset/checkout/switch 指到「另一個資料夾的分支名稱」就擋下。
規則二（所有資料夾）：指令裡寫的分支名稱跟目前分支不同，而且那條線跟目前分支「完全沒有共同歷史」（不相干的另一條線），也擋下。
9/10 在 ~/.openclaw 憑印象寫 main、10/16 在 workspace 憑印象寫 master，同一個坑踩兩次，所以不靠 AI 記得，由這支程式在執行前查真相。
擋下時告訴 AI 正確的分支名稱。其他 git 指令一律放行。
本程式自己出任何錯都放行（回 0），絕不因為壞掉而擋人。
"""
import json
import os
import re
import shlex
import subprocess
import sys

HOME = os.path.expanduser("~")
REPOS = {
    os.path.realpath(os.path.join(HOME, ".openclaw/workspace")): ("main", "master"),  # 正確, 打錯
    os.path.realpath(os.path.join(HOME, ".openclaw")): ("master", "main"),
}
RISKY = {"pull", "push", "rebase", "merge", "reset", "checkout", "switch"}


def toplevel(d):
    try:
        r = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, timeout=5)
        return os.path.realpath(r.stdout.strip()) if r.returncode == 0 else None
    except Exception:
        return None


def expand(p, base):
    p = os.path.expanduser(p.replace("$HOME", HOME))
    return os.path.realpath(p if os.path.isabs(p) else os.path.join(base, p))


def names_branch(args, wrong):
    """args 裡有沒有指到 wrong 這個分支（origin wrong、origin/wrong、x:wrong、checkout wrong）。"""
    for a in args:
        if a.startswith("-"):
            continue
        for part in a.lstrip("+").split(":"):
            part = part.replace("refs/heads/", "").replace("refs/remotes/", "")
            if part in (wrong, "origin/" + wrong):
                return True
    return False


def git(where, *args):
    r = subprocess.run(["git", "-C", where, *args], capture_output=True, text=True, timeout=5)
    return r.returncode, r.stdout.strip()


def unrelated_branch(where, args):
    """args 裡寫到的分支，如果不是目前分支、而且跟目前分支沒有共同歷史，就回傳 (分支名, 目前分支)。"""
    rc, cur = git(where, "branch", "--show-current")
    if rc != 0 or not cur:
        return None
    for a in args:
        if a == "--":
            break
        if a.startswith("-"):
            continue
        for part in a.lstrip("+").split(":"):
            name = part.replace("refs/heads/", "").replace("refs/remotes/", "")
            if name.startswith("origin/"):
                name = name[len("origin/"):]
            if not name or name in (cur, "HEAD", "origin"):
                continue
            for ref in ("refs/remotes/origin/" + name, "refs/heads/" + name):
                if git(where, "rev-parse", "--verify", "-q", ref)[0] != 0:
                    continue
                if git(where, "merge-base", "HEAD", ref)[0] != 0:
                    return name, cur
    return None


def check(command, cwd):
    # 依 ; && || | 換行 切段，追蹤 cd 之後的所在資料夾
    here = cwd
    for seg in re.split(r"&&|\|\||;|\||\n", command):
        try:
            toks = shlex.split(seg)
        except ValueError:
            toks = seg.split()
        if not toks:
            continue
        if toks[0] == "cd" and len(toks) > 1:
            here = expand(toks[1], here)
            continue
        if toks[0] != "git":
            continue
        i, where = 1, here
        while i < len(toks) and toks[i].startswith("-"):
            if toks[i] == "-C" and i + 1 < len(toks):
                where = expand(toks[i + 1], where)
                i += 2
            elif toks[i] == "-c" and i + 1 < len(toks):
                i += 2
            else:
                i += 1
        if i >= len(toks) or toks[i] not in RISKY:
            continue
        top = toplevel(where)
        if top not in REPOS:
            hit = unrelated_branch(where, toks[i + 1:]) if top else None
            if hit:
                return (f"⛔ 已擋下：{top} 目前的分支是「{hit[1]}」，指令裡寫的「{hit[0]}」是一條跟它完全沒有共同歷史的線。"
                        f"照這樣跑會把整個資料夾換成另一套檔案（試金石123）。先跑 git branch --show-current 確認，"
                        f"把「{hit[0]}」改成「{hit[1]}」再跑。")
            continue
        right, wrong = REPOS[top]
        if names_branch(toks[i + 1:], wrong):
            return (f"⛔ 已擋下：{top} 的分支是「{right}」，指令裡寫成「{wrong}」（那是另一個資料夾的分支）。"
                    f"照這樣跑會把整個資料夾換成另一套檔案（10/16 15:00 真的發生過，教練被擋 3.5 小時，試金石123）。"
                    f"請把「{wrong}」改成「{right}」再跑一次。")
    return None


def main():
    try:
        data = json.load(sys.stdin)
        if data.get("tool_name") not in ("Bash", None):
            return 0
        cmd = (data.get("tool_input") or {}).get("command", "")
        if "git" not in cmd:
            return 0
        msg = check(cmd, data.get("cwd") or os.getcwd())
        if msg:
            print(msg, file=sys.stderr)
            return 2
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
