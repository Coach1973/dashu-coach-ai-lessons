---
name: rustdesk-direct-ip-over-tailscale
description: 官方中繼21117壞時，聯想RustDesk輸入Mac的Tailscale IP 100.91.228.91直連成功，免中繼免自架
metadata:
  type: reference
---

聯想→蘋果最佳方式（2026-10-01 21:04 教練實測成功）：聯想 RustDesk 遠端ID欄輸入 `100.91.228.91`（不是ID 99479569），輸蘋果固定密碼。

**Why:** 官方 rs-ny.rustdesk.com 的 21117 中繼埠壞；ID 連線要先等約18秒打洞再走中繼才失敗。Mac端須在 RustDesk 設定→安全→解鎖（Mac管理員密碼，只教練能輸）→勾「啟用IP直接存取」（埠21118），AI無法代做（設定檔會被覆寫、命令列要管理員）。

**How to apply:** 連不上先 `Test-NetConnection 100.91.228.91 -Port 21118`。備援仍是 TigerVNC 捷徑，見 [[reference_lenovo_to_mac_tigervnc_tailscale_2026-10-01]]。自架 hbbs/hbbr 是最後手段。

**2026-10-02 教練裁示更新：** 在家同區網直接用 ID（蘋果99479569）就通，Tailscale+IP 只是外出備援，教練不想一件事做兩種。蘋果的 Tailscale 是教練自己關的，看到它離線別當故障、別叫 Mac 去修（白寫過一封信）。遇到「離線」先想是不是教練自己關的。
