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

---

## 🟢 22:53 更新：真正卡住LINE的根因找到了，是外掛版本落後，不是draining本身

上面記錄的「workspace migration旗標沒清乾淨」只解決了gateway整個掉線的問題（Telegram+LINE
一起斷），但gateway重新啟動後，**LINE三個帳號仍然卡在教練回報的「Sorry, I encountered an
error」**，Telegram正常。

用`openclaw gateway call health`直接查每個channel的lifecycle狀態，抓到真正病灶：
LINE三個帳號（default/bni_tainan/jiaolian_thoughts）全部卡在`"lifecycle": "starting"`，
永遠沒有變成`"ready"`（Telegram三個帳號都是`"ready"`）——外層看起來像「gateway is draining」
的錯誤訊息，其實是message-handler把「channel未就緒」跟「gateway真的在restart drain」共用
同一個`GatewayDrainingError`類別，訊息文字容易誤導人。

**真正根因**：`openclaw gateway status --deep`發現`line`外掛版本落後gateway核心三個小版本
（line: 2026.6.34 vs gateway核心2026.9.4），版本落差導致LINE provider初始化卡住，永遠
不會完成啟動。跟教練這邊完全無關，是gateway核心自動更新過但line外掛沒跟著更新造成的
純技術債。

**修復**：`openclaw plugins update line`（更新到2026.9.4，跟gateway對齊）→
`openclaw gateway restart` → 用health call複查確認三個LINE帳號lifecycle全部變成`ready`
→ 用簽章健檢腳本複測OK。

## How to apply（更新版）

診斷「某個channel收不到訊息但process活著」這類問題，不要只看process存活或HTTP回應碼，
**用`openclaw gateway call health`查該channel每個帳號的`lifecycle`欄位**，卡在`starting`
就是初始化沒完成，這時候第一個該查的是`openclaw gateway status --deep`看有沒有plugin
version drift，而不是急著重啟process（重啟版本沒對齊的外掛，只會卡在同樣的地方）。
