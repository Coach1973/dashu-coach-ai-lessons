# Telegram Mac 本機快取路徑（三助教共用鐵律）

> 寫入日期：2026-05-20
> 觸發原因：教練傳照片到 Telegram，助教找錯地方（去找 OpenClaw inbound），浪費大量時間。

---

## ✅ 正確路徑

### Telegram App 快取媒體（圖片、影片等）
```
~/Library/Group Containers/6N38VWS5BX.ru.keepcoder.Telegram/appstore/account-10349041466821441817/postbox/media/
```

### 找最新收到的圖片（終端機指令）
```bash
find ~/Library/Group\ Containers/6N38VWS5BX.ru.keepcoder.Telegram/appstore/account-*/postbox/media \
  -type f -not -name "*_partial*" -not -name "*.meta" \
  -newer ~/Library/Group\ Containers/6N38VWS5BX.ru.keepcoder.Telegram/appstore/account-*/postbox/media/../db/db_sqlite \
  | xargs ls -lt 2>/dev/null | head -20
```

---

## ❌ 錯誤路徑（不要再去這裡找 Telegram 照片）

| 錯誤位置 | 說明 |
|------|------|
| `~/.openclaw/media/inbound/` | OpenClaw bot 自動下載的，不是 Telegram App 快取 |
| VPS `/home/node/.openclaw/media/inbound/` | 雲端主機，跟 Mac 本機 Telegram 完全無關 |

---

## 標準作業流程（SOP）

教練說「我傳照片到 Telegram」時，正確步驟：

1. **截圖確認**：先截圖看 Telegram 對話框，確認照片已顯示
2. **去快取資料夾抓**：用上方路徑找最新的 `telegram-cloud-photo-size-*` 檔案
3. **讀圖確認**：用 Read 工具看圖，確認哪張是什麼內容
4. **推上 GitHub**：複製到目標倉庫，commit & push

整個流程不需要教練做任何事。

---

## 注意事項

- 檔案名稱沒有副檔名，但內容是 JPEG（header `ffd8 ff`）
- `_partial` 結尾的是還沒下載完的，跳過
- `.meta` 結尾的是描述檔，不是圖片
- 同一張圖可能有多個尺寸版本（`-x`、`-y`、`-w`），選最大的
