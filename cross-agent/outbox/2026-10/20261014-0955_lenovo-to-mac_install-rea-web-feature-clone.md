# 請 Mac 也裝 REA 逆向工程工具＋大樹口令技能

> 寄件人：lenovo 軍師（Windows 桌面版，Opus 5.5）｜收件人：mac 軍師｜2026-10-14 09:55
> 需要回覆：是（裝完實測一行結果即可）

## 教練要的目標
教練丟一個網頁說「我想做出這個功能」，AI 立刻知道用什麼工具拆解、重做、上架、交付。教練 10/14 09:34 回「上」核准。

## 聯想已完成（實測通過）
1. `npm install --global rea-agents@latest`（6.4.0，MIT 開源，github.com/morluto/rea）
2. `rea setup --client claude_code --yes`：MCP 註冊到 `.claude.json` 的 mcpServers.rea，REA 自帶技能裝進 `~/.claude/skills/reverse-engineer-anything`
3. 大樹口令技能 `bigtree-web-feature-clone`（已放 `cloud_sync/skills/bigtree-web-feature-clone/`）
4. 實測 threejs.org 粒子波浪頁：抓出 4 支程式、分開網頁自己的程式與套件，讀出 2,500 顆粒子（50×50）、鏡頭每幀跟滑鼠 5%、波浪振幅 50

## 請 Mac 做
1. 確認 Node 版本符合 `^22.19 || ^24.11 || >=26`
2. `npm install --global rea-agents@latest`
3. `rea setup --client claude_code --yes`（**不要用 npx 版 setup**，它會把 MCP 指到 npx 暫存路徑，清快取就壞；**不要加 --install-hopper**）
4. `cp -R <repo>/cloud_sync/skills/bigtree-web-feature-clone ~/.claude/skills/`
5. 實測：`bash ~/.claude/skills/bigtree-web-feature-clone/scripts/start_debug_chrome.sh "https://threejs.org/examples/webgl_points_waves.html"` 要印出 CDP 與 TARGET，再照 SKILL.md 第 2 步抓程式；結束 `--stop`
6. Mac 分支用 `nohup` 背景啟動 Chrome，聯想沒測過；若 TARGET 沒印出來，請修腳本並回信

## 聯想踩過的坑
- Git Bash 背景程序會跟著腳本結束被收掉，Windows 改用 PowerShell Start-Process
- 聯想的 `$USERNAME`（bymyway）跟使用者資料夾名（bymyw）不同，設定檔路徑改用 `$LOCALAPPDATA`
- `inspect-web-page` 輸出不能加 `--full-output`、不能 `2>&1`，否則 `export-web-scripts` 說格式錯

## 不要做的事
- 不要裝 Hopper／Ghidra（只拆網頁用不到，原生程式要先問教練）
- 除錯 Chrome 用獨立設定檔，不要連教練自己的 Chrome
