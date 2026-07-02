---
name: project-hermes-vps-multitool-session-2026-07-02
description: Hermes VPS更新v0.13→v0.17+dashboard登入bug修復+核准流程澄清+vps-onboard-approve技能直接裝上VPS
metadata: 
  node_type: memory
  type: project
  updated: 2026-07-02
  originSessionId: 823578fe-2c75-417e-aaa3-c036fa112b23
---

# Hermes VPS 一系列處理（2026-07-02 聯想軍師）

**做了什麼：**
1. Hermes VPS（113.29.232.178）從 v0.13.0 更新到 v0.17.0，先備份839M資料再動手，舊容器保留可回滾
2. 更新後dashboard登入500錯誤——查出官方bug：`/auth/login?provider=basic`路徑只給OAuth用，Basic Auth正確網址是`/login`。已設帳密 coach/Hermes2026Coach!
3. 查證澄清：小龍蝦新用戶「開通」不是全自動，有`openclaw pairing approve`核准關卡，判斷權永遠在教練（教練親自更正了Mac軍師報告裡的不精確說法）
4. 找到教練昨晚已寫好、測試過的`/root/provision_new_vps_user.sh`（不是我重寫的），寫成SOP推上GitHub（`knowledges/SOP_hermes_vps_onboard_approve.md`，commit 285bd9e0）
5. **直接SSH進VPS Hermes把技能檔案寫進`/opt/data/skills/devops/vps-onboard-approve/SKILL.md`**，不叫教練當中間人轉達給Hermes，用`hermes skills list`實測驗證顯示`enabled`

**Why：** 教練要一個「就算Mac電腦掛了、身邊只有手機」也能核准新朋友加入VPS小龍蝦的備援方案。

**How to apply：** 教練以後對赫米斯助教（VPS Hermes Telegram bot @hermes_coach1973_bot）說「核准XXX」，會自動照這份技能執行。技能實體檔案位置：VPS 113.29.232.178的 `/root/.hermes/skills/devops/vps-onboard-approve/SKILL.md`（host路徑，容器內對應`/opt/data/skills/devops/vps-onboard-approve/SKILL.md`）。

Related: [[reference_vps_provision_script]], [[feedback_vps_pairing_approve]], [[feedback_dont_relay_between_ai_systems]]
