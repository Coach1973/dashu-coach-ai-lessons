---
name: feedback-hermes-gateway-vs-desktop-app-distinction-2026-09-19
description: "教練說「赫米斯」在不同語境指不同東西——「全部釋放」指令要關的是佔記憶體的桌面版GUI App，Telegram上24小時運作的是ai.hermes.gateway後端process，兩者絕不能混為一談，release_all_memory.sh曾經把兩者一起bootout導致教練Telegram斷線16小時完全不知情"
metadata:
  type: feedback
---

# 赫米斯有兩個不同的東西：桌面版GUI App（可以關）跟Telegram後端gateway（要24小時運作，絕對不能關）

`scripts/release_all_memory.sh`（教練說「全部釋放」時觸發，五個動作之一是
「關掉赫米斯」釋放記憶體）舊版本一次`launchctl bootout`四個launchd服務：
`ai.hermes.gateway`、`ai.hermes.menubar`、`ai.hermes.desktop`、
`ai.hermes.config-watcher`。2026-09-18教練下令「全部釋放」時，這四個
一起被關掉，其中`ai.hermes.gateway`（`python -m hermes_cli.main gateway`，
負責連線Telegram、處理教練在Telegram上跟赫米斯的所有對話）也被停掉，
**教練在Telegram上完全聯絡不到赫米斯長達16小時**，直到教練自己覺得不對勁
主動來問才發現。

更嚴重的是：`hermes_gateway_watchdog.sh`（每5分鐘檢查gateway有沒有卡住的
看門狗）在9/11修過一次bug後，把「launchd裡找不到這個服務」一律當成
「教練故意關閉，不用通知」直接安靜跳過——這16小時完全沒有任何提醒机制，
教練是自己想起來才發現。

## Why 這條很重要

教練親口糾正：「我讓你關掉的是蘋果電腦的『赫米斯』桌面版App，可是我
Telegram上面的那一個應該要24小時運作，你關它幹什麼？」——這句話點出
「赫米斯」這個詞在教練口中其實指兩個不同的東西：

1. **桌面版GUI App**（`Hermes.app`本體+選單列圖示+設定檔監看）——純本機
   互動介面，佔記憶體，教練說「全部釋放」時真正想關的就是這幾個。
2. **Telegram後端gateway**（`ai.hermes.gateway`）——24小時常駐、負責回應
   教練在Telegram上任何時候傳來的訊息，教練預期這個「絕對不會關」，
   跟他有沒有開著Mac桌面版App完全無關（他可能人不在電腦前，純粹用手機
   Telegram找赫米斯）。

這兩者在launchd層面剛好是四個獨立plist，容易被寫程式的人（過去的軍師）
用同一個迴圈全部bootout，因為表面上看起來「都叫赫米斯」，但教練心裡的
分類完全不同：一個是本機工具軟體，一個是24小時待命的服務。

## How to apply

- 任何要「關閉/重啟/操作赫米斯」的腳本或指令，先確認是要動**桌面版GUI**
  （`ai.hermes.desktop`/`ai.hermes.menubar`/`ai.hermes.config-watcher`）
  還是**Telegram後端**（`ai.hermes.gateway`）——預設**`ai.hermes.gateway`
  永遠不動**，除非教練明確講出「連Telegram也要關」這種明確指令。
- 已修復：`scripts/release_all_memory.sh`的bootout迴圈已拿掉
  `ai.hermes.gateway`，只保留三個GUI服務。
- 看門狗（`hermes_gateway_watchdog.sh`）目前的「找不到服務=故意關閉=
  不通知」邏輯本身沒有錯，錯的是「不該被關掉的服務被錯誤地歸類成可以
  被故意關掉」——根治重點在來源（哪個服務會被bootout），不是看門狗本身。

## 相關

- [[feedback_hermes_is_mac_desktop_vps_permanently_off]]（另一個Hermes身份誤判案例：VPS版vs Mac版，跟本案例是不同維度的混淆）
