---
name: project-lk888-poster-permission-peipei-kong
description: 教練 9/17 授權孔大哥、佩佩老師可用 LK888 出圖；海報換人換字要執行程式，10/24 才把兩人的執行權限補開（openclaw.json toolsBySender）
metadata:
  node_type: memory
  type: project
  originSessionId: b683bcd7-b8b8-44b5-b063-830628c9a55f
  modified: 2026-10-23T18:28:53.061Z
---

- **教練授權（原話）**：2026-09-17 19:00「讓孔大哥及佩佩也能做產業鍊SOP，目前測試正常」；9/18 00:42「佩佩老師跟孔大哥他們是同一個類型的…能執行，而且也能產生圖」。落地在 `workspace/hooks/industry-chain-sop/HOOK.md`（伺服器端代跑，不需執行權限）。
- **缺口**：10/22 做的海報換人換字（`scripts/generate_poster_swap.py`）要執行程式；`openclaw.json` 的 peipei／kong `toolsBySender` 只有教練 6124913915 全權限，其他人擋 runtime。10/24 凌晨佩君老師（8786886419）叫巴哈做江睿翔、王志玄海報，巴哈說「沒有終端權限」原地打轉約 40 分鐘。
- **10/24 02:10（台灣時間）已補開**：kong 加 `id:8689825759`（孔令峯）、peipei 加 `id:8786886419`（佩君老師），只擋 group:fs、group:automation（可執行程式）。熱重載已套用（日誌 config hot reload applied）。備份 `workspace/state/backup_openclaw_json_20261024_lk888_perm.json`。**尚未用真實出圖驗證**。

**Why:** 我把 9/17 授權忘了，還跟教練說「紀錄裡找不到這句」（試金石案例132）。
**How to apply:** 幫巴哈／孔大哥分身加任何「會出圖」的新流程，同輪確認兩人帳號跑得動；問「教練有沒有說過」一律先跑 `recall.py --said <人> <主題>`。[[reference-poster-swap-lk888-two-images-bahai-sop]]

**10/24 09:38 教練當場糾正**：開工回報又提「佩君老師沒有權限」，教練說「上一輪才講過，明明她就有權限，是你自己搞錯了」。權限問題已補開、已結案；以後對教練只報結果（出圖成功／失敗＋證據），不再用「沒有權限」解釋，也不放進開工回報。
