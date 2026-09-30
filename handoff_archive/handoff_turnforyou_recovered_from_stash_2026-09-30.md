# 封存：turnforyou 觀眾席最終建置（原始棒，2026-09-28 深夜完成，2026-09-30 從 git stash 救回）

> 這是小龍蝦（MiniMax-M3）09-28 完成 turnforyou 觀眾席任務時寫的接力棒。
> **問題**：它直接整份覆蓋 `JUNSHI_HANDOFF_LATEST.md`（沒有先讀、附加在最新棒之上），而且從沒 commit——
> 內容一直停留在這台 Mac 的「未提交工作區」裡長達近 40 小時，直到 09-30 總結時 `git pull` 才因為
> 檔案衝突被發現。詳情與根源修法見試金石案例 90。
> 原始內容完整保留於下，方便日後查閱 turnforyou 觀眾席建置細節。

---

## 教練這輪交辦

把 mentor100 + 真誠分會 + 8 個 curated店家 + 大樹教練本人，共 **28 位夥伴** 列在 turnforyou 站內的「外圍團隊觀眾席」（Act 06.5），每位要有圖、頭銜、專業描述、來源連結。

---

## 最終線上狀態（2026-09-28 23:10 已上線）

| 編號 | 姓名 | 角色 | 圖檔 | 來源 |
|---|---|---|---|---|
| 1 | 吳大樹 | 大樹教練 | `15-dashu.jpg` | BNI 真誠分會 |
| 2 | 林佳伶 Lavi | LAVision Image | `01-lavi.jpg` | BNI 真誠分會 |
| 3 | 蘇秦 | AI 創意教學專家 | `02-suqin.jpg` | Mentor 100 |
| 4 | 凌榆舜 (iSmart) | 智匯商機 | `03-linyushun.jpg` | Mentor 100 |
| 5 | 余尚恩 | 屏東科大 | `04-yushangen.jpg` | Mentor 100 |
| 6 | 陳佩君 (佩佩老師) | 鋼琴家 | `05-chenpeijun.jpg` | BNI 真誠分會 |
| 7 | 楊在珍 | 信望愛創意 | `06-yangzaizhen.jpg` | BNI 真誠分會 |
| 8 | 鄒昆廷 | 朋昶數位 | `07-zoukunting.jpg` | Mentor 100 |
| 9 | 李中閔 | 宸霖智權 | `08-lizhongmin.jpg` | Mentor 100 |
| 10 | 陳宜璟 | 薩加瑪奇克 | `09-chenyijing.jpg` | Mentor 100 |
| 11 | 王夏儷 | EZ Player | `10-wangxiali.jpg` | Mentor 100 |
| 12 | 葉建葳 | 理理創意 | `11-yejianwei.jpg` | BNI 真誠分會 |
| 13 | 季哥 Eric Chi | 凱基人壽 | `12-jige.jpg` | Mentor 100 |
| 14 | 王彤 | 雲智永續 | `13-wangtong.jpg` | BNI 真誠分會 |
| 15 | 林孟寬 | 青山永續 | `14-linmengkuan.jpg` | Mentor 100 |
| 16 | 林信翰 (阿翰) | 鑫瀚昌旅行社 | 無圖 | event.bymyway.com/hsinhan |
| 17 | 宋美伶 | 鑫瀚昌旅行社 | 無圖 | event.bymyway.com/hsinhan |
| 18 | 許朝竣 (維尼) | 百聖廣告 | `17-xuchaojun.jpg` | event.bymyway.com/bai-sheng |
| 19 | 柯朝陽 | 牛市町 Bull Market | `19-kecy.png` | event.bymyway.com/niu-shi-ting |
| 20 | 黃秀麗 | 全國古典音樂推廣版主 | `20-huangxiuli.jpg` | tava-ai.com（教練新給的） |
| 21 | 傅恩平 | 榮益齋有限公司 | `21-new.jpg`（教練新給的） | event.bymyway.com/fu-en-ping |
| 22 | 楊尚儒 D.M.A. | 小提琴・中提琴 | `16-yangshangru.png` | event.bymyway.com/yang-shang-ru |
| 23 | 張育慈 (慕斯) | 順業肥料 | `18-zhangyuci.jpg` | event.bymyway.com/zhang-yu-ci |
| 24 | 張玉盞 | 立馬集團 | `24-zhangyuzhan.jpg` | event.bymyway.com/ema（頂替 Abby） |
| 25 | 鄭禮昂 | 禮享家企業社 | `19-zhenglianang.jpg` | BNI 真誠分會 |
| 26 | 李美花 | 美麗樂生技 | `21-limeihua.jpg` | BNI 真誠分會 |
| 27 | 鄭綉美 | 方碩方有限公司 | `22-zhengxiumei.jpg` | BNI 真誠分會 |
| 28 | 郭展鴻 | 大紀元時報 | `23-guozhanhong.jpg` | BNI 真誠分會 |

---

## 檔案位置

- **`/Users/bymyway/github_repos/turnforyou/index.html`**（441558 bytes / 已備份 .bak1 ~ .bak17）
- **`/Users/bymyway/github_repos/turnforyou/img/audience/`** — 共 24 張圖檔（25 個檔名但 19-kecy.png 是給柯朝陽新換的）
- 直接讀本機檔（無 .git，server 直接 serve 本機）

---

## 這輪修了哪些 bug / 做了哪些事

### 1. 「下面內容看不到」慘案（修兩次）
- 9/28 第一次修，加了 `.no-js .reveal` CSS fallback + 1.5 秒 setTimeout
- 這輪**徹底改用 opt-in 機制**：把 `.reveal{opacity:0}` 改成 `.reveal.armed{opacity:0}`，JS 啟動時才加 `.armed` 標記。JS 出問題時元素保持可見。

### 2. SyntaxError：重複宣告 const fd
- 9/28 改單時在 form submit handler 內 `const fd = new FormData(form)` 寫了**兩次**，導致 main script 整個中斷
- `renderAudience()` 在 main script 裡 → 永遠沒被呼叫 → audienceGrid 永遠空
- 修法：刪掉重複那行

### 3. fetch+boot 流程的 DATA 被覆蓋
- `data.json` 是頁面真正使用的資料源（353KB），不含 audience 欄位
- `Object.assign({}, DATA, __C.data)` + fetch 後 `DATA = data.json` → FALLBACK 的 audience 被蓋掉
- 修法：獨立 `<script id="audience-data">` 把 29 位觀眾席放進 `window.__AUDIENCE__`，`renderAudience()` 優先讀它

### 4. inline render script 位置錯誤
- 第一次把 script 插在 `<meta charset>` 前面，破壞 HTML parser（會把後面當 script 內容吃掉）
- 修法：移到 `<body>` 開頭之後

### 5. 圖檔沒實際抓
- 教練第一輪問「為什麼沒有頭像」，我才發現前幾輪只說「補 photo 欄位」但根本沒去抓
- 抓了 **18 張**：15 張 mentor100 + 3 張 curated
- 第二輪教練說「真誠分會 12 位你只抓 6 位」，再補抓 **6 張** → 共 24 張

### 6. 編號搞錯（教練糾正）
- 教練說「編號 20 換成黃秀麗」我誤以為是張羽家那筆（其實張羽家在 #8）
- 教練糾正後整個 audience-data 區段重組，最終正確順序：
  - #20 黃秀麗（取代李佩玲）
  - #21 傅恩平（換新照片 21-new.jpg）
  - #24 張玉盞（取代 Abby，有機水產火鍋頂替）
  - Abby 整筆刪除

---

## 重要教訓（給未來的軍師 / 小龍蝦）

### 🔴 「編號」不要自己腦補
教練說「編號 20」，**不要**用圖片檔名（20-huangxiuli.jpg）、**不要**用陣列中的「原編號」（圖檔順序），要看**實際渲染後的編號**（也就是 audience 陣列的索引，從 1 開始）。下一次接到「換編號 X」指令時，**第一件事**：用 curl 拉線上 `/tmp/turnforyou.html`，parse audience-data，列出當前 `[編號] 姓名 → 圖檔`，再決定要改誰。

### 🔴 改東西前先看實際渲染結果
我第一輪說「補 photo 欄位就好」但沒去抓圖 → 教練看不到任何圖 → 來回三輪才搞定。教訓：**有「補資料」動作時，不要只更新 metadata，要實際驗證 URL 是 200、檔案有圖、非 placeholder**。

### 🔴 inline script 別插在 head 開頭
HTML parser 規則：`<script>` 後面如果不是 `</script>` 結尾，會把後續 `<meta>`、`<link>` 等都當 script 內容處理。**所有 inline script 都該放在 `<body>` 開頭之後、或 `</body>` 之前**。

### 🔴 `const fd` 之類變數別重複宣告
9/28 改單時複製貼上沒看仔細，連續貼了兩次 `const fd = new FormData(form)`，瀏覽器直接 SyntaxError 中斷整個 main script。**改單時一律先 grep 確認要改的位置唯一，再 patch**。

### 🔴 主動抓圖時先確認 image type
`file 圖檔.jpg` 可以立刻驗證是否有人像尺寸（200x300 以上）。vision_analyze 確認是否真人是「門檻動作」不是「多餘動作」。

---

## 觀眾席沒圖的 4 位（教練日後可補）

- #16 林信翰 (阿翰) — curated/hsinhan 沒個人肖像（hero 是風景照）
- #17 宋美伶 — 同上
- #19 柯朝陽 — 9/28 已用教練新照片替換
- （如果還要補，告訴我從哪個網址抓）

---

## 接力棒後續待辦（給軍師接手）

1. 觀眾席版面可能微調（教練曾說「內外專家選單」要做，目前留白）
2. 案例牆（Act 06）教練說「可能要做 100 個案例」，需要時間蒐集
3. 報名表單（form submit → Telegram 通知）9/28 接通的，當初因 const fd 雙重宣告壞掉一陣子，本輪修好
4. reveal bug 已徹底修，未來若再有「下面看不到」慘案，先看 `.armed` 是否被 JS 正確加上

---

> 立檔人：小龍蝦（minimax/MiniMax-M3）
> 完成時間：2026-09-28 23:10（台灣時間）
> 線上檔大小：441558 bytes
> 已備份鏈：`.bak1` (424791) → `.bak17` (441558)
> 已知衝突：本棒沒有 commit hash（turnforyou 是直接讀本機檔，沒 git）
