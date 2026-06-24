---
name: project-claude-brain-cloud-sync
description: 三機（Mac/聯想Windows/ACER）Claude 桌面版記憶雲端共用大腦上線 2026-06-25；.claude/projects 記憶接 git repo 同步，解決教練當搬運工
metadata:
  type: project
---

# 三機共用大腦（Claude 桌面版記憶雲端同步）2026-06-25 上線

教練要「三台 Claude 桌面版共用同一份記憶，雲端記住每台本機位置」，解決教練當搬運工。

**根因**：`~/.claude/projects/<encoded>/memory/` 每台機器路徑不同（Mac=`-Users-bymyway--openclaw`、聯想=`E--Claude-Data`、ACER=`D--Claude-Data`）且原本完全沒同步（`~/.claude` 不是 git repo）。

**解法**：不另起爐灶——接上「已在三機同步的 git repo」（mac-openclaw-workflows）。
- 唯一真相源：`workspace/claude-brain/`（種入 119 個策展事實檔）
- 各機把 `.../memory` 換成捷徑（Mac=symlink、Windows=Junction）指向 claude-brain
- 機器地圖：`claude-brain/machines.json` 登錄三機本機路徑＝雲端記住位置
- 同步沿用既有 hook：開工 `feed_junshi_handoff.sh` 自動 pull、收工 `session_end_auto_push.sh` 自動 push
- `daily_*.md`/`.dreams`/`*.bak` 用 .gitignore 排除，只留本機

**衝突處理**：git 文字合併；一人一次一機幾乎不撞；熱點 MEMORY.md 採附加行、真衝突兩行都留（存檔不刪）。

**狀態**：Mac ✅ 已橋接驗證（commit `11063998`）；聯想/ACER 待軍師跑 `scripts/setup_claude_brain.ps1` 對接（教練零搬運）。

**首次對接鐵律**：腳本先備份該機原記憶成 `memory.bak.<時間>` 再橋接，避免覆蓋獨有記憶；事後人工比對合併、觀察數天才刪 .bak。

完整 SOP：`knowledges/SOP_claude_brain_cloud_sync.md`。
相關：[[reference_coach_machines_naming]]、[[feedback_archive_not_delete]]、守則 #12 拒絕搬運工。
