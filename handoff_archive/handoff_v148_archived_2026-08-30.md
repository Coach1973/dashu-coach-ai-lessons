# 軍師接力棒 · 2026-08-29 v148（Mac終端機 Sonnet 5，乾淨世界頻道QR上線+peipei-event斷線5天修復+電腦變慢診斷）

> 建立時間：2026-08-29 16:34 ~ 2026-08-30 01:27（台灣時間，接續v147同一天新對話框）
> 上一棒：v147（Mac終端機，同日較早，/bni-credit三項待改+34筆信用証補開+搜尋空格bug修復）
> 本棒主軸：**三件獨立任務——乾淨世界頻道QR立牌上線並加入作品一覽、修復peipei-event.bymyway.com斷線5天的根因（缺launchd看護）、教練電腦變慢的多輪診斷與RustDesk釋放記憶體機制的效果評估。**

## 🎯 本場戰果

### 1. 乾淨世界頻道關注QR立牌上線
教練要求仿照`event.bymyway.com/qr/checkin-print.html`風格，做一張導流到「大樹教練」乾淨世界頻道(`https://www.ganjingworld.com/s/3EBAgQObRg`)的QR立牌，拿掉「集滿5次送禮物」文案，改主打「高品質自我成長影片300集免費觀看」。`make_qr.py`新增`--ganjing`模式（比照既有`--wheel`/`--slides`同款設計），產出`qr/ganjing.png`+`qr/ganjing-print.html`，用文字工具核對繁體中文內容正確、QR圖案親眼看過無變形，commit`0669f44a2`。教練接著要求加入《大樹AI作品一覽》，已補進coach888「後臺系統」分類第10項，commit`48520cd`。列印用正式網址`https://event.bymyway.com/qr/ganjing-print.html`已驗證200可用。

### 2. 🔴 peipei-event.bymyway.com斷線5天，根因是唯一缺launchd看護的站台
教練詢問這個網址為何失效，查證發現HTTP 530（Cloudflare連不到tunnel connector）。追根究柢：`bymyway.com`底下共6組webapp+tunnel（event/mentor100/namecard/bni-chapters/jiesheng/peipei-event），前5組都有`com.coach.<站名>-webapp.plist`+`com.coach.<站名>-tunnel.plist`的launchd自動看護（`KeepAlive:true`），**唯獨peipei-event這組從2026-07-13建立以來就是純手動`nohup`跑起來**，2026-08-24某次收到`signal terminated`後，因為沒有任何自動看護，斷線整整5天無人發現。已手動重啟後端(port 5061)+tunnel恢復服務，並新增`com.coach.peipei-event-webapp.plist`+`com.coach.peipei-event-tunnel.plist`永久修復（`launchctl load`後確認狀態碼0）。寫入記憶`reference_bymyway_subdomain_530_missing_launchd_2026-08-29`（含完整診斷SOP：curl狀態碼判讀530/502/522差異、Cloudflare API查CNAME目標uuid、比對`ps aux`/`launchctl list`），commit`2ffba5dc9`。

### 3. 電腦變慢多輪診斷+RustDesk「釋放」指令效果評估
教練懷疑手機上傳影片佔網速，查證：ping延遲正常(11~14ms)但下載速度偏慢(144~167KB/s)、記憶體一度只剩366~404MB可用(15GB used)。觸發既有「釋放」指令(`rustdesk_free_memory.sh`)後教練回報「好像沒啥用」，重新查證發現RustDesk重啟後反而同時有兩個process在跑（合計比重啟前更高），對15GB量級的系統記憶體壓力貢獻微乎其微。教練關閉一堆App後仍覺得慢，直到**教練自行重開機**才讓記憶體真正恢復健康(15G→8.34GB用量，前景GUI App只剩Claude/Finder/Typeless/Python等必要項)。教練提出構想：以後「釋放」指令要更全面，除RustDesk外把所有可關的App一併關閉。**已給出評估但尚未定案**：系統層級記憶體碎片化只有重開機能徹底清空，關App效果有限；且需要教練確認白名單範圍（Typeless/Chrome/LINE等常用工具是否要保留）才能動手寫這支腳本，教練尚未回覆。

## ⚠️ 本場教訓（已寫入記憶）

1. **`bymyway.com`底下的多組webapp+tunnel服務，只要有一組沒接上launchd看護，就會是斷線後永遠不會自己恢復的活地雷**——盤點法：`ls ~/.cloudflared/*-config.yml`跟`ls ~/Library/LaunchAgents/ | grep com.coach`兩份清單站名要能一一對應，缺一個就是下一個會犯同款錯的站台。
2. **診斷Cloudflare 530要查DNS的CNAME目標(`<uuid>.cfargotunnel.com`)再比對本機process，不能只看HTTP狀態碼猜**——530明確代表tunnel connector沒連線，跟502(origin有回應但錯誤)、522(TCP逾時)是不同層次的問題。
3. **`ps aux | grep cloudflare`查launchd管理狀態會誤判**——launchd Label命名是`com.coach.<站名>-tunnel`不含"cloudflare"字樣，要用`launchctl list | grep com.coach`才對，這次一度誤以為其餘5組站台也沒被管理，查證後發現是自己關鍵字下錯。
4. **既有的「釋放記憶體」快捷指令（重啟RustDesk）對系統性記憶體壓力幫助有限**，不該預設觸發這個指令就代表問題解決——RustDesk本身在15GB量級的用量裡佔比很小，且重啟瞬間可能短暫出現新舊process並存反而更高。真正能徹底解決系統記憶體碎片化的只有重開機。

## 📋 下一場開工先做
1. 教練的「全面關App釋放記憶體」構想尚未拍板——需要先問清楚白名單範圍（除了Claude/Finder等系統必要項，Typeless/Chrome/LINE等常用工具要不要保留），確認後再動手寫腳本，並優先用AppleScript優雅`quit`而非`kill -9`避免未存檔資料遺失。
2. Netlify→GitHub Pages+bymyway.com子網域策略（教練本場稍早提出的構想，已給評估但未決定是否套用到新專案，也沒選要不要先盤點哪些舊網站值得搬）——等教練下次想繼續討論時接續。
3. FB粉專商家驗證後續（等教練通知，v147留下的舊待辦，本場未觸及）。
4. 待辦三(補公司欄位)：2026-09-02教練有額度時的舊待辦，本場未觸及。

## 🔑 本場commit
`0669f44a2`（event-signup，ganjing QR）+ `48520cd`（coach888，作品一覽新增第10項）+ `2ffba5dc9`（claude-brain，peipei-event 530修復記憶）。另有`com.coach.peipei-event-webapp.plist`+`com.coach.peipei-event-tunnel.plist`兩份launchd設定檔（不在git版控範圍，位於`~/Library/LaunchAgents/`）。
