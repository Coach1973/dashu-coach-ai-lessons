# SOP · Windows / Mac / VPS 軍師雙邊協調規約 v1.0

> 建立：2026-06-17（下午 1:10 台灣時間）
> 建立人：Mac 軍師 Opus 4.7（與 Windows 軍師對齊後簽署）
> 目的：教練主要在 Windows 工作，Mac 為資料倉庫與 OpenClaw 駐點。本 SOP 規範雙邊軍師如何共享同一條品牌時間軸，不打架、不漏接。

---

## 🌐 共用倉庫真相

| 項目 | 內容 |
|------|------|
| GitHub repo | `https://github.com/Coach1973/claude-workflows.git` |
| 分支 | **單一 `main`**（雙方都 push） |
| Mac 路徑 | `~/.openclaw/workspace/` |
| Windows 路徑 | `C:\Users\bymyw\.openclaw\workspace\` |
| 軍師大腦範圍 | 接力棒、特助心法、執行細則、memory/、knowledges/、distill/、SOP、HEARTBEAT.md |

---

## 📜 守則正本（唯一真相）

- **`workspace/特助心法.md`** — 21 守則完整版 + 教練親筆詮釋
- **`workspace/執行細則.md`** — E01~E12 執行框架
- 引用必須一字不差，禁止自行詮釋（守則 #21）
- 注意：`terminal-notes/TOP_ASSISTANT_RULES_v3_final.md` 不存在，R18 / R19 是 5/16 廢版命名，**勿引用**

---

## 🚀 開工 SOP（兩邊通用）

```
1. cd 到 workspace
2. git pull origin main
3. 讀 JUNSHI_HANDOFF_LATEST.md（接力棒）
4. 讀 HEARTBEAT.md（系統狀態）
5. 讀 knowledges/ 最新建立的計劃檔（如有）
6. 讀 memory/YYYY-MM-DD.md 最新一份
7. 第一句回應教練：身份核對 + 上場戰果 + 當下主軸 + 雲端 commit 前 7 碼
```

教練說「開工」即觸發。

---

## 🏁 收工 SOP（兩邊通用）

```
1. 改寫 JUNSHI_HANDOFF_LATEST.md（覆寫接力棒，內容包含「本場戰果 / 下一棒待辦 / commit hash / 限流剩餘 %」）
2. 必要時追記 memory/YYYY-MM-DD.md（用 ### HH:MM 子標題附加，禁止覆蓋既有段落）
3. git add → git commit → git push origin main
4. 告知教練本場 commit hash + 限流剩餘 %
```

---

## 🏷️ commit 訊息格式

**前綴標源 + 動作 + 摘要**：

| 前綴 | 來源 | 範例 |
|------|------|------|
| `[Win]` | Windows 桌面版軍師 | `[Win] cron: 修 jiesheng 早鳥按鈕` |
| `[Mac]` | Mac 終端機/桌面版軍師 | `[Mac] 接力棒 v27：今日 3 件事` |
| `[VPS]` | VPS 端（如有） | `[VPS] 修 docker exec 路徑` |
| 無前綴 | Mac 端 cron 自動寫入（auto-backup / 蒸餾） | 維持原狀 |

---

## ⚖️ 衝突防護

### 大原則
**兩邊不同時開場**——教練同時間只跟一邊對話，另一邊靜默。

### 技術防線
- 開工必 `git pull`，收工必 `git push`
- conflict marker 出現 → **保留兩段內容**讓教練裁決，禁止 `git push --force`

---

## 📋 memory/ 寫入規約

- **檔名**：`YYYY-MM-DD.md`（台灣時區 Asia/Taipei）
- **主要寫手**：Mac 端 cron（每 4 小時蒸餾終端機對話 → 寫入 distilled/，再彙整入 memory/）
- **Windows 補記**：用 `### HH:MM Windows 軍師補記` 子標題附加，不覆蓋既有段落
- **禁止**：跨日改前一天的 memory（除非教練親口要求修正）

---

## 💓 HEARTBEAT.md 寫入規約

- **獨家寫手**：Mac 端 cron（relay_poll 每分鐘、heartbeat_audit 每天 23:50）
- **Windows 完全不寫**——Windows 軍師的工作軌跡會直接出現在 commit log 與接力棒，不需要 HB 紀錄
- 對應守則 #19 心跳必須有意義：審計腳本 `workspace/scripts/fix-p0-findings.sh` 自動巡邏，連 2 筆純 OK 會強制下一筆要做實質任務

---

## ✅ Windows 軍師能做的（雲端任務）

- 網頁推 SOP（GitHub repo push + Netlify zip+API）
- GitHub 推送（PR / release）
- Netlify 站台維護（22 個站）
- VPS ssh 修復（Hermes 113.29.232.178 / 小龍蝦 43.245.60.200）
- 接力棒撰寫與交接
- WordPress 改設定
- 蒸餾 / 整理 workspace 文件

## ❌ Windows 軍師不做的（要派回 Mac）

- OpenClaw cron 設定（macOS launchd / crontab，Mac 專屬）
- Telegram Mac 端訊息快取讀取
- 本機照片 / 影片素材操作（在 Mac）
- LaunchAgents（macOS 專屬）
- 三隻小龍蝦 gateway 操作（Mac 跑：1號 18789 / 2號 18793 / 3號 18790）
- `~/.openclaw/openclaw.json` 改模型設定（鐵律：教練親口授權才能動）

---

## 🚫 永遠不同步的檔案（雙邊各自獨立）

| 項目 | 原因 |
|------|------|
| `~/.openclaw/cron/jobs.json` | Mac OpenClaw daemon 專屬，同步會打架（案例 23 等級災難） |
| `~/.openclaw/agents/` | 同上 |
| `~/.openclaw/openclaw.json` | 同上 |
| `~/.claude/projects/.../memory/`（Claude Code 自動記憶） | 各 session 短期記憶，互通會污染。共用真相走 `workspace/memory/` |
| `~/Library/...`（macOS 系統路徑） | macOS 專屬，Windows 用不到 |

---

## 🔑 雙邊核心燒錄檔同步

- **正本**：`workspace/CLAUDE.md`（由 `scripts/sync_handoff_to_claudemd.sh` 自動鏡像最新接力棒）
- **Mac 鏡像位置**：`~/.claude/CLAUDE.md`
- **Windows 鏡像位置**：`%USERPROFILE%\.claude\CLAUDE.md`
- **同步方式**：每次更新 workspace 後手動 copy 一次（CLAUDE.md 結構穩定，不會常變）

---

## 📌 限流回報文化

接力棒結尾必有：

```
## 📌 本場限流狀態（給教練看）
- 本場開始：剩 XX%
- 本場結束：剩 XX%
- 下次重置：YYYY-MM-DD HH:MM
```

讓另一邊軍師接棒時知道可用空間。

---

> 簽署：Mac 軍師 Opus 4.7（2026-06-17 下午 1:10 台灣時間）
> 待簽署：Windows 軍師（請 Windows 軍師讀完後寫入個人記憶 `feedback_kickoff_protocol.md`，並回報「已簽署 v1.0」）
