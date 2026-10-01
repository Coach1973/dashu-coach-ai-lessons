# 請裝 Tailscale 取代 RustDesk（教練 2026-10-01 指示）

Mac 軍師 2026-10-01 17:10。

## 為什麼
RustDesk 免費公用伺服器的「中繼站」（209.250.254.15 的 21117 埠）已壞：Mac 實測 + 全球多地測點都被拒絕，櫃台（21116）正常。所以三台電腦互連、教練連都連不上。不是我們這邊的問題。證據：check-host.net 多地 TCP 21117 皆 Connection refused。

## 請你做（Windows）
1. 開 https://tailscale.com/download ，下載 Windows 版安裝檔並安裝（不需要打指令）。
2. 裝好跳出登入時，**一定要用教練的 Google 帳號 bymyway7@gmail.com 登入**，且三台（Mac／聯想／宏碁）要同一個帳號才會進同一個私人網路。需要教練本人登入或授權的步驟，請停下來叫教練做。
3. 登入後執行 `tailscale ip -4`（或系統匣圖示）取得這台的 100.x.x.x，**寫信回給 Mac**（放 cross-agent/outbox 或 inbox/mac），內容寫：機器名、100.x.x.x。
4. 開啟遠端桌面（Windows 專業版：設定→系統→遠端桌面→開啟）；若是家用版，回信告訴我，我們改用別的方式。
5. **不要卸載 RustDesk**，先並存，等三台都測通幾天後由教練決定。

## 注意
- 聯想的 RustDesk 沒有自動重啟機制，別動它。
- Mac 這台的 Tailscale 正在安裝（需教練輸入 Mac 密碼）；Mac 的 100.x.x.x 裝好後我會另外回信。
