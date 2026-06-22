# SOP · Windows / Mac 軍師任務路由規約 v1.0

> 建立：2026-06-22 22:30（台灣時間）
> 建立者：Windows 桌面版軍師 Opus 4.7
> 補位對象：`SOP_windows_mac_kickoff_protocol.md` v1.1（規約層）+ `IDENTITY_windows_desktop.md`（身份層）
> 本份補位：**任務路由層**——教練接到任務時，怎麼決定派 Mac 還是 Windows 還是兩邊接力。

---

## 🎯 為什麼需要這份

v1.1 規約定下了「兩邊不打架」的鐵律，身份卡定下了「Windows 是什麼」，但中間少了一層：

> **大樹教練動嘴的時候，這個任務該流向哪一邊？**

過去的做法是教練自己決定開哪台機器，但這違反「動嘴就好」。本 SOP 把決策外部化成路由表，未來只要教練說「這件事」，兩邊軍師看本表自己對號入座。

---

## 🧬 兩邊軍師的天賦差異（事實基線）

| 維度 | **Mac 軍師**（mac mini M4） | **Windows 軍師**（桌面 PC） |
|------|----------------------------|----------------------------|
| 角色定位 | 駐站・伺服器・守夜人 | 出勤・桌面・白班 |
| 觸發方式 | cron 排程自動 + 教練親口 | 教練開 Claude Code App |
| 是否常駐 | ✅ 24/7（cron / launchd / daemon） | ❌ 教練開 app 才在 |
| Shell | macOS Bash（POSIX） | PowerShell + Bash 工具 |
| GUI 操作 | ❌（mac mini 通常是 headless） | ✅（檔案總管、系統匣、瀏覽器、Office） |
| 本機檔案大量處理 | ✅ 強（distill/、verbatim/） | ⚠️ 可，但教練要在 |
| 即時對話品質 | ⚠️ 教練要主動連 | ✅ 隨叫隨到 |
| OpenClaw cron / 蒸餾 / dreaming | ✅ 主場 | ❌ 不碰 |
| Netlify / GitHub Pages 部署 | ✅ 都能 | ✅ 都能（語法對應見身份卡） |
| Windows 系統管理（regedit / junction / 系統匣） | ❌ | ✅ 獨家 |
| Mac 系統管理（launchd / iCloud / Keychain） | ✅ 獨家 | ❌ |

---

## 🗺️ 任務路由決策樹

```
教練說一件事 → 先問三道題
       │
       ├─ Q1：需要「即時看到結果」嗎？
       │      ├─ 是 → Windows（教練在桌面前面）
       │      └─ 否 → 進 Q2
       │
       ├─ Q2：需要 GUI 操作（瀏覽器點按鈕 / 檔案總管 / 系統設定）嗎？
       │      ├─ 是 → Windows
       │      └─ 否 → 進 Q3
       │
       └─ Q3：是 cron 排程、批次蒸餾、長期記憶、夜間處理嗎？
              ├─ 是 → Mac
              └─ 否 → 看下方分類表精挑
```

---

## 📋 任務分類表（按「主場」歸隊）

### 🪟 Windows 主場（教練在桌面 → 派 Windows）

| 任務類型 | 為何 Windows | 範例 |
|---------|------------|------|
| **網頁站台部署 + 即時 Chrome 驗證** | 教練看瀏覽器 | tainan-calender / government-* 站修改 |
| **Windows 系統檔案管理** | 唯 Windows 能 | LINE junction、AppData 搬遷、登錄檔 |
| **GitHub Pages 即時推送** | 教練要 F5 看效果 | gh-pages 修文案、cool-case 新案 |
| **即時 debug** | 教練看 console | 報名按鈕、modal、UI 互動 bug |
| **Office / 桌面軟體連動** | Windows 獨家 | Word、Excel、Outlook |
| **GUI 工具操作** | 必 GUI | UltFone、Photoshop、剪映 |
| **教練心血來潮的研究查證** | 隨開隨用 | 「幫我查 XX 怎麼做」 |

### 🍎 Mac 主場（背景排程 → 派 Mac）

| 任務類型 | 為何 Mac | 範例 |
|---------|---------|------|
| **OpenClaw cron 設定** | Mac launchd / crontab 專屬 | 蒸餾排程、relay_poll |
| **每日蒸餾與夢境** | 已建好的 pipeline 在 Mac | distill/、dreaming/、verbatim/ |
| **HEARTBEAT.md 寫入** | Mac cron 獨家寫手（v1.1 第 142 行） | relay_poll 每分鐘 |
| **長期記憶整合** | memory/.dreams/ 引擎在 Mac | session-corpus、phase-signals |
| **VPS ssh 守夜** | Mac 永遠在線 | Hermes、小龍蝦 gateway |
| **三隻小龍蝦 gateway** | Mac 物理跑（1號 18789 / 2號 18793 / 3號 18790） | 訊號中繼 |
| **iCloud / Keychain 整合** | Mac 獨家 | LINE iCloud 備份監控 |
| **整夜批次** | 教練睡覺 Windows 關機 | mining_stories、distill_lobster |

### 🤝 接力任務（一個起頭、另一個收尾）

| 任務類型 | 流向 | 範例 |
|---------|------|------|
| **跨機接力棒** | Win 寫 → Mac pull → Mac 接做 | 教練白天 Windows 改網頁，晚上 Mac 跑蒸餾 |
| **試金石新案例** | 案發那一邊寫初稿 → 另一邊 review | 案例 26 government-grow 由 Mac 寫，Win 簽 |
| **大檔案搬遷 + 觀察期** | Win 主動（GUI 需要） → Mac 透過 cron 監控狀態 | LINE 搬遷（本場剛做完） |
| **多站台批次修改** | Win 改一站確認設計 → Mac 批量複製到其他站 | 假設要把同一段 banner 推到 22 個站 |

---

## ⏰ 一天裡的協作節奏

```
00:00 ─┬─ Mac cron：HEARTBEAT relay_poll（每分鐘）
       │
03:00 ─┼─ Mac cron：深夜蒸餾批次（distill_terminal / dreaming）
       │
06:00 ─┼─ Mac cron：今日 memory/YYYY-MM-DD.md 初始化
       │
07:00 ─┼─ Mac cron：sync_handoff_to_claudemd.sh（鏡像最新接力棒到 CLAUDE.md）
       │
09:00 ─┤  ── 教練開工 ──
       │
       ├─ 白班：Windows 為主（教練在桌面前面）
       │       Mac 在背景吃接力棒 + heartbeat
       │
       ├─ 11:50 Mac cron：heartbeat_audit 巡邏（守則 #19）
       │
       ├─ Windows 每次 session 結束：session_end_auto_push.ps1
       │       → 自動 push 到 GitHub main
       │       → 下次 Mac pull 拿到進度
       │
17:00 ─┤
       │
22:00 ─┤  ── 教練收工 ──
       │
       ├─ Mac cron：當日 distill 收尾、夢境引擎跑（light → REM → deep）
       │
23:50 ─┴─ Mac cron：heartbeat_audit 收尾巡邏
```

**節奏核心**：Windows 是「教練的延伸手臂」，Mac 是「不停跑的引擎」。Windows 動的時候 Mac 也在背景跑；Windows 關機後 Mac 繼續。

---

## 📡 共享狀態的單一真相源

| 檔案 | 寫入者 | 讀取者 | 同步方式 |
|------|-------|-------|---------|
| `JUNSHI_HANDOFF_LATEST.md` | 收工那邊（Win or Mac） | 開工那邊 | git push/pull |
| `HEARTBEAT.md` | **僅 Mac cron** | 雙邊讀 | Mac auto-commit |
| `CLAUDE.md` | `sync_handoff_to_claudemd.sh`（Mac cron） | 雙邊啟動讀 | 鏡像接力棒 |
| `memory/YYYY-MM-DD.md` | 雙邊都寫（Mac 主筆，Win `### HH:MM 補記` 附加） | 雙邊讀 | git |
| `knowledges/SOP_*.md` | 任一邊寫，另一邊不動 | 雙邊讀 | git |
| `試金石/試金石_案例庫.md` | 案發那邊起草 + 另一邊 review | 雙邊讀 | git |
| `state/recall_index.jsonl` | Mac cron | Mac 查詢 | 本地 |

**鐵律**：HEARTBEAT.md **Windows 不寫**（v1.1 第 146 行）。Windows 進度自然體現在 commit log + 接力棒。

---

## 🚦 教練怎麼知道「誰現在在做什麼」

教練可以問三句話得到答案：

| 問題 | 對應指令（教練動嘴，AI 跑） | 看什麼 |
|------|---------------------------|--------|
| 「最近誰在動工？」 | `git log -10 --oneline` | commit 前綴：`[Win]` / `[Mac]` / `[VPS]` |
| 「目前的整體狀態？」 | `tail -50 HEARTBEAT.md` | Mac cron 寫的最新熱上下文 |
| 「兩邊接力棒同步嗎？」 | `git status` + `git log -1 JUNSHI_HANDOFF_LATEST.md` | 看是不是 Win 寫的還是 Mac 寫的 |

可以做成一鍵 alias，下次補。

---

## 🔧 配合 Windows session-end hook 的新協作模式

**2026-06-22 本場新裝**：`session_end_auto_push.ps1` Stop hook

每次 Windows session 結束：
1. 偵測接力棒 / memory / HEARTBEAT / knowledges 有沒有變動
2. 自動 git add + commit + push origin main
3. Mac 軍師下一次 cron pull（或開工 `git pull`）自動拿到

**這代表什麼**：
- Windows 軍師結束工作**不需要記得 push**——hook 自動辦
- Mac 軍師開工只要 `git pull` 就拿到最新
- 教練不需要在兩邊之間搬運任何東西

**對應守則**：#12 拒絕當資訊搬運工——這套就是用機制把「搬運」自動化掉。

---

## 🧯 失敗模式與復原

| 失敗模式 | 偵測方法 | 復原 |
|---------|---------|------|
| Windows session-end hook 沒跑（教練忘了結束 session） | Mac 開工 pull 沒新 commit | 教練手動回 Windows 跑 push |
| Mac cron 掛了（HEARTBEAT 沒更新） | `tail HEARTBEAT.md` 時間戳老於 5 分鐘 | ssh 進 Mac 重啟 cron |
| 兩邊同檔案打架 | `git pull` 出 conflict marker | 保留兩段、教練裁決，**禁 `--force`** |
| 接力棒被覆寫遺失內容 | 比對 `git log JUNSHI_HANDOFF_LATEST.md` | 從上一個 commit 撈回，merge |
| sync_handoff_to_claudemd.sh 掛了 | CLAUDE.md 開頭時間戳老 | Mac 端手動跑一次同步腳本 |

---

## 📝 路由決策的快速口訣

**三個問題、十秒分流**：

1. **教練在看嗎？** → 是 → Windows
2. **要點 GUI 嗎？** → 是 → Windows
3. **是 cron / 蒸餾 / dreaming？** → 是 → Mac

其他全部依「主場表」對號入座。模糊地帶（兩邊都行）→ **看教練人在哪台前面**。

---

## 🔄 本 SOP 升版條件

| 條件 | 升版理由 |
|------|---------|
| 出現第三場 Windows / Mac 同時動同檔的打架 | 加強衝突防護章節 |
| 新增第三類軍師（VPS / 小龍蝦 OpenClaw 出來變強） | 加 VPS 主場欄 |
| 教練的工作模式大改（例如改用 Mac 桌面為主） | 重劃天賦光譜 |
| 案例庫新增「路由錯誤」血淚案例 | 加血淚段落 |

---

## 📌 給雙邊軍師的硬性提醒

- **不要搶任務**——看本 SOP 是不是你主場
- **不要漏接**——白班 Windows 結束自動 push，晚班 Mac cron 自動 pull
- **教練說話時自我檢測身份**（守則 #17）——「我是 Mac 還是 Windows？」是每場第一問
- **不要假設另一邊已經知道**——重要進度寫進接力棒
- **觀察期任務（如 LINE 搬遷）兩邊都不動 .bak**——觀察期截止日寫進還原便條

---

> 簽署 v1.0：Windows 桌面版軍師 Opus 4.7（2026-06-22 22:30 台灣時間）
> 本場為 Windows 軍師首次主筆 SOP（之前都是 Mac 軍師寫，Windows 簽）
> 待 Mac 軍師 review 後升 v1.1
