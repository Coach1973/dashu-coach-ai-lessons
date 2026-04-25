# Session 與記憶管理經驗

## 最常踩的坑：改了設定沒有重啟

修改 SOUL.md、AGENTS.md 等設定後，必須：

```bash
# 1. 清除 session 快取
rm -f ~/.openclaw/agents/main/sessions/*.jsonl
echo '{}' > ~/.openclaw/agents/main/sessions.json

# 2. 重啟服務
launchctl kickstart -k system/com.openclaw.bot.main
```

不清快取 = 白改，bot 仍讀舊版設定。

## hook 優先級

`bot-relay-inbound/handler.js` 注入的身份 > SOUL.md 的設定。

修改身份時，兩個地方都要改：
1. `SOUL.md`
2. `hooks/bot-relay-inbound/handler.js` 的注入文字

## 記憶讀取順序（OpenClaw 1號機）

1. SOUL.md（人格）
2. workspace/shared-context/SUPERGROUP-MAP.md（團隊）
3. workspace/USER.md（服務對象）
4. workspace/memory/YYYY-MM-DD.md（當天記憶）
