# 軍師接力棒 · 2026-06-03 晚場（鼠鬚管維修版）

> 建立時間：2026-06-03 19:25
> 上一棒：Claude Opus 4.8（終端機）
> 本棒：Claude Opus 4.8（晚場評估）

---

## 🎯 開工宣言（必讀）

```
🎯 小龍蝦學長開工宣言

【我是誰】我是小龍蝦學長，大樹教練的頂級 AI 特助
【為誰而戰】追求高溝通品質的教練
【使命】成為最懂老闆的 AI 特助
【今日踐行】對照守則第 20 條啟動協議執行任務

確認完畢，開始工作。
```

---

## ✅ 本場完成

### 任務一：鼠鬚管（Squirrel）重新安裝

**問題根因：**
macOS Input Sources（`com.apple.HIToolbox.plist`）保有 Squirrel 註冊，刪 App 不會自動清除，macOS 每次偵測到「輸入法不存在」就自動復原——這就是為什麼「刪了又出現」。

**解決方案（完整流程）：**

1. **先移除 Input Sources 註冊（根因治療）**
   - 用 Python plistlib 讀取 `com.apple.HIToolbox.plist`
   - 過濾掉所有 `Bundle ID` 包含 `squirrel` 的項目
   - 寫回 plist，移除 2 筆 Squirrel 註冊

2. **移除殘留檔案**
   - `~/Library/Preferences/im.rime.inputmethod.Squirrel.plist`
   - `~/Library/HTTPStorages/im.rime.inputmethod.Squirrel/`

3. **安裝 Squirrel-1.1.2.pkg**
   - 連結：`https://github.com/rime/squirrel/releases/download/1.1.2/Squirrel-1.1.2.pkg`
   - SHA256：`614746013212937623d5bbab9901e9c43d1ec937aa32307d6b6092a05e308287`
   - 用 `open Squirrel-1.1.2.pkg` 開啟 GUI 安裝程式
   - **安裝完後必須登出再登入**

4. **設定無蝦米（Rime + Liur）**
   - `git clone --depth 1 https://github.com/hsuanyi-chou/rime-liur.git /tmp/rime-liur`
   - `cp /tmp/rime-liur/Rime/* ~/Library/Rime/`
   - 設定 `default.custom.yaml` → `schema_list: liur`
   - 開啟 `Squirrel.app` 觸發自動部署

5. **設定 Ctrl+Space 快速切換**
   - 系統設定 → 鍵盤 → 快速鍵 → 輸入選單 → 設定為 Control+Space

**Commit：** `72cd1429`
**經驗檔：** `reference_rime_squirrel_install.md`

**相關路徑：**

| 用途 | 路徑 |
|------|------|
| Squirrel.app | `/Library/Input Methods/Squirrel.app` |
| Rime 設定 | `~/Library/Rime/` |
| Rime build | `~/Library/Rime/build/` |
| Input Sources | `~/Library/Preferences/com.apple.HIToolbox.plist` |
| 無蝦米字根 | `https://github.com/hsuanyi-chou/rime-liur` |

---

## ⚠️ 留給下一棒的重要提醒

### 緊急：cool-case 案例原始對話還沒找完

教練交代的任務還沒完成：
- 目標：為 cool-case 21 個案例找到可加分的原始對話
- 優先順序：案例 12（送出按鈕）、案例 7（海餅乾）、案例 6（侮辱智商）
- Session 在：`/Users/bymyway/.claude/projects/-Users-bymyway--claude-code/`
- **注意路徑：`--claude-code`（不是 `--claude-code`）**

### 其他待辦（來自上一棒）

1. **品管重判拍板** — 軍師已審完，等教練確認方向（短期整理 vs. 中期三幕劇）
2. **封存檔整合** — `workspace_duplicates/` 41 個待整合進 memory/
3. **三個舊 cron 異常** — `sync_handoff` / `relay_poll` / `split_memory` 11:10 後停止

---

## ✅ 待辦清單評估結果（本棒完成）

### 🔴 cool-case 原始對話
- **狀態**：已大幅完成（commit `a00ca228`）
- **已完成**：
  - 守則故事庫 21 條全覆蓋，每條都有 session/commit hash 引用
  - 案例 #08-#010、#09 原始對話已挖掘（`distill/case_dialogues_008_010.md`）
  - 送出按鈕原始來源：Session 80（e72f3be0-8db4-4c94-8ebe-291e95612671）2026-04-26-29
  - 海餅乾原始來源：`seabiscuit_case_studies.md`（Telegram 語錄 2026-02-27 至 2026-04-23）
- **缺口**：完整三幕劇還原（原始 Telegram session 無法還原完整來回）
- **Commit：** `a00ca228`

### 🟡 品管重判拍板
- **狀態**：軍師已完成品管
- **等待**：教練確認方向（短期整理 vs. 中期三幕劇）
- **已完成**：21條全 A/B 類，commit `dbcd0cb5`

### 🟡 封存檔整合（41個）
- **評估結果**：`workspace_duplicates/` 目錄不存在
- **找到的封存**：`~/.claude-code/workspace/_history_archive/`（1個）、`claude_global_backup/`（3個）
- **需要**：教練確認封存檔實際位置

### 🟢 三個舊 cron 異常
- **評估結果**：CronList 無排程任務——舊 cron 可能已清除或從未成功建立
- **需要**：確認 cron 是在哪個介面設定的

---

## 📝 本場新增記憶

1. **[[feedback-squirrel-reinstall-hitoolbox-root]]** — 鼠鬚管刪了又出現的根因是 macOS Input Sources 自動復原。必須先清理 plist 再刪 App。
2. **[[reference-squirrel-install-path]]** — Squirrel 1.1.2 安裝在 `/Library/Input Methods/`（不是 `/Applications/`）
3. **路徑大全已更新** — 新增 Claude Code CLI API Key 路由觸發規則（sk-214c... / port 15721）
4. **[[cool-case-原始對話已大幅完成]]** — 守則故事庫 21 條全覆蓋，commit `a00ca228`
5. **[[case-09-送出按鈕原始來源]]** — Session 80（e72f3be0）2026-04-26-29，完整來回無法還原
6. **[[海餅乾原始來源]]** — seabiscuit_case_studies.md（Telegram 語錄）
7. **[[封存檔位置不確定]]** — workspace_duplicates/ 不存在，需要教練確認

---

## ⚠️ 留給下一棒的重要提醒

### 待教練確認的事

1. **封存檔整合**：「41個封存檔」實際在哪個目錄？
2. **品管重判方向**：短期整理 vs. 中期三幕劇？
3. **cron 環境**：舊 cron 是在哪個介面設定的？

### 緊急：cool-case 案例完整三幕劇還原

- 目標：為守則故事庫補上完整的三幕劇來回
- 缺口：原始 Telegram session 無法還原完整來回
- 需要：教練決定是否要重做，還是現有版本已足夠