---
name: all-works-complete-works-page
description: 「完整作品一覽」頁(coach1973.github.io/all-works)怎麼運作、資料從哪來、三個事件觸發點、怎麼手動更新與怎麼查；教練找不到某個網頁/某個人的站時先來這裡搜
metadata:
  node_type: memory
  type: reference
  originSessionId: 05edc65e-a502-4df1-9749-c233f35e9ecb
  modified: 2026-10-15T08:18:50.201Z
---

**頁面**：https://coach1973.github.io/all-works/ （倉庫 Coach1973/all-works，本機 `~/github_repos/all-works`，noindex、只給教練自己看；已收進大樹作品集「大樹常用」）。教練 2026-10-15 交辦，起因是 10/14 一週盤點報告與曾博士網頁都找不到。可帶 `?q=曾博士` 直接搜。

**資料三個來源，去重後約 212 筆**：①GitHub 全部倉庫（含私有 51 個，`data.json`，描述只放公開倉庫的）②策展名冊 `event-signup/curated_sites_registry.json`（59 站，`listed:false`＝已下架）③大樹作品一覽 coach888 伺服器狀態（**頁面每次開啟時即時讀**，所以教練在作品集拖拉改名立刻反映）。另外頁面開啟也即時讀 GitHub 公開倉庫清單，補上別台電腦剛建、還沒觸發到的新倉庫。

**去重靠網址 key**：`scripts/all_works_refresh.py` 對每筆算出 keys（github.io/<repo>、event.bymyway.com/curated/<slug>、event.bymyway.com/<路徑>、<repo>.netlify.app、<repo>.bymyway.com），路徑對照從 `event-signup/app.py` 的 `@app.route`＋`*_REPO = Path(".../github_repos/x")` 自動解析（/DIY3 ↔ diy-studio-workshop），不照慣例的寫在檔內 `ALIASES`（zhencheng-guests↔sincere.bymyway.com 等）。Python `canon()` 與頁面 JS `canon()` 必須完全一致（測試會比對）。**新增一個不照命名慣例的站，要補 ALIASES，不然會被算成「只有 GitHub 沒上架」**。

**四種狀態**：已下架（`_archived_*` 倉庫或名冊 listed:false 或作品集「最近刪除」）＞已收進作品一覽（網址在 coach888，或其子頁在）＞只在策展中心＞只有 GitHub 沒上架。

**更新＝事件觸發，沒有排程**：①`scripts/curation_process.py` main() 每批上架處理完 ②`event-signup/app.py` 策展後台下架／重新上架／刪除按下去（`_fire_all_works_refresh`，測試用假名冊不觸發）③Claude Code PostToolUse hook `scripts/all_works_repo_hook.py`（settings.json，偵測 gh repo create/delete/rename/archive、Pages 開關）。三者都只是背景叫 `python3 scripts/all_works_refresh.py --reason ...`（有 flock 鎖、資料沒變就不 commit）；log 在 `state/all_works_refresh.log`。手動更新就直接跑那支。別台電腦建的**私有**倉庫不會觸發，要等下一次任一觸發點。

**驗證**：`python3 scripts/test_all_works_refresh.py`（27 項，含用 node 在假瀏覽器跑頁面搜尋「曾博士」「Scott」）。字級最小 20px（教練規定）已實測。

**要留意**：data.json 在公開倉庫裡，含 51 個私有倉庫的「名稱」（沒放描述）；若教練在意可改成不輸出私有倉庫。作品一覽 CORS 只放行 `https://coach1973.github.io`，所以本機 localhost 測不到作品一覽，要測線上。

Why: 教練要一頁看完累積了多少、找得到人；同一類「找不到」不要再靠 AI 記得。
How to apply: 教練說「找不到某某網頁/某人的站」→ 先開這頁搜；改去重規則動 all_works_refresh.py 並跑測試。相關：[[feedback_new_admin_urls_auto_register_coach888_2026-10-10]]、[[feedback_event_driven_not_polling_pattern]]、[[reference_curation_sop_2026-09-06]]。
