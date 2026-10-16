#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
教練親口提醒守則的次數（成效唯一指標，2026-10-17 教練選定方案 C 第 3 項）

來源：memory/verbatim/2026-*.jsonl（教練每句話逐字存檔，欄位 t／src／who／text，只算 who=教練）
定義：教練「這句話在糾正／提醒 AI 沒照做」——句子層級比對強語氣句型，一句話最多算一次。
      定義固定不改（改了週與週就不能比），要調整先在這裡改 PATTERNS 並重算基線。
排除：超過 2000 字的整段貼上、以框線／程式碼開頭的貼上內容（那是貼進來的材料，不是教練在提醒）。

用法：
  python3 rules_reminder_count.py            # 一行成績（給開工注入）
  python3 rules_reminder_count.py --weekly   # 每週次數表（基線）
  python3 rules_reminder_count.py --samples 2026-10-12   # 列出某日之後命中的句子（檢查有沒有誤抓）
壞了就印空（開工注入不能被它拖垮）。
"""
import sys, os, re, json, glob
from datetime import datetime, timedelta

WORKSPACE = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace")
VERBATIM = os.path.join(WORKSPACE, "memory", "verbatim", "2026-*.jsonl")
LEDGER = os.path.join(WORKSPACE, "distill", "rules_reviewer_ledger.jsonl")

PATTERNS = [
    r"說過了|講過了|說過多少次|講過多少次|提醒過|交代過|跟你說過|不是說過|不是跟你說|不是告訴過|不是有說",
    r"你又(?:忘|犯|來|沒|是|把|在|搞)|怎麼又|又忘了|又犯|毛病又犯|同樣的錯|同一個錯|同一個地方|第二次(?:了|犯)|不是有默契|沒有默契",
    r"我不是(?:說|跟你說|告訴)|我(?:之前|上次|早就|剛剛|剛才)(?:就)?(?:說|講|提|交代)過|怎麼還(?:是|在)|一直犯|老是犯|有沒有(?:照|遵守|遵循|對照).{0,4}守則",
    r"守則.{0,12}(?:違反|沒照|沒遵守|沒有遵守|沒遵循|沒有遵循|忘了|沒做到|沒有做到)|(?:違反|沒照|沒遵守|忘了|沒遵循).{0,6}守則",
]
RE = [re.compile(p) for p in PATTERNS]
# 系統回饋被逐字存檔誤收成教練的話（Stop hook feedback、守則提醒原文、時間鐵律、模型分工亮燈要求等）
HOOK_ECHO = re.compile(r"Stop hook feedback|UserPromptSubmit|PreToolUse|system-reminder|📜|🌱|🚨|🧭|🔍|⚡|請補一則回覆|守則#\d+\s*原文|條件反射")
SPLIT = re.compile(r"[。！？!?\n]")


def load():
    out = []
    for f in sorted(glob.glob(VERBATIM)):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("who") != "教練":
                    continue
                t, text = r.get("t", ""), (r.get("text") or "")
                if len(text) > 2000 or text.lstrip()[:1] in "┌│├└─═║{[<`#|":
                    continue
                if HOOK_ECHO.search(text):
                    continue  # 系統 hook 回饋／提醒被存成「教練的話」，不是教練親口說的
                try:
                    dt = datetime.strptime(t[:16], "%Y-%m-%d %H:%M")
                except ValueError:
                    continue
                hit = None
                for s in SPLIT.split(text):
                    if any(p.search(s) for p in RE):
                        hit = s.strip()
                        break
                if hit:
                    out.append((dt, hit))
    return out


def monday(dt):
    d = dt.date()
    return d - timedelta(days=d.weekday())


def ledger_counts(since):
    c, n = {}, 0
    if not os.path.isfile(LEDGER):
        return c, n
    for line in open(LEDGER, encoding="utf-8"):
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("session", "").startswith("test"):
            continue  # 實測用的假 session 不算
        if (r.get("t") or "") < since:
            continue
        n += 1
        if r.get("rule") is not None:
            k = "#%02d" % int(r["rule"]) if str(r["rule"]).isdigit() else "#%s" % r["rule"]
            c[k] = c.get(k, 0) + 1
    return c, n


def main():
    hits = load()
    this_mon = monday(datetime.now())
    last_mon = this_mon - timedelta(days=7)
    wk = {}
    for dt, _ in hits:
        wk[monday(dt)] = wk.get(monday(dt), 0) + 1
    if "--weekly" in sys.argv:
        for m in sorted(wk):
            print("%s 起那週：%d 次 %s" % (m, wk[m], "█" * wk[m]))
        print("合計 %d 次（%d 週有紀錄）" % (sum(wk.values()), len(wk)))
        return
    if "--samples" in sys.argv:
        since = sys.argv[sys.argv.index("--samples") + 1]
        for dt, s in hits:
            if dt.strftime("%Y-%m-%d") >= since:
                print(dt.strftime("%m-%d %H:%M"), s[:100])
        return
    lc, ln = ledger_counts(this_mon.strftime("%Y-%m-%d"))
    parts = "、".join("%s %d" % (k, v) for k, v in sorted(lc.items(), key=lambda x: -x[1])[:4]) or "尚無"
    print("📊 守則成績：教練親口提醒 上週 %d 次、本週 %d 次（越少越好；週一起算）｜審查員本週記錄違規 %d 筆（%s）" % (
        wk.get(last_mon, 0), wk.get(this_mon, 0), sum(lc.values()), parts))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
