---
name: Hermes 切回 MiniMax 暗號與執行步驟
description: 教練說「Hermes 切回 MiniMax」或「Hermes 切換為 MiniMax API key」時，立刻執行以下步驟，不需確認
type: project
originSessionId: 0d047e5b-f32f-438b-bf9b-ee1440e905b1
---
## 觸發語（任何一句都算）
- 「Hermes 切回 MiniMax」
- 「Hermes 切換為 MiniMax API key」
- 「切回 MiniMax」（語境明確指 Hermes）

## 背景
aiprimetech 帳號到期時間：2026-05-17 約 13:00
到期後 proxy 失效，需切回 MiniMax。

**Why:** 教練明確說過，到了時間點可能已歷經多個工作流程、上下文切換，怕我忘記；要我主動記住並無需確認直接執行。

**How to apply:** 收到暗號後立刻執行下方三步驟，完成後回報結果。

## 執行步驟（直接做，不問教練）

### 第 1 步：改 config.yaml
檔案：`~/.hermes/config.yaml`

改成：
```yaml
model:
  default: claude-opus-4-7
  provider: minimax
  api_mode: anthropic_messages
custom_providers:
- name: minimax
  base_url: https://api.minimax.io/anthropic
  key_env: MINIMAX_API_KEY
  api_mode: anthropic_messages
```
（把 aiprimetech provider 那條拿掉或留著都行，provider 改 minimax 是關鍵）

### 第 2 步：清 auth.json exhausted
用 Python 把 anthropic pool 裡的 last_status 從 "exhausted" 改回 null：
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/Users/bymyway/.hermes/auth.json')
d = json.loads(p.read_text())
for c in d.get('anthropic', []):
    if c.get('last_status') == 'exhausted':
        c['last_status'] = None
p.write_text(json.dumps(d, indent=2))
print('cleared')
"
```

### 第 3 步：確認 LaunchAgent 自動重啟（已裝好）
LaunchAgent `ai.hermes.config-watcher` 監視 config.yaml，改完會自動 kill + 重啟 hermes-bg tmux session。
只需確認日誌有寫入：`tail -5 ~/.hermes/logs/config-watcher.log`

## MiniMax 憑證位置（已備好）
- `.env` 裡：`MINIMAX_API_KEY=sk-cp-0_iW72rvu...`
- `auth.json` minimax 條目：`base_url=https://api.minimax.io/anthropic`，`last_status=null`
- MiniMax base_url 帶 /anthropic 後綴，Hermes 自動識別 anthropic_messages mode
- MiniMax 不需要 x-stainless-* header 過濾（直接允許）
