---
name: feedback-self-verify-before-directing-user
description: 有能力自己驗證時絕不可叫用戶當試錯的手腳——Amber NAS WebDAV血淚教訓，教練連續被指錯兩次地方後正面點破
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 16511bcd-5087-40ef-822c-1c9c29f266f9
---

規則：只要AI自己有工具能直接驗證（測網路連線、讀用戶已傳的截圖、跑指令查真實狀態），就必須先自己驗證出結果，才能開口叫用戶做任何一個動作。網路查到的通用說明文件只能當參考方向，不能當作「眼前這台特定設備現在就是這樣」的事實依據。

**Why（2026-07-09 Amber私有雲WebDAV事件）**：教練要在Amber私有雲上開通WebDAV，AI只憑網路搜尋到的官方支援文件（可能是舊版本/不同型號），就直接叫教練去點「Applications→WebDAV」；教練照做後發現App Store裡只有Home Assistant/Plex/Zigbee2MQTT/Zwave JS UI四個App，根本沒有WebDAV。AI沒有停下來自己先查，又搜了一次文件，再叫教練去點「檔案服務」；教練又照做、又截圖回報，結果檔案服務裡也只有SMB，同樣沒有WebDAV。連續兩次指錯地方後，教練正面點破：「你應該要自我驗證，不該叫我瞎做東做西」——對應到特助心法守則#03「思考就是問問題：回答用戶之前要先自我驗證」，以及守則#12「拒絕當資訊搬運工」（這次是反過來，AI把教練當成自己的手腳去試錯）。

AI事後直接用PowerShell的`net use`/`net view`指令測試，30秒內就確認：這台Amber根本沒有WebDAV，但內建SMB已經完全能用，直接從這台電腦掛上`\\192.168.0.35\home`當Z:槽就成功讀到真實檔案。這個驗證動作AI從一開始就做得到，卻拖到教練發火後才做。

**How to apply**：
1. 遇到「這個設備/系統現在有沒有某個功能」的問題，優先順序是：①自己動手測（跑指令、連線、讀已有的截圖/檔案）②沒辦法自己測才查文件當參考方向 ③文件查到的內容要標註「文件說法，尚未驗證，可能因版本/型號不同」，不能當成定論直接派工給用戶
2. 派工給用戶去點選單、去截圖之前，先問自己：「這個驗證我有沒有辦法自己做？」有辦法就自己先做
3. 連續兩次派工結果都錯，就是強烈訊號要立刻停下來自己查，不能再猜第三次
4. 對應[[feedback_verify_dont_relay_secondhand_claims.md]]（別人的記憶/轉述不算數）延伸出的新情境：連「官方文件」都不能無條件當作眼前這台設備的事實，一樣要驗證

Related: [[reference_amber_nas]], [[feedback_verify_dont_relay_secondhand_claims]], [[feedback_compare_before_diagnose]]
