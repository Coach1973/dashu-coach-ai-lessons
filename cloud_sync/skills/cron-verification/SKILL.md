---
name: cron-verification
description: Use whenever creating, editing, or relying on a scheduled/cron job. The same operation that creates a cron must also create and verify the underlying script actually runs — test immediately, don't assume.
---

# 自動化鐵律：Cron 驗證（執行細則 N5）

對應守則 #05（凡走過必留痕跡）、#08（花時間討論就是為了執行）。

## 規則

- **先問能不能事件觸發**：這件事發生的當下能不能直接觸發（hook／launchd WatchPaths／webhook）？能就不要用定時排程。真的只能排程時，在回覆裡寫明「事件觸發不可行，因為XXX」
- 建立 cron 的同一個操作，必須同步建立腳本並驗證能跑
- 設定完立即測試一次，不要等下次自動觸發才發現壞掉
- 每週檢查 cron log 確認沒有 fail
- 發現 cron 在跑但腳本不存在——馬上補上，不等

## 血淚教訓：「手動測過一次成功」≠「已經真正上線」

- **案例50（VPS polling stale state）**：機制存在但實際運作有斷點
- **案例52（三機總結誤報連續11天無對話）**：`distill_and_push_{acer,lenovo}` 這套中繼蒸餾機制，設計時預想「先在ACER/聯想端排程執行→蒸餾當天memory→推回Mac」，但ACER端從建立以來**從未真正被排程執行過**，聯想端**只手動跑過一次**——判斷邏輯卻把「這個從未穩定運作的中繼檔案存不存在」當成唯一真相源，直接誤報。

**規則**：跨機排程（尤其依賴ACER/聯想/VPS端自己觸發的），光「這台機器手動跑成功一次」不算數，必須確認排程真的被註冊進該機器的系統排程器（Task Scheduler/launchd/cron），並且觀察至少一個排程週期真的自動觸發過，才能認定「已上線」。

## 完成判定

- [ ] 腳本存在且可執行
- [ ] cron/schtasks/launchd 已註冊
- [ ] 立即手動觸發一次，確認產出正確
- [ ] （跨機排程）確認在目標機器上真的被排程器接管，不是只在這台機器測過
