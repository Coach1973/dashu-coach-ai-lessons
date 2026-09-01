> 📦 v161完整內容封存於此（Mac終端機，道德規範中英對照+分會精神複製8分會+真鑫/真鑽/真貴戰情儀表板從零建置+2次試金石教訓）

# 軍師接力棒 · 2026-09-01 v161（Mac終端機 Sonnet 5，道德規範中英對照完成+分會精神複製8分會+真鑫/真鑽/真貴戰情儀表板從零建置+2次真金石教訓）

> 建立時間：2026-09-01 05:22 ~ 08:10（台灣時間，接續v160，教練整晚未睡，本場密度極高）
> 上一棒：v160（真誠分會「分會精神」配色多輪迭代收斂+下一場交辦：道德規範中英對照+全分會套用格式）
> 本棒主軸：**v160交辦的兩項任務都完成；教練提出全新的「BNI大台南南區各分會來賓戰情儀表板」需求，過程中因軍師沒查證URL方向搞錯浪費教練30分鐘（試金石案例68），修正後查到官方會員名單，跟Hermes密集分工完成真鑫/真鑽/真貴三個分會的戰情儀表板+來賓公開查詢系統，過程再爆一次品質事故（試金石案例69）並修復。**

## 🎯 本場戰果

### 1. 道德規範中英對照（v160任務1）已完成
查證兩個官方BNI分會網站（bniarizonasouth.com、bnirsb.com）逐字比對，確認BNI Code of Ethics官方英文6條，補進`bni-chapters`真誠分會`chapter.html`的`ethics-list`區塊+`base.html`新增對應CSS樣式，commit`4bcc161`，curl驗證正式站已生效。

### 2. 分會精神複製到其他8個分會（v160任務2）已完成
教練確認「全部都一樣，不用客製化」，判斷這是純SQL資料複製、可交給Hermes，發信委派（commit`52b42fc40`），Hermes直接動手完成（軍師另一場對話框接手，非Hermes本人），81筆資料（9分會×9條）全部到位，curl驗證9個分會頁面皆顯示「分會精神」。過程中發現並回信Hermes的身份混淆問題（第3次停擺），已把「身份確認」+「做完必回報」兩條硬規則寫進`~/.hermes/workspace/AGENTS.md`熱啟動流程，commit(hermes-h-workspace)`b36a140`。

### 3. 【試金石案例68】BNI大台南南區各分會「來賓戰情儀表板」需求，軍師沒查證URL方向搞錯，浪費教練30分鐘
教練貼`sincere.bymyway.com`要求「照抄」，軍師沒打開查看，憑印象聯想成`bni-chapters`系統，設計了一套錯誤的「後台CRUD+公開表單」方案，被教練連續糾正3次才查證發現這是完全獨立的repo`~/github_repos/zhencheng-guests`（真誠分會邀約來賓戰情儀表板，零登入、會員自己在網頁填121/咖啡會議）。教練當場要求寫入試金石，已記錄案例68+記憶`feedback_url_given_open_it_dont_guess_2026-09-01`。

### 4. 真鑫/真鑽/真貴三分會戰情儀表板從零建置，軍師+Hermes分工完成
- **真鑫**（`~/github_repos/zhenxin-guests`）：軍師先建骨架（commit`0e1d7ec`，複製`zhencheng-guests`+新增`early_bird`早鳥欄位），Hermes接手填真實資料。過程中會員名單經歷28人（Hermes從21場例會推算）→23人（軍師查`claude-brain/data/bni_region_members_contact_2026-08-18.csv`找到BNI Connect官方在籍名單，教練確認28人是「歷史上曾加入又離會的」，只做在籍23人），最終commit`4be45ad`定案。**已正式部署上線**：`https://zhenxin.bymyway.com/`（新建Cloudflare Tunnel`zhenxin-app`+DNS+兩支launchd plist，port 5092）。
- **【試金石案例69】品質事故**：正式站被發現殘留真誠分會的假來賓姓名（李美花/張育慈），根因是軍師早前為了滿足Chrome查證鎖用真誠假資料測試時，`app.py`動態建立、不在`schema.sql`裡的`guest_list`表沒被後續seed腳本清空。已從21場彙整表重新解析102筆真鑫真實來賓明細，寫入`GUEST_LIST_DATA`並補進`seed.py`確保可重複執行，commit`9b36d4a`。後續教練再指出4筆「（無，會員自行出席）」解析錯誤的假資料+文案「教練/軍師提供更新」要改「由教練提供更新」（其他分會的人不知道軍師是誰），已修復commit`2387675`。記憶`feedback_verify_all_tables_not_just_main_schema_2026-09-01`。
- **真鑽**（Hermes建置，`Coach1973/zhenzuan-guests`，commit`aaa268c`）：49人官方名單（軍師從同一份CSV查到），骨架完成，尚未部署正式網址。
- **真貴**（Hermes建置，`Coach1973/zhengui-guests`，commit`48f47a5`）：籌備會，目前無會員名單，骨架先建好，尚未部署正式網址。

### 5. BNI大台南南區「來賓公開查詢」系統上線（原v160之前已規劃，本場由Hermes完成）
`https://coach1973.github.io/BNI-Training/guests.html`，commit(BNI-Training)`9cfebbb`。3718筆BNI Connect官方來賓報表，318個(邀請人,分會)組合，門檻比照培訓總覽既有查詢區塊（固定按鈕+自訂輸入任意月數），隱私原則對齊（只顯示邀請人/分會/日期，不顯示來賓聯絡資訊）。過程中軍師一度誤設計成13個固定門檻按鈕，教練更正「比照培訓查詢方式，重點是自訂輸入」，已即時攔截修正（commit`bd028f283`），Hermes還沒動工前就更正完成。

## ⚠️ 下一場開工先做
1. **讀Hermes完成信**（教練本場結尾特別交代）：真鑫/真鑽/真貴+來宾查詢系統都已回報完成，但可能還有後續進度或問題，開工先查`cross-agent/inbox/mac/`。
2. **真鑽、真貴尚未部署正式網址**：Hermes只完成GitHub repo+本機測試，DNS/Tunnel/launchd這塊軍師還沒做（真鑫已完成部署當範本，`zhenxin.bymyway.com`），下一場比照同樣模式做`zhenzuan.bymyway.com`+`zhengui.bymyway.com`（或教練指定的網址）。
3. **真鑫分組資料**：教練說「真鑫是有分小組的，只是我不知道它是怎麼分的」，之後教練會提供，目前`TEAMS`留空。
4. **真鑽/真貴的來賓/121/咖啡歷史資料**：目前完全空白，等教練提供。
5. v151之前已知舊待辦（FB粉專商家驗證、`/bni-credit`補公司欄位、「釋放記憶體」白名單範圍、12月主題培訓內容）本場均未觸及，繼續掛著。
6. **試金石案例68+69都是同一個「來賓戰情儀表板」任務裡發生的**，下次類似「教練貼URL要求照抄」的任務，開頭第一步就是打開查看，不要再犯。

## 🔑 本場commit
`bni-chapters`：`4bcc161`（道德規範中英對照）。`workspace`：`52b42fc40`+多封cross-agent委派信（分會精神複製委派）、`feec99498`（試金石案例68）、`8a370ea91`等多封信（真鑫/真鑽/真貴+來賓查詢任務委派與更正）、`f5a1e3b26`等信件歸檔commit。`hermes-h-workspace`：`b36a140`（身份確認規則）。`zhenxin-guests`：`0e1d7ec`→`028ef0a`→`4be45ad`（會員名單迭代）→`9b36d4a`（guest_list品質修復）→`2387675`（自行出席假資料+文案修正）。`zhenzuan-guests`：`aaa268c`（Hermes建置）。`zhengui-guests`：`48f47a5`（Hermes建置）。`BNI-Training`：`9cfebbb`（來賓公開查詢guests.html）。部署基礎設施：`~/.cloudflared/zhenxin-config.yml`+`com.coach.zhenxin-webapp/tunnel.plist`（zhenxin.bymyway.com已上線）。

---

