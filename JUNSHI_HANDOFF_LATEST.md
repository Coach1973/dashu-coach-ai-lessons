# 軍師接力棒 · 2026-07-04 v44（Mac 終端機 Sonnet，session 收尾）

> 建立時間：2026-07-04 凌晨 12:10（台灣時間）
> 本棒執行者：Mac 終端機軍師 Sonnet 5
> 上一棒：v43（2026-07-03 下午1:30，新增時間鎖機關+session收尾）
> 本棒主軸：**bymyway.com 首頁正式換成 BigTree 講座頁（教練主動升級決策）+ 時間鎖 hook 首次真實誤報修復**

---

## 🎯 本場最終戰果總覽

### 1. 🟢🟢🟢 bymyway.com 首頁正式換版（本場最大任務）
- **新首頁**：`https://www.bymyway.com/` 直接顯示 BigTree 講座黑金風格頁
- **舊首頁**：搬到 `https://www.bymyway.com/old/`（page_id 25066，資料完全沒動）
- 技術機制：WordPress `page_on_front` 設定切到 27393，跟一般子頁部署共用自動站 SOP
- 連帶內容修改：導覽「立即聯繫」→「登入課程」（連到 `/dashboard`）、頁面最下方新增精選影片區塊（YouTube `zL4InI7s96Q`，從舊首頁原始碼查證找到，不是猜的）
- 踩坑：GitHub Pages 第一次部署失敗（系統暫時性問題），補空白 commit 觸發第二次部署成功
- 復原方法：`page_on_front` 改回 25066 即可，30 秒可逆
- 詳見記憶檔 `project_bymyway_homepage_replaced_with_bigtree.md`

### 2. 🔴 時間鎖 hook 上線後首次真實對話誤報，已修根因
- 案例38後新建的 `rule_taiwan_time_check.sh` 在真實對話中第一次誤判違規（回覆零時鐘數字仍被判定違規）
- 根因：舊版把信封層 `timestamp` 欄位 + 系統自動注入的提醒教材文字（本身含 UTC 範例）誤判成「AI處理過的資料」
- 修法：只掃真正的訊息內容文字，排除信封欄位跟 `type=="attachment"` 事件
- 驗證：原 8/8 回歸測試全過 + 兩個真實誤觸發輪重新模擬皆改回不誤判
- commit `f4c3ef13`
- 詳見記憶檔 `feedback_time_lock_hook_false_positive_fix.md`

### 3. 🟢 其他完成項目（小任務，細節見 git log）
- jiesheng-leadership 新增「與作者有約」實體座談會（7/23，高雄市立圖書館，限額70人）
- jiesheng-leadership 過期場次（6/5~7/1共5場）按鈕改灰色+標「已截止報名」
- bigtree/speakers-2026 新增「媒體報導」區塊，20則報導以分類標籤呈現（人際關係/職場話題/九型人格/公益演講/電臺訪談/雜誌專訪/雜誌廣告/演講邀約/希望之聲電台訪問），標題保留原文章headline；3則watchinese標題後來換成教練提供的真實標題；導覽拿掉「五個相信」減少擁擠

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🔴 | 下一棒軍師 | **教練指定下一個任務：企業健身房（海餅乾俱樂部・商務健身房）案子**。已有進行中的交接檔 `20260630-handoff_biz-gym-to-lenovo.md`（ACER→Lenovo，2026-06-30），內容含完整品牌數據、10個section結構、已上線 v2 於 `coach1973.github.io/bigtree/biz-gym/`。**開工前務必先讀這份交接檔**，避免重新問教練已經給過的品牌數據 |
| 🟡 | 下一棒軍師 | bymyway 新首頁的 OG meta（LINE/FB分享卡）目前沒設，跟舊首頁一樣靠 site_icon(26000大樹logo) fallback；若教練要分享連結出去，需照 SOP 步驟9額外補 |
| 🟢 | 下一棒軍師 | `rule_taiwan_time_check.sh` 修復後還沒經過長期真實對話驗證，運作幾天後回頭檢查 `distill/rule_taiwan_time_violations.log` 有無再誤報 |

---

## 🔑 本場關鍵記憶檔案索引

- `project_bymyway_homepage_replaced_with_bigtree.md` — 首頁換版完整技術細節+復原方法
- `feedback_time_lock_hook_false_positive_fix.md` — 時間鎖機關誤報根因與修法
- `20260630-handoff_biz-gym-to-lenovo.md`（workspace 根目錄）— 企業健身房案子完整交接（下一棒必讀）

---

> Mac 終端機軍師 Sonnet 5 親筆，2026-07-04 凌晨12:10台灣時間。教練確認總結上傳，下一場從企業健身房案子開始。
