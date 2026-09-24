---
name: quanmian-scope-must-clarify
description: 教練說「全面改/全面體檢/全面X」時，範圍預設是「跟他當下對話的這個Claude」，不是所有系統(教練其他地方都用MiniMax)；動手前要跟教練確認範圍
metadata:
  node_type: memory
  type: feedback
  originSessionId: 055522b8-9175-4e6b-8d08-d83e98515a06
  modified: 2026-09-23T05:15:58.996Z
---

教練說「全面改」「全面體檢」這類涵蓋範圍不明的指令時，不要立刻回「好，全面改」就直接動手，先確認範圍是「這個對話框/這個系統」還是「跨所有系統」。

**Why:** 2026-09-23教練原話：「我叫你全面改，你問都不問我就立刻『好，全面改』，這不就是後遺症嗎？你都沒有想過，除了我們在對話的這個Claude以外，我其他全部都是用Minimax。我跟你講全面改，一定是在講Claude這件事情全面改。」教練指出這是「昨天已經討論過」的重複模式。背景：本次「全面改」指令牽連出agents/bni_tainan、agents/jiaolian_thoughts兩個子agent的人設/記憶檔曾經整批從git歷史消失（見[[reference_agents_directory_lost_from_git_history_2026-09-23]]），教練認為這類事故的根源就是過去「全面改」被誤解成跨系統的範圍過大執行，才會留下後遺症。

**How to apply:** 教練是多系統環境的使用者——這個對話框(Claude)、小龍蝦/Telegram/LINE(MiniMax)是分開的。聽到「全面」「所有」「整個系統」這類詞，先反問或至少在動手前想清楚：這次的「全面」是指「這個Claude能碰到的範圍」（本機檔案、git repo、這台Mac上的服務），還是真的要跨到MiniMax那些用OpenClaw跑的agent。範圍不確定就先問一句，不要用「反正都在同一句話裡提到」去擴大解讀。不過教練同一則訊息也強調「對的事該做就做」——這條不是要事事都問，是專指「全面/所有/整個」這種涵蓋範圍本身有歧義的情況，跟一般任務直接執行(守則#08)不衝突。
