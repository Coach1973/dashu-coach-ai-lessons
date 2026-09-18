#!/usr/bin/env python3
"""
AI團隊品質稽核彙整器
用途：stop_rules_master.py 的13條規則(A~M)其實已經對「這台Mac上任何觸發Stop事件的
      session」自動執行品質稽核(含MiniMax手機Remote Control session)，但违规記錄
      只是各自寫進 distill/*violations.log，寫了沒人讀，等於黑洞。
      這支腳本把「自從上次檢查後」的新違規，按session分組彙整成一份精簡摘要，
      並標明是哪個team member(本機軍師 or 手機MiniMax)違規，供開工時自動讀取。
設計：事件驅動思路的延伸——不新增輪詢cron，掛在既有「開工」六步驟注入之後多印一段，
      沒有新違規就完全不輸出(安靜)，教練不需要多做任何事。
建立：2026-09-18 教練要求「怎麼監督MiniMax小老弟品質」後，軍師設計。
"""
import os
import re
import json
import glob

WORKSPACE = "/Users/bymyway/.openclaw/workspace"
DISTILL_DIR = os.path.join(WORKSPACE, "distill")
STATE_PATH = os.path.join(WORKSPACE, "state", "agent_team_qa_last_read.json")
PROJECTS_DIR = os.path.expanduser("~/.claude/projects/-Users-bymyway--openclaw")
DIGEST_OUT = os.path.join(DISTILL_DIR, "agent_team_qa_digest_latest.md")

RULE_LABELS = {
    "rule12_violations.log": "A.搬運工句型(叫教練複製貼上)",
    "rule05_violations.log": "B.完成聲明缺commit hash",
    "rule_taiwan_time_violations.log": "C.時間鐵律(UTC沒換算台灣時間)",
    "rule07_polling_violations.log": "D.提議輪詢設計(該用事件驅動)",
    "rule03_verify_violations.log": "E.疑似未查證就交付",
    "rule08_ask_violations.log": "F.方向清楚卻多此一舉徵詢",
    "rule_traditional_chinese_violations.log": "I.簡體字",
}


def load_state():
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def parse_new_entries(path, last_line_count):
    """回傳(新的完整行數, [(session_short, timestamp, snippet), ...])"""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return last_line_count, []

    new_lines = lines[last_line_count:]
    entries = []
    cur_session, cur_ts, cur_snips = None, None, []
    for line in new_lines:
        m = re.match(r"^\[([\d\- :]+)\] session=(\S+)", line)
        if m:
            if cur_session:
                entries.append((cur_session, cur_ts, cur_snips))
            cur_ts, cur_session, cur_snips = m.group(1), m.group(2), []
        elif line.strip() == "---":
            if cur_session:
                entries.append((cur_session, cur_ts, cur_snips))
            cur_session, cur_ts, cur_snips = None, None, []
        elif line.strip().startswith("•") or (cur_session and line.strip()):
            cur_snips.append(line.strip()[:120])
    if cur_session:
        entries.append((cur_session, cur_ts, cur_snips))
    return len(lines), entries


_MODEL_CACHE = {}


def resolve_session_kind(session_short):
    """用session前8碼比對transcript檔名，grep assistant訊息model欄位判斷是不是MiniMax"""
    if session_short in _MODEL_CACHE:
        return _MODEL_CACHE[session_short]
    kind = "未知"
    matches = glob.glob(os.path.join(PROJECTS_DIR, session_short + "*.jsonl"))
    if matches:
        try:
            with open(matches[0], encoding="utf-8", errors="ignore") as f:
                head = f.read(200000)
            if re.search(r'"model"\s*:\s*"MiniMax', head):
                kind = "📱手機MiniMax"
            elif '"model"' in head:
                kind = "🖥️本機Claude"
        except Exception:
            pass
    _MODEL_CACHE[session_short] = kind
    return kind


def main():
    state = load_state()
    all_findings = []  # (session_short, kind, rule_label, ts, snippet)

    for logname, rule_label in RULE_LABELS.items():
        path = os.path.join(DISTILL_DIR, logname)
        last_count = state.get(logname, 0)
        new_count, entries = parse_new_entries(path, last_count)
        state[logname] = new_count
        for session_short, ts, snips in entries:
            # 跳過明顯的測試/煙霧測試session(smoke/fin/t開頭純測試代號)
            if session_short in ("smoke", "fin") or re.match(r"^t\d+$", session_short):
                continue
            kind = resolve_session_kind(session_short)
            snippet = snips[0] if snips else ""
            all_findings.append((session_short, kind, rule_label, ts, snippet))

    save_state(state)

    if not all_findings:
        # 安靜：沒有新違規就不輸出任何東西，不打擾教練
        if os.path.exists(DIGEST_OUT):
            os.remove(DIGEST_OUT)
        return

    # 按session分組
    by_session = {}
    for session_short, kind, rule_label, ts, snippet in all_findings:
        by_session.setdefault((session_short, kind), []).append((ts, rule_label, snippet))

    lines = ["## 🩺 AI團隊品質稽核（stop_rules_master.py既有規則，自動彙整未讀違規）", ""]
    minimax_count = sum(1 for (_, k) in by_session if "MiniMax" in k)
    lines.append(f"本次彙整發現 {len(by_session)} 個session有新違規記錄（其中 {minimax_count} 個是手機MiniMax）：")
    lines.append("")
    for (session_short, kind), items in sorted(by_session.items(), key=lambda x: x[1][-1][0]):
        lines.append(f"### {kind} session={session_short}（{len(items)}項）")
        for ts, rule_label, snippet in items:
            line = f"- [{ts}] {rule_label}"
            if snippet:
                line += f"：{snippet}"
            lines.append(line)
        lines.append("")

    digest = "\n".join(lines)
    with open(DIGEST_OUT, "w", encoding="utf-8") as f:
        f.write(digest)
    print(digest)


if __name__ == "__main__":
    main()
