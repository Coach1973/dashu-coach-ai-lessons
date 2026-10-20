---
name: feedback-cloud-sessions-get-no-rules-and-never-ship
description: 教練說「聯想的 Claude 很笨、還在問同不同意」＝常是從聯想開的雲端對話(claude.ai/code)，只吃得到該倉庫的 CLAUDE.md，沒有特助心法／hook；雲端推不上 main，做完停在「要你同意」沒人接手合併（10/20 常用網址最近刪除案）
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5a30dc0b-103a-44dd-9abc-ef0d318c8cfe
  modified: 2026-10-20T14:32:40.212Z
---

**查到的（2026-10-20）**：教練貼來的「聯想電腦上的 Claude 對話」其實是雲端對話：提交 `ac3a32d` 作者是 `Claude <noreply@anthropic.com>`、提交說明有 `Claude-Session: https://claude.ai/code/session_01LN2Vrm11MH5qfDrfDTzpaZ`（Sonnet 5.5），從 bni-chapters 倉庫開、中途再去拿 my-tools。認法：聯想本機提交作者是 CoachWU＋「[聯想]」字頭；雲端是 Claude noreply＋Claude-Session 行。雲端只讀得到倉庫裡的 CLAUDE.md／.claude/settings.json：bni-chapters 只有 7KB 專案說明、沒有 settings.json；my-tools 什麼都沒有 → 沒有 21 條守則、亮燈、先查再答、反射。只有 workspace 倉庫與外層 ~/.openclaw 有 cloud_sync 開場注入（見 [[reference-move-to-cloud-this-repo-2026-09-25]]）。

**雲端做不完的結構原因**：雲端推 main 會被自動審查擋（只能推自己的 claude/* 分支），它就停下來「要你明確點頭」；教練去忙 8 小時回來還停在那裡。教練 10/20 原話：「叫他去做事他就去做就好了，還問我同不同意……討論的目的是為了執行」。

**這次的修法**：Mac 接手——伺服器 `_mytools_clean` 補收 `trash`（`3f654abfd`，雲端用假伺服器測不出它會被丟掉）、補齊作品一覽有的永久刪除／永久清空／刪分類進最近刪除，my-tools main `a5e8c69` 上線。

**How to apply**：教練轉貼「別台 Claude 很笨」的對話 → 先看提交作者／Claude-Session 判斷是不是雲端；雲端分支（`git ls-remote … 'refs/heads/claude/*'`）做完的東西由 Mac 驗證後直接合併上線，不再問教練同不同意；雲端用假伺服器測的，上線前一定用正式清理／存檔程式再測一次。根治（讓每個雲端倉庫都吃到全套規則、雲端分支自動交給 Mac 合併）另開工作處理。

**根治已完成（2026-10-21，workspace main `caa5a7436`）**：①規則包——`scripts/cloud/sync_rules_to_repos.py` 把規則同步進 bni-chapters／my-tools／rongtree／taipeiema1017（倉庫清單 `scripts/cloud/cloud_repos.json`，私有放 21 守則全套、公開 my-tools／rongtree 只放雲端行為規則；來源有變才推，session_end_auto_push.sh 背景觸發；新倉庫 `... add <名>`）；真雲端對話實測（bni-chapters，session_01CkfXbCCz5u8DUfQARJyoLf）第一則回覆就亮燈並讀到規則。②交件接手——雲端推 claude/* → webhook（bni-chapters／my-tools 10/21 補掛，原本沒有）寫 `state/cloud_branch_pending` → 開工第一件事 → `scripts/cloud_branch_pickup.sh prep／merge --verified／done`。每日點名有「雲端規則包」「雲端交件待接手」兩行。全文：`knowledges/雲端對話規則與接手流程.md`。**How to apply**：雲端交件通知到了＝下次開工第一件事驗證＋合併上線，不問教練；教練又說雲端很笨 → 先查該倉庫在不在 cloud_repos.json、`sync_rules_to_repos.py status`。
