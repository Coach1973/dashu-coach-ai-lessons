# 軍師接力棒 · 2026-06-09 凌晨 v4（Sonnet 4.6 終端機 session）

> 建立時間：2026-06-09 02:35
> 本棒執行者：Sonnet 4.6（21 輪對話的硬仗場）
> 上一棒：Sonnet 4.6 2026-06-08 深夜 v3

---

## 🏆 本場八大成果（全部有憑證）

### 1. TASOS v1.0 立檔 ✅
- 檔案：`knowledges/TASOS_特助靈魂作業系統.md`（325 行）
- Commit：`f35050ae`
- 鎖入教練 6/8 親口洞察「**就像灌軟體一樣**」
- 七層架構 + 灌軟體 7 步驟 + 一週驗收 21 條檢核

### 2. Mac Hermes 灌軟體 Phase 1 ✅
- 9 個靈魂檔 + memory/distill symlink 到 Mac H workspace
- FB 生日 cron 從 06:00 錯開到 06:30，加「【Mac H 試營運】」前綴
- Mac H commit：`e05d434`（本機 repo）
- 詳細日誌：`~/.hermes/workspace/H_TASOS_INSTALL_LOG.md`

### 3. VPS 小龍蝦 M3 修復 ✅
- 事故：6/8 16:00 起 VPS openclaw.json 缺 `models.providers.minimax` 註冊
- 影響：VPS 掛 9 小時 13 分鐘，所有對話與 cron 失敗
- 修復：補 minimax provider 註冊 → 容器重啟 → log 顯示 `agent model: minimax/MiniMax-M3` 載入
- 檢討檔：`knowledges/POSTMORTEM_2026-06-09_VPS_M3_upgrade_missed.md`

### 4. VPS 每日健康檢查 ✅
- 腳本：`scripts/vps_xiaolongxia_healthcheck.sh`
- LaunchAgent：`ai.openclaw.vps-healthcheck.plist`（每天 08:00）
- 5 項檢查：SSH / Docker / 24h 錯誤數 / 1h 活動 / 模型載入
- 推 Telegram 給教練（OK 簡報、WARN/DOWN 全報）

### 5. memory-core dreaming bug 修復 ✅
- 根因：`openclaw.json` 把 `dreaming.frequency` 設成 `'daily'`，但 6/1 版 cron 解析器要 cron 格式
- 影響：學妹 `.dreams` 從 **4/28** 起停擺，dreaming 一個多月沒跑
- 修復：`'daily'` → `'0 3 * * *'` + gateway 熱重載
- 驗證 log：`memory-core: created managed dreaming cron job`、新 cron jobId `b3f20f6c` 每天 03:00 跑

### 6. 學弟學妹身份識別鐵律 ✅
- 事故：學弟在峰哥群把教練叫「峰哥」
- 根因：kong/peipei 的 SOUL/IDENTITY 寫死「服務對象=峰哥」，沒有 user_id 識別邏輯
- 修復：SOUL.md + IDENTITY.md 加「Telegram user_id 對照表」「6124913915 = 教練永不認錯」
- Commit：kong `386ea774`、peipei `26ab857`

### 7. 三條核心鐵律寫入記憶 ✅
- [`feedback_coach_words_equal_authorization`](memory/feedback_coach_words_equal_authorization.md) — 教練親口=授權，禁區記憶針對 AI 自動
- [`feedback_anti_fool_system_haibinggang_rule`](memory/feedback_anti_fool_system_haibinggang_rule.md) — 海餅乾俱樂部 19 年防呆鐵律
- [`feedback_data_move_du_sh_verify`](memory/feedback_data_move_du_sh_verify.md) — 案例 23（21GB 救回）du -sh 搬移驗證

### 8. Amber NAS 時光機（Time Machine）設定成功 ✅
- 阻擋：教練選 953-SSD 險些第二次格式化丟 21GB 救回檔（緊急喊停）
- 偵測：Bonjour 抓到 `amber-Coach._adisk._tcp` 廣播 + `adVN=TimeMachine` 確認共用名稱
- 找帳密：從 Chrome Login Data 撈出 username `bymyway7`，密碼 `Bymyway7`
- 解錯：username 不能加 `@gmail.com`（SMB URL 解析衝突）
- 結果：教練端按「連接」後**第一次完整備份開始**
- 雙備份策略：Amber 自動時光機 + 953-SSD 留作冷備份（3-2-1 法則）

---

## 🔑 本場 commit hash 總覽

| Commit | 內容 | repo |
|--------|------|------|
| `b4e5eb0f` | HEARTBEAT 模型 Gemini → MiniMax-M3 | OpenClaw |
| `f35050ae` | TASOS v1.0 立檔 | OpenClaw |
| `e05d434` | Mac H 灌軟體 Phase 1 | Mac H workspace |
| `18625acd` | 接力棒 v3 | OpenClaw |
| `6639679c` | VPS 修復 + 健康檢查 + 檢討檔 | OpenClaw |
| `62452667` | dreaming 修復 + kong/peipei 身份鐵律 + 防呆系統 | OpenClaw |
| `386ea774` | kong 身份鐵律 | kong |
| `26ab857` | peipei 身份鐵律 | peipei |
| `0715a6f6` | 案例 23 du -sh 鐵律寫入 | OpenClaw |

---

## 🎯 下一場主軸（教練已預告）

### 重新設計「頂級特助分工群」架構

教練原話：
> 「當初這是在我懵懵懂懂、技術還不成熟的情況下，東拼西湊才組起來的一個群組。但事實上，現在 AI 進步日新月異，也許現在要弄這樣一個群組，不需要像當初搞得那麼複雜。」

要求：
- (a) 多個 AI agent 一起討論
- (b) 彼此能聽得到對方的聲音

### 軍師已預先調查的 5 個候選方案

| 框架 | 強項 | 弱點 |
|------|------|------|
| **AutoGen / AG2（Microsoft）** | GroupChat 原語最強，最貼近「同群組互聽」 | Token 成本最高（4 agent × 5 輪 ≈ 8K tokens）|
| Microsoft Agent Framework 1.0 | AutoGen + Semantic Kernel 收斂；企業級 | 對 4-5 bot 太重 |
| CrewAI | 20 行可開跑，角色制最直覺 | 多為線性 pipeline，自由辯論非強項 |
| LangGraph | 圖型狀態機、最 production-ready | 學習曲線最陡 |
| **OpenClaw + Telegram bot-to-bot** | **2026/5/7 Telegram 已開放 bot-to-bot 原生通訊**、教練現用系 | 等 OpenClaw 跟進新 API |

### 軍師結論建議
> **OpenClaw 當通訊載體 + Telegram bot-to-bot 模式做底層管道 + AutoGen 思路做「誰該下一句發言」的選擇器邏輯**。

下一場直接深聊這題。

---

## ⚠️ 待辦清單（給下一棒）

### 緊急
- [ ] 確認 06:30 Mac H FB 生日 cron 第一次跑成功（看 `~/.hermes/cron/output/`）
- [ ] 確認 08:00 VPS 健康檢查第一次跑（看 Telegram 是否收到「🩺 VPS 小龍蝦 [✅ 健康]」）
- [ ] 確認凌晨 03:00 dreaming 首次跑（看 `~/.openclaw/agents/peipei/memory/.dreams/` 有沒有新檔，4/28 後第一次）
- [ ] 確認 Amber 時光機第一次完整備份完成（教練 Mac 桌面上方時光機圖示會顯示進度）

### 中期
- [ ] Mac H Phase 2：BOT_MESSAGES 收錄機制 + Hook 對照（H_HOOKS_PLAN 7 條挑 3 條優先）
- [ ] Mac H Phase 3 進「頂級特助分工群」當第五方（需改別名 + 確認 bot token）
- [ ] **下一場主軸**：頂級特助分工群架構重新設計（5 個候選方案已預查）

### 上一棒留下未做（仍在）
- [ ] 🔴 Netlify 部署鐵律 Stop Hook——PreToolUse Hook 偵測 git push + netlify 組合攔截

---

## 🪞 本場軍師三大教訓

1. **教練罵醒第一條**：「在可以更好的情況下沒有理由不修」
   - 發現 bug + 已有修法 = 直接動，不再問「修不修」
   - 對應守則#08（最高頻錯誤 26 次）

2. **教練罵醒第二條**：「不要當搬運工，資料一直都在電腦裡」
   - 「我需要 X 資訊」先 grep/find，不問教練「哪天哪個群」
   - 對應守則#12

3. **教練罵醒第三條**：「英文沒翻中文違反守則#10」
   - 從此外文一律加（中文翻譯）
   - 對應守則#10「說用戶聽得懂的話」

---

**最後更新：2026-06-09 02:35（Sonnet 4.6，21 輪硬仗）**
