#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""賈維斯成績單（2026-10-30 教練拍板：四步內在循環的第四步「自我觸發」）

每週一 08:10 由每日點名（daily_team_rollcall.py）呼叫一次，算四個數字，比「上週」對「上上週」：
  ① 教練親口糾正次數   — 沿用 rules_reminder_count.py 的定義（逐字保險箱、只算教練）
  ② 試金石新案例數     — 試金石_案例庫.md 每案開頭第一個日期落在那一週
  ③ 同類重犯案例數     — 上面那些案例裡，內文寫到「同類／復發／同處跌倒／第 N 次…」的
  ④ 常駐規則總字數     — 跟 rules_health_audit.py 同一套量法（心法＋細則＋兩份 CLAUDE.md＋反射索引），現在對一週前
任一項變差（比前一週多；字數比一週前多）→ 加 --trigger 時自動在背景跑一次 jarvis-self-optimize（同一週只跑一次）。
另外：逐字保險箱那週收不到教練的話＝①不可信，也算變差（沉默不是平安，案例136）。

定義固定不改（改了週與週就不能比）；要調整先改這裡的 REPEAT 並在報告註明。

用法：
  python3 jarvis_scorecard.py            # 印成績單幾行（點名訊息用）
  python3 jarvis_scorecard.py --json     # 印完整數字
  python3 jarvis_scorecard.py --trigger  # 印成績單；變差就啟動背景體檢
"""
import sys, os, re, json, glob, importlib.util, subprocess
from datetime import datetime, timedelta

WS = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace")
SCRIPTS = os.path.join(WS, "scripts")
CASEBOOK = os.path.join(WS, "試金石", "試金石_案例庫.md")
RULES_HISTORY = os.path.join(WS, "state", "rules_health_history.jsonl")
HISTORY = os.path.join(WS, "state", "jarvis_scorecard_history.jsonl")
TRIGGERED = os.path.join(WS, "state", "jarvis_scorecard_triggered.json")
TRIGGER_SH = os.path.join(SCRIPTS, "jarvis_scorecard_trigger.sh")

CASE_HEAD = re.compile(r"^## 案例\s*(\d+)", re.M)
DATE = re.compile(r"(20\d\d)[-/.](\d{1,2})[-/.](\d{1,2})")
REPEAT = re.compile(r"同類|同一類|復發|同處跌倒|再犯|又犯|第\s*[二三四五六七八九十2-9]\s*次")
# 「同類再犯就升級…」是寫給未來的條件句，不是這次重犯（2026-11-02 案例137 被誤算）；比對前先拿掉
NOT_REPEAT = re.compile(r"(?:若|如果|如)?(?:同類|同一類)?再犯(?:就|時|的話|要)")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SCRIPTS, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def weeks(now):
    mon = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    return (mon - timedelta(days=7), mon), (mon - timedelta(days=14), mon - timedelta(days=7))


def inside(dt, rng):
    return rng[0] <= dt < rng[1]


def corrections(w, p):
    hits = _load("rules_reminder_count").load()
    return sum(inside(d, w) for d, _ in hits), sum(inside(d, p) for d, _ in hits)


def coach_lines(rng):
    """那週逐字保險箱收到教練幾句（0＝收集壞了，糾正次數不可信）"""
    n = 0
    for f in glob.glob(os.path.join(WS, "memory", "verbatim", "2026-*.jsonl")):
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
                if r.get("who") == "教練" and inside(datetime.strptime(r.get("t", "")[:16], "%Y-%m-%d %H:%M"), rng):
                    n += 1
            except Exception:
                continue
    return n


def cases():
    text = open(CASEBOOK, encoding="utf-8").read()
    heads = list(CASE_HEAD.finditer(text))
    out, undated = [], []
    for i, h in enumerate(heads):
        body = text[h.start(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        m = DATE.search(body[:600])
        try:
            dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except (AttributeError, ValueError):
            undated.append(int(h.group(1)))
            continue
        out.append((int(h.group(1)), dt, bool(REPEAT.search(NOT_REPEAT.sub("", body)))))
    newest = max([n for n, _, _ in out] + undated + [0])
    return out, [n for n in undated if n > newest - 20]  # 最新 20 案裡沒寫日期的會被漏算，要標出來


def rule_chars(now):
    audit = _load("rules_health_audit")
    cur = sum(len(t) for t in audit.load_rules().values())
    base, base_t = None, None
    cutoff = (now - timedelta(days=7)).strftime("%Y-%m-%d %H:%M")
    try:
        for l in open(RULES_HISTORY, encoding="utf-8"):
            r = json.loads(l)
            if r.get("t", "") <= cutoff or base is None:
                base, base_t = r.get("total_chars"), r.get("t")
    except Exception:
        pass
    return cur, base, base_t


def scorecard(now=None):
    now = now or datetime.now()
    w, p = weeks(now)
    c_w, c_p = corrections(w, p)
    cs, undated = cases()
    new_w = [n for n, d, _ in cs if inside(d, w)]
    new_p = [n for n, d, _ in cs if inside(d, p)]
    rep_w = [n for n, d, r in cs if r and inside(d, w)]
    rep_p = [n for n, d, r in cs if r and inside(d, p)]
    chars, base, base_t = rule_chars(now)
    heard = coach_lines(w)
    worse = []
    if heard == 0:
        worse.append("逐字保險箱上週收到教練 0 句（糾正次數不可信）")
    if c_w > c_p:
        worse.append("教練親口糾正 %d→%d" % (c_p, c_w))
    if len(new_w) > len(new_p):
        worse.append("新案例 %d→%d" % (len(new_p), len(new_w)))
    if len(rep_w) > len(rep_p):
        worse.append("同類重犯 %d→%d" % (len(rep_p), len(rep_w)))
    if base is not None and chars > base:
        worse.append("規則總字數 %s→%s（+%s）" % (format(base, ","), format(chars, ","), format(chars - base, ",")))
    return {
        "t": now.strftime("%Y-%m-%d %H:%M"),
        "week": w[0].strftime("%Y-%m-%d"), "prev_week": p[0].strftime("%Y-%m-%d"),
        "corrections": [c_p, c_w], "coach_lines": heard,
        "new_cases": [new_p, new_w], "repeat_cases": [rep_p, rep_w],
        "rule_chars": [base, chars], "rule_chars_base_t": base_t,
        "undated_cases": undated, "worse": worse,
    }


def arrow(a, b):
    return "↑變差" if b > a else ("↓進步" if b < a else "持平")


def lines(s):
    (cp, cw), (np_, nw), (rp, rw), (b, c) = s["corrections"], s["new_cases"], s["repeat_cases"], s["rule_chars"]
    md = lambda d: d[5:].replace("-", "/")
    out = ["📈 賈維斯成績單（上週 %s 起，對上上週 %s 起）" % (md(s["week"]), md(s["prev_week"])),
           "① 教練親口糾正：%d → %d 次（%s）" % (cp, cw, arrow(cp, cw)),
           "② 試金石新案例：%d → %d 案（%s）%s" % (len(np_), len(nw), arrow(len(np_), len(nw)),
                                         "　案例" + "、".join(map(str, nw)) if nw else ""),
           "③ 同類重犯：%d → %d 案（%s）%s" % (len(rp), len(rw), arrow(len(rp), len(rw)),
                                       "　案例" + "、".join(map(str, rw)) if rw else ""),
           "④ 規則總字數：%s → %s 字（%s）" % (format(b, ",") if b is not None else "無紀錄", format(c, ","),
                                        arrow(b, c) if b is not None else "第一次記錄")]
    if s["coach_lines"] == 0:
        out.append("⚠️ 逐字保險箱上週收到教練 0 句，①的數字不可信")
    if s["undated_cases"]:
        out.append("⚠️ 案例" + "、".join(map(str, s["undated_cases"])) + " 沒寫日期，②③沒算到（軍師補日期）")
    return out


def trigger(s):
    """變差就在背景跑一次體檢；同一週只跑一次。回傳一行狀態。"""
    if not s["worse"]:
        return "✅ 四項都沒變差，本週不用體檢"
    try:
        done = json.load(open(TRIGGERED, encoding="utf-8"))
    except Exception:
        done = {}
    if done.get("week") == s["week"]:
        return "🔁 本週已經自動體檢過（%s），不重跑" % done.get("t", "")
    subprocess.Popen(["/bin/bash", TRIGGER_SH, "；".join(s["worse"])],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
    with open(TRIGGERED, "w", encoding="utf-8") as f:
        json.dump({"week": s["week"], "t": s["t"], "why": s["worse"]}, f, ensure_ascii=False)
    return "🤖 變差：%s → 已自動開始跑賈維斯體檢，做完報告會直接傳給教練" % "；".join(s["worse"])


def main():
    s = scorecard()
    if "--json" in sys.argv:
        print(json.dumps(s, ensure_ascii=False, indent=1))
        return
    out = lines(s)
    if "--trigger" in sys.argv:
        out.append(trigger(s))
        try:
            with open(HISTORY, "a", encoding="utf-8") as f:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        except Exception:
            pass
    elif s["worse"]:
        out.append("（變差：%s；測試模式不啟動體檢）" % "；".join(s["worse"]))
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("📈 賈維斯成績單：程式出錯（%s: %s），叫軍師查 scripts/jarvis_scorecard.py" % (type(e).__name__, e))
