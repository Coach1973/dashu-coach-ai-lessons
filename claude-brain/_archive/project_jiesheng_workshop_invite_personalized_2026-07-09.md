---
name: project-jiesheng-workshop-invite-personalized-2026-07-09
description: 結繩領導學工作坊邀請頁新增兩個個人化版本（蔡曜隆/LAVi），並統一同步文案修正到原本4個站台，共6站上線
metadata: 
  node_type: memory
  type: project
  originSessionId: cb7ca9a0-f6af-4595-a452-a688a54624cb
---

2026-07-09，教練要求以現有「workshop-invite」邀請頁為底，新建兩個「以特定人士名義發出邀請」的個人化版本：**workshop-richard**（蔡曜隆）、**workshop-lavi**（LAVi）。

**關鍵誤解與修正**：AI一開始誤把「邀請人」理解成「被邀請的客人」，把蔡曜隆/LAVi的名字放到歡迎客人的位置（badge「XXX 專屬邀請」代表迎接客人）。教練糾正：「邀請人」指的是**發出邀請的人**，蔡曜隆/LAVi的名字要放在原本「大樹教練」（頁面上簽名「大樹教練　敬邀」跟eyebrow「工作坊專屬邀請 · 大樹教練」）的位置——這兩個新頁面是給蔡曜隆/LAVi自己名義發出去的邀請連結，不是邀請他們本人來參加。

**最終6個站台內容（統一同步的文案修正）**：
- 「識人．育人．用人．留人」原本是4個方框（識人/育人/用人/留人各一格），改成6條長條狀（`identity-chip-grid`改`flex-direction:column`，`identity-chip`字級36px降到22px）：識人．育人．用人．留人 / 分析失效與成功的真正原因 / 建立可被理解的指令系統 / 如何讓人願意承擔責任 / 當團隊卡關的拆解方法 / 建立可複製的領導模式
- 講師介紹句：「淬鍊識人、育人、用人、留人智慧」→「淬煉跨領域企業經營智慧」
- 願景句：「做到像101大樓一樣穩」→「一樣屹立不搖」
- （僅workshop-richard/workshop-lavi這兩個新站）底部LINE按鈕改「有問題，詢問課程助教」連到結繩領導學官方LINE@ `https://lin.ee/QuSrjAL`；頁尾掛名「結繩領導學 × 大樹教練」改「結繩領導學 × 兩日實戰工作坊」

**教練明確要求不動的部分（原本4個站台）**：bni-invite、bni-peipei、workshop-invite、workshop-peipei 這4個維持各自原本的底部LINE按鈕（連自己LINE的維持連自己，連佩佩老師的維持連佩佩老師）跟頁尾掛名（大樹教練/佩佩老師），只同步文案修正部分。

**部署技術細節**：全部6個都是全新/更新的Netlify手動zip部署（非git），用`.NET ZipArchive`手動指定正斜線路徑打包（Windows的`Compress-Archive`會產生反斜線路徑導致Netlify解壓縮失敗，這個坑在[[project_media_resource_center_2026-07-09]]已踩過一次）。逐一用API輪詢確認`state:ready`才算數，事後curl驗證線上內容確實含新文字。

**最終上線網址**：bni-invite.netlify.app、bni-peipei.netlify.app、workshop-invite.netlify.app、workshop-peipei.netlify.app、workshop-richard.netlify.app（新）、workshop-lavi.netlify.app（新）

Related: [[project_bni_invite_pages_2026-07-09]], [[project_media_resource_center_2026-07-09]]
