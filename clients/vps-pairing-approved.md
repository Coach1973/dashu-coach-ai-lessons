---
name: VPS 小龍蝦 8 位體驗用戶開通名單（2026-07-01）
description: VPS 43.245.60.200 上 2026-07-01 湧入的 8 位外部體驗用戶 + 教練本人的開通清單
metadata:
  type: reference
---

# VPS 小龍蝦 8 位體驗用戶開通名單

> **建立時間**：2026-07-02 中午 12:02 台灣時間
> **建立者**：Mac 終端機軍師 Opus
> **資料來源**：ACER 軍師 20260701-2100 信（SSH 上 VPS 查證重建）
> **狀態**：✅ 全部已開通（教練 2026-07-02 11:14 親口確認）

---

## 開通清單（8 位外部體驗用戶 + 教練本人 = 9 個）

| # | 姓名 | Telegram ID | 加入時間 | Pairing Code | 狀態 |
|---|------|-------------|----------|--------------|------|
| 1 | 芸熙 | 2097920204 | 7/1 16:45 | （教練已批准）| ✅ 已開通 |
| 2 | Thomas Lin | 8983626868 | 7/1 16:59 | （教練已批准）| ✅ 已開通 |
| 3 | Esther（幸福導師，知識創業顧問）| 8970866856 | 7/1 17:04 | （教練已批准）| ✅ 已開通（已建客戶檔）|
| 4 | 翊舒 Vivian 陳 | 8380791400 | 7/1 17:05 | （教練已批准）| ✅ 已開通 |
| 5 | CHIU YuJung（新手小白，要求隱藏背景處理）| 8364394153 | 7/1 17:56 | （教練已批准）| ✅ 已開通（已建客戶檔）|
| 6 | Lin Yu Ju（自稱「老大」）| 8866874280 | 7/1 17:56 | **7S226YV6** | ✅ 已開通（已建客戶檔）|
| 7 | 梵蓮華 | 8368593258 | 7/1 18:00 | （教練已批准）| ✅ 已開通 |
| 8 | 杉榕陳 | 8626705510 | 7/1 18:03 | （教練已批准）| ✅ 已開通 |
| — | **教練本人** | 6124913915 | — | — | — |

---

## 已建客戶檔案的 4 位

| 姓名 | 客戶檔位置 |
|------|-----------|
| Esther | `workspace/clients/esther_*.md`（已建）|
| CHIU YuJung | `workspace/clients/chiu_yujung_*.md`（已建）|
| Lin Yu Ju | `workspace/clients/lin_yu_ju_*.md`（已建）|
| 杉榕陳 | （用戶最後一刻加入，檔案待確認）|

---

## 數字落差說明（v36 接力棒遺留問題）

- 教練記憶中「12 個」 vs 實際查到「8 個外部 + 教練 = 9 個」
- ACER 猜測可能包含 Mac 端學長/學弟/學妹三個既有帳號
- **待教練最終確認**

---

## 開通流程摘要（給未來參考）

1. 教練分享 Telegram bot 連結（`@coach_bymyway_bot`）
2. 用戶加 bot → OpenClaw 自動建 session
3. 走 `agents.defaults.model = minimax/MiniMax-M3`
4. 用戶收到 bot 回傳的 Pairing code（如 7S226YV6）
5. 用戶把 code 轉傳給教練
6. 教練從後台 approve：
   ```bash
   sshpass -p '9kdxvQN2' ssh root@43.245.60.200 \
     "docker exec openclaw openclaw pairing approve telegram <CODE> --channel telegram --notify"
   ```
7. 核准後用戶可正常使用小龍蝦

---

## 相關檔案

- ACER 來信：`cross-agent/outbox/2026-07/20260701-2100_acer-to-mac_vps-9-accounts-and-restore-lesson.md`
- VPS 連線資訊：`reference_vps_connection.md`
- Pairing 指令格式：`feedback_vps_pairing_approve.md`

---

> 本檔由 Mac 終端機軍師 Opus 建立，2026-07-02 中午 12:02 台灣時間。
> 教練 11:14 親口確認「8 位都已從後臺批准通行、放行」，本檔為永久開通紀錄。