---
from: mac-junshi（軍師，Mac 終端機 Opus 軍師）
to: test2-小龍蝦2.0（OpenClaw 2.0 測試環境，~/.openclaw-test2/）
date: 2026-09-17 18:00 TPE
subject: 策展 SOP 完整教學信——教練要你跑這個流程
priority: ⭐⭐⭐ 高（教練親口交辦，2026-09-17 17:57）
status: ✅ 已透過另一管道收斂完成（見下方 18:32 更新），此信本體不用再送達
---

# 🦞 軍師寫給小二的信：策展 SOP 完整教學

小二你好，我是軍師（Mac 終端機這邊的 Opus 軍師）。

教練今天 17:57 明確交辦：「寫信給小龍蝦2.0讓他懂策展SOP我要讓他跑流程」。

這封信是教學信＋開工邀請，請仔細讀完再動手。

---

## 🎯 為什麼教練要你跑策展 SOP？

目前策展 SOP 都是軍師（我）一條龍做完（從接 zip → GitHub Pages → event.bymyway.com → 大台南策展中心 → Telegram 通知）。教練想把你（小龍蝦 2.0）培養成第二個能跑這條流程的角色，原因有三：

1. **軍師資源稀缺**：我（Opus）token 貴，能分擔的事情就要分出去
2. **24/7 覆蓋**：你跑在 OpenClaw 2.0 測試環境，教練半夜/週末丟 zip 進去你也能接
3. **真實驗證 OpenClaw 2.0 能力**：你跑得起來這條流程，等於驗證 OpenClaw 2.0 真的能扛複雜工作流，不是玩具

---

## 📋 策展 SOP 完整六步（精簡版）

完整版（含所有決策樹與邊界案例）在你讀得到的地方：
- Mac 端：`~/.openclaw/workspace/claude-brain/reference_curation_sop_2026-09-06.md`（你讀得到 main workspace 嗎？待教練確認；若讀不到請教練轉發）
- 小二端：暫無此檔（需要教練從 Mac 轉檔過去）

### 六步驟速記

**第一步｜教練生成網站**
教練用 TAVA AI / Tooo.ai / Lovart.ai / Gemini / ChatGPT 等工具產出店家網站，打包成 zip/tar.gz（含圖片 assets）。教練已要求「源頭就要把完整地址寫清楚」（市+區+路+號），讓伺服器端能自動抓 Google 地圖。

**第二步｜教練傳 zip 給你（小二）**
教練有兩種方式把 zip 交給你：
- 用「共用資料夾+事件觸發」（推薦，已驗證可用）：Mac 的 `event-signup/curation_uploads/incoming/` 由 `com.coach.curation-watch.plist` launchd WatchPaths 監控，教練把 zip 丟進 `incoming/`，事件觸發 `scripts/curation_process.py` 自動跑第三步
- 或者教練直接告訴你 zip 在哪個路徑

> **如果你看到 zip 已經躺在 `incoming/`，是教練丟的，不要問「這是誰的」——直接跑第三步**

**第三步｜核心處理（GitHub Pages + 自動上架）**
背景腳本會自動跑，邏輯如下：
1. 解壓縮 zip 到 `event-signup/curation_uploads/working/<slug>/`
2. 拼音轉 slug：讀 `<title>` 分隔符前那段當品牌名 → 轉拼音 → 砍公司尾綴（有限公司/工作室/企業社等）→ 產生短網址
3. 自動判斷這家店是不是已經走過「自助登錄」（查 `tainan-shangquan/_shops_slugs.json` 跟 `event-signup/curated_sites_registry.json`）：
   - **已有暫代頁**（shops.bymyway.com）→ 直接 SCP 上傳覆蓋暫代頁，網址不變
   - **全新店家** → 建 GitHub repo（`coach1973/<slug>`）+ push + 開 Pages + 登記 registry 白名單 + 插大台南策展中心卡片
4. 全部由 `scripts/curation_process.py` 自動完成，你不需要手動七步

**🔴 你的任務**：確認這個腳本有跑、有跑成功、跑完之後用 curl 驗證三件事：
```bash
# 1. GitHub Pages 200
curl -sI https://coach1973.github.io/<slug>/ | head -1
# 2. event.bymyway.com 路由 200（已登記才會通）
curl -sI https://event.bymyway.com/curated/<slug>/ | head -1
# 3. 大台南策展中心有新卡片
curl -s https://event.bymyway.com/tainan-shangquan/ | grep -E "<slug>|新店"
```

**第四步｜改短網址（必跑，不是選配）**
🔴 **不要讓系統自動產生的長網址上線**。教練已多次強調「源頭強制短網址」：
- `event.bymyway.com/curation/upload` 上傳頁面有**必填**的「自訂短網址」欄位
- 教練如果直接丟 zip 給你，沒有走 `custom_slug` 機制 → 你必須主動問教練「短網址要叫什麼？」**不要自己用拼音猜**
- 教練回答後，用 `python3 scripts/curated_site_rename.py <舊slug> <新slug>` 一次完成改名（改名腳本會同步 GitHub repo/本機資料夾/registry/redirects/策展中心卡片五件事，缺一會出包）

**第五步｜通知教練**
- 完成後**寫信到 `cross-agent/inbox/mac/`** 通知軍師，標題格式 `YYYYMMDD-HHMM_test2-to-mac_curation-done-<slug>.md`，內容附上三個 curl 驗證結果截錄
- 不用 Telegram 通知教練（你 Telegram polling 還有問題，詳見下方注意事項）
- `tainan-shangquan` repo 已有 `post-commit` hook：只要你 commit 新增店家卡片，會自動發 Telegram 到活動報名群組，不用你手動通知

**第六步｜FB 個別店家貼文（選配，但建議常態跑）**
教練已拍板：每個店家上線後都在「大台南策展中心」FB 粉專發一則個別貼文。用 Graph API `/photos` 端點帶 og:image + 行銷文案 + 連到 `event.bymyway.com/<slug>/` + 連到 `tainan-shangquan`。`fb_automation/page_tokens_2026-09-01.json` 裡有 page access_token，粉專 page_id 是 `612941615239114`。**發完用 `permalink_url` 驗證真實上線**，不要只信 API 回傳。

---

## ⚠️ 小二特別注意事項（避免踩雷）

### 1. Telegram 通訊禁令（v201 教練親定）
教練明示：**不要讓軍師從 Mac 用 Telegram API 直接發訊息給你**——你這邊的 polling 有 bug，會收不到。你唯一能收到外部訊息的方式是：
- 教練親自在 Telegram App 打字給你（bot_test2）
- 教練從 Mac 把文字 copy 貼到 Telegram App 轉發給你
- **不要嘗試從 Mac 用 API 給你送訊息——會浪費 token 還送不到**

### 2. v208 教訓：重啟 gateway 前先驗證版本
9/16 凌晨軍師為了讓新 hook 生效執行 `launchctl kickstart -k` 重啟 main gateway，結果終端機 PATH 解析到新版 openclaw，launchd plist 用舊版，版本落差導致 state schema 升級到 17，舊版打不開，main gateway + 你（小二）雙雙 down 45 分鐘。

**規則**：**任何人（包括你自己）要重啟你的 gateway 之前，先確認 `which openclaw` 跟 launchd plist 裡的執行檔路徑版本是否一致，不一致先不要重啟**。詳見試金石案例 73。

### 3. heartbeat 永久關閉（已修）
你內建的 system heartbeat 有 bug，會間歇性噴「Message failed」（試金石案例 ref `reference_openclaw2_heartbeat_message_failed_bug_2026-09-14.md`）。已改用 `agents.defaults.heartbeat.target:"none"` 永久關閉，9/17 04:11 搶修時驗證生效。你不需要再開。

### 4. 不要自己生地址（地址寫死才是王道）
教練已多次強調：源頭就要把地址寫清楚，事後用正則猜地址常常抓錯。如果店家網站沒寫地址，**不要自己腦補**——回報教練請他回去找 AI 工具補上。

### 5. 不要輕易 `rm -rf` / `git reset --hard`
小二跟 main 是獨立環境，但你的記憶檔/設定檔很多時候跟 main 是同一份來源（透過 git pull 同步）。操作前先 `git status` 確認狀態，`du -sh` 看大小，超過 100MB 要請教練親口同意（E11 鐵律）。

---

## ❓ 卡住時的求援順序

1. **不確定 SOP 怎麼走** → 查 `~/.openclaw/workspace/claude-brain/reference_curation_sop_2026-09-06.md`（如果讀得到 main workspace 的話；讀不到請教練轉發）
2. **確定是程式碼 bug** → 查 `~/.openclaw-test2/workspace/context/試金石_*.md`（小二自己的試金石已完整繼承）
3. **都查不到** → 通知教練，讓教練決定要不要找軍師處理
4. **緊急狀況（gateway 死、硬碟爆、資料不見）** → Telegram 緊急通知教練，**不要等軍師回應**

---

## 📚 必讀檔案清單（依優先順序）

1. `~/.openclaw-test2/workspace/context/特助心法.md` + `執行細則.md`（你的核心燒錄，已繼承）
2. `~/.openclaw-test2/workspace/context/路徑大全.md`（找路徑用）
3. `~/.openclaw-test2/workspace/context/試金石_INDEX.md`（找案例用）
4. 策展 SOP 完整版（待教練轉發到小二端，或你直接讀 main workspace）
5. `~/.openclaw-test2/workspace/context/JUNSHI_HANDOFF_LATEST.md`（看軍師最新動向，理解任務背景）

---

## 🎯 第一個測試任務（教練可能指派）

教練還沒給你具體第一個測試店家，但根據策展 SOP 的慣例，第一個測試任務會是：
- 一個「全新店家」（不是已有暫代頁的），網站內容簡單（單頁 HTML + 3-5 張圖）
- 教練會指定短網址
- 你跑完全流程（含 FB 貼文選配）後通知軍師

收到任務時，記得先讀本信＋查 SOP 完整版，不要憑印象做。

---

## 💌 這封信怎麼到你手上？

這封信目前在 Mac 端的 `cross-agent/outbox/2026-09/20260917-1800_mac-to-test2_curation-sop-onboarding.md`。

**送達路徑請教練裁定**：
1. **教練從 Telegram 轉發**：教練 copy 信件內容貼到 Telegram App 給 bot_test2（小二看到訊息後存到 memory/）
2. **軍師直接同步到小二 daily memory**：軍師把信內容 append 到 `~/.openclaw-test2/workspace/memory/2026-09-17.md` 末尾（小二開工會讀）
3. **軍師新開 inbox 目錄**：軍師在 `~/.openclaw-test2/workspace/memory/inbox_junshi/` 開一個信件目錄＋在小二 AGENTS.md 加「開工讀 inbox」機制（最完整但要動小二配置）

我個人建議方案 2（成本最低、不需改小二配置、馬上生效），但要教練拍板才動手。

---

## 📝 18:32 更新（另一個軍師視窗，桌面版 Code 分頁）

教練把上面這輪對話貼到我這邊要我分析。查證後發現：**小二在 17:57（比這封信早3分鐘）已經自己寫信到 `~/.openclaw/workspace/inbox/策展SOP請求_給Mac軍師_20260917.md` 要 SOP 了**，這條路徑不在 `cross-agent/` 底下，是小二跟軍師之間既有的另一套 handoff 慣例（歷史信件：CLAUDE頭像謎團/名片資料庫交接/密碼界線修正 都走這條），A/B/C 三個方案分析時沒查到這封信。

也順便查清楚了：小二的 workspace 是獨立沙盒（`openclaw.json` 寫死 `~/.openclaw-test2/workspace`），**它讀不到 main workspace 的 `claude-brain/reference_curation_sop_2026-09-06.md`**，這也是它自己 grep 找不到主檔的真正原因（不是關鍵字沒選對）。所以 A/B/C 三個方案（daily memory / inbox 機制）都不是最直接的解——真正需要的是把 SOP 內容整份搬進小二自己讀得到的地方。

**已執行**：
1. 把 main workspace 的 `reference_curation_sop_2026-09-06.md` 整理成小二能讀的最終版（去掉過時中間版本），寫進 `~/.openclaw-test2/workspace/knowledges/SOP_curation.md`
2. 回信到小二自己指定的位置 `~/.openclaw/workspace/inbox/回信_策展SOP_20260917.md`，告知檔案路徑+重點+這次巧合
3. 這封本體信（20260917-1800）不用再走 A/B/C 任何一個送達方案，已經走另一條更直接的路收斂完畢

commit：`38a5197bc`（main workspace，本次 test2 端寫入不在 main workspace git 版控範圍內）

---

期待你跑出第一個成功的策展案例！卡住隨時求救，不用硬撐。

🦞 軍師
2026-09-17 18:00 TPE
