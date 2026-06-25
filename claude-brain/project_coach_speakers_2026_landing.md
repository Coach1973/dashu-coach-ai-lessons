---
name: project-coach-speakers-2026-landing
description: 2026 講座系列一頁式行銷頁專案（線上+實體），v2 草稿已套教練 GitHub 設計正典，等講座資料填空後部署
metadata: 
  node_type: memory
  type: project
  originSessionId: 2faf4af2-42ed-4836-905b-190a6d1bc03c
---

# 大樹教練 2026 講座系列行銷頁

## 現況（2026-06-26 凌晨交接）

教練要辦一連串講座（實體+線上），需要一頁式行銷網頁宣傳整個系列。已完成 v2 草稿，**等教練給講座實際資料**（主題/日期/地點/價格/LINE 連結）就能填空＋部署。

**Why**：教練 26 年企業培訓 × AI 特助心法，這波講座是教練品牌 2026 重點曝光。

**How to apply**：
- 明早 Acer 開工首要任務
- 教練給資料 → 填 v2 placeholder → 預覽給教練看 → 教練說「網頁推」才 push
- 切勿主動部署（部署=不可逆對外動作）

## 檔案位置

| 檔 | 路徑 |
|---|---|
| v1 草稿 | `D:\Users\Desktop\大樹教練講座行銷頁_v1.html`（此機桌面） |
| v2 草稿（主推） | `D:\Users\Desktop\大樹教練講座行銷頁_v2.html`（此機桌面） |
| 共用備份 | `E:\Claude-Data\.claude\projects\E--Claude-Data\memory\handoff_coach_speakers_2026-06-27\` |
| 桌面交接棒 | `D:\Users\Desktop\🌅明早Acer開工_交接棒.md`（此機桌面，Acer 看不到） |

## 設計正典來源（教練自己 GitHub）

帳號 **coach1973**（40+ repos）。已對標 3 個講座頁萃取正典：
- `consultant` — 創業避坑掃雷講座
- `government-grow` — 中小微企業多元發展實戰說明會
- `gold-excellence` — 金卓獎好同學暨好夥伴專屬聚會
- `jiesheng-leadership` — 結繩領導學工作坊（用教練本人引言作見證）

## 教練品牌數據（已查證自網路搜尋，勿改）

- 26 年企業培訓資歷
- 5,000+ 場演講足跡
- 15,000+ 位老闆親自教練
- 4 國足跡：台灣、新加坡、馬來西亞、中國大陸
- 海餅乾俱樂部創辦人（2007 年至今）
- 大樹教育顧問創辦人
- BNI 大台南市區執行董事
- 中興大學傑出校友
- 媒體：看雜誌、聯合新聞網、台灣大紀元

聯絡：陳小姐 0988-004-118（沿用 gold-excellence 正典）

## v2 對 v1 的 11 處正典補強

1. 主標衝突感「不是 X，是 Y」結構
2. 副標 × 連接式
3. Nav 電話 + LINE CTA
4. Hero LINE 綠色 CTA（教練每個站終點都是 LINE 官方）
5. 講座卡「限額 N 人」琥珀徽章
6. 講座卡倒數計時（埋 data-deadline 自動算）
7. 章節標題漸層下劃線（60×4px）
8. 教練金句整版（jiesheng 正典手法）
9. 眼眉 emoji + 脈衝紅點
10. 模糊圓球漸層裝飾
11. 浮動 LINE 圓鈕 + 三欄 Footer

## 待教練決定

1. 整體 slogan 是否用「老闆動嘴，AI 替你執行 / 不是學更多 AI 工具，是把對的事交給 AI 做」
2. 講座實際數量（v2 預留 4 卡片 + 2 placeholder）
3. 是否做多頁版（每場一獨立子頁）
4. GitHub repo 名稱建議：`coach-2026-speakers` / `dashu-talks-2026` / 教練自定

## 部署 SOP（教練說推才推）

教練部署字典（鐵律）：
- 「自動站」= 部署到 bymyway → see [[feedback_coach_deploy_vocabulary]]
- 「網頁推」= git push 到 GitHub coach1973
- 「推」= Netlify zip+API 直推（必帶 _headers，see [[feedback_netlify_headers_content_type]]）

## 相關記憶

- [[feedback_read_existing_before_creating]] — 已執行：先抓教練 GitHub 三個對標 repo
- [[feedback_coach_deploy_vocabulary]] — 自動站/網頁推/推 三詞別搞混
- [[feedback_netlify_headers_content_type]] — Netlify 必帶 _headers
- [[feedback_html_preview_chrome_only]] — 本機預覽唯 Chrome
- [[feedback_self_position_elite_expert]] — 行銷世界級水準，自評低於 8 分重做
- [[reference_coach_websites]] — 教練 6 個網站作品清單
- [[reference_netlify_token]] — Netlify Token + 22 站清單

## Acer 開工提醒

⚠️ 此機（Windows）的 .claude/projects 還沒對接 claude-brain repo；Acer 若也沒對接，需先跑 `setup_claude_brain.ps1` 才能同步到這份記憶。
桌面交接棒檔在此機 D:\Users\Desktop\ 只有這台看得到，Acer 從共用大腦 handoff 子目錄取 HTML 副本。
