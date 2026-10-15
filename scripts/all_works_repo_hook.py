#!/usr/bin/env python3
"""Hook：PostToolUse（Bash）— 建/刪/改名/封存 GitHub 倉庫、開關 Pages 的那一刻，更新「完整作品一覽」資料（2026-10-15）

「完整作品一覽」(https://coach1973.github.io/all-works/) 的 GitHub 倉庫資料只在事件發生時更新，沒有任何排程或輪詢
（教練已糾正 6 次）。這支是「新增倉庫」那一刻的觸發點：Claude Code 跑完 `gh repo create` 等指令就背景叫
scripts/all_works_refresh.py（它自己有鎖，同時被叫到會排隊；沒變動就不 commit）。
別台電腦或別的程式建的公開倉庫，頁面開啟時會即時補上（頁面直接讀 GitHub 公開清單）。
失敗不擋工作，只寫 state/all_works_refresh.log。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
CMD = re.compile(
    r"\bgh\s+repo\s+(create|delete|rename|archive|unarchive|fork)\b"
    r"|\bgh\s+api\b[^\n]*(-X|--method)\s+(POST|DELETE)\b[^\n]*(user/repos|/pages\b)", re.I)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    if data.get("tool_name") != "Bash":
        return
    command = str((data.get("tool_input") or {}).get("command", ""))
    if "all_works_refresh" in command or not CMD.search(command):
        return
    try:
        out = open(WS / "state" / "all_works_refresh.log", "a", encoding="utf-8")
        subprocess.Popen([sys.executable, str(WS / "scripts" / "all_works_refresh.py"), "--reason", "Claude Code 建/改倉庫"],
                         stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    except Exception:  # noqa: BLE001
        pass


if __name__ == "__main__":
    main()
