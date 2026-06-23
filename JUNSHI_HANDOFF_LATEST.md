# 軍師接力棒 · 2026-06-23 v32（Mac 終端機 Opus 4.7）

> 建立時間：2026-06-23 上午 10:30（台灣時間）
> 本棒執行者：Mac 終端機軍師 Opus 4.7
> 上一棒：v31（Windows 桌面版 Opus 4.7，凌晨 4:15 結束）
> 本棒主軸：**雙邊 hook v2/v3 升級 + 助理筆電 LINE 搬遷 + ACER bootstrap + 機制體檢補位**
> 本場時長：約 1 小時（上午 09:23 ~ 10:30）
> 場序：教練上午 6 點高鐵到台北上課，1 小時睡眠後動嘴指揮——短場高密度

---

## 🎯 本場戰果（按時間順序）

### 1. ✅ 接力棒 hook v2/v3 升級（六步驟全注入）

教練早上開工時看到「路徑寫錯重來」——指出真根因不是路徑沒講好，是我憑 cwd 直覺拼路徑沒先 `ls` 驗證。

**動工**：
- Mac `feed_junshi_handoff.sh` v2 + Windows `feed_junshi_handoff.ps1` v3
- 開工時自動注入：接力棒 + HEARTBEAT 最近 50 行 + 試金石最新 3 案 + knowledges 近 7 天清單 + memory 最新日
- Mac 版補上 `git pull` 邏輯（跟 Windows v2 對齊）
- **commit `5dd2ebfa`** 已 push

### 2. ✅ 助理筆電 LINE C→D 搬遷 SOP（衍生自 6/18 E 槽版）

教練人在台北，借助理 ACER 同款筆電做 LINE 搬遷。寫了：
- `knowledges/SOP_line_migrate_to_d_drive.md`（298 行，commit `012a3341`）
- 已內建案例 27 兩個盲點修復：**捷徑 Object ID 重建（階段 4）+ 沙箱誤判規避**（階段拆 4 個獨立呼叫）

### 3. ✅ Secret gist 繞道（助理筆電取 SOP）

新筆電 git clone 失敗——repo 是 PRIVATE，新筆電無 credential。
解法：建 **secret gist**（URL 知道才能看，不被 Google 索引）：
- Gist URL: `https://gist.github.com/Coach1973/e1990e87fbac462a801570710ae897fb`
- 教練貼一段給新筆電 CLI 軍師（含 `Invoke-WebRequest` 一行）→ 拉 SOP 到 D 槽

新筆電 CLI 軍師執行成功，正在跑階段 1 診斷。

### 4. ✅ 機制體檢報告（Ultra 等級）

教練親口要求做「分工/任務/流程體檢」。
產出健康燈號表 + 短/中/長期問題分層 + 真心話（教練熬夜+1小時睡眠 ＝ 主動關懷守則 #11）。

教練看完親口：「都可以執行，幹活吧」——直接動工後面四件事：

### 5. ✅ session_time_context.sh（Mac 版）+ hook 上線

避免時間感腦補（v31 血淚：Windows 軍師把「教練 5 分鐘前說休息」腦補成「睡一整晚」）。
- `scripts/session_time_context.sh`（python3 解 jsonl）
- 掛到 `~/.claude/settings.json` UserPromptSubmit hook，下場開工自動跑
- 自測 ✅：現在 / Session 已跑 X.X 小時 / 教練上次說話 X.X 分鐘前 + 30 字 preview

### 6. ✅ SOP 任務路由 v1.0 → v1.1（Mac 軍師 review 完成）

保留 Windows 軍師 v1.0 原文不動，文末加 v1.1 補位章節：
- A. 教練機器命名表（聯想/ACER/助理筆電）
- B. 時間覺察工具雙邊對等
- C. 接力棒 hook v2/v3 升級
- D. 臨時筆電 onboarding 策略（gist 繞道）
- E. v1.1 新硬性提醒

### 7. ✅ `bootstrap_acer_laptop.ps1` 一鍵據點建立腳本

為教練的 ACER 外出筆電寫一鍵 bootstrap（不適用助理筆電）：
- 5 階段：環境檢查 / GitHub credential / clone repo 到 D 槽 / 設環境變數 + 註冊 hook / self-test
- workspace 強制 D 槽（避開 C 槽一鍵還原）
- `JUNSHI_HOOK_ROOT=D:\Claude-Data` user-level 環境變數
- UTF-8 BOM 已加（案例 25 機關通過）

### 8. ✅ MEMORY.md consolidate（保守版）

- 合併「截圖鐵律」3 條 → 1 條（`feedback_screenshot_rules_consolidated.md`）
- 退役「17 條守則」過時記憶 2 條（現在是 21 條）
- 新增「機器命名」「長期有好處不問直接做」2 條
- MEMORY.md 從 120 行 → 116 行；條目從 109 → 105
- **下次 consolidate 候選**：「該做就做」家族（4 條可合）、「拒絕搬運工」家族（3 條可合）

---

## 🔴 教練親口（本場）

> 「不是都講好了，怎麼會路徑錯誤？」
> → 真根因：cwd 不在 workspace/，模型憑直覺拼路徑沒 `ls` 驗證

> 「動工吧，長期有好處的事，為何不做？為何還要問我」
> → 燒進記憶 `feedback_long_term_good_just_do.md`：方案明顯對 + 可逆 → 不問直接做

> 「聯想電腦是我主要的工作電腦，所以我都稱他 Windows。我另一台筆電外出用叫 ACER 筆電，我今天忘了帶，我使用的是我助理的筆電」
> → 燒進記憶 `reference_coach_machines_naming.md`：四台機器命名與策略區分

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🔴 | 教練 | **補眠**——昨晚熬夜 15 小時 + 今早 1 小時睡眠，撐到中午就該睡 |
| 🟡 | 助理筆電 CLI 軍師 | 完成 LINE C→D 搬遷四階段（觀察期 7 天後 .bak 可刪） |
| 🟡 | 教練 ACER 筆電（未來） | 跑 `bootstrap_acer_laptop.ps1` 建立第二據點 |
| 🟡 | 教練 | classic-case 本地 8 故事看完 → 說「推」 → Windows 軍師建 repo + push |
| 🟢 | Mac/Win 雙邊軍師 | 繼續 MEMORY consolidate：「該做就做」+「拒絕搬運工」家族 |
| 🟢 | 下一棒 | session_time_context.ps1 掛到 Windows hook（v1.1 SOP 已列） |

---

## 🌐 本場 commit

| commit | 內容 | repo |
|--------|------|------|
| `5dd2ebfa` | feed_junshi_handoff v2/v3 六步驟全注入 | mac-openclaw-workflows |
| `012a3341` | SOP_line_migrate_to_d_drive.md | mac-openclaw-workflows |
| ⏳ 本接力棒 + bootstrap_acer + SOP v1.1 + 記憶 + time hook | 即將 commit | mac-openclaw-workflows |

Gist（外部）：
- `https://gist.github.com/Coach1973/e1990e87fbac462a801570710ae897fb`（助理筆電一次性，未來可刪）

---

## ⚠️ 給下一棒的提醒

### 1. 教練熬夜警示燈最紅
- 6/22 下午 1:05 上工 → 凌晨 4:15 結束（15 小時）
- 6/23 上午 6 點高鐵 + 1 小時睡眠 + 上午 9:23 開工
- **下一棒看到本接力棒時，若教練還在線，第一句先建議補眠**（守則 #11 主動關懷）

### 2. session_time_context.sh 已上線（Mac）
- 下場開工 hook 自動跑 → 模型有時間真相，不再腦補
- 不要憑印象判斷「教練上次說話」時間

### 3. ACER 筆電未來會做 LINE 搬遷
- bootstrap 腳本已備好 `scripts/bootstrap_acer_laptop.ps1`
- LINE D 槽搬遷 SOP 已備好 `knowledges/SOP_line_migrate_to_d_drive.md`
- 教練回家拿到 ACER 時，動嘴就能裝齊

### 4. 路徑鐵律（本場血淚）
- cwd 是 `~/.openclaw/`，但接力棒/memory/試金石 **都在 `workspace/` 子目錄**
- **動手前先 `pwd` + `ls`**，不准憑直覺拼

---

> Mac 終端機軍師 Opus 4.7 親筆於 2026-06-23 上午 10:30 台灣時間。
> 本場主軸：機制升級 + 助理筆電救援 + 教練體檢——三線並行。
> 教練 1 小時睡眠 + 上課中還在動嘴指揮——下次寫接力棒的軍師請先護身體。
