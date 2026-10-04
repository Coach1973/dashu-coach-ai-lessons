---
name: reference-claude-cowork-vm-bundle-10gb-2026-10-03
description: Claude 桌面版 ~/Library/Application Support/Claude/vm_bundles（10GB）＝Cowork 功能的 Linux 虛擬機，最後使用 9/21，已搬到外接 SSD 改捷徑，舊夾留到 10/09
metadata:
  type: reference
---

`vm_bundles/claudevm.bundle`：`rootfs.img`（10GiB，Linux 磁碟）、`sessiondata.img`（224MB，疑似 Cowork 工作資料）、`vmlinuz`／`initrd`（開機核心）。只有 Claude 桌面版的 Cowork 功能用到；Code 分頁（這個對話）在 Mac 本機直接跑，不在這台虛擬機裡。日誌 `~/Library/Logs/Claude/cowork_vm_*.log`：VM 啟動過 6/11–6/13、7/2、9/21（最後關機 9/21 07:36 台灣時間），之後只有每天比對版本。

**How to apply**：不要刪（`sessiondata.img` 可能有工作資料，且沒測過重新下載）；已用 `scripts/move_to_ssd.sh` 搬到 `/Volumes/953-SSD/Mac本機搬移_20261003/Claude_vm_bundles`，本機是捷徑，舊夾 `vm_bundles.bak.20261003` 10/09 後再刪。更新重開後要確認 Cowork 還能開。
