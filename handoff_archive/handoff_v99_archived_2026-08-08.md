# 軍師接力棒 · 2026-08-05 v99（Mac終端機 Sonnet 5，opencode環境檢查報告review+bigtree金門場資訊補齊+結繩領導學官網大改版）

> 建立時間：2026-08-05 下午～晚上（台灣時間 19:00~21:10）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v98（Mac終端機 Sonnet 5，結繩領導學5項調整+GitHub自動部署推送，同日較早的獨立session）
> 本棒主軸：**三條主線。①教練把 opencode(MiniMax-M3) 寫的環境檢查報告轉來要我複審+反思「軍師為何沒抓到」，查證後發現報告本身也有兩處沒查證就下筆的瑕疵(自稱Opus5/CLAUDE.md鏡像關係)，回信給opencode+CORE_RULES新增R20+E12/E17鐵律擴充，順手在Repo1盤點時抓到`credentials/`真實金鑰從沒被`.gitignore`保護的真安全漏洞並修復。②bigtree大樹小講金門兩場補地址/座位/費用+時間修正(19:30-21:30)+隱藏3個已結束場次+新增「近期活動花絮」7/29真實照片輪播。③結繩領導學官網依教練提供的重構指令書全面重寫(新書發表→兩日工作坊銷售頁)，過程多輪UI微調，最後因未查證`jiesheng-leadership`是GitHub自動部署型，教練還沒說「推」就已經上線，是本場最大教訓。**

## 🎯 本場戰果

### 1. 🎯 opencode環境檢查報告review+CORE_RULES新增R20
教練把 opencode(MiniMax-M3) 主動做的「環境檢查」報告轉來，要我①檢查有無問題②反思「軍師為何沒抓到這些問題」。查證後發現報告本身有兩處未查證就下筆：a) 報告作者把自己(MiniMax-M3)誤植成「Opus 5」；b) 斷言`~/.claude/CLAUDE.md`跟`workspace/CLAUDE.md`「完全獨立、不是bug」，但實際上`scripts/sync_xinfa_to_claude_global.sh`等腳本真的存在部分鏡像關係。寫了一封回信給opencode(`knowledges/2026-08-05_軍師給OpenCode的回信_環境檢查報告回饋.md`)，並把「斷言前先查證、落款前先確認自己是誰」新增為CORE_RULES.md的R20，確保opencode下次開工必讀時看得到。同時把報告建議落地：E12鐵律新增「設定檔打架」判斷項、E17收工流程補環境健檢動作。commit `85a9c0644`（workspace）。

### 2. 🔴🔴 Repo1(~/.openclaw)盤點時發現真安全漏洞：`credentials/`從沒被`.gitignore`保護
盤點134行untracked時發現整個repo從未設過`.gitignore`，而`credentials/`目錄裝著真實LINE/Telegram secret/token(權限600)，一旦有人`git add -A`就會永久寫進git歷史。已新增`.gitignore`排除`credentials/`+`node_modules/`+資料庫備份快照，並補commit兩個乾淨的遺留變更(jiaolian_thoughts語音辨識誠實回覆+舊版opencode報告改名收尾)。commit `6965a61e`+`cd174376`（外層master repo）。

### 3. 🎯 bigtree大樹小講：金門兩場資訊補齊+活動花絮輪播
教練口述補齊8/21西浦頭社區(金門縣金寧鄉西浦頭231號，座位80人)+8/22向陽吉第社區(金門縣金城鎮西海路三段86號，座位60人)，皆免費、歡迎邀請非社區住戶參加；8/21時間修正為19:30-21:30(原寫21:00結束)；隱藏已結束的7/18線上讀書會+7/22高雄場+7/29台南場(資料留在git歷史，教練說法「反正在歷史紀錄裡面都看得到」)；新增「近期活動花絮」輪播(近期場次後、學員見證前)，7/29 AI微論壇台南場24張真實現場照片(`photos-carousel-0729/`，跟「緣起」輪播用的舊版活動剪影`photos-carousel/`是完全不同的兩批照片，md5核對過)。GitHub commit `e198f6e`。

### 4. 🎯🎯🎯 結繩領導學官網大改版：新書發表→兩日工作坊銷售頁
教練提供官網重構指令書(`~/Downloads/結繩領導學_官網重構指令書.docx`)，依11區塊架構全面重寫`index.html`：Hero雙欄(左文案/右書封，沿用舊版浮動動畫)→六大痛點→書/一般課程/工作坊比較表→四大工具(沿用原書內容改寫成「團隊問題→工作坊操作」格式)→兩天四階段(看見/判斷/操作/帶走)→學員見證(含3支FB見證影片連結)→關於曜董(後移)→成交區(NT$10,000，台南8/19-20+台北11/25-26)→FAQ。**舊版首頁(新書發表+11場座談會歷史)完整封存於`archive/`，圖片一併保留，首頁下方留連結可查看，不遺失**。過程多輪教練回饋微調：表頭四連結(工作坊/課程方法/學員回饋/關於曜董)+置中「立即報名工作坊」CTA+右側浮動導覽(仿舊版4圓形按鈕)+手機版漢堡選單+成交區報名按鈕置中(桌面版曾因Hero改版誤傷全域`.cta-row`置中樣式，已修正用`.hero-grid .cta-row`單獨override)+品牌字級22px+補齊`og:`/`twitter:`標籤(乾淨世界頻道連結`https://www.ganjingworld.com/@RPL50`同時補進footer)。每一輪修改都本機驗證(用瀏覽器互動測試按鈕/漢堡選單/RWD斷點)+開真實Chrome給教練看才進下一輪。

### 5. 🔴🔴🔴 教訓：Netlify自動部署型站台未查證，教練還沒說「推」就已上線
教練說「可以先推到GitHub，我讓團隊看完後再決定要不要推Netlify」，我直接執行`git push`——**沒有查證`jiesheng-leadership`是GitHub自動部署型**，想當然爾套用同場對話裡bigtree等手動上傳型站台的經驗。結果Netlify自動部署上線，教練親自發現「已經是新內容了」才揭穿，教練當場糾正：「這個就是你的問題，因為你沒有讀取開工檔案，你不曉得我每一次推播都會扣點數。」查證發現這個教訓其實**早就記錄在案**——`feedback_web_push_sop.md`判斷表格第一行代表站台就是`jiesheng-leadership`，`feedback_netlify_deploy_zip_api.md`也記著2026-06-09一模一樣的事故(當時是Sonnet 4.6犯的)。問題不是沒有經驗，是行動前沒有主動查記憶。已把這次(2026-08-05)重複犯錯的完整經過補進`feedback_netlify_deploy_zip_api.md`，更新description+MEMORY.md索引標題直接寫「動手前必查是哪型」。**教練裁示**：現狀不動(已上線的新版就保留)，之後所有修改一律只在GitHub上處理，不再碰Netlify。commit `7d8dbb5`(改版)+og標籤修正待下次一併commit。

## 📋 下一場直接開工任務
- 結繩領導學og標籤修正已收工時補commit `8acfa56`
- **LINE快取後續**：教練問「快取多久會變」，WebSearch+DNS實測確認LINE無官方TTL、無除錯工具，`?v=`參數是唯一可靠解法；教練回報「快取已更新」時軍師一度誤判成jiesheng-leadership(45分鐘)，經教練澄清其實是指`ai-talk-tw.netlify.app`(約10-11小時)，已更正記憶`reference_line_share_preview_cache_bust.md`。教訓：教練提一句「快取改了」不要直接套用當下正在處理的網址，先確認是哪一個
- Repo1剩餘94行untracked(5個agent目錄個人化設定檔全未進git)：涉及三機同步SOP架構決定，需要教練裁示方向，不要片面處理
- 接力棒瘦身：主檔現有v99/v98/v97三棒，超過E16規定的「最新1~2棒」，下場建議封存v97

## 🔑 本場關鍵檔案索引
- `~/.claude/projects/-Users-bymyway--openclaw/memory/feedback_netlify_deploy_zip_api.md`：新增2026-08-05二度誤推血淚段落+新鐵律
- `~/.openclaw/CORE_RULES.md`：新增R20(斷言前先查證)
- `~/.openclaw/執行細則.md`：E12新增設定檔打架判斷項、E17補環境健檢動作
- `~/.openclaw/.gitignore`：新增，排除credentials/+node_modules+db備份快照
- `~/.openclaw/knowledges/2026-08-05_軍師給OpenCode的回信_環境檢查報告回饋.md`：新增
- `github_repos/bigtree/index.html`：金門場資訊補齊+活動花絮輪播區塊+JS
- `github_repos/bigtree/photos-carousel-0729/`：新增，24張7/29真實照片
- `github_repos/jiesheng-leadership/index.html`：全面重寫(11區塊)
- `github_repos/jiesheng-leadership/archive/`：新增，舊版首頁+圖片完整封存
- commit(openclaw master)：`6965a61e`+`cd174376`
- commit(openclaw workspace)：`85a9c0644`
- commit(bigtree)：`e198f6e`
- commit(jiesheng-leadership)：`7d8dbb5`
