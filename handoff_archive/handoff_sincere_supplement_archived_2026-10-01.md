# 封存：2026-09-30 sincere.bymyway.com 戰情儀表板SOP補充段（已結案，SOP見knowledges/SOP_Hermes協助更新sincere戰情儀表板.md）

# 接力棒補充 — 2026-09-30 sincere.bymyway.com 戰情儀表板任務（已派給軍師）

## 教練交辦

教練要小龍蝦「讀網頁後直接更新」，但小龍蝦發現：
- sincere.bymyway.com 是**後端網站**（不是 turnforyou 那種本機直讀）
- 有 3 個 POST API：`/api/update_metric`、`/api/update_testimony`、`/api/update_training`
- **沒有登入驗證、沒有 cookie session、沒有 token**

## 小龍蝦已派給軍師的任務（task ID: 20260930-194932）

寫在 `/Users/bymyway/.openclaw/workspace/state/JUNSHI_TASK_QUEUE`

請軍師：
1. 判斷 sincere.bymyway.com 是誰管的（軍師 / 其他人 / 教練自己）
2. 寫 SOP：「小龍蝦怎麼協助更新 sincere.bymyway.com 的每週戰情資料」
3. SOP 內容包含：讀資料方式、更新 payload、權限邊界、會員自填 vs 教練提供怎麼分、失敗處置
4. 完成後寫進 JUNSHI_HANDOFF_LATEST.md 或 cross-agent/outbox/

## 小龍蝦已抓好的技術細節（給軍師用）

### 3 個 API payload 格式

```
POST /api/update_metric
{ member_id: int, week_date: "YYYY-MM-DD", metric: "guests"|"ones"|"coffee", value: int }

POST /api/update_testimony
{ member_id: int, event_date: "YYYY-MM-DD", attended: 0|1|null }

POST /api/update_training
{ member_id: int, session_id: int, attended: 0|1|null }
```

### 三項指標對應

- **來賓**（guests）= 教練/軍師提供更新
- **121**（ones）= 會員自填
- **咖啡會議**（coffee）= 會員自填

### 統計期間

- 從 2026/07/23 起，**每週四聚會**
- 8/20 當週改為內訓不列入計算
- 連續無紀錄 4 週 = 🟡 黃色關注，8 週 = 🔴 紅色警告

### 三個助理大使（分組）

- 王者飛翔：謝緯翔（王彤、鄭綉美、林佳伶、郭展鴻、張育慈）
- 百聖維尼：許朝峻（陳佩君、鄭禮昂、葉建葳、黃笛軒、盧尚政、張玉盞）
- 羽宙奇蹟：張敬雍（張羽家、楊在珍、李美花、陳柔璇、黃秀麗）

## 守則

小龍蝦**不會自己 POST 進去寫資料庫**，等軍師 SOP 回來再說。

## ✅ 軍師已完成（2026-09-30 19:XX，Sonnet 5）

**對象更正**：上面「小龍蝦已派給軍師的任務」歸屬有誤——查證原始對話後確認，
19:49教練是在**Hermes桌面版**跟Hermes說「你寫一封信給軍師」，小龍蝦Telegram
收到的是教練自己貼過去的同一段文字，不是小龍蝦主動發起。教練當場糾正，已寫入
記憶`feedback_xiaolongxia_vs_hermes_different_systems_2026-09-22.md`（第三次
小龍蝦/Hermes身份混淆）。**下面SOP是寫給Hermes的，教練請幫忙轉給Hermes。**

SOP全文：`knowledges/SOP_Hermes協助更新sincere戰情儀表板.md`。摘要：

1. **sincere.bymyway.com歸屬**：軍師（Mac本機）自己管——`~/github_repos/zhencheng-guests/`
   （Flask+SQLite，launchd `com.coach.sincere-webapp`+cloudflared tunnel `com.coach.sincere-tunnel`），
   DB未版控，純檢視型無登入驗證（教練已接受這個風險）。
2. **會員自填**（121/咖啡會議/全國見證分享會出席/培訓出席）：既有4個API就夠，
   會員自己在網頁上點，Hermes/軍師不用管。
3. **🔴教練口述提供**（來賓人數+名單、早鳥、新會員）：**沒有API**，只能直接寫SQL——
   詳細指令在SOP第3.3節。**`seed.py`已過期（只到08/27，14人，缺黃秀麗/張玉盞），
   絕對不能重跑，會把09/03之後60+筆來賓名單刪光（DELETE無WHERE等級的危險操作）**。
4. 分工：Hermes把教練口述內容整理成SOP第3.3節的格式，寫進本檔或
   `cross-agent/outbox/`，軍師收到後執行SQL、開瀏覽器核對、回報完成。
5. 教練09-30 19:53貼給小龍蝦的「2026/09/17+09/24真誠例會出席報告」裡的
   (P)/(A)/(L)/(M)/(S)出席狀態碼、參訪人員、6個月累計——**這套系統目前沒有
   對應欄位**，只算guests/ones/coffee/early_bird四項，屬於新功能，不是本次
   SOP範圍，教練若要上儀表板要另外評估。

commit：`1b5b37696`（SOP檔）+ `992524f1a`（本節+記憶更新，自動同步已推送origin/main）
