# /bni-credit網頁下一輪待改清單（2026-08-28教練提出，context 55%先記錄不動手）

教練明確指示：這次只記錄，等他開新對話框再動手改，本檔給下一場直接照著做。

## 待辦一：移除「已失效」(invalidated) 空分類

**背景**：教練問「已失效」跟「已過期」感不感覺是同一件事——查證後發現本質上真的是同一件事：
- 「已過期(expired)」的判定依據：會員資料頁「信用證」連結是`href="#"`（連不到證書頁），這條規則本身就是從真鑽分會丁大成這個真實案例驗證出來的——當初點進去看到的正是「Please contact support for further assistance」這句話，後來才訂規則「看到`#`就直接判定過期不用再點」。
- 「已失效(invalidated)」原本想涵蓋的情況：連結是**正常的**(有真證書編號能點進去)，但點進去後內容本身顯示「Please contact support」錯誤訊息。
- **279筆已開立記錄複查後，「已失效」這個分類一筆都沒有查到**——凡是連結正常的，內容也都正常顯示，「連結正常但內容顯示失效」這種情況從未真的發生過。這個分類目前是空集合。

**要做的事**：
1. `namecard-db/app.py`的`BNI_CREDIT_STATUS_MAP`/`BNI_CREDIT_STATUS_LABELS`/`BNI_CREDIT_STATUS_ORDER`移除`invalidated`這個key
2. `bni_credit_list()`裡`urgency`字典的`"invalidated": 4`那組也拿掉
3. `templates/bni_credit.html`的CSS `select.status-select.status-invalidated`那條規則、以及預設篩選`selected_statuses`裡的`"invalidated"`都要拿掉
4. 資料庫層面不用特別處理——因為這個分類本來就零筆記錄，沒有資料需要遷移
5. 改完照例：語法檢查+`./venv/bin/python3`用test_client測試`/bni-credit`正常渲染+重啟`com.coach.namecard-webapp`+commit+push+用真實Chrome開給教練看

## 待辦二：到期日用顏色標示更細緻的月數分級

教練提出兩個方案，要我評估哪個可視化效果更好：
- **方案一**：≥12個月綠色、12個月以下(到1個月之間)都算黃色、剩1個月算紅色
- **方案二**：12個月綠色、6個月黃色、3個月紅色

**我的分析(供下次開工參考，最終分界值仍需教練拍板)**：
方案一的問題是「12個月以下」這個黃色區間跨度太大(從11個月到1個月通通是黃色)，缺乏區分度，看到黃色沒辦法一眼知道到底急不急。方案二用12/6/3三個月數當刻度點，區間切得更細，資訊量更高，**我建議採用方案二的精神**，但方案二字面上只給了3個點，還缺一個「低於3個月」該算什麼顏色(比紅色更急?還是也算紅色)，以及「6~12個月之間」「3~6個月之間」這兩段區間各自算哪個顏色需要教練明確一次。

**建議的具體分級(下次跟教練確認後再寫死進程式碼，不要自己猜)**：
- ≥12個月：綠色（安全）
- 6~12個月(不含12)：黃色（開始留意）
- 3~6個月(不含6)：橘色（需要新增一個介於黃紅之間的顏色，目前CSS只有warn(橘黃)/urgent(紅)兩種，可以直接沿用現有的warn當「6~12個月」、新增更深的橘色給「3~6個月」，或者教練覺得三段式(綠/黃/紅)就夠不需要四段，這點要問清楚）
- <3個月：紅色（緊急）

**技術實作位置**：`namecard-db/app.py`的`bni_credit_list()`函式裡，目前用`remaining_days`(天數)配合`< 30`/`< 180`兩個門檻分成ok/warn/urgent三級(對應180天≈6個月、30天≈1個月)，改成月數門檻只要把比較條件換算成新的天數界線即可(12個月≈365天、6個月≈183天、3個月≈91天)，`templates/bni_credit.html`裡對應的`remain-label`/`remain-bar .fill`的CSS class(`ok`/`warn`/`urgent`/`overdue`)如果分4級要新增一個class。

## 待辦三：把「公司」欄位補齊

教練說「她們的公司應該都查得到」，要求把目前資料庫裡`company`是空白的記錄補上公司名稱。

**背景**：279筆已開立記錄(active/transferred/redeemed)本來就是從BNI Connect的信用証明細頁抓資料，那個頁面本身就有「公司: xxx」這一行，理論上都抓得到，但過去幾輪清查時有些記錄的`company`欄位是空的——**需要下一場先查清楚是「當初SOP執行時漏抓了」還是「這些人的公司欄位在BNI Connect上本來就是空白」**，不要假設一定查得到就貿然重新爬一次。

**目前資料庫缺公司欄位的確切筆數(2026-08-28查證)**：
| 狀態 | 總筆數 | 缺公司 |
|---|---|---|
| active | 59 | 29 |
| transferred | 158 | 68 |
| redeemed | 62 | 23 |
| expired | 33 | 33(全缺，這批沒有cert_id連不到證書明細頁，公司欄位理論上查不到) |
| not_issued | 38 | 36 |
| ineligible | 52 | 52 |

**active+transferred+redeemed共120筆缺公司、且都有`cert_id`可以直接navigate證書明細頁補查**，這是優先要做、風險最低(純唯讀)的部分。expired的33筆因為連結是`#`本來就進不去明細頁，公司欄位這條路線行不通，要嘛放棄、要嘛改查tabs-6會員資料頁看有沒有公司欄位(先前查證只有部分人的tabs-6頁面會顯示公司，不是每個人都有)。先用資料庫existing的`cert_id`欄位判斷：
1. 先查`SELECT count(*) FROM bni_credit_certificates WHERE company IS NULL OR company = ''`有幾筆
2. 對這些有`cert_id`的記錄(active/transferred/redeemed)，可以直接navigate到`viewAdminRegionCertificateOfCredit?isFormSubmit=true&memberCertificateOfCreditId={cert_id}`重新讀取一次「公司」那一行補上——**這是唯讀動作，不涉及任何按鈕點擊，安全**
3. 對沒有`cert_id`的記錄(not_issued/ineligible/expired)，公司欄位在tabs-6會員資料頁本來就不一定會顯示(參考先前查證，只有部分人的tabs-6頁面有「公司」這個欄位)，這批要嘛也去navigate查一次tabs-6頁面確認到底有沒有公司資訊，要嘛跟教練確認優先度只補「已開立」這批就好
4. 補完後`templates/bni_credit.html`的「公司」欄位顯示邏輯不用改(已經有`{{ r.company or '' }}`)，只是資料庫內容變豐富

## 執行順序建議
待辦一(移除已失效)最簡單，先做。待辦二(顏色分級)動手前先跟教練確認3~6個月/低於3個月的顏色定案。待辦三(補公司)工作量可能最大(要重新navigate很多筆)，建議先SQL查清楚缺多少筆再決定要不要用背景agent處理。
