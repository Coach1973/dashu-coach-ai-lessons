# 聯想→Mac：結繩領導學工作坊戰報系統，程式碼已完成，待Mac部署上線

> 建立時間：2026-07-26 03:03（台灣時間）
> 寄件：聯想（Windows）Claude Code Sonnet 5
> 收件：Mac 軍師（下一場開工請處理）

## 背景

教練 2026-07-25 深夜親口交辦：要做「結繩領導學工作坊」台南／台中／台北三場的即時戰報，追蹤誰報名、誰繳費/未繳費。教練確認比照 `mentor100.bymyway.com` 模式——**純手動輸入，工作人員直接在後台打字，不接LINE不接Google表單**。

## 這台 Windows 已完成的部分（commit `53f9b4a7`，已push）

`mac-openclaw-workflows/jiesheng-report/` 完整程式碼：
- Flask + SQLite，架構沿用 `event-signup` 的 schema自動升級寫法＋session帳密登入模式
- 單一 `registrants` 表（姓名／電話／報名日期／已繳費／繳費方式ATM|PAYUNi|其他／金額／備註）
- 三城市分頁戰報頁（`/admin?workshop=台南|台中|台北`），每頁頂部統計卡（報名/已繳/未繳人數），新增報名者表單，每列可勾選繳費+編輯+刪除
- **本機已用 `smoke_test.py` 完整驗證**：登入／新增／勾選繳費／統計即時反映／三城市互不干擾／刪除，全部PASS（見同資料夾這支腳本，部署後也可以直接對正式網址跑一次確認沒壞）
- 完整部署SOP寫在 `jiesheng-report/README.md`，含LaunchAgent plist範例、環境變數清單、Cloudflare Route設定步驟

## Mac 這邊要做的事（README.md 有完整版，這裡列重點）

1. `git pull` 拿到 `jiesheng-report/` 資料夾
2. 建 venv 裝 `requirements.txt`（Flask/Werkzeug）
3. 設定環境變數，**教練已定案，密碼雜湊值直接複製用，不用重新產生**：
   - `JIESHENG_SECRET_KEY`：隨機字串（自己產生，例如 `openssl rand -hex 32`）
   - `JIESHENG_ADMIN_USER`：`staff`
   - `JIESHENG_ADMIN_PASSWORD_HASH`：`scrypt:32768:8:1$uxXZ8x5sRmBQ97XV$3a8e071bf28e76526543e1599977f67f1d04351243f9d42497ab74948c5c4f0aba33a2342f0091f1b825b4e6a6cce7035d5f92f07a650e6350bee5856ec10022`（明文是教練公司統編，教練自己知道，只存雜湊值不進任何檔案）
   - `JIESHENG_PORT`：預設5061
4. 沿用既有 tunnel `openclaw-macmini` 加一條新 Route（比照 `bni.bymyway.com` 做法）——subdomain **`rpl-workshop`**（教練已定案），domain `bymyway.com`，service指向 `http://localhost:5061`
5. LaunchAgent 常駐（比照 `com.coach.event-webapp.plist`）
6. 上線後拿正式網址跑一次 `smoke_test.py`（設 `JIESHENG_TEST_BASE=https://rpl-workshop.bymyway.com`）確認沒壞

## 為什麼沒有直接在Windows部署完

查證確認這台聯想電腦沒有裝 cloudflared、也沒有任何 `bymyway.com` 子網域的能力——`~/.cloudflared/` 設定只存在Mac，所有 `xxx.bymyway.com` 網域都是Mac那顆 `openclaw-macmini` tunnel在管。所以只能做到「程式碼完整寫好＋本機測試證明邏輯正確」，最後一步的對外開通需要Mac這邊接手，跟 event-signup／mentor100／bni.bymyway.com 都是同樣的分工模式。

## 網域+密碼教練已定案（2026-07-26，README.md已同步更新）

- 網址：`https://rpl-workshop.bymyway.com`
- 工作人員密碼：公司統編（教練口頭指定，雜湊值見上方，明文不進任何檔案）
