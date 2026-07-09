---
name: reference-amber-nas
description: 教練家裡的Amber私有雲儲存主機（192.168.0.35），媒體資源中心的儲存載體，2026-07-09實測確認用SMB（非WebDAV）即可跨電腦存取
metadata: 
  node_type: memory
  type: reference
  originSessionId: 16511bcd-5087-40ef-822c-1c9c29f266f9
---

教練在家裡自建的私有雲儲存主機，品牌是「Amber酷存」（myamberlife.com.tw），型號類似個人/家庭雲端硬碟一體機，非傳統NAS但功能相近。

**基本資訊**：
- 網址（僅限同一個區域網路內）：http://192.168.0.35/#index，主機名稱 `amber-Coach`
- 目前容量：500GB，教練說可隨時外接USB擴充到1TB或2TB
- 24小時運作（家中不斷電、不斷網的前提下）
- 帳密：登入用戶名是email前半段（`bymyway7`，不加@gmail.com），密碼已存在教練跨機共用大腦的原話記錄裡（2026-06-09 02:13前後的verbatim對話），需要時查那邊，不在此重複寫明碼
- 目前用途：Mac的時光機（Time Machine）備份目標

**2026-07-09 實測確認（用PowerShell net use/net view直接驗證，非猜測）**：
- 這台機器**沒有WebDAV功能**（App Store只有Home Assistant/Plex/Zigbee2MQTT/Zwave JS UI四個App；檔案服務頁籤只有SMB選項），先前查到的WebDAV官方文件是別的型號/版本，不適用這台
- **內建SMB（網路芳鄰）已經可以直接跨電腦存取，不需要額外開通任何東西**：`net use Z: \\192.168.0.35\home /user:bymyway7 <密碼>` 實測成功，掛成Z:槽後讀到真實檔案
- 完整分享資料夾清單：`Applications`、`home`、`Music`、`Photos`、`TimeMachine`、`Videos`
- `home`分享裡目前已有的資料夾：`.tmp`、`1123課程錄影`（2024年課程錄影，是現成媒體素材）、`MyDevices`、`MyDocuments`、`TimeMachine`、`Uploads`
- AmberAnywhere（付費訂閱功能，Free Trial到2026-08-22到期）是給「已安裝的App」做對外公開網址用，跟WebDAV/SMB的跨電腦存取是兩回事，目前沒有安裝任何App所以此功能閒置

**How to apply**：媒體資源中心的多電腦存取方案改成SMB掛網路磁碟機，不是WebDAV。Windows用`net use`指令或檔案總管輸入`\\amber-Coach\home`，Mac用Finder的`smb://amber-Coach`（Mac的時光機本來就是走這個）。之後在其他電腦（Acer等）要接上，比照同樣的net use指令即可，不需要教練在Amber後台多做任何設定。
