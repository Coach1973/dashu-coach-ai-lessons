---
name: reference-windows-bash-network-sandbox-isolation
description: 聯想Windows的Bash執行環境跟教練真實桌面/瀏覽器網路隔離，本機dev server(如127.0.0.1:5061)驗證要用靜態HTML快照+桌面開檔，不能指望瀏覽器工具連得到
metadata: 
  node_type: memory
  type: reference
  originSessionId: 938a6591-f076-4848-a9fe-6e4ae87442ef
  modified: 2026-07-26T07:29:53.160Z
---

這台聯想Windows的Claude Code，Bash工具執行環境跟教練實際桌面（Comet等真實瀏覽器）在網路層是隔離的兩個環境。2026-07-26做「結繩領導學工作坊戰報」（Flask本機dev server，port 5061）驗證時實測發現：

- Bash裡`curl`/`python urllib`能正常連到`127.0.0.1:5061`，Flask server確實在跑
- `mcp__Claude_Browser`工具的navigate/preview_start連127.0.0.1會失敗（"could not be opened"）
- `mcp__claude-in-chrome`（號稱教練真實Chrome）navigate後read_page顯示"Frame with ID 0 is showing error page"，同樣連不到
- 教練實際用`comet.exe`開同一個網址，親眼回報「無法連上這個網站」——證實連教練真正的桌面瀏覽器都連不到Bash啟動的伺服器

三種瀏覽器管道（Claude_Browser沙盒／claude-in-chrome／教練真實Comet）通通連不到，但都能開`file://`本機檔案（E:\Claude-Data底下的靜態檔案正常顯示），代表隔離的是「Bash執行環境的網路stack」，不是檔案系統。

**下次要驗證本機dev server（Flask/Node等需要真實伺服器互動的頁面）該怎麼做：**
1. 先用Bash自己模擬HTTP請求（`urllib`+`http.cookiejar`或`curl`）驗證邏輯正確性——登入/送表單/資料是否正確寫入，這部分Bash網路是通的，可以放心測
2. 把「已經渲染好、含真實資料」的HTML回應內容存成靜態檔案（`.write()`存成.html），`cp`到桌面`D:\Users\Desktop\`，再用`comet.exe <windows路徑>`（注意是檔案路徑不是http網址）開起來，教練螢幕上才真的看得到——比照[[feedback_html_delivery_to_desktop]]既有做法
3. 這份靜態快照只能證明「畫面渲染對不對」（版面/CSS/資料顯示），不能再互動（按鈕/表單送出要看步驟1的模擬測試結果），跟教練說清楚這個限制，不要讓他誤以為畫面上可以真的操作

Related: [[feedback_html_preview_chrome_only]]（Comet驗證鐵律本體，這次補上「本機dev server連不到」這個新坑的解法）
