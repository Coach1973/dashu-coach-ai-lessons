#!/usr/bin/env python3
"""把一批新反射併進 knowledges/反射索引.json（2026-10-02，第 3 步逐案轉換用）

用法：python3 scripts/reflex_add.py BATCH.json
BATCH.json = {"reflexes": [ {...}, ... ], "case_ledger": {"案例33": "說明", ...}}
  - reflexes：同 id 就取代、沒有就接在最後（維持索引檔原格式）
  - case_ledger：沒有產生反射的案例去向（已退役／併入某條／已有程式擋住），讓「哪些案例處理過了」有單一真相源
"""
import json
import os
import sys

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(WS, "knowledges/反射索引.json")

batch = json.load(open(sys.argv[1], encoding="utf-8"))
d = json.load(open(INDEX, encoding="utf-8"))
by_id = {r["id"]: i for i, r in enumerate(d["reflexes"])}
for r in batch.get("reflexes", []):
    if r["id"] in by_id:
        d["reflexes"][by_id[r["id"]]] = r
    else:
        by_id[r["id"]] = len(d["reflexes"])
        d["reflexes"].append(r)
if batch.get("case_ledger"):
    d.setdefault("case_ledger", {}).update(batch["case_ledger"])
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
print(f"反射 {len(d['reflexes'])} 條；案例去向 {len(d.get('case_ledger', {}))} 筆")
