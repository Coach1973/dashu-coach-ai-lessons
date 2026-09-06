---
name: reference-bni-guest-dashboard-weekly-update-sop-2026-09-07
description: 真鑫/真鑽/真貴三個BNI分會來賓戰情儀表板，每週填來賓/1對1/咖啡會議數據的SOP，軍師/Hermes/小龍蝦皆可直接執行
metadata:
  type: reference
---

# 三分會來賓戰情儀表板・每週數據更新SOP（2026-09-07教練交辦，查證後確認可完全委派）

三個系統，同架構(Flask+SQLite)，不同repo/port/網域：

| 分會 | repo（`~/github_repos/`下） | DB檔案 | port | 正式網址 |
|---|---|---|---|---|
| 真鑫 | `zhenxin-guests` | `zhenxin_guests.db` | 5092 | https://zhenxin.bymyway.com |
| 真鑽 | `zhenzuan-guests` | `zhenzuan_guests.db` | 5093 | https://real-diamonds.bymyway.com |
| 真貴 | `zhengui-guests` | `zhengui_guests.db` | 5094 | https://real-wealth.bymyway.com |

⚠️ 三個系統各自獨立DB，同一位會員在不同分會的`member_id`不同，不要跨系統套用同一個id。

## 1對1(ones)／咖啡會議(coffee)：走公開API，curl即可，完全不用碰資料庫

```bash
curl -s -X POST https://zhenxin.bymyway.com/api/update_metric \
  -H "Content-Type: application/json" \
  -d '{"member_id": <整數>, "week_date": "YYYY-MM-DD", "metric": "ones", "value": <整數>}'
```
`metric`只能是`"ones"`或`"coffee"`（`db.MEMBER_EDITABLE_METRICS`寫死，`guests`故意不開放這條路，見下方原因）。
`member_id`查法：`sqlite3 ~/github_repos/<repo>/<db>.db "SELECT id, name FROM members"`。
`week_date`必須已存在於`weeks`表且`is_active=1`，否則回400「此週次不開放填寫」（見下方「開新一週」）。
此API本來就是公開、無需登入的（member自填用），三個分會格式完全一致。

## 來賓數(guests)：不開放公開API，改直接寫資料庫

教練/軍師past做法就是這樣——來賓數字來自BNI Connect官方報表，不是會員自填，所以`db.MEMBER_EDITABLE_METRICS`刻意排除`guests`。任何有終端機能力的AI（軍師/Hermes/小龍蝦，都在同一台Mac，都能碰這些DB檔案）可以直接寫：

```bash
sqlite3 ~/github_repos/zhenxin-guests/zhenxin_guests.db \
  "INSERT INTO weekly_data (member_id, week_date, guests) VALUES (<id>, '<week_date>', <count>)
   ON CONFLICT(member_id, week_date) DO UPDATE SET guests=excluded.guests;"
```

受邀來賓名單（首頁會列出當週實際受邀來賓的姓名/專業/邀請人，`guest_list`表）：

```bash
sqlite3 ~/github_repos/zhenxin-guests/zhenxin_guests.db \
  "INSERT INTO guest_list (week_date, name, profession, inviter) VALUES ('<week_date>', '<姓名>', '<專業>', '<邀請人>');"
```

## 開新的一週：`weeks`表要先有這筆才能填數據

```bash
sqlite3 ~/github_repos/zhenxin-guests/zhenxin_guests.db \
  "INSERT INTO weeks (week_date, label, is_active, sort_order) VALUES ('<date>', '<顯示標籤，如9/8這週>', 1, <排序數字，通常比目前最大值+1>);"
```

## 改完要重啟服務嗎？

**不用**——Flask每次網頁請求都是即時查DB，資料庫寫入後立刻反映在網頁上，不需要`launchctl kickstart`。

## 驗證方式（不能只信SQL/curl回傳成功）

改完直接curl該分會首頁確認數字/名單真的顯示出來，例如：
```bash
curl -s https://zhenxin.bymyway.com/ | grep -A2 "<會員姓名>"
```

## How to apply
教練把最新一週的來賓/1對1/咖啡會議數據丟給任何一個AI（軍師/Hermes/小龍蝦），照上面步驟直接動手即可，不用等軍師才能處理。三個分會格式一致，處理完一個分會可以照抄同一套流程換DB路徑跑另外兩個。
