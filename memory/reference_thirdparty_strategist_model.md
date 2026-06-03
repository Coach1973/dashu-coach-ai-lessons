# 🔴 第三方軍師模型接入（命名定稿）

**時間**：2026-06-03 19:34
**教練拍板**：「以後這個模型就叫做第三方軍師模型接入」
**Commit**：`d3978d2f`

## 命名定義
- **正式名稱**：第三方軍師模型接入
- **角色定位**：軍師（限流稀缺資源，只做判斷，不做執行）
- **底層模型**：minimax/MiniMax-M3（具體模型版本，視教練測試切換）

## 接入架構
```
Claude Code CLI / OpenClaw Agent
       ↓
~/.claude/settings.json
       ↓
ANTHROPIC_BASE_URL=http://127.0.0.1:15721
ANTHROPIC_AUTH_TOKEN=PROXY_MANAGED
       ↓
本地代理（127.0.0.1:15721，密鑰由代理託管）
       ↓
第三方模型 API（minimax/MiniMax-M3）
```

## 關鍵設計
- 觸發 API Key（密鑰由本地代理託管，不入 settings.json 明文）：
  `sk-214c4a9c3419d81a459cb8c59e82ff46d1f72ba6fc421648d16a98c0defa85c8`
- PROXY_MANAGED = 標記位，代表「由本地代理負責實際金鑰輪替與配額」
- 不直接把 sk-... 寫入 settings.json，避免日誌/截圖洩漏

## settings.json 驗證（2026-06-03 cat 結果）
```json
"env": {
  "ANTHROPIC_AUTH_TOKEN": "PROXY_MANAGED",
  "ANTHROPIC_BASE_URL": "http://127.0.0.1:15721",
  "API_TIMEOUT_MS": "3000000",
  "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
}
```
✅ 兩個關鍵欄位都正確

## 與 OpenClaw 2026.5.28 升級的關係
- OpenClaw 2026.5.28 升級時，memsearch 插件被移除（不相容）
- 第三方軍師模型接入是獨立的命名/架構議題，跟 memsearch 移除是兩件事
- 但兩者都在 2026-06-03 同日發生，屬於同一次系統調整

## 用語約定
- 之後對教練/文件提到「這個模型」時，正稱 = **第三方軍師模型接入**
- 底層具體模型版本 = `minimax/MiniMax-M3`（可切換）
- 「軍師」= 此模型在團隊架構中的角色名（與學弟/學妹平輩）
