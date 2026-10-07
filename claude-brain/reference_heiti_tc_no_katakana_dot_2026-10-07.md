---
name: reference-heiti-tc-no-katakana-dot-2026-10-07
description: Pillow 用 Mac 的「黑體-繁」(/System/Library/Fonts/STHeiti Medium.ttc index 0) 寫中文時，日文中間點「・」會變方框，要換成「‧」；信任遊戲成績卡就是這樣做
metadata:
  node_type: memory
  type: reference
  originSessionId: 926d5b9e-ad7f-4952-868e-b1e36ce82e03
  modified: 2026-10-07T13:16:26.367Z
---

程式在圖片上寫繁體中文：字型用 `/System/Library/Fonts/STHeiti Medium.ttc`，`index=0` 是「黑體-繁 中」（index 1 是簡體）。PingFang 在 AssetsV2 底下、路徑會變，不要用。

**坑**：遊戲稱號、等級都用「・」（U+30FB，例：廣結善緣・第 4 級），黑體-繁沒有這個字，畫出來是方框。2026-10-07 做信任成績卡時親眼看圖才發現（測試全過也抓不到）。改成「‧」（U+2027）就正常；`trust_card._safe()` 統一替換。

**How to apply**：任何 Pillow 出圖寫中文，交付前一定要打開圖片看一次（N4），特別看標點；有「・」就先換掉。相關：[[reference-lk888-spend-guard-2026-09-26]]
