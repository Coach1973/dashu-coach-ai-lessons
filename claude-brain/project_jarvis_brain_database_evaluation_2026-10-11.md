---
name: project-jarvis-brain-database-evaluation-2026-10-11
description: "賈維斯大腦資料庫評估（10/11）：教練 NotebookLM 實際 153 本筆記本／1,203 份來源，nlm source content 可抽原文（實測）；建議自建「大樹大腦」文字庫＋三個手機入口，NotebookLM 留作簡報工作室；Google AI Edge Foresight 只能 Mac 本機、不適合"
metadata:
  node_type: memory
  type: project
  originSessionId: ad5a08ab-3fc1-4b50-90a5-2500e53efebe
  modified: 2026-10-11T04:28:59.912Z
---

教練 2026-10-11 要求評估「賈維斯大腦」：手機 Telegram／小龍蝦／Claude 隨口問，就能從所有資料（NotebookLM、錄音、筆記）找答案。

**查證過的事實（10/11）**
- NotebookLM（現改名 Gemini Notebook）帳號 bymyway7：**153 本筆記本、1,203 份來源**；最大一本「週一週四分享會匯整」127 份。
- `nlm source content <來源id>` 可取出原始文字（實測【試做】筆記本一份 9,475 字成功）→ 1,203 份可整批搬出。nlm 是非官方工具，Google 改版可能失效。
- NotebookLM 官方沒有跨筆記本搜尋（2026 多份指南確認，只有第三方 Chrome 擴充）；一本上限約 300 份（Pro），1,203 份塞不進一本；沒有官方 API 給 Telegram／Claude 叫用。
- Google AI Edge Foresight：只有 Apple 晶片 Mac、完全本機、實驗版、中文未確認、評測有亂寫摘要 → 手機問不到，不適合當大腦。
- GitHub：官方建議單一 repo 壓縮後 ≤10GB、單檔 <100MB；workspace repo 已 874MB，大腦要另開私有 repo，GitHub 只當備份不當搜尋。
- Mac：M4／16GB RAM；Plaud 175 筆逐字稿已在 SSD；小龍蝦 openclaw.json 已開本機向量搜尋（只搜 memory）。

**建議方案**：一個「大樹大腦」純文字資料夾（Mac SSD，備份私有 GitHub＋Google 雲端硬碟）＋關鍵字＋語意搜尋 → 小龍蝦、Claude 手機遠端、Claude App 連接器三個入口共用。先做試點：搬出全部來源，用教練 10 個真實問題驗收。

**狀態**：報告已交，等教練決定是否開始第一階段。

相關：[[reference-notebooklm-cli-pipeline-2026-10-08]]、[[reference-plaud-backup-and-local-transcribe-2026-10-08]]、[[project_jarvis_growth_plan_2026-10-02]]
