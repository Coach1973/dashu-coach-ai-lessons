# 三機身份定義修復過程報告（2026-04-25）

## 問題描述

教練在「頂級特助分工群」對 @openclaw_macbook4_bot、@CoachWu_openclaw_bot、@coachwu_lenovo_bot 三個 bot 宣布「本群一律禁用語音，立即執行」，引發一連串診斷和修復。

---

## 修復過程記錄

### 第一階段：禁用語音（10 分鐘）

**問題**：TTS 語音功能未關閉  
**原因**：`openclaw.json` 沒有 `messages.tts` 設定  
**操作**：`openclaw config set messages.tts.enabled false`  
**結果**：✅ 寫入成功，gateway 重啟生效

---

### 第二階段：Group Policy not-allowed（30 分鐘）

**問題**：三個 bot 在群組出現 `reason: "not-allowed"` 阻擋  
**原因**：`channels.telegram.accounts` 下的 `groupPolicy` 設定不正確  
**操作**：在 `bot_main`、`bot_kong`、`bot_peipei` 三個帳號下，分別加入 `groupPolicy: "open"` 和 `groups: {"-1003877502911": {requireMention: true}}`  
**結果**：✅ Logs 從 `not-allowed` 變成 `no-mention`，bot 不再被 groupPolicy 阻擋

---

### 第三階段：requireMention 改為 false（20 分鐘）

**教練決策**：把 `requireMention` 改成 `false`，讓三個 bot 都能看到所有群組訊息

**操作**：
```bash
openclaw config set channels.telegram.accounts.bot_main.groups."-1003877502911".requireMention false
openclaw config set channels.telegram.accounts.bot_kong.groups."-1003877502911".requireMention false
openclaw config set channels.telegram.accounts.bot_peipei.groups."-1003877502911".requireMention false
```

**發現新問題**：Telegram Bot API privacy mode 阻擋——需要在 BotFather 關閉三個 bot 的隱私模式

**操作**：教練親自透過 GUI 在 BotFather 操作，三個 bot 都設為 `Privacy mode disabled`  
**結果**：✅ 三個 bot 都能收到所有群組訊息

---

### 第四階段：三機身份錯亂（核心問題）——多次修正失敗

**問題**：kong 和 peipei 被問「你是誰」時，都回答自己是「1號機學長」

#### 修正嘗試 1（失敗）
- **操作**：更新 `~/.openclaw/agents/kong/SOUL.md` 和 `~/.openclaw/agents/peipei/SOUL.md`
- **失敗原因**：kong/peipei 的 SOUL.md 路徑當時寫對了，但 session transcript 裡殘留舊認知

#### 修正嘗試 2（失敗）
- **操作**：清除 `~/.openclaw/agents/kong/sessions/` 和 `~/.openclaw/agents/peipei/sessions/`
- **失敗原因**：同時也清除了 `sessions.json`，導致配對丟失

#### 修正嘗試 3（失敗）
- **操作**：peipei 重新配對（`openclaw pairing approve telegram Q7C8RYLR`）
- **失敗原因**：peipei 的 session 再次建立時讀到舊 SOUL.md 認知

#### 修正嘗試 4（失敗）
- **操作**：寫入 `~/.openclaw-kong/SOUL.md` 和 `~/.openclaw-peipei/SOUL.md`（教練身份表提供的舊路徑）
- **失敗原因**：這些是舊獨立 gateway 的路徑，統一 gateway 不讀取這些路徑

#### 最終成功修正（正確路徑）
- **操作**：寫入統一 gateway 的正確 workspace 路徑
  - main：`~/.openclaw/workspace/SOUL.md`
  - kong：`~/.openclaw/agents/kong/SOUL.md`
  - peipei：`~/.openclaw/agents/peipei/SOUL.md`
- **同步操作**：
  1. 備份三個 SOUL.md
  2. 用 `>` 完全覆蓋（不是 `>>` 追加）
  3. 清除舊 session transcript（`.jsonl` 和 `sessions.json`）
  4. `openclaw gateway restart`

---

## 關鍵發現：為什麼之前修正失敗

### 失敗原因 1：路徑混淆
- **舊路徑**（獨立 gateway）：`~/.openclaw-kong/`、`~/.openclaw-peipei/`
- **新路徑**（統一 gateway）：`~/.openclaw/agents/kong/`、`~/.openclaw/agents/peipei/`
- **問題**：當初更新的是舊路徑，但統一 gateway 讀取的是新路徑，所以更新完全沒生效

### 失敗原因 2：Session Transcript 殘留認知
- **原因**：即使 SOUL.md 寫對了，舊的 session transcript 裡已經有「我是1號機」的認知，agent 啟動時優先讀取 session 歷史
- **解決**：必須同時清除 session transcript（`.jsonl` 檔案）

### 失敗原因 3：追加而非覆蓋
- **原因**：一開始用 `>>`（追加）而不是 `>`（覆蓋），導致舊的「我是學長」定義排在前面，被優先採用
- **解決**：用 `>` 完全覆蓋

---

## 正確的三機身份定義（最終版）

| 項目 | 1號機（學長） | 2號機（學弟） | 3號機（學妹） |
|------|--------------|--------------|--------------|
| 暱稱 | 小龍蝦學長 | 小龍蝦學弟 | 小龍蝦學妹 |
| Telegram Bot | @openclaw_macbook4_bot | @CoachWu_openclaw_bot | @coachwu_lenovo_bot |
| 服務對象 | 大樹教練 | 孔大哥（峰哥） | 佩佩老師 |
| 角色定位 | 統籌指揮 | 執行者 | 執行者 |
| SOUL.md 路徑 | `~/.openclaw/workspace/SOUL.md` | `~/.openclaw/agents/kong/SOUL.md` | `~/.openclaw/agents/peipei/SOUL.md` |
| Session 路徑 | `~/.openclaw/agents/main/sessions/` | `~/.openclaw/agents/kong/sessions/` | `~/.openclaw/agents/peipei/sessions/` |

---

## 最終設定狀態

### Config 設定
- `requireMention: false`（三個 bot 都能看到所有群組訊息）
- `groupPolicy: "open"`（群組政策開放）
- `tools.agentToAgent.enabled: true`（啟用跨機溝通）
- `messages.tts.enabled: false`（語音功能已停用）

### 協作模式（Hub Pattern）
- 學長（main）在群組公開回應教練
- 學弟和學妹透過 `sessions_send` / `sessions_spawn` 跟學長溝通，不在群組公開發言
- 共享資訊寫入 shared memory

---

## Git Commit 歷史（本對話框）

- `6e8437e` — Add coach identity confirmation and 4 core rules to USER.md

---

## 待解決問題

1. **Bot 隱私模式 Warning 仍在**：OpenClaw status 仍顯示 privacy mode warning，但 BotFather 端已確認三個 bot 都是 `disabled`。這是 OpenClaw 的靜態提示，應該是已修復但 warning 未更新。

2. **peipei 專屬群組**：`bot_peipei` 還有另一個群組 `-5115910257`（佩佩老師的小龍蝦助理）尚未確認是否正常運作。

---

## 結論

三機身份問題的核心是**路徑混淆**——統一 gateway 後，kong/peipei 的 workspace 從 `~/.openclaw-kong/` / `~/.openclaw-peipei/` 合併到了 `~/.openclaw/agents/{kong,peipei}/`。所有修正都必須針對新路徑執行，同時清除 session transcript 才能讓新規則生效。
