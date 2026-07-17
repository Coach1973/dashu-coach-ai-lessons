---
name: project-netlify-deploy-quota-2026-07
description: Netlify部署額度追蹤——2026-07-17教練親告只剩16次部署，7/25前每次推Netlify都要計數提醒剩餘次數
metadata: 
  node_type: memory
  type: project
  originSessionId: 54392333-a164-49b3-b17d-eae26af22220
---

# Netlify部署額度追蹤（2026-07月）

**教練原話（2026-07-17）：** 「我的Netlify目前只剩下16次的部署。所以接下來我每一次上傳到Netlify，你都要幫我計算，在25號之前，最多隻有16次的部署時間。」

## 目前狀態

- 起算基準：2026-07-17，剩餘 **16次**
- 額度重置時間點：**2026-07-25**（教練說的期限，推測是Netlify方案的每月build/deploy次數重置日）
- 計算範圍：**每一次**推送到Netlify（不管是zip+API直推、或git連動自動觸發）都算一次，要往下扣

## Why

教練親口設下的硬性提醒——避免額度用完卡住緊急部署需求，尤其教練這台機器有22+個手動部署型網站（見`reference_netlify_token.md`），加上多個活動頁常常臨時要改要推，容易不知不覺就把額度燒光。

## How to apply

**每次要推Netlify之前**：
1. 先報目前剩餘次數（例如「這次推完會剩13次」）
2. 若剩餘次數低（例如≤3次）且不是緊急/教練明確要求，主動提醒「額度快用完了，要現在推嗎，還是等7/25額度重置後再推？」
3. 推送完成後，在這份記憶檔或當場回覆更新最新剩餘次數，方便下次對話接續

## 額度使用紀錄（每次更新剩餘次數）

| 日期 | 事件 | 扣除後剩餘 |
|------|------|-----------|
| 2026-07-17 | 教練告知起始額度 | 16 |

Related: [[reference_netlify_token]], [[feedback_netlify_autodeploy_cost_awareness]]
