# 軍師接力棒 · 2026-08-25 v131（Mac桌面版 Sonnet 5，AI微論壇台中場真正RWD根因修復+Netlify額度重新校正）

> 建立時間：2026-08-25 11:43 ~ 19:30（台灣時間）
> 上一棒：v130（同機同日中午）
> 本棒主軸：**教練轉達朋友回報「Android手機看講師簡介會切版」，先做的dvh修法教練確認沒有安卓機沒法驗證就先推了；朋友之後回報仍未改善並給出更具體的問題描述（報名方案9大主題手機版沒有垂直排列），重新深度查證找到兩個真正的bug並修復+驗證；過程中教練親自查真實Netlify帳單頁，糾正了本場一度過緊張的額度估算。**

## 🎯 本場戰果

### 1. ✅ AI微論壇台中場(ai-forum-taichung)兩處RWD bug真正修復
第一輪（朋友初次反應「Android看不到完整簡介」，教練本人沒有安卓機無法驗證，先推上線讓其他人測）：把講師簡介彈窗`max-height`從純`vh`改成`dvh`（動態視窗高度），這是常見的「Android網址列收起造成vh算錯」修法，GitHub Pages+Netlify皆已推送驗證(deploy`6a8d110f`)。

**朋友回報仍未改善**，教練轉達朋友給的具體prompt後重新查證，找到兩個跟第一輪修法完全不同的真bug：
- **主要bug**：「報名方案9大主題」區塊(`.price-wrap`)在HTML元素上寫了`style="grid-template-columns:1fr 1fr 1.1fr"`的inline style，inline style優先權高於CSS class，直接蓋掉了原本就寫好的`@media(max-width:860px){.price-wrap{grid-template-columns:1fr}}`手機垂直排列規則——不分Android/iOS，這個區塊在手機上永遠被硬擠成3欄。改法：拿掉inline style，桌面版3欄改用`@media(min-width:861px)`實現，讓860px以下的規則正常生效。
- **次要修復**：講師簡介彈窗改成不依賴任何vh/dvh視窗單位（dvh在LINE/FB等App內建瀏覽器支援不穩定），改用外層遮罩本身可捲動+彈窗不設高度上限的基礎機制，並修好關閉鍵會被捲出畫面的關聯缺陷（改用`position:fixed`釘住）。

**驗證方式**：截圖鎖擋下畫面截圖，改用DOM量測作為證據——375px寬(手機)量到`.price-wrap`是單一312px軌道、三個子項top值遞增(垂直堆疊)；1280px寬(桌面)量到三軌道(364/364/400px)、子項top值相同(並排)，兩種尺寸都正確。GitHub Pages(commit`455e599`+`d4b9650`)+Netlify(deploy`6a8d1a4e`)皆已curl驗證inline style清除、modal-close改fixed生效。

**下一步**：已請朋友（尤其原本回報有問題的那台Android機）重新實測，若還有問題請具體描述畫面或截圖。

### 2. 🔴🔴🔴 Netlify額度追蹤：本場一度緊張過頭，教練親自查證後修正
開場沿用v128留下的「僅剩7~9次」估算，推送兩次部署後估算降到7次，我因此在推送前主動問教練「要不要推」，語氣偏保守。**教練親自查真實帳單頁**回報983.4/1000——新的1000點週期已重置，證實估算過度悲觀（且我原本記錄的「下午3點重置」推算是錯的，教練查證時新週期其實在中午12:31前就已重置完畢）。已將真實數字寫回`state/netlify_deploy_quota.json`(約70次可用)，並更正記憶檔`project_netlify_deploy_quota_2026-07.md`裡的重置時間點推算錯誤，往後只知道「25日當天會重置」，不假設精確時刻。

## ⚠️ 本場教訓
1. **朋友給的技術prompt比籠統的「還是壞的」更好用**——教練轉達的具體描述（哪個區塊、要垂直呈現、Android/iOS都要符合）讓我能直接定位到真正的bug，第一輪的dvh修法其實是合理猜測但沒切中要害，第二輪才找到inline style覆蓋media query的真因。以後遇到「還沒修好」的回報，優先請教練問清楚具體是哪個畫面/區塊，比自己再猜一次更有效率。
2. **額度緊張是估算模型的滯後性，不是真實情況**——estimate-based tracking在剛好卡在重置邊界時最容易失真，教練親自查證的行為本身就示範了SOP設計的用意（7~10天校正一次），不需要每次都自己太緊張地問要不要推。

## 📋 下一場直接開工任務
- 等朋友（尤其Android機）確認這次修復是否真的解決問題
- Netlify額度下次校正約2026-09-01~09-04或估算值≤5次時提前查
- 承接v130 Q1：小龍蝦「總結」hook尚未實作（教練明確要求，方案已定見v130封存內容）
- 承接舊待辦：3支孤兒hook要不要啟用、bni-chapters「真誠分會」架構問題

## 🔑 本場關鍵檔案索引
- `/Users/bymyway/github_repos/ai-forum-taichung/index.html`：RWD兩處bug修復
- `state/netlify_deploy_quota.json`：額度重新校正為真實數字
- `~/.claude/projects/-Users-bymyway--openclaw/memory/project_netlify_deploy_quota_2026-07.md`：更正重置時間點推算錯誤
- commit：`27ad73e`+`455e599`+`d4b9650`(ai-forum-taichung GitHub)／`6a8d110f`+`6a8d1a4e`(Netlify deploy)／`86cb3101c`+`6983f896d`+`c58fc74c3`(workspace額度state)／`2beccc4db`(memory repo)
