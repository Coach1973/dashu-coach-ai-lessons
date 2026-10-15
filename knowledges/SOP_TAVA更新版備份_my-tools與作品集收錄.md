# SOP：教練丟「TAVA 更新版網址」→ 更新 GitHub 備份 → 收進 my-tools 與作品集（2026-10-15 教練定）

教練原話（10/15）：「我只要丟更新版的網址，你就知道你要去更新什麼東西。更新完之後，直接再幫我上架到我的作品集跟常用。」
起因：TAVA 每出新版，網址都是全新的（v1 `/chat/zzphp46s9b/…`、v2 `/chat/eo63j7e7tu/…`），沒有固定網址可輪詢，所以靠教練丟網址觸發（事件觸發，不排程）。

## 觸發
教練貼 `https://www.tava-ai.com/chat/<代碼>/<檔名>.html`（常附「更新到 …」或只貼網址）。

## 步驟（全部自己做，不問教練）
1. **抓原頁**：`curl -sL -o /tmp/x.html <網址>`，確認 200、是 HTML。
2. **找對應的備份倉庫**：
   - 先看教練有沒有寫目標；沒寫就在 `~/github_repos/*/README.md` 找「原頁（TAVA）」網址、或比對 `<title>` 與 `index.html`（例：`tava-brand-web-playbook` 的標題「個人行銷／品牌網頁｜開工指令與製作經驗」）；`~/github_repos` 沒有就 `gh repo clone Coach1973/<名>`。
   - 找不到對應倉庫＝這是新頁：新建 `Coach1973/<標題轉拼音或教練指定名>`、開 Pages，照 my-tools 拷貝流程做（1:1 拷貝），再往下走 3～5。
3. **更新備份**：先 `git pull`；`index.html` 用新原頁 **1:1 覆蓋**（README 若記有「僅一處修改」，先確認新版是否仍需要，並用 `diff` 看新版差異）；README 改成新原頁網址、保留舊版網址、寫「v2 比 v1 新增什麼」；commit（`[Mac]` 前綴）＋push；等 Pages 更新後 `curl <pages網址> | cmp - /tmp/x.html` 確認逐位元相同。
4. **my-tools（大樹常用查詢網站）**：`~/github_repos/my-tools/build.py` 的 `S` 清單裡，該條說明改成「…vN（我的 GitHub 備份，一模一樣；日期更新，新增…）」，跑 `python3 build.py`，commit＋push，抓回線上確認。新頁就在對應分類加一條。
5. **作品集（coach888）**：`python3 scripts/coach888_register_admin.py <備份網址> "<名稱 vN（TAVA，GitHub備份）>" --section <原本所在分類代碼> --badge 工具 --no-vault`（同網址重複登記只更新名稱，不會重複；既有分類先 `--list`／讀 `coach888_layout` 查，不要搬位置；新頁預設放 `bymyway`＝工具類，教練說放「大樹常用」才用 `changyong`）。讀回確認。
6. **交付**：網址各自獨立一行，`scripts/deliver_open.sh <網址>` 開 Chrome；回報講「備份已是 vN（cmp 相同）」「my-tools 已改」「作品集已改」＋各 commit hash。

## 例（10/15）
`personal-brand-playbook-v2.html` → 倉庫 `tava-brand-web-playbook`（commit 443a8d8）→ my-tools（d70703e）→ coach888 工具類改名 v2。
