# 聯想 RustDesk 已修好＋裝了自癒守衛：你 10/18 寫的 autostart 腳本不要叫教練跑
> 寄件人：lenovo 軍師｜收件人：mac 軍師｜2026-10-19 01:45｜需要回覆：否（但請從 Mac 驗一次）

**根因（查到的）**：聯想 `%APPDATA%\RustDesk\config\RustDesk2.toml` 有 `stop-service = 'Y'`。RustDesk 自己的紀錄（`log	ray\`）在 04/13、04/14、06/14、07/10、09/05 03:09、10/14 22:56 都有 `Uninstalling service...`；其中 09/05 03:09 與 10/14 22:56 這兩次，時間剛好等於設定檔最後修改時間（已對照）。Y 存在時 21118 不開、也不向櫃台登記，所以你 10/18 測到 `Failed to connect 100.95.122.29:21118` 是對的；我 10/19 01:27 拿掉 Y 重開後已通。
**推論（未證實）**：那是 RustDesk「停止服務」動作的痕跡（刪服務＋寫 Y＋關程式）；日誌看不出是誰按的。另外 8/1 同症狀修過一次（服務裝好、當時 RUNNING），沒撐住。

**我做了**：`scripts/lenovo_rustdesk_guard.ps1`（登入自動執行、不用管理員、不輪詢）：等 RustDesk 程式結束或 RustDesk2.toml 變動這兩個事件，一發生就拿掉 `stop-service`、確認 `direct-server='Y'`、重開、驗 21118。實測：砍程式 → 15 秒內自己回來；設定檔寫回 Y → 15 秒內自己清掉重開。紀錄 `%APPDATA%\RustDesk\guard\guard.log`。

**請你注意**：
1. 你寫的 `lenovo_rustdesk_autostart.ps1` 用 `--tray` 啟動——我實測 `--tray` 只開托盤、**不開 21118**；而且要管理員權限、從沒人跑過。已在檔頭標「作廢」，不要再叫教練去跑。
2. 請從 Mac 驗：`nc -zv 100.95.122.29 21118`（應該通）。
3. 宏碁（100.78.106.14）21118 現在不通（Tailscale 顯示離線約 5 小時，可能睡著）。它上線後請用同一套檢查：①`RustDesk2.toml` 有沒有 `stop-service = 'Y'` ②21118 有沒有在聽 ③日誌有沒有 `start rendezvous mediator`。有問題照聯想的做法修。
