---
name: project-media-resource-center-2026-07-09
description: 教練「媒體資源中心／媒體倉庫」構想的評估與規劃——把散落各機的素材整合到現有Amber私有雲，供未來創作與AI取用，教練說近期忙不急著做
metadata: 
  node_type: memory
  type: project
  originSessionId: 16511bcd-5087-40ef-822c-1c9c29f266f9
---

2026-07-09，教練提出要建立「媒體資源中心」（媒體倉庫），把過去累積的素材（GitHub作品、大樹小講歷史紀錄、其他散落資料）整合到一起，方便日後創作取用，未來也讓AI能直接進去撈素材協作。教練說最近生活工作忙，這件事不急，但比[[project_matrix_marketing_plan_2026-07-09]]更「切合實際、能立即著手」，因為完全自主可控、不用像FB/IG申請公司帳號那樣卡審核。

**AI評估結論**：
1. **儲存位置**：用教練現有的Amber私有雲（192.168.0.35），不建議搬去公有雲（Google Drive/Dropbox等）。理由：教練已有24小時運作的硬體、免月費、資料留在自己家、跟教練說的「完全自主掌控」精神一致。詳見[[reference_amber_nas]]。
2. **多電腦存取方式**：2026-07-09實測確認這台機器根本沒有WebDAV功能（先前查到的官方文件是別的型號），但內建SMB已經可以直接用，AI用PowerShell `net use` 指令實測成功掛成網路磁碟機，不需要教練在Amber後台做任何額外設定。詳見[[reference_amber_nas]]。這個過程中AI犯了先猜測、後查證的錯誤（連續兩次叫教練去點錯的選單），教訓已記在[[feedback_self_verify_before_directing_user]]。
3. **現有素材盤點（僅盤過聯想這台機器，Mac/Acer尚未查）**：
   - GitHub作品：41個repo（完整清單見[[reference_coach_websites]]），涵蓋大樹小講、結繩領導學、BNI系列、特助心法系列等
   - 大樹小講歷史講座紀錄：已存在bigtree repo的archive資料夾，含2026年多場EDM圖片
   - 聯想這台D槽Downloads資料夾底下有大量散落、命名不一致的素材夾（例：AI創作區、媒體檔案、關於大樹教練、全國分享會、資料收集、資訊資料收集、文書檔、重要資料、海餅乾俱樂部、結繩領導學、活動專案、佩佩的策展、公司相關等），這正是教練說「巧婦難為無米之炊」想解決的散亂現況的具體證據
   - Mac跟Acer兩台機器上應該還有更多素材，還沒盤點

**建議的資料夾結構（草案，待教練確認）**：
```
媒體資源中心/
├── 01_品牌素材庫/（Logo、教練照片、書封、簡介文字各版本）
├── 02_歷史活動存檔/（大樹小講各場次EDM+照片，依日期分）
├── 03_網站原始碼備份/（41個GitHub repo的本地鏡像，防帳號出狀況）
├── 04_影音素材/（錄音、影片、Podcast母帶）
├── 05_文案庫/（歷年文案、金句、常用開場白）
├── 06_待發布佇列/（下一場活動的半成品草稿）
└── 00_索引.md（整個資源中心的地圖，AI每次要找素材先看這份）
```

**建議的分階段做法（教練說不急，此為待命方案非已執行）**：
- Phase 0：~~教練登入Amber開通WebDAV~~ 已不需要，SMB直接可用，AI已實測成功掛上`\\192.168.0.35\home`
- Phase 1：AI先把GitHub 41個repo的清單+大樹小講歷史紀錄整理成一份索引檔，不搬檔案先建地圖
- Phase 2：教練確認聯想D槽Downloads那堆散落資料夾裡哪些要留、哪些是垃圾，AI再協助分類搬進資料夾結構
- Phase 3：比照盤點Mac、Acer兩台機器的散落素材，Mac/Acer比照同樣的SMB方式掛上`\\amber-Coach`即可

**How to apply**：教練近期忙，不主動催進度。等教練說「開始弄媒體中心」或類似指示，先從Phase 0（WebDAV開通，需教練本人操作）或Phase 1（純整理索引不搬檔案，AI可獨立先做）啟動。

Related: [[reference_amber_nas]], [[reference_coach_websites]], [[project_matrix_marketing_plan_2026-07-09]]
