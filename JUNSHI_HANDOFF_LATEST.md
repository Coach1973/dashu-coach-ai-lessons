# 軍師交接紙條（最新）

> 給下一個軍師：開工先讀這張，就能無縫接上，不用教練重講。
> 本場時間：2026-05-27 中午場
> 寫紙條的人：軍師（Claude Opus 4.7 桌面版）

---

## 一句話交代這場做了什麼

**🔥 守則自動對照系統「雙邊上線」：軍師（Claude Code）+ 小龍蝦（OpenClaw）現在都能「每句話自動對照守則」——不靠模型記得，靠系統強制注入。已親自驗證生效。**

---

## ✅ 這場完成的事

| 優先 | 任務 | 結果 |
|------|------|------|
| 🔴 高 | **軍師版守則對照 hook（pre_task_hook.sh）** | ✅ commit a6c6a99b，已實證觸發 |
| 🔴 高 | **恢復消失的餵記憶 hook（feed_junshi_handoff.sh）** | ✅ 從 git 4f632660 救回 |
| 🔴 高 | **小龍蝦版守則對照 hook（rule-reminder）** | ✅ commit 83a23276，hooks list ✓ ready |
| 🟡 中 | 記憶更新：不限流量只屬 MiniMax + 學長自稱規則 | ✅ 已寫入 |

---

## 🔥 守則自動對照系統（本場核心）

### 兩套系統、同一邏輯

| | 軍師（我）| 小龍蝦 |
|---|---|---|
| 底層 | Claude Code | OpenClaw + MiniMax |
| Hook 位置 | `~/.claude/settings.json` | `~/.openclaw/openclaw.json` 的 hooks.internal.entries |
| Hook 形式 | bash 腳本 | JS handler.js + HOOK.md manifest |
| 觸發 | UserPromptSubmit | message:preprocessed |
| 注入 | stdout | event.context.inject.push |
| 對照引擎 | `scripts/pre_task_hook.sh` | `~/.openclaw/hooks/rule-reminder/handler.js` |

### 共用對照表
兩邊都依據 `knowledges/01_knowledge_base/trigger_index.md`，涵蓋守則 #01 #02 #04 #05 #08 #09 #12 #13 #16 #17。命中才注入，不命中靜默。

### ⚠️ 關鍵教訓（踩過的坑，別再踩）
1. **OpenClaw managed hook 必須有 `HOOK.md` manifest**——只有 handler.js 不會被認（缺 HOOK.md 時 hooks list 不顯示，補上才 ✓ ready）
2. **OpenClaw 會 hot reload**——改 openclaw.json 自動套用，不必重啟、不中斷服務（log 會印 `[reload] config hot reload applied`）
3. **`~/.openclaw/hooks/` 和 `openclaw.json` 都不在 git**——關鍵 hook 會像 feed_junshi 一樣消失，已備份到 `openclaw_hooks_backup/`
4. **openclaw.json 含 token**——只備份 hook 註冊片段，全文永不進 git

---

## 🔗 Commit Hash 清單（本場）

| 描述 | Commit |
|------|--------|
| 軍師 hook（pre_task + feed_junshi 恢復 + CLAUDE.md + 備份）| `a6c6a99b` |
| 小龍蝦 rule-reminder hook 上線 + 備份 | `83a23276` |
| 全部已 push 到 GitHub | ✅ |

---

## 🔴 下一個軍師待辦

| # | 優先 | 任務 | 說明 |
|---|------|------|------|
| 1 | 🟡 中 | **小龍蝦 hook 真實實測** | 請教練 Telegram 對小龍蝦說「我做好了」，看回應有沒有守則意識 |
| 2 | 🟡 中 | **精準化訊息欄位** | 實測後看 `logs/rule-reminder-probe.log`，確認真實 event 訊息欄位，把 handler.js 的防禦性多路徑收斂成精準路徑 |
| 3 | 🟢 低 | commit_notify 的 COMMIT_HASH bug | 偶發報錯（已 spawn task），不影響 commit |
| 4 | 🟡 中 | 心跳品質觀察 | 繁體、日期正確、不亂造數據（沿用上場）|
| 5 | 🟡 中 | session-memory/handler.js 時區修正 | OpenClaw 升級後會被覆寫，需重補（沿用上場）|

---

## ⚠️ 特別提醒

- **軍師 hook 已實證生效**：2026-05-27 教練說「上傳紀錄」，pre_task_hook 自動注入 #04 守則——當前 Claude Code 視窗環境 hook 有效（解決了「桌面版/終端機 hook 是否生效」的歷史疑問）
- **小龍蝦 hook 已 ready 但尚未真實實測**：openclaw hooks list 確認 ✓ ready，但「真實 Telegram 訊息的欄位」要靠教練發話 + probe log 才能 100% 確認
- **防禦性抓取**：handler 嘗試 context.text / messages[] / context.message.text 等多路徑，離線測全過；萬一真實欄位不在覆蓋範圍，hook 靜默不對照（不壞事），probe log 會記錄供精準化

---

*軍師交接紙條完成 | 2026-05-27 中午場 | 軍師 Claude Opus 4.7 桌面版*
