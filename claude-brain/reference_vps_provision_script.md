---
name: vps-provision-script
description: VPS一鍵開通新用戶獨立空間腳本，取代手動15分鐘SOP，已用假ID測試安全通過
metadata: 
  node_type: memory
  type: reference
  originSessionId: e800e341-3d04-4ed4-bf2a-f43e799bb9e4
---

2026-07-02凌晨，教練要求把當晚手動幫8位用戶建獨立agent的SOP自動化，之後每個開通的VPS小龍蝦都比照獨立架構規格。

**腳本位置**：VPS主機（43.245.60.200）的 `/root/provision_new_vps_user.sh`（不在容器內，容器重建不受影響）

**用法**：`/root/provision_new_vps_user.sh <telegram_id> [顯示名稱]`

**做的事**（一行指令取代原本15分鐘手動流程）：
1. 檢查該Telegram ID是否已開通過（避免重複binding衝突）
2. 備份現有openclaw.json（帶時間戳）
3. 建立獨立workspace，複製通用身份檔（AGENTS.md/SOUL.md/IDENTITY.md/TOOLS.md，不含教練個人資料）
4. 更新openclaw.json加入agents.list+bindings（peer.kind:direct分流，同一Bot Token不用換）
5. 重啟容器
6. 驗證：健康檢查、binding是否生效、**main是否仍是預設agent**（防止意外把教練導向陌生人空間）

**已測試**：用假ID `99999999999` 完整跑過一次（含重複執行測試、確認會拒絕重複開通），驗證無誤後清除乾淨，未影響任何真實用戶。

**限制（教練需理解）**：無法「預先蓋好20-30個空房間等未來的人」——因為binding必須綁定真實存在的Telegram ID，而這個ID要等這個人真的傳第一則訊息才會出現。真正做到的是「開通速度從15分鐘手動變成1行指令幾秒鐘」，不是「預先佔位」。

**磁碟空間查證**（教練原本以為只有8GB，實際查證）：
- VPS總空間100GB，當時用34GB，剩67GB可用
- 單一空帳號workspace僅32KB；有100則對話的活躍帳號約352KB
- 開到100個帳號估計總佔用僅數MB等級，磁碟完全不是限制

**How to apply**：以後教練說「幫XXX開通VPS小龍蝦」，直接SSH上VPS跑這支腳本+對方的Telegram ID即可，不需要重跑當晚那套手動流程。

Related: [[project_vps_multiagent_rollout_2026-07-02]], [[reference_vps_connection]]
