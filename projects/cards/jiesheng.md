# 專案卡：結繩領導學（jiesheng-leadership + 戰報系統）

- **官網 repo**：`/Users/bymyway/github_repos/jiesheng-leadership`
- **🔴🔴 部署型態：GitHub 自動部署型——push = 立刻上線正式站！**（兩度血淚：不能「先推GitHub再等教練說推」，這站 push 就是部署，動手前必想起這條）
- **正式站**：https://jiesheng-leadership.netlify.app （兩日工作坊銷售頁；舊版新書發表內容封存在 archive/）
- **戰報系統**：https://rpl-workshop.bymyway.com/admin （本機 Flask，launchd `com.coach.jiesheng-webapp`，位置 `workspace/jiesheng-report`）｜帳號 RPL（大寫），密碼=公司統編（AI 未接觸）
- **戰報功能**：開課倒數/目標達成率/邀請人下拉（曜董/大樹/佩君/Lavi）/整頁一次「全部儲存」
- **姊妹報名頁**：workshop-invite / workshop-peipei / workshop-lavi / workshop-richard（各自獨立 Netlify 手動推型，付款連結=PayUNi 直連）
- **狀態**：台中場已取消（主站+workshop-invite 皆已同步）
- **血淚**：`.env` 含 `$` 字元的值要單引號包住，否則 bash source 會吃掉
