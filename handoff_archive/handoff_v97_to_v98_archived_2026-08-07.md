# 📦 封存：v97 ~ v98（原始接力棒段落，未刪減）

> 封存時間：2026-08-07（隨 v100 收工瘦身，符合 E16 鐵律「主檔只留最新1~2棒」）

# 軍師接力棒 · 2026-08-05 v98（Mac終端機 Sonnet 5，結繩領導學網站5項調整+GitHub自動部署推送+Netlify額度更新）

> 建立時間：2026-08-05 下午（台灣時間 15:00~19:27）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v97（Mac終端機，opencode兩次當機根因修復）
> 本棒主軸：**教練提出結繩領導學(jiesheng-leadership.netlify.app)網站5項調整。開工先用MD5比對確認正確本地repo(`github_repos/jiesheng-leadership`，排除另一份`~/jiesheng-leadership`已過時的舊複本)，完成全部調整後用本機Chrome實測驗證，教練確認後說「推到netlify」，查證此站是GitHub自動部署型(git push main觸發，跟22個手動zip站不同)，commit `2807592`推送後curl+Chrome雙重驗證正式站生效。教練追問部署額度剩幾次，查證git-auto-deploy也計入同一credit池(依7/22歷史先例)，51→50已更新記錄。全程無教練糾正、無新教訓，屬於乾淨執行既定SOP的任務。**

## 🎯 本場戰果

### 1. 🎯🎯 結繩領導學網站5項調整全部完成並推上正式站
- 「立即報名活動」按鈕改跳轉至`#workshopRegBtn`(座談會已全數結束，主要動線改導向工作坊報名)
- 座談會場次區塊搬到「兩天工作坊」下方，標題加註「（11場活動均已圓滿結束）」，notice-bar改回顧感謝語氣
- 工作坊區塊移除「報名線上座談會」按鈕，只保留「立即報名工作坊」
- 台中場取消，只留台南/台北兩場，FAQ「台南、台中、台北三個城市場次」同步改「台南、台北兩個城市場次」
- 依教練回覆，Hero小字從「線上座談會10場‧免費線上報名」改為「11場活動圓滿結束，可看歷史回顧」

### 2. 🎯 查證確認jiesheng-leadership是GitHub自動部署型站台
本機Chrome預覽(`open -a "Google Chrome"`)驗證版面+按鈕動線無誤後，教練說「推到netlify」。原想用curl查Netlify API核對站台設定，但`netlify_deploy_guard.sh`因指令含真實token被擋下——查`knowledges/SOP_netlify_website_edit.md`既有記載：jiesheng-leadership的Netlify站台`build_settings.repo_url`已連github.com/Coach1973/jiesheng-leadership，**唯一更新路徑是`git push main`**，不走zip+API。依SOP走`git add`+`git commit`+`touch PUSH_APPROVED`(推送鎖通行證)+`git push origin main`，commit `2807592`推送成功，等待Netlify自動build後curl驗證正式站三項關鍵文字皆已生效，並依Stop hook提醒補開一次Chrome看正式站確認。

### 3. 🎯 Netlify部署額度更新：51→50
教練問「還剩下多少次可以推」。查`state/netlify_deploy_quota.json`發現guard的自動扣減機制只認curl POST `.../deploys`結尾指令，git push不會觸發自動扣減——但查歷史紀錄(2026-07-22 jiesheng-leadership那筆`git-auto-deploy`確有計入扣減)，確認git-auto-deploy一樣消耗同一credit池，手動補記本次推送51→50，並誠實告知教練這是本地推算非即時查詢Netlify帳單頁的數字。

## 📋 下一場直接開工任務
- 其餘卡住項目（BNI真誠/真愛/真AI分會、Email自動發送系統、bni-chapters預設密碼等）本場未觸碰，狀態不變
- 接力棒瘦身：本場已封存v93~v96到`handoff_archive/handoff_v93_to_v96_archived_2026-08-05.md`，主檔現只留v98+v97

## 🔑 本場關鍵檔案索引
- `github_repos/jiesheng-leadership/index.html`：5項調整全部完成
- `state/netlify_deploy_quota.json`：新增jiesheng-leadership本次推送記錄，額度51→50
- `handoff_archive/handoff_v93_to_v96_archived_2026-08-05.md`：新增，封存v93/v94/v95/v96
- commit（jiesheng-leadership獨立repo）：`2807592`

---

# 軍師接力棒 · 2026-08-05 v97（Mac終端機，opencode 兩次當機根因修復：snapshot 關閉＋model 改 minimax 自家）

> 建立時間：2026-08-05 中午 12:00~12:36（台北時間）
> 本棒執行者：Mac 終端機軍師
> 上一棒：v96（Mac終端機Opus 5，大樹小講金門場次+歷史紀錄宮格牆改版+健康檢查cron假警報修復）
> 本棒主軸：**教練反映「opencode 已經兩次當掉」，查log抓到兩個AbortError session（11:57+12:05），找三層根因：①snapshot對empty git repo失敗②並行git lock衝突→Bun AbortError→TUI崩③預設model跑錯provider（opencode-go/minimax-m3 vs minimax/MiniMax-M3大小寫差異）。第一版報告建議「去opencode.ai workspace充值」被教練當場糾正「我們是用minimax自家API Key，跟額度無關」——後續curl驗證minimax自家Key HTTP 200有效，確認是opencode預設model跑錯provider而非額度問題。修法4個改動全部完成，knowledges紀錄+試金石案例57同步commit + push。**

## 🎯 本場戰果

### 1. 🎯 opencode 兩次當機根因（三層）

| 層次 | 根因 | 證據 |
|---|---|---|
| 表面 | snapshot 警告噪音 | log 53次 `_archive_2026-05-20/agents_bak/kong.bak/' does not have a commit checked out` |
| 致命 | git index.lock 並行衝突 | log `fatal: Unable to create '...index.lock': File exists` + `AbortError: Aborted` from Bun runtime |
| 體驗 | opencode 預設 model 跑錯 provider | log `providerID=opencode-go modelID=minimax-m3`（應為 `providerID=minimax modelID=MiniMax-M3`）|

### 2. ✅ 修法（4 個改動，全部已驗證生效）

| # | 改動 | 驗證 |
|---|---|---|
| 1 | `~/.config/opencode/opencode.json` 加 `"snapshot": false` | log 不再出現 kong.bak warning |
| 2 | `opencode upgrade` 1.15.13 → 1.18.13 | `opencode --version` 顯示 1.18.13 |
| 3 | `~/.config/opencode/opencode.json` 加 `"model": "minimax/MiniMax-M3"` | `opencode run` 確認 log `providerID=minimax modelID=MiniMax-M3` |
| 4 | 同檔加 `"small_model": "minimax/MiniMax-M2.5-highspeed"` | 解決 `server unavailable key=claude type=local` warning |

**附帶驗證**：minimax 自家 API Key curl 實測 `https://api.minimax.io/anthropic/v1/messages` 回 HTTP 200 → 從頭到尾都有效，不需要去 opencode.ai 充值任何東西。

### 3. 🔴 教練當場糾正：軍師第一版報告錯了

軍師看到 log 報 `providerID=opencode-go` 就直覺聯想「opencode.ai workspace 額度歸零」，建議教練去 `https://opencode.ai/workspace/wrk_01KSYW4B3DF6PWB9MRG95BT6VT/billing` 充值。

**教練原話**：「你沒有搞清楚，之前我們設定 Opencode 使用的是 MiniMax，是我們自己的 API Key，所以跟額度有什麼關係？」

**教訓**（已寫入試金石案例57）：
- 陌生 provider name 必須先 `opencode models` 查證再下結論
- 不要從「錯誤訊息字眼」直接聯想到「對應服務的帳號問題」
- 看到 `Insufficient balance` 要先確認實際用的 provider 跟教練設定的是不是同一個

### 4. 📁 Knowledges 紀錄 + 試金石案例

- `knowledges/2026-08-05_opencode兩次當機根因修復_snapshot關閉＋model改minimax自家.md`（含「教訓段」提醒未來軍師）
- `試金石/試金石_案例庫.md` 新增案例57（陌生provider name瞎猜教訓）

## 📋 下一場直接開工任務

- 接力棒瘦身：目前主檔有 v97/v96/v95/v94 四棒，超過 E16 規定的「最新 1~2 棒」，**下場建議封存 v94/v95 到 handoff_archive**（v93 已在此前測試時封存失敗，本場已 git restore 回原始 214 行版本，待下場重新封存）
- 其餘卡住項目（BNI真誠/真愛/真AI分會、Email自動發送系統等）本場未觸碰，狀態不變

## 🔑 本場關鍵檔案索引

- `~/.config/opencode/opencode.json`：加 `snapshot: false` + `model: minimax/MiniMax-M3` + `small_model: minimax/MiniMax-M2.5-highspeed`（教練後續手動完整化了 provider.minimax 區塊）
- `~/.local/share/opencode/log/opencode.log`：642行（最後更新 12:05，無新錯誤）
- commit（openclaw workspace）：`48c99e9e`（snapshot關+升級）→ `d78d48f8`（model修正+knowledges重寫）
- commit（試金石案例57）：見下一行 commit hash（本場收工產生）
- knowledges 紀錄：`knowledges/2026-08-05_opencode兩次當機根因修復_snapshot關閉＋model改minimax自家.md`
- 試金石案例：案例 57（陌生 provider name 瞎猜教訓）

