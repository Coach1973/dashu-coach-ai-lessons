---
name: reference-project-card-index-must-sync-new-systems-2026-09-07
description: 賈維斯接線員(project_card_router.sh)的INDEX.md沒有跟著新建系統同步更新，導致教練問真鑫/真鑽/真貴戰情儀表板時誤配到結繩領導學的專案卡
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9adaac71-1571-44a9-a4cf-32d7c105d2c4
  modified: 2026-09-06T20:07:14.238Z
---

新建一套獨立系統（repo/DB/網址）時，若沒有同步在`projects/INDEX.md`加一行、`projects/cards/`加一張卡，教練用口語提到這套系統時，`scripts/project_card_router.sh`（UserPromptSubmit hook，偵測關鍵字自動注入專案背景資料）就完全不會有這套系統的卡片可以注入——更糟的是，如果教練用的詞剛好跟別的系統共用（例如「戰報系統」同時被教練口語拿來稱呼結繩領導學的`rpl-workshop`跟真鑫/真鑽/真貴的來賓戰情儀表板），就會被誤配到錯的專案卡，讓AI用錯誤的背景資料理解教練的問題。

2026-09-07實際發生：教練問「戰報系統」（真鑫/真鑽/真貴分會的來賓/1對1/咖啡會議追蹤儀表板）時，因為`bni-guest-dashboards`這套系統(`zhenxin-guests`/`zhenzuan-guests`/`zhengui-guests`三個repo)從建立以來就沒有專案卡，`INDEX.md`裡「戰報系統」這個別名只掛在`jiesheng`(結繩領導學)底下，AI因此被自動注入了完全不相關的結繩領導學背景資料。

**Why**：專案卡索引是「事後才會發現缺漏」的機制——不會主動提醒「這套新系統忘了建卡」，只有教練真的問到、AI給出錯誤背景資料時才會暴露。共用詞彙(如「戰報系統」)的情況更陰險，因為不會報錯，只會安靜地選錯卡。

**How to apply**：
1. 建立任何新的獨立系統（新repo+新網址+新用途）時，動作清單要加上「`projects/cards/`新增一張卡 + `INDEX.md`新增一行」，跟寫SOP文件/寫commit message同一等級的必做事項，不是事後才補
2. 若一個別名（如「戰報系統」）教練確實會用在兩個不同系統上，**兩張卡都掛這個別名**，讓`MAX_CARDS=2`的機制同時注入兩張，AI用句子其餘內容自然消歧——不要只選一個「看起來比較對」的系統把別名搶走，那樣另一個系統永遠不會被正確識別
3. 懷疑AI理解錯教練口語提到的系統時，先查`projects/INDEX.md`有沒有這套系統的卡，而不是直接假設AI记憶力不好

Related: [[project_bymyway_dynamic_hosting_escape_netlify_2026-08-30]]（同樣是「新系統上線時要同步做一輪連動清單」的模式）
