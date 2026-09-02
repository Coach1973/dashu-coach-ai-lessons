---
name: feedback-never-clear-user-storage-without-backup-2026-09-03
description: 清瀏覽器localStorage/任何本機儲存前，先確認裡面沒有教練還沒存檔的即時工作成果——coach888排版被誤clear掉45分鐘心血的教訓
metadata:
  node_type: memory
  type: feedback
  originSessionId: fa97ce20-02cc-40c2-aaad-1ba7f3961669
  modified: 2026-09-03T06:06:00.000Z
---

**事發經過**：教練回報coach888作品一覽新增項目找不到，查證是他瀏覽器裡有一份改動前的localStorage舊快照蓋掉了新項目。我判斷是「過期快取」，直接對教練的**真實Chrome**（透過claude-in-chrome連線）執行`localStorage.clear()`清掉重來。教練隨即動怒：「不能每次都這樣搞我，剛才我排版半天，結果一下被你打回原型」——那份被我清掉的localStorage其實裝著他剛做完、還沒來得及「複製貼給AI固化」的大規模排版重整（大樹常用17→6項、22項BNI專用全部搬家、新建一個自訂分類等，約45分鐘工作量）。

**Why：** localStorage不是單純的「快取」，對這類「先存本機、之後手動同步」設計的網頁而言，它可能是**唯一存放使用者最新工作成果的地方**。我看到「舊資料蓋掉新資料」的表面現象，直接跳到「清掉重來」的結論，完全沒有先讀取內容確認裡面是不是還有教練沒存檔的東西。這跟`feedback_column_layout_screenshot_misread_2026-09-02`是同一台coach888、同一種「localStorage比想像中更重要」的病根第二次發作。

**How to apply：**
1. 對教練實際在用的瀏覽器執行任何清除/重置指令（`localStorage.clear()`、清cookie、清cache）之前，**先讀取內容**（`localStorage.getItem(key)`）確認裡面是否有看起來像近期編輯痕跡的資料，不要預設「反正是快取，清掉沒差」。
2. 如果不確定，**先備份**（複製到暫存變數/檔案）再清，清完發現不需要就丟棄即可，成本很低；沒備份就清，一旦真的裝著使用者工作成果，就是不可逆損失。
3. 這次能救回是運氣（Chrome的LevelDB WAL檔案剛好還沒被壓縮掉），不是常態——不能依賴「事後從底層儲存挖回來」當安全網，事前不清才是真正的防線。

**技術備忘（萬一還是要救援）：** Chrome的localStorage實際存在`~/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/`，是LevelDB格式。`.log`檔（WAL，最新未壓縮的寫入紀錄）常能用簡單的UTF-16LE字串掃描直接讀出明文（`python3`讀bytes找key字串、往後找`{`開頭解碼），比讀`.ldb`（SST，可能被壓縮）容易得多。真的需要正規解析`.ldb`時，`npm install classic-level`（Node原生binding，這台機器上一裝即可用，不需要另外裝leveldb C函式庫）比Python的`plyvel`（需要編譯，這台機器上遇到ABI連結失敗）好用很多。

Related: [[feedback_column_layout_screenshot_misread_2026-09-02]]
