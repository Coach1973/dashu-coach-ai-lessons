# 交接：BNI Connect會員電話/Email收集方法（給接手的新對話框）

> 教練2026-08-26交辦：430位BNI Connect大台南南區會員（92現任+338前會員）
> 已匯入namecard-db，但電話/Email缺很多，教練要求補齊。
> 本檔記錄已驗證可行的方法，避免重新摸索。

## 目前進度
- 94人：從既有ezPay開票資料`claude-brain/data/bni_region_members_contact_2026-08-18.csv`複用，已完成
- 真誠分會（116筆原始資料，108筆抓到）：已完成，見`contact_scrape/batch_zhencheng_p*.json`
- **待做：真富(47)、真愛(27)、真鑫(30)、真鑽(288)，共392筆原始資料**
- 目前430人中已有181人有電話（`sqlite3 namecards.db "SELECT COUNT(*) FROM cards WHERE image_filename LIKE 'bniconnect__%' AND mobile!='' "`可查）

## 已驗證可行的抓取方法（claude-in-chrome，教練Mac本機瀏覽器）

1. 確認裝置：`list_connected_browsers`確認`isLocal:true`是Mac（教練糾正過連錯機器的教訓）
2. 導覽到 `https://www.bniconnectglobal.com/web/secure/operationsChapterManageMembership?countryId=7699&regionId=23268&chapterId=23528`（教練已登入BNI Connect，session共用）
3. 點「選擇分會/核心小組」下拉選單，點分會名稱（真富/真愛/真鑫/真鑽），再點「搜尋會員」——這個網址記得**每次都要重新點分會+搜尋**，不會自動帶出結果
4. 頁面顯示筆數選100（`顯示`下拉選單），減少分頁次數
5. **關鍵技巧**：用`javascript_tool`直接在頁面執行以下腳本，一次抓多人（親測15~17人/次穩定，超過20人容易`Internal error`逾時；回傳資料筆數太多也會被截斷，抓超過~13筆記得用accumulator模式累積在`window.__bniContacts`分批取出）：

```javascript
var links = Array.from(document.querySelectorAll('a[href*="operationsRegionEditMembership"]'));
var people = links.map(function(a) {
  var row = a.closest('tr');
  var name = row ? row.cells[0].textContent.trim() : '';
  var m = a.href.match(/memberId=(\d+)/);
  return { name: name, memberId: m ? m[1] : null };
}).filter(function(p){ return p.memberId; });

function getVal(html, name) {
  var re = new RegExp('name="' + name + '"[^>]*value="([^"]*)"');
  var m = html.match(re);
  return m ? m[1] : '';
}

var results = [];
for (var i = 開始index; i < 結束index; i++) {
  var p = people[i];
  var xhr = new XMLHttpRequest();
  xhr.open('GET', '/web/secure/operationsRegionEditMembership?legacyPortal=true&memberId=' + p.memberId, false);
  xhr.send(null);
  var html = xhr.responseText;
  results.push([p.name, p.memberId, getVal(html,'memberPhoneNumber'), getVal(html,'memberMobileNumber'), getVal(html,'memberEmail')]);
}
JSON.stringify(results);
```

回傳格式是 `[姓名, memberId, 電話, 手機, Email]` 陣列，每批約10~15筆，抓完直接存進本目錄新檔案（比照`batch_zhencheng_p*.json`命名，例如`batch_zhenfu_p1.json`）。

**踩過的坑，不用再踩一次：**
- 「分會名單報告」(reportsChapterRoster) 是PDF格式，`get_page_text`/`read_page`都讀不到內容，Cmd+S也觸發不了真正的下載（遠端瀏覽器控制對系統層級快捷鍵無效），這條路已驗證走不通，不用再試
- 一般`fetch()`+`.then()`拿不到結果——`javascript_tool`不會等待Promise resolve，一定要用**同步XHR**（`xhr.open(..., false)`）
- 曾經被安全過濾器擋下`[BLOCKED: Cookie/query string data]`，原因是用了`btoa`轉二進位編碼，純文字regex擷取不會被擋

## 寫入資料庫的方法

```python
# 比照 parse_and_import.py 的 normalize_name() 邏輯比對姓名
# UPDATE cards SET mobile=?, email=? WHERE id=?
# 電話優先用「手機」欄位，沒有才退回用「電話」欄位
```

完整範例見這次對話已經跑過的Python片段（存在本檔上層對話紀錄裡，或直接照上面邏輯重寫，很短）。

## 完成後

- `git add namecard-db/bni_connect_import/contact_scrape/ namecard-db/bni_connect_import/HANDOFF_*.md`
- commit + push
- 跟教練回報：430人中最終有幾人補到電話/Email，哪些人BNI Connect上本來就沒有留電話（如實回報，不要硬凑）
