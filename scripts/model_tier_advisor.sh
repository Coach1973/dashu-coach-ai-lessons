#!/bin/bash
# Hook：UserPromptSubmit
# 用途：模型分工默契（2026-09-25 教練親定 v2，規則全文 knowledges/模型分工規則_Opus與Sonnet.md）
#   教練每丟一則交辦（含天馬行空的新點子），不管現在哪個模型，回覆第一行都要標示：
#   「🟢 這件 Sonnet 就能做」或「🟣 這件是 Opus 等級（理由）」。
#   Sonnet 碰到 🟣 → 先建議切換、先不動手；Sonnet 做到一半卡關 → 停下建議切 Opus。
#   標示有沒有做到，由 stop_rules_master.py 的 A3 檢查擋下補上。
# 模型判斷：對話紀錄最後一則回覆的 model 欄位，與最後一次 /model 指令，取較新者。
INPUT=$(cat)
printf '%s' "$INPUT" | /usr/bin/python3 -c '
import json, re, sys
d = json.load(sys.stdin)
prompt = (d.get("prompt") or "").strip()
tp = d.get("transcript_path") or ""
if len(prompt) < 15:
    sys.exit(0)

model = ""
try:
    for line in open(tp, encoding="utf-8"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        msg = e.get("message") or {}
        if e.get("type") == "assistant" and msg.get("model") and msg["model"] != "<synthetic>":
            model = msg["model"]
        elif e.get("type") == "user" and isinstance(msg.get("content"), str):
            m = re.search(r"<command-name>/model</command-name>.*?<command-args>([^<]+)</command-args>", msg["content"], re.S)
            if m and m.group(1).strip():
                model = m.group(1).strip()
except Exception:
    pass

ml = model.lower()
high = ("opus" in ml) or ("fable" in ml)
SIGNALS = [
    ("找根因", r"為什麼.{0,30}(會|不會|又|只有|偏偏)|根源|根本原因|徹底|復發|又壞|又出現|還是沒|一直沒|反覆|老是|每次都|繞一大圈"),
    ("多系統", r"架構|整合|串接|全面|體檢|盤點|遷移|搬家|跨機|同步機制"),
    ("不可逆", r"刪除|刪掉|清掉|砍掉|重灌|金鑰|外洩|付費|花錢|合約|報價|退版"),
    ("設計機制", r"設計|規劃|策略|提案|企劃|機制|制度|SOP|規則|流程"),
    ("教練不滿", r"浪費|搞不懂|很蠢|又犯|同樣的錯|受不了|講過|說過了|不 ?OK"),
    ("重要對外", r"對外|公告|新聞稿|簡報|提案書"),
]
hits = [n for n, rx in SIGNALS if re.search(rx, prompt)]
stuck = re.search(r"還是不行|還是沒|還是一樣|又沒|沒用|沒解決|一樣的問題|不對啊|怎麼又", prompt)

out = ["🧭 模型分工標示（knowledges/模型分工規則_Opus與Sonnet.md）：目前是 %s。" % (model or "未知模型"),
       "回覆第一行必須標示：「🟢 這件 Sonnet 就能做」或「🟣 這件是 Opus 等級（理由：…）」。閒聊、道謝也標，寫「🟢 閒聊」即可。",
       ("關鍵字初判命中：%s（字面碰到不算，最後由你判斷）" % "、".join(hits)) if hits
       else "關鍵字初判沒命中；天馬行空的新點子也要自己判斷：要設計、跨系統、不可逆、找根因就是 🟣。"]
if high:
    out.append("判定 🟢：照常做完（已在 Opus 不用中途換），第一行寫「🟢 這件 Sonnet 就能做，下一件可以切回 Sonnet 省流量」。")
else:
    if "直接做" in prompt:
        out.append("教練說「直接做」：用目前模型照常做，標示後直接開始。")
    else:
        out.append("判定 🟣：標示後只加一句「教練，建議切換到 Opus 5.5 再做，可能會節省您的時間；要用目前模型直接做，回『直接做』」，先不動手。判定 🟢：照常做。")
    out.append("做到一半卡關（兩種方法都沒解決、找不到原因）：立刻停下，說「教練，我卡關了，建議切換到 Opus 5.5 接手」＋卡在哪一句。")
    if stuck:
        out.append("⚠️ 教練這句表示上一步沒解決＝卡關訊號，優先建議切 Opus。")
print("\n".join(out))
' 2>/dev/null
exit 0
