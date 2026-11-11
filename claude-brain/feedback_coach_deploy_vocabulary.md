---
name: coach-deploy-vocabulary
description: 教練的部署詞彙字典——「自動站／行動站」「網頁推」「推」三詞的正式定義
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3089ccd5-21cb-458c-92e4-eaecbd96dee9
---

# 🔴 教練部署詞彙字典（2026-06-17 下午 4:42 教練親口定稿）

| 教練說的詞 | 就是指 | 技術動作 | 目標站 |
|----------|--------|---------|--------|
| **「自動站」**（或「行動站」，同義）| **部署到 bymyway.com** | git push 到 GitHub repo（如 `bymyway-website`），bymyway WP iframe 自動拉新版 | bymyway.com 子頁（/ai/、/coach/、/leadership/ 等）|
| **「網頁推」**（這三個字）| **推送到 GitHub** | git add + commit + git push origin <branch> | GitHub 倉庫（教練的測試站）|
| **「推」**（單字）| **推送到 Netlify** | zip + curl Netlify API（不靠 git push 觸發）| `*.netlify.app` 正式站 |

> 補充（2026-11-11）：event.bymyway.com/curated/<slug>/ 的頁面（2026-10 起才有）沒有 Netlify，正式站就是 `~/github_repos/<slug>/`；教練說「推」＝git push 該倉庫（bigtree-web-edit 技能步驟 6）。上表「推＝Netlify」只適用 Netlify 站。

## 兩個彼此釐清的重點

1. **「自動站」≠「網頁推」≠「推」**——三者部署到不同地方，混用會災難
2. **「自動站」和「行動站」是同義詞**——教練 2026-06-17 親口承認「我說錯了，是自動站才對」，所以聽到任何一個都對應同一件事
3. **「網頁推」主要不在 bymyway**，而是 Netlify 線下教練的 GitHub repo（如 jiesheng-leadership、theunrestrictedwar、cool-case）

## Why
教練 2026-06-17 下午 4:42 親口釐清。之前軍師（包括我）多次把這三件事混淆：
- 把「網頁推」當「推 Netlify」→ 多扣點（案例 G/H）
- 把「自動站」聽成「行動站」→ 找不到 SOP（今天下午軍師踩雷）
- 把改 bymyway 當改 Netlify → 走錯流程
- 2026-07-04 凌晨：改 bymyway.com 首頁 iframe 來源（`bigtree/speakers-2026`）的內容，流程走對了（本機預覽→教練說推→git push→線上驗證），但回覆裡口誤講成「網頁推 SOP」——目標站明明是 bymyway.com，該講「自動站 SOP」。教練當場糾正。

## How to apply
1. 教練說「自動站」或「行動站」→ **走 `SOP_bymyway_auto_site.md`** + 「OPE 先驗法」+ git push GitHub（讓 bymyway WP iframe 抓新版）
2. 教練說「網頁推」（連續三字）→ **走 GitHub push**（git push origin <branch>），不碰 Netlify API
3. 教練說「推」（單字）→ **走 Netlify zip+API**（`NETLIFY_DEPLOY_CONFIRMED=1` + zip + curl deploys endpoint）
4. 三者的差別在「教練親口指令的字面」，按字面對應，不要自作解釋

關聯：[[netlify-deploy-zip-api]]、[[web-push-sop]]、[[anti-fool-system-haibinggang-rule]]
