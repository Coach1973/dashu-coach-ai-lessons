# jacky-brand 網站已改為 GitHub 版控（2026-09-30）

## 背景
教練問：jacky-brand（顧瀚鈞個人品牌頁）底層是不是寫在 GitHub 上？能不能用聯想電腦直接改 GitHub 讓網頁跟著更新，不用透過 Mac 本機？

**當下查證結果**：原本不是——`~/github_repos/jacky-brand/` 只是本機一個普通資料夾（zip上傳解壓出來的），沒有 `.git`，純靠 event-signup Flask app 直接讀本機磁碟服務（`/curated/jacky-brand/` 路由）。因為它是純靜態頁（一個 index.html + assets，沒有資料庫、沒有後端邏輯），git 化的成本很低，教練問完當場就做了。

## 已完成
- `~/github_repos/jacky-brand/` 已 `git init`，遠端：`https://github.com/Coach1973/jacky-brand`（私有 repo）
- 順手修掉教練回報的視覺bug：「為什麼回到台灣」區塊（`.band` class）3張卡片文字看不見——根因是 `.band{color:#e7ebf0}`（淺色，給深色背景用）往下蓋到卡片內文 `.pain .q`，但卡片本身背景是白的（`.card{background:var(--surface)}`），變成白底配幾乎白色的字。修法：加一行 `.band .card{color:var(--ink)}`，讓卡片內文字永遠用「淺色系統」自己的正常墨色，不論明暗模式都跟著 `--surface`/`--ink` 一起換，不會再錯位。已用瀏覽器 `getComputedStyle` 實際讀取渲染後的顏色值驗證（修前 text `rgb(231,235,240)` on 白底、修後 `rgb(17,24,32)` on 白底），不是只憑肉眼或工具回報。
- commit：本機 `25174ab`（jacky-brand repo 自己的 commit，不是 workspace repo）

## 跨機編輯怎麼運作（誠實版，不誇大）
1. **Lenovo（聯想）軍師**：`git clone https://github.com/Coach1973/jacky-brand.git`，用任何桌面App（VS Code/記事本/Claude Code自己）改`index.html`文字，`git commit && git push`即可，不需要碰Mac。
2. **回到Mac生效**：因為`/curated/jacky-brand/`是這台Mac的Flask直接讀本機磁碟服務，Lenovo push上GitHub後，**還需要這台Mac把最新版`git pull`下來**，網站才會真的更新——這一步目前沒有自動化（沒有webhook/cron），是因為這是低頻更新的個人靜態頁，暫時不需要建置一整套自動部署機制（N5自動化鐵律：不做用不到的預先設計）。
3. **實際流程**：教練在Lenovo改完push後，跟任何一台Mac的軍師說一聲（或下次開工時）「jacky-brand我在Lenovo改過了，幫我pull一下」，軍師執行：
   ```bash
   cd ~/github_repos/jacky-brand && git pull
   ```
   重新整理網頁就會看到新內容（Flask沒有快取，即時讀檔）。
4. 若教練往後常態需要「push完自動生效、不用喊一聲」，屬於新需求（加webhook或cron pull），到時候再建，不預先做。

## 相關
- 其他 `/curated/` 店家網站（別人上傳的）維持現行「zip上傳、不開放git」的設計，因為對象多半不熟git，這個決定不受本次影響。
- turnforyou 目前也還沒git化，跟jacky-brand同樣是教練個人創作，若教練也想要turnforyou可比照git化，屬於「等教練提起」，不主動做。
