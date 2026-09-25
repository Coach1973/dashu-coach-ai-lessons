---
name: engineering-verification-discipline
description: Discipline for multi-step engineering/coding tasks — state assumptions before touching code, build a real feedback loop before declaring "done", touch only what the task requires. Use when implementing a feature, fixing a bug, or before reporting any task as complete to 教練.
---

# 工程驗證紀律

來源：研究 mattpocock/skills（`diagnosing-bugs`/`tdd`/`code-review` 的核心精神）＋執行細則 N2/N4/N7（原E13~E15，Karpathy 原則）＋試金石案例51/52/53與coach888拖拉排序bug的共同根因。

四個案例根因完全相同：**用簡化/間接的驗證方法就自信回報完成，沒有走到真實使用者路徑或真相源。** 這個skill就是為了堵住這個洞。

## 第一步：動手前先說出假設（執行細則 N2）

- 動手前把自己的假設寫出來，不默默照猜的做
- 有多種解讀而且會改變結果，才把選項列給教練；不影響結果的，自己選一個做並一行交代（要問教練前先過 N2 三關）
- 若存在更簡單的解法，說出來，敢於提異議
- 困惑時先自己查（N3）；查了還是只有教練能回答，才問，不假裝懂了就衝

## 第二步：把任務轉成可驗證目標（執行細則 N4）

開工前先講清楚「執行 X 之後結果是 Y」，不說「讓它能用」。多步驟任務先列「步驟→驗證方式」。

## 第三步：建立一個「真的會抓到這個問題」的驗證迴圈（本skill核心，對應mattpocock diagnosing-bugs Phase 1）

回報完成前，必須有一個**紅色可觸發**的驗證方法——一個你已經實際跑過、能在這個問題真的存在時顯示失敗的檢查。不是「邏輯上看起來對」，是「跑過一次，看到它抓到問題」。

### 血淚教訓：驗證要驗證「操作路徑」，不能只驗證「程式邏輯」

- **coach888拖拉排序bug**：用`dispatchEvent(new Event(...))`直接觸發事件、繞過瀏覽器真實拖放判定機制，誤判「已測試通過」，教練一用就失敗（HTML5 draggable跟內部`<a href>`搶主導權）。**修復後標準**：涉及使用者互動（拖拉/點擊/輸入）的功能，一定要用真實事件序列模擬（mousedown→mousemove→mouseup，或帶DataTransfer的DragEvent），不能只呼叫自己寫的處理函式。

### 血淚教訓：查證要查到最底層/最原始的真相源，不能只查看得到的第一層

- **案例51（Zoom junction誤刪）**：只查資料夾底下子項目有沒有被連結，沒查資料夾本身的ReparsePoint狀態——junction一旦設在上層，底下內容透明重導向後看起來完全正常。教練提出的假設是對的，我一次不完整的查證就否定掉，導致教練基於錯誤回報做決定、誤刪正牌資料。
- **案例52（三機總結誤報連續11天無對話）**、**案例53（HEARTBEAT假旗標憋住5.5天）**：判斷邏輯依賴一個從未真正運作/從未復驗的中繼檔案或衍生旗標，沒有交叉比對更直接可靠、成本極低就能實測的真相源（git log、API實測getMe/getChat）。

**規則**：任何「這個東西是否連結/是否有效/是否活著/是否發生過」的判斷，優先用能直接驗證的真相源（本身狀態、API實測、git log），不要依賴間接、可能斷鏈的中繼資料；「檔案不存在」≠「事件沒發生」，可能只是記錄管線本身沒接上。

## 第四步：只碰必要的，只清自己的亂（執行細則 N7）

- 不順手改旁邊沒被要求的、不重構沒壞的、維持原有風格
- 自己這次改動產生的孤兒（無用import/變數/函式）必須清掉；改動前就存在的死程式碼，只提不動
- 每一行改動都要能追溯到教練的需求

## 完成判定

四步都做到才算「完成」：假設說出來了、目標可驗證、驗證迴圈真的跑過且會抓到問題、改動範圍乾淨。缺一個都不能回報「done」。
