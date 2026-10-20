#!/usr/bin/env python3
"""雲端對話結束檢查（Stop hook）：每個回合最多攔一次，攔了就放行，不會卡死。
1) 交辦（15 字以上）的第一行沒有亮燈 → 請補上
2) 結尾在問教練「要不要／同不同意」→ 請改成直接做完並交件
由 Mac 的 scripts/cloud/sync_rules_to_repos.py 自動同步進來，請勿手改。出任何錯一律放行。"""
import json, os, re, sys


def last_turn(path):
    prompt, first_text, last_text = "", "", ""
    for line in open(path, encoding="utf-8"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("type")
        msg = d.get("message") or {}
        c = msg.get("content")
        if t == "user":
            if isinstance(c, str):
                text = c
            elif isinstance(c, list):
                if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                    continue
                text = "".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
            else:
                continue
            if text.strip() and not text.lstrip().startswith("<"):
                prompt, first_text, last_text = text, "", ""
        elif t == "assistant" and isinstance(c, list):
            text = "".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text").strip()
            if text:
                if not first_text:
                    first_text = text
                last_text = text
    return prompt, first_text, last_text


ASK = re.compile(r"(要不要|需不需要|是否(需要|要|同意|確認)|可以嗎|好嗎|行嗎|同意嗎|請(您|教練)?(確認|同意|批准|點頭)|等(您|教練|你)(同意|確認|決定))")


def main():
    if os.environ.get("CLAUDE_CODE_REMOTE") != "true":
        return
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        return
    prompt, first_text, last_text = last_turn(data.get("transcript_path", ""))
    if not first_text:
        return
    reason = None
    first_line = first_text.splitlines()[0] if first_text.splitlines() else ""
    if len(prompt.strip()) >= 15 and not re.search("[🔵🟢🟣]", first_line):
        reason = "大樹教練的規則：每則交辦的回覆第一行要先亮燈（🔵 這件 Haiku 就能做／🟢 這件 Sonnet 就能做／🟣 這件是 Opus 等級（理由：…）／閒聊寫🔵 閒聊）。請補上亮燈再收尾，不用重做已完成的事。"
    else:
        tail = last_text[-220:]
        if ASK.search(tail) and re.search(r"[？?]\s*$", tail.strip()):
            reason = "大樹教練的規則：做完不要問同不同意（教練原話：『叫他去做事他就去做就好了，還問我同不同意』）。方向清楚就請直接做完：推到 claude/* 分支、在 docs/to_junshi/ 寫信給 Mac 軍師說明驗證方式，由 Mac 驗證合併上線。若這真的是只有教練能決定的事（花錢、對外發言、不可逆、他本人登入）或方向模糊，保留問題並說明是哪一種；否則請改成直接完成並交件。"
    if reason:
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


try:
    main()
except Exception:
    pass
sys.exit(0)
