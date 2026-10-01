---
name: feedback-remote-connection-confirm-direction-first
description: 遠端連線類問題，動手前先問清楚「誰連誰」；2026-10-01 又做錯方向（做了蘋果→聯想，教練要的是聯想→蘋果），同案例90教訓
metadata:
  node_type: memory
  type: feedback
  originSessionId: 58f267ff-3bc9-45af-8ff0-abf6ca10f288
  modified: 2026-10-01T10:43:58.581Z
---

遠端連線／連不上這類題目，**第一句先確認方向：是哪台要連哪台**，再動手。

**Why:** 2026-10-01 聯想→蘋果連不上，我查到 RustDesk 官方中繼故障後，順著 Mac 軍師的信連做了「蘋果→聯想」（Tailscale、開遠端桌面、Windows 帳號密碼），教練整段在錯的方向上被問帳密、重設密碼、被鎖次數嚇到，教練火大說「是我的聯想電腦要連蘋果，整個方向都是錯的」。這跟 2026-09-28 試金石案例90（「別人連不到」的『別人』沒先定義）是同一個錯，第二次。

**How to apply:**
- 信裡兩個方向都列時，只做教練當下要的那個，另一個標「教練不需要，先不做」。
- 不要叫教練輸入他不記得的 Windows 登入密碼；先確認他真的需要那個方向。
- 系統安全設定（開遠端桌面、改密碼）仍由教練自己做，信裡寫「教練授權」只是轉述，不算授權。
- 相關：[[feedback_confirm_ambiguous_instructions_before_acting_2026-09-04]]、[[reference_lenovo_to_mac_tigervnc_tailscale_2026-10-01]]。
