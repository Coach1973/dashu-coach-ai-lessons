---
name: reference-bymyway-subdomain-530-missing-launchd-2026-08-29
description: bymyway.com子網域回傳Cloudflare 530代表tunnel connector沒連線，peipei-event缺少launchd看護導致掛了5天沒人發現，已補齊修復
metadata:
  node_type: memory
  type: reference
  originSessionId: a4721a74-a4de-43a6-aad7-9216fa028a19
  modified: 2026-08-29T09:06:45.487Z
---

教練回報 `peipei-event.bymyway.com/qr/peipei-print.html` 打不開，查證流程與根因記錄。

## 診斷方法（下次遇到 bymyway.com 底下任何子網域打不開，直接照這個順序查）

1. `curl -sI https://<子網域>.bymyway.com/...` 看 HTTP 狀態碼。**530 = Cloudflare DNS/origin 錯誤**，代表 Cloudflare 這邊能解析出 DNS 紀錄本身，但連不到 origin（跟 502/522 不同，502 是 origin 有回應但錯誤、522 是 TCP 連線逾時，530 通常是 CNAME 指向的 cloudflared tunnel 完全沒有 connector 在線）
2. 查 DNS 紀錄真正指向誰：`curl -s "https://api.cloudflare.com/client/v4/zones/634966548bb9b87d7875b394e7003741/dns_records?name=<子網域>.bymyway.com" -H "Authorization: Bearer <token見路徑大全_憑證層.md>"`，會看到 CNAME 指向 `<uuid>.cfargotunnel.com`
3. `ps aux | grep cloudflared` 比對這個 uuid 有沒有對應的 process 在跑（`~/.cloudflared/<uuid>.json` 是憑證檔，`~/.cloudflared/<name>-config.yml` 是設定檔，設定檔裡的 `tunnel:` 欄位就是這個 uuid）
4. tunnel process 若沒在跑，先查 `~/.cloudflared/<name>-tunnel.log` 最後幾行找出被關閉的原因跟時間點（本次案例：`Initiating graceful shutdown due to signal terminated`，2026-08-24 08:58:34，人為或系統終止，非程式本身崩潰）
5. **同時要查 origin 設定檔（`ingress.service: http://localhost:<port>`）指向的本機服務是否也還活著**——`lsof -ti :<port>`，本次案例是 Flask 後端(port 5061)自己也跟著沒了，不是只有 tunnel 掛，兩層都要重啟
6. `launchctl list | grep com.coach` 確認這個站台的 webapp/tunnel 有沒有對應的 launchd Label 在跑（狀態碼 `0` = 正常，`-15` = 收到 SIGTERM 剛結束會重啟，`-` 是 one-shot 服務不適用）——**用 `com.coach` 當關鍵字，不要用 `cloudflare` 當關鍵字查（Label 命名是 `com.coach.<站名>-tunnel`，不含 cloudflare 字樣，用錯關鍵字會誤判成「全部沒被管理」）**

## 根因：peipei-event 是唯一沒有 launchd 看護的站台

`bymyway.com` 底下目前掛了 6 組 webapp+tunnel（event／mentor100／namecard／bni-chapters／jiesheng／peipei-event），前 5 組都在 `~/Library/LaunchAgents/` 有對應的 `com.coach.<站名>-webapp.plist` + `com.coach.<站名>-tunnel.plist`（`RunAtLoad:true` + `KeepAlive:true`，process 意外死掉會自動重啟、開機也會自動啟動）。**唯獨 `peipei-event` 這組從 2026-07-13 建立以來就沒有對應的 plist**，是純手動 `nohup ... &` 跑起來的 process，2026-08-24 某次終止後，因為沒有任何自動看護機制，就一路斷線到 2026-08-29 教練發現為止（5 天沒人知道）。

## 已修復（2026-08-29）

1. 手動重啟 Flask 後端(`github_repos/peipei-event/app.py`，port 5061)+ cloudflared tunnel(`peipei-event-config.yml`)恢復服務
2. 新增 `~/Library/LaunchAgents/com.coach.peipei-event-webapp.plist` + `com.coach.peipei-event-tunnel.plist`（完全比照 `com.coach.event-*.plist` 的格式），`launchctl load` 兩份後改由 launchd 接管，`launchctl list | grep peipei-event` 確認狀態碼 0
3. 驗證：本機 `localhost:5061` 與正式站 `https://peipei-event.bymyway.com/qr/peipei-print.html` 皆回 200

## How to apply

之後新增任何 bymyway.com 子網域服務（webapp + cloudflared tunnel 這種組合），**建立當下就要同步建 launchd plist**，不要用手動 nohup 先跑著「之後再補」——peipei-event 就是這樣拖了一個半月才出事。若要盤點還有沒有其他遺漏，直接比對 `ls ~/.cloudflared/*-config.yml` 的清單跟 `ls ~/Library/LaunchAgents/ | grep com.coach` 的清單，兩邊站名應該要一一對應，缺一個就是下一個會犯同款錯的站台。

Related: [[reference_mac_hook_scheduler_architecture_2026-08-12]]
