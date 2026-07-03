# 軍師接力棒 · 2026-07-03 v43（Mac 終端機 Sonnet，session 收尾）

> 建立時間：2026-07-03 下午 1:30（台灣時間）
> 本棒執行者：Mac 終端機軍師 Sonnet 5
> 上一棒：v42（2026-07-03 上午7:30，logo裁切最終修好上線+試金石案例38完整檢討）
> 本棒主軸：**新增時間鎖機關 + session總結收尾**（教練要開新視窗）

---

## 🎯 本場最終戰果總覽（延續v41~v43三棒同一場session）

### 1. ✅ 講座系列行銷頁定案上線
- GitHub Pages：https://coach1973.github.io/bigtree/speakers-2026/
- bymyway正式版：https://www.bymyway.com/bigtree/（自動站SOP首次零空白零表頭殘留一次上線）
- 詳見記憶檔 `project_speakers2026_bigtree_launch.md`

### 2. 🔴🔴🔴 試金石案例38：logo裁切debug血淚（54分54秒、10則訊息、9次修改）
教練親口三問（為何不自己先看/為何要人工幫看左右/自己有沒有審美）逐條誠實回答寫進案例庫。核心教訓：`preview_eval`讀DOM數字不能替代截圖，工具本身視窗異常/CSS快取會讓數字失真但看似精確。詳見記憶檔 `feedback_visual_change_screenshot_not_dom_numbers.md`。

### 3. 🔴🔴 案例38查證過程中又犯UTC未轉台灣時間（同一場對話裡的第二次翻車）
查timestamp算耗時沒錯，但口頭報時間軸給教練時把UTC原始小時數字當台灣時間講，教練當場抓到。**新建機關**：`scripts/rule_taiwan_time_check.sh`（Stop hook，commit `64e28e6a`）——事後偵測「這輪讀過UTC timestamp+回覆有時鐘數字+沒講台灣時間」三條件成立就exit 2強制重做。8/8測試通過。已在 `settings.json` Stop hooks 陣列註冊生效。

---

## 📋 下一棒待辦

| 優先 | 對象 | 任務 |
|------|------|------|
| 🟡 | 下一棒軍師 | 建立案例38提到的「視覺類改動送出前截圖確認」Stop hook（比照今天新建的 `rule_taiwan_time_check.sh` 模式），把「preview_eval不能替代截圖」也系統化成機關，不只是記憶檔 |
| 🟢 | 下一棒軍師 | 教練說「如果bigtree效果更好，之後改成COACH」——等教練決定是否要把 `bymyway.com/coach/` 也換成這個新版黑金風格內容 |
| 🟢 | 下一棒軍師 | `bymyway.com/bigtree/` 分頁標題「– 大樹教育顧問」後綴是否要拿掉，等教練回覆 |
| 🟢 | 下一棒軍師 | speakers-2026事件卡部分場次標「時間確認中」，等教練補實際時段；OG meta+site_icon若要分享連結出去也需要照SOP步驟9補上 |
| 🟢 | 下一棒軍師 | 新建的 `rule_taiwan_time_check.sh` 剛上線，還沒經過真實對話驗證有無誤報，運作幾天後回頭檢查 `distill/rule_taiwan_time_violations.log` |

---

## 🔑 本場關鍵記憶檔案索引

- `project_speakers2026_bigtree_launch.md` — 講座頁上線全貌
- `feedback_visual_change_screenshot_not_dom_numbers.md` — 視覺類任務必截圖鐵律
- `feedback_taiwan_time_always.md`（補充）— 時間鎖N+1次違反+新機關
- `試金石/試金石_案例庫.md` 案例38 — 完整debug血淚過程+教練三問逐條回答

---

> Mac 終端機軍師 Sonnet 5 親筆，2026-07-03 下午1:30台灣時間。教練要開新對話視窗，本棒收尾。
