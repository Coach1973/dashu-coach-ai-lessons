# 宏碁：條件反射已接線（ACER軍師 2026-10-02 09:15）

- **Python**：原本只有微軟商店假捷徑（rc 9009）。已 `winget install Python.Python.3.12 --scope user`，實際路徑 `C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe`，`print(1)` 正常。
- **接線**：`~/.claude/settings.json` 已加 5 個 hook（備份 settings.json.bak-20261002）：UserPromptSubmit `prompt`；PreToolUse `Bash|Edit|Write` 與 `mcp__claude-in-chrome__.*` 的 `pre_tool`；PostToolUse `Bash|Edit|Write` 的 `post_tool`；Stop `reply`。路徑用 `C:\Users\Administrator\Documents\workspace\scripts\reflex_router.py`。未動 feed_junshi_handoff.ps1。
- **模擬實測（stdin 餵事件，因現行 session 的 hook 設定要新對話框才生效）**：
  1. prompt「幫我開發票，統編要寫」→ 輸出「⚡ 條件反射…發票：先跑 claude-brain/data/query_training_invoice.py 查…」；`state/reflex_hits.log` 多一行 `prompt	R-INVOICE	remind`。
  2. reply 含 `https://event.bymyway.com/x（已確認）` → `{"decision":"block","reason":"⚡ 條件反射… 回覆裡有網址後面直接黏著中文標點…"}`。
  3. pre_tool Bash `echo hi` → 無輸出、正常放行。
- **未驗證**：驗證 3（開工置頂🎯）等聯想推上去；真實新對話框的實際畫面待教練下次開新對話框後再補。
