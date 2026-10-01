#!/usr/bin/env python3
"""Top 30 條件反射報告產生器（2026-10-02）

資料來源（唯一真相源，不手改報告）：
  state/top30_evidence_ids.json   30 個主題、各自的教練重講原話編號、人工判斷的準確度
  knowledges/反射索引.json         每條反射的時刻、刺激、要做什麼
  state/coach_corpus.jsonl        教練原話庫（算每月「重講」比例當量尺）
輸出：knowledges/2026-10-02_Top30條件反射報告.md（給 AI／系統）＋ .html（給教練看）
用法：python3 scripts/render_top30_report.py
"""
import html
import json
import os
import re
import time
from collections import Counter

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = json.load(open(os.path.join(WS, "state/top30_evidence_ids.json"), encoding="utf-8"))
IDX = {r["id"]: r for r in json.load(open(os.path.join(WS, "knowledges/反射索引.json"), encoding="utf-8"))["reflexes"]}
OUT = os.path.join(WS, "knowledges/2026-10-02_Top30條件反射報告")
MOMENT = {"prompt": "教練說話時", "pre_tool": "AI 動手前", "post_tool": "AI 看到結果時", "reply": "AI 回話前",
          "guard": "已有程式擋", "judgment": "判斷類"}
NEW_TODAY = {"R-DEPLOY-WORDS", "R-CURATION-SOP", "R-INVOICE", "R-MEMBER-DB", "R-CROSS-LETTER", "R-HERMES",
             "R-FRIEND-AGENT", "R-SEARCH-HISTORY-FIRST", "R-COPY-EXACT", "R-DOWNLOADS", "R-SHOW-NOT-DO",
             "R-PLAIN-TALK", "R-FB-POST", "R-WEB-EDIT-BASELINE", "R-POLLING-CODE", "R-OPENCLAW-CONFIG",
             "R-DATE-WEEKDAY", "R-CHROME-WHICH-MACHINE", "R-NOTIFY-COACH-NOISE", "R-LETTER-INBOX",
             "R-ASK-CREDENTIAL", "R-PROMISE-MONITOR", "R-COMMAND-FOR-COACH"}

# 量尺：每月教練訊息裡帶「重講訊號」的比例（與挑出 587 則時同一套規則）
REP = re.compile(r"又|再一次|再次|講過|說過|講了(幾|很多|多少|好幾)|說了(幾|很多|多少|好幾)|第[一二三四五六七八九十兩幾\d]+次|老是|每次都|每一次都|一直(都|在|沒|是|犯|忘|問|叫|要)|不是(說|講|跟你)|忘了|忘記|還是(沒|一樣|不)|同樣的(錯|問題|事)|重複|一再|多少次|不要再|別再|又來|早就(說|講|跟)|講幾遍|說幾遍|提醒過|交代過|教過你|跟你說過|我說的是|聽不懂|搞錯|弄錯|怎麼會|為什麼(沒有|又|不|還)")
YOU = re.compile(r"又(犯|錯|忘|來|問|叫|沒|是|搞|弄|出現|發生|再|一次|跑|重複|要我|把|在)")


def monthly_ratio():
    tot, rep = Counter(), Counter()
    for line in open(os.path.join(WS, "state/coach_corpus.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        m = r["t"][:7]
        tot[m] += 1
        hits = REP.findall(r["text"])
        if hits and not (all(h == "又" for h in hits) and not YOU.search(r["text"])):
            rep[m] += 1
    this_month = time.strftime("%Y-%m")  # 還沒過完的月份不列，免得兩天的數字誤導
    return [(m, rep[m], tot[m]) for m in sorted(tot) if tot[m] >= 50 and m != this_month]


def theme_rows():
    acc = EV["accuracy"]
    rows = []
    for t in EV["themes"]:
        rs = [IDX[x] for x in t["reflexes"] if x in IDX]
        main = rs[0]
        moments = "、".join(dict.fromkeys(MOMENT[r["moment"]] for r in rs))
        a = next((acc[r["id"]] for r in rs if r["id"] in acc), None)
        if any(r["id"] in NEW_TODAY for r in rs):
            status = "🆕 新反射"
        elif all(r["moment"] in ("guard", "judgment") for r in rs):
            status = "🔒 既有程式在擋"
        else:
            status = "🔧 已修準"
        rows.append({"rank": t["rank"], "title": t["title"], "kind": t["kind"], "n": len(t["ids"]),
                     "cases": len(t.get("cases", [])), "moments": moments, "say": main["say"],
                     "precision": a["precision"] if a else "—", "recall": a["recall"] if a else "—",
                     "note": a["note"] if a else "", "status": status,
                     "ids": ", ".join(r["id"] for r in rs)})
    return rows


SUMMARY = [
    "讀了什麼：教練 4～10 月的原話 4,092 則。其中帶「又、講過、第 N 次、老是…」的重講訊息 587 則，我一則一則讀完、歸類；另外對照試金石 76 案標題、記憶索引。",
    "結果：最常重講的 30 件事，就佔了全部重講訊息的一半（294／587）。",
    "做了什麼：新增 23 條反射、修準 7 條舊的，全部拿 7～10 月的真實紀錄回測（AI 動手 39,091 次、回話 2,461 輪、教練原話 4,092 則），誤跳的地方都修過。另有 10 件事本來就有程式在擋，登記進來一起管。",
]
PROOF = [
    "7/16 寫進「大樹小講」網頁的「9/15（六）」其實是星期二。教練 7/24 才自己抓到；現在寫進去的那一刻，系統就會說「應該是星期二」。",
    "案例 97 通知網址黏著括號，教練點了十幾二十次打不開。9/24、9/30 寫那段程式的那一刻，現在就會跳出提醒。",
    "AI 回話時網址後面黏中文標點，7～10 月真的犯過 21 次。現在回話前就擋下，網址單獨一行。",
]
LIMITS = [
    "準確度是每條抽 8～10 次、我逐筆判斷，不是全部；「無資料」代表歷史上沒發生過，暫時驗不了。",
    "抓到率只算「教練說話時」那種：拿教練重講的原話去試。推送、身分這類主題，教練抱怨時不會講到那些字，所以不算抓到率。",
    "AI 回話前只能「擋下重寫」，不能只提醒；所以「不要問我」「講白話」這種要判斷的事，主要靠原本的回話檢查＋教練說話時的提醒。",
    "教練貼 AI 的長文進來時，裡面的字也會被當成教練說的，少數會誤跳（常見格式已排除）。",
    "目前只在 Mac（桌面版、終端機）和雲端工作頁生效；聯想、宏碁還沒接上。",
]
NEXT = [
    "第 3 步：Top 30 以外的試金石案例和記憶，逐案補成反射；把舊的通用提醒（trigger_index）收進來，拿掉重複的。",
    "量尺：教練訊息裡「重講」的比例，每週看一次有沒有往下降。",
    "聯想、宏碁接上反射和開工置頂交辦：要寫信過去（跨機鎖要教練同意），信已寫好草稿。",
]


def render_md(rows, ratio):
    out = ["# Top 30 條件反射報告（2026-10-02，Mac 桌面版 Opus 5.5）", "",
           "> 本檔由 `scripts/render_top30_report.py` 產生，不要手改；資料在 `state/top30_evidence_ids.json`、`knowledges/反射索引.json`。", ""]
    out += ["## 一句話", ""] + [f"- {s}" for s in SUMMARY] + ["", "## 會早一步擋下的真實例子", ""]
    out += [f"{i}. {s}" for i, s in enumerate(PROOF, 1)]
    out += ["", "## 量尺起點：教練訊息裡「重講」的比例", "", "| 月份 | 重講則數 | 全部則數 | 比例 |", "|---|---|---|---|"]
    out += [f"| {m} | {r} | {t} | {r / t:.0%} |" for m, r, t in ratio]
    out += ["", "## Top 30", "", "| 名次 | 教練常講的事 | 類型 | 重講次數 | 試金石 | 什麼時候跳 | 準確度 | 抓到率 | 狀態 | 反射 |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    out += [f"| {r['rank']} | {r['title']} | {r['kind']} | {r['n']} | {r['cases']} | {r['moments']} | {r['precision']} | {r['recall']} | {r['status']} | `{r['ids']}` |" for r in rows]
    out += ["", "## 說真話（限制）", ""] + [f"- {s}" for s in LIMITS] + ["", "## 下一步", ""] + [f"- {s}" for s in NEXT]
    out += ["", "## 怎麼重跑", "", "```bash", "python3 scripts/build_coach_corpus.py", "python3 scripts/reflex_backtest.py extract",
            "python3 scripts/reflex_backtest.py run", "python3 scripts/render_top30_report.py", "```", ""]
    open(OUT + ".md", "w", encoding="utf-8").write("\n".join(out))


def render_html(rows, ratio):
    e = html.escape
    peak = max(r / t for _, r, t in ratio)
    bars = "".join(
        f'<div class="bar"><span class="m">{e(m[5:])} 月</span><span class="track"><span class="fill" style="width:{(r / t) / peak * 100:.0f}%"></span></span><span class="v">{r / t:.0%}</span></div>'
        for m, r, t in ratio)
    cards = []
    for r in rows:
        note = f'<p class="note">{e(r["note"])}</p>' if r["note"] else ""
        recall = f'<span>抓到率 <b>{e(r["recall"])}</b></span>' if r["recall"] not in ("—", "") else ""
        cards.append(f'''<article class="card">
  <div class="rank">{r["rank"]}</div>
  <div class="body">
    <h3>{e(r["title"])}</h3>
    <div class="chips"><span class="chip {'need' if r['kind'] == '需求型' else 'guard'}">{e(r["kind"])}</span><span class="chip">重講 {r["n"]} 次</span><span class="chip">{e(r["moments"])}</span><span class="chip st">{e(r["status"])}</span></div>
    <p class="say">{e(r["say"])}</p>
    <div class="nums"><span>準確度 <b>{e(r["precision"])}</b></span>{recall}</div>
    {note}
  </div>
</article>''')
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    page = f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Top 30 條件反射</title>
<style>
:root{{--bg:#f7f5f0;--card:#fff;--ink:#1f2328;--muted:#5d6470;--line:#e4e0d8;--accent:#b4532a;--need:#2f6f4f;--guard:#8a4b9a;--fill:#b4532a}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16181c;--card:#1f2228;--ink:#e8e6e1;--muted:#a3a8b1;--line:#30343b;--accent:#e08a5f;--need:#6fbf95;--guard:#c49ad1;--fill:#e08a5f}}}}
:root[data-theme="dark"]{{--bg:#16181c;--card:#1f2228;--ink:#e8e6e1;--muted:#a3a8b1;--line:#30343b;--accent:#e08a5f;--need:#6fbf95;--guard:#c49ad1;--fill:#e08a5f}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.7 -apple-system,"PingFang TC","Noto Sans TC",sans-serif}}
main{{max-width:860px;margin:0 auto;padding:28px 16px 60px}}
h1{{font-size:28px;line-height:1.3;margin:0 0 6px}}.sub{{color:var(--muted);margin:0 0 22px;font-size:15px}}
h2{{font-size:20px;margin:34px 0 12px;padding-left:10px;border-left:4px solid var(--accent)}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px}}
.box ul,.box ol{{margin:0;padding-left:20px}}.box li{{margin:6px 0}}
.bar{{display:grid;grid-template-columns:44px 1fr 46px;gap:10px;align-items:center;margin:6px 0;font-size:15px}}
.track{{height:12px;background:var(--line);border-radius:6px;overflow:hidden}}.fill{{display:block;height:100%;background:var(--fill)}}
.v{{text-align:right;font-variant-numeric:tabular-nums}}.m{{color:var(--muted)}}
.card{{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:10px 0}}
.rank{{flex:0 0 38px;height:38px;border-radius:50%;background:var(--accent);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center}}
.body{{min-width:0;flex:1}}.card h3{{font-size:18px;margin:4px 0 6px;line-height:1.4}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}}.chip{{font-size:13px;padding:2px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}}
.chip.need{{color:var(--need);border-color:var(--need)}}.chip.guard{{color:var(--guard);border-color:var(--guard)}}
.say{{margin:6px 0;font-size:16px}}.nums{{display:flex;gap:16px;flex-wrap:wrap;font-size:15px;color:var(--muted)}}.nums b{{color:var(--ink)}}
.note{{margin:6px 0 0;font-size:14px;color:var(--muted)}}
</style></head><body><main>
<h1>Top 30 條件反射</h1>
<p class="sub">教練最常重講的 30 件事：看到什麼就自動提醒、做什麼　｜　2026-10-02　Mac 桌面版 Opus 5.5</p>
<h2>一句話</h2><div class="box"><ul>{li(SUMMARY)}</ul></div>
<h2>會早一步擋下的真實例子</h2><div class="box"><ol>{li(PROOF)}</ol></div>
<h2>量尺：教練訊息裡「重講」的比例</h2><div class="box">{bars}<p class="note">之後每週看這條線有沒有往下降。10 月只有 2 天，先不列。</p></div>
<h2>Top 30</h2>
{''.join(cards)}
<h2>說真話（限制）</h2><div class="box"><ul>{li(LIMITS)}</ul></div>
<h2>下一步</h2><div class="box"><ul>{li(NEXT)}</ul></div>
</main></body></html>'''
    open(OUT + ".html", "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    rows, ratio = theme_rows(), monthly_ratio()
    render_md(rows, ratio)
    render_html(rows, ratio)
    print(f"{OUT}.md／.html：{len(rows)} 項，量尺 {[(m, f'{r / t:.0%}') for m, r, t in ratio]}")
