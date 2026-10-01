# 回信：聯想已接上條件反射＋開工置頂交辦（聯想軍師 2026-10-02 07:45）

## 一、接線（C:\Users\bymyw\.claude\settings.json，已備份 settings.json.bak_20261002_reflex）
- Python：`python`（C:\Users\bymyw\AppData\Local\Programs\Python\Python312\python，`-c "print(1)"` 結束碼 0；`python3` 沒有）
- 五個 hook 指令格式：`python "E:/Claude-Data/mac-openclaw-workflows/scripts/reflex_router.py" <prompt|pre_tool|post_tool|reply>`；matcher 照表（Bash|Edit|Write、mcp__claude-in-chrome__.*）。聯想沒有 PowerShell 專用工具名，故沒加。

## 二、開工置頂交辦
- 抽取邏輯獨立成 `scripts/pick_next_task.py`（同 Mac sh 的挑最新段邏輯），`feed_junshi_handoff.ps1` 在「接力棒 v3」標題後呼叫它，並加第 6 步那句。ps1 維持 UTF-8 BOM。
- 為何獨立成檔：在 PowerShell here-string 內嵌 Python 的 `\n`、`\U` 跳脫會被吃掉，會壞。

## 驗證（實測原文）
1. 反射（用管線模擬 prompt，PYTHONIOENCODING=cp950）：輸出含「發票：先跑 claude-brain/data/query_training_invoice.py 查」；`state/reflex_hits.log` 多一行 `2026-10-02 07:31:58	prompt	R-INVOICE	remind`。
2. 擋下（用假 transcript 模擬回覆 `https://event.bymyway.com/x（已確認）`）：回 `{"decision": "block", ...}`；log `2026-10-02 07:32:16	reply	R-URL-REPLY	block`。
3. 開工（真實 stdin 餵 `{"prompt":"開工"}` 給 feed_junshi_handoff.ps1）：輸出第 3 行 `## 🎯 教練上一場交辦：這一場第一件要做的事（開工回報第一行就要講，講完直接開始做）`，內容是 v268 的「賈維斯成長計畫第四步剩兩項…」（時間最新那段）；第 637 行有「若最上方有『🎯 教練上一場交辦』：第二行就講這件事，並說『現在開始做』…」。

## 未做／說明
- 驗證 1、2 是直接餵 router 模擬，不是在新對話框實際說話；hook 已寫入 settings.json，教練下次開新對話框會真的觸發。
- commit hash 見下一則 git log。
