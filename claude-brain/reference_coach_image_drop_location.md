---
name: coach-image-drop-location
description: 教練傳圖片一律進Mac的「下載」（Downloads）資料夾，找圖片先查這裡，不要繞去Desktop或其他路徑
metadata:
  type: reference
---

# 📥 教練傳圖片的唯一位置：~/Downloads

教練 2026-07-11 親口糾正：「我們唯一的搜尋圖片全部都在『下載』項目，好嗎？」

## How to apply
- 教練說「我傳了/下載了幾張圖片」→ 第一動作直接 `ls -la ~/Downloads` 或用時間+檔名比對，不要先繞去 Desktop、workspace 或猜測其他路徑
- 圖片檔名通常是原始下載檔名（例如社群媒體圖片會是類似 `714852654_xxxxx_n.jpg` 這種數字序號檔名，或 LINE/Telegram 匯出的 `178xxxxxxxxxx.jpg` 時間戳檔名），用 `find ~/Downloads -newermt "<教練說的時間>"` 配合檔案大小比對最快
- 這條規則是 Mac 桌面版/終端機環境專用；跟 [[reference_telegram_mac_cache]]（小龍蝦 Telegram inbox 找圖片路徑）是不同情境，不要混用

## Why
教練在同一個查找任務裡，軍師先繞去 Desktop 跟 workspace 目錄找不到，教練直接點破圖片其實一直都在下載資料夾，糾正查找範圍。以後應該優先鎖定這個路徑，加快查找速度、避免讓教練覺得軍師找錯地方。
