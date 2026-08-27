---
name: project_claude_avatar_cool_case
description: cool-case網站Claude頭像設計始末——6/23設計完卻孤立20天未上傳，7/13查出並上線，套進「Opus 軍師」而非原計劃的「Claude 克勞德」
metadata: 
  node_type: memory
  type: project
  originSessionId: 6478f86b-2a53-4ef1-9aba-41c3d1ba22f5
---

## 結論（已完成，不用再查）
`E:\Claude-Data\github_repos\cool-case\assets\claude-avatar.svg`——白底橘邊、圈裡寫
「克勞德／Claude」中英對照，2026-06-23 桌面版對話設計、教練親選 B 款。已於
2026-07-13 套進網站「Opus 軍師」標籤的 8 處對話泡泡（commit `ce1402d`，已推上
`Coach1973/cool-case` gh-pages 分支）。

**Why 是套進「Opus 軍師」而非最初計劃的「Claude 克勞德」**：6/23 設計時的規劃是
把案例分成「小龍蝦」跟「Claude 克勞德」兩個角色。但後續案例演進（含 Mac 新增的
28~40）把 AI 這方統一命名為「小龍蝦 AI 特助」，只剩 8 處保留「Opus 軍師」字樣，
「Claude 克勞德」這個角色名稱在目前網站上已不存在。查證後教練 2026-07-13 親口
選擇把這個頭像套進現存的「Opus 軍師」8 處，取代原計劃。

## Why 之前兩台機器都查無
檔案在 6/23 寫完後，那場對話沒有收尾 commit 就結束，此後 20 天從沒被 push 到
GitHub，所以 Mac／ACER 不管怎麼搜尋 commit 記錄都不可能查到——東西一直只在
聯想這台機器的本機硬碟上，是[[feedback_15min_commit_rule]]這條最高指導原則被
違反的真實案例。同時發現聯想本機 cool-case 的 git clone 本身也已 20 天沒
`git pull`，落後遠端 2 個 commit，已一併拉到最新。

## How to apply
以後若再有「教練記得某個設計/功能，但查 commit log 查無」的情境，除了搜尋
commit 訊息關鍵字，一定要多做一步：進到對應本機 repo 跑 `git status` 看有沒有
未追蹤或未提交的檔案——上傳這個動作可能根本沒發生，不代表東西不存在。
