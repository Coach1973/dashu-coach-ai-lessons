---
name: inputmethod-typeless-conflict-resolved
description: 2026-05-26 教練自行修復 Typeless 與無蝦米輸入法衝突問題
metadata:
  node_type: memory
  type: reference
  originSessionId: current
---

# Typeless 與無蝦米輸入法衝突修復（2026-05-26）

## 問題描述
- 無蝦米輸入法無法使用，切換也沒用，打出來都是英文
- Typeless 語音輸入後，按鍵被修飾鍵干擾

## 根因
- Typeless `pasteLastTranscript` 設定為 `Ctrl+Cmd+V`
- 每次語音辨識後，修飾鍵沒乾淨釋放
- 導致後續所有按鍵被 Ctrl+Cmd 修飾，變成快捷鍵

## 解決方案
**教練自行修復：解除 Typeless 的按鍵設定，只保留一個常用的快捷鍵**

## 結果
✅ 已解決

## 相關背景
- 無蝦米輸入法：嘸蝦米（`/Library/Input Methods/Boshiamy.app`）
- Typeless 版本：1.4.1
- 歷史參考：`reference_coach_input_method.md`（2026-05-22 記錄的 Ctrl+Cmd+V 問題）

## How to apply
- 未來若遇到 Typeless 與輸入法衝突，優先檢查 Typeless 的鍵盤快捷鍵設定
- 解除不必要的按鍵綁定，保留最少需求即可
