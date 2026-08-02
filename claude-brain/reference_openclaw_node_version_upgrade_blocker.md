---
name: reference-openclaw-node-version-upgrade-blocker
description: OpenClaw升級到2026.7.1-2需要node>=22.22.3<23或>=24.15.0<25或>=25.9.0，本機gateway實際用的homebrew node是25.6.1卡在不支援區間，升級前必須先處理node版本
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3b2a9f5b-e76f-47e1-82d9-76f9301b1c99
  modified: 2026-08-02T10:20:10.060Z
---

2026-08-02健檢時嘗試把OpenClaw從2026.6.33升級到2026.7.1-2（教練要求先查清楚升級內容再決定，
查到升級確實對記憶力/穩定度/安全性都有實質改善——「Memory, sessions, and state」105個PR修一致性、
Gateway crash loop修復、憑證安全加固，三個教練在乎的面向都命中，判斷值得升級）。

**執行時真的造成一次短暫服務中斷**：新版要求node版本區間`>=22.22.3<23`或`>=24.15.0<25`或
`>=25.9.0`，但gateway服務實際使用的`/opt/homebrew/opt/node`是25.6.1，剛好卡在25.0~25.9這個
不支援的空隙，導致`openclaw doctor`後置檢查失敗，gateway service真的停在stopped狀態
（LINE/Telegram一度真的連不上），不是嘴上說"可能失敗"。已立刻`npm install -g openclaw@2026.6.33`
回滾+`openclaw daemon restart`恢復服務，`openclaw status --deep`確認Telegram/LINE皆OK後才算數。

**過程中又踩到一次已知的雙node環境坑**（見[[reference_mac_dual_node_environment]]）：
第一次執行rollback用`npm install`（PATH解析到`.hermes/node`底下的npm），裝到假地方，
gateway實際用的`/opt/homebrew/lib/node_modules/openclaw`沒被改到，白忙一次還多產生一包垃圾。
改用完整路徑`/opt/homebrew/bin/npm install -g openclaw@2026.6.33`才是真的改到gateway吃的那份。

**下次要再嘗試升級OpenClaw前，必須先確認**：
1. `/opt/homebrew/opt/node/bin/node --version`（gateway managed service實際用的node）是否落在
   支援區間，不落在的話要先`brew upgrade node@22`或`brew install node@24`並確認gateway改用
   正確路徑，再跑`openclaw update --dry-run`預覽
2. rollback/install openclaw一律用`/opt/homebrew/bin/npm`完整路徑，不要用PATH解析到的npm
3. `openclaw update`本身有內建doctor自檢+失敗自動嘗試恢復舊service，但不保證恢復成功
   （這次就是失敗恢復後gateway仍是stopped，需要人工確認`openclaw status --deep`才知道真相）

相關記憶：[[reference_mac_dual_node_environment]]
