#!/usr/bin/env python3
"""Artifact 發佈後自動收進「大樹作品集」的「大樹常用」（PostToolUse hook，2026-10-15）

起因：教練 10/15 14:40「10/14 一週盤點報告我找不到……不是說做出來的東西都會收錄在大樹作品一覽中嗎？」
      報告發佈成 claude.ai Artifact 後沒有任何東西把它登記進 coach888，只能靠 AI 記得——記不住。
      N8：同類錯改源頭。這支 hook 在 Artifact 工具發佈成功的同一刻自動登記，不靠記憶。

規則：
  - 只處理 Artifact 的「發佈頁面」動作（不處理 list／read／delete／asset 上傳）。
  - 名稱＝HTML 檔的 <title>；找不到就用 tool_input.title。
  - 網址已在作品集裡就不動（不搬位置、不覆蓋教練改過的名稱，register() 會重排所以先自己檢查）。
  - 失敗不擋工作，只寫 state/auto_register_artifact.log；成功時回一行 additionalContext 讓 AI 在回報時講。
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WS / "scripts"))
LOG = WS / "state" / "auto_register_artifact.log"
SECTION, BADGE = "changyong", "報告"


def log(msg: str) -> None:
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%F %T} {msg}\n")
    except OSError:
        pass


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    if data.get("tool_name") != "Artifact":
        return
    ti = data.get("tool_input") or {}
    if ti.get("action") not in (None, "publish") or ti.get("asset") or ti.get("type_url"):
        return
    fp = ti.get("file_path") or ""
    resp = data.get("tool_response")
    text = resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)
    m = re.search(r"Published .*? at (https://claude\.ai/(?:code/)?artifact/[A-Za-z0-9-]+)", text) \
        or re.search(r"(https://claude\.ai/(?:code/)?artifact/[A-Za-z0-9-]+)", text)
    if not m:
        return
    url = m.group(1)
    name = ""
    try:
        head = Path(fp).read_text(encoding="utf-8")[:8192]
        t = re.search(r"<title>(.*?)</title>", head, re.S)
        name = re.sub(r"\s+", " ", t.group(1)).strip() if t else ""
    except OSError:
        pass
    name = name or (ti.get("title") or "").strip() or Path(fp).stem
    try:
        import coach888_register_admin as reg
        state = reg._get()
        layout = json.loads(state["coach888_layout"])
        if any(url in v for v in layout.values()):
            log(f"已在作品集，略過 {url}")
            return
        msg = reg.register(url, name, SECTION, BADGE)
        log(f"{url} {msg}")
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"已自動收進大樹作品集「大樹常用」：{name}（{url}）。回報時講一句，不用再手動登記。"}},
            ensure_ascii=False))
    except BaseException as e:  # SystemExit 也要接住，不能讓 hook 擋工作
        log(f"登記失敗 {url} {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
