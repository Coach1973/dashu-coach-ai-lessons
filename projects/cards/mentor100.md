# 專案卡：AI百人導師計劃（mentor100）

- **repo**：`/Users/bymyway/github_repos/mentor100`｜**資料庫**：同目錄 `mentors.db`（mentors + applications 兩表）
- **正式站**：https://mentor100.bymyway.com （本機 Flask port 5062，launchd `com.coach.mentor100-webapp` + tunnel）
- **部署**：改完程式碼 → `launchctl kickstart -k gui/$(id -u)/com.coach.mentor100-webapp` 重啟即生效（不走 Netlify）
- **上架流程**（教練刻意設計「人工申請」感）：/apply 申請 → 教練後台產生填寫連結 → 講師自填 → 自動上架；後台可「已發佈⇄草稿」一鍵切換
- **種子標籤規則**（教練 2026-08-15 欽定）：實際擔任過活動講師才標 seed（7/29 場3位+8/28 嘉義3位+台中場8位=14位），教練手動建的不算
- **申請通知**：走 `sme-register-fn`（教練 2026-08-15 裁示 B 案：**不接官網雙寫，維持原樣**——表單只收 LINE ID 沒收手機，跟官網以手機為身分證的設計不合）
- **血淚**：刪導師必用 `db.delete_mentor()`（已含孤兒外鍵清理）；直接 DELETE SQL 會讓 applications 表留孤兒引用、/admin 整頁 500
- **log**：`webapp.error.log`（500 先 grep BuildError）
