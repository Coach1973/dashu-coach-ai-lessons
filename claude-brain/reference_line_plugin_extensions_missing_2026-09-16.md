---
name: reference-line-plugin-extensions-missing-2026-09-16
description: 三個LINE帳號(大台南南區小幫手/教練都在想什麼/龍蝦小助教)同時斷線5天多，根因是@openclaw/line外掛套件檔案遺失、openclaw plugins list顯示not installed但config完全正常
metadata: 
  node_type: memory
  type: reference
  originSessionId: 56b9f8ed-5dc0-425a-a86f-82908e70377e
  modified: 2026-09-15T18:48:56.326Z
---

2026-09-10 22:24:48（台灣時間）gateway 一次熱重載重啟後，全域 npm 安裝的 `openclaw` 套件（`/opt/homebrew/lib/node_modules/openclaw/`）底下的 `extensions/line` 資料夾消失（整個 `extensions/` 目錄都不存在），導致 `~/.openclaw/node_modules/@openclaw/line` 這條 symlink 變成 dangling link。**config 本身完全正常**（`channels.line.enabled: true`、`plugins.entries.line.enabled: true`、`plugins.allow` 也有 `line`），gateway process 也正常存活，但每次重啟 gateway 時載入的 plugin 清單都只有 13 個（少了 `line`），且沒有任何 error/warning log 提示原因——要跑 `openclaw plugins list` 才會看到真正的錯誤訊息：`plugins.entries.line: plugin not installed: line`。

教練 2026-09-16 凌晨自己逐一測試三個 LINE 帳號才發現全部當機，距離故障發生已經 5 天 3.5 小時，中間至少 10 次 gateway 排程重啟都沒有自我修復、也沒有任何告警。

**修復方式**：`openclaw plugins install @openclaw/line`（官方外掛安裝指令，會自動裝進相容版本 2026.6.34，裝在 `~/.openclaw/npm/projects/openclaw-line-*/`），裝完必須重啟 gateway 才生效（`launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`）。單純 `npm install -g openclaw@<version>` 重裝核心套件**不會**補回 extensions 資料夾——這次先誤以為是套件重裝問題試了一次，沒用，才查到 line 其實是獨立的「外部外掛」機制，不隨核心套件一起裝。

**根因未完全查明**：`extensions/` 資料夾究竟怎麼消失的沒有查到直接證據——openclaw 核心套件本身 mtime 是 8/24（跟事故時間點 9/10 對不上），事故當下的 gateway log 顯示同一個 ~70 秒窗口內先出現「config reload retry: config file not found」兩次，之後才觸發 SIGUSR1 重啟，懷疑跟某個當下正在寫入 `openclaw.json` 的自動化流程（多機同步/git pull 之類）短暫競態有關，但沒有抓到真正刪除 `extensions/` 資料夾的那個動作。

**新的健康檢查機制**：`scripts/three_line_bots_healthcheck.sh` + launchd `ai.openclaw.line-bots-healthcheck`（每天08:05），三層檢查缺一不可：① process 存活 ② **gateway 最近一次啟動的 plugin 清單裡真的有 `line`**（不能只看 config 顯示 enabled）③ 對外 webhook 端對端路徑有回應（`curl https://event.bymyway.com/line/webhook`，收到 400/403 代表整條 DNS→Cloudflare→tunnel→gateway 都通，這是正確的拒絕回應不是故障）。教練明確要求每天都要回報，不論健康與否，跟一般「只在真的壞掉才播報」的原則不同，是這次事故後的新規則。

**Why**：這是「process 活著 ≠ 真的在運作」這類坑的第三個變體——[[reference_xiaolongxia_line_tunnel_cloudflared]] 記錄過 cloudflared tunnel process 活著但連線斷線 13 小時沒人發現；這次是外掛套件的檔案層級遺失，連 config 本身都顯示一切正常，比 tunnel 那次更難查（沒有明顯的錯誤字樣，要主動跑 `openclaw plugins list` 才會現形）。

**How to apply**：任何要驗證「這個 LINE/Telegram/cloudflared 之類的通道還活著嗎」的健檢，絕對不能只看 `pgrep`/`launchctl list` 顯示 process 在跑就回報正常，要往下多查一層「這個管道最近一次真的處理過東西的證據」（本案是 gateway log 的 plugin 清單、或對外 webhook 端對端回應）。同樣的道理也適用於未來任何新的外掛/channel 設定，安裝後除了看 config 也要看 `openclaw plugins list` 有沒有 warning。

相關：[[reference_xiaolongxia_line_tunnel_cloudflared]]、[[reference_hermes_gateway_hang_watchdog_2026-09-08]]（另一種「process 沒死但卡住」模式）

---

**🔴 2026-09-16 追加教訓：第一次「已修復」驗證用錯網域，教練實測揭穿**

修好外掛後，第一版驗證用 `curl https://event.bymyway.com/line/webhook`，收到 HTTP 403 就當作「webhook 對外路徑正常」回報教練「三個都修好了」。教練幾分鐘後實測傳訊息給「教練都在想什麼」完全沒收到回覆，質疑「你確定真的修好了嗎」——回頭查證才發現 **`event.bymyway.com` 跟這三個 LINE 帳號完全無關**，它是另一個獨立 LINE 官方帳號「大樹教練」`@qaw8118h`（event-signup 報名系統專用，記錄在 `路徑大全_憑證層.md` 第 207 行）在用的網址，兩者碰巧都回 403 只是巧合，完全沒驗證到真正的路徑。

**正確網址查法**：這三個帳號共用「小龍蝦專線」tunnel（id `e35d30ec-45cf-4854-8afc-1bf92b163231`），用 Cloudflare API 查 DNS CNAME 記錄（`GET zones/{zone_id}/dns_records`，找 content 含 tunnel id 的紀錄）才找到真正對應的 5 個公開網址：`bni`/`media`/`openclaw`/`rpl-workshop`/`seabiscuit`.bymyway.com，逐一測試後確認 `bni`/`openclaw`/`seabiscuit` 三個能正確路由到 gateway（`media` 502、`rpl-workshop` 404，同tunnel但配置給別的服務）。

**正確驗證法**：不能只看「有沒有回應」，要用**真的帶正確 HMAC-SHA256 簽章**（用該帳號的 channelSecret 算 `X-Line-Signature`）的合成 webhook 打過去，收到 HTTP 200 才代表簽章驗證通過、訊息真的能被處理——403/400 只代表「有東西接住但拒絕了」，可能是正確拒絕、也可能是打錯地方被別的服務拒絕，兩者外觀完全一樣，光看狀態碼分不出來。健檢腳本已修正為這個做法，commit `0e7b4325f`。

**Why**：這是本案第二層「process/回應活著 ≠ 真的在運作」——連我自己的『驗證』步驟都踩了同一種坑（有回應就當作對，沒去確認回應是不是來自正確的目標）。

**How to apply**：驗證任何「對外服務是否正常」，光測「有沒有回應」不夠，要確認回應**是從正確的目標系統來的**（不是巧合打中別的服務也給了類似回應），且要用能反映真實使用情境的請求（有效簽章/有效格式），不能用最簡單、最容易誤判成功的測試方式。

---

**🔴🔴 2026-09-16 最終結案：完整時間軸+第三層根因(session卡死)+教練當場糾正查證方法**

**完整故事**：
1. **2026-09-10 22:24:48** — gateway熱重載後`@openclaw/line`外掛套件檔案遺失，三帳號靜默斷線
2. **2026-09-16 01:51** — 教練親自測試發現三個帳號全部無回應，回報軍師
3. **01:57** — 用`openclaw plugins install @openclaw/line`修復，重啟gateway確認14個plugin+3帳號provider成功啟動
4. **02:06** — 軍師誤用`event.bymyway.com/line/webhook`(完全不相關的另一個LINE帳號的網址)測試，回報「已修好」——**第一次誤判**
5. **02:09** — 教練實測「教練都在想什麼」沒回應，質疑軍師
6. **02:10~02:18** — 軍師改用直接查詢LINE官方API(`/v2/bot/channel/webhook/endpoint`+`/v2/bot/channel/webhook/test`)確認正確網址`openclaw.bymyway.com`+LINE官方測試回報200——**教練當場糾正這是繞遠路**，密鑰其實都在`路徑大全`，該先查本機文件/log，不該直接打外部API
7. **02:19** — 查本機`/tmp/openclaw/openclaw-*.log`(比持久化的`Library/Logs/openclaw/gateway.log`更詳細)，找到教練09:xx那則真實訊息確實有送達+排隊，但處理過程**卡死**，5分鐘後被gateway自己的「stuck session watchdog」強制中斷，從未產生回覆——**這是跟extensions資料夾遺失完全獨立的第三個問題**
8. **02:23** — 重啟gateway清空卡死的session殘留狀態，請教練重新測試——**教練說「沒反應，連已讀都沒有」，軍師第二次判斷「已修好」被打臉**
9. **02:29~02:37** — 軍師錯誤懷疑LINE官方帳號後台「回應設定」被改，教練親自截圖證實該設定完全正常(Webhook開啟/聊天關閉)——**軍師第二次繞遠路，方向錯誤**
10. **02:41** — 軍師改用LINE Push Message API直接推播測試訊息，教練確認收到——證實outbound通；接著軍師監看60秒log完全沒等到教練回覆的inbound紀錄
11. **02:48** — 教練確認「都正常了」，要求徹底解釋原因+預防

**最終狀態**：三帳號皆已確認正常運作。**stuck session卡死的根本原因未能100%查明**(可能是gateway熱重載/多次重啟期間殘留的session lane狀態損壞，重啟後自然清空)，這點對教練誠實告知，沒有裝懂。

**三層獨立問題**（不要混為一談）：
① `extensions/line`資料夾遺失（根本原因，已修復，觸發原因仍不明）
② session lane卡死5分鐘才被watchdog強制中斷（可能是①修復過程中殘留的狀態污染，重啟後未再重現）
③ 軍師自己的查證方法兩度出錯（測錯網域、猜錯設定項），教練當場指出「所有密鑰都在路徑大全，為何要查LINE官方」——**驗證方法應該優先用本機已有的資料/log，而不是predicated在對外部服務發API請求**，即使外部查詢比較「權威」，也要先窮盡本機資源，效率跟教練的信任都更重要。

**How to apply（給下一次同類事故）**：
1. 健檢先看process→plugin清單→本機log裡inbound事件是否卡住(用`/tmp/openclaw/openclaw-<date>.log`，比`Library/Logs/openclaw/gateway.log`詳細)，這三層本機都查得到，不用碰外部API
2. 只有本機log完全無法判斷時，才考慮打LINE官方API（`webhook/endpoint`查註冊網址、`webhook/test`做端對端驗證），這是最後手段不是第一步
3. 任何「已修好」的回報，證據強度必須對應教練的實際使用場景（真人傳真訊息+等它跑完），不能用curl測一個狀態碼就下結論
