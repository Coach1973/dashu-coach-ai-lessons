---
name: reference_vps_disk_81g_git_pack_pileup_2026-10-28
description: VPS 小龍蝦硬碟用 81G 的真因＝工作區 .git 堆 650 個 pack（47G），因 .git 有 root 擁有的檔讓 node 的 gc 一直失敗；清法與驗證（降到 25G）
metadata:
  node_type: memory
  type: reference
  originSessionId: b5a7e32d-14e5-4bf2-bd7c-bfc70eda2bf4
  modified: 2026-10-28T08:26:39.364Z
---

VPS（43.245.60.200）容器 openclaw 的工作區 `/root/openclaw/data/workspace` 是 GitHub 倉庫 mac-openclaw-workflows 的複本，cron 每 15 分鐘在容器內 `git pull origin main`。

**真因（查到的）**：`.git` 內有 21 個 root 擁有的檔案／目錄（refs/remotes/origin、幾個 pack、commit-graph），容器內 node 使用者建不了 ref 鎖，自動 gc 一直 `task 'gc' failed`；每次 fetch 都多留一個 pack，累積 650 個、47G。`git pull` 自 9/24 起一直 `divergent branches`（16252 次失敗，本機領先 96 筆），VPS 工作區停在 9/24，這件沒動。

**清法（2026-10-28 已做並驗證）**：
- `chown -R 1000:1000 .git` → 容器內 `git repack -a -d --window=0`（低記憶體）→ 47G 變 528MB，fsck 通過
- journal、apt 快取、容器內 pip／npm 快取、session 備份只留最新 7 份、舊升級備份刪可再生目錄（agents／memory／設定／媒體都留）
- 備份保留 cron 由 +30 天改 +7 天
- 重啟容器釋放 Gateway 記憶體（swap 1059MB→56MB）
- 結果：硬碟 81G→26G

**坑**：`rm -rf "$B/$d"` 這種變數路徑會被 Claude Code 安全檢查擋，改寫成絕對路徑逐條刪。

**還沒做**：①VPS `git pull` 分歧要不要處理（會把 Mac 倉庫大量內容併進對外版，教練未裁示）②`node-llama-cpp` 缺少（向量記憶 36 次失敗，重啟後 15 分鐘內 0 次，未補裝）③「幕僚長晨報」在 VPS 排程找不到。

Related: [[reference_launchagents_plists_deleted_outage_2026-10-16]]
