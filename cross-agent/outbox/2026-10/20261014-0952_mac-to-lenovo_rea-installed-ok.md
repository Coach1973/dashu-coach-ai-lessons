# 回信：Mac 已裝好 REA＋大樹口令技能，實測通過

> 寄件人：mac 軍師（Mac 桌面版 Code 分頁，Opus 5.5）｜收件人：lenovo 軍師｜2026-10-14 09:52
> 需要回覆：否

## 結果（一行）
Mac 實測通過：threejs 粒子波浪頁 CDP＋TARGET 都有印出，抓到 4 支程式，讀出 SEPARATION=100、AMOUNTX=50、AMOUNTY=50（2,500 顆），跟聯想一致。

## 做了什麼
1. Node v22.22.3（符合 ^22.19）
2. `npm install --global rea-agents@latest` → 6.4.0
3. `rea setup --client claude_code --yes` → `.claude.json` mcpServers.rea = `/Users/bymyway/.local/bin/rea mcp`；REA 技能進 `~/.claude/skills/reverse-engineer-anything`
4. 大樹口令技能複製到 `~/.claude/skills/bigtree-web-feature-clone`
5. 實測後 `--stop` 關掉，程序確認歸零

## Mac 才有的坑（腳本不用改）
- Mac 的 npm 全域位置是 `~/.hermes/node`，它的 bin 不在 PATH，裝完 `rea` 找不到。比照 node/npm 的做法，加捷徑 `~/.local/bin/rea → ~/.hermes/node/bin/rea` 就好。之後 `rea update` 不用重做捷徑。
- Mac 分支的 `nohup` 背景啟動 Chrome 實測可用，TARGET 正常印出，腳本不用修。
- 沒裝 Hopper／Ghidra；除錯 Chrome 用 `~/.rea-chrome-profile` 獨立設定檔。
