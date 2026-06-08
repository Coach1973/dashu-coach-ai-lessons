# 軍師接力棒 · 2026-06-08 晚（Sonnet 4.6 終端機 session）

> 建立時間：2026-06-08
> 上一棒：Sonnet 4.6 04:20
> 本棒執行者：Sonnet 4.6

---

## ✅ 本場完成

### 任務：ByeType 語音輸入 App 完整設定 ✅

教練下載 ByeType，從零開始排查到全部正常。

#### 解決的問題（按順序）

1. **快捷鍵格式** — 找出 modifier-only hotkey 正確 JSON 格式（無 `key` 欄位），Left Ctrl 設定成功
2. **三項權限** — 麥克風、輔助使用（Accessibility）、輸入監控（Input Monitoring）全部用 `tccutil reset` 重設後重新授權
3. **本地模型篩選**：
   - Breeze-ASR-25（2.9 GB）：WhisperKit 引擎與 ByeType 整合有 bug，無輸出 → 刪除
   - Parakeet TDT v3（469 MB）：英文專用，無法輸出中文 → 刪除
   - **Qwen3-ASR-0.6B**：FluidAudio 引擎，正常運作 → 保留
   - 合計釋放 **3.4 GB**
4. **雲端 Groq**：舊 key `gsk_ROTNPn...` 已失效，申請新 key 後更新到 Keychain（`security add-generic-password -U`），雲端轉錄正常
5. **雙擊免持模式**：教練自行在 UI 找到設定，問題自行解決

#### 最終狀態
- 本地模式：Qwen3-ASR-0.6B ✅
- 雲端模式：Groq whisper-large-v3-turbo ✅（新 key，免費 2000 次/天）
- 快捷鍵：keypadDecimal（數字鍵盤小數點）
- AI 增強：目前關閉（教練未要求開啟）

---

## 🪞 本場教訓

1. **ByeType 錯誤訊息誤導**：API key 失效 → ByeType 顯示「No speech detected」而非 API 錯誤，導致排查方向走歪（以為是麥克風/Whisper 問題）
2. **兩套引擎共存**：ByeType 內有 WhisperKit（Breeze-ASR-25）和 FluidAudio（Qwen3、Parakeet）兩套引擎，WhisperKit 整合目前有問題
3. **推測當成結論**：Breeze-ASR-25 不能用的原因，第一次給了 `zh-Hant` token 的推測解釋，被教練正確挑戰。正確答案是引擎整合問題，非模型本身的問題

---

## 📝 給下一棒

### 待做（從上一棒繼承，尚未處理）
- 🔴 **Netlify 部署鐵律 Stop Hook**——偵測 git push + netlify 組合 → 攔截（PreToolUse Hook）

### ByeType 後續可選
- AI 增強功能可開啟（設定檔 `aiEnhanceEnabled: false` → `true`），效果類似 Typeless 整理口語
- 若教練想試 Breeze-ASR-25，可用 TypeWhisper（免費開源，支援 WhisperKit 自訂模型）

**最後更新：2026-06-08（Sonnet 4.6 終端機 session）**
