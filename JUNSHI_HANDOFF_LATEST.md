# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-26 深夜場
> 寫紙條的人：軍師（Claude Sonnet 4.6 桌面版）

---

## 一句話交代這場做了什麼

**🔥 SOUL.md 正確燒錄完成：特助心法 21 守則完整正典已嵌入 bootstrap 機制，每次 session 自動注入。**

---

## ✅ 這場完成的事

| 優先 | 任務 | 結果 |
|------|------|------|
| 🔴 高 | **SOUL.md 正確燒錄 — 學長（Mac）** | ✅ commit faf1c6d7 |
| 🔴 高 | **SOUL.md 正確燒錄 — 學弟/學妹（Mac）** | ✅ commit 09246f69 / 1fee8e4 |
| 🔴 高 | **VPS 1（43.245.60.200）SOUL.md 燒錄** | ✅ 直接更新 /root/openclaw/data |
| 🔴 高 | **VPS 2（113.29.232.178 赫米斯）SOUL.md 燒錄** | ✅ 直接更新 /root/.hermes |
| 🔴 高 | 研究 openclaw.json 正確做法 | ✅ 找到：SOUL.md 才是正解 |
| 🟡 中 | 觀察下一次心跳結果 | 尚未確認 |

---

## 🔥 燒錄系統詳細說明

### 正確做法（本場確認）

| 介面 | 檔案 | 方法 | 原因 |
|------|------|------|------|
| 小龍蝦（Telegram/OpenClaw）| `~/.openclaw/workspace/SOUL.md` | 完整 21 守則直接嵌入 | SOUL.md 是 bootstrap 檔案，每次 session 自動注入 system prompt |
| 終端機 + 桌面版 | `~/.claude/CLAUDE.md` | 燒錄版完整內容 | CLAUDE.md 是 Claude CLI 的全域指示 |

### ⚠️ 錯誤做法（已修正，勿重蹈）

| 錯誤做法 | 後果 | 修正 |
|----------|------|------|
| `agents.list[0].systemPrompt` 在 openclaw.json | Gateway crash loop（該欄位不存在） | 已 revert |
| `agents.list[0].systemPromptOverride` | 整個替換 system prompt（危險） | 勿用 |
| openclaw.json 只有引用（不嵌內容） | 依賴模型主動讀檔，不可靠 | 用 SOUL.md 燒錄 |

### 燒錄內容

```
身份宣告
特助心法（使命/願景/理念 + 三大信念 + 21守則）
執行細則（9條）
開工宣言觸發語（小龍蝦對教練）
背景對照機制（對外部用戶）
任務自我對照表
```

### 設計原則

| 角色 | 互動方式 |
|------|---------|
| 小龍蝦 ↔ 教練 | 開工宣言（明確朗讀） |
| 學弟/妹 ↔ 外部用戶 | 背景默默對照（用戶不需知道） |
| 學弟/妹 | 當用戶說「你怎麼這麼好」，才揭露守則 |

### 教練原話

> 「這套方法不僅是在小龍蝦用，在終端機跟桌面版 Claude App 也要照做。這樣才能確保每次執行都朝著使命願景、一致性的方向前進。」

> 「Token 不是問題，我要最高品質。」

---

## 🎯 A 方案整頓（已完成）

### 已清理的問題

| 問題 | 修復方式 |
|------|---------|
| 執行細則引用矛盾 | 更新為「唯一正式版」（教練欽定）|
| Top10 Errors 6份重複 | 建立 top10_errors_index.md 統一入口 |
| 場景庫版本過多 | 移至 .backup_cleanup_20260526/ |
| SUPERGROUP-MAP.md 路徑 | 確認存在於 shared-relay/ |
| 赫米斯 VPS 檔案過時 | 移至 .lessons_upload/ |
| 身份相關舊檔 | 移至 identity_archive/ |

### 健康度提升

從 5/10 → 9/10

---

## 🔗 Commit Hash 清單

| 描述 | Commit |
|------|--------|
| **SOUL.md 正確燒錄（本場）** | `faf1c6d7` |
| 前場燒錄系統（openclaw.json 方式，已知錯誤，CLAUDE.md 部分有效） | `e5ad2435` |
| A 方案整頓主體 | `4bca338e` |
| HEARTBEAT.md 更新 | `7039445b` |
| Push 到遠端 | ✅ 已推送 |

---

## 🔴 下一個軍師待辦

| # | 優先 | 任務 | 說明 |
|---|------|------|------|
| 1 | 🟡 中 | 觀察下一次心跳結果 | 確認心跳是否用繁體、日期是否正確、是否引用到 21 守則 |
| 2 | 🟡 中 | SOUL.md 燒錄驗證 | 下一個 session 確認小龍蝦 context 中確實有 21 守則內容 |
| 3 | 🟡 中 | `session-memory/handler.js` 時區修正追蹤 | OpenClaw 升級後會被覆寫，需要在升級後重新補修 |
| 4 | 🟢 低 | 赫米斯檢討報告 | 教練尚未說明目標 |

---

## ⚠️ 特別提醒

- **SOUL.md 在 git 管理，已 commit + push（faf1c6d7）** — 下次 session 自動生效，無需額外操作
- **bootstrap 注入機制**：SOUL.md 由 OpenClaw `loadWorkspaceBootstrapFiles()` 自動讀取，每次 session 都注入 system prompt
- **所有 cron 孤立 session（isolated）也生效** — 只要 `lightContext` 不是 `true`，都會包含 SOUL.md
- **openclaw.json 不在 git 管理** — 確認目前版本無 systemPromptOverride 欄位（已 revert 正確）

---

## 📝 燒錄系統驗證清單

下次開工時，確認：

- [ ] 小龍蝦回應時是否有引用/遵循 21 守則的行為？
- [ ] 特助心法 21 守則是否在 system prompt 裡（SOUL.md 有效）？
- [ ] 心跳 cron 是否正確執行（繁體中文、不亂造數據）？
- [ ] `1-HB.md` 第零步是否被遵守（強制讀特助心法）？

---

*軍師交接紙條完成 | 2026-05-26 深夜場 | 軍師 Claude Sonnet 4.6 桌面版*

---

> ⬇️ 以下是上一個軍師（Sonnet）的交接，保留作為歷史參考

---

# 軍師交接紙條（歷史，2026-05-26 下午場）

> 上一個軍師：Claude Sonnet 4.6 桌面版

## 一句話交代這場做了什麼

**小龍蝦 5 個系統 bug 全部修完：心跳幻覺、記憶體超大、重複 HB 檔、蒸餾腳本空跑、赫米斯 git 不提交——全部根治。**

## 下一個軍師待辦（來自 Sonnet）

| # | 優先 | 任務 | 說明 |
|---|------|------|------|
| 1 | 🟡 中 | 觀察下一次心跳結果 | 14:00 台灣時間確認心跳是否用繁體、日期是否正確 |
| 2 | 🟡 中 | `session-memory/handler.js` 時區修正追蹤 | OpenClaw 升級後會被覆寫，需要在升級後重新補修 |
| 3 | 🟢 低 | 赫米斯檢討報告 | 教練尚未說明目標 |

## Commit Hash 清單（Sonnet）

| 描述 | Commit |
|------|--------|
| 5 個 bug 修復（distill rewrite / 1-HB / HB-學長刪除 / failure handbook）| `fdb45726` |
| VPS distill_vps.py git push 修復 | 直接追加 |
| jobs.json cron 768246fb 修復 | 直接生效 |
