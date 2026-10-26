# 教訓：curation_check_result.py 回 `found:false` 不等於「上架失敗」

> 記錄日期：2026-10-27（hsiuli 黃秀麗個人品牌頁案）
> 來源：聯想軍師 2026-10-04 派工單 `cross-agent/inbox/xiaolongxia/20261004-1419_lenovo-to-xiaolongxia_hsiuli-curation-shop-upload.md`

## 情境

教練要上架 BNI 夥伴黃秀麗的個人品牌頁，走策展 SOP（`kind=shop`，短網址 `hsiuli`），信裡把來源網址、slug、金鑰位置、驗證步驟全都寫好了。

小龍蝦收到後查 `python3 scripts/curation_check_result.py hsiuli`，得到：

```json
{ "found": false, "status": "not_found" }
```

於是把這件事標成「結不了案／404／設定遺失」，前後拖了 **23 天**，期間每次狀態檢查都得到同樣的 `found:false`，卻從來沒有回報教練「我卡在哪裡」。

2026-10-27 重新從頭查證才發現：**這件事根本沒做過**。

## 根因

`found:false` 有**兩種完全不同的意思**，外觀一樣，處置相反：

| 情況 | 判別依據 | 該怎麼做 |
|---|---|---|
| ① 上架真的失敗／卡住 | log 有這個關鍵字，或 `incoming/`、`processing/`、`failed/` 有對應檔案 | 查 log、查失敗原因、必要時重傳 |
| ② 從來沒上過 | log 查無此關鍵字，三個目錄都沒有對應檔案 | **這是待辦，不是問題** → 直接照信做完 |

當時只看到 `found:false` 就往「網址被占用／設定遺失」方向猜，**從沒驗證過 ① 還是 ②**，所以 23 天裡從未真正動手。

## 正確做法

1. 先分清楚 ①／②：`grep` log 關鍵字 + `ls` `curation_uploads/{incoming,processing,failed}/`。
2. 是 ② → 這就是一件還沒做的任務，直接做，不要寫信求助、不要猜設定壞掉。
3. 上傳前確認教練已拍板的事項（`kind`、slug、來源網址）——**已拍板的不需要再問任何人**。
4. 上傳後一律跑 `curation_check_result.py <slug>` 拿真正結果，不要用 curl 猜網址。

## 同場實測：`kind=shop` vs `kind=creation` 的驗收標準不同

這次 `kind=shop` 實測結果：

| 項目 | `kind=shop` | `kind=creation` |
|---|---|---|
| GitHub repo | 會建 | 會建（private） |
| GitHub Pages | **會開**（`https://coach1973.github.io/<slug>/` 回 200） | **不會開**（Pages 網址 404，registry 的 `github_pages_url` 是空字串） |
| 大台南商圈名冊卡 | **會自動插入** | 不插（`no_shop_card`） |
| 狀態工具回值 | `success_shop_new` | `success_creation` |

→ **不要拿 creation 的驗收標準去套 shop，也不要把 shop 的當成 creation 的成功**。

## 同場實測：FB 自動貼文可能整站停用

log 記「⏸️ FB自動貼文已暫停(App Review未通過，訪客看不到)，跳過…請人工評估是否手動補發」。這是**全站既有狀態**，不是本個案問題，但上架後要照實回報，不要假裝 FB 也發了。

## 結果（本案）

- 上傳 `kind=shop` + `custom_slug=hsiuli` → HTTP 200「✅ 已收到「hsiuli.zip」」→ `success_shop_new`／`live_check_http_status: 200`。
- 名冊卡已插（category=`樂`）／repo `Coach1973/hsiuli` 已建且 Pages 200／群組通知 `message_id=12806` 已送。
- 最終網址：https://event.bymyway.com/curated/hsiuli/

## 最重要的一句

**收件匣裡的未結案信件＝待辦，不是垃圾。**
狀態查詢回 `found:false` 時，先問自己一句：「這件事到底做過了嗎？」——然後回報教練你在等什麼。拖 23 天不動還不回報，是比做錯更嚴重的事。
