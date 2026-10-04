---
name: feedback-mac-preboot-volume-not-pending-update-2026-10-03
description: Mac 的 Preboot 磁碟區（約18GB）是開機用檔案，不是已下載的系統更新；10/02 被貼錯標籤，教練 10/03 追問才發現；更新完不會省出 18GB
metadata:
  type: feedback
---

10/02 前一場量空間，把 `diskutil apfs list` 的 Preboot 卷（17.9GB）說成「已下載、還沒安裝的系統更新約 18GB，更新完會清掉」。實測不是：Preboot 內是開機檔與 Cryptexes；本機真正的更新下載檔只在 `/Library/Updates`（6/27、9/15 舊殘留 1.1GB）與 `/System/Library/AssetsV2/com_apple_MobileAsset_MacSoftwareUpdate`（10/03 才開始下載）。

**Why**：教練 10/03 追問「不是說下載暫存檔有 18G 嗎？為什麼還要重新下載？」——標籤沒驗證，害他以為更新檔早就下載好、更新完就省 18GB。
**How to apply**：回報空間時每一塊要對應到量過的路徑；量不到就說「系統用的，沒辦法確認內容」。不要承諾「更新完會省出空間」。已有反射 `R-DISK-LABEL-VERIFY` 撐著；案例見試金石案例100。
