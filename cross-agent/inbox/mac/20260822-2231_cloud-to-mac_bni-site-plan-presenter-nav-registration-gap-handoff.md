# 三件事交接：BNI大樹學堂規劃＋展示切換列待部署＋bigtree報名雙寫缺口待完成

> **寄件人**：雲端Claude Code session（教練用手機/網頁連線開的，不是本機Mac mini，這種身份還沒有既有代號，暫稱「cloud」）
> **收件人**：Mac
> **時間**：2026-08-22 22:31 台灣時間
> **教練是否在場**：是，教練本人下令要求把這場對話的問題整理成信寄給Mac
> **回覆要求**：需要執行（含2件待Mac動手完成的技術任務），不須回信，直接在下一場Mac session的接力棒續寫即可

## 內容

這場雲端session做了三件事，其中兩件**因為碰不到Mac mini本機（沒有event.db、沒有OpenClaw gateway、沒有claude-in-chrome），只能做到「規劃/寫好程式碼」，最後一哩路要靠Mac完成**。教練親自確認過這個環境限制（我有做hostname/路徑/process檢查證明給他看），所以才有這封信。

### 一、BNI大樹學堂官網規劃（bni.bymyway.com）—— 純規劃，無待辦，僅供知悉

教練想把他所有講BNI主題的YouTube影片整理成一個教學網站，仿照mentor100/chapters.bymyway.com的Flask+SQLite架構，走闖關式學習路徑+測驗+排行榜遊戲化機制。完整規劃見`knowledges/2026-08-21_BNI大樹學堂官網規劃_bni.bymyway.com.md`。

**目前狀態**：教練說BNI相關影片實際只有約20支（不是原先以為的300+，那是他所有影片的總數），且已認領要自己去YouTube帳號整理連結清單給AI。**這件事現在卡在等教練提供清單，沒有Mac要動手的部分，純知會**。哪天教練說「YouTube清單給你了」，直接接手寫程式碼骨架即可，規劃檔裡資料庫schema、頁面結構都已經想好了。

### 二、展示用快速切換列 —— 程式碼已寫好推上main，⏳待Mac pull+重啟服務

教練反映現場做講座時常要在「簽到頁／轉盤頁／後台」三個網頁之間切換很麻煩，希望同一頁內能直接跳轉。

**已完成**：在`event-signup/templates/checkin.html`、`wheel.html`、`admin.html`三個範本裡，加了共用元件`templates/_presenter_nav.html`（右下角固定小工具列，📷簽到／🎡轉盤／⚙️後台三顆圓形按鈕，點了直接跳轉）。已用`jinja2.Environment(loader=FileSystemLoader('templates'))`本機解析驗證三個模板+include都能正確載入，commit`bc31134`已推main。

**待Mac做**：
```bash
cd ~/.openclaw/workspace && git pull
launchctl kickstart -k gui/$(id -u)/com.coach.event-webapp   # 或教練慣用的重啟方式
```
重啟後訪問`/checkin`確認右下角有出現三顆按鈕即代表生效。

**⚠️ 這3個頁面是我對教練口述的猜測**（他講的是「後台掃描報到、滾輪掃描報到、後台滾輪」，我對照系統路由猜是`/checkin`+`/wheel`+`/admin`），Mac部署後教練實測若發現猜錯了，直接問他要哪3頁，改`_presenter_nav.html`裡3個連結的`href`即可，5分鐘內能改完。

### 三、🔴🔴🔴🔴 重大發現：bigtree-tw報名表單從未真正寫入資料庫，需要Mac完成最後一步

**觸發原因**：教練反映金門場(8/21)報名數異常——當地推廣人員說有十幾個報名，但用LINE訊息統計出來只有5個。

**查證結果**（完整版見`knowledges/2026-08-21_bigtree報名雙寫缺口調查_金門場報名數異常.md`）：查`bigtree`這個repo，官網主表單`submitRegistration()`（`index.html`約611行）送出報名時，**只打了兩支都不落地存資料庫的Netlify函式**（`sme-register-fn`純轉發、`xiaolongxia-notify`純推播佩佩老師），**全站所有場次都沒有呼叫`/api/register`**。用`git log`+全repo`grep "slug"`確認整個commit歷史裡`index.html`從未寫過這段程式碼——舊接力棒記錄寫「已建`/api/register`端點+15場session slug+bigtree前端雙寫，deploy已上線」，**這句話是錯的，前端雙寫從來沒真的做過**（後端`event-signup/app.py`的`/api/register`端點倒是真的存在、程式邏輯也正常，只是前端沒接上去）。

也就是說：不只金門場，**所有場次的報名，長期以來都只活在教練LINE的通知訊息裡，沒有一筆真正進資料庫**。金門場的「5」很可能就是唯一有留下數位痕跡的報名，推廣人員說的十幾個如果是走口頭/當地群組收單，從來沒碰過網站表單，就完全不在任何系統裡——是根本沒被看見，不是bug漏接。

**已經想好修法**，卡在雲端session拿不到的東西：
```bash
# 需要Mac在有event.db存取權限的環境跑這個，把結果貼進這封信的回信或下一棒接力棒：
cd ~/.openclaw/workspace/event-signup
./venv/bin/python3 -c "
import db
conn = db.get_conn()
for r in conn.execute('SELECT slug, name, event_date FROM events ORDER BY event_date').fetchall():
    print(r['slug'], '|', r['name'], '|', r['event_date'])
conn.close()
"
```
拿到真實slug清單後，在`bigtree/index.html`的`submitRegistration()`裡（`sme-register-fn`/`xiaolongxia-notify`那兩個`fetch`旁邊）多加一個真正打`https://event.bymyway.com/api/register`的`fetch`，帶對應場次的真實`slug`。**修復code骨架已經寫在調查檔案裡**，只差真實slug對照表沒有就不敢先猜著寫上去——因為`/api/register`對查無slug的請求會回`{"ok": false}`但HTTP狀態碼仍是200，猜錯了畫面上完全看不出來，等於又製造一次跟這次一樣的假象。

金門場今天已經流失的報名沒辦法技術復原，如果推廣人員手上有名單，可以請教練口述給任何一台機器，用`/admin`後台手動補登即可（不影響簽到/集點功能）。

## 對應檔案

- `knowledges/2026-08-21_BNI大樹學堂官網規劃_bni.bymyway.com.md`
- `knowledges/2026-08-21_bigtree報名雙寫缺口調查_金門場報名數異常.md`
- `event-signup/templates/_presenter_nav.html`＋`checkin.html`／`wheel.html`／`admin.html`
- commit：`b77da32`（BNI學堂規劃初稿）、`bc31134`（展示切換列）、`aa0fd16`（bigtree調查+接力棒更正+規劃補充）
- `JUNSHI_HANDOFF_LATEST.md`待辦表已同步更新（第一列🔴🔴🔴🔴 bigtree雙寫缺口、新增一列🟢展示切換列）

## 完成後請做

- [ ] 讀完
- [ ] 執行：pull+重啟服務讓展示切換列生效；跑上面那段查詢拿到event.db真實slug清單，接著把bigtree前端雙寫真正寫完
- [ ] 把本檔移到 `outbox/2026-08/`
