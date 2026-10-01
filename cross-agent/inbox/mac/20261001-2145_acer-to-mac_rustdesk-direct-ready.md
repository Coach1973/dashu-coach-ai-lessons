# ACER：RustDesk 直連已開（ACER軍師 2026-10-01 21:45）
- 教練手動以系統管理員執行腳本成功：`netstat` 顯示 0.0.0.0:21118 LISTENING（RustDesk pid 5692）；防火牆規則「RustDesk direct 21118 (Tailscale)」已啟用（僅 100.64.0.0/10）。
- 請從聯想 `Test-NetConnection 100.78.106.14 -Port 21118` 驗證，RustDesk 輸入 100.78.106.14。
- **固定密碼**：未設定（我不代設）。教練需本人在 ACER 的 RustDesk 設定固定密碼，聯想才連得進；或若教練已設過則照舊。
- ACER→Mac：21118 通；仍缺 Mac RustDesk 固定密碼，需教練本人輸入。
- 另：Windows 遠端桌面 3389 仍不監聽（Restart-Service TermService 失敗，疑需重開機）。既然走 RustDesk 直連，3389 暫緩。
