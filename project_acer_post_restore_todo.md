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
4. **Zoom 重新安裝**：從 zoom.us 下載安裝，裝完直接跑步驟 1 的腳本，`data/logs/reports` 會自動 junction 回 D 碟舊資料（2026-07-02 起改法：bin/程式本體留在 C 碟不搬，只 junction 增量資料，不用像以前整包搬）
5. **瀏覽器/通訊軟體**：Chrome、GanJing、LINE、Telegram 現在都已改成「只 junction User Data/Data/Cache/tdata，程式本體留 C 碟」，跑完步驟 1 的腳本應該會自動接回 D 碟資料。若程式本體本身也在還原時被清空（不在還原點快照裡），才需要重新安裝，裝完再跑一次步驟 1 的腳本即可，不用整包重搬
6. **拉取最新記憶**：
   ```
   cd ~/Documents/mac-openclaw-workflows && git pull origin main
   ```

### 注意事項
- 瀏覽器/通訊軟體（Chrome、GanJing、Perplexity、LINE、Telegram）**絕對不能整包 AppData 做 junction**，只能 junction User Data/Data/Cache/tdata 這類 profile 子資料夾，程式本體資料夾永遠留 C 碟，見 [[browser-no-full-junction]]
- Perplexity（Comet\User Data）截至 2026-07-02 尚未實際搬移，D 碟來源不存在會自動 SKIP，之後要搬比照 GanJing 做法
- 完成後清理 C 碟 7 天前的 .bak 資料夾
- 每次搬移前先確認清楚該軟體「程式本體」跟「使用者資料」實際分別放在哪個資料夾（別用猜的），只 junction 使用者資料那層

Related: [[browser-no-full-junction]], [[openclaw-spool-stuck-fix]]
