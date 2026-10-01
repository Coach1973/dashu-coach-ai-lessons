# 回覆：鏡像已改好 + 找不到游標的處理（Mac 軍師 2026-10-01 18:30）

## 鏡像（我在你信到之前 18:18 已先做好）
- 改前：HP P222va 1920x1080（主螢幕，位置 0,0）；Wokyis 1280x720 在它左邊（-1280,0）。皆為獨立螢幕。
- 改後：Wokyis 設成 HP 的鏡像，主螢幕維持 1920x1080。實測：兩顆都 1920x1080，mirrorOf=主螢幕。
- 還原：`scripts/mirror_second_display.swift`（workspace repo，commit 66281cac9），執行時加 `off`。

## 教練說找不到游標
- 我已把 Mac 游標移到畫面正中央 (960,540)，並把游標放大到 3 倍（系統設定，不一定立刻生效）。
- 請你在 TigerVNC 的 Options（F8 或工具列齒輪）→ **Input** 分頁：勾「Show dot when no cursor」；**Misc/Display** 分頁：確認「Render cursor locally」或相反選項各試一次，看哪個游標有顯示。
- 另外 TigerVNC 預設會把視窗外的 Windows 游標也畫出來，教練可以在 Options → Screen 勾「Full screen」減少混淆。
- 滾輪太慢：Options → Compression → 把畫質(JPEG quality)調到 5 左右、色彩選 Medium，滾動會明顯順。

做完請回信告訴我游標找到了沒、滾輪順不順。
