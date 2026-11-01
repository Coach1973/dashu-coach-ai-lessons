#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查話工具（recall）——「記住用戶每一句話」的入口（2026-06-11 軍師建立，教練拍板）

設計理念：腦子裡只放地圖，倉庫的東西用的時候才撈。
  - 倉庫：~/.openclaw/agents/*/sessions/*.jsonl（原文 100% 都在）
        + ~/.openclaw/workspace/memory/*.md（每日摘要的「👤 教練：」行）
  - 索引：~/.openclaw/workspace/state/recall_index.jsonl（每天凌晨自動重建）
        只收「真人說的話」，過濾排程/心跳/作夢等系統噪音
  - 入口：本工具。搜尋只回前 N 筆，Context 成本幾百字，不是整個檔。

⚠️ 2026-06-11 重大發現：OpenClaw 對話原文檔（sessions/*.jsonl）在 Context Overflow
重啟時會被清掉——「原文 100% 都在」對小龍蝦不成立。因此本工具多一層：
  - 逐字保險箱：~/.openclaw/workspace/memory/verbatim/YYYY-MM.jsonl（只加不刪）
    每 30 分鐘把 sessions 裡的真人訊息抄進來，從此原文永遠不再蒸發。

用法：
  收割原文（每 30 分鐘 cron 自動跑）：
      python3 recall.py --harvest
  說話當下收割＋核對（2026-10-30 教練拍板事件觸發；桌面版 hook、小龍蝦 coach-context 外掛呼叫）：
      python3 recall.py --harvest-now 終端機      # 等 20 秒讓訊息寫進檔，收割，15 分鐘內沒收到這個來源就出聲
  保險箱體檢（每日點名呼叫）：
      python3 recall.py --check
  建索引（每日 cron 自動跑，也可手動）：
      python3 recall.py --build
  查話（預設前 10 筆，新的在前，全部台灣時間）：
      python3 recall.py 壽星
      python3 recall.py 壽星 生日          # 多關鍵詞 = OR（任一命中）
      python3 recall.py --limit 20 早鳥
  教練有沒有說過 A 跟 B（回答「您沒講過」之前必跑，2026-10-24）：
      python3 recall.py --said 佩佩 LK888
  模糊搜尋：同義詞表 state/recall_synonyms.json，查任一詞自動連同組詞一起查
"""
import json, glob, os, sys, re, datetime

HOME = os.path.expanduser("~")
SESS_GLOB = HOME + "/.openclaw/agents/*/sessions/*.jsonl"
TERMINAL_GLOB = HOME + "/.openclaw/workspace/terminal-notes/raw_sessions/*.jsonl"
# 2026-10-30 賈維斯體檢：桌面版「開工」對話存在 worktree 專案夾，raw_sessions 只備份主資料夾 → 10/27 起教練的話沒收進來。
# 直接讀 Claude Code 專案夾（主資料夾＋所有 worktree），只看 3 天內有動的檔，夠 30 分鐘收割一次用。
LIVE_TERMINAL_GLOB = HOME + "/.claude/projects/-Users-bymyway--openclaw*/*.jsonl"
# 小龍蝦 10 月起（OpenClaw 2026.9.4）對話改存各分身 sqlite，sessions/*.jsonl 只剩舊檔 → 從 10 月起群組原話全沒收。
AGENT_DB_GLOB = HOME + "/.openclaw/agents/*/agent/openclaw-agent.sqlite"
RECENT_SECONDS = 3 * 86400
MEMORY_GLOB = HOME + "/.openclaw/workspace/memory/*.md"
VERBATIM_DIR = HOME + "/.openclaw/workspace/memory/verbatim"
INDEX = HOME + "/.openclaw/workspace/state/recall_index.jsonl"
SYNONYMS = HOME + "/.openclaw/workspace/state/recall_synonyms.json"
TZ = datetime.timezone(datetime.timedelta(hours=8))

# 系統噪音特徵：user 訊息開頭/內含這些字樣 = 不是真人說話，不進索引
NOISE_PREFIXES = ("[cron:", "[OpenClaw", "System:", "[system")
NOISE_CONTAINS = ("heartbeat poll", "HEARTBEAT_OK", "Write a dream diary",
                  "【0 Token 半自動排程】", "relay poll")

AGENT_NAMES = {"main": "小龍蝦群", "kong": "峰哥群", "peipei": "佩佩群"}


def taiwan_time(ts):
    try:
        if isinstance(ts, (int, float)):
            t = datetime.datetime.fromtimestamp(ts / 1000, TZ)
        else:
            t = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).astimezone(TZ)
        return t.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ts)


def is_noise(text):
    if text.startswith(NOISE_PREFIXES):
        return True
    return any(k in text for k in NOISE_CONTAINS)


def extract_text(content):
    if isinstance(content, list):
        return " ".join(c.get("text", "") for c in content if isinstance(c, dict))
    return str(content or "")


def scan_sessions():
    """掃對話原文檔，產出乾淨的「真人訊息」條目"""
    for path in glob.glob(SESS_GLOB):
        agent = path.split("/agents/")[1].split("/")[0]
        try:
            f = open(path, encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in f:
            if '"user"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            m = d.get("message") or {}
            if m.get("role") != "user" or m.get("toolName"):
                continue
            text = extract_text(m.get("content")).strip()
            if not text or is_noise(text):
                continue
            yield {
                "t": taiwan_time(d.get("timestamp")),
                "src": AGENT_NAMES.get(agent, agent),
                "who": "真人訊息",
                "text": re.sub(r"\s+", " ", text)[:1000],
            }
        f.close()


def scan_agent_dbs():
    """掃小龍蝦各分身 sqlite 的真人訊息（只看最近 3 天，收割每 30 分鐘跑一次）"""
    import sqlite3, time
    since = int((time.time() - RECENT_SECONDS) * 1000)
    for path in glob.glob(AGENT_DB_GLOB):
        agent = path.split("/agents/")[1].split("/")[0]
        try:
            conn = sqlite3.connect("file:%s?mode=ro" % path, uri=True, timeout=5)
            rows = conn.execute("SELECT event_json FROM transcript_events WHERE created_at >= ? "
                                "AND event_json LIKE '%\"role\":\"user\"%'", (since,)).fetchall()
            conn.close()
        except Exception:
            continue
        for (raw,) in rows:
            try:
                d = json.loads(raw)
            except Exception:
                continue
            m = d.get("message") or {}
            meta = m.get("__openclaw") or {}
            # inter_session＝分身互相傳話（11/01 起已關），不是真人說話，以前被記成「真人訊息」
            if m.get("role") != "user" or m.get("toolName") or (m.get("provenance") or {}).get("kind") in ("internal_system", "inter_session"):
                continue
            text = extract_text(m.get("content")).strip()
            if not text or is_noise(text) or text.startswith(("[System]", "[OpenClaw", "An async command")):
                continue
            yield {
                "t": taiwan_time(d.get("timestamp")),
                "src": AGENT_NAMES.get(agent, agent),
                "who": meta.get("senderName") or "真人訊息",
                "text": re.sub(r"\s+", " ", text)[:1000],
            }


def scan_terminal():
    """掃終端機對話（Claude Code 格式），抽教練打的字：舊備份＋專案夾裡 3 天內有動的檔"""
    import time
    live = [p for p in glob.glob(LIVE_TERMINAL_GLOB) if time.time() - os.path.getmtime(p) < RECENT_SECONDS]
    for path in glob.glob(TERMINAL_GLOB) + live:
        try:
            f = open(path, encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in f:
            if '"user"' not in line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("type") != "user" or d.get("isSidechain"):
                continue
            m = d.get("message") or {}
            if m.get("role") != "user":
                continue
            c = m.get("content")
            if isinstance(c, list):
                texts = [x.get("text", "") for x in c
                         if isinstance(x, dict) and x.get("type") == "text"]
                text = " ".join(texts)
            else:
                text = str(c or "")
            text = re.sub(r"</?pasted_content[^>]*>", "", text)   # 教練貼上的語音稿也是他的話
            text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S).strip()   # worktree 第一句前面黏著系統提示，不剝掉整句會被當系統訊息丟掉（10/30「開工」全漏）
            if (not text or is_noise(text) or text.startswith("<")
                    or text.startswith(("Caveat:", "[Request interrupted", "Stop hook feedback", "Base directory for this skill"))):
                continue
            yield {
                "t": taiwan_time(d.get("timestamp")),
                "src": "終端機",
                "who": "教練",
                "text": re.sub(r"\s+", " ", text)[:1000],
            }
        f.close()


def harvest():
    """逐字保險箱：把 sessions 還活著的真人訊息抄進永久檔（只加不刪）。
    OpenClaw 重啟會清 sessions，所以要趁訊息還在時收割。"""
    os.makedirs(VERBATIM_DIR, exist_ok=True)
    seen = set()
    for vf in glob.glob(VERBATIM_DIR + "/*.jsonl"):
        for line in open(vf, encoding="utf-8", errors="ignore"):
            try:
                e = json.loads(line)
                seen.add(e["t"] + e["text"][:80])
            except Exception:
                pass
    added = 0
    import itertools
    for e in itertools.chain(scan_sessions(), scan_agent_dbs(), scan_terminal()):
        key = e["t"] + e["text"][:80]
        if key in seen:
            continue
        seen.add(key)
        month = e["t"][:7] if re.match(r"\d{4}-\d{2}", e["t"]) else "unknown"
        with open(os.path.join(VERBATIM_DIR, month + ".jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
        added += 1
    print("✅ 逐字保險箱：新收 %d 句（永久保存於 %s/）" % (added, VERBATIM_DIR))
    probs = vault_problems()
    if probs and datetime.datetime.now(TZ).hour >= 12:   # 半夜到早上沒人說話是正常的，中午後才報
        print("⚠️ " + "；".join(probs))
        notify("🔴 逐字保險箱：" + "；".join(probs) + "。收割程式可能沒讀到新的對話位置，叫軍師查 scripts/recall.py。", "verbatim_stale")


NOTIFY = HOME + "/.openclaw/workspace/scripts/notify_coach.sh"
STALE_HOURS = 6


def vault_newest():
    """保險箱裡每個來源最新一句的時間（檔案是補收後追加，順序不保證，要全掃取最大）"""
    newest = {}
    for vf in glob.glob(VERBATIM_DIR + "/*.jsonl"):
        for line in open(vf, encoding="utf-8", errors="ignore"):
            try:
                e = json.loads(line)
            except Exception:
                continue
            t, src = e.get("t", ""), e.get("src", "")
            if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}$", t) and t > newest.get(src, ""):
                newest[src] = t
    return newest


def vault_problems():
    """回傳保險箱的問題清單（空＝正常）。10/30 教訓：來源搬家後收割一直印「新收 0 句」當成功，停了 6 週沒人發現。"""
    newest = vault_newest()
    now = datetime.datetime.now(TZ)
    out = []
    if not newest:
        return ["保險箱是空的"]
    latest = max(newest.values())
    age = now - datetime.datetime.strptime(latest, "%Y-%m-%d %H:%M").replace(tzinfo=TZ)
    if age > datetime.timedelta(hours=STALE_HOURS):
        out.append("全部來源已 %d 小時沒新增（最後一句 %s）" % (age.total_seconds() // 3600, latest))
    miss = uncovered_stores()
    if miss:
        out.append("有 %d 個新的對話檔沒人收（例：%s）" % (len(miss), miss[0]))
    return out


def uncovered_stores():
    """24 小時內有寫入的對話類檔案，卻不在收割範圍＝對話又搬家了（9/16 改存 sqlite 就是這樣漏了 6 週）"""
    import fnmatch, time
    covered = (SESS_GLOB, AGENT_DB_GLOB)
    out = []
    for path in glob.glob(HOME + "/.openclaw/agents/*/**/*", recursive=True):
        if not path.endswith((".jsonl", ".sqlite", ".db")) or not os.path.isfile(path):
            continue
        if time.time() - os.path.getmtime(path) > 86400:
            continue
        if ".sqlite." in os.path.basename(path):
            continue  # openclaw-agent.sqlite.generation-writer／reindex-lock 這類 4KB 空鎖檔，不是對話（2026-11-01 誤報 3 次）
        if not any(fnmatch.fnmatch(path, g) for g in covered):
            out.append(path.replace(HOME, "~"))
    return out


def notify(msg, key):
    import subprocess
    subprocess.run([NOTIFY, msg, "21600", key], check=False)   # 同一件事 6 小時只報一次


def harvest_now(expect):
    """說話當下收割：同一時間只跑一個，等訊息寫進檔後收割，再核對剛說的話有沒有進來。"""
    import fcntl, time
    lock = open(HOME + "/.openclaw/workspace/state/recall_harvest.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)   # 另一個收割在跑就排隊等，跑完再收、再核對
    time.sleep(20)
    harvest()
    if expect == "-":   # 不是教練本人說的，只收割不核對
        return
    cutoff = (datetime.datetime.now(TZ) - datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M")
    if expect != "終端機":
        # 2026-11-02：11/01 四次警報全是誤報——①分工群一句話三個分身都收到，保險箱只存一份（記在先掃到的分身名下），
        # 照分身名找就找不到；②分身「接續工作」也會觸發，但教練根本沒說新的話。
        # 改成直接核對：分身資料庫裡 15 分鐘內有署名的真人訊息，是不是每一句都進了保險箱。
        seen = set()
        for vf in glob.glob(VERBATIM_DIR + "/*.jsonl"):
            for line in open(vf, encoding="utf-8", errors="ignore"):
                try:
                    e = json.loads(line)
                    seen.add(e["t"] + e["text"][:80])
                except Exception:
                    pass
        missing = [e for e in scan_agent_dbs() if e["t"] >= cutoff and e["who"] != "真人訊息"
                   and e["t"] + e["text"][:80] not in seen]
        if missing:
            notify("🔴 逐字保險箱：%s有 %d 句話沒收進保險箱（例：%s %s）。叫軍師查 scripts/recall.py。"
                   % (expect, len(missing), missing[0]["t"], missing[0]["text"][:30]), "verbatim_expect_" + expect)
        return
    t = vault_newest().get(expect, "")
    if t < cutoff:
        notify("🔴 逐字保險箱：%s剛有人說話，但保險箱沒收到（%s最後一句 %s）。對話存放位置可能又變了，叫軍師查 scripts/recall.py。"
               % (expect, expect, t or "從沒收過"), "verbatim_expect_" + expect)


def build():
    entries = []
    # 來源一：逐字保險箱（含已被系統清掉的歷史原文）
    for vf in glob.glob(VERBATIM_DIR + "/*.jsonl"):
        for line in open(vf, encoding="utf-8", errors="ignore"):
            try:
                e = json.loads(line)
                e["ref"] = vf
                entries.append(e)
            except Exception:
                pass
    # 來源一之二：對話原文檔（小龍蝦＋終端機）還活著、但尚未收割的訊息
    import itertools
    for e in itertools.chain(scan_sessions(), scan_agent_dbs(), scan_terminal()):
        e = dict(e, ref="sessions", text=e["text"][:300])
        entries.append(e)
    # 來源二：每日摘要裡的教練原話
    for path in glob.glob(MEMORY_GLOB):
        day = os.path.basename(path)[:10]  # YYYY-MM-DD
        if not re.match(r"\d{4}-\d{2}-\d{2}", day):
            continue
        try:
            f = open(path, encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(f, 1):
            if "👤 教練：" not in line:
                continue
            text = line.split("👤 教練：", 1)[1].strip()
            if not text or is_noise(text):
                continue
            entries.append({
                "t": day,
                "src": "每日摘要",
                "who": "教練",
                "text": re.sub(r"\s+", " ", text)[:300],
                "ref": "%s:%d" % (path, i),
            })
        f.close()
    # 去重（作夢任務會大量複製同句話）
    seen, uniq = set(), []
    for e in sorted(entries, key=lambda x: x["t"]):
        key = e["text"][:120]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(e)
    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    with open(INDEX, "w", encoding="utf-8") as f:
        for e in uniq:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print("✅ 索引重建完成：%d 句真人的話 → %s" % (len(uniq), INDEX))


def expand_keywords(words):
    """同義詞展開：查任一詞，同組的詞一起查（模糊搜尋第一階段）"""
    out = set(words)
    try:
        groups = json.load(open(SYNONYMS, encoding="utf-8"))
        for g in groups:
            if any(w in g for w in words):
                out.update(g)
    except Exception:
        pass
    return list(out)


def search(words, limit=10):
    if not os.path.exists(INDEX):
        print("索引不存在，先建一次……")
        build()
    kws = expand_keywords(words)
    hits = []
    for line in open(INDEX, encoding="utf-8"):
        if not any(k in line for k in kws):
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue
        if any(k in e["text"] for k in kws):
            hits.append(e)
    hits.sort(key=lambda x: x["t"], reverse=True)
    shown = hits[:limit]
    label = " / ".join(kws)
    print("🔎 查「%s」：共 %d 筆，顯示最近 %d 筆（台灣時間）\n" % (label, len(hits), len(shown)))
    for e in shown:
        print("[%s]（%s·%s）%s" % (e["t"], e["src"], e["who"], e["text"][:150]))
    if len(hits) > limit:
        print("\n……還有 %d 筆，要看更多：recall.py --limit %d %s" % (len(hits) - limit, limit + 10, " ".join(words)))


def _group_of(word):
    """一個詞所屬的同義詞組（含自己）"""
    g = set([word])
    try:
        for grp in json.load(open(SYNONYMS, encoding="utf-8")):
            if word in grp:
                g.update(grp)
    except Exception:
        pass
    return sorted(g, key=len, reverse=True)


# 教練的話常常已經「做進系統」：設定檔、hook、分身說明檔裡有寫，就代表教練交代過
LANDED_GLOBS = [
    HOME + "/.openclaw/workspace/hooks/*/HOOK.md",
    HOME + "/.openclaw/agents/*/*.md",
    HOME + "/.openclaw/openclaw.json",
    HOME + "/.openclaw/workspace/knowledges/*.md",
    HOME + "/.claude/projects/-Users-bymyway--openclaw/memory/*.md",
]


def said(topics, limit=15):
    """2026-10-24 教練：「你一句我沒講過，我就得叫小龍蝦去翻紀錄」——
    回答「教練有沒有說過 A 跟 B」前一定跑這個：每個主題各自展開同義詞，
    同一句話裡每個主題都命中才算；再查這件事有沒有被做進設定檔／hook／分身說明檔。
    查無結果時只准說「我用哪些詞查了哪些地方沒找到」，不准說「你沒講過」。"""
    if not os.path.exists(INDEX):
        build()
    groups = [_group_of(t) for t in topics]
    hits = []
    for line in open(INDEX, encoding="utf-8"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        txt = e.get("text", "").lower()
        if all(any(k.lower() in txt for k in g) for g in groups):
            hits.append(e)
    hits.sort(key=lambda x: x["t"])
    print("🔎 原話（每個主題都要命中；同義詞已展開）")
    for i, g in enumerate(groups):
        print("   主題%d：%s" % (i + 1, " / ".join(g)))
    print("   共 %d 筆（台灣時間，舊到新）：\n" % len(hits))
    for e in hits[:limit]:
        print("[%s]（%s·%s）%s" % (e["t"], e["src"], e["who"], e["text"][:200].replace("\n", " ")))
    if len(hits) > limit:
        print("……還有 %d 筆（--limit 調大）" % (len(hits) - limit))

    landed = []
    for pat in LANDED_GLOBS:
        for f in glob.glob(pat):
            try:
                lines = open(f, encoding="utf-8", errors="ignore").read().split("\n")
            except Exception:
                continue
            for i in range(len(lines)):
                if not any(any(k.lower() in lines[i].lower() for k in g) for g in groups):
                    continue
                win = "\n".join(lines[max(0, i - 3):i + 4]).lower()
                if all(any(k.lower() in win for k in g) for g in groups):
                    landed.append((f.replace(HOME, "~"), i + 1, lines[i].strip()[:160]))
                    break
    print("\n🧱 已做進系統的證據（設定檔／hook／分身說明檔／記憶，前後 3 行內每個主題都出現）：%d 處" % len(landed))
    for f, n, t in landed[:limit]:
        print("  %s:%d  %s" % (f, n, t))

    print("\n" + ("✅ 有找到，回覆要引用上面的原話或檔案行號。" if hits or landed else
                  "⚪ 查無。回覆只准寫：「我用上面這些詞查了原話索引和系統設定，沒找到」，"
                  "並問教練大概哪一天、在哪個群說的；不准寫「您沒講過」「從來沒有」。"))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--said"]:
        lim = 15
        if "--limit" in args:
            i = args.index("--limit")
            lim = int(args[i + 1])
            del args[i:i + 2]
        said(args[1:], lim)
        sys.exit(0)
    if not args or args == ["--help"]:
        print(__doc__)
        sys.exit(0)
    if "--harvest-now" in args:
        i = args.index("--harvest-now")
        harvest_now(args[i + 1] if i + 1 < len(args) else "終端機")
        sys.exit(0)
    if "--check" in args:
        probs = vault_problems()
        print("\n".join(probs) if probs else "✅ 逐字保險箱正常")
        sys.exit(1 if probs else 0)
    did = False
    if "--harvest" in args:
        harvest()
        did = True
    if "--build" in args:
        build()
        did = True
    if did:
        sys.exit(0)
    limit = 10
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])
        del args[i:i + 2]
    search(args, limit)
