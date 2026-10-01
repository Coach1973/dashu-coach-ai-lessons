#!/usr/bin/env python3
"""條件反射回測（2026-10-02，Top 30 用）

拿歷史資料重播 knowledges/反射索引.json 的每一條反射，算「會跳幾次、跳的是不是對的」：
  prompt    → state/coach_corpus.jsonl（教練原話，先跑 build_coach_corpus.py）
  pre_tool  → 所有對話紀錄裡 AI 真的下過的指令／改過的檔
  post_tool → 同上，配對到的工具結果
  reply     → 所有對話紀錄裡 AI 每一輪回給教練的話

用法：
  python3 scripts/reflex_backtest.py extract           # 從 ~/.claude/projects/*/*.jsonl 抽資料（快取，含指令原文，不進 git）
  python3 scripts/reflex_backtest.py run [id ...]      # 回測，印出每條命中數與抽樣
  python3 scripts/reflex_backtest.py run --json OUT    # 另存結果給報告用
比對規則與 reflex_router.py 相同（同一個 text_for／strip_code），回測結果才代表上線行為。
"""
import glob
import json
import os
import random
import re
import sys
from collections import Counter

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WS, "scripts"))
import reflex_router as rr  # noqa: E402

CACHE = os.path.join(WS, "state/reflex_backtest")
TOOLS = os.path.join(CACHE, "tool_events.jsonl")
REPLIES = os.path.join(CACHE, "replies.jsonl")
CORPUS = os.path.join(WS, "state/coach_corpus.jsonl")
CAP = 6000  # 每筆內容上限（頭尾各半），控制快取大小


def clip(s):
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False)
    return s if len(s) <= CAP else s[:CAP // 2] + "\n…\n" + s[-CAP // 2:]


def result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(x.get("text", "") for x in content if isinstance(x, dict) and x.get("type") == "text")
    return ""


def is_real_prompt(d):
    if d.get("type") != "user" or d.get("isMeta"):
        return False
    c = d.get("message", {}).get("content")
    if isinstance(c, str):
        return True
    return isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "text" for x in c)


def extract():
    os.makedirs(CACHE, exist_ok=True)
    files = sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")))
    nt = nr = 0
    with open(TOOLS, "w", encoding="utf-8") as ft, open(REPLIES, "w", encoding="utf-8") as fr:
        for f in files:
            pending, turn, turn_ts, sess = {}, [], "", os.path.basename(f)[:8]

            def flush():
                nonlocal nr
                if turn:
                    fr.write(json.dumps({"s": sess, "t": turn_ts, "text": clip("\n".join(turn))}, ensure_ascii=False) + "\n")
                    nr += 1

            for line in open(f, encoding="utf-8", errors="ignore"):
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if is_real_prompt(d):
                    flush()
                    turn, turn_ts = [], d.get("timestamp", "")
                    continue
                c = d.get("message", {}).get("content") if isinstance(d.get("message"), dict) else None
                if not isinstance(c, list):
                    continue
                for x in c:
                    if not isinstance(x, dict):
                        continue
                    if d.get("type") == "assistant" and x.get("type") == "text":
                        turn.append(x.get("text", ""))
                    elif d.get("type") == "assistant" and x.get("type") == "tool_use":
                        ti = x.get("input") or {}
                        keep = {k: clip(ti[k]) for k in ("command", "file_path", "path", "url", "content", "new_string") if k in ti}
                        pending[x.get("id")] = {"s": sess, "t": d.get("timestamp", ""), "tool": x.get("name", ""), "input": keep}
                    elif d.get("type") == "user" and x.get("type") == "tool_result":
                        ev = pending.pop(x.get("tool_use_id"), None)
                        if ev:
                            ev["result"] = clip(result_text(x.get("content")))
                            ft.write(json.dumps(ev, ensure_ascii=False) + "\n")
                            nt += 1
            flush()
            for ev in pending.values():  # 沒拿到結果的（被擋下、中斷）也算一次動手
                ev["result"] = ""
                ft.write(json.dumps(ev, ensure_ascii=False) + "\n")
                nt += 1
    print(f"{len(files)} 份對話紀錄 → 工具事件 {nt} 筆、回覆 {nr} 輪（{CACHE}）")


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def text_of(moment, row):
    """跟 reflex_router.text_for 同一套：只是把歷史資料包成 hook 事件的樣子。"""
    if moment == "prompt":
        return row["text"]
    if moment == "reply":
        return rr.strip_code(row["text"])
    evt = {"tool_input": row["input"], "tool_response": row.get("result", "")}
    return rr.text_for(moment, evt)


def run(ids, out_json=None, samples=8, seed=7):
    reflexes = [r for r in json.load(open(rr.INDEX, encoding="utf-8"))["reflexes"]
                if r.get("moment") in ("prompt", "pre_tool", "post_tool", "reply") and (not ids or r["id"] in ids)]
    data = {}
    if any(r["moment"] == "prompt" for r in reflexes):
        data["prompt"] = load(CORPUS)
    if any(r["moment"] in ("pre_tool", "post_tool") for r in reflexes):
        data["tool"] = load(TOOLS)
    if any(r["moment"] == "reply" for r in reflexes):
        data["reply"] = load(REPLIES)
    rnd = random.Random(seed)
    report = []
    for r in reflexes:
        m = r["moment"]
        rows = data["tool" if m in ("pre_tool", "post_tool") else m]
        hits, sessions, months = [], set(), Counter()
        for row in rows:
            if m in ("pre_tool", "post_tool") and r.get("tool") and not re.fullmatch(r["tool"], row["tool"]):
                continue
            txt = text_of(m, row)
            mo = re.search(r["match"], txt or "")
            if not mo:
                continue
            if r.get("check") == "weekday" and not rr.check_weekday(txt):
                continue
            hits.append((row, mo))
            sessions.add(row.get("s", ""))
            months[(row.get("t") or "")[:7]] += 1
        pick = rnd.sample(hits, min(samples, len(hits)))
        ex = []
        for row, mo in pick:
            src = row.get("text") or row["input"].get("command") or row["input"].get("file_path") or ""
            a, b = mo.start(), mo.end()
            ctx = (text_of(m, row) or "")[max(0, a - 60): b + 60].replace("\n", " ")
            ex.append({"t": (row.get("t") or "")[:16], "hit": mo.group(0)[:80], "ctx": ctx, "src": src[:160].replace("\n", " ")})
        item = {"id": r["id"], "moment": m, "level": r.get("level"), "pool": len(rows), "hits": len(hits),
                "sessions": len(sessions), "by_month": dict(sorted(months.items())), "samples": ex}
        report.append(item)
        print(f"\n■ {r['id']}（{m}/{r.get('level')}）命中 {len(hits)}／{len(rows)}，{len(sessions)} 個對話；{dict(sorted(months.items()))}")
        for e in ex:
            print(f"   [{e['t']}] «{e['hit']}» …{e['ctx']}…")
    if out_json:
        json.dump(report, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "extract":
        extract()
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        args = sys.argv[2:]
        out = None
        if "--json" in args:
            i = args.index("--json")
            out = args[i + 1]
            args = args[:i] + args[i + 2:]
        run(args, out)
    else:
        print(__doc__)
