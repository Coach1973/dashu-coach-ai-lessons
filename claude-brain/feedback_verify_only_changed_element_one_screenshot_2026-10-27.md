---
name: feedback-verify-only-changed-element-one-screenshot-2026-10-27
description: 改網頁小地方後驗證只截「被改動的那一小塊」一張；整頁往下掃、重複截圖是白燒額度（champagne-salon 匯款帳號案 5 截 7 看）
metadata:
  type: feedback
---

教練 2026-10-27 17:00 糾正：在 champagne-salon 報名表下加匯款帳號，原文只有一處、一次就改對，但我為了「找到它」整頁往下掃，截圖 5 次、看圖 7 張；教練說「這樣是不是不夠遵守我的指令」。

**Why**：每看一張圖＝多一輪、整段對話再重讀一次，吃額度（10/26 分析：燒額度看「每輪當下的對話容量」×輪數）。N4 要求交付前親眼驗證，但沒要求整頁掃。

**How to apply**：已知原始碼行號／元素就只截那一塊一張（複製頁面到 /tmp、CSS 隱藏其他區塊，或滾到該元素）；沒裝的工具（playwright）先 `import` 試一次就改用 Chrome headless，不重試。同類錯第二次出現不加記憶，改反射 R-VERIFY-ONE-SHOT-ELEMENT-ONLY（knowledges/反射索引.json）的刺激。見 [[feedback-context-30pct-line-2026-10-26]]。
