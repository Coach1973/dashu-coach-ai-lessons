# 大樹大腦（賈維斯資料庫）工具

- 正本：`/Volumes/953-SSD/大樹大腦/`（raw 原文、clean 去重後、reports 報告、manifest.jsonl）
- Mac 工作副本：`~/大樹大腦/clean/`（SSD → Mac 單向同步）
- `export_notebooklm.py`：用 nlm（兩個帳號 profile：default=bymyway7、seabiscuit=seabiscuitclub）搬 NotebookLM 來源原文，只讀、可續跑。
- `dedupe.py`：raw → clean，完全相同合併、很像只列報告（reports/near_dups.csv），不動 NotebookLM。
- 2026-10-11 首次全量：2,157 份來源 → 去重後 1,871 份（合併 278、跳過 8 份空的 YouTube）。
