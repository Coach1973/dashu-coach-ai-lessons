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
