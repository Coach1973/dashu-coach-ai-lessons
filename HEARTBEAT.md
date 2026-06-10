# HEARTBEAT 熱上下文（每次心跳必讀）

> ⚠️ 剛剛因 Context Overflow（對話太長）自動重啟
> 重啟時間：2026-06-10 10:38
> 對話記錄已完整存入 memory/2026-06-10.md 並推上 GitHub，零遺漏

## 🔴 重啟後第一件事

直接告訴教練：「🦞 對話記錄已滿，已自動重啟，請繼續下指令」
⚠️ **不要讀 memory 大檔**（memory/2026-06-10.md 可能超過 50KB，讀了會造成模型空白回應）

## ⚡ 系統狀態
- Primary 模型：minimax/MiniMax-M3（全面使用，2026-06-09 教練親口確認）
- 名稱對等：Telegram = 小龍蝦 = 電報

## ⚠️ 所有對話守則
- 全部繁體中文，不夾任何英文
- 能自己做直接做，不問確認
- 截圖禁用，直接讀檔案
- 執行完通報 Telegram（Chat ID: 6124913915）
- 預估超過 5 萬 Token 先回報教練確認
- ⚠️ 不要讀大型 memory 檔（會造成模型空白回應）

## 學長 relay poll
### 2026-06-10 2026-06-10 12:10 - relay poll OK

---

## 🆕 給軍師：本棒慘痛教訓（教練說「一會丟給軍師處理」）

**見 `.learnings/LEARNINGS.md` 開頭新章節（2026-06-10）**

### 重點一句話
教練罵「感覺我現在就是搬運工」「很煩」——因為我繞了 1 小時清 LiteSpeed Cache（教練去後台按按鈕也清不掉），正解其實是改 `site_icon = 書封面 book.png`，1 個 API call、2 秒生效、教練 0 按鈕。

### 軍師要做的事
1. **更新 SOP 自動站 v3.2**：site_icon 跟 OG meta 分工、子品牌站 site_icon 應跟子品牌一致
2. **更新 memory/索引**：把 v3.1 描述改成 v3.2
3. **蒸餾到試金石**：這案例的關鍵 = 「教練 0 按鈕」原則 + 「LiteSpeed 不可清快取」環境限制
4. **更新 auto-site-sop-bymyway skill**：跟 SOP v3.2 同步
5. **2 個 Astra hook（ID 27362 + 27364）**：決定留或刪（site_icon 解法生效後這 2 個 hook 其實多餘了，但清掉要進資料庫，問教練）

### 完整教訓見 `.learnings/LEARNINGS.md` 2026-06-10 章節


