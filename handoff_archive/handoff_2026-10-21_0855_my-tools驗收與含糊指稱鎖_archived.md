## 🔴 給跨對話框軍師讀的總結摘要（2026-10-21 08:55 台灣時間，Mac 桌面版 Code 分頁（「開工」臨時 worktree kaigong-9f059b），Sonnet 5.5→Opus 5.5；教練說「總結」；本段 00:50～08:55，對話容量約 34%）

**主軸：驗收 my-tools 照抄重做 → 抓到並修好「永久刪除／清空後重新載入又回到最近刪除」→ 上線；教練糾正我講話含糊 → 做成收工檢查「含糊指稱鎖」。**
- **my-tools 驗收**：用教練 Chrome 逐項真操作（新增／改名／拖曳分類與項目、收合、刪除進最近刪除、批量搬回、單筆永久刪除、清空、熱門排行 `mytools::` 前綴、複製排序、跨載入記得住），全過。唯一 bug：`merge()` 把 `removed` 網址補回最近刪除，永久刪除的項目重載後變幽靈。改成只有沒有 `trash` 欄位的舊版存檔才補——my-tools `46affd5`，線上與倉庫逐位元組相同、parity_check 缺 0 項、Console 無錯誤。教練真實資料測前備份、測後逐字還原（5 分類 35 項；最近刪除＝大樹教練待辦事項、約瑟布 2 項，已寫進 `trash`）。「永久清空」確定路徑在真資料上被自動模式擋下（會刪教練 2 項），改用假端點隔離副本驗證。
- **雲端來信**（bni-chapters 分支 claude/epic-allen-gyl3sg）已讀並 mark，內容已被規則包涵蓋。
- **策展上傳金鑰（教練 10/21 裁示：不用換、不用改，不再提）**：coach888 公開頁項目「策展上傳網址（教練自己手動上傳用）」＝`https://event.bymyway.com/curation/upload?key=…`；`https://event.bymyway.com/u/xntrmdhgsu` 是同一把鑰匙的短網址。查證：每次上傳立刻通知「活動報名即時通知」群（app.py `curation_upload` → `_notify_xiaolongxia`）；不帶 key 的 `/curation/upload` 本來就要登入；key 是給小龍蝦／赫米斯／聯想這些 AI 免登入上傳用。
- **含糊指稱鎖**：`scripts/stop_rules_master.py` 規則 O＋7 項測試（全套 31/31）；回測 333 則真實回覆命中 2 則（本案原句＋1 則輕微誤擋「同時拿到一條專屬修改連結」）；試金石案例129。教練授權用終端機搬進正式資料夾：workspace main `faea30ffa`（分身 `2440858ae`），改前備份 `state/backup_20261021_rule_o/`。
- **教練原話線索**：「你給了一句非常模糊的話，害我去搜尋是不是這兩條，結果你才跟我說都不是。」「我不是跟你說過我是小白嗎？」「你就不能一次把話說清楚、白話一點一次到位嗎？」→ 提到網址／群組一律寫完整網址或全名；講風險前先查第一手證據；術語翻成白話（worktree＝分身、Stop hook＝收工前的自動檢查）。
- **問總結的固定格式（教練 08:53 肯定並要求所有 AI 照做）**：用收尾框問「對話容量 xx%、本週額度 xx%，要現在總結嗎？」＋按鈕「總結」，教練按一下就好、不用打字、不用問容量。已寫進容量提醒 `scripts/context_percent_hook.py`（SUMMARY_ASK）與反射 R-ASK-SUMMARY-WITH-CONTEXT-PCT。
- **額度**：08:50 本週額度已用 98%（12:59 重置）、5 小時額度 24%。

### 📋 下一場開工先做（以本棒為準）
1. 看含糊指稱鎖有沒有誤擋（`distill/rule_vague_reference_violations.log`）；同一類誤擋第二次就改設計，不補白名單。
2. 小旭老師報名通知改 Telegram 專屬群「小旭老師活動報名通知」（等教練建群；原文留 `event-signup/notify_failures.log`），群編號填進規則表後拿掉 LINE 那條。
3. 看 `state/line_push_blocked.log` 與每日點名「LINE推播閘門」一行；要推播需教練明說。
4. 開工注入若出現「☁️ 雲端對話交件」→ `cloud_branch_pickup.sh prep/merge --verified` 接手，不問同不同意。
5. 承接 10/19 棒第 1～6 項（審查員觀察期 10/20 已滿未對照；連排訪談等，封存 `handoff_archive/handoff_2026-10-19_1136_審查員與訪談緩衝_archived.md`）。

🔧 AI 自己的清單：雲端規則包 4 項與 LINE 閘門 7 項（見封存 `handoff_archive/handoff_2026-10-21_0025_2026-10-20_2220_雲端規則包與LINE閘門_archived.md`）；規則體檢：專案 CLAUDE.md 與特助心法重複約 877 字（鏡像造成，只出建議）。
🙋 要教練決定：無新增。
🤫 等教練自己提起：公開倉庫是否放守則全文；榮樹下大群機器人要不要放回（先講明推播已禁）；LINE 計費整理成客服問題。
