---
name: check-openclaw-version-before-gateway-restart
description: 重啟main gateway前要先確認終端機PATH版本跟launchd正式服務版本是否一致，不一致先不要重啟，否則可能撞上state資料庫schema不相容導致服務完全down機
metadata:
  type: feedback
---

這台機器同時裝了兩個openclaw版本：`/opt/homebrew/lib/node_modules/openclaw`（homebrew，較舊）跟`/Users/bymyway/.nvm/versions/node/v24.21.0/lib/node_modules/openclaw`（nvm，較新，終端機`PATH`優先解析到這個）。main gateway的launchd服務(`ai.openclaw.gateway.plist`)寫死用其中一個版本的絕對路徑，不會自動跟終端機同步。

在終端機執行任何`openclaw`指令（`plugins install`、`infer`、`pairing approve`等）都可能觸發state資料庫schema自動升級，但如果正式服務用的是**不同版本**且**還沒重啟**，它會繼續安然無事地跑——直到下次重啟，直接撞上schema不相容，整個服務(main gateway，教練唯一的LINE+Telegram溝通管道)完全停擺。

**Why**：2026-09-16凌晨，軍師在終端機操作觸發了新版本(2026.9.4)把state資料庫schema從1升到17，正式服務還在跑舊版本(2026.6.34)毫無異狀；軍師之後為了讓新hook生效`launchctl kickstart -k`重啟main gateway，直接撞上版本不相容，main gateway完全down機45分鐘，搶修過程中還誤殺了小二(test2)的子process連帶讓它也停止服務。完整經過見[[試金石案例73]]。

**How to apply**：
1. 任何要重啟main gateway（或其他launchd管理的正式openclaw服務）之前，先跑`which openclaw`跟`plutil -p <plist路徑>`裡`ProgramArguments`的執行檔路徑做比對，兩者版本不一致就先不要重啟，找出原因再動手
2. 在終端機執行`openclaw`相關CLI指令時，如果遇到「config驗證錯誤」「schema不符」這類訊息，不要當成「跟眼前任務無關的舊技術債」直接繞過——這可能是版本落差已經造成資料庫被升級的警報，要主動查證
3. `kill -9`任何process前，先`ps -p <pid> -o ppid,command`確認父子關係，不能只憑「看起來像殘留」的直覺判斷
4. `plutil -replace`修改plist後，順手`chmod 644`確認權限沒被意外改掉（launchd對plist權限敏感，錯誤權限會讓bootstrap回報不明確的"Input/output error"）
