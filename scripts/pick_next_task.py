# -*- coding: utf-8 -*-
"""從接力棒挑「時間最新」的教練交辦段落（邏輯同 feed_junshi_handoff.sh 的 NEXT_TASK）。用法：python pick_next_task.py <接力棒檔>"""
import re, sys

lines = [l.rstrip("\r") for l in open(sys.argv[1], encoding="utf-8-sig").read().split("\n")]
cands, ts = [], ""
for i, l in enumerate(lines):
    if l.startswith("## "):
        m = re.search(r"(20\d\d-\d\d-\d\d)\s*(\d\d:\d\d)", l)
        ts = f"{m.group(1)} {m.group(2)}" if m else ""
        if l.startswith("## 🎯"):
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            cands.append((ts, -i, lines[i:end]))
    elif re.match(r"^### 📋 下一場(開工)?(先做|第一件)", l):
        end = next((j for j in range(i + 1, len(lines)) if re.match(r"^(##|---)", lines[j])), len(lines))
        cands.append((ts, -i, lines[i + 1:end]))
if cands:
    sys.stdout.buffer.write("\n".join(l for l in max(cands)[2] if l.strip()).encode("utf-8"))
