---
name: feedback-gateway-migration-flag-not-truly-cleared-2026-09-22
description: 案例79的「workspace migration」旗標doctor --fix+gateway start只是讓process跑起來，底層旗標沒真的清除，下次重啟(gateway restart)會重新炸開，教練在旁沒先確認就重啟連Telegram一起斷線
metadata:
  type: feedback
---

# Gateway workspace migration旗標：doctor --fix只是繞過，沒有真的修好

## 事件

09/21 07:36案例79：gateway因「Legacy workspace setup state requires migration」重啟失敗被launchd停放，
09/22 09:50用`openclaw doctor --fix`+`openclaw gateway start`修復，process重新跑起來，
Telegram整天正常，看起來已解決。

**但09/22 22:44軍師（未經教練確認）執行`openclaw gateway restart`測試LINE問題時，
同一個「Legacy workspace setup state requires migration」錯誤再次出現**——這次連
一起正常運作中的Telegram也被拖下線（restart是全通道性的，不是只重啟LINE）。

## 根因

`openclaw doctor --fix`當時只是繞過了這個檢查讓process能啟動，**沒有真正完成底層
workspace migration**，這個「legacy」旗標持續潛伏，只要gateway做一次完整restart
（不只是process意外死掉重啟，是主動執行restart指令）就會重新命中，再次要求
`doctor --fix`才能重新啟動。

## 教訓

1. **`openclaw doctor --fix`不是萬靈丹**——它能讓process重新跑起來，但不保證問題
   的底層狀態真的被清乾淨，同一個坑會在下次「主動restart」時原封不動再跳一次
2. **`openclaw gateway restart`是全通道性的重砲動作**——會影響Telegram/LINE/所有channel，
   不是針對單一channel的輕量修復。診斷LINE問題時直覺想「重啟看看」，要先想清楚
   這會不會連累正常運作中的其他通道，動手前跟教練確認影響範圍
3. **判斷「這次故障是不是我造成的」要查持久化log**（`~/Library/Logs/openclaw/gateway.log`，
   不是每天重置的`/tmp/openclaw/`那份），才能拉出跨日的完整時間軸，不能只看當天log
   就下結論說「這是全新問題」或「這是舊問題」

## How to apply

- 下次再撞到「Legacy workspace setup state requires migration」，別再只當成一次性事件處理，
  這個旗標本身沒被根治，可能要去查openclaw官方文件/issue是否有真正清除這個legacy狀態的
  正確流程（不只是doctor --fix這個繞過方案）
- 任何要對gateway做`restart`（不是單純process掛掉後的`start`）的操作，先確認當下有沒有
  正常運作中的通道會被波及，操作前跟教練說一聲，不要先斬後奏

## 相關

- 案例79（[[feedback_xiaolongxia_vs_hermes_different_systems_2026-09-22]]附近的接力棒記錄）
