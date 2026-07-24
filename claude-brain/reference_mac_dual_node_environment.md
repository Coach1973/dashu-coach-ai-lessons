---
name: mac-dual-node-environment
description: 這台Mac有兩套獨立node/npm（.hermes/node排PATH第一個 vs /opt/homebrew是gateway服務實際用的），任何openclaw gateway/update層級指令執行前要先確認用對路徑
metadata: 
  node_type: memory
  type: reference
  originSessionId: f3c850ef-8e4e-4a89-aaad-d65fdb8d3bf9
  modified: 2026-07-24T00:20:29.361Z
---

2026-07-24更新OpenClaw從6.11到6.33時發現：這台Mac終端機shell的`which node`/`which npm`預設指向`/Users/bymyway/.hermes/node`，但OpenClaw gateway服務（LaunchAgent）實際固定用`/opt/homebrew/opt/node/bin/node`。

**踩過的坑**：
1. `openclaw update --tag <dist-tag>` 內部呼叫npm時用了hermes那套，裝完後`/opt/homebrew/bin/openclaw`完全沒變版本——要改用`/opt/homebrew/bin/npm install -g openclaw@<version>`明確指定正確npm才會裝到gateway真正在用的地方。
2. `openclaw gateway install --force`重裝LaunchAgent時，若shell當下PATH第一個是hermes的node，產生的plist會指向錯的node路徑，導致服務描述文件（Command行）跟原本不一致。要用`PATH="/opt/homebrew/opt/node/bin:/opt/homebrew/bin:$PATH" openclaw gateway install --force`強制指定。

**How to apply**：以後任何會動到gateway服務層級的指令（`openclaw gateway install`、`openclaw update`、`openclaw gateway restart`背後如果牽涉重裝），執行前先跑`which node`確認是不是`/opt/homebrew`那套，不是的話要在指令前明確加`PATH=...`，不能信賴shell預設PATH順序。`openclaw gateway status`的「Command:」那一行是驗證node路徑對不對的最快方式。

Related: [[project_openclaw_update_2026-07-24]]
