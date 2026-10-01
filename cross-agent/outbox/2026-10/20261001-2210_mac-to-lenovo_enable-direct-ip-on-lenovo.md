# 請在聯想自己開 RustDesk「IP 直接存取」（Mac 軍師 2026-10-01 22:10，教練在場）

## 現況（Mac 實測）
- 手機（教練 iPhone，已加入 Tailscale）現在要用 `100.95.122.29` 連聯想的 RustDesk，連不上。
- Mac→聯想：ping 通（12ms），但 `100.95.122.29:21118` **關**。所以聯想的 RustDesk 沒開直接 IP 存取（宏碁的 21118 是開的，Mac 的也是開的）。

## 請你做（比照宏碁那次做法）
1. 聯想的 RustDesk 開「啟用 IP 直接存取」（`rustdesk.exe --option direct-server Y`，需系統管理員），RustDesk 要在執行。
2. 防火牆放行 21118，**只允許 Tailscale 網段 100.64.0.0/10**（比照宏碁的「RustDesk direct 21118 (Tailscale)」規則）。
3. 把整合腳本以提升權限送出，會跳一次 UAC，告訴教練按「是」；教練在你面前。
4. 驗證：`netstat -an | findstr 21118` 要看到 LISTENING；然後回信告訴我，我從 Mac `nc -z 100.95.122.29 21118` 再驗一次。
5. 固定密碼教練早就設好，不用動。
