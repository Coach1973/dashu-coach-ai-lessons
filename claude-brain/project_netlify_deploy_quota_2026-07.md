---
name: project-netlify-deploy-quota-2026-07
description: Netlify部署額度追蹤——本質一直是credit制，「剩幾次」是拿credit餘額除以15(每次部署耗15點)換算出來的，2026-07-25credit核發後額度回升到約71次
metadata: 
  node_type: memory
  type: project
  originSessionId: 54392333-a164-49b3-b17d-eae26af22220
  modified: 2026-07-25T07:56:38.477Z
---

# Netlify部署額度追蹤（2026-07月）

## 🔴 2026-07-25更正：不是改制，是credit餘額變多了

教練糾正：Netlify帳號**一直都是**credit制，不是今天才「改制」。之前追蹤的「剩幾次」這個數字，本來就是我們自己拿credit餘額換算出來的——**每次部署扣15點credit**。

教練親貼Netlify帳單頁（`app.netlify.com/teams/bymyway7/billing/general#credit-balance`）截圖，目前credit餘額：

- **Personal plan credits**：1000點，2026-07-25核發，2026-08-25到期，目前剩**999.5點** → 約66次部署額度
- **無到期日credits**：500點，2026-05-30核發、無到期日，目前剩**70.1點** → 約4次部署額度
- 兩池合計約**71次**部署額度
- Credit依到期日先扣（soonest first），會先扣8/25到期那組

## Why

7/17記錄的「16次」是當時credit餘額換算出來的數字，7/25這天核發了新一批1000點credit，餘額大漲，換算出來的次數自然跟著跳升到71次——這不是系統規則變了，只是餘額本身變多了。之後每次真的部署，都要用「credit餘額差 ÷ 15」來確認換算率有沒有跑掉。

## How to apply

**每次要推Netlify之前**：
1. 先報目前剩餘次數（餘額/15換算），例如「這次推完約剩70次」
2. 若剩餘次數低（≤3次）且不是緊急/教練明確要求，主動提醒額度快用完
3. 推送完成後，比對前後credit餘額差異是否仍是15點，更新這份記憶檔與`state/netlify_deploy_quota.json`

## 額度使用紀錄（每次更新剩餘次數，換算率15點/次）

| 日期 | 事件 | 扣除後剩餘 |
|------|------|-----------|
| 2026-07-17 | 教練告知起始額度 | 16 |
| 2026-07-19~07-24 | 陸續多次部署（tainan-calender/bigtree-tw/ai-talk-tw/jiesheng-leadership等） | 見`state/netlify_deploy_quota.json`history區塊 |
| 2026-07-25 | 教練貼帳單截圖，新credit核發，餘額換算回升 | 約71 |
| 2026-07-25 | ai-talk-tw部署：現場設攤6家廠商+贊助好禮+贊助人名單+入門禮補充(deploy 6a646c0213e4778b1f227e4e) | 70 |

Related: [[reference_netlify_token]], [[feedback_netlify_autodeploy_cost_awareness]]
