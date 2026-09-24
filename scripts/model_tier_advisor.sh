#!/bin/bash
# Hook：UserPromptSubmit
# 用途：模型分工默契（2026-09-25 教練親定，規則全文 knowledges/模型分工規則_Opus與Sonnet.md）
#   在 Sonnet（或更低）碰到 Opus 級任務 → 注入「先一句話提醒教練切 Opus，先不動手」
#   在 Opus 碰到庶務 → 注入「做完最後一行提醒可切回 Sonnet」
#   同一對話框同一種提醒只一次：以我過去回覆裡真的出現過提醒句為準（結構判斷，不靠記得）。
# 模型判斷：對話紀錄最後一則回覆的 model 欄位，與最後一次 /model 指令，取較新者。
INPUT=$(cat)
printf '%s' "$INPUT" | /usr/bin/python3 -c '
import json, re, sys
d = json.load(sys.stdin)
prompt = d.get("prompt") or ""
tp = d.get("transcript_path") or ""
if len(prompt.strip()) < 15 or not tp:
    sys.exit(0)

model, said_up, said_down = "", False, False
try:
    for line in open(tp, encoding="utf-8"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        msg = e.get("message") or {}
        if e.get("type") == "assistant":
            if msg.get("model") and msg["model"] != "<synthetic>":
                model = msg["model"]
            for c in msg.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "text":
                    t = c.get("text", "")
                    said_up |= "適合讓 Opus 等級" in t
                    said_down |= "切回 Sonnet 省流量" in t
        elif e.get("type") == "user":
            c = msg.get("content")
            if isinstance(c, str):
                m = re.search(r"<command-name>/model</command-name>.*?<command-args>([^<]+)</command-args>", c, re.S)
                if m and m.group(1).strip():
                    model = m.group(1).strip()
except Exception:
    sys.exit(0)

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
hits = [name for name, rx in SIGNALS if re.search(rx, prompt)]
doc = "knowledges/模型分工規則_Opus與Sonnet.md"

if not high and hits and not said_up:
    print("🧭 模型分工評估（%s）：目前是 %s，這句命中 Opus 級訊號：%s。" % (doc, model or "非Opus", "、".join(hits)))
    print("先判斷是不是真的 Opus 級（找根因／多系統／不可逆／設計機制／教練不滿／重要對外）：")
    print("→ 是：這則回覆只講一句提醒＋一句理由，先不動手：「教練，我認為這個任務適合讓 Opus 等級來解決，可能會節省您的時間（理由：…）。要我直接用 Sonnet 做，回『直接做』就好。」")
    print("→ 否（只是字面碰到關鍵字）：完全不提，照常做。")
elif high and not hits and not said_down:
    print("🧭 模型分工評估（%s）：目前是 %s。若這句是交辦一件庶務（查資料／照SOP上架／改字／例行），照常做完，最後一行加：「這件是一般庶務，下一件可以切回 Sonnet 省流量。」本對話框只講一次；若是重大決策、找根因、閒聊或道謝就不提。" % (doc, model))
' 2>/dev/null
exit 0
