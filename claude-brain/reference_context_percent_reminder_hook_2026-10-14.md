---
name: reference-context-percent-reminder-hook-2026-10-14
description: 對話容量提醒 hook：context 跨 30/35/40/50% 各提醒教練一次（教練 30% 出頭就開新對話）；怎麼算、怎麼改門檻、桌面版看不到 context 時怎麼查
metadata:
  type: reference
---

2026-10-14 教練發現桌面版畫面看不到 context 用量（只剩 5 小時／每週額度），請 AI 在 30、35、40、50% 各提醒一次；他習慣 30% 出頭就開新對話框。不需升級模型。

**怎麼做的**：`workspace/scripts/context_percent_hook.sh`，掛在 `~/.claude/settings.json` 的 UserPromptSubmit（緊接 session_length_hook.sh 之後；改前備份 `settings.json.bak-20261014-before-context-hook`）。教練每說一句話才算一次（事件觸發，不輪詢）。算法＝對話檔 `~/.claude/projects/.../{session_id}.jsonl` 最後一則 AI 回覆的 input＋cache_creation＋cache_read，除以視窗 100 萬（可用 CONTEXT_WINDOW 覆寫）；實測對照桌面版 `get_usage`（mcp__ccd_session_mgmt__get_usage 的 context 欄）相符。門檻改 `LEVELS`。同一場只在第一次跨線提醒，記號在 /tmp/context_remind_<session_id>。

**Why**：教練看不到畫面上的容量，又習慣依容量決定何時開新對話。**How to apply**：教練問「用了多少」→ 直接呼叫 get_usage 讀；提醒出現時回覆最前面用一句白話講目前百分比，建議說「總結」。若 hook 沒觸發，先查是否掛進 settings.json 與新對話才載入。
