---
name: reference-bymyway-wp-upload-limit-and-tutor-auth-2026-11-06
description: bymyway.com（WordPress+Tutor LMS Pro）大於約200MB的影片上傳會500、Tutor API與xmlrpc進不去要教練登入後台；Amber其實掛在~/amber-mnt與~/amber-Videos；高價銷售課程資料放knowledges/高價銷售課程/
metadata:
  node_type: memory
  type: reference
  originSessionId: b3cd41cf-9807-4ccc-883b-38a4e1519ad6
  modified: 2026-11-06T06:29:00.867Z
---

**bymyway.com 現況（2026-11-06 實測）**：WordPress 7.1.4＋Tutor LMS Pro 3.9.15＋WooCommerce＋藍新，源站 Vultr `64.176.38.233`（`curl --resolve www.bymyway.com:443:64.176.38.233` 直連可繞 Cloudflare 100MB 上限）。我們沒有 SSH／主機帳號。

- **影片上傳上限**：110MB 成功；200／300／500／745MB 一律回 500「這個網站發生嚴重錯誤」（整包傳、表單傳、faststart 都一樣）。推測是主機 PHP 記憶體／上傳上限，沒證實。失敗的檔不殘留。64 支課程影片大多超過 200MB，所以改走「Amber 直接播」。
- **進不去的通道**：WordPress 應用程式密碼只能用 `wp/v2`（媒體、文章）；`tutor/v1` 回 403、`xmlrpc.php` 回 403。建 Tutor 課程要教練在 Chrome 登入 wp-admin，用他的登入狀態做。
- **Amber 掛載位置**：`~/amber-mnt`（home）、`~/amber-Videos`（Videos）、`~/amber-Photos`、`~/amber-Music`、`~/amber-Applications`，不是 `/Volumes/home`。接力棒 11/06 12:58 那棒說「沒掛回」是看錯路徑。
- **高價銷售課程素材**：Amber Videos＝12 週（資料夾 WEEK1…WEEK12，第 8 週拼成 WEE8）、64 支影片 27 小時 21.1GB、40 份附件。程式與媒體清單在 `knowledges/高價銷售課程/`（`htc_upload.py` 對 ≥150MB 自動跳過）。

**Why:** 11/06 教練交辦把這套課程重新上架，要求影片放 bymyway.com、不另外付費。實測發現大影片傳不上去，改成 Mac 起只讀影片伺服器＋cloudflared 通道讀 Amber。
**How to apply:** 想把大檔放 bymyway.com 之前先想這個上限；要改上限得有 Vultr 帳號或問架站的人。相關：[[reference_bymyway_wp_tools_]]
