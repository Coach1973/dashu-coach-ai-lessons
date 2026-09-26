---
name: reference-git-rebase-continue-requires-all-modified-staged-2026-09-26
description: git 2.53「You must edit all merge conflicts」誤導訊息——index已無unmerged條目時仍拒絕rebase --continue，真因是還有「已修改未staged」的非衝突追蹤檔案
metadata:
  node_type: memory
  type: reference
  originSessionId: 6b72f753-9867-4140-bb70-667351cad624
  modified: 2026-09-26T14:51:53.433Z
---

聯想Windows機器（git 2.53.0.windows.2）處理 `mac-openclaw-workflows` repo 的 HEARTBEAT.md 合併衝突時，`git add HEARTBEAT.md` 後衝突確實已解決（`git ls-files -u` 與 `git ls-files --stage` 逐一核對過都是 stage 0），但反覆執行 `git rebase --continue` 一律回報：

```
You must edit all merge conflicts and then
mark them as resolved using git add
```

**真因**：同一次 rebase 停下時，repo 裡另一個追蹤檔案（`state/sync_health/tree.json`，由背景hook寫入）也處於「已修改但未 staged」狀態——它不是衝突檔（沒有 `<<<<<<<` 標記，`git status` 顯示的是單純 `M ` 不是 `UU`），但 git 在這個版本仍然把它一起算進「還沒處理完」的範圍，直到把這個檔案也 `git add` 進去，`rebase --continue` 才放行。

**Why**：這跟一般認知「rebase --continue 只需要 resolve 衝突標記的檔案」不同，浪費了好幾輪工具呼叫去檢查 `git ls-files -u`、`git diff --check`、index stage number，全部都顯示乾淨卻還是卡住，最後才想到去 `git add -A` 涵蓋所有 modified 檔案。

**How to apply**：下次 `git rebase --continue` 報同樣的錯誤訊息，且已確認過 `git ls-files -u` 是空的（真的沒有殘留衝突標記）：
1. 直接跑 `git status --short`，把所有非 `??`（未追蹤）的項目全部 `git add`（含看起來與這次衝突無關的檔案）
2. 再跑一次 `git rebase --continue`
3. 不用浪費時間繼續用 `git diff --check` / `git ls-files --stage` 這類工具反覆確認「衝突是不是真的清乾淨」——那些檢查是對的，問題不在那裡

Related: [[feedback_check_handoff_before_diagnosing_git_anomaly_2026-09-21]]（同一台機器、同一個repo，此前也發生過6天沒人發現的中斷rebase，一併查看避免同類git狀態再度悄悄卡住）
