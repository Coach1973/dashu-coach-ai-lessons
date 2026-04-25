# 2026-04-26 Hub Pattern 三機架構建立

## 背景
三隻小龍蝦（main、kong、peipei）在各自的 Telegram 對話框正常運作，但彼此無法順暢互動，且身份認知錯亂（全部自稱「學長」）。

## 根本原因
1. **路徑錯誤**：一直更新舊的 standalone 路徑（`~/.openclaw-kong/`、`~/.openclaw-peipei/`），而統一 gateway 實際讀取的是 `~/.openclaw/agents/kong/` 和 `~/.openclaw/agents/peipei/`
2. **BOOTSTRAP.md 未刪除**：這個「出生證明」檔案存在時，bot 會強制執行「我是誰」初始化流程，忽略 SOUL.md 規則
3. **Session 快取問題**：修改檔案後未重啟 gateway，舊 session 仍使用舊內容

## 解決方案
1. 刪除 BOOTSTRAP.md（每台機器都要刪）
2. 在正確路徑寫入完整的 USER.md、memory/people.md、MEMORY.md
3. 在 SOUL.md 加入「啟動必讀」段落
4. 重啟 gateway

## 最終架構（Hub Pattern）
- **main（學長）**：統籌指揮，唯一在群組公開回應教練
- **kong（學弟）**與 **peipei（學妹）**：只透過 agentToAgent 跟學長溝通，不在群組公開發言
- shared memory 作為共同中樞

## 教訓
- 修改前一定要確認 bot 實際讀取的 workspace 路徑（用 `openclaw status` 查詢）
- BOOTSTRAP.md 存在就會強制初始化，必須刪除
- 修改完一定要重啟 gateway
- 三機的名稱與番號必須與 SUPERGROUP-MAP.md 完全對應，不可任意變動
