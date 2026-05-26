# 系統優化報告

> 建立時間：2026-05-26 19:55
> 軍師自動生成
> 任務：檢查 Workspace、桌面歷史資料，掃描系統優化點

---

## 📊 Workspace 狀態

### 磁碟空間
| 分區 | 總容量 | 已用 | 剩餘 | 使用率 |
|------|--------|------|------|--------|
| / | 228GB | 11GB | 113GB | 10% |
| ~/ | 228GB | 90GB | 113GB | 45% |

**狀態**：🟢 磁碟空間充足

---

## 📦 Workspace 主要資料夾

| 資料夾 | 大小 | 說明 |
|--------|------|------|
| scripts/ | 260MB | 腳本（佔最大空間）|
| distill/ | 7.6MB | 蒸餾過的案例 |
| shared-relay/ | 11MB | 共享Relay |
| memory/ | 980KB | 記憶體資料 |
| knowledges/ | 新建 | 知識庫系統 |

---

## ✅ 已直接執行的優化

| 項目 | 說明 | 狀態 |
|------|------|------|
| 更新 HEARTBEAT.md | 同步最新的模型和身份判定 | ✅ 已完成 |

---

## ⚠️ 需要注意的項目

### 1. UserPromptSubmit Hook 指向不存在的檔案

**問題**：
`~/.openclaw/settings.json` 中的 UserPromptSubmit hook 指向：
```
/Users/bymyway/.openclaw/workspace/scripts/feed_junshi_handoff.sh
```
但這個檔案不存在，會導致 hook error。

**建議**：
- 需要問教練確認：這個 hook 是否還需要？
- 如果不需要，可以移除這個 hook
- 如果需要，要建立這個檔案

---

### 2. Cron Jobs 頻率優化

**現有 cron jobs**：

| 頻率 | 任務 | 風險 |
|------|------|------|
| `* * * * *` | relay_poll | 每分鐘執行，可能過度頻繁 |
| `*/5 * * * *` | sync_handoff | 每5分鐘，可接受 |
| `*/15 * * * *` | checkpoint_audit | 每15分鐘，可接受 |
| `0 */2 * * *` | run_distill | 每2小時，可接受 |
| `50 23 * * *` | heartbeat_audit | 每天23:50，可接受 |

**建議**：
- `relay_poll` 每分鐘執行可能過度頻繁，建議調整為每5分鐘
- 需要問教練確認：relay_poll 的理想頻率是多少？

---

### 3. daily_xxxx.md 檔案過大

**問題**：
daily_xxxx.md 檔案最大的有 900KB+，這些檔案是歷史對話記錄，佔用空間且難以維護。

**建議**：
- 可以考慮將舊的 daily 檔案歸檔到 _history_archive/
- 或者將多個 daily 檔案合併成月度檔案
- 需要問教練確認：這些 daily_xxxx.md 是否還需要保留？

---

### 4. distill 目錄有大量 JSONL 檔案

**問題**：
distill/ 目錄有大量 .jsonl 檔案，總共約 7MB，包括：
- terminalB_candidates.jsonl (765KB)
- terminalB_candidates_all.jsonl (1MB)
- terminalB_large_messages.jsonl (423KB)

**建議**：
- 這些 JSONL 是中間產物，可以考慮清理
- 或者確認這些檔案的用途後再處理
- 需要問教練確認：這些 JSONL 是否還需要保留？

---

## 🔧 可以直接執行的優化（無需確認）

| 項目 | 說明 | 預期效果 |
|------|------|----------|
| 清理 _history_archive | 這個目錄是空的（0B），可以確認是否需要 | 確認目錄用途 |
| 更新 top10_errors_index.md | 加入知識庫建立記錄 | 保持索引最新 |

---

## 📋 待確認項目（需要教練回答）

| # | 項目 | 問題 |
|---|------|------|
| 1 | UserPromptSubmit hook | 是否需要保留？還是要移除？ |
| 2 | relay_poll 頻率 | 每分鐘執行是否必要？建議改為每5分鐘 |
| 3 | daily_xxxx.md | 舊的 daily 檔案是否需要歸檔？ |
| 4 | JSONL 檔案 | distill/ 的 JSONL 檔案是否需要清理？ |

---

## 🎯 已發現的有用資源

| 資源 | 位置 | 說明 |
|------|------|------|
| 特助場景庫 117 | ~/Desktop/ | 已建立知識庫，117個場景已結構化 |
| distill/ | ~/.openclaw/workspace/distill/ | 蒸餾過的失敗案例 |
| 觸發訊號庫 | knowledges/ | 知識庫核心，已完成 |

---

*軍師建立，2026-05-26*
*使命：成為最懂老闆的 AI 特助*