---
name: project-amber-smb-login-git-backup-in-progress-2026-11-06
description: Amber 掛載帳號是 bymyway7（不是 amber-Coach）；11/06 .git 25G 備份到 SSD+Amber 進行中、305G 用量報告、時光機 244G 空殼待壓縮
metadata:
  node_type: memory
  type: project
  originSessionId: 3911ece3-1706-4159-a358-f1bddb025b24
  modified: 2026-11-06T05:46:41.187Z
---

11/06 下午（kai-2d6c69 worktree 對話）進度，接力棒被 worktree 守衛擋住沒寫成，改記在這：

- 已刪 `Claude-3p/vm_bundles` 11G（教練口頭授權），本機可用 31G→42G。
- **Amber 掛載要用帳號 `bymyway7`**（AmberCloud email 前半，Amber 後台「檔案服務」頁寫明）。`amber-Coach` 是主機名，用它會 Authentication error。鑰匙圈存的帳號就是 bymyway7。掛載點暫為 `~/amber-mnt`、`~/amber-Videos` 等，**不是** `/Volumes/home`（名片辨識監看程式若寫死 /Volumes/home 仍看不到）。mount_smbfs 密碼要 URL 編碼；macOS 沒有 `timeout`，用 `perl -e 'alarm N; exec @ARGV'`。
- `.git` 25G 備份：SSD 份完整（`/Volumes/953-SSD/Mac應用資料/openclaw-git-backup-20261106/.git`，13:21 完成）；Amber 份（`~/amber-mnt/大樹大腦備份/openclaw-git-backup-20261106/.git`）背景 rsync 進行中，第一次跑到 1.5G 就莫名中斷、重啟過。**核對（檔案數／大小／git fsck）通過前不准刪本機 .git。**
- Amber 305G：TimeMachine sparsebundle 244G（時光機自己算只用 135G、只有 10/29、10/30 兩個備份點、上限 150G；推論多的約 109G 是空殼要 hdiutil compact，未證實未動；結果代碼 56 未查）、Videos 20G（2024 課程影片，教練說重要不動）、其餘小；約 40G 來源未查明。
- 教練裁示：SSD 掉線半年才一次，別再拿來問；時光機只留最近幾次穩定備份。

**Why:** 教練要清出本機空間（目標約 49G）。**更新 14:30：** .git 已搬到 SSD（本機是捷徑，另有 Amber 保險備份），本機刪完可用 71G；名片辨識系統早已全在 Mac 本機、Amber 名片媒合中心已刪。接力棒已寫（commit a63128b32）。剩：時光機壓縮實測、舊監看 plist 清理。
**How to apply（舊，僅供參考）:** 開工先看 Amber 份 rsync 是否完成並核對，再問教練能否刪本機 .git（改捷徑指 SSD）；Chrome 5.9G 搬 SSD 要先關 Chrome。
