---
name: feedback-xiaolongxia-vs-hermes-different-systems-2026-09-22
description: 教練口中「小龍蝦」指OpenClaw本身的main agent gateway(ai.openclaw.gateway/bot_main)，跟「Hermes」(ai.hermes.gateway/「Hermes特助(mac)」)是這台Mac上兩套完全獨立、平行存在的Telegram bot系統，故障診斷前要先確認教練指的是哪個對話框顯示名稱，不能憑印象套用上次查過的系統
metadata:
  node_type: memory
  type: feedback
  originSessionId: bd49abcb-5f4a-4574-9e5d-4772a5ef12a2
  modified: 2026-09-30T11:59:18.385Z
---

# 「小龍蝦」跟「Hermes」是這台Mac上兩套完全不同的Telegram bot系統

2026-09-22教練問「小龍蝦為何沒有反應」，軍師一開始把「Hermes」（第三方
系統，bot顯示名「Hermes特助(mac)」，靠`ai.hermes.gateway`這個launchd
服務運作）當成教練口中的「小龍蝦」去診斷、重啟，查了將近一小時的log、
webhook conflict、Telegram API，結果全部查錯方向。教練後來直接點破
「小龍蝦沒反應，Hermes那邊可以」，才驚覺這是兩個完全獨立、互不相干的
系統：

1. **「小龍蝦」= OpenClaw本身的main agent gateway**（`ai.openclaw.gateway`，
   服務`openclaw.json`裡的`bot_main`帳號）
2. **「Hermes」= 第三方系統，桌面版場景的技術後端**（`ai.hermes.gateway`，
   bot顯示名「Hermes特助(mac)」）

兩者各自有自己的launchd服務標籤、log路徑（`~/Library/Logs/openclaw/
gateway.log` vs `~/.hermes/logs/gateway.log`）、bot token、Telegram
聊天視窗。教練會用「小龍蝦」統稱「那個在Telegram上聽我說話的AI」，
但底層可能是不同process，不能憑印象套用「上次查過的那個」。

## Why 這條很重要

這次因為查錯對象浪費了大量時間，真正的根因（`ai.openclaw.gateway`
被launchd停放、process完全沒在跑）遲遲沒被找到，教練連續3天完全
聯絡不到小龍蝦的窘境又多拖了將近一小時才開始真正修復。這是繼
[[feedback_hermes_gateway_vs_desktop_app_distinction_2026-09-19]]
之後，同一個「Hermes」相關的身份混淆問題第二次發生，但方向相反：
上次是把該分開的東西誤當成一體「關掉」（全部釋放誤斷線16小時），
這次是把該分開的東西誤當成一體去「診斷」。

## How to apply

- 教練說「小龍蝦/赫米斯/XX沒反應」時，第一步先問清楚：是哪個
  Telegram對話框、顯示名稱是什麼——不要直接假設是上次查過的那個系統。
- 這台Mac上至少有兩套獨立Telegram agent：`ai.openclaw.gateway`
  （小龍蝦本尊）跟`ai.hermes.gateway`（Hermes）。診斷任一個故障前，
  先用`launchctl print gui/<uid>/<label>`確認是在查哪一個服務。
- 診斷「AI沒反應」類故障，第一層要先確認process本身有沒有在跑
  （`state`是否為`running`），不要跳過這層直接假設process活著只是
  卡住——這次真正的根因就是process根本沒在跑，被launchd安靜地停放，
  比process crash更隱蔽，一般的「process exists」檢查也不容易抓到。

## 2026-09-30 第三次搞混：接力棒把Hermes發起的任務寫成「小龍蝦已派給軍師」

教練先在Hermes桌面版跟Hermes討論sincere.bymyway.com更新，19:49教練對
Hermes說「你寫一封信給軍師」；教練同時把同一段文字貼進小龍蝦Telegram
（19:50）。小龍蝦看到自己Telegram收到這段文字，誤以為是自己主動發起，
寫進接力棒「小龍蝦已派給軍師的任務」。軍師開工時雖然同時讀到案例93後
新增的「第5.5步：原始對話digest」（裡面就有Hermes那句「你寫一封信給
軍師」的原文），卻沒有拿去跟接力棒的paraphrase交叉比對，直接照抄
「小龍蝦已派給軍師」回報，教練當場點破才發現搞錯。

機制本身沒壞——第5.5步的原始digest是對的、就攤在眼前，問題出在軍師
拿到「paraphrase版接力棒」跟「原始digest」兩份資料時，沒有主動比對
兩者是否一致就照抄了paraphrase。

## How to apply（追加）

- 接力棒裡任何「XX已派給軍師的任務／XX發現／XX交辦」這類轉述句，
  開工時要跟同一次注入的「第5.5步原始對話digest」交叉核對是誰在跟
  教練對話、誰被指名去寫信——兩者衝突時，**原始對話digest優先**，
  paraphrase可能是轉述者（通常是小龍蝦寫接力棒時）自己以為的版本。
- 這是同一組「小龍蝦vs Hermes身份混淆」的第三次案例，跟前兩次的差異：
  前兩次是操作/診斷對象搞錯，這次是「轉述任務來源」搞錯。

## 相關

- [[feedback_hermes_gateway_vs_desktop_app_distinction_2026-09-19]]
  （同樣是「Hermes相關」的身份混淆，但方向相反：那次是該分開的東西
  被誤當成一體關掉，這次是該分開的東西被誤當成一體去診斷）
- 試金石案例79（完整事故記錄：根因/修復/防呆機制）
