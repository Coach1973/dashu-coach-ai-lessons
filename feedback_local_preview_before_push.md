---
name: feedback-local-preview-before-push
description: 教練要求：HTML 網頁專案修改階段，先用本地檔案 + 桌面預覽，不急著 commit/push 上線。push 比較費工，等定稿才推。
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5a4bbfc2-481b-467b-b94a-aada4001c7c4
---

# 修改階段：先本地預覽，定稿才 push

教練 2026-06-29 16:36 親口：
> 「目前還在修改階段，可以先使用 html 的方式讓我看，因為推上去，還是比較工的。」

## 規則

HTML / 網頁 / EDM 類專案在「修改迭代階段」：

1. **單一來源檔**放在 `~/Documents/<project-name>/index.html`
2. **每次修改後同步到桌面預覽資料夾**：
   `D:\Users\Desktop\<project-name>_預覽\index.html`（含所有 assets）
3. 教練雙擊桌面 HTML 就能看效果
4. **只有教練親口說「推上去／上線／push」時，才 commit + push** 到 GitHub Pages

## Why

- push 涉及：git add / commit / push / 等 GH Pages 部署 30-90 秒
- 修改 10 次就 push 10 次 = 浪費 10 次「教練等部署」的時間
- 桌面預覽：改完 reload 立刻看
- 教練的工作節奏是「迭代很多次再定稿」，定稿前不該頻繁公開上線

## How to apply

**修改階段**（教練還在挑語感、調文案、改配色時）：
- ✅ 修改主檔
- ✅ 同步桌面預覽資料夾
- ✅ 跟教練說「桌面預覽更新好了，請 reload」
- ❌ **不要** 自動 commit + push

**定稿階段**（教練說「OK 推上去」「上線吧」「push」）：
- ✅ commit 到 local repo
- ✅ push 到 GitHub Pages

## 相關記憶

- [[feedback_no_improvise_when_copying]] — 照抄不擅作主張的同類精神
- [[feedback_dont_guess_coach_data_from_web]] — 對教練的工作流程要尊重，不擅自加動作
