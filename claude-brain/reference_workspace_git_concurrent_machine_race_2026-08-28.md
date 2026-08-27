---
name: reference-workspace-git-concurrent-machine-race
description: workspace repo多機並發時的git衝突處理法+編輯前務必重新Read確認內容未被其他機器改版
metadata: 
  node_type: memory
  type: reference
  originSessionId: d5fe9c18-5091-4fff-8716-7d9c0b806495
  modified: 2026-08-27T19:13:19.090Z
---

`E:\Claude-Data\workspace`（= `mac-openclaw-workflows` 雲端 repo）常有多台機器（Mac/聯想/ACER）的「session-end自動同步」背景hook同時在跑，跟軍師手動git commit/push容易撞在一起。

**遇到 push 被拒（fetch first）時**：
1. 先 `git status --short` 確認自己有沒有未commit的髒東西，有就先commit或stash
2. 用 `git pull origin main`（非 `--rebase`），衝突多半發生在HEARTBEAT.md這類純append log檔——這種衝突直接手動保留雙方段落（HEAD區塊+incoming區塊都留著，按時間順序排），不要選邊站丟掉任一方
3. **不要用 `git rebase --abort` 補救**——若正在rebase時中途出狀況直接abort，會把working tree還原到rebase開始前的狀態，連自己剛才commit但還沒推上去的內容都會一起消失（本場實際發生：`scripts/deploy_bigtree_after_0916_event.sh`+待辦表編輯整包被abort清空，得重寫一次）。優先用一般`git pull`+手動解衝突，真的卡死再考慮`rebase --abort`並且要先確認自己的變更已經另外備份/記在對話裡

**編輯共用檔案前，先假設內容可能已經過期**：本場開工時讀到的`archive/大樹小講_歷史講座紀錄.html`是舊版`.item`卡片列表格式，但實際要commit時Mac已經把它同步重構成「宮格牆+EVENTS陣列」新格式。若沒有先重新Read最新內容就直接用old_string套用舊格式做Edit，會產生格式不一致的髒資料或Edit失敗。**任何要編輯這個共用repo裡「別的機器也可能在改」的檔案（歷史紀錄頁/待辦表/HEARTBEAT等），下手前先重新Read一次確認最新結構，不要相信session一開始讀到的版本。**

Related: [[project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26]]（同一個repo的跨機同步根因系列）
