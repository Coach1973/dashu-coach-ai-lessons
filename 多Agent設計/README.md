# 多 Agent 設計經驗總結

## 核心原則

### 跨進程通訊唯一正確方式：共享檔案

三機（OpenClaw 1/2/3號機）是獨立進程，**sessions_send 無法跨進程路由**。

正確做法：寫入共享檔案 `BOT_RELAY.json`，由 cron 每分鐘輪詢。

```json
{
  "messages": [{
    "id": "唯一id",
    "from": "學長",
    "bot": "2",
    "content": "任務內容",
    "status": "pending"
  }]
}
```

### Turn-Taking Protocol

同一話題連續發言超過 3 次，停止等人類裁決。防止無限循環。

### 每次發言結尾標記

- `[完成，等待回應]` — 需要下一棒接話
- `[完成，無需回應]` — 自己是最後一棒
- `[轉交 @xxx]` — 明確交給下一棒
