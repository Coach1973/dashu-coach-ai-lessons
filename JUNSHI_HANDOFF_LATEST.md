# 軍師交接紙條（最新）

> 給下一個視窗的軍師：開機先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-23 凌晨（深夜工作場）
> 寫紙條的人：終端機（Sonnet，Opus 流量耗盡後接手收尾）

---

## 一句話交代這場做了什麼

**修復了三個積累已久的系統地基問題**，讓「小龍蝦學長」的工作區不再資料推來推去推到不見：
1. 特助心法.md 成功落地 Mac 主線 + 推上 GitHub
2. 1.3GB 瀏覽器垃圾（fb_session_data）從 git 歷史剔除、加入 gitignore
3. 造成「資料推來推去不見」的反向同步被砍掉

---

## 這場做了什麼（按完成順序）

### ✅ 特助心法.md 正式落地 Mac + GitHub
- 位置：`~/.openclaw/workspace/特助心法.md`
- 99 行，3538 bytes，內容來源：桌面版 HTML（`~/Desktop/頂級特助21守則_純淨版.html`）
- 已驗證零差異（對照 VPS 正典 + 桌面 HTML 五句關鍵句）
- 已推上 GitHub origin/main，`git cat-file -e origin/main:特助心法.md` 確認 3538 bytes 存在
- **原因**：2026-05-20 的部署（commit 0870160f）因後來有人整批換掉 git 歷史（兩個 disjoint root：4/10 vs 4/26）而孤立在「暫存鏈末端」，Mac 主線再也讀不到那份檔。此次重建才算補完。

### ✅ 1.3GB Chrome 瀏覽器快取清除
- 路徑：`scripts/fb_session_data/`（Chrome profile 被誤掃進 git 自動備份）
- 教練確認「垃圾還存什麼，刪掉」後才刪除（非珍貴歷史，是可再生的快取）
- 用 `git filter-branch --index-filter` 從未推的 47 筆 commit 歷史中剔除 blob
- `scripts/fb_session_data/` 加入 `.gitignore`，避免復發

### ✅ 反向同步元兇砍掉（`sync-telegram-memory.sh`）
- 原本腳本第 125-133 行有一段：rsync Claude 助教記憶 → 學長 workspace 根目錄 + git push
- 這段會把任意 .md 覆蓋到學長工作區，是「資料推來推去不見」的根因
- 已備份：`~/.openclaw/scripts/sync-telegram-memory.sh.bak-0523-0340`
- 已移除反向同步，替換成解釋性注解（說明為何不做）

### ✅ AGENTS.md 舊謊言修正
- 原文說「守則總綱.md是參考版，舊版規則檔已歸檔至_history_archive/」
- 實際上 `_history_archive/` 是空的，這是謊言
- 已改成：「守則正典只有一份：特助心法.md（21條，一字不差），舊版規則檔已退場，一律以此為準」

### ✅ 路徑大全 加入開機流程
- `~/.claude/CLAUDE.md` 自動啟動協議區段新增第 3 項：
  「找路徑／密碼／API Key 先查 `~/.openclaw/workspace/路徑大全.md`」
- **背景**：這場之前教練問「路徑大全已在開機指令了，為何還要我提供？」——確認了它不在舊版，故此場補上

---

## 🔴 現場狀態（開工必看）

### 尚未提交的檔案（教練確認是重要工具，不是垃圾）

```
M .memsearch/memory/2026-05-23.md   ← 搜尋索引/記憶日誌（4864行）
M HEARTBEAT.md                       ← 心跳記錄（含學弟 2號機資料，見下）
M state/session_counter.json         ← 對話輪數計數器
```

**這三個檔案是重要工具，開工就應該 commit 推上去。**

### HEARTBEAT.md 含學弟（2號機）資料——這是同步邊界的問題
- HEARTBEAT.md 裡面記錄的心跳是「2號機，小龍蝦學弟，服務孔大哥」的記錄
- 學弟資料出現在學長 workspace → 說明同步邊界還有漏洞
- 這個問題這場發現了但沒時間修，下場要查：學弟的 .openclaw-peipei 有沒有 git remote 也是學長的 GitHub？

### 未竟事項

| 優先 | 任務 |
|------|------|
| 🔴 高 | commit 三個已修改但未提交的檔案（.memsearch、HEARTBEAT、session_counter） |
| 🔴 高 | 寫本場 SESSION 記錄檔（claude-sessions/SESSION_2026-05-23_*.md） |
| ✅ 已完成 | 路徑大全.md 加上特助心法.md 正典條目 |
| ✅ 已完成 | 修 CLAUDE.md 中 `執行細則.md` 的殭屍引用（已移除，改為兩份正典） |
| ✅ 已完成 | feedback_archive_not_delete.md 已加進 MEMORY.md 索引 |
| 🟠 低 | 追查 HEARTBEAT.md 學弟資料為何出現在學長 workspace（同步邊界漏洞） |
| 🟠 低 | 確認學弟/學妹各自 .git remote 不指向學長的 GitHub repo |

---

## 這場教練親自糾正的教訓（下場必銘記）

1. **資料處置：預設「存檔」不是「清除」**
   - 教練從頭到尾說「歷史存檔」，我說成「清掉/清除」被當場擋
   - 唯一例外：教練親自確認是「可再生垃圾」後才刪（此場 1.3GB Chrome 快取）

2. **不要把「看起來像雜訊的工具」當垃圾**
   - HEARTBEAT.md、session_counter.json、.memsearch 索引被我標為「自動同步雜訊」
   - 教練：「教練不會無緣無故要求要有一個 Session 東西，搜尋索引也不會無緣無故存在」
   - 要讀內容、理解用途，再判斷，不憑格式猜

3. **特助心法.md 從來不是「從未建立」**
   - 2026-05-20 有 commit（0870160f，13:19:07）確實建立過
   - 後來 git 歷史被整批替換（disjoint root），那個 commit 孤立了
   - 說「從來沒被建出來過」是錯的，要查証再說

---

## 給下一個軍師的提醒

- **教練是電腦小白**：說人話，禁用 git/cron/relay/repo 等行話，必須用中文解釋
- **不要替教練做選擇**：方向模糊就問，但方向清楚就直接做，不問「要做嗎」
- **承諾鐵律**：口頭說「完成」= 零；commit hash 才算
- **判斷力護欄**：不可逆動作（刪檔/push --force/對外發布）先問教練
- **特助心法.md 是唯一正典**（守則 21 條，一字不差），CLAUDE.md 裡的 21 條精華版只是提醒索引
