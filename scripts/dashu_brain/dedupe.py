#!/usr/bin/env python3
"""去重：raw/ → clean/，並產出 reports/。只讀 raw，不改 NotebookLM。

1. 內容完全一樣（去掉空白後 sha256 相同）→ 合併成一份，檔頭記下所有出處。
2. 內容很像（共同片段 ≥ 0.8）或「小的被大的包含」（≥ 0.9）→ 只列報告，兩份都留，不自行判斷。
3. 空白或字數 < 20 的來源 → 記進報告，不放進 clean。
輸出：clean/<筆記本>/<來源>.txt（檔頭 --- 區塊記出處）、reports/exact_dups.csv、reports/near_dups.csv、reports/skipped.csv
"""
import csv, hashlib, json, os, re, shutil, sys
from collections import defaultdict

BASE = "/Volumes/953-SSD/大樹大腦"
CLEAN = os.path.join(BASE, "clean")
REP = os.path.join(BASE, "reports")
K = 8        # 字元片段長度
SAMPLE = 8   # 每 8 個片段取 1 個（hash % 8 == 0）


def safe(s, n=60):
    s = re.sub(r'[\\/:*?"<>|\n\r\t]+', "_", (s or "無標題")).strip(" ._")
    return (s or "無標題")[:n]


def norm(t):
    return re.sub(r"\s+", "", t)


def shingles(t):
    out = set()
    for i in range(0, max(len(t) - K + 1, 1)):
        h = int(hashlib.md5(t[i:i + K].encode()).hexdigest()[:8], 16)
        if h % SAMPLE == 0:
            out.add(h)
    return out


def main():
    rows = {}
    for l in open(os.path.join(BASE, "manifest.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        rows[(r["account"], r["notebook_id"], r["source_id"])] = r   # 同一筆記本內的來源，多次紀錄只留最新
    docs, skipped = [], []
    for r in rows.values():
        p = r["path"]
        if not os.path.exists(p):
            skipped.append((r["account"], r["notebook"], r["title"], r["status"]))
            continue
        t = open(p, encoding="utf-8").read()
        n = norm(t)
        if len(n) < 20:
            skipped.append((r["account"], r["notebook"], r["title"], "字數不足"))
            continue
        docs.append({**r, "text": t, "norm": n})

    # 1) 完全相同
    groups = defaultdict(list)
    for d in docs:
        groups[hashlib.sha256(d["norm"].encode()).hexdigest()].append(d)
    uniq = []
    os.makedirs(REP, exist_ok=True)
    with open(os.path.join(REP, "exact_dups.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["保留的來源", "保留的帳號", "保留的筆記本", "被合併的份數", "被合併的出處"])
        for g in groups.values():
            g.sort(key=lambda d: (-len(d["text"]), d["account"]))
            keep = g[0]
            keep["origins"] = [(d["account"], d["notebook"], d["title"], d["source_id"]) for d in g]
            uniq.append(keep)
            if len(g) > 1:
                w.writerow([keep["title"], keep["account"], keep["notebook"], len(g) - 1,
                            " | ".join(f"{a}/{nb}/{ti}" for a, nb, ti, _ in keep["origins"][1:])])

    # 2) 很像 / 被包含（倒排索引找候選）
    sh = [shingles(d["norm"]) for d in uniq]
    inv = defaultdict(list)
    for i, s in enumerate(sh):
        for h in s:
            inv[h].append(i)
    pairs = set()
    cnt = defaultdict(int)
    for i, s in enumerate(sh):
        cnt.clear()
        for h in s:
            for j in inv[h]:
                if j > i:
                    cnt[j] += 1
        for j, c in cnt.items():
            a, b = len(sh[i]), len(sh[j])
            if not a or not b:
                continue
            jac = c / (a + b - c)
            contain = c / min(a, b)
            if jac >= 0.8 or contain >= 0.9:
                pairs.add((i, j, round(jac, 2), round(contain, 2)))
    with open(os.path.join(REP, "near_dups.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["A帳號", "A筆記本", "A來源", "A字數", "B帳號", "B筆記本", "B來源", "B字數", "相似度", "包含度(小被大包含)"])
        for i, j, jac, con in sorted(pairs, key=lambda x: -x[3]):
            a, b = uniq[i], uniq[j]
            w.writerow([a["account"], a["notebook"], a["title"], len(a["text"]),
                        b["account"], b["notebook"], b["title"], len(b["text"]), jac, con])
    with open(os.path.join(REP, "skipped.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["帳號", "筆記本", "來源", "原因"])
        w.writerows(skipped)

    # 3) 寫 clean/（每次重建，raw 不動）
    if os.path.isdir(CLEAN):
        shutil.rmtree(CLEAN)
    used = set()
    for d in uniq:
        folder = os.path.join(CLEAN, safe(d["notebook"]))
        os.makedirs(folder, exist_ok=True)
        name = safe(d["title"])
        path = os.path.join(folder, name + ".txt")
        if path in used:
            path = os.path.join(folder, f"{name}__{d['source_id'][:8]}.txt")
        used.add(path)
        head = ["---", f"標題: {d['title']}", f"類型: {d.get('type')}", "出處:"]
        head += [f"  - {a} / {nb} / {ti} ({sid[:8]})" for a, nb, ti, sid in d["origins"]]
        head += ["---", ""]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(head) + d["text"])
    print(f"來源 {len(rows)} → 有內容 {len(docs)} → 去掉完全重複後 {len(uniq)} 份")
    print(f"完全重複被合併 {len(docs) - len(uniq)} 份；很像或被包含 {len(pairs)} 組（只列報告）；跳過 {len(skipped)} 份")


if __name__ == "__main__":
    main()
