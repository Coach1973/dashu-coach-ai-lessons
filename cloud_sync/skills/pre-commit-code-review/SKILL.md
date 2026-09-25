---
name: pre-commit-code-review
description: Use before committing non-trivial code changes (new features, bug fixes, interactive UI) to a project repo. Two-axis check — Standards (matches this repo's own conventions) and Spec (actually does what 教練 asked, verified via a real usage path).
---

# Commit 前雙軸品質關卡

來源：研究 mattpocock/skills 的 `code-review`（Standards + Spec 雙軸），對應到我們的情境改寫。目的：在教練親自使用前，先攔住像coach888拖拉排序bug那種「commit了但教練一用就失敗」的狀況。

## 軸一：規範（Standards）

- 這次改動有沒有照這個專案既有的風格（縮排、命名、既有的CSS/JS慣例）？
- 有沒有動到沒被要求的地方（違反 N7「只碰必要的」）？
- 有沒有留下自己這次改動造成的孤兒（無用import/變數/函式/CSS class）？
- 有沒有引入不必要的新依賴/新框架，來解決一個原本簡單就能解決的問題？

## 軸二：需求（Spec）

- 這是不是教練真正要的？重讀一次教練的原始要求，逐條對照有沒有漏掉
- 用**真實使用者操作路徑**驗證過了嗎？（見`engineering-verification-discipline` skill——不能只呼叫自己的處理函式，要模擬真實滑鼠事件/真實API呼叫/真實瀏覽器操作）
- 如果是視覺變更，有沒有用截圖或瀏覽器親眼看過（見`image-visual-delivery-check` skill）？

## 執行方式

兩軸都要走過一遍才能commit。commit message要寫「驗證方法+結果」，不是只寫「fix bug」——例如「模擬真實滑鼠事件序列測試過組內排序/跨組移動/重整後保留三種情境」，讓下一個讀commit log的人（或自己）知道這個修復被驗證到什麼程度。

## 何時可以跳過

單純文字修改、純樣式微調（顏色/字級）、教練親口說「小改動不用這麼慎重」時可以簡化，但涉及使用者互動邏輯或資料處理的改動一律走完整流程。
