---
name: reference-wu-shang-qian-swap-old-svg-slots-hero-reframe-token-cost-2026-10-30
description: 吳尚謙頁(wu-shang-qian)換 AI 圖：舊頁位置是 svg data-img-id 要先轉成 img data-slot 再跑 swap 腳本；主視覺臉被拱形框切到→補邊縮小右移重製；換圖流程 token 實測約 1.1～3.5 萬
metadata:
  node_type: memory
  type: reference
  originSessionId: bff5e1f5-571c-46e1-85a4-40e2929938d6
  modified: 2026-10-30T06:08:24.207Z
---

教練 10/30 13:41 說吳尚謙頁在 data-slot 規則之前就做好，要比照林晃誼流程換圖並算 token。實測（commit：換圖 `c7cf7ff`、主視覺 `00970f1`，repo `~/github_repos/wu-shang-qian`，網頁在 `https://coach1973.github.io/wu-shang-qian/`，推完約 1～2 分鐘才更新）：

- **舊頁位置認法**：`<div class="ph"><svg … data-img-id="IMG-001">…</svg></div>`。`swap_slot_images.py` 不認，所以先用 python 把 svg 換成 `<img data-slot="IMG-001" src="空白gif" alt="AI 繪製…">`，再跑原腳本（沒改腳本）。腳本會把 `~/.openclaw/media/outbound` 裡每個 IMG-00N 最新一張都試，別頁的舊圖（如林晃誼 IMG-004）因找不到位置不會誤換，但要看輸出確認。
- **IMG-003 這類「實景修飾」真人照片不自動換**，先請教練看。
- **主視覺臉被切（教練 14:03 糾正）**：`.portrait .frame` 拱形半徑 240px 但寬只有約 420px，CSS 夾成 210px 半圓，圓角切到貼左上的臉。做法：用 PIL 把原圖左、上用邊緣延伸＋高斯模糊補邊並淡出到背景色（13,12,16）、縮約 14% 靠右下，輸出 1047×1501（比例＝框 3:4.3），`object-position:50% 50%`。先用 PIL 模擬拱形框看過再上線；不用 CSS 縮放，因為縮小會露出照片左邊被切的外套硬邊。
- **token 實測**（解析 session jsonl 的 usage）：讀完圖→換圖→push 約 1.1 萬；到 push 約 3.1 萬；含驗證約 3.5 萬新 token；另每輪重讀對話 cache 約 190 萬。頁面有 data-slot 的話約 1 萬。**Why:** 教練只想知道數字、不當搬運工。**How to apply:** 教練問 token 就用 session jsonl 的 usage 量，講「新進＋我寫出」與 cache 分開，別拿估的。

相關：[[reference_swap_slot_images_after_publish_flow_2026-10-30]]、[[feedback_verify_only_changed_element_one_screenshot_2026-10-27]]

- **教練 14:08 新需求（未做）：圖片上傳策展中心後自動壓到清晰但最輕。** 已查到：`optimize_site_assets.py` 只處理獨立圖檔（>100KB、長邊2000、webp q82），不處理內嵌 base64；吳尚謙頁內嵌98張解開3.69MB、base64後4.92MB，重壓長邊1200/q75只省10%、900/q70省23%；更有效推論是拆成獨立檔＋延遲載入（未證實），要先定方向。接力棒下一場第2項。
