---
name: reference-hinotes-no-local-recordings-chrome-data-on-e
description: 教練問「HiNotes 錄音檔存在哪個磁碟機」→ 電腦上沒有；HiNotes 是 Chrome 網頁應用程式，錄音在雲端與 HiDock 錄音裝置，要手動下載才落在 D:\Users\Downloads；聯想 Chrome 資料夾其實是捷徑到 E 槽
metadata:
  node_type: memory
  type: reference
  originSessionId: fc9b26dc-27b6-48c5-888f-4207170ef56f
  modified: 2026-10-21T08:37:08.202Z
---

教練 2026-10-21 08:20～08:57 在聯想問 HiNotes 錄音檔在 D 還是 E 槽，想搬到 E 省 D 槽容量。**查到的**：

- HiNotes＝Chrome 網頁應用程式（app-id `dngcajkojnnfdpjejmagoflohnikkaek`，2026-04-06 安裝），桌面捷徑在 `D:\Users\Desktop\HiNotes.lnk`（桌面資料夾本身就在 D 槽），只是用 Chrome 開網頁，沒有安裝目錄。
- **C 槽的 Chrome 資料夾 `C:\Users\bymyw\AppData\Local\Google\Chrome\User Data` 是 Junction → `E:\Claude-Data\AppData\Chrome-User-Data`**，所以 Chrome 裡 HiNotes 的資料（IndexedDB 0.1 MB、其餘都是網頁快取）實體本來就在 E 槽；`File System` 233 MB 全是網頁圖片與字型，不是錄音；整個 Chrome 資料夾找不到 5 MB 以上的音檔。
- 全磁碟（C/D/E）檔名含 hinotes／hidock 的只有：D 的捷徑、E 的 Chrome 資料、`E:\HiNotes錄音備份`（建立 6/18，只有 1 檔 `20240827培訓錄音.aac` 41.6 MB，像人工備份）。
- Chrome 下載位置 `D:\Users\Downloads`；教練手動從 HiNotes 匯出才會落在那裡，該夾有 184 個音檔共 5.05 GB（`錄音檔` 52 個 1.76 GB、`媒體檔案` 32 個、`全國分享會` 63 個、`ZOOM` 20 個，後者是 Zoom 自己的錄音），無法分辨哪些來自 HiNotes。
- 教練 10/21 補充：這些音檔「應該是螢幕錄影程式微 iTop 每次錄影產生的」。**查到的**：iTop Screen Recorder 6.5（裝在 `D:\Program Files\iTop Screen Recorder\`）的 `Main.ini` 設定「音訊／截圖／專案」存檔位置都是 `D:\Users\Downloads\`，「影片」預設在 `C:\Users\bymyw\AppData\LocalLow\iTop Screen Recorder\Videos\`（目前是空的）。**對不上的**：Downloads 第一層現在沒有任何 iTop 音檔，184 個全在子資料夾，無法逐一確認哪些是 iTop 產生的（教練可能自己歸過類）。

**教練的結論（他自己回憶）**：HiDock 裝置有「是否把錄音轉移到電腦存檔」的選項；打開 App 才上傳雲端，電腦本機不留檔，要手動下載才會有。他的雲端另有容量上限（他記得「好像多少 G」，我沒查證）。

**沒查的**：`%TEMP%` 裡有沒有上傳暫存；插著錄音裝置時 F:／S:（目前是空的抽取式磁碟機）會不會掛載；HiNotes 雲端實際用量。

**How to apply**：教練再問 HiNotes 錄音位置 → 先講「電腦沒留檔、在雲端，手動下載才在 D:\Users\Downloads」；要釋放 D 槽容量，該看的是 `D:\Users\Downloads` 的音檔，不是 HiNotes。Windows 上掃 Chrome 資料先 `fsutil reparsepoint`／看 LinkType，別被 C 槽路徑騙了。
