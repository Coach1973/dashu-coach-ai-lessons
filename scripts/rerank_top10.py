#!/usr/bin/env python3
"""
rerank_top10.py — 痛點計分與重新排名（確定性，不呼叫 LLM）
用途：統計場景庫 + 自動增量場景 + 計分log 裡每條守則被違反次數，重算痛點排名
資料來源：
  - distill/特助場景庫_格式D_128合併版.md（人工主庫）
  - distill/特助場景庫_自動增量.md（OpenClaw 自動產生）
  - distill/痛點計分_log.jsonl（OpenClaw 每日寫入的違反紀錄）
輸出：distill/痛點排名_自動.md（機器計算，給軍師/教練看哪條守則最該補強）
執行：Mac crontab 每日 23:40，不消耗 Claude Code Token
軍師建立 2026-05-28
"""
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone, timedelta

BASE = os.path.expanduser("~/.openclaw/workspace/distill")
MAIN_LIB = os.path.join(BASE, "特助場景庫_格式D_128合併版.md")
AUTO_LIB = os.path.join(BASE, "特助場景庫_自動增量.md")
SCORE_LOG = os.path.join(BASE, "痛點計分_log.jsonl")
OUTPUT = os.path.join(BASE, "痛點排名_自動.md")

TWN = timezone(timedelta(hours=8))

# 21 守則簡稱（對照特助心法.md）
RULE_NAMES = {
    1: "在乎感受", 2: "方向確認", 3: "思考問問題", 4: "解決問題",
    5: "commitHash", 6: "完美交接", 7: "失敗為成功之母", 8: "討論後執行",
    9: "知道為什麼", 10: "說人話", 11: "自動自發", 12: "拒絕搬運工",
    13: "客戶聲音", 14: "提煉習慣", 15: "說不知道", 16: "複雜非正解",
    17: "環境確認", 18: "語音糾偏", 19: "心跳有意義", 20: "啟動協議",
    21: "一字不差",
}

# 守則標記行：**守則：** 或 **違反守則：** 開頭
RULE_LINE_RE = re.compile(r"^\*\*(?:違反)?守則[：:]")
RULE_NUM_RE = re.compile(r"#(\d{1,2})")


def count_from_markdown(path):
    """從場景庫 markdown 統計每條守則被違反次數（略過 HTML 註解範本）"""
    counter = Counter()
    case_count = 0
    if not os.path.exists(path):
        return counter, case_count
    in_comment = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            # 略過 <!-- ... --> 註解區塊（範本不算真實案例）
            if "<!--" in line:
                in_comment = True
            if in_comment:
                if "-->" in line:
                    in_comment = False
                continue
            if line.startswith("## 案例"):
                case_count += 1
            if RULE_LINE_RE.match(line):
                for m in RULE_NUM_RE.findall(line):
                    n = int(m)
                    if 1 <= n <= 21:
                        counter[n] += 1
    return counter, case_count


def count_from_log(path):
    """從計分 log（JSONL）統計，並記錄最後犯錯日期"""
    counter = Counter()
    last_date = {}
    entries = 0
    if not os.path.exists(path):
        return counter, last_date, entries
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            # 略過格式說明行（_format / _example）
            if "_format" in d or "_example" in d:
                continue
            entries += 1
            date = d.get("date", "")
            rules = d.get("違反守則", d.get("rules", []))
            for r in rules:
                # 接受 "#08" / "08" / 8
                if isinstance(r, str):
                    mm = RULE_NUM_RE.search(r) or re.search(r"(\d{1,2})", r)
                    if not mm:
                        continue
                    n = int(mm.group(1))
                else:
                    n = int(r)
                if 1 <= n <= 21:
                    counter[n] += 1
                    if date and (n not in last_date or date > last_date[n]):
                        last_date[n] = date
    return counter, last_date, entries


def main():
    now = datetime.now(TWN)
    now_str = now.strftime("%Y-%m-%d %H:%M")

    main_counter, main_cases = count_from_markdown(MAIN_LIB)
    auto_counter, auto_cases = count_from_markdown(AUTO_LIB)
    log_counter, last_date, log_entries = count_from_log(SCORE_LOG)

    total = Counter()
    total.update(main_counter)
    total.update(auto_counter)
    total.update(log_counter)

    grand_total = sum(total.values())
    total_cases = main_cases + auto_cases

    # 排名
    ranked = total.most_common()

    lines = [
        "# 痛點排名（自動計算）",
        "",
        f"> 機器計算，不靠 LLM 猜測 | 更新：{now_str}（台灣時間）",
        f"> 資料來源：人工主庫 {main_cases} 案 + 自動增量 {auto_cases} 案 + 計分log {log_entries} 筆",
        f"> 守則違反總次數：{grand_total}",
        "",
        "---",
        "",
        "## 📊 守則違反排行（高 → 低）",
        "",
        "| 排名 | 守則 | 名稱 | 違反次數 | 佔比 | 最後犯錯 |",
        "|------|------|------|----------|------|----------|",
    ]

    for i, (rule, cnt) in enumerate(ranked, 1):
        name = RULE_NAMES.get(rule, "?")
        pct = f"{cnt / grand_total * 100:.1f}%" if grand_total else "0%"
        ld = last_date.get(rule, "—")
        flag = ""
        # 近 30 天內有犯 → 標 🟢 活躍
        if rule in last_date:
            try:
                d = datetime.strptime(last_date[rule], "%Y-%m-%d").replace(tzinfo=TWN)
                if (now - d).days <= 30:
                    flag = " 🟢"
            except ValueError:
                pass
        lines.append(f"| {i} | #{rule:02d} | {name} | {cnt}{flag} | {pct} | {ld} |")

    lines += [
        "",
        "---",
        "",
        "## 🔬 軍師解讀提示",
        "",
        "- **🟢 = 近 30 天仍在犯**：這條守則的養分最該優先補進「兩問句」與 trigger_index。",
        "- 排名靠前 + 仍活躍 = 系統反覆跌倒處，是守則打磨的第一優先。",
        "- 此檔為自動累計，人工主庫 top10_dynamic.md 仍是官方策展版；兩者對照看趨勢。",
        "",
        f"*由 rerank_top10.py 自動生成 | {now_str}*",
    ]

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[rerank {now_str}] 完成")
    print(f"  總案例：{total_cases}（主庫{main_cases} + 自動{auto_cases}）")
    print(f"  計分log：{log_entries} 筆")
    print(f"  守則違反總次數：{grand_total}")
    print(f"  前5痛點：{[f'#{r:02d}({c})' for r, c in ranked[:5]]}")
    print(f"  輸出：{OUTPUT}")


if __name__ == "__main__":
    main()
