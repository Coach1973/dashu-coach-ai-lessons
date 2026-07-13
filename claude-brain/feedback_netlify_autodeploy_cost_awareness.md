---
name: feedback-netlify-autodeploy-cost-awareness
description: 教練親口定義的網頁部署SOP——判斷準則是「這個站有沒有已經公開推廣給群眾」，不是「有沒有講到Netlify」
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2be4fc3d-0468-40ed-9dee-dd84f711a9f1
---

## 教練 2026-07-09 親口定義的完整邏輯

**判斷準則：這個網站是否已經公開推廣、丟出去給群眾點閱過？**

1. **已經公開推廣的網站**（例如「結繩領導學」jiesheng-leadership、「全球健康發展協會」northern-tw/northern411——⚠️2026-07-13教練糾正：這裡原本誤植成goeasy-ai，goeasy-ai其實是另一個不相關專案「AI一鍵起飛3小時實戰講座活動頁」，已修正）：
   - 這些網址是教練刻意公開給所有人用的，已經丟出去幾千個連結
   - **任何更新都必須直接推到 Netlify**，確保群眾點擊舊連結時看到最新內容——這是必要行為，不是要避免的成本
   - 只要沒有實際更新內容，Netlify 就不會扣點；有更新才推、推了才扣，這是正常、正確的使用方式，**不需要每次推送前都額外提醒扣點成本**

2. **內部測試中的網頁**（還沒公開發布、還在打磨階段）：
   - 一律先留在 GitHub 就好，不要推到 Netlify
   - 等教練明確要「推廣/上線」才轉為公開狀態並推 Netlify

## 我先前的誤判與更正

2026-07-09 這一晚做 invite-bni.html／invite-peipei.html 時，我一度以為「這個 repo 是 GitHub 自動部署型」本身就是需要提醒扣點成本的風險（見同名記憶舊版），但教練澄清：**jiesheng-leadership 本來就是已公開推廣的站，推 Netlify 是正確且必要的行為**，我先前那個「查到 provider:github 就要提醒」的判斷太粗糙，用錯了警戒對象。

真正該提醒/確認的時機，是**新建一個還沒公開過的頁面**（例如這次新增的 invite-bni.html／invite-peipei.html）——這種情況要先確認：這是要立刻公開推廣（該推 Netlify），還是還在內部測試階段（先留 GitHub 就好）。**不是看 repo 的技術設定，是看這個「頁面／網址」本身的推廣狀態。**

## 另一個相關教訓：新建頁面的網址長度

教練同一次也提到：當天新增的兩個網址（`jiesheng-leadership.netlify.app/invite-bni.html`、`.../invite-peipei.html`）「不是我想要的，不希望網址這麼長」。教練偏好簡短好記的獨立網址（參考他其他站台命名：bni-happy、bni-88888、bni-traffic 這種簡短獨立域名），而不是掛在既有長網域底下的長路徑。這不是急件（教練說「到時候我還得上去改，或者我再叫你改也行」），但下次新建要公開推廣的頁面時，應該主動考慮：是否該建一個簡短獨立的 Netlify site，而不是預設掛在既有 repo 底下用長路徑。

## How to apply
1. 新建一個頁面前，先判斷：這是要公開推廣的（推 Netlify）還是內部測試的（留 GitHub）？不確定就問教練。
2. 已經公開推廣的既有站台，改完內容正常推 Netlify，不需要每次都問或提醒扣點——這是教練要的正確行為。
3. 若新頁面確定要公開推廣，主動想一下網址要不要簡短獨立命名，而不是預設塞進既有長網域路徑。

相關：[[reference-netlify-token]]
