---
name: reference-lenovo-to-mac-tigervnc-tailscale
description: 聯想連蘋果電腦的現行方式（RustDesk 官方中繼 21117 壞掉後改走 Tailscale＋TigerVNC），含位址、帳號、桌面捷徑、已知限制
metadata:
  node_type: memory
  type: reference
  originSessionId: 58f267ff-3bc9-45af-8ff0-abf6ca10f288
  modified: 2026-10-01T10:43:42.898Z
---

2026-10-01 RustDesk 官方公用中繼站（rs-ny.rustdesk.com:21117，同 IP 其他埠皆通）故障，三台電腦互連全斷，改走 Tailscale 私人網路。

**聯想→蘋果（教練真正要的方向，已通）**
- 聯想桌面捷徑「連蘋果電腦」＝TigerVNC 1.16.2，參數 `-AlwaysCursor=1 -CursorType=System 100.91.228.91::5900`。
- 登入：Mac 帳號 `bymyway` ＋ **Mac 開機密碼**（ARD 驗證，不是 VNC 密碼；密碼我不碰）。
- Tailscale：聯想 `tree` 100.95.122.29，Mac `mac-mini` 100.91.228.91，同一帳號 bymyway7（教練本人登入）。
- Mac 兩個螢幕已改鏡像（單螢幕 1920x1080），因為 TigerVNC 官方版沒有縮放到視窗，雙螢幕併圖會被裁切。還原用 `scripts/mirror_second_display.swift off`。
- 若螢幕又異常，截 TigerVNC 視窗自己看（PowerShell GetWindowRect＋CopyFromScreen 只截該視窗），不要叫教練描述。

**蘋果→聯想（教練不需要）**：Windows 遠端桌面教練已在設定打開（3389），帳號 `TREE\bymyway` 是本機帳號、教練不記得密碼；要用請他自己在系統管理員終端機 `net user bymyway *` 重設（錯誤碼 5＝終端機沒用管理員開，不是失敗次數）。我不改密碼、不用指令開 RDP（系統安全設定）。

**Why:** 這是 RustDesk 修好前教練唯一能用的遠端路徑，且之後會重複用到。
**How to apply:** 教練說「連不上蘋果／RustDesk 壞了」，先確認方向，再看這份；RustDesk 官方修好（21117 通）才考慮回頭用它。RustDesk 兩台都沒卸載。
