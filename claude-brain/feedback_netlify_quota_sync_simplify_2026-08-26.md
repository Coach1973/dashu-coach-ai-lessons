---
name: feedback-netlify-quota-sync-simplify-2026-08-26
description: 教練糾正三機Netlify額度同步不用建自動化攔截hook，簡單記數+總結時寫回共用檔案就夠——過度工程化反而自我卡住
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4e652b8a-8bea-4bf1-bb10-68f6594c133b
  modified: 2026-08-27T02:19:06.334Z
---

聯想這台機器推部署完全沒被扣點過，跟Mac對不上帳，查出根因是Mac的`netlify_deploy_guard.sh`（PreToolUse攔截Bash指令，偵測到真實部署POST才自動扣點寫回`state/netlify_deploy_quota.json`）從沒被移植到聯想。第一反應是照抄Mac那套邏輯寫`netlify_deploy_guard.ps1`並註冊成PreToolUse hook——結果**這支hook本身因為BOM編碼問題直接把自己的下一個Bash指令攔到報錯**，卡住了整個對話（跟[[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]同一種「新寫的Windows hook沒先驗證編碼」的坑）。

教練當場糾正：「你這一次用了幾次之後，你就會總結上傳，軍師那邊讀到之後就會扣掉你這個用掉的次數，就這麼簡單啊！你要算那麼久，算什麼？」——直接點破我把一個「三機共用一個數字、定期同步就好」的問題，升級成「每個Bash指令都要即時精準攔截」的自動化系統，不必要地增加了複雜度跟自我卡住的風險。

**Why：** 教練的判斷標準很清楚——多機共享一個緩慢變動的狀態值（部署額度這種一天頂多變動幾次的東西），不需要為了「絕對即時、絕對精準」去接自動化攔截層。用「做完當下手動算一次＋收工（總結）時寫回共用檔案上雲端」這種輕量模式，其他機器下次git pull就拿到最新值，已經完全夠用，還不會有攔截邏輯寫錯卡住自己指令的風險。

**How to apply：** 下次遇到「三機/多機要對同一個數字同步」的需求，先問自己：這個數字變動頻率高不高？即時性真的重要嗎？如果答案是「不高/不重要」，優先選手動記數+總結時同步寫回，不要預設要建PreToolUse類自動化攔截hook。真的需要自動化時，任何新寫的Windows PowerShell hook上線前，先用ASCII-only debug probe或直接檢查BOM，避免編碼問題讓hook攔死自己的後續指令（同案例64/reference_lenovo_summary_hook_jq_missing_fixed教訓）。

相關：[[project_netlify_deploy_quota_2026-07]]（額度追蹤SOP主檔，教練先前已拍板「每7~10天校正一次」同樣是「別過度即時查證」的判斷邏輯）、[[reference_lenovo_summary_hook_jq_missing_fixed_2026-08-26]]（新Windows hook編碼坑同源）、[[project_lenovo_cross_machine_sync_4layer_rootcause_2026-08-26]]（本次發現guard從沒移植的原始脈絡）
