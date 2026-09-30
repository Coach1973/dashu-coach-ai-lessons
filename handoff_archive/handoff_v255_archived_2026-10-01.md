## 🔴 給跨對話框軍師讀的總結摘要（2026-09-30 19:00，Mac桌面版 Opus 5.5，新的一棒 v255）

**本場主軸：產業鏈SOP兩個AI同時出包的總檢討與機制修復；怡靜群組／帳號開通前置；LINE小龍蝦可出LK888圖；讀赫米斯週日~週二紀錄，準備 turnforyou 下一步。**

### 1. 產業鏈SOP出包總檢討（試金石案例93）
根因三個都是軍師的機制洞：①生圖腳本f-string寫法只在Python3.14測過，Hermes(3.11)一跑就崩→已改，三版本實測；②SOP寫「要比對905項BNI詞庫」但小龍蝦實際讀的技能檔沒寫→已補（`agents/main/agent/workshop-skills/industry-chain-prompt/SKILL.md`，此資料夾不進版控）；③開工六步看不到其他AI當天做的事→新增第5.5步`scripts/today_other_agents_digest.py`直讀小龍蝦inbound_echo＋Hermes state.db。另把接力棒v251~v252封存，開工注入不再被截斷。commit `8873d57d1` `13582eea5`。

### 2. 怡靜（陳怡靜，跨境電商）群組與帳號
- 「宜靜 AI 群」連結 https://t.me/+l7q1xK04SFE0MTRl ：龍蝦特助 @openclaw_macbook4_bot **要先被加進群**，機器人無法自己用連結入群；至今gateway log沒有任何該群訊息。等她在群裡@它講一句 → 從 `state/inbound_echo` 抓群ID＋她的Telegram ID → 在 openclaw.json bot_main.groups 加該群（requireMention視需要）＋toolsBySender。**權限原則：只開她要更新的指定資料庫（做成專用小工具），不開整台Mac。** 教練會再貼要開放哪些資料庫。
- 帳號：`namecard-db/venv/bin/python3 scripts/grant_partner_accounts.py --phone 09xxxxxxxx --name 陳怡靜` 一次開好 team.bymyway.com 總管理（涵蓋第一~第五分會）＋namecard.bymyway.com 已批准帳號，密碼皆88888。已在資料庫複本測過。**等教練給她手機號碼。**
- 出席紀錄：team01.bymyway.com（`~/github_repos/team01-guests`，port 5091）是第一分會邀約來賓儀錶板，有 guest_list 表但**沒有登入後台**；第二分會版本不存在。等教練的資料庫清單再做。
- VPS pairing碼QJJKXVY8查她ID被安全檢查擋（憑證資料夾），不用再試，等群裡講話即可。

### 3. 內外部資源＋觀眾席構想（軍師建議，待教練拍板）
- 內部＝大台南區現役BNI會員（權威來源：大台南南區94人資料）；外部＝非會員（mentor100講師、策展店家、前會員、來賓）。
- 建議做一份「人才庫」單一資料來源，觀眾席從它長出來，上面加「全部／內部／外部」切換（就是教練09-29提過的「內外專家選單」），不再把28人寫死在HTML裡。
- 專業欄位用905項BNI詞庫的名稱，同一份人才庫就能直接餵產業鏈圖（節點＝真的人）。
- 公開頁只放各人已公開的資料（照片、公司、專業），不放電話。94人以上要分組／可收合／可搜尋，不然頁面太長。

### 4. LINE小龍蝦出LK888圖（教練要求，只限教練本人帳號）
根因：LINE只收公開HTTPS網址的圖。已加 `event.bymyway.com/chain-img/`（檔名帶亂數）＋`generate_industry_chain.py --publish`；大台南小幫手新技能 `industry-chain-image`、main技能加 Branch D。第一次真實使用時要確認LINE上看得到圖。commit `676e96224`。

### 5. 權限與「上」
Claude Code 自動安全檢查會擋：AI自己改權限（Self-Modification）、讀憑證資料夾、把授權寫成常駐規則。教練親定：被擋時整理好問一句，教練回「上」＝當下授權；不准丟指令叫教練去終端機跑（記憶 feedback_dont_ask_obvious_yes_and_never_hand_commands_2026-09-30）。

### 📋 下一場開工先做
（目前沒有懸而未決的事）09-30 晚上教練交辦的都已上線，教練會接著「邊做邊改」。等教練提起時的現況：
- **turnforyou**（event.bymyway.com/curated/turnforyou/ ＝本機 `~/github_repos/turnforyou/`，無git，備份 index.html.bak18/.bak19、data.json.bak-20260930）：8席中第1凌榆舜、第5邱裕榮、第7顧瀚鈞 Jacky 已是真人；第2/3/4/6/8席仍是示範假資料。邱裕榮沒照片（放 `img/mentors/qiu-yurong.jpg` 就自動顯示，現為空椅設計）。Act04標題已改「你的想法，就是你的作品。／你想用什麼形式來展現，是你的自由。」。觀眾席27位（凌榆舜升上導師席已移除）。教練說「有些字要改」尚未指明。改席位要同時改 data.json 和 index.html 內嵌 `window.__C__` 的 seats（網頁先用內嵌、再被 data.json 覆蓋），空照片會自動退回 img/mentors/0N.jpg 示範照。
- **jacky-brand**（event.bymyway.com/curated/jacky-brand/ ＝ `~/github_repos/jacky-brand`，無git，備份 index.html.bak-20260930）：已改以台灣為重心。教練說 FB 有一張適合當封面的照片，AI 沒找到單人照，等教練指出。
- **教練新方向（09-30）**：團隊重心在台灣、不傾向與中國大陸合作、一律繁體（圖片裡的字也算）→記憶 feedback_taiwan_focus_no_china_emphasis_2026-09-30。
- **陳怡靜**：team.bymyway.com 總管理帳號已開（0919013658／88888，實測登入看得到五分會）；名片系統教練已開。「宜靜 AI 群」龍蝦特助要先入群、她在群裡@講一句才抓得到群ID與她的ID；要開放哪些資料庫等教練給清單（只開指定資料庫的專用小工具，不開整台Mac）。
- **內外部資源＋觀眾席構想**：見上方第3點建議，等教練拍板。

### 🔑 本場commit
`2a38af044` `8873d57d1` `13582eea5` `676e96224` `39bebb91b` `15effa746` `e562a67ec` `8937f050e` `539652c7c` `0fdab1741`，本次總結commit另計。

