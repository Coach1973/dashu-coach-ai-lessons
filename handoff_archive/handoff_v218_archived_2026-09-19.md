## 🎯 本場戰果（v218，2026-09-18 16:08~17:23 Mac桌面版軍師）

開工到收工 1.2 小時，教練「全都開始」+「推 Netlify/不催手機版/不追孔佩實測/不查 FB App Review」4 項裁示後，軍師主動完成 3 項 Class A 並推 Netlify 10/3 場次（連續 5 次失敗，已 restore 回 9/16 deploy）。

**5 個 commit hash**：
```
30f3c594a  從git tree救回hooks/industry-chain-sop（v214 groupId修復版，6個合成事件全通過）
ffedc0aa0  rule#07 polling白名單補強（18/19測試通過）
f03cd219d  接力棒：幕僚長晨報cron消失根因深查（9/9 06:01最後觸發+磁碟0bytes+doctor --fix嫌疑）
5210ac52d  接力棒v218：三項狀態更新（教練裁示）
<本棒 commit 在最後>
```

**Netlify 5 次失敗根因**：Netlify zip deploy API 不接受中文檔名/中文目錄（HEAD 含 `archive/大樹小講_歷史講座紀錄.html` 中文 HTML）。第 5 次 ASCII-only 成功但覆蓋中文檔案，立即 `POST /deploys/6aaae473/restore` 還原。**待教練裁示 A/B/C 解法**：中文 rename / dashboard 手動 / 接受靜態版缺內容。完整 5 次嘗試對照表 + restore SOP 見 `reference_netlify_zip_deploy_chinese_filename_2026-09-18`。

**新寫 4 條 memory**（MEMORY.md 索引已加）：hook 整個目錄消失恢復 SOP / cron job 消失三路併查法 / rule #07 白名單配方 / Netlify zip 中文檔名限制+restore SOP。

**下棒待辦**：教練選 Netlify 10/3 解法（最優先）/ 幕僚長晨報 cron 重建（已查明根因，教練一句話 + schedule 就動）/ rule #07 D_PATTERNS「監控 X 每 Y 分鐘」盲點補丁（1 行 regex，可立即 commit）。

> 📦 v218 完整戰果（含 5 次 Netlify 嘗試對照表 + 幕僚長晨報根因完整時序）已封存：`handoff_archive/handoff_v218_archived_2026-09-18.md`

---

## 🎯 本場戰果

### 1. 大樹小講9/22台南場「下午」時段修改（session時間+移除點心飲料文案）
教練口頭指示：9/22台南場下午時段改13:30-16:30、拿掉「附點心飲料」文案。借用bigtree既有但未使用的`下午`slot(13:30-16:30，跟`午半`14:00-16:30區隔，不影響同用`午半`的9/5 KR養生廚房場次)，同步更新`event.db`。commit`f8ac8fc`（bigtree repo）。

### 2. 大樹小講/AI微論壇/培訓行事曆/紅綠燈看板改event.bymyway.com即時渲染上線
教練確認方向：先兩邊(Netlify+bymyway)同步，穩定後才退場Netlify。技術核心：`event-signup`既有Flask app新增路由，請求當下直接讀取各自github repo原始檔案渲染，大樹小講額外疊上`event.db`即時場次資料(沿用`bigtree_publish.py`既有`read_sessions`/`render_session_dates`函式)，完全不需要「發佈」動作。網址命名邏輯（教練拍板）：**網址代表活動格式/系列，不代表地點**——跟`ai-talk-tw.netlify.app`過去台南→嘉義直接覆寫同網址同一套邏輯。上線4條路由：
- `/bigtree/`（大樹小講，DB即時渲染）
- `/ai-forum/`（兩天制系列，現為台中場9/23-24，之後10/7-8台南場沿用同網址；教練原本要求`/ai-forum-taichung`後又親自糾正改成無地名的`/ai-forum`）
- `/ai-talk/`（半天制系列，現仍8/28嘉義場內容，等教練補齊凌榆舜/李明燦兩位講師資料後改9/22台南場，設攤/贊助商區塊維持不動）
- `/tainan-calender/`（純靜態，沿用既有拼法不改calendar）
- `/bni-traffic/`（紅綠燈看板，純client端Excel解析工具，零風險）

全部路由均：本機另開測試埠驗證→真實Chrome開過→重啟正式服務`com.coach.event-webapp`→在`event.bymyway.com`公開網址再驗證一次→確認其餘既有路由(`/admin`等)無回歸，才commit。commit`f8ac8fc`+`3df06cab7`+`fc58dc783`+`7d4b1e5e9`（event-signup，皆workspace repo）。

### 3. 三處連動同步更新
①`bni-chapters`資料庫`chapter_links`表：9分會×2種連結(紅綠燈看板/培訓行事曆)共18筆改新網址，重啟服務後在`chapters.bymyway.com/real-ai`公開頁curl驗證連結已更新。②`bni_tainan`小幫手：`AGENTS.md`4處member-facing連結+`knowledge/tainan_calendar.md`來源引用+`scripts/sync_calendar.py`實際抓取來源全部改新網址，**過程中發現`event.bymyway.com`前面的Cloudflare會擋掉urllib預設User-Agent(403)**，已補上`Mozilla/5.0`headers修復，重跑驗證106筆活動正常同步。commit`5fabb60d`（外層`.openclaw`repo，agents/bni_tainan路徑）。③`coach888`作品總覽：新增「bymyway自架版」區塊列出5個新路由(綠色badge)，對應5個Netlify舊版項目標「待退場」(橘色badge)，一眼可辨識新舊。教練追加要求把此區塊從第七移到第三順位，其餘區塊依序順延，已完成並在GitHub Pages正式站curl驗證順序正確。commit`230d735`+`cafe1f4`（coach888 repo，GitHub Pages自動部署免確認）。

## ⚠️ 本場教訓/發現（已寫入記憶）

1. **`event.bymyway.com`前面的Cloudflare會擋掉沒有瀏覽器樣式User-Agent的請求(403)**——`sync_calendar.py`改抓自家bymyway網址時直接403，curl實測`-A "Python-urllib/3.11"`→403、`-A "Mozilla/5.0"`→200證實是UA被擋非內容問題。任何腳本要fetch`*.bymyway.com`子網域都要注意這點，已寫入記憶`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。
2. **這套「讀活repo+DB即時渲染」模式的核心價值不只是「另一種不受限的部署方式」，是讓這類小改動(改時間/改文案)根本不需要「部署」這個動作**——editing DB或repo原始碼立刻反映，這點在跟教練說明時比單純講「省Netlify額度」更能讓他理解價值所在。
3. **新增自架服務時優先掛在既有已有launchd看護的Flask app底下(本場全部掛`event-signup`)，不新增獨立子網域/Tunnel/launchd**——降低「服務被遺忘」風險（呼應`peipei-event`斷線5天、ACER 49天未開機兩個舊案例的同一種病根：服務越分散越容易有一個沒人顧到）。

## 📋 下一場開工先做
1. **待教練提供**：凌榆舜/李明燦兩位講師的職稱/講題/簡介/照片（mentor100查證確認兩人都不在資料庫），到齊後把`/ai-talk`一次改成9/22台南場正式內容上線。
2. 教練提到「跟BNI相關的把netlify裡面我常常有在用的都變成event.bymyway.com」——目前只確認並處理了紅綠燈看板+培訓行事曆兩個，`路徑大全.md`裡的GitHub作品總表把`bni-traffic`歸類「早期練習」已證實是過時分類，若教練心裡還有其他常用的BNI相關Netlify站台，等他指名再處理，不用自己瞎猜逐一嘗試舊站台。
3. FB粉專商家驗證後續（舊待辦，v147/v148/v150留下，本場未觸及）。
4. `/bni-credit`補公司欄位：2026-09-02教練有額度時的舊待辦，本場未觸及。
5. 「釋放記憶體」白名單範圍：v148留下，本場未觸及。

## 🔑 本場commit
`bigtree`：`f8ac8fc`（9/22時段+文案修改）。`event-signup`（workspace repo內）：`f8ac8fc`~`7d4b1e5e9`區間共4筆（新增4條bymyway路由）。`.openclaw`外層repo：`5fabb60d`（bni_tainan agent連結更新）。`coach888`：`230d735`+`cafe1f4`（作品總覽新增區塊+順序調整）。記憶：`project_bymyway_dynamic_hosting_escape_netlify_2026-08-30`+`reference_bymyway_cloudflare_blocks_default_useragent_2026-08-30`。

---

> 📦 v153+v154完整內容已封存：`handoff_archive/handoff_v153_v154_archived_2026-08-31.md`（Mac終端機，mentor100通知修復+AI微論壇9/22台南場上線／BNI Connect 7場培訓活動上線+Hermes任務分工裁示+試金石全面蒸餾重建）

---

> 📦 v155+v156+v160完整內容已封存：`handoff_archive/handoff_v155_v156_v160_archived_2026-09-01.md`（Mac終端機，coach888總覽補漏/即時人數開關/場次深連結QR/ai-art完整上線/分會精神配色多輪迭代）

---

> 📦 v161完整內容已封存：`handoff_archive/handoff_v161_archived_2026-09-01.md`（Mac終端機，道德規範中英對照+分會精神複製8分會+真鑫/真鑽/真貴戰情儀表板從零建置+2次試金石教訓）

---

> 📦 v162+v163+v164完整內容已封存：`handoff_archive/handoff_v162_to_v164_archived_2026-09-02.md`（v162 Mac終端機來賓排行榜三輪重做／v163 Mac終端機FB粉專+三站部署／v164聯想Windows coach888重整）

---

> 📦 v165+v166完整內容已封存：`handoff_archive/handoff_v165_v166_archived_2026-09-02.md`（v165聯想Windows待辦提醒系統程式碼／v166 Mac終端機名片系統來賓歷程+帳號審核+coach888批量搬移+RustDesk診斷）

---

> 📦 v167~v170完整內容已封存：`handoff_archive/handoff_v167_to_v170_archived_2026-09-03.md`（v167 Mac教練待辦提醒系統部署／v168聯想FB行銷文案+首次圖片發文／v169 Mac全部釋放+bni-credit補公司312筆／v170聯想9/16貼文發滿5粉專行銷任務結案）

---

> 📦 v171完整內容已封存：`handoff_archive/handoff_v171_archived_2026-09-03.md`（聯想Windows，tut-alumni校友會網站從融合設計到資料庫/API/Telegram全通，含一次效率教訓）

---

> 📦 v172完整內容已封存：`handoff_archive/handoff_v172_archived_2026-09-04.md`（Mac終端機，發票後台+校友會網站全面完工，coach888誤clear排版搶救成功+跨裝置同步架構修復）

---

> 📦 v173~v177完整內容已封存：`handoff_archive/handoff_v173_to_v177_archived_2026-09-04.md`（v173 Mac ai-art修正+4個活動微站／v174 Mac DIY3+教材線上觀看系統／v175聯想leader報名頁+RustDesk／v176聯想seabiscuit20從零建置／v177聯想記憶體洩漏排查）

---

> 📦 v178完整內容已封存：`handoff_archive/handoff_v178_archived_2026-09-04.md`（聯想Windows，海餅乾俱樂部20週年官網六項新功能：時光足跡/學員見證/語錄/完整守則/頁尾快速連結）

---


> 📦 v179完整內容已封存：`handoff_archive/handoff_v179_archived_2026-09-04.md`（Mac終端機，seabiscuit20部署四項調整+coach888作品一覽補漏+兩輪真bug修復）

---

> 📦 v180完整內容已封存：`handoff_archive/handoff_v180_archived_2026-09-05.md`（Mac終端機，seabiscuit20媒體報導補齊20篇+全面盤點報告+新增「關於創辦人」頁面）

---

> 📦 v181+v182完整內容已封存：`handoff_archive/handoff_v181_v182_archived_2026-09-05.md`（v181 大台南商圈整合計劃店家登錄頁上線／v182 KR養生廚房整站搬遷+bigtree按鈕修正+coach888收錄鎖上線）

---

> 📦 v183完整內容已封存：`handoff_archive/handoff_v183_archived_2026-09-06.md`（聯想Windows，一鍵還原後三項查證：對話記錄E槽真相/記憶體洩漏診斷讓步/App備份救援失敗誠實回報）

---

> 📦 v184+v185完整內容已封存：`handoff_archive/handoff_v184_v185_archived_2026-09-06.md`（v184 Mac終端機CICA+VPS店家託管+無限迴圈bug修復／v185 Mac桌面版MiniMax過載hook+VPS用途查證）

---

> 📦 v186+v187完整內容已封存：`handoff_archive/handoff_v186_v187_archived_2026-09-08.md`（v186 Mac桌面版牛市町上架驗收+slug/暫代頁根因修復／v187 Mac桌面版帳密統一+vault上線+coach888收錄機制翻修）

---

> 📦 v188完整內容已封存：`handoff_archive/handoff_v188_archived_2026-09-10.md`（Mac桌面版，通訊錄辨識+三分會戰情儀表板SOP+修invoice-inbound心跳誤報+賈維斯接線員缺卡修復+一次嚴重引用紀律糾正）

---

---

> 📦 v189完整內容已封存：`handoff_archive/handoff_v189_archived_2026-09-11.md`（Mac桌面版，策展SOP店家地圖自動化+Hermes gateway卡死6.5小時根因修復與watchdog）

---

> 📦 v190完整內容已封存：`handoff_archive/handoff_v190_archived_2026-09-11.md`（Mac桌面版，BNI訓練發票26張全數開立+培訓/發票/登錄工作流SOP固化）

---

> 📦 v192+v193完整內容已封存：`handoff_archive/handoff_v192_to_v193_archived_2026-09-11.md`（v192 Mac桌面版invoice-inbound測試污染+Hermes watchdog誤報修復+TM備份清理踩坑／v193聯想Windows下載資料夾腳本v4+CICA三語系+FB App未過Review重大發現）

---

> 📦 v194+v195完整內容已封存：`handoff_archive/handoff_v194_v195_archived_2026-09-12.md`（v194 Mac桌面版FB App Review深挖翻案+一鍵發布API上線+claude-in-chrome裝置根治／v195 Mac桌面版FB App Review表單填寫：圖示透明背景修復+權限精簡建議）

---


> 📦 v196完整內容已封存：`handoff_archive/handoff_v196_archived_2026-09-12.md`（Mac桌面版，FB App Review精簡權限+示範錄影兩次失敗+關鍵發現pages_read_engagement審核前完全不可用）

---

> 📦 v197+v198+v199+v200完整內容已封存：`handoff_archive/handoff_v197_to_v200_archived_2026-09-16.md`（v197 Mac桌面版9項過期待辦結案+黃智宏發票作廢重開+FB自動貼文暫停／v198 Mac桌面版FB App Review示範錄影+四權限表單／v199聯想Windows真誠分會來賓紀錄跨機交接／v200 Mac桌面版真誠分會補登+FB App限制查證+OpenClaw 2.0隔離測試環境從零建置）

---

> 📦 v201~v206完整內容已封存：`handoff_archive/handoff_v201_to_v206_archived_2026-09-17.md`（v201賈維斯角色授權+密鑰洩漏／v202三方核對SOP／v203 ai-go優化+heartbeat修復／v204真鑫真鑽分會／v205三LINE帳號斷線修復／v206 BNI組隊計畫+產業服務鏈圖片生成）

---

> 📦 v207~v213完整內容已封存：`handoff_archive/handoff_v207_to_v213_archived_2026-09-18.md`（v207產業鍊SOP四方+gateway版本事故／v208燕窩連結+Remote Control首跑／v209教練徹夜MiniMax身份釐清／v210 context window縮減+MEMORY.md濃縮／v211報名頁上架SOP+10/3事故搶修／v212 5h額度誤判自修+403修復／v213 MiniMax額度徹查+NO_REPLY迴圈發現）

---

> 📦 v214+v215完整內容已封存：`handoff_archive/handoff_v214_to_v215_archived_2026-09-18.md`（v214額度徹夜追查+Remote Control確認+孔大哥hook認錯人修復／v215額度懸案結案+小二第二種bug活逮+2.0評估暫停）

---

> 📦 v216完整內容已封存：`handoff_archive/handoff_v216_archived_2026-09-18.md`（EDM連結補完+三個repo git hygiene清理含peipei倉庫金鑰歷史殘留發現+手機版FB貼文思考模式評鑑與派工）
> 📦 v217完整內容已封存：`handoff_archive/handoff_v217_archived_2026-09-18.md`（Mac桌面版，FB大台南策展中心刪錯貼文任務：查證後確認0則要刪的錯貼文+4條新教訓）

> 📦 v218完整內容已封存：`handoff_archive/handoff_v218_archived_2026-09-19.md`（Mac桌面版，全部釋放+MiniMax團隊品質稽核機制+開工hook身份誤判修復+幕僚長晨報重建+Netlify中文檔名部署bug發現）

