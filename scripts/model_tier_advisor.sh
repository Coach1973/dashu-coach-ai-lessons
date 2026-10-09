#!/bin/bash
# Hook：UserPromptSubmit
# 用途：模型分工亮燈（v3 三燈號，2026-10-09 教練親定；規則全文 knowledges/模型分工規則_Opus與Sonnet.md）
#   教練每丟一則交辦（含天馬行空的新點子），不管現在哪個模型，回覆第一行都要亮燈：
#   「🔵 這件 Haiku 就能做」「🟢 這件 Sonnet 就能做」「🟣 這件是 Opus 等級（理由）」。
#   模型等級不夠 → 先建議切換、先不動手；做到一半卡關 → 停下建議往上切。
#   亮燈有沒有做到，由 stop_rules_master.py 的 A3 檢查擋下補上。
# 模型判斷：hook 輸入若有 model 欄位就用它；否則看對話紀錄最後一則回覆的 model 與最後一次 /model。
#   注意：送出前剛用 /model 切換時，切換紀錄寫進對話檔比 hook 執行晚，這裡會看到舊模型
#   （2026-10-09 查證），所以提示裡明講「以你系統提示的模型為準」。
INPUT=$(cat)
printf '%s' "$INPUT" | /usr/bin/python3 -c '
import json, re, sys, os
d = json.load(sys.stdin)
prompt = (d.get("prompt") or "").strip()
tp = d.get("transcript_path") or ""

# 存下 hook 輸入有哪些欄位（不存教練原話），日後 Claude Code 若直接提供模型欄位就能發現
try:
    st = "/Users/bymyway/.openclaw/workspace/state/model_tier_advisor_last_input.json"
    json.dump({k: (v if isinstance(v, (str, int, float, bool)) and k != "prompt" else type(v).__name__)
               for k, v in d.items()}, open(st, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
except Exception:
    pass

if len(prompt) < 15:
    sys.exit(0)

model = ""
mv = d.get("model")
if isinstance(mv, dict):
    mv = mv.get("id") or mv.get("display_name") or ""
if isinstance(mv, str) and mv:
    model = mv
else:
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

OPUS = [
    ("找根因", r"為什麼.{0,30}(會|不會|又|只有|偏偏)|根源|根本原因|徹底|復發|又壞|又出現|還是沒|一直沒|反覆|老是|每次都|繞一大圈"),
    ("多系統", r"架構|整合|串接|全面|體檢|盤點|遷移|搬家|跨機|同步機制"),
    ("不可逆", r"刪除|刪掉|清掉|砍掉|重灌|金鑰|外洩|付費|花錢|合約|報價|退版"),
    ("設計機制", r"設計|規劃|策略|企劃|機制|制度|(新|建立|寫|改|訂)(一個|一份|成)?(SOP|規則|流程)"),
    ("教練不滿", r"浪費|搞不懂|很蠢|又犯|同樣的錯|受不了|講過|說過了|不 ?OK|不滿意|偷工減料|不是我要的|問那麼多"),
    ("重要對外", r"對外|公告|新聞稿|提案書"),
]
HAIKU = r"戰報|戰情|儀表板|套版|套底圖|BNI ?PPT|策展|上架|大樹作品|籌備會|例會|名單|行事曆|[Cc]alendar|日曆|發票|開票|名片"
o_hits = [n for n, rx in OPUS if re.search(rx, prompt)]
h_hits = sorted(set(re.findall(HAIKU, prompt)))
stuck = re.search(r"還是不行|還是沒|還是一樣|又沒|沒用|沒解決|一樣的問題|不對啊|怎麼又", prompt)

hint = []
if h_hits:
    hint.append("像固定 SOP（%s）→ 可能 🔵" % "、".join(h_hits))
if o_hits:
    hint.append("碰到 Opus 訊號（%s）→ 可能 🟣" % "、".join(o_hits))

out = [
    "🧭 模型分工亮燈（knowledges/模型分工規則_Opus與Sonnet.md）：hook 看到的模型是 %s——只供參考，以你系統提示寫的模型為準（教練剛用 /model 切換時，這裡會是舊的）。" % (model or "未知"),
    "回覆第一行必須亮燈：「🔵 這件 Haiku 就能做」／「🟢 這件 Sonnet 就能做」／「🟣 這件是 Opus 等級（理由：…）」。閒聊、道謝寫「🔵 閒聊」。",
    ("關鍵字初判：%s（字面碰到不算，最後由你判斷）。" % "；".join(hint)) if hint
    else "關鍵字初判沒命中：已有 SOP 的固定動作是 🔵；明確但沒 SOP 是 🟢；要設計、跨系統、不可逆、找根因是 🟣。",
    "🔵 的前提是照 SOP 走得通：SOP 出錯或要想新做法 → 升 🟢；要找原因、多系統、不可逆、教練不滿 → 升 🟣。",
]
if "直接做" in prompt:
    out.append("教練說「直接做」：用目前模型照常做，亮燈後直接開始。")
else:
    out.append("亮燈後：你是 Haiku → 遇 🟢 只加一句「教練，建議切換到 Sonnet 5.5 再做；要用目前模型直接做，回『直接做』」，遇 🟣 只加一句「教練，建議切換到 Opus 5.5 再做，可能會節省您的時間；要用目前模型直接做，回『直接做』」，都先不動手。"
               "你是 Sonnet → 遇 🟣 同樣建議切 Opus、先不動手；遇 🔵 照做，第一行補「下一件可以切到 Haiku 省流量」。"
               "你是 Opus → 遇 🔵／🟢 照做完，第一行補「下一件可以切到 Haiku／切回 Sonnet 省流量」。")
out.append("做到一半卡關（兩種方法都沒解決、找不到原因）：立刻停下，說「教練，我卡關了，建議切換到 ○○ 接手」＋卡在哪一句（Haiku 卡關建議 Sonnet，要找根因就建議 Opus；Sonnet 卡關建議 Opus）。")
if stuck:
    out.append("⚠️ 教練這句表示上一步沒解決＝卡關訊號，優先建議往上切。")
print("\n".join(out))
' 2>/dev/null
exit 0
