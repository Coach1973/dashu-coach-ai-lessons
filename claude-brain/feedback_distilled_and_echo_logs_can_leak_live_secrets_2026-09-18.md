---
name: feedback-distilled-and-echo-logs-can-leak-live-secrets-2026-09-18
description: terminal-notes/distilled與state/inbound_echo這類「已篩選過」的衍生檔案，仍可能原封不動含真實API Key/Token，commit前要單獨掃描，不能假設蒸餾過程會自動遮蔽
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 03318971-0b8e-4d14-a5f7-ece34565e951
  modified: 2026-09-18T11:48:05.852Z
---

清理 workspace repo（mac-openclaw-workflows）長期累積的未 commit 檔案時，掃描發現 `state/inbound_echo/2026-09-12.jsonl` 與兩份 `terminal-notes/distilled/*.txt` 內，原封不動含一組 Telegram bot token（已遮蔽，實際值見 `路徑大全_憑證層.md`）與一組正在使用中的 Netlify 部署 token（已遮蔽，實際值見 `路徑大全_憑證層.md`，同一把 token 本場稍早才剛用來部署 bigtree-tw）。已刻意不 commit 這 3 個檔案（其餘 47 個同批檔案已掃描確認乾淨並 commit，commit `577281fbc`）。

**Why：** [[reference_terminal_notes_raw_sessions_no_gitignore_2026-09-14]] 案例已經處理過「原始逐字稿 raw_sessions 會外洩密鑰」，當時的假設是「蒸餾/摘要後的衍生檔案應該是安全的」，所以只把 `raw_sessions/` 加進 `.gitignore`。這次證實這個假設是錯的——`terminal-notes/distilled/`（對話蒸餾摘要）與 `state/inbound_echo/`（訊息即時落地log）這兩種「已加工過」的衍生檔案，只要教練或任何人在原始對話裡貼過真實金鑰，蒸餾/落地流程並不會自動遮蔽或排除它，金鑰就會原封不動被複製過去。

**How to apply：** 往後任何要把 `terminal-notes/distilled/`、`state/inbound_echo/`、或未來新增的任何「衍生自對話內容」的目錄批次 commit 前，都要單獨用 regex 掃過常見金鑰格式（Telegram bot token `\d{8,10}:[A-Za-z0-9_-]{30,}`、Netlify `nfp_`、GitHub `ghp_`、OpenAI `sk-`、Google `AIza`等），不能因為「這是加工過的摘要」就假設乾淨。目前這 3 個檔案仍留在磁碟未 commit、未刪除，教練若要徹底清乾淨，需要決定：①該把這兩個真實金鑰視為已外洩(即使只在本機也算過surface)輪替掉 ②還是接受風險維持現狀（比照 [[reference_terminal_notes_raw_sessions_no_gitignore_2026-09-14]] 的先例）。這兩種都需要教練裁示，不是 AI 能單方面決定的事——涉及正在使用中的 Netlify 部署 token 若輪替需同步改掉 `scripts/deploy_bigtree_after_0916_event.sh` 等所有引用處。

**相關：** [[reference_terminal_notes_raw_sessions_no_gitignore_2026-09-14]]
