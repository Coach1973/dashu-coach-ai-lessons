# 交接棒：商務健身房網站 → Lenovo Claude

**時間：** 2026-06-30  
**來自：** ACER Claude（claude-opus-4-7）  
**交給：** Lenovo Claude  
**任務狀態：** 進行中（修改迭代階段）

---

## 一、主要任務

幫大樹教練做「**海餅乾俱樂部・商務健身房**」招募落地頁。

**策略方向（教練親口）：**
- 這個網站是一張「**戰略地圖**」，或稱「遊戲攻略」
- **公開所有規則**，讓所有人看到一致性的答案
- 教練信心不怕人學，因為能不能執行靠的是「執行者是否堅信這套標準」
- **去 BNI 化**：網站不提 BNI 平台名稱，等面談自然知道
- 強調「**最優質的商務團隊**」

---

## 二、檔案位置

| 用途 | 路徑 |
|------|------|
| 主來源檔 | `C:\Users\Administrator\Documents\biz-gym\index.html` |
| 桌面預覽資料夾 | `D:\Users\Desktop\商務健身房_預覽\` （含 index.html, coach-hero.jpg, line-qr.png）|
| 線上版（已上線 v2）| https://coach1973.github.io/bigtree/biz-gym/ |

**⚠️ 現在是修改迭代階段，不要 push，桌面預覽給教練看就好。**  
教練說「上線」「推上去」才 commit + push。

---

## 三、網站結構（10 sections）

1. **NAV** — 固定頂欄 + 漢堡選單
2. **HERO** — 主視覺，含英雄圖（coach-hero.jpg），有「公開所有規則」宣言
3. **認知翻轉** — 「付了會費，只是買到進門的權利」
4. **為什麼是大樹教練** — 品牌數據卡片區（見下方正確數字）
5. **海餅乾正典** — 照抄，CC BY-ND 4.0，一字不改
6. **六大商務器材** — 6 張工具卡
7. **當責方程式** — 「夢想 + 承諾 + 計畫 + 當責 = 轉化」
8. **下次見面會** — 目前是 placeholder「即將公告」（待教練給日期）
9. **FAQ** — 常見問答
10. **90 分鐘 CTA** — 報名 modal + LINE 連結

---

## 四、正確品牌數據（只信這份，不准上網查）

| 項目 | 正確值 |
|------|--------|
| 職銜 | 大台南市區執行董事 |
| 培訓年資 | 26 年 |
| 演講場次 | 6,000+ 場 |
| 足跡 | 台灣、中國、馬來西亞、汶萊（四國）|
| 海餅乾創始 | 2007 年 |
| 商務健身房會員 | 100 位企業家 |
| 年產值 | 5 億 |
| LINE 官方帳號 | @qaw8118h |
| LINE 連結 | https://line.me/R/ti/p/@qaw8118h |

---

## 五、Modal 報名表單設定

- **POST URL：** `https://sme-register-fn.netlify.app/.netlify/functions/register`
- **SESSION_NAME：** `'海餅乾俱樂部・商務健身房 90 分鐘認知翻轉會議'`
- **LINE_REGISTRATION_URL：** `'https://line.me/R/ti/p/@qaw8118h'`
- 送出成功後開新分頁 → LINE @qaw8118h

---

## 六、海餅乾正典（照抄規則）

CC BY-ND 4.0，**一字不改，不准改寫、不准優化、不准簡化**。  
原文在 `biz-gym/index.html` 的 `#hbc-canon` section 內，照用。

---

## 七、已確認去除的元素

以下絕對不能出現（已全部清除，grep 確認 0 matches）：
- `BNI`
- `Phil Berg`
- `Power Team`
- `大台南南區`（錯誤職銜）
- `@hqh8897h`（錯誤 LINE ID）

---

## 八、尚未完成的內容

1. **下次見面會**（#upcoming-session section）— 目前顯示「即將公告」，等教練提供：
   - 下次見面日期、時間、地點
   - 費用（或免費）
   - 名額
   
2. **教練的思想與 BNI 系統**內容還需要補充（教練說還要完善）

3. **見面會報名流程** 是直接點 CTA 還是 modal 另設一個「見面會報名」待確認

---

## 九、工作規則（關鍵）

1. **修改後同步桌面預覽**，不 push
2. **桌面預覽路徑：** `D:\Users\Desktop\商務健身房_預覽\`
3. 教練說「推上去」才 push 到 GitHub Pages
4. GitHub repo：`Coach1973/bigtree`，子目錄 `biz-gym/`

---

## 十、記憶索引

- `feedback_local_preview_before_push.md` — 修改階段先本地預覽
- `feedback_no_improvise_when_copying.md` — 照抄不擅自優化  
- `user_coach_brand_data.md` — 品牌數據唯一真相
- `feedback_dont_guess_coach_data_from_web.md` — 不准上網查教練資料

---

**下一步：** 等教練打開桌面預覽 `D:\Users\Desktop\商務健身房_預覽\index.html` 後，告訴你要改什麼，依指示修改並更新桌面預覽。
