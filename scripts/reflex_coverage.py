#!/usr/bin/env python3
"""試金石案例 → 反射 覆蓋率檢查（2026-10-02，第 3 步逐案轉換用）

案例庫每個「## 案例 X」標題，算「已處理」的條件：
  ① 反射索引任一筆的 source 提到它（案例27、案例C、案例F-2026-06-07 …）
  ② 或出現在索引的 case_ledger（沒產生反射的案例去向：已退役／併入／已有程式擋住）
  ③ 或 Top30 證據檔把它掛在某個主題的 cases
記憶（2026-10-02 第四步加）：MEMORY.md 索引連到的每個記憶檔，算「已處理」的條件：
  ① 反射索引任一筆的 source 提到它的檔名
  ② 或出現在索引的 memory_ledger（併入哪條／參考資料／判斷類／已有程式擋住／已退役）
用法：python3 scripts/reflex_coverage.py        # 印未處理清單（案例＋記憶）
"""
import json
import os
import re

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = json.load(open(os.path.join(WS, "knowledges/反射索引.json"), encoding="utf-8"))
top30 = json.load(open(os.path.join(WS, "state/top30_evidence_ids.json"), encoding="utf-8"))

KEY = r"(\d+(?:-2026-\d\d-\d\d)?|[A-Z](?:-2026-\d\d-\d\d)?)"
done = set()
for r in idx["reflexes"]:
    for m in re.finditer(r"案例\s*(" + KEY + r"(?:[／/、]\s*" + KEY + r")*)", r.get("source", "")):
        done |= set(re.findall(KEY, m.group(1)))
for k in idx.get("case_ledger", {}):
    m = re.match(r"案例\s*" + KEY, k)
    if m:
        done.add(m.group(1))
for t in top30["themes"]:
    done |= {str(c) for c in t["cases"]}

seen, todo = set(), []
for line in open(os.path.join(WS, "試金石/試金石_案例庫.md"), encoding="utf-8"):
    m = re.match(r"^## (?:📖 )?案例\s*" + KEY, line)
    if not m or m.group(1) == "X":
        continue  # X 是案例模板，不是案例
    key = m.group(1)
    base = re.match(r"\d+|[A-Z]", key).group(0)  # 案例 25-2026-06-18 這類日期後綴，算同一案例
    if key in seen:
        continue
    seen.add(key)
    if key not in done and base not in done:
        todo.append(line.strip()[:90])
print(f"案例標題 {len(seen)} 個；已處理 {len(seen) - len(todo)}；未處理 {len(todo)}")
for t in todo:
    print("  ", t)

MEM = os.path.realpath(os.path.expanduser("~/.claude/projects/-Users-bymyway--openclaw/memory"))  # 這是連到 workspace/claude-brain 的捷徑，先解開，../knowledges 這類相對連結才算得對
if os.path.exists(os.path.join(MEM, "MEMORY.md")):
    sources = " ".join(r.get("source", "") for r in idx["reflexes"])
    ledger = idx.get("memory_ledger", {})
    links = {}
    for line in open(os.path.join(MEM, "MEMORY.md"), encoding="utf-8"):
        if line.startswith("- ["):
            for f in re.findall(r"\]\(([^)]+\.md)\)", line):
                links.setdefault(os.path.basename(f)[:-3], f)
    files = list(links)
    mtodo = [f for f in files if f not in sources and f not in ledger]
    missing = [f for f, rel in links.items() if not os.path.exists(os.path.normpath(os.path.join(MEM, rel)))]
    print(f"記憶索引 {len(files)} 個；已處理 {len(files) - len(mtodo)}；未處理 {len(mtodo)}；索引斷鏈 {len(missing)}")
    for f in mtodo + [f"（斷鏈）{m}" for m in missing]:
        print("  ", f)
