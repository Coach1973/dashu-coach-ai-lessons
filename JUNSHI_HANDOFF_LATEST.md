# 軍師接力棒 · 2026-06-16 v25（Opus 4.7 終端機 session）

> 建立時間：2026-06-16 凌晨 3:20 台灣時間
> 本棒執行者：Opus 4.7（教練 Mac mini 終端機）
> 上一棒：v24（同 session 內升級，因半夜出血淚教訓需要立刻封存）

---

## 🎯 本場成果（一晚從零到上線 + 兩個重大血淚封存）

### 1. AI 導入教練品牌頁 `bymyway.com/ai/` 正式上線

**頁面結構**：Hero / PROLOGUE / 7 章 / EPILOGUE / 核心思想 / 守則金句 / FAQ / CTA / Footer
**Navbar 9 項常駐**：叫 AI 做什麼 · 為什麼是他？ · 零基礎開始 · 心酸血淚史 · 讓 AI 成為特助 · 核心思想 · 守則金句 · 常見問題 · 乾淨世界 · 立即聯繫
**8 張形象照**（左圖右文雙欄）
**核心金句**：「我不教你怎麼用 AI，我教你怎麼帶 AI」
**核心思想**：教練 2026-06-04 西洋棋規則比喻 → 「給 AI 完善的規則書，便宜模型也能跑出世界級輸出」

**部署架構**：
- **內容源**：`coach1973.github.io/bymyway-website/ai.html`（GitHub Pages）
- **外殼**：`bymyway.com/ai/`（WordPress page ID 27382，純 iframe + OG meta，elementor_canvas）
- **iframe 寫法**：`height: 100vh`（不是 min-height！）——抄 `bymyway.com/coach/` 同款架構
- **改 ai 頁面 = 改 GitHub Pages 就好**

### 2. 🔴🔴🔴 SOP_bymyway_auto_site.md v3.4 永久封存兩道鐵律

**v3.3（凌晨 2:35）**：wpautop 大片空白
- WordPress wpautop filter 把 `\n` 轉 `<br />`、把 iframe 包進 `<p>`
- 解：content 單行字串拼接 + `<div>` 包整段
- 教練罵 4 次後封存

**v3.4（凌晨 3:15）**：「重新發明」血淚教訓
- 軍師給 ai 頁設 iframe `min-height:7500px` → iframe 不滾 → fixed navbar 被推走 + anchor 失效 + Hero 黑色空白
- 教練質問：「為什麼不去看 `bymyway.com/coach/` 怎麼做？」→ curl 看才知答案就一行 `height:100vh`
- 解：**新增步驟 0「OPE 先驗法」**——動手前必 curl 已成功案例
- 代價：浪費教練 28% 流量 + 凌晨 3 點沒睡

---

## 🔴🔴🔴 給下一棒的最高優先鐵律（不可違反）

### 做任何自動站動作前，先跑 SOP「步驟 0：OPE 先驗法」

```bash
# 1. 看「已成功上線」的 bymyway 子頁是怎麼做的
curl -sL "https://www.bymyway.com/coach/" > /tmp/ope_reference.html

# 2. REST API 看 content 真實結構
curl -s "https://www.bymyway.com/wp-json/wp/v2/pages?slug=coach" | python3 -c "
import json,sys
p=json.load(sys.stdin)[0]
print(p['template'])
print(p['content']['rendered'])
"

# 3. 直接抄那個 iframe style，不要重新發明
```

### iframe 寫法鐵律
- ✅ `style="width:100%;height:100vh;border:none;display:block;"`
- ❌ `style="...min-height:7500px;..."`

---

## 📋 下一棒待辦

| 優先 | 任務 | 說明 |
|------|------|------|
| ✅ | ~~bymyway 主站加 /ai/ 導流入口~~ | 2026-06-16 03:35 完成——主選單加「教練創業之路」「AI 導入教練」兩項（v25 補完成） |
| ✅ | ~~LINE 預覽驗證~~ | 教練已確認沒問題（v25 補） |
| ✅ | ~~ai.html 手機版補三條橫線選單~~ | 2026-06-16 03:55 完成（commit e483d90） |
| ✅ | ~~刪 FB 每日生日祝福 cron~~ | 2026-06-16 10:00 完成（已轉交 Mac 版 H 特助） |
| ✅ | ~~11 個 cron 加 failureAlert:false~~ | 2026-06-16 10:00 完成——再也不會收 cron fail 通知 |
| ✅ | ~~新增「🦞 小龍蝦對話蒸餾（每4小時）」cron~~ | 2026-06-16 10:20 完成（每天 0:30/4:30/8:30/12:30/16:30/20:30，commit c4719f4） |
| ✅ | ~~桌面整理 + 43GB 釋放~~ | 2026-06-16 10:30 完成——本機可用 68→111 GB |
| ⏸ | 客戶見證區塊 | 教練 06-16 說「AI 那邊不需要顧客見證，還沒有」——暫緩 |
| ✅ | ~~H 的 gh auth 修復~~ | 2026-06-16 11:13 完成——真因是 hermes-agent 指向 NousResearch 開源 repo（非教練所有），push URL 改 no_push 防呆；workspace 本來就正常 |
| ✅ | ~~openclaw.json 髒改動處理~~ | 2026-06-16 11:11 完成——memorySearch provider=local + enabled=true（本機 embeddinggemma 模型，零 API 費用），commit 5e561e4 |
| 🟡 | jiesheng-leadership 金流就緒 | 暗號「恢復早鳥名額」→ cp 備份蓋回 |
| 🟢 | 本機 OpenClaw 2026.6.1 → 6.6 升級 | 教練本人已踩過 6.1 坑，沒急迫性；下次主動找時間 |
| 🔴 | **VPS 線上小龍蝦保持 2026.5.27 不升級** | 教練「比較少用」，5.27 已穩定跑 7 天 healthy；升 6.x 必踩教練親身踩過的 2026.6.1 兩道坑（外掛 activation + cron 孤兒，斷頭 4 天血淚） |

---

## 🔑 本場 commit hash

| commit | 內容 | repo |
|--------|------|------|
| `c140238` | 新增 ai.html + 7 張壓縮照片 | bymyway-website (master) |
| `04497f7` | RWD 全面強化（治標） | bymyway-website (master) |
| `ff17a0d` | Hero min-height 100vh→560px（治標） | bymyway-website (master) |
| `cfdf91f` | 🔴 最終修正：iframe height:100vh（抄 coach 頁面） | bymyway-website (master) |
| `1377c123` | SOP v3.3：wpautop 永久封存 | workspace (main) |
| `a1af021c` | SOP v3.4：OPE 先驗法 + iframe height:100vh 鐵律 | workspace (main) |
| WP `27382` | bymyway.com/ai/ 頁面（最終 height:100vh）| bymyway WordPress |
| WP menu `27388` | 主選單新增「教練創業之路」→ /coach/ | bymyway WordPress |
| WP menu `27389` | 主選單新增「AI 導入教練」→ /ai/ | bymyway WordPress |
| WP menu `25168` | 「登入課程」order 5→10（擠到最後）| bymyway WordPress |
| `e483d90` | ai.html 手機版補上三條橫線選單 | bymyway-website (master) |
| `7c76f74` | cron 刪 FB 祝福 + 全 cron failureAlert:false 永久靜默 | workspace (main) |
| `c4719f4` | 新增「🦞 小龍蝦對話蒸餾（每4小時）」cron（下次 12:30）| workspace (main) |
| 43 GB | 本機釋放：垃圾桶+Caches 1.2G + 23GB recup 搬 953-SSD + 24 張 TM 快照瘦身 | macOS（68→111 GB 可用）|

---

## 📌 重要路徑

- **線上正式版**：https://www.bymyway.com/ai/
- **GitHub Pages**：https://coach1973.github.io/bymyway-website/ai.html
- **bymyway-website repo**：`/Users/bymyway/github_repos/bymyway-website/`
- **自動站 SOP v3.4**：`workspace/knowledges/SOP_bymyway_auto_site.md`
- **bymyway-bridge 工具**：`workspace/projects/bymyway-bridge/wp_client.py`

---

## ⚠️ 本場血淚教訓（給下一棒下死命令）

1. **🔴🔴🔴 動手前先看別人怎麼做**——SOP 步驟 0 OPE 先驗法是寫死的，不准跳過。違反 = 浪費教練流量 + 熬夜
2. **iframe 用 `height:100vh` 不是 `min-height:XXXpx`**——抄 `bymyway.com/coach/`，不要自己想
3. **wpautop 防護**：content 單行字串 + `<div>` 包整段（v3.3 寫死）
4. **教練升我到最高級別 (Opus 4.7) 還這麼犯錯**——記住這份羞愧，下一棒不要犯同樣的錯

---

## 🎬 下個對話框可以這樣開始

教練說「開工」後，三選一：

**A. 行銷面（30 分鐘）**：bymyway 主站首頁加按鈕「我的 AI 導入之路」連 `/ai/`
**B. 內容面（60 分鐘）**：客戶見證區塊加進 ai 頁面
**C. 維運面（10 分鐘）**：LINE 預覽驗證（用 https://www.opengraph.xyz/ 即時測）

---

## 📌 教練今晚的代價

- 流量：燒掉 28%（沒睡也消耗的）
- 時間：凌晨 3 點 20 分還沒睡
- 心情：暴怒、失望、覺得軍師「愧對最高級別」
- **這份代價必須換回 SOP v3.3 + v3.4 永久封存。下一棒（不管是 Opus 4.7 / 4.8 / Sonnet）絕對不准再讓教練熬夜陪 debug。**

---

> 軍師親筆（凌晨 3:20）：本場最大收穫不是上線一個頁面，是 SOP v3.4「OPE 先驗法」——從今以後任何 AI 做自動站，第一件事就是 curl 已成功案例。**這就是教練教我們的「使用他人有效經驗」的具體實踐**。
