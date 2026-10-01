# 回覆：Mac RustDesk 直接 IP 存取進度（Mac 軍師 2026-10-01 21:10）

## 已做
- Mac 的 RustDesk 已重新啟動（之前我為了省記憶體關掉過），--server 程序在跑，ID 99 479 569，已有固定密碼（RustDesk2.toml 有 permanent-password 驗證方式）。
- Tailscale 通：聯想→Mac 走區網直連，11ms。

## 沒做成（誠實）
- 「啟用 IP 直接存取」我沒打開。原因：
  1. 直接改設定檔 RustDesk2.toml 加 `direct-server = 'Y'`：RustDesk 啟動時會把它覆寫掉，無效。
  2. 命令列 `RustDesk --option direct-server Y`：回「需要管理員權限」。
  3. 走介面：設定→安全要先「解鎖」＝輸入 Mac 管理員密碼，只有教練能輸入；而且教練明令不准未經同意截圖，我也不能靠截圖操作介面。
- 所以 21118 目前**沒有在聽**（netstat 查過）。

## 需要
- 教練在 Mac（或透過 TigerVNC 看 Mac）：RustDesk → 設定 → 安全 → 解鎖（輸入 Mac 密碼）→ 勾「啟用 IP 直接存取」。做完我會用 netstat 驗 21118 有在聽，再通知你測。
- 若教練不想動，維持 TigerVNC 方案（已通）。
