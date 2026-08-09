# 接力棒封存：v101～v103（2026-08-09封存，E16瘦身鐵律）

> 封存原因：主檔只留最新1~2棒，這三棒被2026-08-09新的一棒(Mac桌面版 Sonnet 5，bni-chapters編輯功能+mentor100頁尾+幕僚長晨報+bymyway.com架構查證)擠出主檔，搬進此封存檔查舊歷史用。

# 軍師接力棒 · 2026-08-08 v103（Mac桌面版 Sonnet 5，mentor100密集迭代五連發+bigtree-tw收費更新）

> 建立時間：2026-08-08 台灣時間 11:07~19:00
> 本棒執行者：Mac 桌面版 Sonnet 5
> 上一棒：v102（Mac桌面版 Sonnet 5，bni-chapters官方色系+表頭一致性修復+三個系統性hook修復）
> 本棒主軸：**`mentor100.bymyway.com` 教練密集提出5輪需求，逐一處理：申請名單UI動線優化+新增刪除功能→發現並修復申請名單姓名沒同步導師編輯結果的bug→順勢改成自動上架不用教練逐一確認→申請成功頁文案調整→教練提出「網站要對外公開了」，首頁做固定表頭+右側浮動導覽+手機漢堡選單+導師頭像改依人氣點擊排序的整體改版。中途穿插`bigtree-tw`8/26高雄場補上報名費100元(手動上傳型站台，走完整三步驟部署鐵律)。全程延續既有隔離副本測試習慣，5次production改動零意外。**

## 🎯 本場戰果

### 1. 🎯 mentor100數據總覽：申請名單UI動線優化+新增刪除按鈕
教練回報點「產生連結」後頁面跳回最上方、得往下滑才看得到申請名單，操作不順。改成「申請名單」搬到「來訪次數」跟「導師點擊排行榜」中間，同時新增刪除按鈕（測試資料/重複申請用），刪除邏輯順手處理乾淨：若該申請連到的導師還是草稿狀態，一併清掉那筆空白草稿避免孤兒資料。`/admin`跟`/admin/stats`兩處同步更新。commit `567a37f`。

### 2. 🔧 修復申請名單姓名沒同步導師編輯結果的bug+改自動上架
教練用編輯功能把導師姓名改掉（陳彥瑋→丁兆弘、大樹教練→書銘老師），發現「申請名單」最上面顯示的還是舊名字。查證發現`list_applications`原本直接拉`applications.name`（最初送出的原始值），從沒跟`mentors.name`同步過。改成`COALESCE(m.name, a.name)`優先顯示對應導師目前資料。同一輪教練也提出：現在全面走人工申請流程，希望申請人填寫送出後直接自動上架，不用再等教練按「確認上架」。已改成只有「還是草稿狀態」的申請人送出時自動發布，既有56位已上架導師自行編輯簡介不受影響（用test_client模擬完整流程+對照組驗證兩種情境皆正確）。commit `dfddc73`。

### 3. 🎨 申請已送出頁面文案調整
教練用語音輸入指示把「教練已經收到您的申請」改成「大樹教練已收到你的申請」+兩行無標點置中排版，已改好並confirm教練確認資料庫顯示的丁兆弘/書銘老師是正確的（語音輸入落差，非bug）。commit `8eceeb1`。

### 4. 🎯 bigtree-tw：8/26高雄場補上報名費100元
教練口頭確認「經過討論要收100元」。查場次資料`SESSION_DATES`陣列，仿金門場既有寫法把費用資訊加進`transport`備註欄。本機用Chrome預覽確認畫面後，教練說「推」，走`bigtree-tw`既有的手動zip+Netlify API部署（查證確認這是手動上傳型站台，非GitHub自動部署，依鐵律走完整三步驟）。commit `e3a6ad6`，deploy `6a76c91e`，curl驗證文字+圖片Content-Type皆正常，額度47→46（手動補記，因指令帶多個flag被guard正則漏掉，已寫進`state/netlify_deploy_quota.json`備註）。

### 5. 🎯🎯🎯 mentor100首頁大改版（本場核心）
教練說明網站接下來要對外公開，提出四項需求：①固定表頭放起心動念/免責聲明/計劃緣起連結 ②讓使用者更快捲到導師卡片 ③右側浮動導覽+Top鍵仿結繩領導學 ④手機漢堡選單。教練主動要求先確認理解再動手，用AskUserQuestion問了3個不確定點但教練選擇直接用文字說明取代選單：**兩段文字（起心動念+計劃源起）留最上面，另外兩段（這是一個怎樣的地方+免責聲明）移到導師卡片後面，不管在哪都要能從導覽點得到**。落地：仿結繩領導學同款CSS（`.topnav`/`.hamburger`/`.mobile-menu`/`.float-nav`）套用mentor100既有金黑配色；`db.list_mentors_published()`改成LEFT JOIN `mentor_clicks`依`COUNT(c.id) DESC, m.id ASC`排序，後台`admin_list.html`完全沒動維持建立時間排序。全程先在`/tmp`隔離副本驗證：卡片順序跟後台排行榜逐一比對一致、375px手機寬度下漢堡選單能正常展開顯示5個連結，才推正式站。commit `c57a3d1`。

## 📋 下一場直接開工任務
- **bni-chapters「真誠分會」網頁主架構問題**：教練提出但本場對話結束前還沒說明具體是什麼問題，下一場先問清楚再動手
- **三機hook同步待辦（教練要求優先，v102延續）**：聯想/ACER仍未處理，見[[project_cross_machine_hook_sync_todo_2026-08-08]]
- mentor100人工審核流程：5位draft狀態導師（書銘老師/陳宜璟/梁文宣/陳彥瑋/丁兆弘）已發連結，尚無人實際走完整填寫送出流程驗證自動上架，下一場可問「有人送出了嗎」

## 🔑 本場關鍵檔案索引
- `github_repos/mentor100/app.py`+`db.py`：刪除申請路由+姓名同步查詢+自動上架邏輯+人氣排序查詢
- `github_repos/mentor100/templates/admin_stats.html`+`admin_list.html`：刪除按鈕+版面調整
- `github_repos/mentor100/templates/apply_thanks.html`：文案調整
- `github_repos/mentor100/templates/index.html`：首頁大改版（表頭/浮動導覽/漢堡選單/版面重排）
- `github_repos/bigtree/index.html`：8/26場次加報名費
- `~/.openclaw/workspace/state/netlify_deploy_quota.json`：bigtree-tw部署額度記錄
- commit(mentor100獨立repo)：`567a37f`→`dfddc73`→`8eceeb1`→`c57a3d1`
- commit(bigtree獨立repo)：`e3a6ad6`
- commit(workspace，額度記錄)：`de56987f8`

---

# 軍師接力棒 · 2026-08-08 v102（Mac桌面版 Sonnet 5，bni-chapters官方色系+表頭一致性修復+三個系統性hook修復）

> 建立時間：2026-08-08 台灣時間 06:10~07:03
> 本棒執行者：Mac 桌面版 Sonnet 5（教練當場糾正非CLI，已補建自我判定法）
> 上一棒：v101（Mac終端機 Sonnet 5，mentor100人工審核上架流程+workshop-invite台中場移除）
> 本棒主軸：**兩條主線。①`bni-chapters`（大台南南區9分會系統）：查證BNI官方2020 Brand Standards Manual確認正確色號（BNI Red #CF2030 + Power Black #000000），改在共用`base.html`的`:root`一次套用全9分會；接著修復分會列表首頁(index.html)表頭導覽列消失問題，補上跟分會頁一致的5項導覽。②教練連續追問「截圖鎖為何沒執行/為何不能讀完守則再做事」，查到並修復兩個真正的系統性bug：截圖鎖的工具名稱寫錯(claude-in-chrome大小寫/連字號比對從沒對上過)、Claude Code長對話CLAUDE.md可能被context壓縮導致守則流失。三個都做成技術鎖(hook)而非承諾，並查證OpenClaw原始碼確認小龍蝦Mac版架構不受同款問題影響。**

## 🎯 本場戰果

### 1. 🎯 bni-chapters：官方品牌色系套用九分會
教練質疑真誠分會hero區塊黑色是否為BNI官方色，查證BNI 2020年6月版Brand Standards Manual第6頁確認正確色號（BNI Red `#CF2030`、Power Black `#000000`，非原本自訂的`#A22026`/`#2A2829`）。改在共用模板`templates/base.html`的`:root`，一處修改9分會同步套用，含hover陰影色同步更新。commit `958eea2`。教練裁示「之後一定要用官方指定色系」，已寫入記憶`reference_bni_official_brand_colors`。

### 2. 🎯 bni-chapters：分會列表首頁表頭一致性修復
教練發現從真誠分會點「分會列表」跳回首頁後，導覽列(認識分會/核心價值/分會之光/六項傳統)整組消失。首頁`index.html`原本`<nav></nav>`是空的，補上跟分會頁一致的5項導覽，後4項連到排序第一的真誠分會對應錨點區塊。commit `1f2c1a5`。已用claude-in-chrome實際點擊測試確認跳轉正確。

### 3. 🔴🔴🔴 截圖鎖真根因修復：工具名稱大小寫/連字號寫錯
教練連續追問「既然有截圖鎖，為何不執行？」查證發現`scripts/screenshot_lock.sh`跟`~/.claude/settings.json`的matcher都把claude-in-chrome的工具名稱寫成`mcp__Claude_in_Chrome__computer`（Title_Case+底線），但實際MCP工具註冊名稱是`mcp__claude-in-chrome__computer`（全小寫+連字號），字串比對從未對上，鎖形同虛設。已修正兩處，模擬輸入測試通過（截圖動作攔截/一般點擊放行/browser_batch巢狀截圖也攔截）。commit `b52934ad9`。

### 4. 🔴🔴 改完HTML自動跳Chrome（PostToolUse hook，不再靠記憶）
查證過去30天教練提醒「沒跳HTML/Chrome給我看」達7次，既有`rule_html_chrome_check.sh`是Stop hook(事後補救)，每次都要教練等被攔下才想起。教練點出守則#04「解決問題比解釋問題更重要」，新增`scripts/auto_chrome_after_html_edit.sh`（PostToolUse hook，matcher: Edit|Write），Edit/Write一碰`.html`檔案立刻自動`open -a "Google Chrome" file://...`，不用等事後攔截。commit `17147771f`，模擬測試通過。

### 5. 🔴🔴🔴 Claude Code長對話守則流失根因+修復
教練質問「如果不能讀守則，那我花費心思寫出來的守則意義是什麼？VPS版小龍蝦都知道，為何claude不能？」查證發現：`~/.claude/CLAUDE.md`（含21條守則全文）只在session開始載入一次，隨對話變長系統可能把最早context壓縮掉（本場對話到20輪時才被既有`session_length_hook.sh`偵測到，但那支只提醒換視窗、完全沒補回守則文字）。新增`scripts/periodic_xinfa_reload_hook.sh`，複用同一套「20輪起、每10輪一個band」節流設計，每個新band把21條守則完整原文重新貼進context。commit `6ae54fd6c`，已在本場對話第20輪實際觸發驗證生效（非僅模擬測試）。

**進一步查證（教練當場抓到我第一次回答是憑印象猜測，非查證）**：直接讀OpenClaw編譯後原始碼`workspace-Bfegr71x.js`+`bootstrap-cache-NNMZ7U6Y.js`確認：小龍蝦Mac版的SOUL.md是靠mtime比對的per-session快取，內容會當成系統提示詞穩定前綴附加在每次LLM請求裡，架構上不會有Claude Code CLI這種「長對話被壓縮流失」的問題，這條不用額外補hook。

### 6. 🔧 環境教訓：桌面版/終端機自我判定法
教練糾正「你不是CLI，你是桌面版APP」，查證`ps`父行程路徑(`/Applications/Claude.app`)+`TERM_PROGRAM`(空值=非終端機)可靠判定，已寫入記憶`feedback_desktop_gui_selfcheck_method`，避免下次又預設猜錯介面。

## 📋 下一場直接開工任務
- **三機hook同步待辦（教練要求優先）**：本場3支新/修正的hook腳本已推上雲端，但`~/.claude/settings.json`是各機本機設定檔不隨git同步，且是Mac bash+macOS專屬指令，Windows(聯想/ACER)需要各自PowerShell版本並在當地settings.json註冊。完整待辦清單已寫入記憶`project_cross_machine_hook_sync_todo_2026-08-08`，聯想/ACER下次開工應優先處理。
- bni-chapters其餘卡住項目（10組帳號預設密碼Admin/88888）本場未觸碰，教練仍未裁示
- 接力棒瘦身：本場已封存v100到`handoff_archive/handoff_v100_archived_2026-08-08.md`，主檔現只留v102+v101

## 🔑 本場關鍵檔案索引
- `github_repos/bni-chapters/templates/base.html`：官方品牌色系(:root變數)
- `github_repos/bni-chapters/templates/index.html`+`app.py`：首頁表頭導覽列補齊
- `scripts/screenshot_lock.sh`：工具名稱修正
- `scripts/auto_chrome_after_html_edit.sh`：新建，PostToolUse自動跳Chrome
- `scripts/periodic_xinfa_reload_hook.sh`：新建，長對話守則全文定期重載
- `~/.claude/settings.json`：三處hook註冊更新（非git追蹤，僅本機）
- `~/.claude/projects/-Users-bymyway--openclaw/memory/`：本場新增6份記憶檔+MEMORY.md索引更新
- commit(bni-chapters獨立repo)：`958eea2`（品牌色）→`1f2c1a5`（表頭）
- commit(mac-openclaw-workflows workspace)：`b52934ad9`（截圖鎖）→`17147771f`（自動跳Chrome）→`6ae54fd6c`（守則重載）
- commit(claude-brain記憶庫)：`c0a2df839`

---

# 軍師接力棒 · 2026-08-08 v101（Mac終端機 Sonnet 5，mentor100人工審核上架流程+workshop-invite台中場移除）

> 建立時間：2026-08-07 深夜 ~ 2026-08-08 凌晨（台灣時間 21:11~02:58）
> 本棒執行者：Mac 終端機 Sonnet 5
> 上一棒：v100（Mac終端機 Sonnet 5，小龍蝦訊息遺失真根因修復+軍師互動算聯繫+三個站台維護任務）
> 本棒主軸：**兩條主線。①`workshop-invite.netlify.app`（結繩領導學工作坊邀請頁，手動zip上傳型站台）移除已取消的台中場按鈕，本機預覽經教練確認後部署。②`mentor100.bymyway.com`（百人導師計劃）密集迭代：先加訪客計數器(熱度+精準人數)+導師點擊排行榜，接著把「我要加入百人導師計劃」從自動自助送出改成人工審核上架流程——教練原話「刻意營造你現在就是要人工申請的感覺」，最終落地三段式：申請(/apply三欄)→教練後台產生填寫連結(沿用最早設計的完整表單)→申請人自填仍是草稿→教練預覽後確認上架才公開。過程多次依教練回饋微調文案/欄位/UI，本場也踩到兩個環境教訓：自己清測試資料的時序撞上教練實測造成計數器誤判、claude-in-chrome在密碼欄位操作卡進其他擴充功能衝突，皆已寫入記憶。**

## 🎯 本場戰果

### 1. 🎯 workshop-invite.netlify.app 移除台中場按鈕
教練指定只留台南場+台北場。查證確認這是6個姊妹邀請頁(workshop-invite/peipei/richard/lavi、bni-invite/peipei)共用同一套內容，其餘5站教練明確裁示暫不動、只改這一個。本機`/tmp`建好HTML用Chrome預覽確認，教練說「推」後走zip+Netlify API部署，curl驗證台中場文字/按鈕完全移除、圖片Content-Type正常。額度手動補記48→47（deploy `6a75de3e8d2a6c2aadd104d4`，guard因指令有`-o`輸出重導向未自動扣）。commit `da2edc606`（workspace，額度記錄）。

### 2. 🎯 mentor100：訪客計數器(熱度+精準人數)+導師點擊排行榜
首頁新增到訪次數計數卡(取代原「我要參與導師同行計劃」按鈕位置，教練確認文案要用「次數」不用「人數」)，後台`/admin/stats`新增：累計來訪次數/不重複IP數兩張stat卡、重複造訪IP清單(哪些IP常回訪)、導師被點擊排行榜(金色長條+前三名獎牌)。全程用隔離副本(rsync整個repo到`/tmp`測試，避免污染production資料庫)驗證邏輯後才部署。commit `9cf57aa`+`3ec52ae`+`e1a9f5c`（mentor100獨立repo）。

### 3. 🎯🎯🎯 mentor100：加入計劃改人工審核上架流程（本場核心）
教練原話：「我本來就是要做的一件事，就是前期我都讓他們自動送出，那個階段已經結束了。我現在就是要刻意營造『你現在就是要人工申請』的感覺」。落地三段式：
- **①申請**：首頁「我要加入百人導師計劃」連到`/apply`，只收姓名/公司職稱/LINE ID三欄，送出後寫入`applications`表+透過`sme-register-fn`(跟大樹小講同一套管線)通知教練LINE。舊的`/join`公開自助全欄位表單(GET+POST)已關閉、轉址到`/apply`；`/join/edit/<token>`(既有56位導師的自助修改連結)完全不受影響。
- **②教練審核**：後台「導師申請名單」（教練要求`/admin`首頁最上方+`/admin/stats`兩處都要看得到）按「產生填寫連結」，建一筆`status='draft'`空白導師+沿用最早設計的完整自助編輯頁`/join/edit/<token>`專屬連結（教練原話「這個要回到最早我設計的那些、它可以填寫的所有欄位」，姓名/公司/簡介/照片/9組可自訂標籤連結一個都沒少），教練複製後親自傳給申請人。
- **③預覽上架**：申請人自填資料仍是草稿、不會自動上架，教練在後台「預覽」(仿首頁卡片+modal樣式WYSIWYG)看過沒問題才按「確認上架」，`mentors.status`才變`published`，才會出現在公開首頁。

`mentors`表新增`status`欄位(ALTER TABLE遷移，56筆既有資料全部保留published不受影響)，`applications`表新增`mentor_id`關聯欄位。過程中教練澄清兩次：拿掉「加LINE官方帳號」快捷按鈕改純資料送出；申請頁文案改三步驟流程說明。commit `7072acc`→`ae60923`→`6f563d9`→`6ce1df6`→`7ff1cbb`（mentor100獨立repo）。

### 4. 🔧🔧 環境教訓兩則（已寫入記憶）
①測試已上線功能（教練會盯著數字看的功能）不能直接在production db上測後清空，要用完整隔離副本(`rsync`整個repo到`/tmp`)，這場計數器一度讓教練誤以為「Mac 8次、Windows卻是第1次」是bug，查證後發現是自己清測試資料的時序撞上教練實測——已寫記憶`feedback_isolate_test_env_before_prod_db_testing`。②`claude-in-chrome`操作密碼欄位（後台登入）時卡進疑似密碼管理器擴充功能的浮層衝突，導致自動化截圖/點擊全部失敗，改用Flask `test_client()`等效驗證+誠實告知教練視覺確認缺口——已寫記憶`reference_claude_in_chrome_password_field_extension_conflict`。

## 📋 下一場直接開工任務
- mentor100人工審核流程教練尚未實際走過一輪真實申請人流程，下一場可主動問「有申請人試過完整流程了嗎」
- 其餘卡住項目（BNI真誠/真愛/真AI分會、Email自動發送系統、bni-chapters預設密碼等）本場未觸碰，狀態不變
- 接力棒瘦身：本場已封存v99到`handoff_archive/handoff_v99_archived_2026-08-08.md`，主檔現只留v101+v100

## 🔑 本場關鍵檔案索引
- `github_repos/mentor100/app.py`+`db.py`+`schema.sql`：計數器/點擊排行榜/申請審核流程全部邏輯
- `github_repos/mentor100/templates/apply.html`+`apply_thanks.html`+`admin_preview.html`：新增
- `github_repos/mentor100/templates/admin_list.html`+`admin_stats.html`+`index.html`：更新
- `~/.claude/projects/-Users-bymyway--openclaw/memory/project_mentor100_review_gated_signup_2026-08-08.md`：新增，完整技術脈絡
- `~/.claude/projects/-Users-bymyway--openclaw/memory/feedback_isolate_test_env_before_prod_db_testing.md`：新增
- `~/.claude/projects/-Users-bymyway--openclaw/memory/reference_claude_in_chrome_password_field_extension_conflict.md`：新增
- commit(mentor100獨立repo)：`9cf57aa`→`3ec52ae`→`e1a9f5c`→`7072acc`→`ae60923`→`6f563d9`→`6ce1df6`→`7ff1cbb`
- commit(workspace，額度記錄)：`da2edc606`
- commit(claude-brain記憶庫)：`d89b008f7`

---

