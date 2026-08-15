# 軍師接力棒 · 2026-08-14 v108（Mac桌面版 Sonnet 5，LINE三帳號個人記憶標準化修復+報名系統雙寫遷移bymyway.com）

> 建立時間：2026-08-14 01:38 ~ 03:46（台灣時間）
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v107（Mac桌面版 Sonnet 5，台南行事曆9/21改期+ai-fit新站上線+大樹小講報名轉發機制+LINE連線故障排除）
> 本棒主軸：**兩條主線都是教練親自發現問題、逐層深挖到底的架構修復。①教練被LINE版龍蝦小助教問「您是哪一位」動怒，查證抓到兩層根因（people.md/USER.md漏登LINE ID＋line-user-memory hook對main/default頻道sessionKey格式判斷有bug，main帳號從未真正運作過），兩層都修好並用合成webhook實測驗證。②教練問報名統計，發現event.db只算現場簽到、線上報名完全沒有資料庫紀錄；深入查證+教練親自糾正後確認sme-register-fn（Netlify）是純轉發不落地的真正缺口，教練裁示要遷回bymyway.com，執行雙寫並存架構（event-signup新增CORS端點+bigtree前端新增第三條寫入路徑），本機+瀏覽器實測後教練確認「推」，已上線。過程中教練兩批共貼51筆歷史報名通知文字，backfill進資料庫，去重複後49人，教練明確表示要用來印簽到表。**

## 🎯 本場戰果

### 1. 🔴🔴🔴🔴🔴 LINE三帳號個人記憶標準化：main/default頻道從未真正運作過
教練在LINE傳訊息給「龍蝦小助教」，被問「您是哪一位」當場動怒。查證發現兩層根因：①`people.md`/`USER.md`教練條目只登記Telegram ID，從沒登記過LINE ID，已補上兩個已知LINE ID並註明一律視為教練本人（commit`246e51766`）。②更深層、影響所有人的bug：`hooks/line-user-memory/handler.js`的`parseSession()`原本只靠`sessionKey.includes('line')`判斷頻道，但`main`帳號的sessionKey固定是`agent:main:main`（不含"line"字串），導致這支hook對main頻道的**所有人**從第一關就`return null`，整套機制形同虛設；同時也移除了原本寫死排除教練LINE ID的`COACH_LINE_IDS`清單（教練裁示三帳號要用同一套標準，含教練本人）。改用`ctx.channelId`判斷頻道（跟`inbound-message-echo-log`已驗證過的正式欄位一致），commit`d12bc391`。用合成簽章webhook實測驗證：教練LINE ID傳訊息後`agents/main/clients/{教練LINE ID}.md`真的被建立且正確累積，測試假資料已清除。詳見記憶`project_line_per_user_memory_standardization_2026-08-14`。

### 2. 🔴🔴🔴 報名統計雙資料源發現+bymyway.com雙寫遷移上線
教練問「幫我統計各場次報名幾人」，一開始只查到`event.db`的現場簽到人數。教練點破這只算現場簽到、不算線上報名，後者完全沒有資料庫紀錄。深入查證+教練親自糾正一輪（教練一度誤以為跟Netlify無關，AI用Netlify API+bigtree原始碼註解「送出後教練的LINE會直接收到通知」兩項證據攤開，教練接受後裁示「資料庫要建在bymyway.com」）後確認：`sme-register-fn`（`sme-register-fn.netlify.app`，6+網站共用）純轉發LINE/Telegram通知、完全不落地任何資料庫，這是真正缺口。

教練要求安全雙寫並存（新舊不衝突，確認bymyway.com穩定後才拔Netlify），已執行：
- `event-signup/app.py`新增`/api/register`端點（CORS支援，跟既有`/e/<slug>`共用`db.upsert_signup()`邏輯，任何失敗都回200不拋錯），commit`e773c4dd6`
- `event.db`補齊大樹小講全部15場session的slug對照（含9~12月未來場次）
- `bigtree/index.html`新增第三條並行fetch路徑寫進`event.bymyway.com/api/register`，原本`sme-register-fn`+`xiaolongxia-notify`兩支Netlify通知完全不動，repo commit`3130b93`
- 瀏覽器實測驗證slug對照正確（特別驗證8/25同天雙場次day/night有正確分開）+資料成功寫入資料庫，教練確認「可以推了」後正式部署：deploy`6a7e15b116b28f7990b3a616`，curl驗證文字/新程式碼/圖片皆正常，額度41→40（workspace commit`f395b1ff5`）

**backfill歷史資料**：教練分兩批共貼51筆真實線上報名通知文字，解析寫入`event.db`新建的`advance_registrations`表，去重複（抓到1筆真重複）後49位不重複報名者，統計交付教練。**教練明確表示「要記得這份名單，我到時要印簽到表」**——這是重要下游用途，須確保不被誤刪。詳見記憶`project_dual_registration_data_sources_2026-08-14`。

### 3. 🔧 附帶修正：13小時斷線是時區換算錯誤
教練質疑「cloudflared斷線13小時」跟「LINE正常對話」矛盾，查證發現是UTC時間被直接當台灣時間念（少換算+8小時），實際只斷約5.4小時（8/13 19:47~8/14 01:09台灣時間），且教練對話是01:19才開始，已在斷線恢復之後，兩者並無矛盾。已寫入記憶提醒此類時區換算錯誤模式。

## 📋 下一場直接開工任務
- **雙寫並存觀察期**：教練尚未指定要觀察多久才拔掉`sme-register-fn`/`xiaolongxia-notify`，下次先問教練bymyway.com這邊資料是否穩定累積
- ~~三機同步：Windows/ACER的`line-user-memory`hook修復待處理~~ **2026-08-14查證更正並結案**：`line-user-memory`是OpenClaw gateway hook（`ai.openclaw.gateway.plist`，只在這台Mac mini跑），非Claude Code的`~/.claude/settings.json` hook，Windows/ACER並未各自安裝OpenClaw gateway，git push就是唯一需要的同步動作，不需要教練開機、不需要任何機器移植腳本。**教訓見同棒下方新增記錄**，避免下次又照抄這行過時文字
- **49人backfill名單**：教練要用來印簽到表，查詢方式已寫進`USER.md`（`SELECT session_label, COUNT(*) FROM advance_registrations ...`）
- 「真誠分會」網頁主架構問題等v107遺留待辦仍未處理（新LINE帳號4GLBTVK3已於2026-08-14教練確認測試正常，結案）

## 🔑 本場關鍵檔案索引
- `hooks/line-user-memory/handler.js`+`HOOK.md`：main/default頻道支援修復
- `workspace/memory/people.md`+`USER.md`：教練LINE ID身份對照+報名統計SOP
- `event-signup/app.py`：新增`/api/register`端點
- `event-signup/event.db`：新增`advance_registrations`表(49人backfill)+15場session slug補齊
- `github_repos/bigtree/index.html`：新增BYMYWAY_API第三條寫入路徑
- commit(workspace)：`246e51766`+`d12bc391`+`65869b86c`+`a14a9d05e`+`e773c4dd6`+`f395b1ff5`
- commit(bigtree)：`3130b93`，deploy`6a7e15b116b28f7990b3a616`
- commit(memory記憶庫)：`730d2824a`+`9d96abf66`+`33f1aed91`
