---
name: danger-command-five-gates
description: Use before running any irreversible command — rm -rf, Remove-Item -Recurse -Force, git reset --hard, git push --force, git clean -fd, DROP TABLE/TRUNCATE/DELETE without WHERE, or any full-directory/full-disk/full-database wipe. Enforces a five-gate check before execution.
---

# 危險指令零容忍鐵律（執行細則 N6，2026-06-17 案例24教訓，636GB學費）

對應守則 #03 #07 #15 #17。教練欽定「唯一正式版」：`~/.openclaw/workspace/執行細則.md`——這條規則**不在**`~/.claude/CLAUDE.md`（軍師/特助燒錄檔），是本次研究比對兩份文件時發現的缺口，本skill補上這個安全空隙。

## 涵蓋指令（不限於）

- `rm -rf` / `rm -r` / `find ... -delete` / `find ... -exec rm`
- `Remove-Item -Recurse -Force` / `rmdir /S`
- `git reset --hard` / `git clean -fd` / `git push --force`
- `rsync --delete` / `shred`
- `DROP TABLE` / `TRUNCATE` / `DELETE FROM ...`（無 WHERE）
- 任何整槽、整目錄、整資料庫的清除

## 執行前必過五道閘門（缺一不算合格）

1. **絕對路徑硬編碼**——目標寫死路徑字串，禁止用變數作為唯一來源（防跨shell跳脫災難）
2. **目標echo給教練看**——執行前先print完整目標路徑與計算大小
3. **大小驗證**——`du -sh`（Mac/Linux）/ `Get-ChildItem -Recurse | Measure-Object Length -Sum`（Windows）顯示受影響大小
4. **超過100MB必須通行證**——教練親口同意後才執行
5. **超過1GB任何身份不得自主執行**——必須教練親口此刻授權，不能用之前的授權類推

## 血淚教訓：查「是否被連結/是否在使用中」不能只查一層（案例51）

刪除前若涉及判斷「這個資料夾是否被連結到別處」，要**先查資料夾本身**的 Attributes/ReparsePoint 狀態，再往下查子項目——junction設在上層時，子項目透明重導向後看起來完全正常，只查子項目會漏掉「上層本身就是連結」這種情況，導致對「完全沒有連結」下錯誤的絕對結論。

## 鐵律

寧可多問一句、多驗證一次，也不要在不確定的狀態下執行不可逆操作。教練的信任建立在「你判斷錯了會先自己攔住自己」，不是「教練事後才發現你判斷錯了」。
