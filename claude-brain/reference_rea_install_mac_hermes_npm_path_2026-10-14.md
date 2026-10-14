---
name: reference-rea-install-mac-hermes-npm-path
description: Mac 上 npm 全域套件裝在 ~/.hermes/node，bin 不在 PATH；裝 rea-agents 後要補 ~/.local/bin 捷徑，rea setup 才會寫對 MCP 路徑
metadata:
  type: reference
---

聯想 10/14 來信要求 Mac 裝 REA（逆向工程工具）＋大樹口令技能 `bigtree-web-feature-clone`。Mac 實測：
- `npm install --global rea-agents@latest` 裝到 `~/.hermes/node/bin/`（因 `~/.local/bin/node`、`npm` 是指向 `~/.hermes/node/bin/` 的捷徑），不在 PATH → 裝完 `which rea` 找不到。
- 解法：`ln -s ~/.hermes/node/bin/rea ~/.local/bin/rea`，再 `rea setup --client claude_code --yes`（MCP 寫成 `/Users/bymyway/.local/bin/rea mcp`）。不要用 npx 版 setup、不要加 --install-hopper。
- 技能複製：`cp -R workspace/cloud_sync/skills/bigtree-web-feature-clone ~/.claude/skills/`；`start_debug_chrome.sh` 的 Mac 分支（nohup 背景）實測可用。
- REA 的 MCP 工具要重開新對話才載入；之前先用 `rea <指令>` 指令列，結果相同。
- 觸發口令：教練丟網頁說「我想做出這個功能／這個特效怎麼做的／拆解這個網頁」。
