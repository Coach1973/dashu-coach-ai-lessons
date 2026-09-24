---
name: feedback-hermes-gateway-vs-desktop-app-distinction-2026-09-19
description: 【09-25教練定義】教練說「赫米斯」預設＝Mac桌面版Hermes.app(類似Claude的CLI UI，可接各家模型)，Telegram那條線不碰也不拿來當選項問；登入自動跳出已修(desktop.plist的SuccessfulExit隱含RunAtLoad)。原始事件：教練說「赫米斯」在不同語境指不同東西——「全部釋放」指令要關的是佔記憶體的桌面版GUI App，Telegram上24小時運作的是ai.hermes.gateway後端process，兩者絕不能混為一談，release_all_memory.sh曾經把兩者一起bootout導致教練Telegram斷線16小時完全不知情
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dfd3491-32da-49ec-be24-a2c0d54e850c
  modified: 2026-09-24T19:46:31.805Z
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

## 2026-09-25 第三次搞混（教練原話定義，以此為準）

教練：「Hermes 在 Mac 電腦裡面是一套跟 Claude 一樣的 CLI UI 程式……背後可以接 Claude、Minimax、OpenAI」「誰叫你關小龍蝦了？」
- **教練說「赫米斯」預設＝Mac 桌面版 `/Applications/Hermes.app`**。Telegram 那條線在教練心中歸「小龍蝦/Telegram 系統」（有 20MB 上限），除非教練明講，**不碰、也不拿來當選項問**。
- 這次我問「只關視窗 vs 連 Telegram 一起關」＝又把 Telegram 線端上桌，教練當場動怒。

**登入自動跳出的真正原因（已修）**：`~/Library/LaunchAgents/ai.hermes.desktop.plist` 寫 `RunAtLoad=false`，但 `KeepAlive` 裡有 `SuccessfulExit` —— launchd 規定這個鍵「隱含 RunAtLoad=true」，所以每次登入照樣執行 `open Hermes.app`（`launchctl print` 顯示 runs=1）。已改 `KeepAlive=false`，重新載入後 runs=0、App 不再自動開，原檔備份 `~/.hermes/ai.hermes.desktop.plist.bak-2026-09-25`。
- 我先前「macOS 登出記住視窗」的推論是錯的（TAL 清單根本沒有 Hermes）。教練一句「LINE、OpenCode、Telegram 都不會，為什麼 Hermes 會？」就推翻了——**只有單一 App 有怪行為時，先找那個 App 自己的啟動設定，不要推給全系統行為。**
- 看 launchd 有沒有在登入時跑某個 job：`launchctl print gui/$(id -u)/<label>` 看 `runs =`，比讀 plist 的 RunAtLoad 可靠。

## 相關

- [[feedback_hermes_is_mac_desktop_vps_permanently_off]]（另一個Hermes身份誤判案例：VPS版vs Mac版，跟本案例是不同維度的混淆）
