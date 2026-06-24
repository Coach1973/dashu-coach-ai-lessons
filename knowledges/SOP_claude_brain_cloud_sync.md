# SOP · Claude 桌面版三機共用大腦（雲端同步記憶）

> 建立：2026-06-25 凌晨 · Mac 終端機軍師 Opus 4.8
> 緣起：教練要「聯想 / Mac / ACER 三台 Claude 桌面版共用同一份記憶」，且「雲端要記得每台機器本機存在哪」。
> 目標：解決「教練當搬運工」——三台機器的記憶自動同步，教練不必手動複製貼上任何東西。

---

## 一、白話版（教練看這段就夠）

**問題**：您三台電腦的 Claude 桌面版，記憶各記各的——這台學到的東西，那台不知道。因為每台電腦把記憶存在不同的本機資料夾，名字還跟工作目錄綁死（Mac 是一串、聯想是 `E--Claude-Data`、ACER 是 `D--Claude-Data`），天生對不上。

**解法（一句話）**：我們本來就有一個 GitHub 雲端倉庫在三台機器之間自動同步（開工自動下載、收工自動上傳）。我把「沒在同步的記憶」**接上這條本來就在跑的管線**——不必另外裝雲端硬碟、不必 iCloud、不必教練做任何搬運。

**接法**：在每台機器，把它本機的記憶資料夾換成一個「捷徑」，指向雲端倉庫裡那份**共用大腦**（`claude-brain`）。三台機器的捷徑都指向同一份，於是學到的記憶自動互通。

**雲端怎麼記住每台機器的位置**：倉庫裡有一張「機器地圖」`machines.json`，把三台機器的本機路徑都登錄起來。將來加第四台，只要在地圖加一筆、在那台跑一次安裝腳本，就接上了——還是不用您搬任何東西。

**目前進度**：Mac 這台已經接好、驗證過了。聯想（Windows）和 ACER 只要各跑一行指令就接上（指令在下面，Windows 軍師會處理，您不用動手）。

---

## 二、技術架構（給 Windows / ACER 軍師對接）

### 三個組件
| 組件 | 是什麼 | 位置 |
|------|--------|------|
| **共用大腦** | 唯一真相源，三機記憶的本體 | repo `mac-openclaw-workflows` 內的 `claude-brain/` |
| **本機橋接** | 每台機器的記憶資料夾換成捷徑指向共用大腦 | Mac=symlink、Windows/ACER=Junction |
| **機器地圖** | 登錄每台機器本機路徑（＝教練要的「雲端記住位置」）| `claude-brain/machines.json` |

### 為什麼用「既有 git repo」而非 iCloud / Google Drive
- repo **本來就在三機同步**（Mac 推 `[Mac]`、Windows 推 `[Win]`），零新基礎建設。
- 開工 hook `feed_junshi_handoff.sh` 已自動 `git pull`；收工 hook `session_end_auto_push.sh` 已自動 commit+push。**大腦掛進來就免費搭上這兩班車。**
- git 對純文字記憶檔有**版本歷史 + 自動合併 + 可回溯**，雲端硬碟做不到（且 iCloud 在 Windows 體驗差、Google Drive 會產生 `.conflict` 副本）。

### 回答 Windows 軍師原本提的三個問題
1. **路徑差異怎麼對齊** → 用「捷徑（symlink/Junction）」當轉接頭。各機本機路徑不同沒關係，捷徑一律指向 repo 內同一個 `claude-brain/`。對齊靠 `machines.json` 登錄。
2. **用什麼機制同步** → **既有的 git repo**（不是 iCloud/Drive）。免費沿用現有 pull/push hook。
3. **衝突怎麼處理** → 見第四節。

---

## 三、同步範圍（哪些記憶上雲、哪些只留本機）

| 類別 | 同步？ | 說明 |
|------|--------|------|
| `MEMORY.md` | ✅ 上雲 | 記憶索引（共用） |
| `feedback_* / project_* / reference_* / user_*` | ✅ 上雲 | 策展事實檔（共用大腦本體，目前 119 個） |
| `daily_*.md` | ❌ 只本機 | 大型逐日對話日誌（Mac 上 65 個共 12MB），各機暫存，`.gitignore` 排除 |
| `.dreams/`、`*.bak` | ❌ 只本機 | 睡眠期暫存、備份 |

> Mac 首次橋接時，原本的 `daily_*.md`（12MB）已存檔到 `memory.bak.20260625-014317`，不刪、可回溯。

---

## 四、衝突處理（Windows 軍師提的第 3 點）

| 情境 | 處理 |
|------|------|
| **同步層** | git——文字自動合併、完整歷史、可 rollback |
| **同時兩台寫同一檔** | 幾乎不可能：教練一個人、一次用一台機器 |
| **記憶設計天然防衝突** | 一檔一事實（kebab-case 一檔一個 fact），衝突只會落在單一小檔 |
| **唯一熱點 = `MEMORY.md`** | 它是常被「附加新行」的索引。附加行 git 多半能自動合併；萬一真衝突，原則是**兩行都留**（守則：存檔不刪，絕不弄丟任何一條記憶），事後人工去重 |
| **開工先 pull** | hook 已自動，確保動工前先吃到別台的最新記憶 |
| **收工自動 push** | hook 已自動，確保這台的新記憶當場上雲 |

---

## 五、首次全面上線的順序（🔴 重要：避免覆蓋掉某台的獨有記憶）

共用大腦的初始內容 = **Mac 種子**（Mac 的 `MEMORY.md` 最完整，119 個事實檔）。
其他機器接入時，安裝腳本會**先把該機原記憶備份成 `memory.bak.<時間>` 再橋接**，所以**不會弄丟**該機原有的獨有記憶——只是暫時不在共用大腦裡。

**對接後的合併動作**（Windows / ACER 軍師執行）：
1. 跑安裝腳本 → 該機接上共用大腦（原記憶已自動備份）。
2. 比對 `memory.bak.<時間>` 與共用大腦，把該機**獨有、且值得共用**的事實檔補進共用大腦、push。
3. 確認無誤、觀察幾天後，`.bak` 才可刪。

---

## 六、安裝指令（一鍵，教練零搬運）

### Mac（已完成，僅供重裝參考）
```bash
bash ~/.openclaw/workspace/scripts/setup_claude_brain.sh
```

### Windows（聯想）/ ACER — Windows 軍師執行
```powershell
# 先確保 repo 已 git pull 到最新（claude-brain 才存在）
powershell -ExecutionPolicy Bypass -File <repo路徑>\scripts\setup_claude_brain.ps1
# 若自動偵測的 repo 位置不對，加 -RepoRoot 指定，例如：
#   ...setup_claude_brain.ps1 -RepoRoot "E:\Claude-Data\workspace"
```
腳本會**自動**：偵測本機是哪台 → 備份原記憶 → 建 Junction → 驗證 MEMORY.md 讀得到。
**教練全程不需複製貼上任何路徑。**

> ⚠️ Windows 軍師注意：`machines.json` 裡 `brain_repo_root` 目前填的是推測值
> （`E:\Claude-Data\workspace` / `D:\Claude-Data\workspace`）。請確認 repo 實際 clone 在哪，
> 對接時用 `-RepoRoot` 覆蓋或回頭更新 `machines.json`。

---

## 七、可逆性（出問題怎麼還原）
任何一台要還原成「本機獨立記憶」：
```bash
# Mac
rm ~/.claude/projects/<encoded>/memory          # 移除捷徑（不會刪到共用大腦本體）
mv ~/.claude/projects/<encoded>/memory.bak.<時間> ~/.claude/projects/<encoded>/memory
```
Windows 同理（`Remove-Item` 捷徑 + `Move-Item` 還原 .bak）。

---

## 八、現狀快照（2026-06-25 凌晨）
- ✅ Mac：已橋接並驗證（symlink → claude-brain，119 事實檔）
- ✅ `claude-brain/`、`machines.json`、`.gitignore`、雙平台安裝腳本、本 SOP 皆已建立
- ⏳ Windows / ACER：待軍師跑腳本對接（教練不需動手）

---

## 相關
- 機器命名：[[reference_coach_machines_naming]]
- 拒絕當搬運工：守則 #12
- 存檔不刪：[[feedback_archive_not_delete]]
