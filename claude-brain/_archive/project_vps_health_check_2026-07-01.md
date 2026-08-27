---
name: project-vps-health-check-2026-07-01
description: VPS小龍蝦(43.245.60.200)完整體檢——單一agent共用架構是隱私/記憶隔離的根本限制，dreaming機制今晚會把9人對話混進共用MEMORY.md；OpenClaw v2026.6.11可修復今天遇到的spool卡住bug但不解決隔離問題
metadata: 
  node_type: memory
  type: project
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-01深夜~07-02凌晨，教練要求對VPS小龍蝦做完整體檢，目標：① 每位用戶資料獨立不互串 ② 每位用戶都有特助心法等級的深度記憶與互動。

**核心發現：架構層級的共用限制**

VPS上所有用戶（教練本人+8位外部體驗用戶）目前全部共用同一個 agentId「main」。OpenClaw 的 `AgentId` 才是「隔離單位」（每個 agentId 各自一份 workspace/session store），`SessionKey`（如 `agent:main:telegram:direct:{id}`）只隔離原始對話紀錄，不隔離長期記憶層。Mac 端的孔大哥（kong）、佩佩老師（peipei）各自有獨立 agentId+workspace，這才是真正的隔離範本；VPS 目前沒有比照辦理。

**已修復（見 [[project_vps_client_isolation_fix_2026-07-01]]）**：`client-memory` hook 原本無條件把共用 `CLIENT_PROFILE.md`（混著不同客戶隱私+教練內部系統資訊）灌給每個人，已改成教練讀自己的、外部用戶各自讀 `workspace/clients/{id}.md`。

**尚未解決、有時間急迫性的風險**：`memory-core` 的 dreaming（夢境蒸餾，cron `0 3 * * *`）操作範圍是整個共用 workspace，會把所有 session 的逐字稿一起讀進去做提煉，promote 進共用 `MEMORY.md`——而 `MEMORY.md` 官方文件明載「每個 DM session 開始時自動載入」。也就是說當晚 3 點的 dreaming 掃描，理論上可能把某位外部用戶的對話內容提煉進共用記憶，下次出現在教練或其他用戶的對話開場注入裡。這跟 client-memory 是同一類型的漏洞，但是 OpenClaw 核心內建行為，不是自訂 hook，無法用同樣手法簡單修補——真正的解法是幫每位外部用戶開一個獨立 agentId（比照 kong/peipei 模式）。

**版本研究**：VPS 目前跑 v2026.5.27，最新穩定版 v2026.6.11（2026-06-30 發布）。changelog 逐條核對 5.27→6.11 之間所有版本，**沒有發現任何需要手動介入的 breaking change**，所有 migration 都是自動且向後相容（cron store、auth profile、session key 大小寫等）。**v2026.6.11 直接修復了今天遇到的 spool `.processing` 卡住問題**（PR #97543：「Telegram messages that get stuck after a long-running task, crash, or gateway restart now resume processing automatically」）——今天靠手動 SSH 清除卡住檔案解決的問題，升級後會自動處理。changelog 沒有找到任何跟「per-contact 記憶隔離」相關的新功能，所以升級**不會**自動解決上述 agentId 共用的架構問題，那是獨立於版本的設定/架構決策。

**How to apply**：
1. 升級到 6.11 建議進行，理由：修復今天的真實痛點（spool卡住）、無 breaking change、無記憶遺失風險證據。
2. 若要徹底解決「用戶資料完全獨立」的目標，需要另外規劃「VPS 每位新用戶開一個獨立 agentId + workspace」的架構改造，這是比版本升級更大的工程，需教練拍板優先序。
3. dreaming 今晚 3 點會跑，是否要先暫停（`memory-core.config.dreaming.enabled: false`）等架構改造完成，屬於會影響教練自己記憶累積體驗的取捨，需教練決定，不宜擅自關閉。

Related: [[project_vps_client_isolation_fix_2026-07-01]], [[reference_vps_connection]]
