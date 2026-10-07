---
name: reference-notebooklm-cli-pipeline-2026-10-08
description: NotebookLM 自動化工具 nlm（notebooklm-mcp-cli）已裝在 SSD 並登入教練帳號；錄音→NotebookLM簡報→套底圖整條流程實測通過；指令、耗時、底圖要用 safe 模式的原因
metadata:
  type: reference
---

**安裝（2026-10-08，教練說「裝」）**：`/Volumes/953-SSD/NotebookLM工具/venv/bin/nlm`（notebooklm-mcp-cli 0.15.4，MIT，非 Google 官方、用未公開介面，作者自己寫可能違反 Google 條款）。登入帳號 bymyway7@gmail.com（PRO consumer 方案，`nlm usage` 看滾動窗口＋每週上限），登入狀態存在 Mac 鑰匙圈（`~/.notebooklm-mcp-cli/profiles/default`），約 2~4 週自動續。`nlm login --check` 驗證。登入需教練在彈出的 Chrome 視窗輸入 Google 密碼（AI 不碰）。

**流程（實測 2026-10-08，10 頁簡報）**：`nlm notebook create "標題" --json` → `nlm source add <id> --text "$(cat 逐字稿.txt)" --title … --wait` → `nlm slides create <id> --format detailed_deck --language zh-TW --confirm`（另有 presenter_slides）→ `nlm studio status <id> --json` 輪詢（**生成約 7 分鐘**，status queued→completed）→ `nlm download slide-deck <id> --format pptx|pdf -o 路徑`。NotebookLM 產出的 PPTX 每頁是一張圖（不能改字）。
**套底圖**：見技能 pptx-brand-background（knowledges/SKILL_簡報套底圖_通用版.md）。**NotebookLM 簡報底部常有說明文字，BNI 底圖用預設 mask 模式會被左下 LOGO／右下弧形吃掉字，要加 `--mode safe`**（內容縮進乾淨區，文字全留）。
**試做成品**：`/Volumes/953-SSD/NotebookLM工具/試做/`（NotebookLM原版 pdf/pptx、BNI版_安全區.pptx（推薦）、BNI版_BNI會員心得分享.pptx（滿版，有字被蓋））；教練 NotebookLM 帳號裡留了測試筆記本「【試做】BNI會員心得分享（Plaud錄音）」。
**未解**：聯想（Windows）能不能裝、NotebookLM 吃不吃音檔（網頁版支援，工具說明沒寫）、一鍵注入頁尚未做。

相關：[[reference_plaud_backup_and_local_transcribe_2026-10-08]]

**教練糾正（2026-10-08 02:37）**：教練只是要「測試能不能進入 NotebookLM」，我卻一路做到簡報＋套BNI底圖＋開Keynote，被說「不用那麼麻煩、你跑得有點太快」。測試類請求只做到能回答「能／不能」，要往下做的下一步用一句話講，不要先跑完整流程（守則16、執行細則N7）。
