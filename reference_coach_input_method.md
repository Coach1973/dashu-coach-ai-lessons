---
name: coach-input-method
description: 教練口中的「香草／小草輸入法」=OpenVanilla，慣用的中文輸入法是裡面的 liu7 嘸蝦米
metadata: 
  node_type: memory
  type: reference
  originSessionId: ddc5e99b-ea0c-43f0-8898-5b61266824c4
---

教練講的「**香草輸入法**」「**小草輸入法**」指的都是 **OpenVanilla**（Vanilla＝香草；裝在 `~/Library/Input Methods/OpenVanilla.app`，bundle id `org.openvanilla.inputmethod.OpenVanilla`，版本 1.8.4）。

教練**慣用的中文輸入法**是 OpenVanilla 裡的 **liu7＝嘸蝦米**（劉氏拆碼輸入法，bundle `org.openvanilla.OVIMTableBased.liu7`）。

**2026-05-22 根因確認 ✅（已驗證）：** 教練實測：語音輸入後先按一下 Ctrl、再按一下 Cmd，再打 e 就不跳了 → 坐實根因。 教練在 RustDesk 遠端（Windows→Mac）打字時，打 E/F/I/M 會跳快捷鍵（emoji/全螢幕/搜尋），時好時壞。**教練關鍵實測：完全不用語音輸入→正常；一旦用 Typeless 語音輸入→問題就出現。** → 真正根因是 **Typeless 語音輸入**，不是輸入法、也不是純 RustDesk。

**機制（高度吻合）：** Typeless 的「貼上辨識文字」快捷鍵＝`LeftCtrl+LeftCmd+V`（見其 app-settings.json）。語音轉文字後 Typeless 自動貼上，但 **Ctrl+Cmd 修飾鍵沒乾淨放開**（RustDesk 遠端下放開訊號易丟），導致後續打字母全被加上 Ctrl+Cmd 變快捷鍵。對應 RustDesk issue #5707「command-control 一直被按著」。
- **即時自救：** 語音輸入後、打字前，先單獨按一下 Ctrl、再按一下 Cmd 解開卡住的修飾鍵。
- **根治方向：** 調整 Typeless 的貼上快捷鍵/輸出方式，避開 Ctrl+Cmd 組合（待驗證後執行）。
- ⚠️ 教訓：第一輪查過 Typeless 但太早排除（只看設定乾淨沒往「貼上動作卡修飾鍵」想），中途誤判成「換官方輸入法就解決」。靠教練實測才回正軌。

**輸入法現況：** 教練已把 OpenVanilla 從輸入來源清單移除（但 `~/Library/Input Methods/OpenVanilla.app` 檔案還在，隨時可加回當後路）；改用**官方嘸蝦米試用版**（`/Library/Input Methods/Boshiamy.app`，bundle `com.boshiamy.inputmethod.BoshiamyIMK`）＋ABC。⚠️ Boshiamy 是**試用版**，留意到期，屆時需購正式版或加回免費的 OpenVanilla。簡體拼音(SCIM)已移除。
- 加新輸入法：系統設定>鍵盤>輸入來源>編輯>左下「＋」；按＋即出現，不必登出登入。

**How to apply:**
- 聽到「香草／小草輸入法」自動對映到 OpenVanilla，不要誤會成內建輸入法。
- **絕對不要移除 OpenVanilla 或停用嘸蝦米**——那是教練打中文的唯一慣用法，移除＝害他不能打中文（呼應教練「別像上次刪了害我半天不能做事」的鐵律）。
- 嘸蝦米是「拆碼輸入法」，中文模式下會把英文字母當字根；教練要打純英文需切英數模式或內建 ABC。
- 相關：語音對映見 [[feedback_voice_typo_shixing_shouze]]；遠端環境見 [[coach-rustdesk-remote-env]]。
