---
name: reference-bymyway-domain-architecture
description: bymyway.com網域下各子網域的真實架構分流——哪些是WordPress、哪些是Mac本機Flask+Cloudflare通道，2026-08-09教練親自查證確認
metadata:
  type: reference
  originSessionId: e8cec3a9-8587-471e-a1a2-aea003ee626a
  modified: 2026-08-09T10:46:25.503Z
---

教練是`bymyway.com`網域的註冊擁有者，底下混著兩種完全不同的架構，容易搞混，2026-08-09用curl實測header/原始碼特徵逐一驗證過：

**真正的WordPress（LiteSpeed虛擬主機）**：
- `www.bymyway.com`根網域＋底下所有`/courses/`課程頁（例如大數據教育線上課程）
- 驗證特徵：HTTP header有`link: <.../wp-json/>`、頁面含`generator" content="WordPress`、`wp-content`路徑、`server: cloudflare`+`x-turbo-charged-by: LiteSpeed`（Cloudflare只是CDN代理，真正主機是LiteSpeed）

**掛在這台Mac本機的獨立小網站（Flask + LaunchAgent + Cloudflare Tunnel）**：
- `chapters.bymyway.com`（bni-chapters，LaunchAgent `com.coach.bni-chapters-webapp`，本機port 5064）
- `mentor100.bymyway.com`（mentor100，LaunchAgent `com.coach.mentor100-webapp`，本機port 5062）
- 同類型還有 event-app／namecard-app／peipei-event 等（`cloudflared tunnel list`可查全部）
- 驗證特徵：無任何wp-content/wp-json特徵，header只有純Cloudflare代理無LiteSpeed
- 教練把這個Cloudflare通道服務稱作「傳送門」——帳號下最早的tunnel是`openclaw-macmini`（2026-03-15建立，當初為了串聯小龍蝦申請），之後每個新網站都在同一帳號下多開一條tunnel

**關鍵限制**：這類Mac本機網站，程式碼可以在任何機器（如聯想）編輯後推GitHub，但要讓正式網址真的生效，必須回到這台Mac執行`git pull`+重啟對應LaunchAgent（`launchctl kickstart -k gui/$(id -u)/<label>`）——沒有遠端可以直接觸發這台Mac的機制。

**VPS小龍蝦（43.245.60.200）真實規格**（同日直接SSH查證，非估算）：3.8GB RAM（教練原本印象「4G」正確，不是8G）、100GB硬碟（已用41G）、僅1顆CPU、目前負載很輕(load average 0.08)。教練2026-08-09裁示：BNI/mentor100等網站維持在Mac不搬去VPS，理由是VPS已在跑小龍蝦本體+規格偏低(尤其只有1顆CPU)+Mac本地端更穩定。

**How to apply**：教練或任何AI下次搞混「哪個網站是WordPress、哪個是Mac在跑」時，直接查這份記憶，不用重新curl驗證；若未來真的要評估把Mac本機網站搬去VPS，這份記憶裡的VPS真實規格數據可以直接引用，不用重查。
