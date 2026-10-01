#!/usr/bin/env python3
"""從 knowledges/反射索引.json 產生 knowledges/情境目錄.md（給人看的版本，唯一真相源是 JSON）。"""
import json, collections
WS = "/Users/bymyway/.openclaw/workspace"
d = json.load(open(f"{WS}/knowledges/反射索引.json", encoding="utf-8"))
MOMENT = {"prompt": "教練說話時自動調出", "pre_tool": "AI 動手前自動調出", "post_tool": "AI 看到結果時自動調出",
          "reply": "AI 回話前自動檢查", "guard": "🔒 程式已擋住", "judgment": "判斷類（靠 21 條）"}
groups = collections.OrderedDict()
for r in d["reflexes"]:
    groups.setdefault(r["situation"], []).append(r)
out = ["# 情境目錄：要做這件事之前，先看這幾行", "",
       "> ⚠️ 本檔由 `scripts/render_situation_directory.py` 從 `knowledges/反射索引.json` 自動產生，**不要手改**；要新增或修改，改 JSON 再重跑。",
       "> 大部分條目不用靠記性：系統會在對的時刻自動調出（`scripts/reflex_router.py`）。試金石／記憶全文是檔案櫃，要查才查。", ""]
for sit, rs in groups.items():
    out.append(f"## {sit}")
    for r in rs:
        tag = MOMENT.get(r["moment"], r["moment"]) + ("・擋下" if r.get("level") == "block" else "")
        by = f"（{r['enforced_by']}）" if r.get("enforced_by") else ""
        out.append(f"- [{tag}{by}] {r['say']}　出處：{r['source']}")
    out.append("")
open(f"{WS}/knowledges/情境目錄.md", "w", encoding="utf-8").write("\n".join(out))
print(f"情境目錄：{len(groups)} 個情境、{len(d['reflexes'])} 條")
