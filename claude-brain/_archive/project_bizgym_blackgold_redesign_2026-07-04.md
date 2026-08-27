---
name: project-bizgym-blackgold-redesign-2026-07-04
description: 商務健身房(biz-gym)網站黑金風格改版進度，10個section已套用但還沒推上線
metadata: 
  node_type: memory
  type: project
  originSessionId: 235960d2-ceaf-4f60-9d5d-6261adca7f0b
---

教練嫌棄 biz-gym（海餅乾俱樂部・商務健身房，`coach1973.github.io/bigtree/biz-gym/`）原本米杏色+橘棕色風格「沒質感」，字太小太虛，要求重新設計。

## 定案結果（教練 2026-07-04 拍板）
- **風格**：延續 bymyway 首頁/講座頁同一套黑金系統（`--gold:#c8a96e`、`--dark:#0a0a0a` 三階層背景），不是另創新風格
- **字體**：全站統一 **Noto Sans TC 粗黑體**（拿掉原本混用的 Noto Serif TC），純白實色（不用半透明），字級全面拉大到 18-21px 地板（不再有小到看不清楚的次要文字）
- 曾經測試過 LXGW WenKai TC（霞鶩文楷手寫楷體）當替代方案，教練最終選標準黑體不選它
- 文案修正：「台南最優質商務團隊創辦人/主理人」→「最優質商務團隊的幕後推手」（教練覺得事業不只在台南），全站4處都改了

## 目前狀態（尚未上線，等教練說「推」）
- 正式檔案 `biz-gym/index.html` 本機已經是新版（10個section全套用，逐段截圖驗證過），舊版備份在 `index.html.bak-before-blackgold-20260704-0157`
- 還沒 commit、沒 push，線上 `coach1973.github.io/bigtree/biz-gym/` 還是舊版
- 本機還留著幾個過程檔案沒清（`mockup-blackgold.html`、`option-A/B/C-*.html`、`mockup-font-compare.html`、`index-new-blackgold.html`），是設計過程的存檔，教練拍板後可以清掉

## Why
教練自我定位是「大樹教練的作品」，質感等於品牌信任度；黑金風格已經是 bymyway.com 首頁+講座頁的正典，商務健身房延用可以維持品牌一致性，不要三套風格各自為政。

## How to apply
下一場 session 開工，若教練提到「商務健身房」「biz-gym」，先確認是否已經說「推」——沒有的話帶他看本機預覽，不要自己假設已核准就 push。
相關：[[feedback_web_push_sop]]、[[feedback_coach_deploy_vocabulary]]
