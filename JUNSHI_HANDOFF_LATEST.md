# 軍師接力棒 · 2026-06-08 04:20（Sonnet 4.6 + Opus 4.6 終端機 session）

> 建立時間：2026-06-08 04:20
> 上一棒：Hermes M3 2026-06-07 14:10
> 本棒執行者：Sonnet 4.6（開工+執行）→ Opus 4.6（FAQ 優化）

---

## ✅ 本場完成

### 任務一：文章評估——AI 長期記憶系統（weichen.ink）✅
- 教練分享一篇 Obsidian 長期記憶管理文章
- 結論：**我們的系統已比文章更完整**
  - 路徑大全 = INDEX 路由功能
  - memory/ = 長期記憶
  - 試金石 = 失敗決策庫
  - MEMORY.md = 索引指針
  - 接力棒 = 跨 session 交接
  - Hook 自動化 = 文章沒有的層次
- 文章對我們的價值：**驗證方向正確**，僅此而已

### 任務二：教練中文詞彙→檔案對照表 ✅
- 教練指正「路徑大全就是 INDEX」——以此建立中文→英文檔案對照記憶
- 路徑大全=INDEX、靈魂檔案=SOUL.md、記憶檔=memory/、接力棒=JUNSHI_HANDOFF、試金石=試金石_案例庫、心跳檔=HEARTBEAT
- 存入 `feedback_coach_chinese_file_mapping.md`，更新 MEMORY.md 索引

### 任務三：jiesheng-leadership.netlify.app 工作坊版本恢復 ✅
- 教練要求恢復有工作坊的版本
- 備份檔位置：`knowledges/jiesheng_index_with_workshop_backup.html`
- **第一次推送漏了圖片**（又犯 SOP 明文禁止的老錯誤）
- 發現後立刻從舊部署 `6a1521cc4cf2e700088106d9`（5/26）抓回 book.png
- teacher.jpg 從 `6a1ae004e01a44b445827223`（5/30）抓回
- 最終部署 ID：`6a267f3d469d6600ca0168b2`

### 任務四：四處修正 ✅
1. **標題**：「結繩領導學｜現場座談會 × 實體工作坊」（三組詞都在）
2. **台中場飯店**：台中市區 → 朝暮良辰文南館
3. **Q&A 整體優化**（Opus 操刀）：6 題→7 題，形成行銷漏斗
4. **圖片**：book.png + teacher.jpg + _headers 全部打包

#### Q&A 設計邏輯（漏斗結構）
1. 活動包含哪些內容？→ 三合一開門見山
2. 座談會和工作坊有什麼不同？→ 「看懂 vs 帶回去用」
3. 這本書適合什麼樣的人？→ 尾巴帶出工作坊
4. 不是工程背景也能理解嗎？→ 帶出現場引導
5. 可以先來座談會再決定？→ 降低門檻
6. 怎麼參加？要付費嗎？→ 座談免費＋工作坊連結
7. 工作坊兩天會做什麼？→ 四大收穫收尾

部署 ID：`6a267f3d469d6600ca0168b2`，HTTP 200，圖片驗證通過

---

## 🪞 本場教訓

1. **圖片又漏了**：SOP 明文寫「禁止不包圖片」，還是犯了。根因：第一次推送時直接用 knowledges/ 的備份 HTML 打包，沒走 SOP 第一步「下載現有版本所有檔案」。這是第 N 次犯同樣的錯（守則 #07）。
2. **守則 #15 落地**：文章分析時，一開始多加了「INDEX.md 路由表」建議，教練指正路徑大全已有此功能。承認錯誤比硬撐有價值。

---

## 📊 部署紀錄

| 部署 ID | 時間 | 內容 |
|--------|------|------|
| `6a263972005a13c5be8523b5` | 06-08 03:39 | 第一次推送（漏圖片）|
| `6a267f3d469d6600ca0168b2` | 06-08 04:13 | 最終版（含圖片+FAQ優化）|

---

## 📝 給下一棒

### Meta Automation 待做清單（剩 1 個）
- 🔴 **Netlify 部署鐵律 Stop Hook**——偵測 git push + netlify 組合 → 攔截
  - 替代方案：PreToolUse Hook（推送前攔截）可能比 Stop Hook 可靠

### 圖片漏失問題（系統性修復建議）
- 圖片漏失已多次發生，SOP 文字規範不夠——考慮寫成 shell 腳本自動化「下載現有部署所有檔案」步驟
- 或在部署 zip 打包前加一個 check：`ls *.png *.jpg` 失敗就 abort

### 已完成的鉤子
- `scripts/rule12_porter_check.sh`（搬運工句型）
- `scripts/rule05_hash_check.sh`（完成詞缺 hash）
- `scripts/e07_settings_inject.sh`（模型問題自動注入）
- 註冊位置：`~/.claude/settings.json`

### 記憶更新
- 新增 `feedback_coach_chinese_file_mapping.md`：教練中文→檔案對照表

**最後更新：2026-06-08 04:20（Sonnet 4.6 + Opus 4.6 終端機 session）**
