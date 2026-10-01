#!/usr/bin/env python3
"""教練原話庫（2026-10-02，Top 30 條件反射用）

從 memory/verbatim/*.jsonl 抽出「教練本人說的話」，去掉系統塞進去的雜訊，存 state/coach_corpus.jsonl。
- 終端機：全部是教練打的字，但混有 hook 回饋、對話接續通知、技能說明等系統文字 → 濾掉
- 群組：只留 sender 是教練（6124913915）的，去掉 Conversation info／Sender 這類 metadata
- <pasted_content> 保留（教練常把手機語音稿貼進來，那也是他的話），標 pasted=true
輸出欄位：t, src, text, pasted
用法：python3 scripts/build_coach_corpus.py
"""
import glob
import json
import os
import re

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(WS, "state/coach_corpus.jsonl")
COACH_ID = "6124913915"

# 開頭是這些的終端機訊息＝系統文字，不是教練說的
NOISE_PREFIX = (
    "Stop hook feedback", "This session is being continued", "Base directory for this skill",
    "Continue from where you left off", "Your tool call was malformed", "Try again",
    "[Request interrupted", "<task-notification>", "<command-name>", "<command-message>",
    "<local-command", "Caveat:", "API Error", "bymyway@wudashudeMac-mini",
    "PreToolUse:", "PostToolUse:", "UserPromptSubmit", "[Image", "<bash-",
)


GROUP_NOISE_PREFIX = ("[Subagent Context]", "Continue the OpenClaw runtime", "📋 新報名通知",
                      "[User sent media", "<media:", "[Image]", "System:", "[System")


def clean_group(text, src):
    if "Conversation info" not in text[:200] and "Sender (untrusted" not in text[:1500]:
        # 沒有寄件人標記：小龍蝦群是教練跟小龍蝦的直線，視為教練本人；其他群分不出是誰說的，不收
        if src != "小龍蝦群" or text.startswith(GROUP_NOISE_PREFIX):
            return None
        return text.strip() or None
    if COACH_ID not in text[:1500]:
        return None
    # metadata 都包在 ``` 區塊裡，教練的話在最後一個區塊之後
    body = re.sub(r"(?s)^.*```\s*", "", text) if "```" in text else text
    body = re.sub(r"(?s)\[Reply chain.*$", "", body)  # 引用的上下文不是教練這次說的
    return body.strip() or None


def main():
    rows, seen = [], set()
    for f in sorted(glob.glob(os.path.join(WS, "memory/verbatim/*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            text = (d.get("text") or "").strip()
            if d.get("src") == "終端機":
                if not text or text.startswith(NOISE_PREFIX):
                    continue
            else:
                text = clean_group(text, d.get("src"))
                if not text:
                    continue
            key = (d.get("t", "")[:16], text[:200])
            if key in seen:
                continue
            seen.add(key)
            rows.append({"t": d.get("t", ""), "src": d.get("src", ""), "text": text,
                         "pasted": "<pasted_content" in text})
    rows.sort(key=lambda r: r["t"])
    with open(OUT, "w", encoding="utf-8") as fo:
        for r in rows:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")
    by_src = {}
    for r in rows:
        by_src[r["src"]] = by_src.get(r["src"], 0) + 1
    print(f"{len(rows)} 則 → {OUT}")
    print(by_src)


if __name__ == "__main__":
    main()
