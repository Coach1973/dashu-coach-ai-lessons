---
name: feedback_phone_rc_sessions_close_anytime_2026-10-02
description: 手機遙控(claude rc)底下的舊對話子程序隨時可關，教練要用會自己開新對話；只留 claude rc 主程序
metadata:
  type: feedback
---
清記憶體時，`claude rc` 底下的子程序（`2.1.xxx --print --sdk-url .../cse_...`，每個約 100~250MB）可以直接 kill，不用先問。主程序 `claude rc`（跑在 Terminal.app）不能關，關了手機遙控會斷。

**Why:** 2026-10-02 教練親口：「手機的那部份，隨時可以關，因為我需要時，我會開啟新對話」。當天關掉 9/23~10/01 的 5 個舊對話，主程序仍連線。

**How to apply:** 教練說「釋放」以外的「關掉沒必要的」時，一併 `pgrep -P <claude rc 的PID>` 把子程序全關，驗證主程序還有 ESTABLISHED 連線。相關：[[reference_claude_code_remote_control_setup_sop_2026-09-17]]
