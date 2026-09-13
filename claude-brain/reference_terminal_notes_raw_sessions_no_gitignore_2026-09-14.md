---
name: terminal-notes-raw-sessions-no-gitignore
description: terminal-notes/raw_sessions/243個原始逐字稿檔案完全沒有.gitignore保護，全部進版控，是金鑰重複外洩的源頭
metadata:
  type: reference
---

# terminal-notes/raw_sessions/ 結構性缺口：243個原始逐字稿零保護，是金鑰反覆外洩的源頭（2026-09-14）

## 發現經過
處理小二Telegram token第三度洩漏時查證發現：`.gitignore`完全沒有排除`terminal-notes/`，`git ls-files terminal-notes/raw_sessions/`回傳243個已追蹤檔案。這些是**原始、未加工的逐字稿**（相對於`distill/`是蒸餾後的摘要），任何對話中貼出的密碼/金鑰/Token都會被完整原文寫進這裡並進git版控。

查證發現至少2個舊檔（`11a2e6f7-...jsonl`10筆、`c23aa475-...jsonl`20筆）已經在**先前的commit裡**留有小二Telegram token明文，是之前兩次「緊急遮蔽」都沒掃到的漏網之魚——那兩次只查了`distill/`+`memory/verbatim/`+`state/inbound_echo/`等「加工過」的已知風險資料夾，沒查到這個存放原始逐字稿的資料夾。

## 為什麼會反覆發生
`distill/terminal_YYYY-MM-DD.md`這類蒸餾檔，是某個自動化腳本**從`terminal-notes/raw_sessions/`原始逐字稿重新產生**的。就算把蒸餾檔裡的金鑰遮蔽掉，只要原始逐字稿本身還留著明文、腳本又重新跑一次蒸餾，遮蔽過的內容就會被覆蓋回明文——這解釋了為什麼同一組token今晚在同一個晚上洩漏了三次。**只清蒸餾後的衍生檔案，不清原始來源，等於治標不治本。**

## 尚未解決（待教練裁示）
1. 這兩個舊檔裡已經commit過的30筆明文token——當下處理方式是建議直接把小二的Telegram token輪替第三次（token本身作廢，歷史裡的明文就不再是風險），而非改寫git歷史（risk較高，這個repo有教練/聯想/ACER/Hermes多台機器同步拉取，force-push可能造成衝突）。
2. 更根本的源頭修復：`terminal-notes/raw_sessions/`要不要整批加進`.gitignore`（只保留本機不上雲，蒸餾檔`distill/`才進版控）？還是要做一個「寫入前先脫敏」的前處理層？這是架構層級的決定，尚未跟教練討論定案。

## 悟到什麼
1. **查證「有沒有清乾淨」時，要往上游追到「這份衍生檔案是從哪裡重新產生的」，不能只查衍生檔案本身**——衍生檔案清乾淨了，如果生成它的原始來源沒清，下一次自動化流程重跑就會把污染帶回來。
2. **「已知風險資料夾」清單本身可能不完整**——這是今晚同一個晚上第二次犯這個模式的錯（第一次是verbatim/vs一般memory日誌，這次是distill/衍生檔vs terminal-notes/原始來源），下次查證「有沒有敏感資料殘留」，優先假設清單本身可能有漏，先問「這份資料的上游來源是什麼」再決定查證範圍。

## 相關
- [[feedback_scan_full_context_not_just_known_risk_folder_2026-09-13]]（同一晚第一次發現的同類模式，此案例是第二次發作，範圍更廣）
- [[reference_openclaw2_heartbeat_message_failed_bug_2026-09-14]]（本次發現的觸發任務背景）
