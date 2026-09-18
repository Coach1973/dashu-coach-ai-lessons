---
name: feedback_check_shared_resource_before_recommending_revoke
description: 建議撤銷/輪替任何憑證前，必須先查該憑證的實際使用範圍(路徑大全)，不能假設它只屬於眼前這個小任務——教練當場糾正「沒查証之前不要亂建議，時間很寶貴」
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c23aa475-6fb1-4f77-8a84-3e87c7916908
  modified: 2026-09-13T10:26:08.819Z
---

發現憑證洩漏、要建議教練撤銷/輪替時，先查`路徑大全_憑證層.md`或對應設定檔，確認這組憑證的**實際共用範圍**，不能因為「這次是在小二(單一測試環境)的脈絡下發現的」就假設它只屬於小二。

**Why**：2026-09-13訓練小二時發現小二的MiniMax API Key(`sk-cp-0_iW72...`)明文洩漏進git歷史，第一時間直接建議教練「撤銷或輪替這組key」，但查`路徑大全_憑證層.md`第89~108行才發現，這組key其實是**教練全部服務共用的唯一一組MiniMax訂閱帳號**(2026-08-26教練親口確認)——小龍蝦一代、BNI小幫手、教練都在想什麼、namecard-db、VPS小龍蝦全部共用同一組。若教練真的照建議去撤銷，會讓上述全部正式服務同時斷線，是我在沒查證前就給出的高風險錯誤建議。教練當場糾正：「沒查証之前，不要給我亂建議，我的時間很寶貴」。

**How to apply**：任何「建議撤銷/輪替/刪除某個憑證或設定」的話要出口前，先做兩件事：①查`路徑大全_憑證層.md`或`grep`該憑證的其他使用位置，確認它是「這個任務專屬」還是「跨系統共用」②共用的東西，撤銷前必須先列出「會被打斷的所有服務清單」給教練看，不能只講「這樣比較安全」就要教練照做。同一輪對話裡若已經因為類似原因給錯一次建議(如[[feedback_scan_full_context_not_just_known_risk_folder]])，代表要更謹慎，不要連續兩次在同一件事上因為沒查證而拖累教練時間。此案與[[feedback_diagnose_root_cause_before_trial_and_error]]、[[feedback_check_master_index_before_claiming_cant_find]]同屬「動手/建議前先查路徑大全」系列。
