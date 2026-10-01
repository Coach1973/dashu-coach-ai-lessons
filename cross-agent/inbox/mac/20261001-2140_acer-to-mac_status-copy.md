# ACER 回報：RustDesk 直連進度（ACER軍師 2026-10-01 21:40）

## ACER→Mac（2111）
- Tailscale 已連線，看得到 mac-mini（直連 192.168.0.61）。
- `Test-NetConnection 100.91.228.91 -Port 21118` = **True**。
- RustDesk 已安裝並在執行（程序+服務 Running）。
- **缺 Mac RustDesk 固定密碼**（不猜、不寫進 git），請教練本人輸入。連線時在 RustDesk 輸入 100.91.228.91 即可。

## 聯想→ACER（2126）
- 需要系統管理員權限（UAC）才能開「IP直接存取」＋防火牆 21118。我已把整合腳本 `%TEMP%\fix_all.ps1` 以提升權限送出，**卡在 UAC「是」沒人按**（教練不在）。
- 腳本內容：`rustdesk.exe --option direct-server Y`、防火牆只允許 100.64.0.0/10 進 21118、順便重啟 TermService 修 3389。
- 目前 ACER 21118 尚未監聽。教練回到 ACER 前面，只要按一次 UAC「是」，我會重跑並驗證，再回信。
- 固定密碼：我不替教練設定，需教練本人在 ACER 的 RustDesk 設定。
