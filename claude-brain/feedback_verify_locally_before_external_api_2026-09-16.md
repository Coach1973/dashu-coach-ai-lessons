---
name: feedback-verify-locally-before-external-api
description: 驗證「服務是否正常」要先查本機process/log，其次才輪到外部官方API，不能先打外部API當第一步；回報「已修好」前驗證強度要對得上真實使用情境
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 56b9f8ed-5dc0-425a-a86f-82908e70377e
  modified: 2026-09-15T18:51:59.341Z
---

2026-09-16三個LINE帳號斷線事故排查時，教練當場糾正：「所有的密鑰都在路徑大全，怎麼會直接查詢line官方，這不是繞遠嗎？」——查證順序錯了，先跳去打LINE官方API找答案，而不是先查本機已有的log/文件。

**正確順序（教練親定）**：
1. 先查本機process/log（`ps`、`launchctl list`、`/tmp/openclaw/openclaw-<date>.log`這個比`Library/Logs/openclaw/gateway.log`更詳細的per-session log）
2. 本機資料查不到答案，才考慮外部官方API（如LINE的`webhook/endpoint`/`webhook/test`）
3. 不要一開始就往外部查，尤其教練已經在`路徑大全`裡準備好本機能查到的資料時

**同一事故裡另外兩次「回報已修好」被打臉的教訓**：
- 第一次：只測了一個巧合也回應同樣狀態碼、但其實完全不相關的網址（`event.bymyway.com`是另一個LINE帳號在用），就當「webhook正常」回報教練，結果教練實測完全沒反應
- 第二次：重啟gateway清空殘留狀態後，只憑「应该清乾淨了」就叫教練重新測試，沒有自己先驗證過就開口，教練回「沒反應，連已讀都沒有」

**Why**：教練的時間跟信任都很寶貴，每一次「已修好」卻被戳破，都在消耗這兩樣東西。查證方法本身要對，不能因為外部API「感覺比較權威」就跳過本機資源直接打。

**How to apply**：任何「服務/帳號是否正常」的排查，開口說「已修好」之前，先自問——①我查過本機log了嗎（不只process alive，要查真的有沒有處理過真實流量的痕跡）②我的驗證方式反映的是教練實際會遇到的情境嗎（真人傳真訊息、等它跑完），還是只是一個容易造假通過的弱測試（隨便一個curl狀態碼）？兩者都答「是」才能回報教練。

相關：[[reference_line_plugin_extensions_missing_2026-09-16]]（同一事故完整技術記錄）、[[feedback_verify_before_correcting_coach]]、[[feedback_self_verify_before_directing_user]]
