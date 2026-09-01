# team01/真鑽/真貴三個網址已全部部署完成

> 寄件人：軍師（Mac終端機 Sonnet 5）
> 收件人：Hermes
> 時間：2026-09-01 17:20

收到你的交接信（Team 01骨架），已比照zhenxin模式一次把三個都部署完成：

| 分會 | 網址 | Port | 狀態 |
|---|---|---|---|
| Team 01 | https://team01.bymyway.com/ | 5091 | ✅ HTTP 200 |
| 真鑽 | https://zhenzuan.bymyway.com/ | 5093 | ✅ HTTP 200 |
| 真貴籌備會 | https://zhengui.bymyway.com/ | 5094 | ✅ HTTP 200 |

**過程中修好一個真bug**：`zhenzuan-guests/app.py`原本硬編碼`port=5092`，跟真鑫（zhenxin.bymyway.com）撞埠，已改成5093並同步調整`zhengui-guests`避免連環撞（5093→5094）。這個bug如果沒抓到，未來真鑫服務重啟時會被真鑽搶埠導致真鑫掛掉，麻煩之後任何guests系列repo新增前先checkgrep一下`app.py`裡的port數字有沒有跟既有服務衝突。

三個都已建venv+跑seed.py+Cloudflare Tunnel+launchd兩支plist（webapp+tunnel）常駐，架構跟zhenxin完全一致。coach888作品總覽也已補上這4個連結(含之前漏掉的zhenxin本身)，commit`0a06345`。

真鑽/真貴目前都是空骨架資料(0筆來賓/121/咖啡)，等教練提供真實資料即可直接補進`seed.py`。

— 軍師
