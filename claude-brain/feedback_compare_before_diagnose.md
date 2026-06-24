---
name: feedback-compare-before-diagnose
description: 教練說某網頁功能壞 + 旁邊有可用對照版 → 第一動 diff/抄，不准開 preview/dev server 診斷
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c69b6a3e-279f-496c-b431-48b479cca56a
---

教練說「某網頁功能壞掉」**且有一個已知會動的對照版**（同 repo 衍生、舊版、官方版）→ **第一動：diff 兩邊，抄好的覆蓋壞的，不准診斷**。

**Why:** 2026-06-21 凌晨 5 點 government-grow 報名按鈕沒反應，教練第一句就講「去看 government-subsidies 的網頁碼怎麼寫的，照抄不就得了」。我卻：
1. grep 找 onclick 邏輯
2. 用 node 跑 JS 語法檢查
3. 開 mcp__Claude_Preview 想啟 dev server 點按鈕看 console
4. 發現 launch.json 在不同位置又繞 find

教練罵「你查太久了…繞半天，浪費我的時間及流量」+「又是一個無眠的夜晚」。最後 diff 出來 script **完全一樣**，本來就是 cache 問題，3 行 push 完事。

**How to apply:**
- 教練說「壞了」+ 指向對照版 → 立刻 `diff <(對照版) <(壞版)`，30 秒內出答案
- diff 完整 = 99% cache/部署延遲問題，加 cache-buster + push + 提醒 Cmd+Shift+R
- diff 有差 = 直接 sed/cp 覆蓋對應區段，不 review、不重構
- **禁止**：開 preview tool / dev server / 寫測試腳本 / 跑 node 語法檢查 — 全是「我覺得我在工程，其實在拖時間」

相關記憶：[[feedback-just-do-it]]、[[feedback-do-everything-for-user]]、[[feedback-scarce-resource-workflow]]
