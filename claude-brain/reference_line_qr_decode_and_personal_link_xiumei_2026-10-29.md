---
name: reference-line-qr-decode-and-personal-link-xiumei-2026-10-29
description: 教練給 LINE QR 圖時怎麼解碼成加好友連結（scratchpad opencv 虛擬環境，不裝系統 Python）；QR 內容是 line.me/ti/p/<代碼>，不是文字 ID；鄭綉美個人 LINE 正確代碼 b6hkGJBpdU（10/29 教練糾正舊的 aYDPnfRMc3）
metadata:
  node_type: memory
  type: reference
  originSessionId: 9c86f7c2-18f7-4cd2-9341-58f58670f78c
  modified: 2026-10-29T01:27:42.961Z
---

教練丟 LINE 的 QR code 圖來，要網頁能讓電腦掃、手機點直接加好友時：

- **解碼**：系統 Python 沒有 cv2（PEP 668 擋 pip）。在 scratchpad 建虛擬環境 `python3 -m venv <scratchpad>/qrvenv`，`pip install opencv-python-headless`，用 `cv2.QRCodeDetector().detectAndDecode(img)` 讀。10/29 的圖一次就解出來。
- **內容**：解出來的是 `https://line.me/ti/p/<代碼>`，是加好友連結，**不是**文字 ID（`@xxxx` 那種）。文字 ID 要本人到 LINE 個人檔案找，QR 無法反推。
- **綉美個人 LINE**：正確代碼 `b6hkGJBpdU`（10/29 教練給的新圖）。舊的 `aYDPnfRMc3` 是錯的，已從 `xiumei/index.html` 拿掉（commit 39bffa9）。公司 LINE `@562hjdjz` 不受影響。
- **頁面做法**：按鈕 `href` 用 `line.me/ti/p/<代碼>`（手機點開直接加好友）＋下方放 QR 圖檔放在 `assets/`（電腦掃）。

**Why:** 教練糾正「之前個人 LINE 是錯的」，要我用他給的 QR 把連結換對，並讓電腦上能掃。
**How to apply:** 教練再丟 QR 圖 → 用上面的虛擬環境解碼 → 核對是不是 `line.me/ti/p/...`；看到是 `line.me/R/ti/p/@...` 的是官方帳號，不是個人。
