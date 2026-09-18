---
name: feedback_scan_full_context_not_just_known_risk_folder
description: 給新環境(小二)歷史記憶前，只排除已知風險資料夾(verbatim/)不夠，一般memory每日檔案裡也可能藏明文金鑰，必須對整個複製範圍做全文grep
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c23aa475-6fb1-4f77-8a84-3e87c7916908
  modified: 2026-09-13T10:07:01.669Z
---

排除已知的高風險資料夾(如verbatim/原始逐字稿)不等於安全，一般看起來「已提煉」的memory每日檔案裡，仍可能因為當天對話直接貼過明文機密而夾帶洩漏，必須對整個要交付的範圍做一次全文grep(常見金鑰格式)才算做完敏感資料檢查。

**Why**：2026-09-12 v200那棒建置OpenClaw 2.0隔離測試環境「小二」時，已經做過一次安全掃描並發現、排除了`verbatim/`資料夾裡的明文金鑰洩漏，但**沒有對其餘複製過去的內容(memory/每日檔案、試金石、handoff_archive共26MB)做全文掃描**，隱含假設「只有verbatim/這種原始逐字稿才會有洩漏，經過整理的memory每日檔案應該是安全的」。2026-09-13教練授權接手訓練小二後重新做一次全面`grep`，在`context/archive/2026-05-23.md`（教練那天測試第三方Claude API Key的逐字對話third-person筆記）裡抓到兩組真實明文金鑰(`sk-e9d1316d...`、`sk-6d07b650...`)，雖然這兩組key測試當下就已401失效，風險相對低，但仍是不該留在測試環境裡的明文機密，且證明「memory每日檔案」這個看似已提煉的層級，一樣可能因為當天教練直接貼出真實憑證做測試而夾帶洩漏，不是只有verbatim/才有這個問題。

**How to apply**：往後任何要把workspace內容（不論是memory/、試金石/、knowledges/，或任何聲稱「已經提煉過」的檔案）複製給新環境或第三方讀取前，一律對**整個要交付的範圍**跑一次`grep -rloE`常見金鑰格式(`sk-`、`AIza`、`ghp_`、`xox[baprs]-`、Telegram bot token格式`\d{8,10}:AA...`等)，逐一人工核對命中內容是真實金鑰還是誤報(如檔案路徑裡剛好含類似格式的字串)，不能因為「這個資料夾不是verbatim/原始逐字稿、應該是安全的」就跳過。命中真實金鑰時直接遮蔽取代(保留其餘教學/案例價值的文字內容)，不需要整個檔案刪除或隔離。此案與[[reference_verbatim_pipeline_cli_only_not_desktop_chat]]、小二相關教訓([[project_xiaoer_openclaw2_test_environment_2026-09-13]])同屬一組「給新環境喂歷史記憶前的安全檢查」系列。
