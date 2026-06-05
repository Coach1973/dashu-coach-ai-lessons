---
name: coach-input-method
description: 教練 2026-06-02 起改用鼠鬚管 Squirrel + RIME liur 嘸蝦米；OpenVanilla 與 Boshiamy 已完全卸載
metadata: 
  node_type: memory
  type: reference
  originSessionId: ddc5e99b-ea0c-43f0-8898-5b61266824c4
---

# 教練的輸入法（2026-06-02 重大升級）

> **教練現在用的中文輸入法：鼠鬚管 Squirrel + RIME `liur` 方案（嘸蝦米）。**
> 「liur」「liu7」「嘸蝦米」是同一個東西的不同寫法（liur = RIME 方案名 = 劉氏拆碼 liu7 = 嘸蝦米中文俗稱）。

## 現況（2026-06-02 23:15 起生效，教練實測「打的很順」）

| 項目 | 內容 |
|------|------|
| 主要輸入法 | 鼠鬚管 Squirrel + RIME `liur` 方案 |
| App | `/Library/Input Methods/Squirrel.app`（bundle `im.rime.inputmethod.Squirrel`，Hans/Hant 兩模式） |
| 設定檔 | `~/Library/Rime/`（12 個 yaml + opencc/） |
| 編譯產出 | `~/Library/Rime/build/`（含 `liur.extended.table.bin` 2.7MB 等字典 binary）|
| 字根源 | GitHub `hsuanyi-chou/rime-liur`（49 萬行完整字根） |
| 切換輸入法 | Ctrl+Space 或選單列輸入法圖示 |
| 重新部署 | `open -a Squirrel` → 選單列圖示 → 重新部署 |
| 命令列強制重建 | `"/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel" --build` |

## 已卸載（不要再說教練在用）

- ❌ **Boshiamy 嘸蝦米試用版**（`/Library/Input Methods/Boshiamy.app`）—— 2026-06-02 23:17 sudo 完整移除，相關 plist 與 `~/Library/Application Support/Boshiamy` 全清
- ❌ **OpenVanilla**（舊稱「香草/小草輸入法」）—— 從輸入清單移除已久；**2026-06-05 確認 `/Library/Input Methods/` 與 `~/Library/Input Methods/` 兩個目錄都沒有 OpenVanilla.app 檔案**，完整卸載
- 備份位置（要還原需從官網重抓）：`~/Library/Rime/_backup_boshiamy_uninstall_20260602_231649/`

## 紅線（2026-06-02 修訂）

- **新紅線：** 系統至少保留一個能打中文的輸入法在輸入清單裡
- 移除任何輸入法前，先驗證替代品穩定運作超過 24 小時
- 鼠鬚管本身不要隨意更動設定，除非教練明確要求
- 不要再建議「加回 OpenVanilla 當後路」——app 檔案已不存在，要還原需從 OpenVanilla 官網重抓

## 語音辨識常見誤判（守則 18 必看）

| 教練口說 | 可能被語音辨識成 | 正確對映 |
|---------|----------------|---------|
| 嘸蝦米 | 無蝦米、五蝦米、liur、liu7 | RIME `liur` = 嘸蝦米 |
| 鼠鬚管 | 鼠鬚、鬚管、Squirrel | 鼠鬚管 = Squirrel.app |
| 香草 | 小草 | 舊稱 OpenVanilla（已卸載，別再提） |

## How to apply

- 教練說「嘸蝦米」「無蝦米」「liur」「liu7」任一個 → 自動對映到 RIME `liur` 方案
- 不要再說「教練的輸入法是 OpenVanilla」或「教練用 Boshiamy 試用版」——都已卸載
- 教練說「我的輸入法」「打中文的」 → 預設指鼠鬚管 + RIME `liur`
- 相關記憶：`feedback_voice_typo_shixing_shouze`（語音糾偏）、`project_coach_rustdesk_remote_env`（遠端環境）
