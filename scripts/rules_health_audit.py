#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
規則自動體檢：機械層（2026-10-17 教練 02:26 要求；設計見 knowledges/守則納入賈維斯_研究與方案_2026-10-17.md 第六節）

零額度、只讀、只出報告，不改任何規則檔。四項檢查：
  1 過時：規則檔提到的檔案／腳本／plist 還在不在
  2 重複：同一段文字出現在幾份規則檔（區分「自動鏡像（設計如此）」與「真正重複」）
  3 份量：規則總行數／字數趨勢（寫進 state/rules_health_history.jsonl）
  4 沒必要：反射命中統計（紀錄不到 90 天一律不建議退休）
觸發（事件，不定時）：收工（junshi-shutdown-summary 步驟 1）＋規則檔 commit（.git/hooks/pre-commit，只提醒不擋）。
輸出：distill/rules_health_report.md（一頁內白話）＋ stdout 一行摘要。
鐵則：任何錯誤一律放行（exit 0），絕不擋教練（2026-10-16 教訓）。

用法：python3 rules_health_audit.py [--quiet]（--quiet 只寫報告、不印摘要）
"""
import sys, os, re, json, collections
from datetime import datetime

HOME = os.path.expanduser("~")
W = os.path.join(HOME, ".openclaw", "workspace")
REPORT = os.path.join(W, "distill", "rules_health_report.md")
HISTORY = os.path.join(W, "state", "rules_health_history.jsonl")
HITS = os.path.join(W, "state", "reflex_hits.log")
REFLEX_INDEX = os.path.join(W, "knowledges", "反射索引.json")

RULE_FILES = collections.OrderedDict([
    ("特助心法", os.path.join(W, "特助心法.md")),
    ("執行細則", os.path.join(W, "執行細則.md")),
    ("全域CLAUDE", os.path.join(HOME, ".claude", "CLAUDE.md")),
    ("專案CLAUDE", os.path.join(W, "CLAUDE.md")),
])
# 兩份自動同步腳本把心法與執行細則鏡像進全域 CLAUDE.md：全域 CLAUDE 與這兩份重複是設計如此，不算問題
MIRROR_SOURCES = {"特助心法", "執行細則"}
MIRROR_TARGET = "全域CLAUDE"
HANDOFF_START = "## 🔴 最新接力棒（系統自動鏡像"
HANDOFF_END = "接力棒鏡像結束"

PATH_EXT = r"(?:jsonl|json|sh|py|md|plist|html|ps1|txt|csv)"  # .log 是執行時才產生的檔，不判過時；jsonl 要排在 json 前面
BACKTICK = re.compile(r"`([^`\n]{3,160})`")
BARE_PATH = re.compile(r"(?<![\w/.])((?:scripts|knowledges|distill|state|memory|claude-brain|handoff_archive|試金石|cloud_sync|hooks|agents|~/\.claude|~/\.openclaw)/[^\s`'\"）)」，、；;]+?\.%s)(?![A-Za-z0-9_])" % PATH_EXT)
SKIP_TOKEN = re.compile(r"[*<>$\{\}…]|YYYY|MM-DD|xxx|XXX|<|\bN\b|\.\.\.|^https?:|^-|^\(|例：|\|")
IGNORE_NAMES = {"CLAUDE.md", "SKILL.md", "README.md", "settings.json", "MEMORY.md"}  # 到處都有、不代表單一檔


def read(p):
    try:
        with open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def strip_handoff_mirror(text):
    """workspace/CLAUDE.md 開頭那一大段接力棒鏡像不算規則（每次收工自動換，不是規則份量）"""
    i = text.find(HANDOFF_START)
    if i < 0:
        return text
    j = text.find(HANDOFF_END, i)
    if j < 0:
        return text
    k = text.find("\n", j)
    return text[:i] + text[k + 1:]


def load_rules():
    out = collections.OrderedDict()
    for name, p in RULE_FILES.items():
        t = read(p)
        out[name] = strip_handoff_mirror(t) if name == "專案CLAUDE" else t
    # 反射索引的 say／match 欄位也是規則文字
    try:
        d = json.load(open(REFLEX_INDEX, encoding="utf-8"))
        out["反射索引"] = "\n\n".join((r.get("say") or "") for r in d.get("reflexes", []))
    except Exception:
        out["反射索引"] = ""
    return out


# ───────── 1 過時 ─────────
_index = None


def basename_index():
    global _index
    if _index is not None:
        return _index
    idx = set()
    roots = [W, os.path.join(HOME, ".claude"), os.path.join(HOME, "Library", "LaunchAgents")]
    for r in roots:
        for dp, dn, fn in os.walk(r):
            dn[:] = [d for d in dn if d not in (".git", "node_modules", "__pycache__", "backups_manual", ".venv", "venv")]
            idx.update(fn)
    _index = idx
    return idx


def exists(token):
    tok = token.rstrip(".,:;、。）)」")
    p = os.path.expanduser(tok)
    if os.path.isabs(p):
        return os.path.exists(p)
    for base in (W, os.path.join(HOME, ".openclaw"), os.path.join(W, "scripts"), os.path.join(HOME, ".claude")):
        if os.path.exists(os.path.join(base, p)):
            return True
    if "/" not in tok:  # 只有檔名：全工作區找一次
        return tok in basename_index()
    return False


def extract_paths(text):
    found = set()
    for m in BARE_PATH.finditer(text):
        found.add(m.group(1))
    for m in BACKTICK.finditer(text):
        tok = m.group(1).strip().split()[0] if m.group(1).strip() else ""
        if re.search(r"\.%s$" % PATH_EXT, tok) and not tok.startswith("-"):
            found.add(tok)
    return {t for t in found if not SKIP_TOKEN.search(t) and os.path.basename(t) not in IGNORE_NAMES}


def check_stale(rules):
    dead = collections.defaultdict(set)
    total = set()
    for name, text in rules.items():
        for t in extract_paths(text):
            total.add(t)
            if not exists(t):
                dead[t].add(name)
    return total, dead


# ───────── 2 重複 ─────────
def check_dup(rules):
    """逐行比對（行長 ≥12 字、正規化空白）：守則 21 條在兩份檔措辭略不同（「為什麼重要」vs「為什麼這條守則很重要」），
    整段雜湊看不出來，逐行才抓得到標題與守則本文的重複。"""
    owners = collections.defaultdict(set)
    for name, text in rules.items():
        for line in text.split("\n"):
            norm = re.sub(r"\s+", " ", line).strip()
            if len(norm) >= 12 and not re.fullmatch(r"[-=*_ |:]+", norm):
                owners[norm].add(name)
    mirror_chars, mirror_n = collections.Counter(), collections.Counter()
    real_chars, real_n = collections.Counter(), collections.Counter()
    for norm, names in owners.items():
        if len(names) < 2:
            continue
        srcs = names & MIRROR_SOURCES
        if MIRROR_TARGET in names and srcs:
            for src in srcs:  # 全域 CLAUDE 照抄心法／執行細則：設計如此
                key = frozenset([src, MIRROR_TARGET])
                mirror_chars[key] += len(norm)
                mirror_n[key] += 1
            names = names - {MIRROR_TARGET}
        if len(names) >= 2:  # 剩下仍在兩份以上＝真正重複（例：守則 21 條又寫進專案 CLAUDE.md）
            key = frozenset(names)
            real_chars[key] += len(norm)
            real_n[key] += 1
    return mirror_chars, mirror_n, real_chars, real_n


# ───────── 3 份量 ─────────
def sizes(rules):
    return {n: {"lines": t.count("\n") + 1 if t else 0, "chars": len(t)} for n, t in rules.items()}


def trend(now):
    prev = first = None
    try:
        rows = [json.loads(l) for l in open(HISTORY, encoding="utf-8") if l.strip()]
        if rows:
            first, prev = rows[0], rows[-1]
    except Exception:
        pass
    rec = {"t": datetime.now().strftime("%Y-%m-%d %H:%M"), "sizes": now,
           "total_chars": sum(v["chars"] for v in now.values())}
    if not prev or prev.get("sizes") != now:
        try:
            os.makedirs(os.path.dirname(HISTORY), exist_ok=True)
            with open(HISTORY, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        except Exception:
            pass
    return rec, prev, first


# ───────── 4 沒必要 ─────────
def check_reflex():
    try:
        ids = [r["id"] for r in json.load(open(REFLEX_INDEX, encoding="utf-8"))["reflexes"]]
    except Exception:
        return None
    hits = collections.Counter()
    first_t = None
    if os.path.isfile(HITS):
        for line in open(HITS, encoding="utf-8", errors="ignore"):
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            if first_t is None:
                try:
                    first_t = datetime.strptime(parts[0][:19], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            hits[parts[2]] += 1
    days = (datetime.now() - first_t).days + 1 if first_t else 0
    zero = [i for i in ids if hits[i] == 0]
    gone = [i for i in hits if i not in set(ids)]
    return {"total": len(ids), "days": days, "zero": zero, "gone": gone, "top": hits.most_common(5)}


# ───────── 報告 ─────────
def main():
    rules = load_rules()
    total_paths, dead = check_stale(rules)
    mirror_chars, mirror_n, real_chars, real_n = check_dup(rules)
    now = sizes(rules)
    rec, prev, first = trend(now)
    rf = check_reflex()

    findings = []

    L = ["# 規則體檢報告（機械層）", "", "> %s 自動產生。零額度、只讀、不改任何規則。「候選」＝程式判斷，需要人（或 AI）確認才處置。" % rec["t"], ""]

    L.append("## 1. 過時：規則檔提到的檔案還在不在")
    L.append("- 掃到 %d 個路徑／檔名，**找不到 %d 個**。" % (len(total_paths), len(dead)))
    for t, names in sorted(dead.items())[:12]:
        L.append("  - `%s`（出現在：%s）" % (t, "、".join(sorted(names))))
    if len(dead) > 12:
        L.append("  - …另 %d 個略" % (len(dead) - 12))
    if dead:
        findings.append("過時候選 %d 個" % len(dead))
    L.append("")

    L.append("## 2. 重複：同一行文字在幾份檔（逐行比對，措辭略不同也抓）")
    for k, v in sorted(mirror_chars.items(), key=lambda x: -x[1]):
        L.append("- 自動鏡像（設計如此，不算問題）：%s，%d 行、約 %d 字" % ("＋".join(sorted(k)), mirror_n[k], v))
    for k, v in sorted(real_chars.items(), key=lambda x: -x[1]):
        L.append("- **真正重複**：%s，%d 行、約 %d 字" % ("＋".join(sorted(k)), real_n[k], v))
        findings.append("%s 重複約 %d 字" % ("＋".join(sorted(k)), v))
    if not mirror_chars and not real_chars:
        L.append("- 沒有重複行。")
    L.append("")

    L.append("## 3. 份量：規則總字數趨勢（目標往下）")
    for n, v in now.items():
        L.append("- %s：%d 行／%d 字" % (n, v["lines"], v["chars"]))
    msg = "- 合計 %d 字" % rec["total_chars"]
    if first and first.get("total_chars"):
        diff = rec["total_chars"] - first["total_chars"]
        msg += "（與第一次紀錄 %s 相比 %+d 字）" % (first["t"], diff)
    else:
        msg += "（這是第一次紀錄，之後每次體檢會比對）"
    L.append(msg)
    L.append("- 每場對話常駐載入的是 全域CLAUDE＋專案CLAUDE；反射索引由 hook 程式讀、命中才送進對話，不佔常駐份量。")
    L.append("")

    L.append("## 4. 沒必要：反射命中統計")
    if rf:
        L.append("- 反射 %d 條；命中紀錄只累積 **%d 天**。" % (rf["total"], rf["days"]))
        if rf["days"] < 90:
            L.append("- 紀錄不到 90 天，**不列退休建議**（未命中 %d 條僅供參考，危險指令類本來就該很少命中）。" % len(rf["zero"]))
        else:
            L.append("- 90 天內從沒命中的候選 %d 條：%s…（需人確認，不自動退休）" % (len(rf["zero"]), "、".join(rf["zero"][:8])))
            findings.append("退休候選 %d 條" % len(rf["zero"]))
        L.append("- 最吵前 5：%s" % "、".join("%s %d 次" % (i, c) for i, c in rf["top"]))
        if rf["gone"]:
            L.append("- 命中紀錄裡有、索引已沒有的反射 %d 條（已刪除或改名）：%s" % (len(rf["gone"]), "、".join(rf["gone"][:5])))
    else:
        L.append("- 讀不到反射索引，略過。")
    L.append("")

    L.append("## 處置分級")
    L.append("- 機械的（死路徑、重複副本改成「見某檔」）：AI 自己改並 commit。")
    L.append("- 守則 21 條原文：一字不動。執行細則、CLAUDE.md 的精簡：只出建議，教練拍板才改。")
    head = "✅ 體檢通過" if not findings else "⚠️ 體檢發現 %d 項：%s" % (len(findings), "；".join(findings))
    L.insert(2, "**結論：%s**" % head)
    L.insert(3, "")
    try:
        os.makedirs(os.path.dirname(REPORT), exist_ok=True)
        with open(REPORT, "w", encoding="utf-8") as f:
            f.write("\n".join(L) + "\n")
    except Exception:
        pass
    if "--quiet" not in sys.argv:
        print("🩺 規則體檢：%s（規則合計 %d 字；一頁報告 distill/rules_health_report.md）" % (head, rec["total_chars"]))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # 壞了就放行
        if "--quiet" not in sys.argv:
            print("🩺 規則體檢自己出錯（已放行）：%s: %s" % (type(e).__name__, str(e)[:120]))
    sys.exit(0)
