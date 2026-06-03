# 軍師接力棒 · 2026-06-04 凌晨（Top30 試金石 Hook 啟用版）

> 建立時間：2026-06-04 00:35
> 上一棒：Claude Opus 4.8（6/3 晚場）
> 本棒：Claude Opus 4.8（試金石 Hook 啟用）

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

### 任務一：4/5/6 月試金石整合完成

**整合內容：**
- 4月：8 個案例（三機身份維修、30分鐘回報失敗、身份搞混等）
- 5月：15 案例（A-O，failure-case-handbook.md）
- 6月：4 個新案例（鼠鬚管、aiprimetech、Proxy 等）
- 總計：**32+ 個錯誤案例**

**試金石系統架構：**
```
Top30_Index.md         ← 🏆 主榜單（30個案例排行，Hook 引用）
├── 試金石_守則與流程.md（21個案例）
├── 試金石_溝通與語音.md（5個案例）
├── 試金石_記憶與蒸餾.md（4個案例）
├── 試金石_專案與代碼.md（7個案例）
├── 試金石_模型與設定.md（5個案例）
├── 試金石_輸入法.md（1個案例）
└── 試金石_部署與發布.md（2個案例）
```

**視覺化版：**
- `試金石_視覺化總整理.html` — 卡片式佈局、彩色標籤

### 任務二：Top30 試金石 Hook 建立並啟用 🆕

**新增 Hook：** `~/.openclaw/workspace/scripts/top30_zhushi_hook.sh`

**功能：**
- 教練說「你又犯」「這個犯過了」「之前說過」等觸發詞時
- 自動從 `Top30_Index.md` 找對應的 30 案例
- 注入完整 NEC 檢查清單到 context
- 涵蓋 12 種關鍵字自動匹配（路徑/模型/distill/守則/Hook/接力棒/30分鐘/身份/gateway 等）

**測試結果：**
- ✅ 觸發詞「你又犯了路徑問題」→ 自動找到 #2 三機身份維修
- ✅ 觸發詞「你又犯切換模型」→ 自動找到 #1 模型切換失效
- ✅ 無觸發詞 → 靜默退出（不打擾）

**已掛載到：** `~/.claude/settings.json` 的 `UserPromptSubmit` hooks

### 任務三：視覺化 HTML 建立

- `試金石_4-5-6月錯誤總整理.html` — 純文字版
- `試金石_視覺化總整理.html` — 🎨 視覺化版（紫 Gradient + 卡片 + 標籤）

---

## 🔴 4/5/6 月案例對應守則

| 月份 | 案例數 | 整合狀態 |
|------|--------|---------|
| 4月 | 8 個 | ✅ 全部寫入 `試金石_守則與流程.md` |
| 5月 | 20+ 個 | ✅ 全部寫入對應 `試金石_*.md` |
| 6月 | 4 個 | ✅ 全部寫入對應 `試金石_*.md` |

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

## 📝 本場新增記憶

1. **[[Top30-Index-建立]]** — 30 案例排行主榜單，commit `04ddb0d3`
2. **[[Top30-Hook-啟用]]** — top30_zhushi_hook.sh 掛載到 settings.json，已通過 3 種觸發詞測試
3. **[[試金石視覺化版]]** — 紫 Gradient 卡片式 HTML，教練友善
4. **[[ai-primetech-確認]]** — unlimited.aiprimetech.io 是正確的第三方代理（不是 synterolink）
5. **[[鼠鬚管重複問題]]** — macOS Input Sources 自動復原的根因 + 完整修復流程，commit `72cd1429`

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

---

## 🔗 本場 Commit Hash 總覽

| Commit | 內容 |
|--------|------|
| `72cd1429` | 鼠鬚管移除與重新安裝經驗 |
| `a00ca228` | cool-case 原始對話大幅完成 |
| `dbcd0cb5` | 21條守則全 A/B 類品管 |
| `04ddb0d3` | Top30 試金石主榜單建立 |
| `2b6a354e` | 試金石視覺化版（卡片+標籤）|
| `5c23d5a9` | 試金石 4/5/6 月總整理 |
| `e600b02f` | 試金石 INDEX 4月案例更新 |
| `b26f4abe` | 試金石新增 4月案例016-021 |
| `be138c89` | 試金石新增 6月案例（路徑搞混等）|
| `fd85ba52` | 試金石整合 4月+5月+6月 |
| `686c6f36` | Workspace 最終上傳 |

---

*軍師建立，2026-06-04 00:35*

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