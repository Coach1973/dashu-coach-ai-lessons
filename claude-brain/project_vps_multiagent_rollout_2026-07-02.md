---
name: project-vps-multiagent-rollout-2026-07-02
description: VPS小龍蝦(43.245.60.200)完成版本更新至v2026.6.11+每位外部用戶獨立agent架構，4位活躍用戶對話紀錄完整搬遷驗證，教練本人main agent不受影響
metadata: 
  node_type: memory
  type: project
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-02凌晨，接續 [[project_vps_health_check_2026-07-01]] 的體檢發現，完成兩件大事：

**一、版本更新 v2026.5.27 → v2026.6.11**
- `openclaw update` 42秒完成，`openclaw doctor` 全過，容器重啟後確認版本生效
- 直接修復了7/1當天遇到的spool `.processing`卡住問題（PR #97543已內建於此版本）
- 逐條核對changelog確認無breaking change，9位用戶session資料重啟後完整（session數、jsonl行數皆核對過）

**二、每位外部用戶獨立agent架構**
根因：VPS原本9人（教練+8位外部體驗用戶）共用一個agentId「main」，導致MEMORY.md/dreaming/CLIENT_PROFILE.md等長期記憶層混在一起。今天先前只修了client-memory hook（治標），這次是治本：比照Mac端孔大哥(kong)/佩佩老師(peipei)模式，用OpenClaw官方`agents.list`+`bindings`機制，幫8位外部用戶各自開一個完全獨立的agent。

**執行細節**：
- 8個新agentId：`trial-{telegram_id}`，各自獨立workspace（`~/.openclaw/workspace-trial-{id}`）與session store（`~/.openclaw/agents/trial-{id}/`）
- 每個新workspace種入通用身份檔（AGENTS.md/SOUL.md/IDENTITY.md/TOOLS.md，從main複製，不含教練個人資訊），有既有客戶檔案的（CHIU/Esther/LinYuJu）種進其MEMORY.md當起點
- Binding用`{channel:"telegram", peer:{kind:"direct", id:"{telegram_id}"}}`——同一個Bot Token不用換，靠寄件人ID分流（OPE查證：這是官方WhatsApp/Telegram通用模式，不是WhatsApp專屬）
- **關鍵bug當場抓到並修正**：`agents.list`新增後系統自動把第一個entry設成預設agent（本例是芸熙），若不修正，教練本人或任何未匹配規則的訊息會被導向陌生用戶的私人空間！已明確加入`{id:"main", workspace:"~/.openclaw/workspace", default:true}`並置頂，同時明確加教練本人(6124913915)的binding，`openclaw agents list --bindings`驗證main已正確變回default

**四位真實活躍用戶（Esther/在珍老師、CHIU YuJung、Lin Yu Ju/老大、杉榕陳）對話搬遷**：
教練親自拍板方案——先備份、裝完再匯入（其餘4位當天才開通、幾乎沒對話，不需要搬遷）。
1. 先把4人.jsonl原始逐字稿複製到VPS**主機層**（不在容器內，雙重備份：`/root/vps_migration_backup_20260702-010238/session_raw/`）
2. 建好新agent架構後，把備份複製進新agent的session目錄，手動建構sessions.json entry
3. **踩到一個關鍵坑**：VPS開了`session.dmScope:"per-channel-peer"`，所以新agent的session key格式不是文件講的`agent:<id>:main`，而是要保留`agent:trial-{id}:telegram:direct:{id}`這個granular格式——第一次建錯了key，靠`openclaw sessions --agent`指令回傳的`runtimePolicySessionKey`欄位發現對不上，即時修正
4. 最終驗證：`openclaw sessions --all-agents`顯示這4人的session同時出現在main（舊資料完整保留未刪除）跟trial-{id}（新獨立空間）底下，且sessionId完全一致；.jsonl行數（79/100/51/78）跟原始備份逐字對應，零資料流失

**收尾驗證**：容器重啟healthy、gateway health check OK、`openclaw security audit`0 critical（4個warning都是既有一般性加固建議，跟這次隔離工程無關）。

**Why**：教練明確定調兩個目標——①用戶資料獨立不互串 ②每人都有特助心法等級的深度記憶。這次是實現這兩個目標的架構層解法，不是頭痛醫頭。教練也用「信念第三條」（長期有好處的事今晚就做）拍板不等到白天。

**How to apply**：
1. 未來VPS再開通新的外部體驗用戶，應直接建立獨立agent（照這次的workspace-trial-{id}+binding模式），不要讓新人落回共用的main。
2. 8個新agent目前workspace只有通用身份檔+（部分人）既有客戶檔案，還沒有自己的dreaming/長期蒸餾機制在跑——這是下一步可以做的（讓每個人的agent workspace也啟用memory-core dreaming，真正做到「越聊越懂這個人」）。
3. VPS已有自己的GitHub憑證（見[[reference_vps_github_credentials]]），這次的openclaw.json改動本身不在git追蹤範圍內（openclaw.json/agents/等目錄在workspace repo外），痕跡留在VPS主機層的備份檔和這份記憶紀錄。

Related: [[project_vps_health_check_2026-07-01]], [[project_vps_client_isolation_fix_2026-07-01]], [[reference_vps_github_credentials]], [[reference_vps_connection]]
