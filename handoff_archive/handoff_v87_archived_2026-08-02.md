# 軍師接力棒 · 2026-07-29 v87（聯想Windows Sonnet 5，BNI大台南南區＋真誠分會網站版型規劃，教練交棒給Mac）

> 建立時間：2026-07-29（台灣時間）
> 本棒執行者：聯想Windows桌面版 Sonnet 5
> 上一棒：v86（Mac桌面版Sonnet5，AI微型論壇台南場正式登場：現場緊急支援+LINE綁定bug修復+活動轉型回顧頁）
> 本棒主軸：**開工六步驟後，教練交辦卡了多棒的「真誠/真愛/真實AI分會願景說明書」——這次終於給了具體參考：bnidahan.com.tw（教練心目中理想範例）+bni-tainan.com/Training-Program（區域參考頁），要求BNI標準色系。實際瀏覽兩站抓出真實CSS色碼後，產出真誠分會＋大台南南區兩份完整HTML版型草稿，教練用Comet看過確認「方向正確」。教練接著問要不要親自逐步交代細節，軍師表態自己先動手做，但教練提醒公開網路查得到的分會資料很少，上網查詢是浪費token，直接問比較快——已改口直接列5項關鍵事實請教練回覆。教練最後決定切換到Mac電腦接手，本棒任務是把目前進度完整交棒。**

## 🎯 本場戰果

### 1. 開工六步驟＋一個當場未解的小疑點
執行六步驟時查`state/recall_index.jsonl`發現：v85接力棒寫完(7/28 19:06)後教練同晚又開新對話(20:03-20:32)，已把AI微論壇60位報名者Email整理進Gmail草稿匣(BCC保護隱私)準備寄提醒信，教練最後一句是「一會兒我就來寄信了」。開工回報時主動提出詢問是否已送出，教練當下沒回答就轉向其他任務。**事後對照Mac的v86才確認：AI微論壇7/29台南場當天已經正式辦過(見v86完整戰果)，代表這封提醒信的時效已經過去，不再是急件，純粹是個可以順口收個尾的小疑點，不影響任何現況任務。**

### 2. 🎯🎯 BNI真誠分會＋大台南南區網站版型規劃（本場主軸）
教練給定兩個參考網址，先用Browser工具實際瀏覽並用`javascript_tool`抓取頁面真實computed style，取得BNI品牌色實測值：bnidahan.com.tw主色`rgb(162,32,38)`≈`#A22026`、bni-tainan.com主色`rgb(145,14,20)`≈`#910E14`，確認BNI標準色系是深酒紅色系，非憑印象猜測。

**版型設計邏輯**：
- **真誠分會**（單一分會品牌站，比照bnidahan.com.tw結構）：Header導覽(認識分會/特色團隊/會員名錄/分會之光/活動)→Hero+「預約參訪」CTA→參訪須知4卡(正式服裝/50張名片/20秒自介/早餐Buffet，文字沿用bnidahan原文，教練已表示部分數字要改但尚未給確切值)→核心價值(Givers Gain)→分會之光(示意數據待填)→Footer社群連結
- **大台南南區**（區域總站，比照bni-tainan.com/Training-Program結構）：Header導覽(認識BNI/轄下分會/培訓計畫/最新消息)→滿版酒紅色Hero→轄下分會卡片(真誠/真愛/真實AI，此區為延伸設計，原站沒有因為它是單分會頁)→培訓計畫卡片(MSP/成功藍圖/引薦/帶來賓)→最新消息列表→Footer

先用`mcp__visualize__show_widget`做過一版精簡wireframe給教練看方向，教練確認「方向正確」後，因教練說「你至少要跳HTML出來給我看吧」，改用這台機器既有SOP（`feedback_html_preview_chrome_only`：聯想這台Chrome會跳空白頁，改用Comet）——寫出兩份**完整靜態HTML**(非簡化widget版，含真實CSS排版/hover效果/Noto Sans TC字型)存到`D:\Users\Desktop\`，用`comet.exe`跳出兩個視窗給教練看，教練確認滿意。

**教練釐清協作模式**：教練問「你要自己先動手做，還是我一步一步跟你說？」，軍師表態自己先動手做（守則#12拒絕當資訊搬運工），原打算上網查真誠/真愛/真實AI分會有沒有公開資料可引用，**教練當場糾正**：「網路上可以公開查詢的資訊不多，直接問我比較快」——BNI分會資料屬於內部/私有性質，本來就不是WebSearch查得到的範疇，已改為直接列出5項需要教練親自提供的關鍵事實(參訪須知數字/真愛與真實AI分會slogan/分會之光是否放真實數據/大台南南區轄下分會範圍/各分會FB與Line連結)。

**部署位置**：教練確認先放GitHub Pages測試稿(非Netlify正式站)，已放進`knowledges/2026-07-29_bni-nantai-mockup/`(注意：github_repos/整個資料夾被.gitignore排除，每個子資料夾其實是獨立GitHub repo，不能直接放草稿進去，這是本場才發現的真規則，暫放knowledges等內容定案後再由Mac建立實體GitHub repo)。

### 3. 🎯 Chrome新使用者資料夾位置（快速問答）
教練問Chrome新增使用者的User Data會落在C槽還是E槽，查證這台機器`C:\Users\bymyw\AppData\Local\Google\Chrome\User Data`本身是Junction指向`E:\Claude-Data\AppData\Chrome-User-Data`，回答新增的Profile會落在E槽（因為整個User Data資料夾早就搬家了）。

## 📋 下一場（Mac）直接開工任務

- **🟡 主線**：等教練回覆5項BNI網站細節後，把`knowledges/2026-07-29_bni-nantai-mockup/`兩份草稿的佔位內容(黃色提示條標記處)換成真實資料，並產出真愛分會/真實AI分會兩個套版版本，之後視教練指示建立實體GitHub repo+開Pages
- **🔴🔴🔴 BNI大台南小幫手「主動提醒」功能**（v77已設計好cron事件驅動架構，方向清楚，已多場未動手，優先度持續最高）
- 順手可問一句：AI微論壇那封60位BCC提醒信Gmail草稿後來寄了嗎（非急件，見上方戰果1說明）
- 嘉義場籌備（見v86，教練尚未給細節）

## 🔑 本場關鍵檔案索引
- `knowledges/2026-07-29_bni-nantai-mockup/真誠分會_index.html`：真誠分會版型草稿(比照bnidahan.com.tw)
- `knowledges/2026-07-29_bni-nantai-mockup/大台南南區_index.html`：大台南南區版型草稿(比照bni-tainan.com/Training-Program)
- `D:\Users\Desktop\bni_真誠分會_mockup.html`、`D:\Users\Desktop\bni_大台南南區_mockup.html`：教練Comet驗收用的桌面副本(與repo版內容相同)
- 本場無commit（版型草稿存於knowledges，尚未有正式commit對應的獨立repo）

