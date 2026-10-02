---
name: project_yijing_agent_telegram_group_2026-09-30
description: 怡靜AI群(-5480670608)改由Mac小龍蝦的獨立分身yijing回話（比照學弟/學妹架構），教練不要VPS版；群裡原本加的是VPS的@coach_bymyway_bot所以一直「不在准許名單被略過」
metadata:
  node_type: memory
  type: project
  originSessionId: 460979e3-7b38-4c37-8a42-e8e91101983f
  modified: 2026-09-30T17:32:05.779Z
---

2026-09-30 教練：怡靜AI群要用 Mac 版小龍蝦，比照孔大哥（學弟）、佩佩老師（學妹）那套邏輯替怡靜建一個；不要 VPS 版。

- 查出來的根因：群裡加的是 VPS 的 @coach_bymyway_bot，VPS 設定沒有准許群組，每則訊息都被記成 not-allowed 略過。Mac 這邊一則也沒收到。
- 已建分身 `yijing`（workspace `~/.openclaw/agents/yijing`，有自己的 git，本機 commit `d8a117e`，尚未建 GitHub 備份庫——建 repo 會被安全檢查擋，要教練授權）。
- `openclaw.json`：bindings 新增「bot_main + 群組 -5480670608 → yijing」，放在 bot_main 通用綁定之前；bot_main.groups 加該群，requireMention=false，並沿用 toolsBySender（只有教練可用 runtime/fs/automation）。commit `0e1e12c62`（外層 repo）。設定熱重載已套用，不必重啟。
- Mac 機器人 @openclaw_macbook4_bot 必須由教練拉進群，才會開始回話；進群後要實測回話的是 yijing 分身，並從對話抓怡靜的 Telegram user_id 補進 IDENTITY.md。
- 怡靜名字寫「怡靜」；教練語音常打成「宜靜」。

- 10-01 已上線：`scripts/team_tool.py`（五分會查詢＋第一分會出席更新）＋safety-locks 的 yijing 白名單（只准 team_tool／產業鏈出圖、只能寫自己資料夾），群組 toolsBySender 全開改由白名單管。
- **教練 10-01 定的下一步**：①建立「怡靜學姐」——「怡靜」是關鍵詞，後面接學姐／董顧／區董等不同場合稱呼都要叫得到；②幫怡靜的協會用現成報名系統，有人報名→怡靜AI群＋活動報名即時通知群都收到。下一場一開始就設計。

**Why:** 教練要每位夥伴都有獨立記憶的專屬特助，喜好與需求分開記。
**How to apply:** 之後新增夥伴專屬特助，照這個模式（agents add → 寫五份檔 → peer 綁定群組）；VPS 版不要拿來當選項。

相關：[[project_curated_sites_github_cross_machine_edit_2026-09-30]]
