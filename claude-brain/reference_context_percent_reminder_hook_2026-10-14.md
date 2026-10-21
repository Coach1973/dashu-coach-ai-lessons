---
name: reference-context-percent-reminder-hook-2026-10-14
description: 對話容量提醒 hook：context 跨 30/35/40/50% 各提醒教練一次（教練 30% 出頭就開新對話）；怎麼算、怎麼改門檻、桌面版看不到 context 時怎麼查
metadata:
  type: reference
---

2026-10-14 教練發現桌面版畫面看不到 context 用量（只剩 5 小時／每週額度），請 AI 在 30、35、40、50% 各提醒一次；他習慣 30% 出頭就開新對話框。不需升級模型。

**怎麼做的**：`workspace/scripts/context_percent_hook.sh`，掛在 `~/.claude/settings.json` 的 UserPromptSubmit（緊接 session_length_hook.sh 之後；改前備份 `settings.json.bak-20261014-before-context-hook`）。教練每說一句話才算一次（事件觸發，不輪詢）。算法＝對話檔 `~/.claude/projects/.../{session_id}.jsonl` 最後一則 AI 回覆的 input＋cache_creation＋cache_read，除以視窗 100 萬（可用 CONTEXT_WINDOW 覆寫）；實測對照桌面版 `get_usage`（mcp__ccd_session_mgmt__get_usage 的 context 欄）相符。門檻改 `LEVELS`。同一場只在第一次跨線提醒，記號在 /tmp/context_remind_<session_id>。

**Why**：教練看不到畫面上的容量，又習慣依容量決定何時開新對話。**How to apply**：教練問「用了多少」→ 直接呼叫 get_usage 讀；提醒出現時回覆最前面用一句白話講目前百分比，建議說「總結」。若 hook 沒觸發，先查是否掛進 settings.json 與新對話才載入。

**10/17 補（教練 02:40 問「查容量花不花 token」）**：容量 % 由 `context_percent_hook.py` 在本機讀對話檔的 usage 算，不花模型 token；只有出聲時（跨 30/35/40/45/50% 與預設每 5 句，`CONTEXT_REPORT_EVERY`）才各約 100 token 進對話。`get_usage` 是工具呼叫＝多一趟來回（整段對話再讀一次快取）＋結果數百 token；**5 小時額度 % 只有 get_usage 看得到**。兩個容量來源曾差 3%（hook 30%、get_usage 27%，切 Sonnet 後），原因沒查。教練答案：查容量不貴就過 30% 頻繁報（35/40/45/50）。

**2026-10-19 教練定的兩個默契**：
1. **過 30% 之後，每則回覆在所有內容講完之後的「最後一句」固定寫「這場對話已用約 X%」**（教練原話：「我們看到最後一定都是看最後一句的總結」）。`scripts/context_percent_hook.py` 的提醒文字已改成叫 AI 放最後一句（30% 以下的定期報告仍放第一行）；亮燈仍在第一行；收工回報第一句固定「總結已完成…」、最後一句才是容量。
2. **關鍵字**：教練問「對話百分比剩多少」（或「目前對話的百分比是多少」、「容量剩多少」）→ hook 偵測 UserPromptSubmit 的 `prompt`，**不論有沒有過 30%** 都送出「已用 X%、剩 Y%」，AI 直接列給教練、不用叫 get_usage。5 小時／每週額度仍只在問總結那一句才用 get_usage 查。測試 `scripts/test_context_percent_hook.py`（第 11b／12b／13 系列）。

**10/21 問總結的固定格式（教練肯定並要求 Claude 介面所有 AI 照做）**：用收尾框（wrap_up）問「對話容量 xx%、本週額度 xx%，要現在總結嗎？」，按鈕第一顆「總結」（message「總結」）。教練原話：「如果你能主動問我，我連『總結』兩個字都不用打，直接按總結就好了…決定權在我。」已寫進 `scripts/context_percent_hook.py` 的 SUMMARY_ASK 與反射 R-ASK-SUMMARY-WITH-CONTEXT-PCT。
