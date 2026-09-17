---
name: feedback-simply-scan-size-first-2026-09-18
description: 任何「修某個錯誤」的任務，動手前第一步先做最簡單的全域掃描確認「真的有錯的」= 幾則，若 = 0 就停手講明事實，不必寫複雜的處理腳本。
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1de66f96-d9d3-5a68-89e7-7fea62fd2005
---

# 先掃規模再寫腳本，「=0 則」就停手

**規則**：任何「修某個錯誤」、「刪掉錯的」、「修一批 X」的任務，**動手前第一步**先做一個最簡單的全域掃描（10 行內能寫完的那種），把「真的有錯的 = N 則」算出來。若 N = 0，停下來把事實講清楚；若 N = 數十以內，可以考慮寫腳本；若 N = 數百以上，再評估批次處理策略。

**Why**：2026-09-18 凌晨 v217 場寫了 `delete_wrong_v2.js` + `delete_wrong_v3.js` + `dump_full.js` 三個腳本，每個都幾百行（scrapeAllPosts / deletePost / selector 嘗試各種 aria-label / 「⋯」→「刪除貼文」對話框處理），花了好幾輪 + 教練 4 次催促「為什麼不刪掉」、「趕緊做」。最後實際上 = 0 則錯，**白寫了**這些複雜腳本。

正確流程應該是：
1. dump 全文 + grep `event.bymyway.com/curated/<slug>` 統計每個 slug 出現幾次 → 5 行 code 完事
2. 看到所有 slug 都是 2~4 次而非合理的 1 次 → 切半段檢查（再寫 5 行）→ 全部半段都是 1 次 → 確認 N=0
3. **回報**「沒事可做，把事實攤開」

把這套「最簡掃描」做完只要 10 分鐘，寫複雜的鑑別+自動刪除腳本+跑到 v3 花了將近 1 小時。

**How to apply**：

| 任務規模判斷 | 對應處理 |
|------------|---------|
| N = 0（沒錯的） | 立刻講事實，不寫腳本 |
| N ≤ 10 | 可以一個一個手動點，或者寫簡單腳本跑 |
| 10 < N ≤ 100 | 寫批次腳本值得，但要驗證 1 個 sample 再批次 |
| N > 100 | 才需要寫複雜的 retry / error handling / partial-success recovery，但此時仍應停下來問教練是否要批次處理 |

**反向應用**：這個原則也適用於「修 N 個 bug」、「跑 N 個 task」、「找 N 個檔案」等所有「先確認規模」的場景——第一步永遠是「掃描」，而不是「寫複雜處理」。

**關聯**：
- [[feedback_no_wrong_posts_no_action_2026-09-18]] — N=0 時的具體應對
- [[feedback_assert_before_verify_pattern_2026-09-17]] — 「先斷言後查證」的相反，先查證確認規模再決定要不要動
- [[feedback_cap_retries_report_when_stuck_2026-09-03]] — 「同一死角最多 3 次」同精神，達到 3 次就回報別再撞
