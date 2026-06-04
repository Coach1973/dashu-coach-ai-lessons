# 軍師接力棒 · 2026-06-05（Hermes 助教 M3 終端機 session 完）

> 建立時間：2026-06-05 03:00
> 上一棒：軍師接力棒 2026-06-04 23:55（三待辦全清版）
> 本棒執行者：Hermes 助教（終端機跑 M3）
> 接班建議：直接進 Hermes 桌面版 App 對話，狀態全部已同步

---

## 🎯 開工宣言（給終端機/桌面版用，不是給小龍蝦）

```
🎯 Hermes 助教開工宣言

【我是誰】我是 Hermes，大樹教練的 AI 特助（終端機跑 M3）
【為誰而戰】追求高溝通品質的教練
【使命】成為最懂老闆的 AI 特助
【今日踐行】對照守則第 20 條啟動協議執行任務

確認完畢，開始工作。
```

> 註：身份 = 特助（服務教練），底層模型 = M3（技術細節）
> 軍師 = 終端機/桌面版跑 Opus；Telegram 小龍蝦獨立軌道

---

## ✅ 本場完成（Herme 助教 M3）

### 三待辦全清（同場接力棒三個）

1. **cool-case 寶藏挖掘** ✅
   - 對照 `https://coach1973.github.io/cool-case/` 後，8 個待挖案例全有原話
   - master_index 8 個名稱對齊實際標題
   - Commit：`4338e157`（含接力棒更新）

2. **品管重判拍板** ✅（4 方向一次解決）
   - #20 維持 A 類（案例 20-1 有真實教練原話 session 0541f0c0）
   - 一魚多吃：接受共用
   - 三幕劇：守則故事庫 21 條 + 三幕劇_TOP4.md 並存
   - master_index 8 名稱對齊 GitHub Pages
   - Commit：`4338e157`

3. **封存檔整合** ✅
   - 41 個 daily_2026-*.md：36 trash + 1 拆檔 + 4 補檔
   - Commit：`81b765cf`

### MEMORY 全面檢視（教練指導）

- 4,340 → 1,640 字元（-62%），197% → 74%
- 修正 5 個錯誤理解（VPS/小龍蝦/學長學弟學妹/三機 Mac mini 等）
- 桌面 HTML：`/Users/bymyway/Desktop/Hermes_MEMORY_最終版_20260605.html`

### Hermes 桌面版 App 安裝

- 安裝指令：`curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash -s -- --include-desktop`
- 退出碼 0，Hermes.app 301MB
- `/Applications/Hermes.app` symlink（Spotlight 找得到）

### 選單列小工具 v2（控制 Hermes 桌面版）

- `~/Library/LaunchAgents/ai.hermes.desktop.plist` — 登入自動啟動桌面版
- `~/.hermes/scripts/hermes-menubar-v2.py` — 12 個選項（啟動/重啟/關閉 桌面版 + CLI + Dashboard）
- 狀態每 10 秒自動更新

---

## 🪞 教練教我的關鍵教訓

### 1. 三層身份架構

| 介面 | 模型 | 身份 |
|------|------|------|
| 終端機/桌面版 | Opus | 軍師 |
| 終端機/桌面版 | 其他（M3/Sonnet/Haiku） | 助教 |
| Telegram | （任何） | 小龍蝦/特助（獨立軌道）|

### 2. 流量分工策略

- 克勞德（Opus）做高價值任務（蒸餾/決策）流量貴
- Hermes（M3）流量無限，接克勞德的接力棒勞力活
- 做完上傳清掉克勞德待辦

### 3. 守則 18 違規（最重要）

- **語音糾偏必問不猜**
- 觸發：上下文斷/詞不達意/詞彙陌生/邏輯反常 → 必先問
- 教練實錄：J=鍵盤誤觸、「嘸蝦米」→「五筆」同音誤判

---

## 📝 新增待辦（給下一棒）

1. **試用 Hermes 桌面版 App**（教練已轉移過去使用）——驗證功能
2. **守則 17「身份 ≠ 模型」全機規則同步** —— 三個 repo 都應該反映
3. **守則故事庫 GitHub Pages 一對一映射** —— 確保 cool-case 21 個案例都對應守則
4. **三個舊 cron 異常**（sync_handoff/relay_poll/split_memory 11:10 後停止）
5. **MEMORY 是否已自動反映新的 liur=蝦米 認知**（下次開機驗證）
6. **OpenVanilla 已刪除但 workspace MEMORY.md 還寫著**（教練尚未處理，不在這次範圍）

---

## 📊 Commit 清單（本場）

| Commit | 內容 |
|--------|------|
| `81b765cf` | 封存檔整合：補回 4/11~4/13 缺口，5/20 拆雙時段，trash 41 個重複封存檔 |
| `4338e157` | 品管四拍板 + 接力棒三待辦全清 |
| `（待本次 commit）` | 今日工作記錄 + 接力棒更新 |

---

**最後更新：2026-06-05 03:00（Hermes 助教 M3 終端機 session 結束）**

**下一棒：教練已轉移到 Hermes 桌面版 App**
