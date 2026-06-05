# 軍師接力棒 · 2026-06-05（minimax-m3 終端機 session 完）

> 建立時間：2026-06-05 17:30
> 上一棒：軍師接力棒 2026-06-05 03:00（Hermes 助教 M3 終端機 session 完）
> 本棒執行者：minimax-m3 軍師（opencode CLI 終端機）
> 接班建議：教練已在終端機（opencode CLI）執行本場，待辦已全清

---

## 🎯 開工宣言（給終端機/桌面版用，不是給小龍蝦）

```
🎯 minimax-m3 開工宣言

【我是誰】我是 minimax-m3，大樹教練的 AI 軍師（opencode CLI 終端機）
【為誰而戰】追求高溝通品質的教練
【使命】成為最懂老闆的 AI 特助
【今日踐行】對照守則第 20 條啟動協議 + E04 行動前三問

確認完畢，開始工作。
```

> 註：身份 = 軍師（服務教練），底層模型 = minimax-m3（執行類，非 Opus）
> 軍師 = 終端機/桌面版跑 Opus；本棒 minimax-m3 同屬軍師軌道但屬「執行類」

---

## ✅ 本場完成（minimax-m3 軍師）

### 教練指令：5 待辦全處理

**待辦 1｜試用 Hermes 桌面版 App — 教練說完成可刪除 ✅**
**待辦 2｜守則 17「身份 ≠ 模型」全機規則同步 — 教練說完成可刪除 ✅**
**待辦 3｜守則故事庫 GitHub Pages 一對一映射 — 教練說完成可刪除 ✅**
**待辦 4｜三個舊 cron 異常 — 上一棒已驗證健康（commit `eff1539b`）✅ 保留**
**待辦 5｜MEMORY 是否已自動反映新的 liur=蝦米 認知 — 本場執行 ✅**
**待辦 6｜OpenVanilla 已刪除但 MEMORY.md 還寫著 — 本場執行 ✅**

### 任務一：MEMORY 反映 liur=蝦米 認知 ✅

- 認知正解：**「liur」= RIME 方案名 = 劉氏拆碼（liu7）= 嘸蝦米**，三個字是同一個東西的不同寫法
- 教練實測 2026-06-02 23:15「打的很順，一切正常」
- 改寫 `reference_coach_input_method.md` 整檔，全面反映 2026-06-02 升級到鼠鬚管 + RIME liur

### 任務二：MEMORY 反映 OpenVanilla 已刪除 ✅

- **實況驗證（2026-06-05 17:25）：** `ls /Library/Input Methods/` 只有 Squirrel.app；`ls ~/Library/Input Methods/` 是空的（只有 `.localized` 0 byte）→ **OpenVanilla.app 確實完整刪除**
- 修正 `reference_coach_input_method.md` 過時描述（舊版寫「`~/Library/Input Methods/OpenVanilla.app` 檔案還在」是錯的）
- 更新 `MEMORY.md` 索引 line 18：「教練的輸入法：香草=OpenVanilla=嘸蝦米」→「鼠鬚管 Squirrel + RIME liur 嘸蝦米」

### 三條新規範（從這次整理提煉）

| 規範 | 內容 |
|------|------|
| **字根三寫一體** | 「liur」「liu7」「嘸蝦米」自動對映到 RIME `liur` 方案，不再糾結 |
| **卸載清單對外公開** | MEMORY.md 索引要把「已卸載的輸入法」明確標 ❌，避免下次又被舊索引誤導 |
| **紅線改版** | 舊「絕不可移除 OpenVanilla」→ 新「至少保留一個能打中文的輸入法」（已 2026-06-02 教練同意）|

---

## 🪞 教練教我的關鍵教訓（這場特別收穫）

### 1. 接力棒上的「待辦描述」可能是過時快照
- 待辦 5「liur=蝦米」乍看不知道是什麼，實際是 2026-06-02 升級鼠鬚管時的新認知
- 待辦 6「OpenVanilla 已刪除」描述對，但「workspace MEMORY.md 還寫著」要動手才知道是 `reference_coach_input_method.md` 整檔都過時
- **教訓：執行待辦前先驗證事實（ls / Library 狀態），不要照字面瞎搜**

### 2. 過時記憶是隱形炸彈
- `reference_coach_input_method.md` 寫「`~/Library/Input Methods/OpenVanilla.app` 檔案還在」→ 實際 2026-06-05 17:25 驗證根本不存在
- 如果不驗證，下次有 AI 看到「檔案還在」就會以為教練還能用 OpenVanilla，給出錯誤建議
- **教訓：寫進記憶的硬體狀態都該加「最後驗證日期」欄位**

---

## 📝 給下一棒

### 待辦（已全清）✅
- 接力棒 6 個待辦全部處理完畢
- 教練已轉移到 Hermes 桌面版 App（待辦 1 已刪除），可隨時接力

### 環境狀態（給下一棒快速上手）
- 終端機軌道：opencode CLI minimax-m3（同本棒）
- 小龍蝦軌道：Telegram 1號機 @openclaw_macbook4_bot
- 工作區 git：1 個本地未推送 commit（`a43f4925` auto-backup）+ 數個未提交修改（auto-backup 自動產生，無需手動處理）
- HEARTBEAT：17:01 Context Overflow 重啟（小龍蝦軌道），17:19 relay poll OK，17:25 OpenVanilla 狀態驗證完

### 提醒
- 教練的輸入法 = 鼠鬚管 + RIME liur 嘸蝦米（不要再說 OpenVanilla）
- 守則 18 語音糾偏表已更新到 `reference_coach_input_method.md`（liur/liu7/嘸蝦米 三寫一體）
- 紅線已改版：至少保留一個能打中文的輸入法

---

## 📊 Commit 清單（本場）

| Commit | 內容 |
|--------|------|
| `（本次）` | MEMORY 全面反映輸入法升級（reference_coach_input_method.md 改寫 + MEMORY.md 索引更新 + 接力棒更新）|

---

**最後更新：2026-06-05 17:30（minimax-m3 終端機 session 結束）**

**下一棒：接力棒已全清，教練決定下個任務**
