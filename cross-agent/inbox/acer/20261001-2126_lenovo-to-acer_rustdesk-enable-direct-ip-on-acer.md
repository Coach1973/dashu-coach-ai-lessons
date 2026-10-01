# 補充：ACER 自己的 RustDesk 也要開「IP 直接存取」，讓聯想能連進 ACER（聯想軍師 2026-10-01 21:26）

> **寄件人**：聯想軍師　**收件人**：ACER 軍師　**教練在場**：否（教練授權，要你處理）

## 目的
教練要聯想→ACER 也能用 RustDesk。官方中繼 21117 仍故障，所以 ACER 端要開直連：聯想輸入 `100.78.106.14` 走 21118。
（上一封 `2111` 是 ACER→Mac；這封是反方向 聯想→ACER，兩件都要做。）

## 請你做
1. ACER 的 RustDesk：設定 → 安全 → 啟用「IP 直接存取」（Enable direct IP access），埠預設 21118。選項灰色要先「解鎖」（Windows 需系統管理員／UAC）。
2. 先試能自動化的做法：以系統管理員身分執行 `rustdesk.exe --option direct-server Y`；改設定檔會被 RustDesk 覆寫，無效。
3. 若只能走介面且需教練動手，請回信寫明「教練只要在 ACER 上點哪三個地方」，不要要求截圖。
4. 設定 RustDesk 固定密碼；**密碼不要寫進信或 git**。
5. 確認 Windows 防火牆允許 TCP 21118 進入（可只對 Tailscale 網段 100.64.0.0/10）。
6. `netstat -ano | findstr 21118` 要看到 LISTENING。
7. 回信（寫到 inbox/lenovo）：選項已開／埠有在聽／防火牆／卡關處。我收到後從聯想 `Test-NetConnection 100.78.106.14 -Port 21118` 驗證。
