# 軍師接力棒 · 2026-06-08 晚 v2（Sonnet 4.6 終端機 session）

> 建立時間：2026-06-08 晚
> 上一棒：Sonnet 4.6 04:20
> 本棒執行者：Sonnet 4.6

---

## ✅ 本場完成

### 任務一：ByeType 語音輸入 App 完整設定 ✅

1. **快捷鍵** — keypadDecimal（數字鍵盤小數點），modifier-only 正確 JSON 格式
2. **三項權限** — 麥克風、Accessibility、Input Monitoring 全部授權
3. **本地模型** — Qwen3-ASR-0.6B 正常，Breeze-ASR-25（2.9G）+ Parakeet（469M）刪除，釋放 3.4 GB
4. **雲端 Groq** — 舊 key 失效，新 key 更新到 Keychain，免費 2000 次/天
5. **波形顯示** — `localStreamingEnabled` 改為 `true`，重啟 ByeType 後應出現波形
6. **雙擊免持模式** — 教練自行在 UI 找到設定

#### 最終狀態
- 本地：Qwen3-ASR-0.6B ✅
- 雲端：Groq whisper-large-v3-turbo ✅
- AI 增強：關閉（未要求開啟）
- 選單列圖示：ByeType 無法隱藏（App 內建限制，無解）

### 任務二：OpenWhispr 移除 ✅
- `/Applications/OpenWhispr.app` + 所有快取/設定全部刪除
- 原因：功能與 ByeType 重疊，同時開啟會互搶麥克風

---

## 🪞 本場教訓

1. **ByeType 錯誤訊息誤導**：API key 失效 → 顯示「No speech detected」，害排查走錯方向
2. **推測當成結論**：Breeze-ASR-25 失效原因第一次給錯解釋，被教練挑戰後才找到正確答案（WhisperKit 引擎整合問題）
3. **截圖規則**：教練再次提醒不截圖，已記錄在 memory

---

## 📝 給下一棒

### 待做
- 🔴 **Netlify 部署鐵律 Stop Hook**——PreToolUse Hook 偵測 git push + netlify 組合攔截

### ByeType 後續可選
- AI 增強功能（`aiEnhanceEnabled: false` → `true`），效果類似 Typeless 整理口語
- 若想試 Breeze-ASR-25，用 TypeWhisper（免費開源，支援 WhisperKit 自訂模型）

**最後更新：2026-06-08 晚 v2（Sonnet 4.6）**
