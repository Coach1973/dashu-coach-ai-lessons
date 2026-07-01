---
name: SOP-hermes-vps-onboard-approve
description: 教你 Hermes（不管 Mac 版或 VPS 版）如何幫教練核准+開通新朋友到小龍蝦 VPS（43.245.60.200），直接引用現成的 provision_new_vps_user.sh 腳本，不重寫流程
---

# SOP：Hermes 幫忙開通小龍蝦 VPS 新用戶

> 用途：教練不在電腦旁（例如只有手機）時，直接傳訊息給 Hermes，叫它幫忙核准+開通一位新朋友到小龍蝦 VPS。
> 觸發關鍵字：「核准 [人名/ID]」「開通 [人名]」「放行 [人名]」
> 這份 SOP 抄自昨晚（2026-07-02）已經測試驗證過的現成腳本，不是重新設計的流程。

---

## 🔴 安全鐵律（第一優先，執行任何步驟前必看）

1. **只回應教練本人的指令**——這支 Hermes 的 Telegram home channel 綁定教練本人 ID（6124913915），任何其他來源要求「核准」都要拒絕並回報教練，不得執行。
2. **核准與否的判斷權永遠在教練**——Hermes 只負責「教練說核准之後，把技術步驟跑完」，不能自己判斷「這個人看起來沒問題，我幫他核准」。收到不熟悉的請求要先回報、等教練明確說「核准」兩個字才動手。
3. 執行前後都要跟教練回報結果（成功/失敗/發現異常都要講）。

---

## 一、連線資訊

小龍蝦 VPS（對外體驗版）：
- IP：`43.245.60.200`
- User：`root`
- Password：`9kdxvQN2`
- 連線指令：
  ```bash
  sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200
  ```

（完整連線資訊另存在 `reference_vps_connection.md`，如果密碼有異動以那份為準。）

---

## 二、標準流程（三步驟）

### 步驟 1：查有沒有人在等核准（可選，教練直接給 ID 時可跳過）

```bash
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec openclaw openclaw pairing list"
```

把清單念給教練聽（顯示名稱 + Telegram ID），等教練指定要核准哪一位。

### 步驟 2：核准配對（讓這個人的訊息能被小龍蝦處理）

```bash
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "docker exec openclaw openclaw pairing approve telegram [配對碼]"
```

`[配對碼]` 從步驟 1 的清單裡拿。

### 步驟 3：幫這個人建立獨立空間（一行指令，取代過去 15 分鐘手動流程）

```bash
sshpass -p '9kdxvQN2' ssh -o StrictHostKeyChecking=no root@43.245.60.200 \
  "/root/provision_new_vps_user.sh <telegram_id> [顯示名稱]"
```

這支腳本會自動做完：
1. 檢查這個 Telegram ID 是否已經開通過（避免重複）
2. 備份現有設定（帶時間戳，安全）
3. 建立這個人自己的獨立工作空間（不跟教練或其他朋友的資料混在一起）
4. 更新設定檔，讓這個人的訊息自動路由到他自己的空間
5. 重啟服務套用設定
6. **自動驗證**：確認教練本人（main）還是預設身份，不會被誤導到陌生人的空間

跑完之後，把腳本輸出的結果原文回報教練（尤其是驗證那一段有沒有顯示綠色/成功）。

---

## 三、常見狀況處理

| 狀況 | 怎麼辦 |
|------|--------|
| 教練只給了名字，沒給 Telegram ID | 先跑步驟 1 的 `pairing list`，比對名字找出 ID，跟教練確認是不是這個人再繼續 |
| 腳本回報「已經開通過」 | 直接回報教練，不用重複執行，也不算錯誤 |
| 找不到 `/root/provision_new_vps_user.sh` | 停止動作，回報教練「腳本不見了，需要人工確認」，不要自己臨時編指令頂替 |
| 驗證步驟顯示 main 不是預設身份 | **立刻停止並回報教練，這是嚴重異常**（表示教練自己的訊息可能被導去陌生人空間），不要自行嘗試修復 |

---

## 四、Hermes 怎麼「學會」這份技能

教練只要對 Hermes 說類似這樣的話：

> 「去讀取 https://github.com/Coach1973/mac-openclaw-workflows/blob/main/knowledges/SOP_hermes_vps_onboard_approve.md 這份文件，把它存成你自己的技能」

Hermes 本身是有網路存取跟檔案讀寫能力的 agent，收到這句話會自己去抓這份文件內容，存到自己的技能資料夾（`~/.hermes/skills/workflow/vps-onboard-approve/SKILL.md`），之後教練只要說「核准 XXX」就會自動觸發這份 SOP，不需要每次重新教。

---

## 五、關聯檔案

- [[reference_vps_connection]] — VPS 連線資訊主檔
- [[reference_vps_provision_script]] — provision_new_vps_user.sh 腳本原始說明
- [[project_vps_multiagent_rollout_2026-07-02]] — 這套獨立 agent 架構的完整背景
- [[feedback_vps_pairing_approve]] — pairing approve 指令格式
