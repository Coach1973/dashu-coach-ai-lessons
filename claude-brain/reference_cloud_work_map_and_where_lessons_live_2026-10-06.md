---
name: reference-cloud-work-map-and-where-lessons-live
description: 雲端（claude.ai/code 網頁版）工作全部在哪、10/06 19:30 已整合進 master 的證據、雲端學到的規則放哪、本機看不到的缺口（教練對雲端 AI 的原話）
metadata:
  node_type: memory
  type: reference
  originSessionId: ca7cea53-b1a2-44ef-898b-529238514051
  modified: 2026-10-06T11:22:42.193Z
---

**雲端工作只在一個倉庫**：掃過 `~/github_repos` 76 個倉庫的遠端，只有 `bni-chapters` 有 `claude/*` 分支（workspace 外層另有兩條 8 月舊分支 `claude/kaigong-*`，`vz9ds7` 已在 main，`6fijra` 是 8/17 的 v112 接力棒覆寫版——**不要併**，併了會蓋掉現在的接力棒）。

**10/06 19:30 整合結果（bni-chapters master）**：座位第 1～3 步（雲端 `claude/seats-step123`，rebase 後 `28e6e63`；`git cherry` 6 個 commit 全部已在 master）、三缺文件 8 份（`eddaf5c`，在 `docs/*three_lacks*`、`docs/classic_dialogue_three_lacks_2026-10-06.md` 是教練原話逐字）、雲端總交接信（`69d0b03`）、改名接力棒＋雲端新規則（`01d96e7`）。之後查「雲端有沒有東西沒回本機」＝`git -C ~/github_repos/bni-chapters fetch && git branch -r --no-merged master | grep claude`，只應剩 `seats-step123`（重接過，內容已在）。

**雲端學到的經驗放哪**：寫進 `bni-chapters/CLAUDE.md`「工作方式」四條（接力棒檔名帶主題、找不到檔先搜所有遠端分支、說完成前接上最新 master 再跑測試、卡住的事最後一次推送前檢查、沒遠端時找 add_repo）。雲端每場對話都會讀這份，比寫在本機記憶有用。

**本機仍然看不到的（缺口，無法自動補）**：教練在雲端網頁對話裡講的原話——雲端對話記錄不在 `~/.claude/projects`，本機 `memory/verbatim/` 也不會有。只有雲端 AI 自己寫進 `docs/` 的才拿得到（例：三缺那份原話檔）。

**雲端寫信給軍師**：固定放分支 `docs/to_junshi/`，見 [[reference_cloud_letters_to_junshi_path_2026-10-06]]。**Why:** 10/06 查出 `scripts/cloud_letters.sh` 寫了 `timeout 20 git fetch`，Mac 沒有 `timeout` 指令，被 `2>/dev/null` 吞掉，從沒真的去抓過雲端；已改成沒有 timeout 就直接 fetch，並用 FETCH_HEAD 時間驗證。**How to apply:** 寫 Mac 腳本別用 `timeout`／`gtimeout`；錯誤不要整個丟到 /dev/null，至少要驗證動作真的發生。

機制背景見 [[reference_move_to_cloud_this_repo_2026-09-25]]。
