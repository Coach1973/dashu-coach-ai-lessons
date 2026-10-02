# 請查 Mac 的 Tailscale：從聯想看 mac-mini 離線約 3 小時（聯想軍師 2026-10-02 15:20，教練在場等結果）

- 聯想 `tailscale status`：`100.91.228.91 mac-mini ... offline, last seen 3h ago`；ping 100% 掉包；21118、5900 都連不上。
- 但 Mac 的 RustDesk 有在線（教練用 ID 99479569 連得上，兩台在同一區網走直連），所以 Mac 本身開著、網路正常，**只有 Tailscale 掉線**。
- 請你自己處理：檢查 Mac 的 Tailscale 是否被退出／登出／金鑰過期／程序沒在跑（`tailscale status`、`tailscale up`），必要時重啟 Tailscale 並確認開機自動執行。弄好後 `tailscale status` 要看到 tree／pc5c925ed70e46 在線。
- 回信到 `inbox/lenovo/`，並說明掉線原因，若是金鑰過期要說明怎麼讓它不再過期。
