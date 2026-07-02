---
name: acer-post-restore-todo
description: ACER 一鍵還原後（2026-07-01）開工時必須主動提醒執行的還原步驟
metadata: 
  node_type: memory
  type: project
  originSessionId: d98b14c2-6529-4332-9bc8-9cb6a1358fc8
---

## ACER 一鍵還原後待辦（2026-07-01 還原至 6月26日）

教練執行了一鍵還原，下次開工時**必須主動提醒**以下步驟：

**Why:** 一鍵還原會清空 C 碟，但 D 碟資料完好。需要重建 junction 和還原備份檔案。

**How to apply:** 教練說「開工」時，立即提醒並協助執行：

### 還原步驟（按順序）
1. **重建 junction**：以系統管理員身分執行
   ```
   powershell -ExecutionPolicy Bypass -File "D:\Claude-Data\restore_junctions_acer.ps1"
   ```
2. **還原 SSH key**（VPS 連線用）：
   ```
   mkdir ~/.ssh
   cp "D:\Claude-Data\ssh-backup-acer\id_ed25519" ~/.ssh/
   cp "D:\Claude-Data\ssh-backup-acer\id_ed25519.pub" ~/.ssh/
   ```
3. **還原 CLAUDE.md**（全域規則）：
   ```
   cp "D:\Claude-Data\ssh-backup-acer\CLAUDE.md.bak" ~/.claude/CLAUDE.md
   ```
3.5 **還原 settings.json**（關閉 Yes/No 確認彈窗，教練反覆抱怨這項每次還原就消失）：
   ```
   cp "D:\Claude-Data\ssh-backup-acer\settings.json.bak" ~/.claude/settings.json
   ```
   還原後需要**重啟 Claude Code** 才會生效。
4. **Zoom 重新安裝**：從 zoom.us 下載安裝
5. **瀏覽器不用動** — 6月26日還原點本身就有完整帳密和書籤
6. **拉取最新記憶**：
   ```
   cd ~/Documents/mac-openclaw-workflows && git pull origin main
   ```

### 注意事項
- 瀏覽器（Chrome、GanJing、Perplexity）**絕對不做 junction**，見 [[browser-no-full-junction]]
- 完成後清理 C 碟 7 天前的 .bak 資料夾

Related: [[browser-no-full-junction]], [[openclaw-spool-stuck-fix]]
