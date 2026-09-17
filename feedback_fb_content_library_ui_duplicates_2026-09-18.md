---
name: feedback-fb-content-library-ui-duplicates-2026-09-18
description: FB經理人「內容資料庫」body.innerText把每則貼文顯示兩段（內文+展開副本），slug URL count 2~4次是UI假象不是真的重複網址；判斷「真重複」要看「半段內部」。
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1de66f96-d9d3-5a68-89e7-7fea62fd2005
---

# FB 內容資料庫的 UI 重複假象陷阱

**規則**：掃描 FB 經理人「內容資料庫」（`professional_dashboard/content/content_library/`）的貼文是否有「重複網址」時，**絕對不能用全文的 `event.bymyway.com/curated/<slug>` 出現次數當判斷**——要切到「半段內部」（「已發佈•時間」這個分隔符之間的內容）單獨數，才知道實際有幾個 URL。

**Why**：2026-09-18 凌晨掃大台南策展中心策展貼文時，FB 內容資料庫預設時間範圍「過去 28 天：8月21日 - 9月18日」內 13 則全部正確（v4 跑的，單一 URL 格式），但 body.innerText 全文 dump 出來 9543 字，每個 slug 看似出現 2~4 次。

實際抓出來看：
```
張育慈｜順業肥料資材行從土壤到餐桌...👉 https://event.bymyway.com/curated/zhang-yu-ci/...
張育慈｜順業肥料資材行 從土壤到餐桌...👉 https://event.bymyway.com/curated/zhang-yu-ci/...
```
這是**同一則貼文被內容資料庫列了兩段**（預覽行 + 展開後的貼文副本），每段內各有 1 個 URL，所以全文看是 2 次，半段看是 1 次。

每個 slug 的真實出現次數：
- `xiaonan/xiangjuchang/sbip/peipei/nmda-2/nmda/kangyenju/historic-residence` → 全文 4 次（每則被列兩段 × 每段 2 URL = 4）→ 實際 1 次
- `zhang-yu-ci/xie-wei-xiang` → 全文 2 次（剛貼的最上面兩則，FB 還沒展開副本）→ 實際 1 次

**沒有任何一則真的有重複網址**，全部都是 v4 buildPostBody 寫的單一 URL 格式。

額外坑：
- `div[role="article"]` selector 在 content_library 完全抓不到 0 個，內容資料庫的 DOM 結構跟 timeline 不同
- body.innerText 裡的 `<a href="/posts/...">` permalink 也極少，只有 nav 那邊的 1 個，不是策展貼文本身
- 區段切法：以「已發佈•」當分隔符，能切出 N 段（N = 貼文數 × 2），但 permalink 大部分抓不到，所以「區段」對齊不到「策展貼文」

**How to apply**：

| 場景 | 判斷方式 |
|------|---------|
| 看 body.innerText 全文的 slug URL count | 必須 ÷ 2 或 ÷ 4 才知道實際幾則，不要直接用 count ≥ 2 判定「重複要刪」 |
| 切半段（以「已發佈•時間」分隔）檢查 | 半段內 URL count = 1 才是正常單一 URL 格式，count ≥ 2 才叫真重複 |
| 看到 body.innerText 同一 slug count ≥ 2 | 先去看「半段內」是怎麼回事，多半是 UI 重複列出，先別寫複雜刪除腳本 |
| 要從 content_library 抓 permalink | 別浪費時間，content_library 的策展貼文 permalink 在 body DOM 裡幾乎抓不到，改去 timeline/post 單頁才能拿 |

**關聯**：
- [[feedback_simply_scan_size_first_2026-09-18]] — 這個假象讓我寫了 v2/v3 兩版複雜判斷腳本，第一步就應該做最簡掃描確認「真的有錯的」=幾則
- [[feedback_never_click_action_buttons_on_thirdparty_systems_2026-08-28]] — 複雜假象+想要趕快做事會讓人手滑去點「⋯」→「刪除」，在第三方系統絕不點送出
