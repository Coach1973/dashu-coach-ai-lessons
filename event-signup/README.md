# 活動報名系統（event-signup）

> 教練 2026-07-12 構想：來賓掃 QR → 留基本資料 → 進來賓名單系統，之後辦活動持續通知。
> 架構完全比照名片系統（namecard-db）：Mac 資料庫 + Flask 網頁 + 獨立 Cloudflare Tunnel。

## 網址

- 報名頁：`https://event.bymyway.com/e/<活動代號>`（例：`/e/ai-talk-0729`）
- 教練後台：`https://event.bymyway.com/admin?key=<管理密鑰>`（密鑰在 `.env`，不進版本庫）
- 名單下載：後台頁面上的「下載名單」按鈕（CSV，Excel 直接開）

## 來賓流程

掃 QR → 填姓名/手機/公司職稱（30秒）→ 感謝頁 → 加 LINE 好友（`@qaw8118h`，之後活動群發通知）

## 去重邏輯

- 手機號正規化後（只留數字、+886 轉 0）當同一人的身分證
- 同一人報不同場 → 名單只有一筆，活動記錄累加
- 同一人同一場重複填 → 顯示「您已完成報到」，不重複記錄

## 常駐服務（比照名片系統，KeepAlive 開機自動跑）

| LaunchAgent | 作用 |
|---|---|
| `com.coach.event-webapp.plist` | Flask 網頁，port 5060 |
| `com.coach.event-tunnel.plist` | Cloudflare Tunnel `event-app`（獨立通道，跟 LINE 專線、名片通道互不影響） |

通道設定：`~/.cloudflared/event-config.yml`（tunnel id `739a34e4`）

## 辦新活動 SOP

```bash
cd ~/.openclaw/workspace/event-signup
# 1. 建活動（slug 用 英文-月日）
./venv/bin/python3 -c "
import db; conn = db.get_conn()
conn.execute(\"INSERT INTO events (slug, name, event_date) VALUES ('新代號', '活動名稱', '2026-MM-DD')\")
conn.commit(); conn.close()"
# 2. 產 QR + A4 立牌頁
./venv/bin/python3 make_qr.py 新代號
# 3. qr/新代號-print.html 用 Chrome 開 → 列印成立牌
```

## 檔案

- `app.py` 網頁主程式｜`db.py` 資料庫｜`schema.sql` 表結構｜`make_qr.py` QR 產生器
- `templates/` 報名頁(form)、感謝頁(thanks)、後台(admin)——黑金風格，Noto Sans TC
- `event.db` 來賓資料庫（不進版本庫）｜`qr/` QR 圖與立牌頁
