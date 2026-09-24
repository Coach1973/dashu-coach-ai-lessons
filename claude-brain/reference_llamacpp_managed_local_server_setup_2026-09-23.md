---
name: llamacpp-managed-local-server-setup
description: OpenClaw本機語意記憶搜尋(embedding)失效10+小時的完整修復SOP，關鍵是openclaw configure互動精靈選「Managed local server」而非預設的「Existing llama-server」
metadata:
  node_type: memory
  type: reference
  originSessionId: 055522b8-9175-4e6b-8d08-d83e98515a06
  modified: 2026-09-23T06:01:18.218Z
---

2026-09-23全面體檢發現：`openclaw doctor`跟`openclaw memory index`長期回報「embedding provider "local" is configured but unavailable」，本機語意搜尋(供memory-core的dreaming/consolidation功能用)已連續失敗10+小時無人發現。

## 根因與修復步驟（缺一不可）
1. **外掛版本落後**：`llama-cpp`外掛版本(2026.6.33)落後gateway核心(2026.9.4)——先跑`openclaw plugins update @openclaw/llama-cpp-provider@2026.9.4 && openclaw gateway restart`，但**光這樣還是不會好**
2. **管理伺服器從未註冊**：真正卡住的是`openclaw configure`互動精靈裡的一個關鍵分岔，路徑：`openclaw configure --section model` → Model/auth provider選「**Local llama.cpp**」→ Local llama.cpp auth method時**必須選「Managed local server」**（精靈預設反白的是「Existing llama-server」，這個假設你已經有外部伺服器在跑，選了它整條路就死路一條，這正是這次卡住幾小時的關鍵）→ 接著會問「Install a verified METAL llama.cpp server...download only the local embedding model (about 0.3 GB)? Your chat model will stay unchanged.」選**Yes**
3. `openclaw configure --section plugins`裡的「OpenClaw Memory」(memory-core外掛本身)選項**不是**這個問題的解法，那裡只管dreaming排程等設定，跟這次的embedding server無關，別浪費時間繞去那裡

## 這個互動精靈無法用expect/自動化腳本盲操
試過打字進搜尋框(一次性/逐字慢速)、方向鍵導航，`log_file`截圖都顯示輸入完全沒進到程式裡（畫面停在初始狀態），懷疑是這套TUI框架的raw-mode輸入機制跟expect的pty不相容。**這一步只能請教練本人在終端機前手動跑**，AI無法代勞（不違反守則#12，是真的做不到，已充分嘗試）。

## 驗證方式（缺一不算真的修好）
```
openclaw capability embedding create --provider local --text "測試" --json   # 應回傳真實向量數字，不是錯誤訊息
openclaw memory index                                                        # 應顯示每個agent「N files indexed」且exit code 0
```
2026-09-23實測：main 538個、kong 425個、peipei 435個、bni_tainan 242個、jiaolian_thoughts 231個檔案全部索引成功。

## 影響範圍評估（供未來判斷優先度）
這個功能壞掉完全不影響小龍蝦/LINE/Telegram/報名系統等核心運作，只影響memory-core的「dreaming」背景記憶整理品質（各agent的DREAMS.md日記）。下次如果又復發，可以先判斷「有沒有影響核心功能」再決定要不要立刻修。
