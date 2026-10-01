# 封存：v263 聯想 Windows 棒（2026-10-02 00:25，RustDesk Tailscale 直連＋單檔 HTML 作品 ema1017）

## 🔴 給跨對話框軍師讀的總結摘要（2026-10-02 00:25 台灣時間，聯想 Windows 桌面版 Sonnet 5.5，v263，教練在聯想前）

**主軸：①RustDesk 改走「Tailscale IP 直連」繞過官方壞掉的中繼；②教練單檔 HTML 作品放到 event.bymyway.com/curated/ema1017/，並教會赫米斯做法。**

### 1. RustDesk 直連（取代官方中繼 21117 故障）
- 官方 21117 仍不通（21:40 與 00:10 重測皆 False），21116 通所以顯示「已就緒」是假象。
- 做法：被連方 RustDesk 開「啟用 IP 直接存取」（埠 21118，需解鎖/系統管理員，AI 無法代做），連線方在遠端 ID 欄輸入對方 Tailscale IP。Mac=100.91.228.91（聯想→Mac 教練實測連上）；聯想=100.95.122.29（教練已手動開）；ACER=100.78.106.14（21:45 已開、防火牆只放 Tailscale 網段）。固定密碼教練早已設好，不要再提「缺密碼」。
- 聯想→ACER 與 ACER→Mac 教練尚未回報實測；00:10 從聯想測 ACER 21118 為 False（ACER 當時可能睡眠/離線，Tailscale 顯示離線）。
- 5 封來信（Mac/ACER）已歸檔；Mac 22:10 那封已被 21:12 取消信作廢。
- 教訓：給 ACER 的信第一次誤放 outbox（應放 inbox/acer/），ACER 讀不到，教練回報才發現。

### 2. 單檔 HTML 作品（教練說「大樹作品SOP」）
- 教練丟 `design (1).html`（中華網紅協會零基礎學AI課 10/17），赫米斯說只收 zip。已完成：網名由教練指定 **ema1017**，https://event.bymyway.com/curated/ema1017/ （首頁與 4 張圖都 200；Telegram 通知教練已收到）。
- 做法與坑已寫進 `knowledges/SOP_教練個人創作上架event.bymyway.com不進商圈.md`（2026-10-02 新增段）：自己打包 zip、外連圖片必須下載（Lovart 4張約13.8MB）、圖片比首頁晚 1~2 分鐘才可讀、短網址撞名要先下架自己舊版。
- 已下架我自己傳錯的 `ai-class-1017`（教練同意）與第一版 ema1017。
- 已寫信給赫米斯：`cross-agent/inbox/hermes/20261002-0020_...`（含可複製的 Python 腳本）。
- 殘留：`E:\Claude-Data\` 有 ai-class-1017.zip／ema1017.zip／pk2／zpk／cookie.tmp（刪檔鎖擋，待教練同意清理）。

### 📋 下一場先做
1. 教練回報 聯想→ACER、ACER→Mac 實測結果；ACER 離線就等它醒來再測 `Test-NetConnection 100.78.106.14 -Port 21118`。
2. 簡報 BNI版 三份：底部字幕被左下 LOGO 蓋住，教練還沒決定「照現狀」或「有字幕頁內縮排版」（v262 遺留）。
3. 官方 RustDesk 中繼 21117 修好後再驗證。

---

