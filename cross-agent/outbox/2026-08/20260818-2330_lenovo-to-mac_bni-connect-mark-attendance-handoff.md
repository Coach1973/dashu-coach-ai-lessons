# 聯想→Mac 交接：BNI Connect活動出席勾選任務，教練裁示改由Mac執行

> 時間：2026-08-18 23:30
> 寄件：聯想Windows Sonnet 5
> 收件：Mac桌面版/終端機
> 原因：教練判斷「以前不會像Windows電腦限制這麼多」，裁示改到Mac環境操作試試

## 背景

教練今晚交辦兩件事：①開立BNI培訓發票 ②訓練AI在BNI Connect系統裡標記活動出席名單（教練已手動勾過一部分，現在要教AI也會做）。①已進行到一半（見下方待辦），②卡在BNI Connect活動列表頁反覆碰到伺服器503錯誤+瀏覽器CDP逾時卡頁，教練裁示②改到Mac機器試試看。

## 任務②：BNI Connect活動出席勾選（教練原話SOP）

**操作路徑**：
1. 網址：`https://www.bniconnectglobal.com/web/secure/appsManageEvents`
2. 勾選「顯示一個月之前的活動」（checkbox id=`viewOlderEventsFlag`）
3. 顯示筆數建議選100（比較快）
4. 找到對應日期（例如2026年5月11日），系統活動列表會從2026年12月往前排，要往前翻頁找5~6月
5. 點選對應場次（例如「MSP初階」）
6. 點選「標記出席」，對照簽到表把有出席的人打勾
7. 若有人不在名單上（未登錄），點「增加出席者」，選對應分會+姓名，勾選出席
8. 最後按「提交」

**教練特別交代**：開錯/勾錯很麻煩，操作時務必多做確認再送出，不求快。

## 聯想這邊卡住的技術細節（Mac操作前建議先看）

- 頁面本身是**jQuery 1.4.2**的老舊系統，`viewOlderEventsFlag`這個checkbox用`.click()`(JS)可以正確勾上（跟真人點擊一致），但「查看活動」按鈕(`id=viewEvents`, `type=submit`, **不在`<form>`裡面**，也查不到jQuery `_data` events)用一般`.click()`或`computer`工具真人點擊都**沒有觸發任何AJAX**，最後改用`jQuery('#viewEvents').trigger('click')`才成功送出請求
- 送出後端點是`POST /web/secure/appsEventsManageViewEventsJson`，**連續兩次都回傳503**（服務暫時不可用），導致頁面一直顯示「未找到符合的記錄」。不確定是伺服器端本身暫時不穩，還是跟聯想這台的連線/擴充功能有關——**建議Mac先單純測一次這個查詢動作，看是否一樣503，藉此判斷是不是真的「Windows限制」問題，還是BNI Connect當下剛好在鬧脾氣**
- 同一場對話裡，這個頁面在等待fetch回應時也發生過一次`CDP sendCommand "Runtime.evaluate" timed out after 45000ms`（跟今晚稍早ezPay發票頁卡住的模式一樣），可能是原生對話框或長時間無回應的請求卡住JS執行緒，必要時用`navigate()`重新整理頁面可恢復

## 任務①：ezPay發票開立進度（供Mac參考，教練說明天再繼續，非緊急）

已完成：張騰文$1800發票已真正開立成功（DQ92662303，商店344031309大樹教育顧問有限公司，自訂編號081701），但**尚未補上Email通知**（ezPay session今晚已逾時登出，需教練重新登入才能繼續，這件事教練說明天處理，不急）。

18人已知名單（含Email，供直接開立用）+ 94人BNI大台南南區會員完整聯絡資料庫（Email/電話）已建好並推上雲端：
- `claude-brain/data/bni_region_members_contact_2026-08-18.csv`（94人memberId/姓名/分會/公司/Email/電話）
- `knowledges/2026-08-18_培訓發票開立_已知vs待問名單.md`（18人已知+38人待問+Email補齊對照表）
- `knowledges/2026-08-18_大台南南區4至8月培訓出席與開票總清冊_教練提供權威版.md`（59人完整出席明細，教練今晚提供的權威版清冊，取代較舊版本）

## 建議Mac開工時先讀

`JUNSHI_HANDOFF_LATEST.md`最新棒（v115聯想）+ 上述三個檔案，即可掌握完整脈絡，不用重新問教練。
