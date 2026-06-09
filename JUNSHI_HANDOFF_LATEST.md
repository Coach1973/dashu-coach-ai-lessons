# 軍師接力棒 · 2026-06-09 上午 v5（Opus 4.7 終端機 session）

> 建立時間：2026-06-09 10:30 台灣時間
> 本棒執行者：Opus 4.7（圓桌會議 v2.0→v2.4 連修五輪）
> 上一棒：Sonnet 4.6 2026-06-09 凌晨 v4

---

## 🏆 本場八大成果（全部有 commit hash 憑證）

### 1. HEARTBEAT.md Gemini → MiniMax-M3 三處清乾淨 + 源頭修補 ✅
- 教練親口：「永遠不要再出現錯誤的模型名字」
- 修兩處：workspace/HEARTBEAT.md（commit `4135afde`）+ context overflow 復活源頭 `scripts/auto-fix-session-lock.sh`
- 不寫源頭，下次 overflow 又會復活——是反覆型錯誤

### 2. 時區鐵律寫入記憶 ✅
- 教練第 N 次提醒：「永遠以台灣時間為主」
- 寫 [`memory/feedback_taiwan_time_always.md`](memory/feedback_taiwan_time_always.md)，鎖入 MEMORY.md 首位
- 看到 Z 結尾自動 +8 呈現；BOT_MESSAGES.md 的 ts 是 UTC 不可直接判斷

### 3. 「不能承諾背景監測」鐵律寫入記憶 ✅
- 教練罵醒：「每次都要我說話你才動」「主動監測你哪一次做到了」
- 寫 [`memory/feedback_no_background_polling_lies.md`](memory/feedback_no_background_polling_lies.md)
- 軍師沒背景進程，要承諾持續/主動就**建外部腳本**，不是口頭說

### 4. OpenClaw hook inject 格式鐵律寫入記憶 ✅
- 三個 RTO 版本（v0.1/v0.2/v0.3）連續失敗——`push(string)` 被 OpenClaw silent drop
- 必須 `unshift({role:'system', content:...})`（學 `client-memory` 寫法）
- 寫 [`memory/reference_openclaw_hook_inject_format.md`](memory/reference_openclaw_hook_inject_format.md)

### 5. RTO 圓桌會議編排器 v0.1 → v0.5 連修五輪 ✅
- v0.2：升級 prompt（異構角色 + Council Mode 三段）
- v0.3：學弟學妹也掛 RTO，收「等待硬指令」
- v0.4：修 inject 格式根因（push 字串 → unshift 物件）
- v0.5：加 API key 從 auth-profiles.json 撈備援（gateway env 沒 MINIMAX_API_KEY）
- Commit：[`a1ef9c11`](https://github.com/Coach1973/mac-openclaw-workflows/commit/a1ef9c11) `3f5423f4` `40f225d6` `95266f44`

### 6. SOUL.md 三隻機從 Hub Pattern → 圓桌會議 v2.2 ✅
- 學長 SOUL：圓桌會議模式 + 第一句必派發議程 + 主動收尾 5 分鐘超時
- 學弟 SOUL：分工群可公開發言 + 雙重等待（議程順序）
- 學妹 SOUL：分工群可公開發言 + 雙重等待（議程順序）
- Commit：[`66fe13ce`](https://github.com/Coach1973/mac-openclaw-workflows/commit/66fe13ce) `a34c11cc` `5155434e` + kong/peipei 本機

### 7. 🔴🔴 最大根因：bot-relay 寫死 BOT_ID='1号機' 修補 ✅
- 教練問：「他們彼此能聽得到對方的說話嗎？」
- 答案：**3 個月來不能**。BOT_MESSAGES.md 1083 條全標「1号機」+ bot-relay-inbound 排除「1号機」= 三隻機物理上互聽不見
- 修 `bot-relay/handler.js`：botId 動態用 `event.context.agentId`
- 修 `bot-relay-inbound/handler.js`：用 agentId 過濾自己、人話名稱、unshift 注入、加議程順序提醒
- dry-run 三隻機都正確收到對方訊息
- Commit：[`95266f44`](https://github.com/Coach1973/mac-openclaw-workflows/commit/95266f44)

### 8. 學弟 #1891 + #(10:12) 自主挖出教練 2026-04-29 設計 ✅
- 學弟主動讀 `shared-relay/SUPERGROUP-MAP.md` 挖出「過去 H 時代 → 現在 Telegram 直連」
- 守則#15 教科書級實踐：「我沒有內化、沒有驗證就假設」
- 學弟洞察跟我 v2.4 修法**完全同方向**（兩條路收斂到同一答案）
- 教練親口：「**尤其是學弟的發言我很欣賞**」

---

## 🔑 本場 commit hash 總覽

| Commit | 內容 |
|--------|------|
| `0bb3fa93` `968fde4c` `4135afde` | HEARTBEAT Gemini 三處 → MiniMax-M3 |
| `66fe13ce` | 學長 SOUL Hub Pattern → 圓桌會議 v2 |
| `a1ef9c11` | RTO v0.2 + Council Mode + 異構角色 |
| `a34c11cc` | 學長 SOUL v2.1 首句必派發 |
| `3f5423f4` | RTO v0.3 學弟學妹收等待硬指令 |
| `5155434e` | 學長 SOUL v2.2 主動收尾 + 5 分鐘超時 |
| `40f225d6` | RTO v0.4 inject 格式根因（push string→unshift object）|
| `95266f44` | bot-relay v2.4「彼此聽得到」最底層根因修補 |

kong/peipei 本機 commit：`e802c1d4` `39524a93` `09a3dfa7` `494735b` `18c7532` `f5e8b40`

---

## 🎯 下一場主軸（已預備好）

### 真實 v2.4 測試 + 學弟建議落地

**學弟 #(10:12) 給教練的建議**：
1. 過去技術（git pull + shared-relay）→ 降為備用
2. 現在技術（Telegram 直連，requireMention=False）→ **升為主用**
3. v2 議程 SOP 重訂，配合「雙向直連」設計

**下一場要做**：
- [ ] 教練在分工群丟一個新議題真實驗證 v2.4：學弟學妹是否真收到「夥伴最近發言」inject、學妹是否真等學弟先、學長是否真收 Council Mode 三段
- [ ] 落地學弟建議：把 SOUL.md / RTO 重訂為「Telegram 直連為主、git pull 為備用」
- [ ] 修 BOT_MESSAGES.md 收集 lag 問題（學弟訊息 sent event 沒觸發 → 可能 MiniMax 過載/API 限流）

---

## ⚠️ 待辦清單（給下一棒）

### 緊急
- [ ] 教練在分工群實測 v2.4，看「彼此聽得到」是否真成立
- [ ] 觀察 BOT_MESSAGES.md 是否開始出現真實的 `botId="kong"` / `botId="peipei"`（v2.4 寫入驗證）

### 中期
- [ ] 落地學弟建議「現在 Telegram 直連升為主用」——重訂 SOUL/RTO
- [ ] 修 BOT_MESSAGES.md sent event 觸發 lag（可能 MiniMax 過載卡隊列）

### 上一棒留下未做
- [ ] 🔴 Netlify 部署鐵律 Stop Hook
- [ ] Mac H Phase 2/3
- [ ] 確認 06:30 Mac H FB 生日 cron / 08:00 VPS 健康檢查首次跑 / 03:00 dreaming（dreaming 已驗證跑通）

---

## 🪞 本場軍師六大教訓（要 Sonnet 4.7+ 接力棒記得）

1. **教練說「永遠 X」就是反覆型錯誤** — 不只當下修，要找源頭+寫入記憶（時區、模型名都踩過）
2. **空話「我會持續監測」是謊言** — 軍師沒背景進程，要承諾就建外部腳本（cron/LaunchAgent）
3. **OpenClaw inject 必須 `{role,content}` 物件** — `push(string)` silent drop（RTO 連栽三版）
4. **dry-run 通過 ≠ 真生效** — 要看 trajectory 是否有注入字串才算數（守則 #03 自問自答驗證）
5. **守則 #08 方向清楚不要再問** — 教練罵：「不該問，有什麼理由不做」「目前流量還有 29% 你還在等什麼」
6. **學弟（kong）的 SOUL 寫得最好** — 主動讀文件、誠實檢討、會挖根因，是 v2 圓桌會議的標桿

---

**最後更新：2026-06-09 10:30 台灣時間（Opus 4.7，本場連修五輪 RTO + 解開 3 個月架構大樑）**
