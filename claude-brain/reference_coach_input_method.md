---
name: coach-input-method
description: 教練 2026-06-02 起改用鼠鬚管 Squirrel + RIME liur 嘸蝦米；Boshiamy 試用版已卸載
metadata: 
  node_type: memory
  type: reference
  originSessionId: ddc5e99b-ea0c-43f0-8898-5b61266824c4
---

## 2026-06-02 重大更新（軍師 Claude Sonnet 4.6 親手執行）

**教練現在的中文輸入法：鼠鬚管 Squirrel + RIME `liur` 方案（hsuanyi-chou/rime-liur）**
- App 路徑：`/Library/Input Methods/Squirrel.app`
- Bundle ID：`im.rime.inputmethod.Squirrel`（Hans/Hant 兩個 input mode）
- RIME 設定：`~/Library/Rime/`（12 個 yaml 檔 + opencc/）
- 編譯產出：`~/Library/Rime/build/`（含 `liur.extended.table.bin` 等字典 binary）
- 預設 schema：liur（49 萬行完整無蝦米字根，源自 GitHub `hsuanyi-chou/rime-liur`）
- 教練實測：**「打的很順，一切正常」**（2026-06-02 23:15）

**已卸載：**
- Boshiamy 試用版（`/Library/Input Methods/Boshiamy.app`）—— 2026-06-02 23:17 sudo 移除
- 相關 plist 與 `~/Library/Application Support/Boshiamy` 全清
- 備份在 `~/Library/Rime/_backup_boshiamy_uninstall_20260602_231649/`（含 plist；.app 本身未備份，要還原需重去官網下載）

**仍在系統但已從輸入清單移除：**
- OpenVanilla（`~/Library/Input Methods/OpenVanilla.app`）—— 教練更早之前移出選單

---

## How to apply（新版）

### 紅線（更新）
- 鼠鬚管已驗證能打中文，**舊紅線「絕不可移除 OpenVanilla/嘸蝦米」已不適用**
- 新紅線：**至少保留一個能打中文的輸入法在系統清單裡**；要移除任何一個前，先驗證替代品穩定運作超過 24 小時

### 鼠鬚管維護常識
- 改 `~/Library/Rime/*.yaml` 後要重新部署：`open -a Squirrel` 然後在選單列點圖示→「重新部署」
- 命令列強制重建：`"/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel" --build` 或 `rime_deployer --build "$HOME/Library/Rime" "$HOME/Library/Rime/build"`
- 切換到鼠鬚管：Ctrl+Space 或選單列輸入法圖示

### 危險操作（軍師親身教訓 2026-06-02）
**修 `~/Library/Preferences/com.apple.HIToolbox.plist` 之前**：
1. **先 `cp` 一份備份**
2. Python plistlib.dump 簽名是 `dump(value, fp)`，**不是 `dump(fp, value)`**——搞反了會把整個 plist 變 0 byte，教練的所有輸入法設定都會消失
3. 改完先 `plutil -lint` 驗證，再 `defaults read` 驗證
4. 最後才 `killall cfprefsd` 觸發重讀

---

## 歷史紀錄（2026-05-22 OpenVanilla 時代，留檔）

教練講的「**香草輸入法**」「**小草輸入法**」=**OpenVanilla**（bundle `org.openvanilla.inputmethod.OpenVanilla`，1.8.4）。教練慣用 OpenVanilla 裡的 **liu7=嘸蝦米**（bundle `org.openvanilla.OVIMTableBased.liu7`）。

**RustDesk + Typeless 語音輸入根因（已修）：** Typeless「貼上辨識文字」快捷鍵 `LeftCtrl+LeftCmd+V`，遠端下修飾鍵放開訊號易丟（RustDesk #5707），後續打 E/F/I/M 變快捷鍵。即時自救：語音輸入後先按一下 Ctrl 再 Cmd 解卡。根治方向：調 Typeless 貼上快捷鍵避開 Ctrl+Cmd。

相關：[[feedback_voice_typo_shixing_shouze]] / [[coach-rustdesk-remote-env]]
