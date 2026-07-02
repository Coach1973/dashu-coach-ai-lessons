---
name: acer-post-restore-todo
description: ACER 一鍵還原後（任何還原點，含2026-07-01/2026-05測試）開工時必須主動提醒執行的還原步驟
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
0. **修復 `~/Documents/mac-openclaw-workflows` 本機路徑**（2026-07-03 發現：這是 C 槽真實資料夾，不是 junction，還原後極可能消失或變成舊版本，開工自動 git pull 會失效）：
   ```
   powershell -Command "Test-Path $env:USERPROFILE\Documents\mac-openclaw-workflows"
   ```
   不存在就 `git clone https://github.com/Coach1973/mac-openclaw-workflows.git ~/Documents/mac-openclaw-workflows`，存在但太舊就直接 `git pull origin main`
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
5. **瀏覽器/通訊軟體**：Chrome、GanJing、LINE、Telegram、Perplexity(Comet) 現在都已改成「只 junction User Data/Data/Cache/tdata，程式本體留 C 碟」，跑完步驟 1 的腳本應該會自動接回 D 碟資料。若程式本體本身也在還原時被清空（不在還原點快照裡），才需要重新安裝，裝完再跑一次步驟 1 的腳本即可，不用整包重搬
6. **拉取最新記憶**：
   ```
   cd ~/Documents/mac-openclaw-workflows && git pull origin main
   ```

### 注意事項
- 瀏覽器/通訊軟體（Chrome、GanJing、Perplexity、LINE、Telegram）**絕對不能整包 AppData 做 junction**，只能 junction User Data/Data/Cache/tdata 這類 profile 子資料夾，程式本體資料夾永遠留 C 碟，見 [[browser-no-full-junction]]
- Perplexity（Comet\User Data）2026-07-03 已搬移完成。特殊狀況：發現它的程式本體（Comet\Application、CometUpdater、Update）之前被舊版整包搬移邏輯放到 D 碟去了（桌面/工作列/開始功能表捷徑全部指向 D 碟），已全部搬回 C 碟並修正 4 個捷徑指向。以後每個軟體搬移前都要先查捷徑實際指向哪裡，不要假設程式本體一定在 C 碟
- 完成後清理 C 碟 7 天前的 .bak 資料夾
- 每次搬移前先確認清楚該軟體「程式本體」跟「使用者資料」實際分別放在哪個資料夾（別用猜的），只 junction 使用者資料那層

Related: [[browser-no-full-junction]], [[openclaw-spool-stuck-fix]]
