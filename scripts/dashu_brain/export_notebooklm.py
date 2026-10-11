#!/usr/bin/env python3
"""把 NotebookLM 兩個帳號的所有來源原文，搬到 SSD（只讀不改，可續跑）。

用法：python3 export_notebooklm.py [--limit-notebooks N] [--profile default|seabiscuit]
輸出：../raw/<帳號>/<筆記本>__<id8>/<來源>__<id8>.txt  +  ../manifest.jsonl
已存在的檔案直接跳過（續跑安全）。
"""
import argparse, hashlib, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

NLM = "/Volumes/953-SSD/NotebookLM工具/venv/bin/nlm"
BASE = "/Volumes/953-SSD/大樹大腦"
ACCOUNTS = {"default": "bymyway7", "seabiscuit": "seabiscuitclub"}


def run(args, profile, retries=3):
    for i in range(retries):
        p = subprocess.run([NLM, *args, "--profile", profile], capture_output=True, text=True, timeout=180)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout
        time.sleep(2 * (i + 1))
    return None


def safe(s, n=60):
    s = re.sub(r'[\\/:*?"<>|\n\r\t]+', "_", (s or "無標題")).strip(" ._")
    return (s or "無標題")[:n]


def fetch_source(job):
    profile, account, nb, src = job
    d = os.path.join(BASE, "raw", account, f"{safe(nb['title'])}__{nb['id'][:8]}")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{safe(src.get('title'))}__{src['id'][:8]}.txt")
    meta = {"account": account, "notebook_id": nb["id"], "notebook": nb["title"],
            "source_id": src["id"], "title": src.get("title"), "type": src.get("type"),
            "url": src.get("url"), "path": path}
    if os.path.exists(path):
        meta["status"] = "skip_exists"
        meta["sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()
        return meta
    out = run(["source", "content", src["id"], "--json"], profile)
    if out is None:
        meta["status"] = "fail"
        return meta
    try:
        text = json.loads(out).get("content") or ""
    except Exception:
        text = out
    if not text.strip():
        meta["status"] = "empty"
        return meta
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(path + ".tmp", path)
    meta["status"] = "ok"
    meta["chars"] = len(text)
    meta["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=list(ACCOUNTS), action="append")
    ap.add_argument("--limit-notebooks", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    profiles = a.profile or list(ACCOUNTS)
    mf = open(os.path.join(BASE, "manifest.jsonl"), "a", encoding="utf-8")
    for profile in profiles:
        account = ACCOUNTS[profile]
        nbs = json.loads(run(["notebook", "list", "--json"], profile) or "[]")
        if a.limit_notebooks:
            nbs = nbs[: a.limit_notebooks]
        print(f"[{account}] 筆記本 {len(nbs)}", flush=True)
        for i, nb in enumerate(nbs, 1):
            out = run(["source", "list", nb["id"], "--json"], profile)
            srcs = json.loads(out) if out else []
            srcs = srcs if isinstance(srcs, list) else srcs.get("sources", [])
            jobs = [(profile, account, nb, s) for s in srcs]
            with ThreadPoolExecutor(a.workers) as ex:
                for m in ex.map(fetch_source, jobs):
                    mf.write(json.dumps(m, ensure_ascii=False) + "\n")
            mf.flush()
            print(f"[{account}] {i}/{len(nbs)} {nb['title'][:30]} ({len(srcs)} 份)", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
