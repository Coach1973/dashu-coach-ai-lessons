# 小龍蝦常用流程（需要時才讀）

> 2026-10-21 從 SOUL.md 原樣搬來，內容未修改。小龍蝦開機每個檔最多讀 2 萬字，SOUL.md 已達 97%，所以把長的操作步驟移到這裡；SOUL.md 原位置留一行指向。

### 🎯 策展SOP：教練丟一個店家網站zip給你，直接上傳指定網址，不用自己動手建站（2026-09-06凌晨04:00簡化，取代舊版手動七步驟）

> 舊規則（教練實測`ls -la`後確認你有終端機能力→要你自己手動建GitHub repo跑七步驟）已作廢。
> 原因：手動七步驟存在的唯一理由是「上傳網址原本不會判斷店家是否已有暫代頁，會誤建重複網站」，
> 這個判斷邏輯2026-09-06凌晨已經寫進背景腳本自動處理，上傳網址現在對「全新店家」跟
> 「已有暫代頁的店家」兩種情況都安全。手動流程反而更慢、更耗你的資源，改用上傳網址即可。

教練傳一個打包好的網站zip/tar.gz（TAVA AI、Tooo.ai、Lovart.ai等工具做的店家/夥伴網站）給你，
要求上架時，**只做這一件事，不要自己建GitHub repo、不要自己SCP、不要問要不要轉交軍師**：

0. **🔴 先分清楚類型（2026-09-24起上傳網址強制要填 kind，沒填會被擋下）**：店家/夥伴網站→`kind=shop`；教練自己的創作（漫畫/故事/作品集/送件包，教練說「大樹作品」「大樹創作」「大樹創作SOP」）→`kind=creation`，系統會原封不動上架、自動放進大樹作品一覽「最新作品」第一筆、通知群組，**不用再照舊版手動七步驟改coach888網頁**。分不出來就問教練「這是店家網站，還是您的大樹作品？」，不要猜。
1. 先問清楚：檔案在哪個路徑？（不確定就問，不要瞎猜）。檔案超過20MB時Telegram收不到，請教練直接用手機開「大樹常用」裡的作品上傳頁自己傳，一樣選類型即可。
2. **再問清楚：這個網站要用什麼短網址？**（例如「百聖廣告設計工程有限公司」→`bai-sheng`，只能小寫英文/數字/短橫線）——2026-09-06教練拍板：源頭解決網址過長問題，這一步不能省略、不能自己亂猜拼音，一定要教練親口確認，因為上傳後系統不會再自動幫忙改名。
2.5 **店家／合作夥伴網站（kind=shop）不要問「要不要同時放進大樹作品」**（2026-10-13教練罵「上架就上架，別再問來問去」，推翻10/10的「一定要問」）——預設就是放（不帶 also_works，伺服器自動當 1）；只有教練自己明講「不要放大樹作品」才加`-F also_works=0`。kind 照教練說的 SOP 名稱選（說策展＝shop、說大樹作品／大樹創作＝creation），不看網站內容猜、不列 A/B/C/D 選項。
3. 執行：
   ```bash
   curl -s -F "kind=<shop或creation>" [-F "also_works=<1或0，只有shop要>"] -F "package=@<確認到的真實檔案路徑>" -F "custom_slug=<教練確認的短網址>" \
     "https://event.bymyway.com/curation/upload?key=VoARDsbU85r2fhzJPCwhLv-xVm6pHTxZ" \
     -o /tmp/curation_upload_resp.html -w "HTTP %{http_code}\n"
   grep -o "已收到「[^」]*」" /tmp/curation_upload_resp.html
   ```
4. 看到HTTP 200+「已收到」字樣，就跟教練回報：「已上傳，系統正在背景自動處理，完成後教練會收到Telegram通知附上網址，通常10~20秒內完成。」——這句話講完可以先告一段落，不用死等。
5. 如果HTTP狀態碼不是200或抓不到「已收到」，把完整錯誤訊息告訴教練，不要自己瞎猜原因——最常見是短網址格式不對或已被其他店家用過。
6. **🔴🔴 2026-09-26新增鐵律：需要立刻知道結果時（教練在等、或想自己確認），禁止用「等N秒＋猜`/curated/<你填的slug>/`網址」的方式驗證，一律跑這支工具**（2026-09-26鑫瀚昌旅行社案例：curl 200後查`/curated/hsinhan/`猜了4次都404，寫信給軍師才知道其實6秒就處理完成，只是這家店命中既有暫代頁、`custom_slug`被系統略過，真正網址是`shops.bymyway.com/xin-han-chang-lv-xing-she/`——網址本來就不該用猜的）：
   ```bash
   python3 ~/.openclaw/workspace/scripts/curation_check_result.py "<你送出的zip檔名關鍵字或custom_slug>"
   ```
   回傳JSON會直接告訴你：處理完了沒(`pending`)、成功(`success_shop_new`/`overwritten_existing`/`success_creation`)還是失敗(`failed`)、**真正的最終網址**(`actual_url`，2026-09-27起全部店家網址統一是`event.bymyway.com/curated/<slug>/`；看到`overwritten_existing`只代表這家店原本有暫代頁、已覆蓋成完整網站，舊的`shops.bymyway.com`網址會自動轉過來)、這個網址現在活著沒(`live_check_http_status`)。**這支工具查得到結果，就不用再寫信問軍師**；查不到（`not_found`）才需要考慮寫信求助。
7. 完整技術細節見`claude-brain/reference_curation_sop_2026-09-06.md`（跟軍師共用同一份workspace repo，讀得到）

### 🎯 報名頁上架SOP：一頁式報名網頁，接上event.bymyway.com資料庫+Telegram通知（2026-09-17教練拍板）

跟策展SOP不同，這種頁面有報名表單要即時寫入資料庫，**五步驟**：
1. 確認教練提供的zip/tar.gz檔案路徑
2. 建GitHub repo(`coach1973/<slug>`) + push + 開Pages（跟策展SOP第三步同樣手法，純靜態站）
3. 報名表單JS改呼叫共用端點`https://event.bymyway.com/api/register`（**不要新建`/api/<name>/join`專屬端點**，這支已經是通用設計）：
   ```js
   fetch('https://event.bymyway.com/api/register', {
     method: 'POST', headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({slug, name, phone, company, email, note, source})
   });
   ```
4. 用curl在`event.bymyway.com/admin/sessions/save`建立對應的場次代碼(slug必須跟第3步JS裡的完全一致)：
   ```bash
   curl -s -c /tmp/cookie.txt -d "username=0901056777" -d "password=88888" \
     https://event.bymyway.com/admin/login -o /dev/null
   curl -s -b /tmp/cookie.txt -X POST https://event.bymyway.com/admin/sessions/save \
     -d "slug=<場次代碼>" -d "name=<活動名稱>" -d "event_date=YYYY-MM-DD" -d "status=active"
   ```
   **🔴如果這場活動屬於大樹小講(bigtree)系列**，這步要多帶一個欄位：`-d "event_url=https://coach1973.github.io/<slug>/"`——`bigtree_publish.py`會自動讀這欄，官網對應場次卡片就會出現「我要看活動網頁」按鈕連過去，不用另外改bigtree原始碼。非bigtree的一次性活動不需要這步。
5. 送一筆真實測試報名，確認Telegram「活動報名即時通知」群組有收到+`event.db`的`signups`表有新紀錄，驗證完清掉測試資料。**不用另外通知教練**，Telegram已經自動發了。

完整技術細節+特別注意事項見`claude-brain/reference_event_registration_page_sop_2026-09-17.md`（跟軍師共用同一份workspace repo，讀得到）

### 🎯 一鍵發布：教練貼event.bymyway.com網址+說「請發布/請更新」，直接觸發不用等軍師（2026-09-11教練交辦）

適用範圍：`event.bymyway.com/<名稱>/`這類網站（大樹小講/AI微論壇/DIY系列/海餅乾20週年等，共21個），
內容改在GitHub（教練/軍師/聯想/ACER任何一台推送commit都算），但Mac讀的是本機clone，
沒人手動`git pull`就不會反映最新內容。跟大台南商圈計畫(`tainan-shangquan`)不是同一種架構——
那個是內容直接寫進資料庫，送出當下就生效，完全不需要這個步驟。

教練貼一個`event.bymyway.com/<名稱>/`網址，說「請發布」「請更新」時，**只做這一件事**：

1. 從網址抓出`<名稱>`那一段（例如`event.bymyway.com/ai-forum/`→`ai-forum`）
2. 執行：
   ```bash
   curl -s "https://event.bymyway.com/api/site-update/<名稱>?key=p35JuRW2fbn776sr2FRkZ8u2pbGTNev3"
   ```
3. 回應`"ok": true`→跟教練回報：「已更新，最新版本commit XXXXXXX」（把回應裡的`commit`欄位貼出來）
4. 回應`"ok": false, "error": "unknown repo"`→回應裡的`known_repos`就是目前支援的完整清單，把清單念給教練聽，請他確認是不是打錯名稱
5. 這支端點只做`git pull`，不會動資料庫、不會刪除任何東西，可以放心觸發，不用問「確定嗎」

**教練說「這個網址太長/改短一點」時**：這也是你能直接做的事，不用轉交軍師。完整三步驟（①用帳密`0901056777`/`88888`登入取得session cookie，POST到`/curation/admin/delete/<舊slug>`下架 ②用新短網址重新curl上傳同一份zip ③若這家店之前發過FB貼文，查`distill/curation_process.log`找post_id，用Graph API編輯貼文文字換成新網址）都寫在`claude-brain/reference_curation_sop_2026-09-06.md`「改短網址完整SOP」那節，照著做即可。

### 🎨 產業鍊SOP：教練說「[專業別/店家]的產業鍊SOP」時，自己組prompt生一張產業服務鏈圖回傳（2026-09-16教練交辦，BNI組隊計畫用）

觸發句型：句子裡出現「XX的產業鍊SOP」或「XX的產業鏈SOP」（XX是任意專業別/店家名稱，例如「培訓講師的產業鍊SOP」「王聖凱的產業鍊SOP」）。

看到就**只做這一件事**，不用問要不要做：

1. 自己動腦組一個完整的圖片生成prompt，格式固定套這個模板：
   ```
   我需要做一張產業服務鏈，要用手繪可愛風格做出來。中心是「<專業別/店家名稱>」的插畫。
   標題：<你自己想一個貼切的四到八字標題>。
   為<這個專業別/店家的目標客群>提供從<第一項服務>到<最後一項服務>的一條龍支援。
   周邊環繞以下專業類別節點，每個節點配精緻手繪icon：<你自己列出15~20個跟這個專業別異業合作最相關的服務類別，用頓號分隔>。
   所有文字必須完全正確、清晰可讀，不能有亂碼或錯字。
   ```
   異業服務類別要挑真的跟這個專業別會合作往來的（例如培訓講師會搭配：簡報設計、教材製作、線上課程平台、攝影棚、活動主持人、會計記帳、法律顧問等），不要憑空亂湊。
2. 執行：
   ```bash
   python3 ~/.openclaw/workspace/scripts/generate_industry_chain.py \
     --prompt "<你組好的完整prompt>" \
     --telegram-chat-id 6124913915 \
     --caption "<專業別/店家名稱>的產業鍊圖"
   ```
3. 這支腳本呼叫的是教練已付費的lk888 API（GPT Image 2模型），生成通常要30~90秒，先跟教練說「生成中，稍等一下」再等結果，不要催促也不要重複呼叫。
4. 看到終端機印出「已推送Telegram」就結束，圖片會自動送到教練Telegram，**不用你再手動描述圖片內容**。
5. **已知特性，不要為了追求完美重複呼叫**：GPT Image 2大約有5~10%機率會把某個周邊節點文字生錯（重複或錯字），教練已經表態「不求精準及完美，因為額度有限」——生一次就好，除非教練自己說「重生一張」，否則不要自己判斷「畫得不夠好」就自動重跑，每次呼叫都會扣教練的付費額度。
6. 如果指令回傳「錯誤：...」，把完整錯誤訊息告訴教練，不要自己瞎猜原因。

不在這張表上的事情，照舊寫一般信件（不加 DISPATCH），系統會通知教練「有信要人看」，
不會被吃掉。完整協議與安全設計見 `cross-agent/README.md`。

### 🎯 真鑫/真鑽/真貴分會戰情儀表板：教練丟最新一週的來賓/1對1/咖啡會議數據給你，直接寫進去，不用等軍師（2026-09-07教練交辦）

教練把某分會某一週的次數數據（來賓/1對1/咖啡會議）告訴你時，直接照`claude-brain/reference_bni_guest_dashboard_weekly_update_sop_2026-09-07.md`的步驟動手：
1. 先查清楚是哪個分會（真鑫`zhenxin-guests`／真鑽`zhenzuan-guests`／真貴`zhengui-guests`，DB路徑都在`~/github_repos/<repo>/`）
2. 1對1／咖啡會議：curl POST該分會網址的`/api/update_metric`（公開API，帶`member_id`/`week_date`/`metric`/`value`即可，不用登入）
3. 來賓數：直接`sqlite3`寫`weekly_data`表的`guests`欄位（這個沒有公開API，因為來賓數來自官方報表非會員自填，用INSERT...ON CONFLICT UPDATE）
4. 新的一週如果`weeks`表還沒有這筆，要先INSERT一筆`is_active=1`的週次記錄才能填數據
5. 改完不用重啟服務，Flask每次都即時查DB；用curl該分會首頁確認數字真的顯示出來再回報教練
完整SQL/curl指令範例都在上面那份SOP文件裡，照著抄就好。

