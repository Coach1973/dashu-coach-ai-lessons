---
name: project-mentor100-review-gated-signup-2026-08-08
description: mentor100百人導師計劃從自動自助上架改為人工審核流程上線，含訪客計數器+導師點擊排行榜+申請/預覽/上架三段式流程
metadata: 
  node_type: memory
  type: project
  originSessionId: fc75ce1b-c241-4d2d-ac45-f4b2e9391167
  modified: 2026-08-07T18:59:02.597Z
---

2026-08-08，教練把 `mentor100.bymyway.com`（百人導師介紹站）從「訪客自助填表送出、立刻上架首頁」改成「先申請、教練審核、才上架」的人工守門流程，同一場還加了訪客數據功能。完整脈絡：

**1. 訪客計數器 + 導師點擊排行榜**：首頁新增「自2026年8月8日起到訪次數」計數卡（教練原話：先寫「到訪人數」後改「到訪次數」，因為「算次數比較精準」），取代原本「我要參與導師同行計劃」按鈕位置。後台`/admin/stats`新增熱度(含重複造訪)+精準人數(去重IP)+重複造訪IP清單+導師被點擊排行榜(金色長條+前三名獎牌)。

**2. 報名流程改人工審核（教練原話關鍵句）**：「我本來就是要做的一件事，就是前期我都讓他們自動送出，那個階段已經結束了。我現在就是要刻意營造『你現在就是要人工申請』的感覺」——這不是bug也不是妥協，是刻意的體驗設計，教練明確說「繞了一圈又回到原點，沒錯，我就是要這個結果」。

**3. 三段式最終流程**：① 首頁「我要加入百人導師計劃」按鈕連到`/apply`，只收姓名/公司職稱/LINE ID三欄，送出後寫入`applications`表+透過`sme-register-fn`(跟大樹小講同一套管線)通知教練LINE ② 教練在後台「導師申請名單」（`/admin`首頁最上方 + `/admin/stats`都有，教練要求兩處都要看得到）按「產生填寫連結」，建一筆`status='draft'`的空白導師+沿用最早設計的完整自助編輯頁(`/join/edit/<token>`，姓名/公司/簡介/照片/9組可自訂標籤連結，教練原話「這個要回到最早我設計的那些、它可以填寫的所有欄位」，強調不能簡化) ③ 申請人自填資料仍是草稿不會自動上架，教練在後台「預覽」（`/admin/mentors/<id>/preview`，仿照首頁卡片+modal樣式做WYSIWYG預覽）看過沒問題才按「確認上架」，`mentors.status`才變`published`，`list_mentors_published()`過濾後才會出現在公開首頁。

**技術要點**：`mentors`表新增`status`欄位(draft/published，預設published，ALTER TABLE遷移，56筆既有資料全部保留published不受影響)，`applications`表新增`mentor_id`關聯欄位。舊的`/join`公開自助全欄位表單(GET+POST)已關閉、轉址到`/apply`；`/join/edit/<token>`(既有56位導師的自助修改連結)完全不受影響。草稿導師用生成的`_placeholder.jpg`佔位照片(已`git add -f`強制納入版控，因為`static/uploads/*`平常被`.gitignore`排除)。

**過程中的澄清（非教練糾正，是需求細化）**：一開始我把「填寫連結」設計成簡化版三欄表單，教練澄清要的是原本設計的完整表單(靠既有`join_edit.html`機制直接滿足，不用重做)；一開始把「加LINE官方帳號」快捷按鈕加進申請頁/成功頁，教練要求拿掉，改純資料送出。

Commits（mentor100獨立repo）：`e1a9f5c`（文案改到訪次數）→`7072acc`（人工申請流程+LINE通知）→`ae60923`（拿掉LINE按鈕）→`6f563d9`（三步驟文案）→`6ce1df6`（審核上架流程主體）→`7ff1cbb`（申請名單同步顯示於admin_list）。

Related: [[project_mentor100_edit_link_selfservice_2026-08-02]]（`edit_token`/`join_edit`機制的更早期背景）
