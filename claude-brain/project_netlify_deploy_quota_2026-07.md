---
name: project-netlify-deploy-quota-2026-07
description: Netlify部署額度SOP——每月25日重置周期、credit÷15算剩幾次，每次部署後必須查真實帳單頁更新，不能只靠估算遞減
metadata:
  node_type: memory
  type: project
  originSessionId: ca65df7a-23a8-43a7-996d-71d26e2119b8
  modified: 2026-08-24T17:13:22.764Z
---

# Netlify部署額度SOP（2026-08-25教練拍板正式版）

## 🔴 帳單周期：每月25日重置，不是24日

帳單頁面（`app.netlify.com/teams/bymyway7/billing/general`）明載「Current billing period runs from Jul 25 to Aug 24」——**24日是週期最後一天，25日才是真正重置那天**（帳戶API的`next_billing_period_start`為每月25日00:00 -07:00，換算台灣時間是當天下午3點）。教練口頭記成「24日結算」，正確講法是「25日重置、24日是舊週期最後一天」，兩種講法指的是同一件事，不用糾正教練，理解成同一天即可。

## 換算公式（每次部署後都要用）

**剩餘部署次數 = 帳單頁「Credits available」總數 ÷ 15**（無條件捨去，因為credit依到期日先扣完才會扣下一個池，兩池加總算即可，不用個別分開算再加總的次數）

## 🔴 核心教訓：估算遞減法會長期失準，必須定期回頭核對真實帳單頁

`state/netlify_deploy_quota.json`原本用「每次部署扣15點，遞減記錄」的估算法追蹤，但2026-08-25教練要求直接查真實帳單頁時發現：估算值停留在「約34次」，真實只剩**9次**（總額147點：Personal plan池76.4點+無到期日池70.1點）。落差原因是這段時間有多次部署沒有被正確記錄扣減（`netlify_deploy_guard.sh`的自動扣減邏輯依賴指令結尾剛好是`/deploys`，接了pipe或多個flag的curl指令會漏抓，見下方舊教訓），估算法只要漏抓一次就會開始跟真實值脫鉤，而且不會自己修正。

**結論：估算遞減法只能當「部署當下的即時提醒」用，不能取代真實查證。**

## ✅ 教練2026-08-25拍板的新SOP

1. **每次執行Netlify部署後**，直接查一次`https://app.netlify.com/teams/bymyway7/billing/general`（用claude-in-chrome連教練本機已登入Chrome，或Personal Access Token查`/api/v1/accounts`拿billing period日期，但credit餘額本身目前只能從網頁的Usage & billing頁面讀到，API沒有直接回傳「剩餘credit」欄位）
2. 讀取頁面上「Credits available」總數，除以15算出剩餘部署次數
3. 回報教練時附上這個數字，同時更新`state/netlify_deploy_quota.json`的`quota_as_of`/`quota_remaining`/`credit_pools`欄位為真實值（不要再只做遞減估算，要真的去查）
4. 若剩餘次數≤3且非教練明確要求的緊急部署，主動提醒額度快用完

## 2026-08-25查證的真實數字（供下次快速比對用）

- 當期週期：Jul 25 ~ Aug 24（8/25即將重置）
- Personal plan credits：76.4 / 1,000 remaining（2026-07-25核發，2026-08-25到期）
- 無到期日 credits：70.1 / 500 remaining（2026-05-30核發，無到期日）
- 合計147點 → **約9次部署額度**
- 本期消耗明細：Production deploys 49次=735點／Web requests 99,186次=19.8點／Bandwidth=168.4點／Compute=0.4點／AI inference=0點，合計消耗923.6點

## Why

教練親口點出：這套系統的最高目標是像鋼鐵人的賈維斯——教練交代過、說過的每一句話，AI都要記得並且能自動串連起來，不用每次重複交代。額度快沒了卻不知道、教練得自己上網去查，就是「AI沒有主動幫教練把關」的反面案例；估算法失準卻沒人發現，正是「記得了但沒有用出來」（對應守則#01「記不住就是不在乎」的延伸——這裡是「記錯了、不驗證，比不記得更糟」）。

## How to apply

- 之後任何一台機器的軍師要推Netlify前，先用這份SOP的公式估個大概（沒空查真實頁面時的備援），但**部署完成後一定要抽空查一次真實帳單頁**，不能讓估算值連續好幾天沒人回頭核對
- 8/25當天或之後，額度會重置回1000點（Personal plan池），到時候直接更新這份記憶檔的「當期週期」跟餘額，不用重新推導公式

Related: [[reference_netlify_token]], [[feedback_netlify_autodeploy_cost_awareness]]
